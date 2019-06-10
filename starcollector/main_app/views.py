from django.shortcuts import render
from django.http import HttpResponse

class Star:
    def __init__(self, name, type_of_star, distance, mass):
        self.name = name
        self.type_of_star = type_of_star
        self.distance = distance
        self.mass = mass

stars = [
    Star('Deneb', 'A2 Ia', 2615, 19),
    Star('Altair', 'A7 V', 16.7, 1.79),
    Star('Vega', 'A0 Va', 25, 2.135),
    Star('Proxima Centauri', 'M5.5Ve', 4.244, 0.122),
]

# Create your views here.
def home(request):
    return HttpResponse("<h1>Star Collector Home!</h1>")

def about(request):
    return render(request, 'about.html')

def stars_index(request):
    return render(request, 'stars/index.html', {'stars': stars})