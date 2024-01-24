from django.db import models

# Create your models here.

class User_reg(models.Model):
    Firstname=models.CharField(max_length=200)
    Lastname=models.CharField(max_length=100)
    Address=models.CharField(max_length=500)
    Gender=models.CharField(max_length=500)
    State=models.CharField(max_length=20)
    District=models.CharField(max_length=500)
    Panchayat=models.CharField(max_length=200)
    DOB=models.CharField(max_length=200)
    Email=models.CharField(max_length=200)
    Password=models.CharField(max_length=200)
    confirmPassword=models.CharField(max_length=200)
    img=models.ImageField(upload_to='uimg')
    voteid=models.CharField(max_length=500,default="0")
    voterid=models.CharField(max_length=500,default="0")
    OTP=models.CharField(max_length=50,default=0)
    flag=models.BooleanField(default=False)

    def __str__(self) :
        return self.Firstname


