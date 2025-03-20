from django.contrib import admin
from opinionapp.models import Opinion, reaction, user

# Register your models here.
admin.site.register(Opinion)
admin.site.register(reaction)
admin.site.register(user)