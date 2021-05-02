from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm 
from .models import Transcript

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['address','mobile','profile_pic']


class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['address','mobile','profile_pic']



class AdminRequestForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of client model will be shown there in html
    teacher=forms.ModelChoiceField(queryset=models.Teacher.objects.all(),empty_label="Teacher Name",to_field_name='id')
    student=forms.ModelChoiceField(queryset=models.Student.objects.all(),empty_label="Student Name",to_field_name='id')


class AskDateForm(forms.Form):
    date=forms.DateField()


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))



class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        fields = '__all__'        