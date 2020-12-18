from rest_framework import serializers
import datetime
from backend_site.models import suspect_from_app_User

class serializer_suspectData(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, default="unknown")
    last_name = serializers.CharField(max_length=100, default="unknown")
    gender = serializers.CharField(max_length=100, default="unknown")
    cnic = serializers.IntegerField(default=0)
    address = serializers.CharField(max_length=300, default="unknown")
    education = serializers.CharField(max_length=300, default="unknown")
    marital_status = serializers.CharField(max_length=100, default="unknown")
    age = serializers.IntegerField(default=0)
    date_of_birth = serializers.DateField(default="2050-01-01")
    nationalilty = serializers.CharField(max_length=100, default="unknown")
    entry_date = serializers.DateTimeField(default=datetime.datetime.now())
    status = serializers.IntegerField(default=0)
    description = serializers.CharField(max_length=2000, default="unknown")


