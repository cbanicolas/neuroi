#encoding:utf-8
from django.contrib import admin
from django.forms import forms, CharField
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from django_bootstrap_calendar.models import CalendarEvent
from embed_video.admin import AdminVideoMixin

from .models import ContenidosPacientes, ContenidosPacientesFiles, HistoriasClinicas, HistoriasClinicasFiles, Nota, Video, UserExtension, Localidad

class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['id','titulo']
    list_editable = ['titulo']
    list_filter = ['titulo']
    search_fields = ['titulo']

class ContenidosPacientesFilesInline(admin.TabularInline):
    model = ContenidosPacientesFiles
class ContenidosPacientesAdmin(admin.ModelAdmin):
    list_display = ['usuario','titulo','tipo','visible','fecha']
    list_editable = ['titulo','tipo','visible']
    list_filter = ['fecha']
    date_hierarchy = 'fecha'
    search_fields = ['titulo','usuario']
    inlines = [ContenidosPacientesFilesInline, ]


class HistoriasClinicasFilesInline(admin.TabularInline):
    model = HistoriasClinicasFiles
class HistoriasClinicasAdmin(admin.ModelAdmin):
    list_display = ['paciente','localidad','fecha']
    list_editable = ['paciente','localidad']
    list_filter = ['localidad','fecha']
    date_hierarchy = 'fecha'
    search_fields = ['paciente',]
    inlines = [HistoriasClinicasFilesInline, ]


class NotaAdmin(admin.ModelAdmin):
    list_display = ['titulo','fecha']
    list_filter = ['fecha']
    date_hierarchy = 'fecha'
    search_fields = ['titulo','nota']

class VideoAdmin(AdminVideoMixin,admin.ModelAdmin):
    list_display = ['titulo','fecha']
    list_filter = ['fecha']
    date_hierarchy = 'fecha'
    search_fields = ['titulo','descripcion']

class UserExtensionInline(admin.StackedInline):
    model = UserExtension
    can_delete = False
    verbose_name = 'Datos adicionales'
    verbose_name_plural = 'Datos adicionales'

class UserAdmin1(UserAdmin):
    inlines = (UserExtensionInline, )
    list_display = ('email', 'first_name', 'last_name', 'display_localidad', 'display_telefono')

    #list_filter = (
    #    ('localidad', admin.RelatedOnlyFieldListFilter),
    #)

    def display_localidad(self, request):
        if UserExtension.objects.filter(user__id = request.id):
            return UserExtension.objects.get(user__id = request.id).localidad
        else:
            return None
    display_localidad.short_description = 'Localidad'

    def display_telefono(self, request):
        if UserExtension.objects.filter(user__id = request.id):
            return UserExtension.objects.get(user__id = request.id).telefono
        else:
            return None
    display_telefono.short_description = 'Teléfono'


admin.site.unregister(User)
admin.site.register(User, UserAdmin1)

admin.site.register(CalendarEvent)

admin.site.register(Localidad,LocalidadAdmin)
admin.site.register(ContenidosPacientes,ContenidosPacientesAdmin)
admin.site.register(HistoriasClinicas,HistoriasClinicasAdmin)
admin.site.register(Nota,NotaAdmin)
admin.site.register(Video,VideoAdmin)