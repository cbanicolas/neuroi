#encoding:utf-8
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .models import ContenidosPacientes, ContenidosPacientesFiles, Nota, Video
from .utils import enviar_mail

def index(request):
    context = {
        'notas' : Nota.objects.filter(visible=True).order_by('-id')[:6],
        'videos' : Video.objects.filter(visible=True).order_by('-id')[:6]
    }
    return render_to_response('inicio.html',context, context_instance=RequestContext(request))


def login_user(request):
    ############ HACER USO DEL NEXT QUE VIENEEEEE !!! NO ESTA FUNCANDO PORQUE HAY Q MODIICAR EL REDIRECT ################
    if not request.user.is_authenticated():
        username = password = state = ''

        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                #if user.is_active:
                    login(request, user)
                    if request.POST.get('remember_me') is not None:
                        request.session.set_expiry(0)
                    try:
                        return redirect(request.GET['next'])
                    except:
                        return redirect('pacientes')
                #else:
                    #state = "Tu cuenta no esta activa."
            else:
                messages.error(request, 'Su usuario y / o contraseña no son correctos.')

        context = {
            'username': username,
            'state' : state,
        }
        return render_to_response('inicio.html',context, context_instance=RequestContext(request))
    else:
        if request.user.is_staff:
            messages.info(request, 'Usted se encuentra autentificado con una cuenta de administrador, salga de su cuenta desde el panel de administración.')
            return redirect('home')
        else:
            return redirect('pacientes')


@login_required()
def pacientes(request):

    #BUSCO LOS AVISOS
    if request.method == 'POST': # SI VIENE BUSQUEDA
        params = {'usuario_id': request.user.id, 'titulo__icontains' : request.POST['buscar']}
    else:
        params = {'usuario_id': request.user.id}
    params = {k: v for k, v in params.items() if v is not None}
    contenidos_list = ContenidosPacientes.objects.filter(**params).order_by('-id')

    context = {
        'contenidos' : contenidos_list,
    }
    return render_to_response('pacientes.html',context, context_instance=RequestContext(request))


def nota(request, tit_slug=''):
    nota = get_object_or_404(Nota, slug=tit_slug)

    context = {
        'nota' : nota,
    }
    return render_to_response('nota.html',context, context_instance=RequestContext(request))

def contacto(request):
    if request.method == 'POST':
        from django.conf import settings
        mail = {
            'name': request.POST['name'],
            'message': request.POST['message'],
            'from_email' : settings.DEFAULT_FROM_EMAIL,
            'reply_to' : request.POST['email'],
            'to': settings.DEFAULT_FROM_EMAIL,
        }
        if enviar_mail(mail=mail):
            messages.success(request, 'Gracias por contactarte, a la brevedad responderemos tu consulta.')

    context = {

    }
    return render_to_response('inicio.html',context, context_instance=RequestContext(request))