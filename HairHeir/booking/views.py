import datetime
from cgi import log

from django.contrib.auth import login
from .models import User, City, Type
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import CreateView, TemplateView

from .forms import ClientSignUpForm, FreelancerSignUpForm
from .models import Freelancer, Client, Type


# Create your views here.
def index(request):
    city = City.objects.all()
    types = Type.objects.all()
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    context = {
        'cities': city,
        'types': types,
        'today': today
    }
    return render(request, 'booking/index.html', context)


def freelancer(request, freelancer_id):
    user = get_object_or_404(User, pk=freelancer_id)

    context = {
        'freelancer': user
    }
    return render(request, 'booking/freelancer.html', context)


def client(request, client_id):
    try:
        user = User.objects.get(pk=client_id)
    except Client.DoesNotExist:
        raise Http404("Client Does not exist")

    context = {
        'client': user
    }
    return render(request, 'booking/client.html', context)


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/booking/client/' + str(user.pk))


class FreelancerSignUpView(CreateView):
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Freelancer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/booking/' + str(user.pk))


def Search(request):
    city = request.POST['city']
    types = request.POST['type']

    if (city == 'NULL') & (types == 'NULL'):
        freelancer = Freelancer.objects.all()
    elif city == 'NULL':
        user_list = []
        users = User.objects.filter(is_freelancer=True)
        for user in users:
            user_list.append(user.pk)

        freelancer = Freelancer.objects.filter(type__id=types, user__in=user_list)
    elif types == 'NULL':
        user_list = []
        users = User.objects.filter(is_freelancer=True, city=city)
        for user in users:
            user_list.append(user.pk)

        freelancer = Freelancer.objects.filter(user__in=user_list)
    else:
        user_list = []
        users = User.objects.filter(is_freelancer=True, city=city)
        for user in users:
            user_list.append(user.pk)

        freelancer = Freelancer.objects.filter(type__id=types, user__in=user_list)


    context = {
        'users': freelancer
    }
    return render(request, 'booking/result.html', context)
