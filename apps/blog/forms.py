# -*- coding: utf-8 -*-
from apps.blog.models import Post
from apps.blog.models import Comment, PerfilUser
from django.forms.widgets import Textarea
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def check_size(value):
    if len(value) < 5 or len(value) > 30:
        raise ValidationError("Title shouldn't have less than 5 and more than 30 chars")


def check_size_comment(value):
    if len(value) < 2:
        raise ValidationError("Title should be at least 2 characters long man.")


def without_asterix(value):
    if "*" in value:
        raise ValidationError("Value can't contain an asterix char")


class PostForm_0(forms.Form):
    title = forms.CharField(required=True, help_text="Help text here")
    content = Textarea(attrs={'cols': 60, 'rows': 15})


def check_title(value):
    if len(value) < 4:
        raise ValidationError("El titulo debe contener mas de 4 caracteres")
    return value


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['title'].help_text = "Aqui va el titulo del post"
        self.fields['title'].label = 'Titulo'
        self.fields['title'].validators = [without_asterix, check_size]

    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 15}),
        }


class CommentForm(forms.ModelForm):
    """Comments form for the posts"""
    #content = forms.TextField(required=True, help_text="Comenta aqui", label="Comentario", validators=[without_asterix, check_size_comment])
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': Textarea(attrs={'cols': 30, 'rows': 4}),
        }


class UserRegisterForm(forms.ModelForm):
    """ Form to create user"""
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(u"Contraseña erronea")
                #self.error_messages['password_mismatch'])
        return password2

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PerfilUserForm(forms.ModelForm):
    """ Form to load extended user information"""
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end
        super(PerfilUserForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)

    def save(self, *args, **kwargs):
        # save both forms
        self.uf.save(*args, **kwargs)
        return super(PerfilUserForm, self).save(*args, **kwargs)

    #first_name = forms.CharField(label="Nombre", required=False)
    #last_name = forms.CharField(label="Apellido", required=False)

    class Meta:
        model = PerfilUser
        fields = ('genre', 'birth_date')