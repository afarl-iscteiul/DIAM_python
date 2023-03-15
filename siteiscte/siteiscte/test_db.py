from votacao.models import Questao, Opcao


def calculaTotalvotos():
    numero_votos = 0
    lista_votos = Opcao.objects.all()
    for opcao in lista_votos:
        numero_votos += opcao.votos
    return numero_votos


if __name__ == '__main__':
    calculaTotalvotos()
