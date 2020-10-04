from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "real_name",
            "phone_number",
        )


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError({"password": "비밀번호를 확인해주세요"})
        password_validation.validate_password(password, self.instance)
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    # 핸드폰 번호가 유효한지, 즉 이미 존재하는 번호인지 아닌지를 체크한다.
    def validate_phone_number(self, value):
        check_query = User.objects.filter(phone_number=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.pk)

        if self.parent is not None and self.parent.instance is not None:
            user = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=user.pk)

        if check_query.exists():
            raise serializers.ValidationError("해당 사용자 휴대폰 번호은 이미 존재합니다.")
        return value

    class Meta:
        model = User
        fields = (
            "token",
            "username",
            "real_name",
            "phone_number",
            "password",
            "password_confirm",
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class FindUsernameSerializer(serializers.Serializer):
    model = User

    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def validate(self, data):
        real_name = data.get("real_name")
        phone_number = data.get("phone_number")

        try:
            obj = User.objects.get(phone_number=phone_number)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"오류": "입력하신 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다. 다시 확인해주세요."}
            )

        if not obj.real_name == real_name:
            raise serializers.ValidationError(
                {"오류": "입력하신 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다. 다시 확인해주세요."}
            )
        return data


class FindPasswordSerializer(serializers.Serializer):
    model = User

    username = serializers.CharField(required=True)
    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get("username")
        real_name = data.get("real_name")
        phone_number = data.get("phone_number")

        try:
            obj = User.objects.get(username=username)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "입력하신 ID와 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다. 다시 확인해주세요."}
            )

        if not (obj.real_name == real_name and obj.phone_number == phone_number):
            raise serializers.ValidationError(
                {"error": "입력하신 ID와 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다. 다시 확인해주세요."}
            )
        return data
