from django.db import models
import datetime

    
class Owner(models.Model):
    
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Animal(models.Model):
    
    name = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    kingdom = models.CharField(max_length=100)
    phylum = models.CharField(max_length=100)
    t_class =models.CharField(max_length=100)
    order = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    geographic_location = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    location_published = models.CharField(max_length=200)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " " + self.owner

    