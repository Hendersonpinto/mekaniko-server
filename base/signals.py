from django.db.models.signals import pre_save
from django.contrib.auth.models import User


def updateUser(sender, instance, **kwargs):
    # The instance is the actual object being saved
    user = instance

    # This will overwrite username with the email value, for all of our models
    if user.email != '':
        user.username = user.email


# We are running updateUser whenever a user is being pre_saved
pre_save.connect(updateUser, sender=User)
