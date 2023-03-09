from votacao.models import Questao, Opcao

def __totalNumeroVotos__():
    numero_votos = 0
    lista_votos = Opcao.objects.all()
    for opcao in lista_votos:
        numero_votos += opcao.votos
    return numero_votos

def __opcaoComMaisVotosPorQuestao__():
    lista_questoes = Questao.objects.all()
    for questao in lista_questoes:
        # opcao = questao.opcao_set.all()
        opcao = questao.opcao_set.filter().order_by('-votos')[:1].get()
        print(f'questao: {questao.__str__()} \n'
              f'opcao com mais votos : {opcao} com {opcao.votos} votos')


