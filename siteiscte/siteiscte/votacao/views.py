import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Questao, Opcao, Aluno
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
        return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))


def criarquestao(request):
    if request.method == 'POST':
        questao_texto = request.POST.get("questao_texto")
        questao = Questao(questao_texto=questao_texto, pub_data=datetime.datetime.now())
        questao.save()
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/criarquestao.html')


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
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        opcao_texto = request.POST.get("opcao_texto")
        votos = 0
        opcao = Opcao(questao=questao, opcao_texto=opcao_texto, votos=votos)
        opcao.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    else:
        return render(request, 'votacao/criaropcao.html', {'questao': questao})


def eliminaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        opcao_seleccionada = request.POST.get("opcao_id")
        # opcao_apagar = get_object_or_404(Opcao, id=opcao_seleccionada)
        opcao_apagar = questao.opcao_set.get(pk=opcao_seleccionada)
        opcao_apagar.delete()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    else:
        return render(request, 'votacao/criaropcao.html', {'questao': questao})


def autenticar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/login.html')


def logout(request):
    logout(request)
    # direcionar pag sucesso


def umaview(request):
    if not request.user.is_authenticated:
        return render(request, 'votacao/login_error.html')
