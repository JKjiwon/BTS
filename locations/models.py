from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    """ Photo 모델 정의 """

    image = ProcessedImageField(
        upload_to="location_photos",  # 저장 위치
        processors=[ResizeToFill(1280, 720)],  # 처리할 작업 목록
        format="JPEG",  # 저장 포맷(확장자)
        options={"quality": 90},  # 저장 포맷 관련 옵션 (JPEG 압축률 설정)
    )
    location = models.ForeignKey(
        "Location", related_name="photos", on_delete=models.CASCADE
    )  # 사진의 장소,  Location 의 ForeignKey

    def __str__(self):
        return self.location.name

    class Meta:
        ordering = ("-pk",)  # 나중에 생성된 장소가 맨위에 오도록 정렬


class Location(models.Model):
    """장소 모델 정의"""

    creator = models.ForeignKey(
        "users.User", related_name="locations", on_delete=models.CASCADE
    )  # 장소 생성자, User의 ForeignKey
    name = models.CharField(max_length=140)  # 장소이름
    description = models.TextField(default="")  # 장소설명
    city = models.CharField(max_length=80)  # 도시명
    address = models.CharField(max_length=150)  # 주소
    lat = models.DecimalField(max_digits=10, decimal_places=6)  # 위도
    lon = models.DecimalField(max_digits=10, decimal_places=6)  # 경도
    category = models.CharField(max_length=140)  # 장소 카테고리

    class Meta:
        ordering = ("-pk",)  # 나중에 생성된 장소가 맨위에 오도록 정렬

    def __str__(self):
        return self.name
