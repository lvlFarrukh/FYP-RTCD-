from django.db import models
import datetime

# Create your models here.

def upload_location(instance, filename):
    extension = filename.split('.')[1]
    return f"backend_site/dataset_suspected/{instance.id}_0.{extension}"

class controller_user(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    cnic = models.BigIntegerField()
    image = models.ImageField(upload_to='backend_site/controller_user')
    password = models.CharField(max_length=15)
    user_type = models.BooleanField(default=0)
    status = models.BooleanField(default=0)

    def __str__(self):
        return self.name

# Suspect persons models

class suspect_person_detail(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="unknown")
    last_name = models.CharField(max_length=100, default="unknown")
    gender = models.CharField(max_length=100, default="unknown")
    cnic = models.BigIntegerField(default=0)
    address = models.CharField(max_length=300, default="unknown")
    education = models.CharField(max_length=300, default="unknown")
    marital_status = models.CharField(max_length=100, default="unknown")
    age = models.IntegerField(default=0)
    date_of_birth = models.DateField(default="2050-01-01")
    nationalilty = models.CharField(max_length=100, default="unknown")
    entry_date = models.DateTimeField(default=datetime.datetime.now())
    status = models.BooleanField(default=0)
    image = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return f"id: {self.id}, Date: {self.entry_date}"
