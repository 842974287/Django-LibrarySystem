# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class List(models.Model):
    Id = models.IntegerField(primary_key = True, verbose_name = u'ID')
    Name = models.CharField(max_length = 20, verbose_name = u'姓名')
    Telephone = models.CharField(max_length = 15, verbose_name = u'手机号码')
    TimeOne = models.CharField(max_length = 300, verbose_name = u'6月24日 周六10:10-11:40')
    TimeTwo = models.CharField(max_length = 300, verbose_name = u'6月27日 周二早上3-4节')
    TimeThree = models.CharField(max_length = 300, verbose_name = u'7月2日 周日14:00-17:00')
    TimeFour = models.CharField(max_length = 300, verbose_name = u'7月4日 周二9:00-11:00')
    TimeFive = models.CharField(max_length = 300, verbose_name = u'7月8日 周六10:10-11:40')
    TimeSix = models.CharField(max_length = 300, verbose_name = u'7月9日 周日08:30-10：00')
    TimeSeven = models.CharField(max_length = 300, verbose_name = u'7月11日 周二早上3-4节')
    TimeEight = models.CharField(max_length = 300, verbose_name = u'7月16日 周日08:30-10:00')

    def __unicode__(self):
        return str(self.Id) + '_' + self.Name
