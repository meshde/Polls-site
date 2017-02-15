from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question,Choice
# Create your views here.

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
	
