from django.db import models

class Devices_details(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=255)
    device_details = models.CharField(max_length=255)
    device_status = models.IntegerField()

    class Meta:
        db_table = 'Devices_details'

class Data_store(models.Model):
    id = models.AutoField(primary_key=True)
    device_values = models.IntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    device_id = models.IntegerField()
    class Meta:
        db_table = 'Data_store'

class Admin_details(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    class Meta:
        db_table = 'Admin_details'