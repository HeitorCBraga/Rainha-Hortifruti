from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

from .models import Cliente, Produto, Nota, ItemNota

def index(request):
    return render(request, 'vendas/index.html')

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'vendas/listar_produtos.html', {'produtos': produtos})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'vendas/listar_clientes.html', {'clientes': clientes})

def nova_venda(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Cliente.objects.get(id=cliente_id)

        nota = Nota.objects.create(cliente=cliente, data=timezone.now())

        produtos = request.POST.getlist('produto')
        quantidades = request.POST.getlist('quantidade')
        precos = request.POST.getlist('preco_unitario')

        for i in range(len(produtos)):
            produto = Produto.objects.get(id=produtos[i])
            quantidade = float(quantidades[i])
            preco_unitario = float(precos[i])

            ItemNota.objects.create(
                nota=nota,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario
            )

        return redirect('index')

    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'vendas/nova_venda.html', {
        'clientes': clientes,
        'produtos': produtos
    })

def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        localizacao = request.POST.get('localizacao')
        Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone, localizacao=localizacao)
        return redirect('clientes')
    return render(request, 'vendas/novo_cliente.html')


def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone)
        return redirect('clientes')
    return render(request, 'vendas/novo_cliente.html')

def novo_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        Produto.objects.create(nome=nome, preco=preco)
        return redirect('produtos')
    return render(request, 'vendas/novo_produto.html')


def listar_notas(request):
    notas = Nota.objects.select_related('cliente').order_by('-data')
    return render(request, 'vendas/listar_notas.html', {'notas': notas})

def detalhe_nota(request, nota_id):
    nota = Nota.objects.get(id=nota_id)
    itens = ItemNota.objects.filter(nota=nota).select_related('produto')
    total = sum(item.quantidade * item.preco_unitario for item in itens)
    return render(request, 'vendas/detalhe_nota.html', {
        'nota': nota,
        'itens': itens,
        'total': total
    })

def nota_pdf(request, nota_id):
    nota = Nota.objects.get(id=nota_id)
    itens = ItemNota.objects.filter(nota=nota).select_related('produto')
    total = sum(item.quantidade * item.preco_unitario for item in itens)

    html_string = render_to_string('vendas/nota_pdf.html', {
        'nota': nota,
        'itens': itens,
        'total': total
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=nota_{nota.id}.pdf'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        HTML(string=html_string).write_pdf(output.name)
        output.seek(0)
        response.write(output.read())

    return response
