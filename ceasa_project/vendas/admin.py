from django.contrib import admin
from .models import Cliente, Produto, Nota, ItemNota

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(Nota)
admin.site.register(ItemNota)
