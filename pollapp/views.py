from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
from django.utils import timezone
# Create your views here.


class IndexView(generic.ListView):
	template_name = 'polls\\index.html'
	context_object_name = 'lq_list'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

		
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls\\detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())
	
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls\\results.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

def index(request):
	ls = Question.objects.order_by('-pub_date')[:5]
	temp = loader.get_template('polls\\index.html')
	context = {
		'lq_list':ls
	}
	return HttpResponse(temp.render(context,request))
	#return HttpResponse("Welcome to the index page of my first app!")
	
def detail(request, qid):
	#try:
	#	question = Question.objects.get(pk=qid)
	#except:
	#	raise Http404("Question doesn't exist!")
	question = get_object_or_404(Question,pk=qid)
	return render(request,"polls\\detail.html",{'question':question})
	#return HttpResponse("You're looking at question %s."%qid)

def results(request, qid):
	quest = get_object_or_404(Question,pk=qid)
	return render(request,"polls\\results.html",{'question':quest})
	#return HttpResponse("You're looking at the results of question %s."%qid)

def vote(request, qid):
	quest = get_object_or_404(Question, pk=qid)
	try:
		selected = quest.choice_set.get(pk=request.POST['choice'])
	except:
		return render(request,'polls\\detail.html',{'question':quest,'error_message':'You didnt select a valid choice',})
	selected.votes += 1
	selected.save()
	return HttpResponseRedirect(reverse('pollapp:results',args=(quest.id,)))
	#return HttpResponse("You're voting on question %s."%qid)
	
