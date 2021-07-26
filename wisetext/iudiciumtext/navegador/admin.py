from django.contrib import admin

# Register your models here.
from .models import Acordao

class AcordaoAdmin(admin.ModelAdmin):
    list_display = ('id_processo',)

admin.site.register(Acordao, AcordaoAdmin)