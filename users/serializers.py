from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.validators import UniqueValidator
from django.utils.translation import ugettext_lazy as _
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    회원 읽기 Serializer
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "real_name",
            "phone_number",
        )


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    회원 생성 Serializer
    """

    token = serializers.SerializerMethodField()
    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    # 회원 생성시 JWT토큰 반환
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    # 회원가입 시 비멀번호 유효성 검사
    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    # 회원가입 시 비멀번호와 확인 비밀번호가 같은지 검사
    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError({"비밀번호": ["다시 확인해주세요"]})
        password_validation.validate_password(password, self.instance)
        return data

    # 회원가입 시 비밀번호 암호화 설정
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    # 핸드폰 번호가 이미 존재하는 번호인지 아닌지 검사
    def validate(self, data):
        phone_number = data.get("phone_number")
        check_query = User.objects.filter(phone_number=phone_number)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.pk)

        if self.parent is not None and self.parent.instance is not None:
            user = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=user.pk)

        if check_query.exists():
            raise serializers.ValidationError({"휴대폰 번호": ["이미 존재합니다."]})
        return data

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
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(), message=_("이미 존재합니다."),
                    )
                ]
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    """
    비밀번호 변경 Serializer
    """

    model = User
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        # 현재 비밀번호가 맞는지 확인 검사
        user = self.context["request"].user
        password = data.get("password")
        if not user.check_password(password):
            raise serializers.ValidationError({"비밀번호": ["잘못되었습니다."]})

        # 새 비밀번호 유효성 검사
        new_password = data.get("new_password")
        password_validation.validate_password(new_password, self.instance)

        # 새 비밀번호와 확인 비밀번호가 같은지 검사
        new_password_confirm = data.get("new_password_confirm")
        if new_password != new_password_confirm:
            raise serializers.ValidationError({"새 비밀번호": ["다시 확인해주세요"]})

        return data


class FindUsernameSerializer(serializers.Serializer):
    """
    회원 ID 찾기 Serializer
    """

    model = User
    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    # 입력한 정보에 해당하는 회원이 있는지 확인
    def validate(self, data):
        real_name = data.get("real_name")
        phone_number = data.get("phone_number")

        try:
            obj = User.objects.get(phone_number=phone_number)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"실패": ["입력하신 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다."]}
            )

        if not obj.real_name == real_name:
            raise serializers.ValidationError(
                {"실패": ["입력하신 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다."]}
            )
        return data


class FindPasswordSerializer(serializers.Serializer):
    """
    회원 Password 찾기 Serializer
    """

    model = User
    username = serializers.CharField(required=True)
    real_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    # 입력한 정보에 해당하는 회원이 있는지 확인
    def validate(self, data):
        username = data.get("username")
        real_name = data.get("real_name")
        phone_number = data.get("phone_number")

        try:
            obj = User.objects.get(username=username)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"실패": ["입력하신 ID와 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다."]}
            )

        if not (obj.real_name == real_name and obj.phone_number == phone_number):
            raise serializers.ValidationError(
                {"실패": ["입력하신 ID와 이름과 휴대폰번호에 해당하는 회원정보를 찾지 못했습니다."]}
            )
        return data
