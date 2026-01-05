from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm
from django.contrib.auth.decorators import login_required


def acceder(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			nombre_usuario = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			usuario = authenticate(username=nombre_usuario, password=password)
			if usuario is not None:
				login(request, usuario)
				messages.success(request, F"Bienvenid@ de nuevo {nombre_usuario}")
				return redirect("index")
			else:
				messages.error(request, "Los datos son incorrectos")
		else:
			messages.error(request, "Los datos son incorrectos")

	form = AuthenticationForm()
	return render(request, "acceder.html", {"form": form})



def salir(request):
	logout(request)
	messages.success(request, F"Tu sesion se ha cerrado correctamente")
	return redirect("index")


def usuarios(request):
	datos = User.objects.all()
	return render(request, 'usuarios.html', {"datos": datos})


@login_required(login_url='/acceder')
def userupdate(request, id):
        instance= get_object_or_404(User, pk=id)
        form = UserForm(request.POST or None, instance=instance)
        context= {'form': form}
        if form.is_valid():
                obj= form.save(commit= False)
                obj.save()
                messages.success(request, "El usuario fue actualizado")
                return redirect("usuarios")

        else:
                context= {'form': form, 'error': 'Error al actualizar'}
                return render(request,'usuariosupdate.html' , context)

def inicio(request):
	menus = "HOLA"
	return render(request, 'index.html')