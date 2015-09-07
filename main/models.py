from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings

class Question(models.Model):
	loc_name = models.CharField("Location name",max_length=64,blank=False)
	text = models.TextField(blank=True)
	answer = models.CharField(max_length=64,blank=True)
	rent = models.FloatField("Accomodation cost per second",default=0.0)
	stipend = models.FloatField(default=0.0)
	def __str__(self):
		return self.loc_name

class Player(models.Model):
	user = models.OneToOneField(User)
	score = models.FloatField()
	curr_loc = models.ForeignKey(Question,null=True)
	arrival_time = models.DateTimeField()

	# initially timer will be paused (arrival_time=null)
	# When a user visits a place timer will (re)start (arrival_time=timezone.now())
	# When game ends timer will stop (arrival_time=null)
	def __str__(self):
		return self.user.username

	def dyn_score(self):
		if self.curr_loc:
			return self.score - (timezone.now()-self.arrival_time).total_seconds()*self.curr_loc.rent
		else:
			return self.score

	def commit_rent(self):
		self.fly_to(self.curr_loc,timezone.now())
		self.save()

	def fly_to(self,new_loc,depart_time):
		# Does not save the model
		if self.curr_loc:
			self.score-= (depart_time-self.arrival_time).total_seconds()*self.curr_loc.rent
			if new_loc and new_loc!=self.curr_loc:
				distance = Distance.objects.get(source=self.curr_loc, dest=new_loc).distance
				self.score-= distance*settings.CONFIG["travel_cost_per_km"]
		self.arrival_time = depart_time
		self.curr_loc = new_loc

	def attempts_left(self):
		# returns None if self.curr_loc is None
		# returns -1 if can't attempt because question is already correctly attempted
		# otherwise returns number of attempts left
		max_attempts = settings.CONFIG['max_attempts_per_question']
		if (not self.curr_loc) or (not self.curr_loc.answer):
			return None
		try:
			att_obj = Attempt.objects.get(user=self.user, question=self.curr_loc)
			if att_obj.correct:
				return -1
			else:
				return max_attempts - att_obj.attempts
		except Attempt.DoesNotExist:
			return max_attempts

	def submit(self,user_answer):
		if (not user_answer) or (not self.curr_loc) or (not self.curr_loc.answer):
			# if location is None or passive or user submitted an empty string, return None
			return None
		result = (user_answer == self.curr_loc.answer)
		att_obj = Attempt.objects.get_or_create(user=self.user, question=self.curr_loc)[0]
		max_attempts = settings.CONFIG['max_attempts_per_question']
		if att_obj.correct or att_obj.attempts >= max_attempts:
			return None
		att_obj.attempts+= 1
		att_obj.correct = result
		att_obj.save()

		divider = settings.CONFIG["score_divider"]
		if result:
			self.score+= self.curr_loc.stipend/(divider**(att_obj.attempts-1))
			self.save()
		return result

	contact_fields = ('name1','name2','phone1','phone2','email1','email2','bitsid1','bitsid2')
	name1 = models.CharField(max_length=200,blank=False)
	name2 = models.CharField(max_length=200,blank=False)
	phone1 = models.BigIntegerField()
	phone2 = models.BigIntegerField(blank=True,null=True)
	email1 = models.EmailField(blank=False)
	email2 = models.EmailField(blank=True)
	bitsid1 = models.CharField(max_length=16,blank=True)
	bitsid2 = models.CharField(max_length=16,blank=True)

class Attempt(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	attempts = models.IntegerField(default=0)
	correct = models.BooleanField(default=False)
	def __str__(self):
		return self.user.username+" : "+self.question.loc_name

class Distance(models.Model):
	source = models.ForeignKey(Question,related_name='sources')
	dest = models.ForeignKey(Question,related_name='dests')
	distance = models.FloatField("Distance between 2 cities in km")
	def __str__(self):
		return self.source.loc_name+" to "+self.dest.loc_name+" : "+str(self.distance)
