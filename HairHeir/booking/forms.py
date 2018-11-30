from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import (Freelancer, Client, User, Skill, Type)


class ClientSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'address', 'city']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user)
        return user


class FreelancerSignUpForm(UserCreationForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'address', 'city']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_freelancer = True
        user.save()
        freelancer = Freelancer.objects.create(user=user)
        freelancer.skill.add(*self.cleaned_data.get('skills'))
        freelancer.type.add(*self.cleaned_data.get('types'))
        return user
