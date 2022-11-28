from django import forms

from postagens.models import Postagem

class CriaFormularioDaPostagem(forms.ModelForm):

    class Meta:
        model = Postagem
        fields = ['titulo', 'corpo', 'imagem']


class AtualizaFormPostagem(forms.ModelForm):

    class Meta:
        model = Postagem
        fields = ['titulo', 'corpo', 'imagem']

    def save(self, commit=True):
        postagem_blog = self.instance
        postagem_blog.titulo = self.cleaned_data['titulo']
        postagem_blog.corpo = self.cleaned_data['corpo']

        if self.cleaned_data['imagem']:
            postagem_blog.imagem = self.cleaned_data['imagem']

        if commit:
            postagem_blog.save()
        return postagem_blog

class DeletaFormPostagem(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo', 'corpo', 'imagem']

    def delete(self, commit=True):
        postagem_blog = self.instance
        postagem_blog.titulo = self.cleaned_data[None]
        postagem_blog.corpo = self.cleaned_data[None]
        postagem_blog.imagem = self.cleaned_data[None]
        return postagem_blog