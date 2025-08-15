from django.db import models
from decimal import Decimal

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    UNIDADES = [
        ('kg', 'Quilo (kg)'),
        ('cx', 'Caixa (Cx)'),
        ('un', 'Unidade'),
    ]

    nome = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=50, unique=True, blank=True, null=True)
    unidade = models.CharField(max_length=10, choices=UNIDADES, default='kg')
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nome} ({self.get_unidade_display()}) - R${self.preco:.2f}"

class Nota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Nota #{self.id} - {self.cliente.nome}"

class ItemNota(models.Model):
    nota = models.ForeignKey(Nota, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return Decimal(self.preco_unitario) * Decimal(self.quantidade)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - R${self.subtotal():.2f} (Nota #{self.nota.id})"

class PrecoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'data')

    def __str__(self):
        return f"{self.produto.nome} - R${self.preco:.2f} em {self.data.strftime('%d/%m/%Y')}"

