# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Book(models.Model):
    ISBN = models.CharField(max_length = 20, primary_key = True, verbose_name = u'ISBN')
    BookName = models.CharField(max_length = 100, verbose_name = u'书名')
    PublishingCompany = models.CharField(max_length = 100, verbose_name = u'出版社')
    Author = models.CharField(max_length = 100, verbose_name = u'作者')
    Storage = models.IntegerField(u'馆藏数量')
    Number = models.IntegerField(u'可借数量')
    IsAvailuable = models.BooleanField(u'是否可借')

    def __unicode__(self):
        return self.BookName + '_' + self.Author

class Reader(models.Model):
    GENDER_CHOICES = (
        (0, 'Unknown'),
        (1, 'Male'),
        (2, 'Female'),
    )
    ReaderId = models.CharField(max_length = 20, primary_key = True, verbose_name = u'读者Id')
    ReaderName = models.CharField(max_length = 20, verbose_name = u'姓名')
    Gender = models.IntegerField(default = 0, choices = GENDER_CHOICES, verbose_name = u'性别')
    MaxBook = models.IntegerField(default = 10, verbose_name = u'可借数量')
    Borrowed = models.IntegerField(default = 0, verbose_name = u'已借数量')
    Telephone = models.CharField(max_length = 15, verbose_name = u'联系电话')

    def __unicode__(self):
        return self.ReaderId + '_' + self.ReaderName

class BorrowList(models.Model):
    ListId = models.CharField(max_length = 50, primary_key = True, verbose_name = u'ID')
    Reader = models.ForeignKey(Reader)
    Book = models.ForeignKey(Book)
    BorrowDate = models.DateTimeField(auto_now_add = True, verbose_name = u'借出日期')
    DeadLine = models.DateTimeField(default = timezone.now() + timedelta(days = 20), verbose_name = u'归还日期')
    Panelty = models.IntegerField(default = 0, verbose_name = u'罚款')

    def __unicode__(self):
        return self.ListId
