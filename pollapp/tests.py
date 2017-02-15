from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse
# Create your tests here.


class QuestionMethodTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.recent(), False)	
	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.recent(), False)
	def test_was_published_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.recent(), True)

class QuestionViewTest(TestCase):
	def test_index_view_no_quest(self):
		#No questions must be handled gracefully
		r = self.client.get(reverse('pollapp:index'))
		self.assertEqual(r.status_code,200)
		self.assertQuerysetEqual(r.context['lq_list'],[])
		self.assertConatins(r,'No polls')
	def test_index_view_future_quest(self):
		#Questions of the future must not be displayed
		Question.objects.create(qtxt='test',pub_date=timezone.now()+datetime.timedelta(days=30))
		r = self.client.get(reverse('pollapp:index'))
		self.assertEqual(r.status_code,200)
		self.assertQuerysetEqual(r.context['lq_list'],[])
		self.assertConatins(r,'No polls')
	def test_index_view_past_and_future_quest(self):
		#future questions must be ignored
		Question.objects.create(qtxt='future',pub_date=timezone.now()+datetime.timedelta(days=30))
		Question.objects.create(qtxt='past',pub_date=timezone.now()+datetime.timedelta(days=-30))
		r = self.client.get(reverse('pollapp:index'))
		self.assertEqual(r.status_code,200)
		self.assertQuerysetEqual(r.context['lq_list'],['<Question: past>'])
		
		
class QuestionDetailViewTest(TestCase):
	def test_detail_view_future_question(self):
		q = Question.objects.create(qtxt='Future', pub_date=timezone.now()+datetime.timedelta(days=30))
		r = self.client.get(reverse('pollapp:detail',args=(q.id,)))
		self.assertEqual(r.status_code,404)
	def test_detail_view_past_question(self):
		q = Question.objects.create(qtxt='Future' ,pub_date=timezone.now()+datetime.timedelta(days=-5))
		r = self.client.get(reverse('pollapp:detail',args=(q.id,)))
		self.assertContains(r,q.qtxt)
	def test_detail_view_no_choice(self):
		q = Question.objects.create(qtxt='Past', pub_date=timezone.now()+datetime.timedelta(days=30))
		r = self.client.get(reverse('pollapp:detail',args=(q.id,)))
		self.assertContains(r,'No choices.Please Contact Admin')
	def test_detail_view_choice(self):
		q = Question.objects.create(qtxt='Past' ,pub_date=timezone.now()+datetime.timedelta(days=30))
		c = q.choice_set.create(ctxt='choice')
		r = self.client.get(reverse('pollapp:detail',args=(q.id,)))
		self.assertContains(r,c.ctxt)
	
class QuestionResultsViewTest(TestCase):
	def test_detail_view_future_question(self):
		q = Question.objects.create(qtxt='Future', pub_date=timezone.now()+datetime.timedelta(days=30))
		r = self.client.get(reverse('pollapp:results',args=(q.id,)))
		self.assertEqual(r.status_code,404)
	def test_detail_view_past_question(self):
		q = Question.objects.create(qtxt='Future' ,pub_date=timezone.now()+datetime.timedelta(days=-5))
		r = self.client.get(reverse('pollapp:results',args=(q.id,)))
		self.assertContains(r,q.qtxt)
	def test_detail_view_no_choice(self):
		q = Question.objects.create(qtxt='Past', pub_date=timezone.now()+datetime.timedelta(days=30))
		r = self.client.get(reverse('pollapp:results',args=(q.id,)))
		self.assertContains(r,'No choices.Please Contact Admin')
	def test_detail_view_choice(self):
		q = Question.objects.create(qtxt='Past',pub_date=timezone.now()+datetime.timedelta(days=30))
		c = q.choice_set.create(ctxt='choice')
		r = self.client.get(reverse('pollapp:results',args=(q.id,)))
		self.assertContains(r,c.ctxt)