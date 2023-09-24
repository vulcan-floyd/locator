from audioop import add
from django.shortcuts import render, redirect
from django.http import HttpResponse
import folium
import geocoder

from .models import Search
from .forms import SearchForm 

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    # if request.method == 'Post':
    #     address = request.Post.get('address')

    address = Search.objects.all().last()
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('You address input is invalid')

    m = folium.Map(location=[19, -12], zoom_start=2)
    folium.Marker([lat, lng], tooltip='Click for More', popup=country).add_to(m)
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form
    }
    return render(request, 'index.html', context)
