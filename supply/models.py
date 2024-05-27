from django.db import models

class Restaurant(models.Model):
    Restaurant_ID = models.IntegerField(primary_key=True)
    Restaurant_Name = models.CharField(max_length=50)
    Restaurant_Latitude = models.CharField(max_length=50)
    Restaurant_longitude = models.CharField(max_length=50)
    Restaurant_Rating = models.IntegerField()
    Food_available = models.IntegerField()

class Hotspot(models.Model):
    Hotspot_ID = models.IntegerField(primary_key=True)
    Hotspot_Name = models.CharField(max_length=50)
    Hotspot_Latitude = models.CharField(max_length=50)
    Hotspot_longitude = models.CharField(max_length=50)
    Food_needed = models.IntegerField()
    Satisfied = models.BooleanField(default=False)


class FoodRequest(models.Model):
    Restaurant_ID = models.IntegerField()
    Supplier_name = models.CharField(max_length=50)
    food_details = models.TextField()
    user_identifier = models.TextField()
    status = models.CharField(max_length=20, default='Pending')


    
