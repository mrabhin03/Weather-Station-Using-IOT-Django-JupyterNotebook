from django.db import models

class Devices_details(models.Model):
    devices_id = models.AutoField(primary_key=True)
    Device_name = models.CharField(max_length=255)
    Device_Details = models.CharField(max_length=255)
    Device_status = models.IntegerField()

    class Meta:
        db_table = 'Devices_details'

class ev_data_store(models.Model):
    main_id = models.IntegerField(primary_key=True)
    values = models.IntegerField()
    DateTime = models.DateTimeField(auto_now_add=True)
    devices_id = models.ForeignKey(Devices_details, on_delete=models.CASCADE, related_name='ev_data_store')
    class Meta:
        db_table = 'ev_data_store'
