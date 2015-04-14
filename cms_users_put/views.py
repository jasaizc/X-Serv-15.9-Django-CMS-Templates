from django.shortcuts import render
from models import Usuarios
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.template import Context 

# Create your views here.

def todo(request):
  lista = Usuarios.objects.all()
  salida = "<ul>\n"
  for fila in lista:
    salida += "<li><a href=usuario/" + fila.name + ">" + fila.birthday + "</a></li>\n"
    salida += "</ul>\n"
    return HttpResponse(salida)

@csrf_exempt
def info(request):
  salida = " "
  if request.method == "GET":  
    lista = Usuarios.objects.all()
    salida += logueo(request)
    salida +="<br>Los recursos que puede ver son: "
    for i in lista:
      salida += "<br><a href=/usuarios/" + i.name + ">" + i.name + "</a>"
      salida += "<br><a href=/anotated/" + i.name + ">" + i.name + "</a>"
    if not lista:
      return HttpResponse("No hay datos")
    else:
      return HttpResponse(salida)
      
def logueo(request):
  if request.user.is_authenticated(): 
    return ("<p>Hola " + request.user.username + " <a href='/admin/logout/'>Logout</a>") 
  else: 
    return ("<p>No estas <a href='/admin/'>Logueado</a>") 

    
@csrf_exempt  
def mostrartemplate(request,recurso):
  salida = " "
  if request.method == "GET":
    lista = Usuarios.objects.filter(name=recurso)
    salida += logueo(request)
    if not lista:
      return NotFound(request,recurso)
    for i in lista:
      salida += "<br>Name: " + i.name + "<br>Birthday: " + i.birthday
    
  if request.method == "PUT":
    print request.body
    if request.user.is_authenticated():      
      nuevo = Usuarios(name = recurso, birthday = request.body)
      nuevo.save()
      salida += "Creado el recurso, pruebe en /usuarios/" + recurso + "o /anotated/" + recurso      
    else:
      salida = logueo(request)     
  try:
    lista = Usuarios.objects.filter(name=recurso)
    for i in lista:
      salida += request.method  + " "  + str(i.id) + " " + i.name + " " + i.birthday
        
    #PLANTILLA###########
    # 1. Indicar la plantilla a utilizar
    plantilla = get_template('index.html')
    # 2. Definir el contexto
    # MUY IMPORTANTE EN EL INDEX DEBE DE HABER LAS ETIQUETAS {{ title }} y {{ contenido }}, MIRAR EN marioz/index.html
    c = Context({'title': recurso, 'contenido': salida, 'user': request.user.username,})
    # 3. Renderizar
    renderizado = plantilla.render(c)
    return HttpResponse(renderizado)
  except Usuarios.DoesNotExist:
    salida += "Page not found: " + recurso
    return HttpResponseNotFound(salida) 

@csrf_exempt   
def valores(request,recurso):
  salida = " "
  if request.method == "GET":
    lista = Usuarios.objects.filter(name=recurso)
    salida += logueo(request)
    if not lista:
      return NotFound(request,recurso)
    for i in lista:
      salida += "<br>Name: " + i.name + "<br>Birthday: " + i.birthday
    
  if request.method == "PUT":
    print request.body
    if request.user.is_authenticated():      
      nuevo = Usuarios(name = recurso, birthday = request.body)
      nuevo.save()
      salida += "Creado el recurso, pruebe en /usuarios/" + recurso + "o /anotated/" + recurso      
    else:
      salida = logueo(request) 
      
  return HttpResponse(salida)    
def NotFound(request,recurso):  
  valor = "Valor No encontrado, quiere crear uno, o visualizarlo, pruebe con <a href='/usuarios'>/usuarios</a>: " + logueo(request)
  return HttpResponse(valor)
