
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    lastpage = models.IntegerField(null=True, blank=True, default=1)
    verified = models.BooleanField(default=False)
    email_uid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=Profile)
def verification_email(sender, instance, created, **kwargs):
	if not instance.verified:
		send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(instance.email_uid)}),
            from_email = 'snehithjk@gmail.com',
            recipient_list = ['snehithjk@outlook.com'],
            fail_silently=False,
        )
