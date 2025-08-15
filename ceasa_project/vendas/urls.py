from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),

    # Clientes
    path('clientes/', views.listar_clientes, name='clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),

    # Produtos
    path('produtos/', views.listar_produtos, name='produtos'),
    path('produtos/novo/', views.novo_produto, name='novo_produto'),

    # Vendas
    path('venda/', views.nova_venda, name='nova_venda'),

    # Notas fiscais
    path('notas/', views.listar_notas, name='listar_notas'),
    path('notas/<int:nota_id>/', views.detalhe_nota, name='detalhe_nota'),
    path('notas/<int:nota_id>/pdf/', views.nota_pdf, name='nota_pdf'),
]
