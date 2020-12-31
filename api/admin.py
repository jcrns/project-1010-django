from django.contrib import admin

from .models import Preference, Politician, Profile, Event, Movement

admin.site.register(Preference)
admin.site.register(Politician)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Movement)
