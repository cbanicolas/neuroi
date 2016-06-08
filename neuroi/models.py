#encoding:utf-8
import datetime
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField

from utils import enviar_mail

def send_promotion(sender, instance, created, **kwargs):
    if instance.email: #para q no mande cuando se modifique el objeto mas adelante
        from django.template.loader import render_to_string
        from django.contrib.sites.models import Site

        context_mail = {
            'email' : instance.email,
            'current_site': Site.objects.get_current(),
        }

        mail = {
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "reply_to" : settings.DEFAULT_FROM_EMAIL,
                "to": instance.email,
                "subject": render_to_string('promociones/send_destacado_gratis_subject.txt', context_mail),
                "message": render_to_string('promociones/send_destacado_gratis.html', context_mail),
        }

        if enviar_mail(mail=mail): # esto retorna true o false, ver en utils
            pass
        #FIN -----------------------------------------------

class Localidad(models.Model):
    titulo = models.CharField(max_length=90, db_index=True)

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = 'Localidades'

class UserExtension(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    localidad = models.ForeignKey(Localidad)
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')

class ContenidosPacientesFiles(models.Model):
    file = models.FileField(upload_to=settings.FILE_UPLOAD_PATH)
    contenido = models.ForeignKey('ContenidosPacientes')

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

class ContenidosPacientes(models.Model):
    usuario = models.ForeignKey(User)
    titulo = models.CharField(max_length=90)
    descripcion = models.TextField(max_length=2000)

    TIPOS = (
        ('INF', 'Informes'),
        ('PED', 'Pedidos'),
    )
    tipo = models.CharField(max_length=3, choices=TIPOS, null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add=True)
    fecha_ultima_edicion = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Informe o Pedido'
        verbose_name_plural = 'Informes y Pedidos'


class HistoriasClinicasFiles(models.Model):
    file = models.FileField(upload_to=settings.FILE_UPLOAD_PATH)
    historiaclinica = models.ForeignKey('HistoriasClinicas')

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

class HistoriasClinicas(models.Model):
    paciente = models.CharField(max_length=90, verbose_name='Nombre completo')
    localidad = models.ForeignKey(Localidad)

    fecha = models.DateTimeField(auto_now_add=True)
    fecha_ultima_edicion = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.paciente

    class Meta:
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'

class Nota(models.Model):
    titulo = models.CharField(max_length=90, unique=True)
    slug = models.SlugField(max_length=70,editable=False,unique=True)
    nota = RichTextUploadingField()
    imagen = models.ImageField(upload_to="uploads")

    fecha = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Nota, self).save(*args, **kwargs)


class Video(models.Model):
    titulo = models.CharField(max_length=90, unique=True)
    descripcion = models.TextField()
    video = EmbedVideoField()  # same like models.URLField()

    fecha = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.titulo



#SEÑALES -------------------------------------------------------------------------------
#ESTA SEÑAL ENVIA EL MAIL DE LA PROMOCION
signals.post_save.connect(send_promotion, sender=User)