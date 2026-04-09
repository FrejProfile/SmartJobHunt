from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.table_browser, name='table_browser'),
    path('api/scrape/', views.scrape_jobs, name='scrape_jobs'),
    path('api/delete/', views.delete_jobs, name='delete_jobs'),
    path('edit/filters/', views.active_filters, name='active_filters'),
    path('edit/<slug:slug>/', views.edit_markdown, name='edit_markdown'),
]
