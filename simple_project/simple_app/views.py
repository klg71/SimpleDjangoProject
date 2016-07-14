from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.http.request import QueryDict

from django.views.decorators.csrf import csrf_exempt

# Create your views here

def get_index(request):
    #print(request.stream)
    context={'name':'World'}
    context.update(csrf(request))
    print(request.body)
    if 'name' in request.POST:
        context['name']=request.POST['name']


    return render(request,'simple_app/index.html',context); 
