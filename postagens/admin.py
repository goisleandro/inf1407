from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from postagens.models import Postagem

class ContaAdmin(UserAdmin):
    list_display = ('titulo')
    search_fields = ('titulo',)
    readonly_fields = ('data_publicacao', 'data_atualizacao',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Postagem)