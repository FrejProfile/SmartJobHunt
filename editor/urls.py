from django.urls import path

from . import views

app_name = 'editor'

urlpatterns = [
    path('profile/', views.edit_profile, name='edit_profile'),

    # Competences — static paths before dynamic ones
    path('competences/', views.competences, name='competences'),
    path('competences/index/', views.edit_index, name='edit_index'),
    path('competences/create/', views.new_competence, name='new_competence'),
    path('competences/<str:category>/', views.edit_competence, name='edit_competence'),
    path('competences/<str:category>/create/', views.new_competence, name='new_sub_competence'),
    path('competences/<str:category>/<str:sub>/', views.edit_competence, name='edit_sub_competence'),

    # Cover letters
    path('letters/', views.cover_letters, name='cover_letters'),
    path('letters/<int:job_id>/', views.edit_cover_letter, name='edit_cover_letter'),
]
