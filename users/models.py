from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    real_name = models.CharField(_("real name"), max_length=150, blank=True)

    phone_number = models.CharField(
        _("phone number"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. digits only."),
        error_messages={"unique": _("A user with that phone number already exists."),},
    )
    favs = models.ManyToManyField("locations.Location", related_name="favs")
