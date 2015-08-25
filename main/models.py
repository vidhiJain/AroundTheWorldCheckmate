from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone

class Question(models.Model):
	text = models.TextField()
	loc_name = models.CharField("Location name",max_length=64,blank=False)
	rent = models.FloatField("Accomodation cost per second")
	answer = models.CharField(max_length=64,blank=False)
	max_attempts = models.IntegerField(default=0)
	marks = models.FloatField()
	# divider = models.FloatField()
	def __str__(self):
		return self.loc_name

class Player(models.Model):
	user = models.OneToOneField(User)
	score = models.FloatField()
	curr_loc = models.ForeignKey(Question)
	arrival_time = models.DateTimeField(null=True)
	# initially timer will be paused (arrival_time=null)
	# When a user visits a place timer will (re)start (arrival_time=timezone.now())
	# When game ends timer will stop (arrival_time=null)
	def __str__(self):
		return self.user.username

	# Contact details
	name1 = models.CharField(max_length=200,blank=False)
	name2 = models.CharField(max_length=200,blank=False)
	phone1 = models.BigIntegerField(null=False)
	phone2 = models.BigIntegerField(null=True)
	email1 = models.EmailField(blank=False)
	email2 = models.EmailField(blank=True)

class Attempt(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	attempts = models.IntegerField(default=0)
	correct = models.BooleanField(default=0)
	def __str__(self):
		return self.user.username+" : "+self.question.loc_name

class Distance(models.Model):
	source = models.ForeignKey(Question,related_name='sources')
	dest = models.ForeignKey(Question,related_name='dests')
	distance = models.FloatField("Distance between 2 cities in km")
	def __str__(self):
		return self.source.loc_name+" to "+self.dest.loc_name+" : "+str(self.distance)
