from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'votacao'

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [

    # ex: votacao/
    path("", views.autenticar, name='autenticar'),

    # ex: votacao/logout/
    path("logout/", views.logoutview, name='logout'),

    # ex: votacao/Personal
    path("personal", views.paginapessoal, name='paginapessoal'),

    # ex: votacao/main
    path('main', views.index, name='index'),

    # ex: votacao/registo
    path('registo', views.registo, name='registo'),

    # ex: votacao/criarquestao
    path('criarquestao', views.criarquestao, name='criarquestao'),

    # ex: votacao/eliminarquestao
    path('eliminarquestao/', views.eliminarquestao, name='eliminarquestao'),

    # ex: votacao/5/criaropcao
    path('<int:questao_id>/criaropcao', views.criaropcao, name='criaropcao'),

    # ex: votacao/5/eliminaropcao
    path('<int:questao_id>/eliminaropcao/', views.eliminaropcao, name='eliminaropcao'),

    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),

    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),

    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),


]