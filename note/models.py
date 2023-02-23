from django.db import models
from django.conf import settings
from django.utils import timezone


class Folder(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='folders')
    
    created_dt = models.DateTimeField(auto_now_add=timezone.now)
    updated_dt = models.DateTimeField(auto_now=timezone.now)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')
    
    def children_in_li(self, folders=None):
        if self.folders.count() == 0:
            return ''
        if folders == None:
            folders = self.folders.all()
        
        result = '<ul>'
        for folder in folders:
            result += f'<li> \
                        <a href="/folder/{ folder.id }/" style="color: black; text-decoration: none;">{ folder.name }</a> \
                        </li>'
            if folder.folders.count() != 0:
                result += self.children_in_li(folder.folders.all())
        
        return result + '</ul>'
    
    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=64, null=True)
    content = models.CharField(max_length=1000, null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, related_name='notes')
    
    created_dt = models.DateTimeField(auto_now_add=timezone.now)
    updated_dt = models.DateTimeField(auto_now=timezone.now)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    # deadline = models.DateTimeField(null=True)
    
    def __str__(self):
        return f'{self.title[:32]}... {self.content[:32]}...'
