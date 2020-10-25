from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["GET"])
def validate_jwt_token(request):

    try:
        token = request.META["HTTP_AUTHORIZATION"]
        data = {"token": token.split()[1]}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
    except Exception as e:
        return Response(e)

    return Response(status=status.HTTP_200_OK, data={"result": "token is valid"})


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):
        serializer = self.get_serializer(data=get_request_data(request))

        serializer.is_valid(raise_exception=True)  # pass the 'raise_exception' flag
        user = serializer.object.get("user") or request.user
        token = serializer.object.get("token")
        response_data = jwt_response_payload_handler(token, user, request)
        return Response(response_data)
