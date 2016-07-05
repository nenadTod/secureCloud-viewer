from django.shortcuts import render, redirect
from functools import wraps
from cloud_API.dropbox_API import DropboxAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.google_drive_API import GoogleDriveAPI
from django.views.decorators.csrf import csrf_protect
from SCCrytpo_API.SCDecryptor import SCDecryptor
import shutil

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
            request.session['folder_name'] = ""
            request.session['history'] = []
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

    images_per_page = 6
    dir_path = "viewer/static/user_data/"
    dir_path_view = "user_data/"

    history = request.session['history']
    if len(history[active_page - 1]) == 0:


        cloud_name = request.session.get('cloud_name')

        if cloud_name == 'google_drive':
            drive = GoogleDriveAPI()
            drive.authenticate()
        else:
            drive = request.session.get('drive')


        scd = SCDecryptor()
        folder_name, images, pages_no, images_no = scd.decryptShared(dir_path, dir_path_view,
                                                                     request.session['gallery_location'],
                                                                     drive,
                                                                     request.session['folder_name']
                                                                     , images_per_page, active_page)
        history[active_page - 1] = images
    else:
        images = request.session['history'][active_page - 1]

    request.session['current_page'] = int(active_page)
    request.session['current_images'] = images
    request.session['history'] = history
    context = get_context(request)
    return render(request, 'viewer/index.html', context)


@csrf_protect
@session_decorator
def change_cloud(request):
    cloud_name = request.POST.get('cloud_name')
    if cloud_name is not None:

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

        if (cloud_name != 'google_drive'):
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
        cloud_name = request.session.get('cloud_name')

        if cloud_name == 'google_drive':
            drive = GoogleDriveAPI()
            drive.authenticate()
        else:
            drive = request.session.get('drive')

        images_per_page = 6

        dir_path = "viewer/static/user_data/"
        dir_path_view = "user_data/"

        scd = SCDecryptor()
        folder_name, images, pages_no, images_no = scd.decryptShared(dir_path, dir_path_view,
                                                                     gallery_name, drive, ""
                                                                     , images_per_page, 1)

        request.session['gallery_location'] = gallery_name
        request.session['number_of_images'] = int(images_no)
        request.session['number_of_pages'] = int(pages_no)
        request.session['current_page'] = 1
        request.session['current_images'] = images
        request.session['folder_name'] = folder_name

        history = []
        for x in range(0, pages_no):
            temp = []
            history.append(temp)


        if len(images)> 0:
            history[0] = images

        request.session['history'] = history

    return redirect('index', permanent=True)


@csrf_protect
def close_session(request):
    folder = str(request.session['folder_name'])
    if folder != "":
        dir_path = "viewer/static/user_data/"

        shutil.rmtree(dir_path + folder)

    request.session.clear()
    return redirect('index', permanent=True)


def get_context(request):
    context = {
        "selected_drive": request.session['cloud_name'],
        "cloud_user": request.session['user_username'],
        "folders_list": request.session['cloud_galleries'],
        "selected_gallery": request.session['gallery_location'],
        "images_number": request.session['number_of_images'],
        "total_pages": request.session['number_of_pages'],
        "active_page": request.session['current_page'],
        "images_list": request.session['current_images'],
    }
    return context
