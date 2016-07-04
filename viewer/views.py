from django.shortcuts import render, redirect
from django.http import HttpResponse
from functools import wraps
from cloud_API.dropbox_API import DropboxAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.google_drive_API import GoogleDriveAPI
import os
from django.views.decorators.csrf import csrf_protect
from SCCrytpo_API.SCDecryptor import SCDecryptor


def session_decorator(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        request = args[0]
        if 'cloud_name' not in request.session:
            request.session['cloud_name'] = ""
            request.session['user_username'] = ""
            request.session['cloud_galleries'] = {}
            request.session['gallery_location'] = ""
            request.session['number_of_images'] = 0
            request.session['number_of_pages'] = 0
            request.session['current_page'] = 0
            request.session['current_images'] = []
            request.session['drive'] = {}
        run = function(*args, **kwargs)
        return run
    return wrapped


@session_decorator
def index(request):
    context = get_context(request)
    return render(request, 'viewer/index.html', context)


@session_decorator
def open_page(request):
    active_page = request.GET.get('page_number')
    if not active_page:
        active_page = 1
    active_page = int(active_page)
    pages_no = int(request.session['number_of_pages'])
    if active_page < 1 or pages_no < active_page:
        active_page = 1

    # TODO get images on current page from cloud
    images = ['viewer/img/image1.jpg', 'viewer/img/image2.jpg', 'viewer/img/image3.jpg',
              'viewer/img/image4.jpg', 'viewer/img/image5.jpg', 'viewer/img/image6.jpg',
              'viewer/img/image7.jpg', 'viewer/img/image8.jpg', 'viewer/img/image9.jpg']

    request.session['current_page'] = int(active_page)
    request.session['current_images'] = images
    context = get_context(request)
    return render(request, 'viewer/index.html', context)


@csrf_protect
@session_decorator
def change_cloud(request):
    cloud_name = request.POST.get('cloud_name')
    if cloud_name is not None:

        user = "Micko"
        if cloud_name == 'google_drive':
            drive = GoogleDriveAPI()
        elif cloud_name == 'one_drive':
            drive = OneDriveAPI()
        else:
            drive = DropboxAPI()

        drive.authenticate()
        folders = drive.shared_with_me()

        folders.update(drive.list_subfolders())

        d, user = drive.get_user_data()

        request.session['drive'] = drive
        request.session['cloud_name'] = cloud_name
        request.session['user_username'] = user
        request.session['cloud_galleries'] = folders

    return redirect('index', permanent=True)


@csrf_protect
@session_decorator
def change_gallery(request):
    gallery_name = request.POST.get('gallery_name')
    if gallery_name is not None:

        cloud_name = request.session['cloud_name']
        if cloud_name == 'google_drive':
            drive = GoogleDriveAPI()
            drive.authenticate()
        else:
            drive = request.session.get('drive')

        dir_path = "viewer/static/user_data/"

        #drive.download_shared_file(gallery_name, 'meta1-de.txt', temp_dir)
        scd = SCDecryptor()
        ret_val = scd.decryptShared(dir_path, gallery_name, drive)


        # drive.download_file(gallery_name, 'slika.jpg', 'viewer/static/viewer/img')
        #drive.download_shared_file(gallery_name, 'meta1-de.txt', 'tu')
        #drive.download_file(gallery_name, 'test2.jpg', temp_dir)
        user_id = drive.get_user_id_by_folder_id(gallery_name)

        # TODO get number of images in selected folder
        images_no = 10
        # TODO get number of pages for this folder (single page contains 15 images)
        pages_no = 3
        # TODO get images for this folder
        images = ['user_data/tu/test2.jpg', 'viewer/img/image2.jpg', 'viewer/img/image3.jpg',
                  'viewer/img/image4.jpg', 'viewer/img/image5.jpg', 'viewer/img/image6.jpg',
                  'viewer/img/image7.jpg', 'viewer/img/image8.jpg', 'viewer/img/image9.jpg']

        request.session['gallery_location'] = gallery_name
        request.session['number_of_images'] = int(images_no)
        request.session['number_of_pages'] = int(pages_no)
        request.session['current_page'] = 1
        request.session['current_images'] = images

    return redirect('index', permanent=True)


@csrf_protect
def close_session(request):
    request.session.clear()
    return redirect('index', permanent=True)


def get_context(request):
    context = {
        "selected_drive": request.session['cloud_name'],
        "cloud_user": request.session['user_username'],
        "folders_list":  request.session['cloud_galleries'],
        "selected_gallery": request.session['gallery_location'],
        "images_number": request.session['number_of_images'],
        "total_pages": request.session['number_of_pages'],
        "active_page": request.session['current_page'],
        "images_list": request.session['current_images'],
    }
    return context
