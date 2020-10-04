from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    """ Photo Model Definition """

    image = ProcessedImageField(
        upload_to="location_photos",  # 저장 위치
        processors=[ResizeToFill(1280, 720)],  # 처리할 작업 목록
        format="JPEG",  # 저장 포맷(확장자)
        options={"quality": 90},  # 저장 포맷 관련 옵션 (JPEG 압축률 설정)
    )
    location = models.ForeignKey(
        "Location", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.location.name

    class Meta:
        ordering = ("-pk",)


class Location(models.Model):
    """Location Model Definition"""

    creator = models.ForeignKey(
        "users.User", related_name="locations", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=140)
    description = models.TextField(default="")
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lon = models.DecimalField(max_digits=10, decimal_places=6)
    category = models.CharField(max_length=140)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.name
