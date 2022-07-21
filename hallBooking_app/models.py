from xml.dom.pulldom import default_bufsize
from django.db import models
from user_app.models import User
# Create your models here.

class ConfrenceHall(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    max_occupancy = models.IntegerField()
    booking_limit = models.IntegerField()
    isactive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class ConfrenceHallImages(models.Model):
    hall = models.ForeignKey(ConfrenceHall, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hall/images')
    
    def __str__(self):
        return "Hall " + self.hall + " Image"
    
class HallBookings(models.Model):
    def json_default1():
        return { "HOD": None, "AO": None, 'Employee': None}
    def json_default2():
        return { "HOD": None, "AO": None}
    start = models.DateTimeField()
    end = models.DateTimeField()
    participantcount =  models.IntegerField()
    hall = models.ForeignKey(ConfrenceHall, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255)
    submittedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.JSONField(default = json_default1)
    response = models.JSONField(default = json_default2)
    responseTime = models.JSONField(default = json_default1)
    isEditable = models.JSONField(default = json_default1)
    submittedAt = models.DateTimeField(auto_now_add=True)