from django.db import models

class inventory(models.Model):
    login_id=models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    price = models.IntegerField()
    starting_inventory= models.IntegerField()
    supplier_id=models.IntegerField()
    inventory_received = models.IntegerField(default=0)
    inventory_shipped = models.IntegerField(default=0)    
    current_inventory = models.IntegerField(default=0)
    minimum_required = models.IntegerField(default=0)
class suppliers(models.Model):  
    login_id=models.CharField(max_length=100)
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    supplier_name = models.CharField(max_length=100)
class orders(models.Model):
    login_id=models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    product_id = models.IntegerField()
    number_shipped = models.IntegerField()
    order_date = models.CharField(max_length=100)
class purchases(models.Model):
    login_id=models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    product_id = models.IntegerField()
    number_received = models.IntegerField()
class to_order(models.Model):
    login_id=models.CharField(max_length=100)
    supplier_id = models.IntegerField()
    model_number = models.CharField(max_length=100)
    number = models.IntegerField()