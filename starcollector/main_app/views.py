from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Star
from .forms import ViewingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def stars_index(request):
    stars = Star.objects.all()
    return render(request, 'stars/index.html', {'stars': stars})


def stars_detail(request, star_id):
    star = Star.objects.get(id=star_id)
    viewing_form = ViewingForm()
    return render(request, 'stars/detail.html', {
        'star': star,
        'viewing_form': viewing_form
    })


class StarCreate(CreateView):
    model = Star
    fields = '__all__'
    success_url = '/stars/'


class StarUpdate(UpdateView):
    model = Star
    fields = ['type_of_star', 'distance', 'mass']


class StarDelete(DeleteView):
    model = Star
    success_url = '/stars/'


def add_viewing(request, star_id):
    form = ViewingForm(request.POST)
    if form.is_valid():
        new_viewing = form.save(commit=False)
        new_viewing.star_id = star_id
        new_viewing.save()
    return redirect('detail', star_id=star_id)