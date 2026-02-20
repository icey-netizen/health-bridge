from django.db import models

# Create your models here.
class Patient(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    medicalhistory = models.TextField()


  
  