from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Questao, Opcao, Aluno
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------

@login_required(login_url='/votacao/')
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')
    # Caso quem acede seja o admin e ele nao vota
    if not request.user.is_superuser:
        aluno = Aluno.objects.get(user_id=request.user.id)
        resultado = aluno.grupo + 10 - aluno.votos

        context = {
            'latest_question_list': latest_question_list, 'username': request.user.username, 'aluno': aluno,
            "resultado": resultado}

        return render(request, 'votacao/index.html', context)
    else:
        context = {
            'latest_question_list': latest_question_list, 'username': request.user.username}

        return render(request, 'votacao/index.html', context)


@login_required(login_url='/votacao/')
def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    aluno = Aluno.objects.get(user_id=request.user.id)
    resultado = aluno.grupo + 10 - aluno.votos

    context = {
        'aluno': aluno,
        "resultado": resultado,
        "questao": questao}

    return render(request, 'votacao/detalhe.html', context)


### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------
@login_required(login_url='/votacao/')
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    aluno = Aluno.objects.get(user_id=request.user.id)
    resultado = aluno.grupo + 10 - aluno.votos

    context = {
        'aluno': aluno,
        "resultado": resultado,
        "questao": questao}

    return render(request, 'votacao/resultados.html', context)


@login_required(login_url='/votacao/')
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    aluno = Aluno.objects.get(user_id=request.user.id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção"})
    else:
        if aluno.votos > 0:
            aluno.votos -= 1
            aluno.save()
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
            return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))
        else:
            return render(request, 'votacao/detalhe.html',
                          {'questao': questao, 'error_message': "Não tem votos suficientes", })


### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------

@login_required(login_url='/votacao/')
@permission_required('auth.is_superuser', login_url='/votacao/')
def criarquestao(request):
    if request.method == 'POST':
        try:
            questao_texto = request.POST.get("questao_texto")
        except KeyError:
            return render(request, 'votacao/criarquestao.html')
        if questao_texto:
            questao = Questao(questao_texto=questao_texto, pub_data=timezone.now())
            questao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:criarquestao'))

    return render(request, 'votacao/criarquestao.html')


@login_required(login_url='/votacao/')
@permission_required('auth.is_superuser', login_url='/votacao/')
def eliminarquestao(request):
    questoes = Questao.objects.all()
    if request.method == 'POST':
        try:
            questao_id = request.POST.get("questao_id")
        except KeyError:
            return render(request, 'votacao/eliminarquestao.html')
        if questao_id:
            questao_selecionada = Questao.objects.get(id=questao_id)
            questao_selecionada.delete()
            return HttpResponseRedirect(reverse('votacao:index'))
        else:
            return HttpResponseRedirect(reverse('votacao:eliminarquestao'))

    return render(request, 'votacao/eliminarquestao.html', {'questoes': questoes})


### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------

@login_required(login_url='/votacao/')
@permission_required('auth.is_superuser')
def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)

    if request.method == 'POST':
        try:
            opcao_texto = request.POST.get("opcao_texto")
        except KeyError:
            return render(request, 'votacao/criaropcao.html')
        if opcao_texto:
            votos = 0
            opcao = questao.opcao_set.create(opcao_texto=opcao_texto, votos=votos)
            opcao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:criaropcao'))

    return render(request, 'votacao/criaropcao.html', {'questao': questao})


@login_required(login_url='/votacao/')
@permission_required('auth.is_superuser')
def eliminaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        try:
            opcao_seleccionada = request.POST.get("opcao_id")
        except KeyError:
            return render(request, 'votacao/apagaropcao.html')
        if opcao_seleccionada:
            opcao_apagar = questao.opcao_set.get(pk=opcao_seleccionada)
            opcao_apagar.delete()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:eliminaropcao'))
    else:
        return render(request, 'votacao/eliminaropcao.html', {'questao': questao})


### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------


def registo(request):
    if request.method == 'POST':
        username = request.POST['user']
        mail = request.POST['mail']
        password = request.POST['pass']

        user = User.objects.create_user(username, mail, password)

        curso = request.POST['curso']
        aluno_user = Aluno(user=user, curso=curso)
        aluno_user.user.username
        aluno_user.save()

        return HttpResponseRedirect(reverse('votacao:autenticar'))

    return render(request, 'votacao/registo.html')


def autenticar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votacao:index'))
        else:
            error_message = "Username or password incorrect"
            return render(request, 'votacao/login.html', {'error_message': error_message})

    return render(request, 'votacao/login.html')


@login_required(login_url='/votacao/')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:autenticar'))

### -------------------- ### -------------------- ### -------------------- ### -------------------- ### -------------

@login_required(login_url='/votacao/')
def paginapessoal(request):
    aluno = Aluno.objects.get(user_id=request.user.id)
    resultado = aluno.grupo + 10 - aluno.votos

    context = {
        'aluno': aluno,
        "resultado": resultado}

    return render(request, 'votacao/paginapessoal.html', context)

@login_required(login_url='/votacao/')
def fazer_upload(request):

    aluno = Aluno.objects.get(user_id=request.user.id)
    resultado = aluno.grupo + 10 - aluno.votos

    context = {
        'aluno': aluno,
        "resultado": resultado}


    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # update user image
        aluno = Aluno.objects.get(user=request.user.id)
        aluno.avatar = uploaded_file_url
        aluno.save()

        context = {
            'aluno': aluno,
            "resultado": resultado,
            "uploaded_file_url": uploaded_file_url
        }

        return render(request, 'votacao/fazer_upload.html', context)
    return render(request, 'votacao/fazer_upload.html', context)
