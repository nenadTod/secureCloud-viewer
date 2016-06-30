from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = get_context()
    return render(request, 'viewer/index.html', context)

def open_page(request):
    active_page = request.GET.get('page_number')

    ## realy change page

    if not active_page:
        print('pao')
        active_page = 1

    context = get_context()
    return render(request, 'viewer/index.html', context)

def change_cloud(request):
    cloud_name = request.POST.get('cloud_name')

    ## realy change cloud

    context = get_context()
    return render(request, 'viewer/index.html', context)


def change_gallery(request):
    gallery_name = request.POST.get('gallery_name')

    ## realy change gallery

    context = get_context()
    return render(request, 'viewer/index.html', context)


def close_session(request):

    ## realy close session

    context = get_context()
    return render(request, 'viewer/index.html', context)


def get_context():
    context = {
        "selected_drive": "google_drive",
        "selected_gallery": "nothing",
        "active_page": 7,
        "total_pages": 42,
    }
    return context
