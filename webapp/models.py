from django.db import models


# Create your models here.
class user(models.Model):
	name=models.CharField(max_length=100);
	email=models.CharField(max_length=100);
	pwd=models.CharField(max_length=100);
	zip=models.CharField(max_length=100);
	gender=models.CharField(max_length=100);
	age=models.CharField(max_length=100);

class accuracysc(models.Model):
    algo=models.CharField(max_length=100);
    accuracyv=models.FloatField(max_length=1000)
    prec=models.FloatField(max_length=1000)
    recall=models.FloatField(max_length=1000)
    f1sc=models.FloatField(max_length=1000)


	

class tweets(models.Model):
	sno = models.CharField(max_length=100);
	tweet = models.TextField();
	sentiment=models.CharField(max_length=100);

	

