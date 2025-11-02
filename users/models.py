from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from pages.models import Template
from django.db.models.signals import post_save
import uuid


# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveBigIntegerField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.CharField(default=('No Bio added'), max_length=2555,blank=True, null=True)
    occupation = models.CharField(default=('No Occupation added'), max_length=50,blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('view_profile', args=[str(self.id)])


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=get_user_model())


class TemplatesOwned(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user  = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    template = models.CharField(max_length=36,blank=False, null=False)
    class Meta:
        db_table = 'TemplatesOwned'

    def __str__(self):
        return str(self.id)