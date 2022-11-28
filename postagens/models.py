from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

def caminho_upload(instance, filename, **kwargs):
    file_path = 'blog/{autor_id}/{titulo}-{filename}'.format(
       autor_id = str(instance.autor.id), titulo=str(instance.titulo), filename=filename
    )
    return file_path

class Postagem(models.Model):
    titulo = models.CharField(max_length=50, null=False, blank=False)
    corpo = models.TextField(max_length=5000, null=False, blank=False)
    imagem = models.ImageField(upload_to=caminho_upload, blank=False)
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #slug cria uma URL automaticamente para as postagens
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.titulo

@receiver(post_delete, sender=Postagem)
def delete_submissao(sender, instance, *args, **kwargs):
    instance.imagem.delete(False)

def pre_salvar_postagem_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.autor.username + "-" + instance.titulo)

pre_save.connect(pre_salvar_postagem_receiver, sender=Postagem)
