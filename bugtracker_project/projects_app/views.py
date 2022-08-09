from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProjectForm
from .models import Project
from django.db.models import Count

def home(request):
    project_list =Project.objects.filter().annotate(bugscount=Count('bug'))
    page = request.GET.get('page',1)

    paginator = Paginator(project_list,3)
    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        project_list = paginator.page(1)
    except EmptyPage:
        project_list = paginator.page(paginator.num_pages)
    context = {
        'projects': project_list,
    }
    return render(request, 'projects_app/home.html', context)

def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm()    
    
    context = {
        'form': form
    }
    return render(request, 'projects_app/add_project.html',context)