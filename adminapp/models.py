from django.db import models

# Create your models here.

class admin_reg(models.Model):
    Firstname=models.CharField(max_length=200,null=True)
    Lastname=models.CharField(max_length=100,null=True)
    Address=models.CharField(max_length=500,default="a")
    DOB=models.CharField(max_length=200,null=True)
    Email=models.CharField(max_length=200,null=True)
    Password=models.CharField(max_length=200,null=True)
    confirmPassword=models.CharField(max_length=200,null=True)
    img=models.ImageField(upload_to='uimg',null=True)
    def __str__(self) :
        return self.Firstname
class Result(models.Model):
    result=models.BooleanField(default=False)


class time_set(models.Model):
    start=models.BooleanField(default=False)
    end=models.BooleanField(default=False)
   
    