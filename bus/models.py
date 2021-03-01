from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=13)
    desc = models.CharField(max_length=500)
    mdate = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class Appointement(models.Model):
    apt_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    pin_code = models.CharField(max_length=9)
    phone = models.CharField(max_length=13)
    issue = models.CharField(max_length=1000)
    busno = models.CharField(max_length=10)
    
    user = models.CharField(max_length=15)
    mdate = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class Billgeneration(models.Model):
    bil_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=13)
    busno = models.CharField(max_length=10)
    workdone = models.CharField(max_length=100)
    futurework = models.CharField(max_length=1000)
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    apt_id = models.IntegerField()
    user = models.CharField(max_length=15)
    byuser = models.CharField(max_length=15)
    bdate = models.DateTimeField(default=now)
    workdone1 = models.CharField(max_length=100)
    wamount1 = models.IntegerField()
    workdone2 = models.CharField(max_length=100)
    wamount2 = models.IntegerField()
    workdone3 = models.CharField(max_length=100)
    wamount3 = models.IntegerField()
    workdone4 = models.CharField(max_length=100)
    wamount4= models.IntegerField()
    workdone5 = models.CharField(max_length=100)
    wamount5 = models.IntegerField()
    workdone6 = models.CharField(max_length=100)
    wamount6 = models.IntegerField()
    workdone7 = models.CharField(max_length=100)
    wamount7 = models.IntegerField()
    workdone8 = models.CharField(max_length=100)
    wamount8 = models.IntegerField()
    workdone9 = models.CharField(max_length=100)
    wamount9 = models.IntegerField()
    workdone10 = models.CharField(max_length=100)
    wamount10 = models.IntegerField()
    workdone11 = models.CharField(max_length=100)
    wamount11 = models.IntegerField()
    workdone12 = models.CharField(max_length=100)
    wamount12 = models.IntegerField()
    workdone13 = models.CharField(max_length=100)
    wamount13 = models.IntegerField()
    workdone14 = models.CharField(max_length=100)
    wamount14 = models.IntegerField()
    workdone15 = models.CharField(max_length=100)
    wamount15 = models.IntegerField()

    def __str__(self):
        return self.name 