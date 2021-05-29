from django.contrib import admin
from .models import Profile, Contact, AdminContact

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(AdminContact)
