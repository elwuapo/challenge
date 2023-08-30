from django.db import models

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    status    = models.CharField(max_length=10)
    filename  = models.CharField(max_length=256, default='')
    path      = models.CharField(max_length=256, default='')
    url       = models.CharField(max_length=256, default='')


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=256, default='')
    email     = models.EmailField(max_length=256, default='')

class Punch(models.Model):
    punch_id   = models.AutoField(primary_key=True)
    type       = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    punch_time = models.DateTimeField(null=True, blank=True, default=None)
    person     = models.ForeignKey('Person', on_delete=models.CASCADE)