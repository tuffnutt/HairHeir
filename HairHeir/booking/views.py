import datetime
from cgi import log

from django.contrib.auth import login
from django.db.models import Q

from .models import User, City, Type
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import CreateView, TemplateView

from .forms import ClientSignUpForm, FreelancerSignUpForm
from .models import Freelancer, Client, Type, Schedule, City, District, Province


# Create your views here.
def index(request):
    city = City.objects.all()
    types = Type.objects.all()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    topfive = Freelancer.objects.all().order_by('-rate')[:4]
    context = {
        'cities': city,
        'types': types,
        'today': today,
        'topfive': topfive
    }
    return render(request, 'booking/index.html', context)


def freelancer(request, freelancer_id):
    user = get_object_or_404(User, pk=freelancer_id)

    context = {
        'freelancer': user
    }
    return render(request, 'booking/freelancer.html', context)


def user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.is_freelancer:
        schedules = Schedule.objects.filter(freelancer_id=user.pk)
        date_list = []

        for schedule in schedules:
            date_list.append(schedule.date)

        print(date_list)
        context = {
            'users': user,
            'schedule': date_list
        }
        return render(request, 'booking/freelancer.html', context)
    else:
        context = {
            'user': user
        }
        return render(request, 'booking/client.html', context)

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
        return redirect('/user/' + str(user.pk))


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
        return redirect('/user/' + str(user.pk))


def Search(request):
    city = request.POST['city']
    types = request.POST['type']
    start = request.POST['from']
    end = request.POST['to']

    if (city == 'NULL') & (types == 'NULL'):
        freelancer_list = []

        schedules = Schedule.objects.filter(date__range=(start, end), status=True)
        for schedule in schedules:
            freelancer_list.append(schedule.freelancer_id)

        freelancer = Freelancer.objects.all().exclude(pk__in=freelancer_list)
    elif city == 'NULL':
        user_list = []
        freelancer_list = []
        users = User.objects.filter(is_freelancer=True)
        for user in users:
            user_list.append(user.pk)

        schedules = Schedule.objects.filter(date__range=(start, end), status=True)
        for schedule in schedules:
            freelancer_list.append(schedule.freelancer_id)

        freelancer = Freelancer.objects.filter(type__id=types, user__in=user_list).exclude(pk__in=freelancer_list)
    elif types == 'NULL':
        user_list = []
        freelancer_list = []
        users = User.objects.filter(is_freelancer=True, city=city)
        for user in users:
            user_list.append(user.pk)
        schedules = Schedule.objects.filter(date__range=(start, end), status=True)

        for schedule in schedules:
            freelancer_list.append(schedule.freelancer_id)

        freelancer = Freelancer.objects.filter(user__in=user_list).exclude(pk__in=freelancer_list)
    else:
        user_list = []
        freelancer_list = []
        users = User.objects.filter(is_freelancer=True, city=city)
        for user in users:
            user_list.append(user.pk)

        schedules = Schedule.objects.filter(date__range=(start, end), status=True)
        for schedule in schedules:
            freelancer_list.append(schedule.freelancer_id)

        freelancer = Freelancer.objects.filter(type__id=types, user__in=user_list).exclude(pk__in=freelancer_list)

    city1 = City.objects.all()
    types1 = Type.objects.all()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    context = {
        'cities': city1,
        'types': types1,
        'from': start,
        'to': end,
        'type': types,
        'city': city,
        'users': freelancer,
        'price': "1000",
        'rating': "0",
        'gender': 'all',
        'location': 'city'

    }
    return render(request, 'booking/result.html', context)




def AdvancedSearch(request):
    city = request.POST['city']
    types = request.POST['type']
    start = request.POST['from']
    end = request.POST['to']
    pricerange = request.POST['price']
    rate = request.POST['rating']
    gender = request.POST['gender']
    location = request.POST['location']


    if (city == 'NULL') & (types == 'NULL'):
        if gender == 'all':
            freelancer_list = []

            schedules = Schedule.objects.filter(date__range=(start, end), status=True)
            for schedule in schedules:
                freelancer_list.append(schedule.freelancer_id)

            freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5)).exclude(pk__in=freelancer_list)
        else:
            freelancer_list = []

            schedules = Schedule.objects.filter(date__range=(start, end), status=True)
            for schedule in schedules:
                freelancer_list.append(schedule.freelancer_id)

            freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5), gender=gender).exclude(
                pk__in=freelancer_list)
    elif city == 'NULL':
        if gender == 'all':
            user_list = []
            freelancer_list = []
            users = User.objects.filter(is_freelancer=True)
            for user in users:
                user_list.append(user.pk)

            schedules = Schedule.objects.filter(date__range=(start, end), status=True)
            for schedule in schedules:
                freelancer_list.append(schedule.freelancer_id)

            freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange), rate__range=(rate, 5), user__in=user_list).exclude(pk__in=freelancer_list)
        else:
            user_list = []
            freelancer_list = []
            users = User.objects.filter(is_freelancer=True)
            for user in users:
                user_list.append(user.pk)

            schedules = Schedule.objects.filter(date__range=(start, end), status=True)
            for schedule in schedules:
                freelancer_list.append(schedule.freelancer_id)

            freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange),
                                                   rate__range=(rate, 5), user__in=user_list, gender=gender).exclude(
                pk__in=freelancer_list)
    elif types == 'NULL':
        if gender == 'all':
            if location =='city1':
                user_list = []
                freelancer_list = []
                users = User.objects.filter(is_freelancer=True, city=city)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5), user__in=user_list).exclude(pk__in=freelancer_list)
            elif location == 'district':
                user_list = []
                freelancer_list = []
                district = City.objects.get(pk=city).district
                city_list = []
                cities = City.objects.filter(district=district)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list).exclude(pk__in=freelancer_list)
            else:
                user_list = []
                freelancer_list = []
                province = City.objects.get(pk=city).district.pk
                district = District.objects.filter(province=province)
                district_list = []
                for dt in district:
                    district_list.append(dt.pk)
                city_list = []
                cities = City.objects.filter(district__in=district_list)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list).exclude(pk__in=freelancer_list)
        else:
            if location == 'city1':
                user_list = []
                freelancer_list = []
                users = User.objects.filter(is_freelancer=True, city=city)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list, gender=gender).exclude(pk__in=freelancer_list)
            elif location == 'district':
                user_list = []
                freelancer_list = []
                district = City.objects.get(pk=city).district
                city_list = []
                cities = City.objects.filter(district=district)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list, gender=gender).exclude(pk__in=freelancer_list)
            else:
                user_list = []
                freelancer_list = []
                province = City.objects.get(pk=city).district.pk
                district = District.objects.filter(province=province)
                district_list = []
                for dt in district:
                    district_list.append(dt.pk)
                city_list = []
                cities = City.objects.filter(district__in=district_list)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list, gender=gender).exclude(pk__in=freelancer_list)
    else:
        if gender == 'all':
            if location =='city1':
                user_list = []
                freelancer_list = []
                users = User.objects.filter(is_freelancer=True, city=city)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange), rate__range=(rate, 5), user__in=user_list).exclude(pk__in=freelancer_list)
            elif location == 'district':
                user_list = []
                freelancer_list = []
                district = City.objects.get(pk=city).district
                city_list = []
                cities = City.objects.filter(district=district)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list).exclude(pk__in=freelancer_list)
            else:
                user_list = []
                freelancer_list = []
                province = City.objects.get(pk=city).district.pk
                district = District.objects.filter(province=province)
                district_list = []
                for dt in district:
                    district_list.append(dt.pk)
                city_list = []
                cities = City.objects.filter(district__in=district_list)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange), rate__range=(rate, 5),
                                                       user__in=user_list).exclude(pk__in=freelancer_list)
        else:
            if location == 'city1':
                user_list = []
                freelancer_list = []
                users = User.objects.filter(is_freelancer=True, city=city)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange),
                                                       rate__range=(rate, 5), user__in=user_list, gender=gender).exclude(
                    pk__in=freelancer_list)
            elif location == 'district':
                user_list = []
                freelancer_list = []
                district = City.objects.get(pk=city).district
                city_list = []
                cities = City.objects.filter(district=district)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange),
                                                       rate__range=(rate, 5),
                                                       user__in=user_list, gender=gender).exclude(pk__in=freelancer_list)
            else:
                user_list = []
                freelancer_list = []
                province = City.objects.get(pk=city).district.pk
                district = District.objects.filter(province=province)
                district_list = []
                for dt in district:
                    district_list.append(dt.pk)
                city_list = []
                cities = City.objects.filter(district__in=district_list)
                for ct in cities:
                    city_list.append(ct.pk)

                users = User.objects.filter(is_freelancer=True, city__in=city_list)
                for user in users:
                    user_list.append(user.pk)
                schedules = Schedule.objects.filter(date__range=(start, end), status=True)

                for schedule in schedules:
                    freelancer_list.append(schedule.freelancer_id)

                freelancer = Freelancer.objects.filter(type__id=types, price__range=(0.0, pricerange),
                                                       rate__range=(rate, 5),
                                                       user__in=user_list, gender=gender).exclude(pk__in=freelancer_list)



    city1 = City.objects.all()
    types1 = Type.objects.all()
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    context = {
        'cities': city1,
        'types': types1,
        'from': start,
        'to': end,
        'type': types,
        'city': city,
        'users': freelancer,
        'price': pricerange,
        'rating': rate,
        'gender': gender,
        'location': location
    }
    return render(request, 'booking/result.html', context)
