
from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
from django.utils import timezone
import bcrypt


def index(request):

    context = {

    }
    return redirect('/wall')


def wall(request):
    if 'usuario' not in request.session:
        messages.error(request, "No estas logeado")
        return redirect("/login")
    
    context = {
        'posts' : Message.objects.filter(created_at__lte=timezone.now()).order_by('created_at'),
        'comentario' : Comment.objects.all()

    }
    return render(request, 'index.html', context)


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_nombre'] =  request.POST['nombre']
            request.session['register_apellido'] =  request.POST['apellido']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_nombre'] = ""
            request.session['register_apellido'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                firstname = request.POST['nombre'],
                lastname = request.POST['apellido'],
                email=request.POST['email'],
                password=password_encryp,
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['usuario'] = {
                "id" : usuario_nuevo.id,
                "firstname": f"{usuario_nuevo.firstname}",
                "lastname": f"{usuario_nuevo.lastname}",
                "email": usuario_nuevo.email
            }
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')


def login(request):
    if request.method == 'GET':

        if 'usuario' in request.session:
            messages.warning(request, "Ya estas logeado")
            return redirect("/")

        context = {}
        return render(request, 'login.html', context)

    if request.method == 'POST':
        print("POST DEL LOGIN: ", request.POST)
        usuarios = User.objects.filter(email=request.POST['email'])
        if usuarios:
            usuario = usuarios[0]
            if bcrypt.checkpw(request.POST['password'].encode(), usuario.password.encode()):
                usuario_session = {
                    "id" : usuario.id,
                    "firstname": f"{usuario.firstname}",
                    "lastname": f"{usuario.lastname}",
                    "email": usuario.email
                }
                request.session['usuario'] = usuario_session
                messages.success(request, "Logeado correctamente")
                return redirect('/')
            else:
                messages.error(request, "La contraseña o el correo NO ES CORRECTO")
        else:
            messages.error(request, "La contraseña o el correo NO ES CORRECTO")
        return redirect("/login")


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect("/login")


def mensaje(request):
    if request.method == "POST":
        mensaje = request.POST['mensaje']
        usuarios = request.session['usuario']
        #print(usuarios['id'])
        #for user in usuarios:
            #print(user)
        #print(request.session['usuario'])
        mensajebd = Message.objects.create(
            usuariom_id = usuarios['id'],
            mensaje = request.POST['mensaje'],
        )
        return redirect("/wall")

def comentario(request):
    if request.method == "POST":
        usuario = request.session['usuario']
        id = usuario['id']
        user = User.objects.get(id=id)
        print(user)
        post = Message.objects.get(id=1)
        Comment.objects.create(
            comentario = request.POST['comentario'],
            author = user,
            mensajec = post
        )
        return redirect("/wall")