from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Star, Observatory, Photo
from .forms import ViewingForm


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'starcollector-chung972'

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

@login_required
def stars_index(request):
    stars = Star.objects.filter(user=request.user)
    return render(request, 'stars/index.html', {'stars': stars})


@login_required
def stars_detail(request, star_id):
    star = Star.objects.get(id=star_id)
    observatories_star_unviewable_from = Observatory.objects.exclude(
        id__in=star.observatories.all().values_list('id'))
    viewing_form = ViewingForm()
    return render(request, 'stars/detail.html', {
        'star': star,
        'viewing_form': viewing_form,
        # the key for unassociated observatories is important; esp when printing out (using {{}}} ) in the details.html page
        'observatories': observatories_star_unviewable_from
    })


class StarCreate(LoginRequiredMixin, CreateView):
    model = Star
    fields = ['name', 'type_of_star', 'distance', 'mass']
    success_url = '/stars/'

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class StarUpdate(LoginRequiredMixin, UpdateView):
    model = Star
    fields = ['type_of_star', 'distance', 'mass']


class StarDelete(LoginRequiredMixin, DeleteView):
    model = Star
    success_url = '/stars/'


@login_required
def add_viewing(request, star_id):
    form = ViewingForm(request.POST)
    if form.is_valid():
        new_viewing = form.save(commit=False)
        new_viewing.star_id = star_id
        new_viewing.save()
    return redirect('detail', star_id=star_id)


class ObservatoryList(LoginRequiredMixin, ListView):
    model = Observatory


class ObservatoryDetail(LoginRequiredMixin, DetailView):
    model = Observatory


class ObservatoryCreate(LoginRequiredMixin, CreateView):
    model = Observatory
    fields = '__all__'


class ObservatoryUpdate(LoginRequiredMixin, UpdateView):
    model = Observatory
    fields = ['name', 'location']


class ObservatoryDelete(LoginRequiredMixin, DeleteView):
    model = Observatory
    success_url = '/observatories/'


@login_required
def assoc_observatory(request, star_id, observatory_id):
    Star.objects.get(id=star_id).observatories.add(observatory_id)
    return redirect('detail', star_id=star_id)


@login_required
def unassoc_observatory(request, star_id, observatory_id):
    Star.objects.get(id=star_id).observatories.remove(observatory_id)
    return redirect('detail', star_id=star_id)


@login_required
def add_photo(request, star_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to star_id or star (if you have a star object)
            photo = Photo(url=url, star_id=star_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', star_id=star_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
