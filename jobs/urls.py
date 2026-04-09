from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.table_browser, name='table_browser'),
    path('edit/filters/', views.active_filters, name='active_filters'),
    path('edit/<slug:slug>/', views.edit_markdown, name='edit_markdown'),
]
