from django.db import models
import datetime


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
    status = models.IntegerField(default=0)
    description = models.CharField(max_length=2000, default="unknown")
    image = models.ImageField(upload_to=upload_location)
    
    def __str__(self):
        return f"id: {self.id}, Date: {self.entry_date}"

class app_user(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="unknown")
    last_name = models.CharField(max_length=100, default="unknown")
    email = models.EmailField(unique=True, max_length=200, default="unknown")
    password = models.CharField(max_length=50, default='not set')
    gender = models.CharField(max_length=100, default="unknown")
    cnic = models.BigIntegerField(default=0, unique=True)
    address = models.CharField(max_length=300, default="unknown")
    date_of_birth = models.DateField(default="2050-01-01")
    phone_number = models.BigIntegerField(default=0)
    registration_date = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"id: {self.id}, cnic: {self.cnic}"

class suspect_from_app_User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(app_user, on_delete=models.CASCADE)
    video_url = models.URLField(max_length=200)
    description = models.CharField(default="unknown", max_length=600)
    report_date = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=0)

    def __str__(self):
            return f"id: {self.id}, Report Data: {self.report_date}"

class suspect_from_anonymous(models.Model):
    id = models.AutoField(primary_key=True)
    video_url = models.URLField(max_length=200)
    description = models.CharField(default="unknown", max_length=600)
    report_date = models.DateTimeField(default=datetime.datetime.now())
    status = models.IntegerField(default=0)

    def __str__(self):
        return f"id: {self.id}, Report Data: {self.report_date}"




