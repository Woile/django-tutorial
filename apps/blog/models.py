from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Post(models.Model):
    author = models.ForeignKey(User, null=True)
    title = models.CharField(blank=False, max_length=100)
    content = models.TextField(blank=False, max_length=40)
    datetime = models.DateTimeField(blank=True, auto_now_add=True)
    visits = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    datetime = models.DateTimeField(blank=True, auto_now_add=True)
    content = models.TextField(blank=False, max_length=100)

    class Meta:
        ordering = ['-datetime']

class PerfilUser(models.Model):
    user = models.OneToOneField(User)
    GENRE_CHOICES = (
        ('m', 'Masculino'),
        ('f', 'Femenino'),
    )
    AUTHORIZATION = (
        ('Y', 'YES'),
        ('N', 'NO'),
    )
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, null=True)
    birth_date = models.DateField(null=True)
    create_post = models.CharField(max_length=1, choices=AUTHORIZATION, null=True)
    comment = models.CharField(max_length=1, choices=AUTHORIZATION, null=True)

# Used ONLY when creted an User, this will create an empty PerfilUser
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUser.objects.create(user=instance)

# This signal is sent after the save is done, so, after a User is created
post_save.connect(create_user_profile, sender=User)


