from django.contrib import admin
from .models import Contact ,Appointement ,Billgeneration
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','desc')

class AppointementAdmin(admin.ModelAdmin):
    list_display = ('name','busno','phone','issue','email','address','pin_code','user')

class BillgenerationAdmin(admin.ModelAdmin):
    list_display = ('bil_id','name','amount','email','phone','workdone','futurework','user','byuser','bdate','apt_id')

admin.site.register(Contact , ContactAdmin)
admin.site.register(Appointement , AppointementAdmin)
admin.site.register(Billgeneration , BillgenerationAdmin)