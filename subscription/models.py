from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class Sub(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )
    startDate = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'Sub'
        ordering = ['-user']

    def __str__(self):
        return str(self.id)

def create_sub(sender, instance, created, **kwargs):
    if created:
        user_profile = Sub(user=instance)
        user_profile.save()


post_save.connect(create_sub, sender=get_user_model())