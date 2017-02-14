#from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
# Create your models here.

#Next line needed to use __str__ in Python 2.7
@python_2_unicode_compatible
class Question(models.Model):
	qtxt = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.qtxt
	def recent(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
		
#Next line needed to use __str__ in Python 2.7
@python_2_unicode_compatible
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	ctxt = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.ctxt