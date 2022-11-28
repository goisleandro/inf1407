from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from conta.forms import RegistroForm, AutenticacaoForm, AtualizaContaForm
from conta.models import Conta
from postagens.models import Postagem
from django.http import JsonResponse

def tela_inicial_view(request):
    
    context = {}
    postagem_blog = sorted(Postagem.objects.all(), key=attrgetter('data_atualizacao'), reverse=True)
    context['postagem_blog'] = postagem_blog

    return render(request, "conta/home.html", context)

def registro_view(request):
    context = {}
    if request.POST:
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            conta = authenticate(email=email, password=raw_password)
            login(request, conta)
            return redirect('tela-inicial')
        else:
            context['registro_form'] = form
    else:
        #request.GET
        form = RegistroForm()
        context['registro_form'] = form
    
    return render(request, 'conta/registro.html', context)

def logout_view(request):
    logout(request)
    return redirect('tela-inicial')

def login_view(request):
    context = {}

    user = request.user
    #usuário já se encontra logado
    if user.is_authenticated:
        return redirect("tela-inicial")

    #usuário tentou logar (preencheu login e senha) e formulário precisa ser autenticado
    if request.POST:
        form = AutenticacaoForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("tela-inicial")
    else: #usuário não tentou logar e se encontra na página de login
        form = AutenticacaoForm()

    context['login_form'] = form
    return render(request, 'conta/login.html', context)

def atualiza_view(request):
    if not request.user.is_authenticated:
        return redirect("tela-login")

    context = {}

    if request.POST:
        form = AtualizaContaForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['msg_sucesso'] = "Alteração salva!"
    else:
        form = AtualizaContaForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['conta_form'] = form

    postagens_blog = Postagem.objects.filter(autor=request.user)
    context['postagens_blog'] = postagens_blog

    return render(request, 'conta/atualiza.html', context)

def precisa_autenticar_view(request):
    return render(request, 'conta/precisa-autenticar.html', {})

def verifica_titulo(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("tela-precisa-autenticar")
    postagem_blog = get_object_or_404(Postagem, slug=slug)
    if postagem_blog.autor != user:
        return HttpResponse('Você não é o autor desta postagem.')

    
    titulo = request.GET.get("id_title", None)
    resposta = {
        'existe':
            Postagem.objects.filter(id_title__iexact=titulo).exists()
    }
    return JsonResponse(resposta)