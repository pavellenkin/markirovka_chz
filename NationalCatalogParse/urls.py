"""
URL configuration for NationalCatalogParse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from remark.views import remark
from ordering_economic.views import ordering_economic
from main.views import *
from dispenser_tasks.views import *
from invent.views import invent
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from settings.views import settings, certs, models, service, export, safe_download_tsd_file
from django.conf.urls import include
from settings import views


urlpatterns = [
path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', main_menu),
    path('natcat/', header_mainapp),
    path('ps_in_code/', post_input_code),
    path('st/',st),
    path('invent/',invent),
    path('nc_find/',nc_find),
    path('check_code/',check_code),
    path('change_date/',change_date),
    path('error_server/',error_server),
    path('error_not_found/',error_not_found),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('barcode.png'))),
    path('remark/',remark),
    path('read_code/',read_code),
    path('settings/',settings),
    path('certs/',certs, name='certs'),
    path('models/',models),
    path('service/',service),
    path('export/',export),
    path('ordering_economic/',ordering_economic),
    path('download/tsd/', safe_download_tsd_file, name='download_tsd'),
    path('articles/', views.articles_page, name='articles_page'),
    path('upload-articles/', views.upload_articles_file, name='upload_articles'),
    path('download-articles/', views.download_articles_file, name='download_articles'),
    path('download-template/', views.download_articles_template, name='download_template'),
    path('dispenser-tasks/', document_list, name='document_list'),
    path('create/', create_document_task, name='create_document_task'),
    path('documents/status/<str:doc_id>/', get_document_status, name='get_document_status'),
    path('documents/failed/<str:doc_id>/', get_document_failed, name='get_document_failed'),
    path('documents/delete/<str:doc_id>/', delete_document, name='delete_document'),
    path('documents/download/<str:doc_id>/', download_document, name='download_document'),
    path('documents/api/<str:doc_id>/', document_api, name='document_api'),
    path('certs/set-active/', views.set_active_cert, name='set_active_cert'),
    path('clear-tsd-file/', views.clear_tsd_file, name='clear_tsd_file'),
    path('check-tsd-file/', views.check_tsd_file, name='check_tsd_file'),

]

