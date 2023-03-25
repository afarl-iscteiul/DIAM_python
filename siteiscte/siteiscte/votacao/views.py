import datetime


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone

from .models import Questao, Opcao, Aluno
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def voto(request, questao_id):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    questao = get_object_or_404(Questao, pk=questao_id)
    aluno = Aluno.objects.get(user_id=request.user.id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        if aluno.votos > 0:
            aluno.votos -= 1
            aluno.save()
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
            return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))
        else:
            return render(request, 'votacao/detalhe.html',
                          {'questao': questao, 'error_message': "Não tem votos suficientes",})


def criarquestao(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
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
    else:
        return render(request, 'votacao/criarquestao.html')


def eliminarquestao(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
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
    else:
        return render(request, 'votacao/eliminarquestao.html', {'questoes': questoes})


def registo(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        curso = request.POST.get("curso")
        user = User.objects.create_user(username, email, password)
        # user.save()
        novouser = Aluno(user=user, curso=curso)
        novouser.user.username
        novouser.save()
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/registo.html')


def criaropcao(request, questao_id):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        try:
            opcao_texto = request.POST.get("opcao_texto")
        except KeyError:
            return render(request, 'votacao/criaropcao.html')
        if opcao_texto:
            votos = 0
            opcao = Opcao(questao=questao, opcao_texto=opcao_texto, votos=votos)
            opcao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:criaropcao'))
    else:
        return render(request, 'votacao/criaropcao.html', {'questao': questao})


def eliminaropcao(request, questao_id):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login.html')
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
            return HttpResponseRedirect(reverse('votacao:apagaropcao'))
    else:
        return render(request, 'votacao/apagaropcao.html', {'questao': questao})


def autenticar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votacao:index'))
        else:
            error_message = "Username ou passwords incorretos!"
            return render(request, 'votacao/login.html', {'error_message': error_message})
    else:
        return render(request, 'votacao/login.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))

def loginerror(request):
    if not request.user.is_authenticated:
        return render(request, 'votacaologinerror.html')
