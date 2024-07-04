from django import forms
from ..models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group

class FoodserviceWorkerForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Логин пользователя")

    class Meta:
        model = FoodserviceWorker
        fields = ['username']

    def save(self, commit=True):
        worker = User.objects.get(username=self.cleaned_data['username'])
        foodservice_worker = super().save(commit=False)
        foodservice_worker.worker = worker
        foodservice_worker.role = "worker"
        
        if commit:
            foodservice_worker.save()
            workers_group = Group.objects.get(name="workers")
            workers_group.user_set.add(worker)
    
        return foodservice_worker
    
    def clean_username(self):
        cd = self.cleaned_data
        user = User.objects.filter(username=cd["username"])
        if not user.exists():
            raise forms.ValidationError("Такого пользователя не существует")
        
        
        return cd["username"]

class FoodserviceForm(forms.ModelForm):
    class Meta:
        model = Foodservice
        fields = ['title', 'type', 'owner']
        labels = {
            'title': _('Название'),
            'type': _('Тип заведения'),
            'owner': _('Владелец')
        }