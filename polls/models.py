from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Countries(models.Model):
    name=models.CharField(max_length=100, blank=True)
class Cities(models.Model):
    country=models.ForeignKey(Countries,related_name="country_name", on_delete=models.CASCADE)
    name=models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    gender=models.CharField(null=True,max_length= 200)
    age=models.IntegerField(null=True, default=0)
    countries=models.ForeignKey(Countries, related_name="country", on_delete=models.CASCADE,null=True)
    cities=models.ForeignKey(Cities, related_name="city", on_delete=models.CASCADE,null=True)
    company=models.CharField(null=True,max_length= 200)


class Product(models.Model):
    name=models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
class SalesProduct(models.Model):
    user=models.ForeignKey(User, related_name="user_sales", on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(null=True, blank=True)
    sales_number=models.IntegerField(null=True, default=0)
    revenue= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product=models.ForeignKey(Product,related_name="product_name", on_delete=models.CASCADE)

class AuditModel(models.Model):
    """ Base Model for all models, providing insertion and updating timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BlackListedToken(AuditModel):
    token = models.TextField()

    def __str__(self):
        return self.token