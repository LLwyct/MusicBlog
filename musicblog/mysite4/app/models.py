# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import random
# Create your models here.
class essay(models.Model):
    title = models.CharField(max_length=128,blank=False,null=False)
    auther = models.CharField(max_length=50,blank=False,null=False)
    creatdate = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    platform = models.CharField(max_length=128)
    link = models.CharField(max_length=2048,blank=False,null=False)
    like = models.IntegerField(default=0)
    comment = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    popular = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    lable = models.CharField(max_length=128,default='')
    def __str__(self):
        return self.title

class like(models.Model):
    user = models.CharField(max_length=128)
    essayid = models.IntegerField()

class isopen(models.Model):
    user = models.CharField(max_length=128)
    essayid = models.IntegerField()

class comment(models.Model):
    essayid = models.IntegerField()
    user = models.CharField(max_length=128)
    commentcontent = models.CharField(max_length=1024)
    commentdate = models.DateTimeField(auto_now_add=True)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','creatdate','id')

admin.site.register(essay, BlogPostAdmin)

class BlogPostAdmin2(admin.ModelAdmin):
    list_display = ('essayid','user','commentcontent','commentdate')

admin.site.register(comment,BlogPostAdmin2)

class BlogPostAdmin3(admin.ModelAdmin):
    list_display = ('essayid','user')
admin.site.register(like,BlogPostAdmin3)