from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# from six import string_types
import datetime


class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.questao_texto

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)

    # Cada utilizador tem um limite para o número de votos que pode realizar no site.
    # Esse limite é definido pelo número do seu grupo de trabalho acrescido de 10.
    # Por exemplo, para o grupo “LIGEPL10” o limite é 20; para “LEI-22” o limite é 32; para “TB-03” o limite é 13; e assim por diante.
    numero_grupo=12
    grupo = models.IntegerField(default=numero_grupo)
    votos = models.IntegerField(default=numero_grupo + 10)
    avatar = models.ImageField(default='default_avatar.jpg')
