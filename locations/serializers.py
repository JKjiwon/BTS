from rest_framework import serializers
from . import models


class PhotoSerializer(serializers.ModelSerializer):
    """
    사진에 대한 Serializer
    """

    location = serializers.SlugRelatedField(
        queryset=models.Location.objects.all(), slug_field="name"
    )

    class Meta:
        model = models.Photo
        fields = (
            "pk",
            "url",
            "location",
            "image",
        )


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    장소에 대한 Serializer
    """

    creator = serializers.ReadOnlyField(source="creator.username")
    photos = PhotoSerializer(many=True, read_only=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = models.Location
        fields = (
            "is_fav",
            "creator",
            "pk",
            "url",
            "category",
            "name",
            "description",
            "address",
            "lat",
            "lon",
            "city",
            "photos",
        )

    def create(self, validated_data):
        """
        장소를 생성할때 이미지를 여러개 추가 할 수 있도록 설정
        """
        images_data = self.context["request"].FILES
        location = models.Location.objects.create(**validated_data)
        for images_data in images_data.getlist("image"):
            models.Photo.objects.create(location=location, image=images_data)
        return location

    def get_is_fav(self, obj):
        """
        "좋아요" 기능 , 로그인한 사용자가 "좋아요" 항목에 추가한 장소를 보여줄수 있도록 설정
        """
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False
