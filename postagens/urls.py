from django.urls import path
from postagens.views import (
    cria_post_view,
    detalhes_post_view,
    edita_post_view,
    deleta_post_view,
    deletar_post_view,
    verifica_titulo,
)

app_name= 'postagens'

urlpatterns = [
    path('cria/', cria_post_view, name="cria"),
    path('<slug>/', detalhes_post_view, name="detalhe"),
    path('<slug>/edit/', edita_post_view, name="edita"),
    path('<slug>/delete', deleta_post_view, name="apaga"),
    path('<slug>/deleted', deletar_post_view, name="apagar"),
    path('<slug>/verificaTitulo/', verifica_titulo,name='verificaTitulo'),
]