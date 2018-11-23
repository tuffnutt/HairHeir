from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Freelancer, Client


# Create your views here.
def index(request):
    context = {
    }
    return render(request, 'freelancer/index.html', context)


def freelancer(request, freelancer_id):
    user = get_object_or_404(Freelancer, pk=freelancer_id)

    context = {
        'freelancer': user
    }
    return render(request, 'freelancer/freelancer.html', context)


def client(request, client_id):
    try:
        user = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        raise Http404("Client Does not exist")

    context = {
        'client': user
    }
    return render(request, 'freelancer/client.html', context)
