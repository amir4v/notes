from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    
    path('add-folder/', views.AddFolder.as_view(), name='add-folder'),
    path('add-folder/<int:parent_id>/', views.AddFolder.as_view(), name='add-folder'),
    path('edit-folder/<int:id>/', views.EditFolder.as_view(), name='edit-folder'),
    
    path('folder/<int:id>/', views.FolderDetail.as_view(), name='folder-detail'),
    
    path('add-note/', views.AddNote.as_view(), name='add-note'),
    path('add-note/<int:folder_id>/', views.AddNote.as_view(), name='add-note'),
    path('edit-note/<int:id>/', views.EditNote.as_view(), name='edit-note'),
    
    path('note/<int:id>/', views.NoteDetail.as_view(), name='note-detail'),
    
    path('change-direction/<str:dir>/', views.ChangeDirection.as_view(), name='change-direction'),
    
    path('hierarchy-folders/', views.hierarchy_folders, name='hierarchy-folders'),
    
    path('go-to-parent-folder/<int:id>/', views.go_to_parent_folder, name='go-to-parent-folder'),
]
