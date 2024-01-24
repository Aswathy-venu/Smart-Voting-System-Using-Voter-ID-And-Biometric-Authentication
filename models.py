from django.db import models

# Create your models here.

class panchayat_reg(models.Model):
    Firstname=models.CharField(max_length=200)
    Lastname=models.CharField(max_length=100)
    Pid=models.CharField(max_length=100)
    Address=models.CharField(max_length=500)
    Pname=models.CharField(max_length=500)
    Email=models.CharField(max_length=20)
    Password=models.CharField(max_length=200)
    confirmPassword=models.CharField(max_length=200)
    img=models.ImageField(upload_to='uimg')
    def __str__(self) :
        return self.Firstname
    

class panchayat_people(models.Model):
    Name=models.CharField(max_length=200)
    voteID=models.CharField(max_length=200)
    panchID=models.ForeignKey(panchayat_reg,on_delete=models.CASCADE)
    def __str__(self) :
        return self.Name
class Candidates(models.Model):
    Name=models.CharField(max_length=200)
    Party=models.CharField(max_length=200)
    electionsymbol=models.ImageField(upload_to="esymbol")
    VoteCount=models.IntegerField(default=0)
    panchID=models.ForeignKey(panchayat_reg,on_delete=models.CASCADE)
    approve=models.BooleanField(default=False)
    Reject=models.BooleanField(default=False)
    result=models.BooleanField(default=False)
    def __str__(self) :
        return self.Name