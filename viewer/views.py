from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    selected_drive = "google_drive"    #google_drive, dropbox, one_drive
    context = {"selected_drive": selected_drive,}
    return render(request, 'viewer/index.html', context)


def change_cloud(request):
    cloud_name = request.POST.get('cloud_name')
    context = {"selected_drive": cloud_name,}
    return render(request, 'viewer/index.html', context)
