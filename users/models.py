from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """ 회원 모델 정의 """

    real_name = models.CharField(_("real name"), max_length=150, blank=True)  # 회원 이름

    phone_number = models.CharField(
        _("phone number"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. digits only."),
        error_messages={"unique": _("이미 존재합니다."),},
    )  # 휴대폰 번호, Unique key로 설정
    favs = models.ManyToManyField(
        "locations.Location", related_name="favs"
    )  # "좋아요" 리스트, Location 과 다 대 다 관계
