from rest_framework import serializers
from . import models


class PhotoSerializer(serializers.ModelSerializer):
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

    # 다중 이미지 처리
    def create(self, validated_data):
        images_data = self.context["request"].FILES
        location = models.Location.objects.create(**validated_data)
        for images_data in images_data.getlist("image"):
            models.Photo.objects.create(location=location, image=images_data)
        return location

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False
