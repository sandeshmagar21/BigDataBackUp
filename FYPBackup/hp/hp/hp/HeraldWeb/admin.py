from django.contrib import admin

from .models import Contact, Student, Transcript

# Register your models here.

admin.site.register(Contact),
admin.site.register(Student),
admin.site.register(Transcript)