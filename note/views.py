from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from helper import clean_text
from .models import Folder, Note


class Home(View):
    def get(self, request):
        folders = request.user.folders.filter(parent=None)
        notes = request.user.notes.filter(folder=None)
        return render(request, 'note/home.html', {'folders': folders, 'notes': notes})


class AddFolder(View):
    def get(self, request, parent_id=None):
        if parent_id != None:
            parent = request.user.folders.get(id=parent_id)
        else:
            parent = None
        
        folders = request.user.folders.all()
        return render(request, 'note/add-folder.html', {'folders': folders, 'parent': parent})
    
    def post(self, request):
        name = request.POST['name']
        parent = clean_text(request.POST.get("parent", None))
        
        folder = Folder.objects.create(name=name, parent_id=parent, user=request.user)
        
        return redirect(reverse('folder-detail', kwargs={'id': folder.id}))


class EditFolder(View):
    def get(self, request, id):
        folder = request.user.folders.get(id=id)
        return render(request, 'note/add-folder.html', {'folder': folder})
    
    def post(self, request, id):
        name = request.POST['name']
        parent = request.POST.get("parent", None)
        
        folder = request.user.folders.get(id=id)
        folder.name = name
        folder.parent = parent
        folder.save()
        
        return redirect(reverse('folder-detail', kwargs={'id': folder.id}))


class FolderDetail(View):
    def get(self, request, id):
        folder = request.user.folders.get(id=id)
        folders = folder.folders.all()
        notes = folder.notes.all()
        return render(request, 'note/folder-detail.html', {'folder': folder, 'folders': folders, 'notes': notes})


class AddNote(View):
    def get(self, request, folder_id=None):
        if folder_id != None:
            folder = request.user.folders.get(id=folder_id)
        else:
            folder = None
        
        folders = request.user.folders.all()
        return render(request, 'note/add-note.html', {'folders': folders, 'folder': folder})
    
    def post(self, request):
        title = clean_text(request.POST.get('title', None))
        content = clean_text(request.POST.get('content', None))
        folder = request.POST.get('folder', None)
        
        if folder != None and folder != 'None':
            folder = request.user.folders.get(id=folder)
        else:
            folder = None
        
        if title == None and content == None:
            raise Exception('title == None and content == None')
        
        if title == None:
            title = ''
        
        note = Note.objects.create(title=title, content=content, folder=folder, user=request.user)
        
        return redirect(reverse('note-detail', kwargs={'id': note.id}))


class EditNote(View):
    def get(self, request, id):
        note = request.user.notes.get(id=id)
        return render(request, 'note/add-note.html', {'note': note})
    
    def post(self, request, id):
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        folder = request.POST.get('folder', None)
        
        if title == None and content == None:
            raise Exception('title == None and content == None')
        
        note = request.notes.get(id=id)
        note.title = title
        note.content = content
        note.folder = folder
        note.save()
        
        return redirect(reverse('note-detail', kwargs={'id': note.id}))


class NoteDetail(View):
    def get(self, request, id):
        note = request.user.notes.get(id=id)
        folder = note.folder
        return render(request, 'note/note-detail.html', {'note': note, 'folder': folder})


class ChangeDirection(View):
    def get(self, request, dir):
        # request.cookie
        # request.cookies
        # request.COOKIE
        request.COOKIES
        request.session
        # request.sessions
        # request.SESSION
        # request.SESSIONS
        # request.COOKIES['dir'] = dir
        request.COOKIES.get('key') # ['key']
        request.session['key'] = 'value'
        
        #
        response = HttpResponse(dir)
        response.set_cookie('dir', dir)
        
        return response


def hierarchy_folders(request):
    folders = request.user.folders.filter(parent=None).order_by('created_dt')
    return render(request, 'note/hierarchy-folders.html', {'folders': folders})
    # return HttpResponse(str([folder.name for folder in folders]))


def go_to_parent_folder(request, id):
    folder = request.user.folders.get(id=id)
    
    if folder.parent == None:
        return redirect(reverse('home'))
    
    folder_id = folder.parent.id
    return redirect(reverse('folder-detail', kwargs={'id': folder_id}))
