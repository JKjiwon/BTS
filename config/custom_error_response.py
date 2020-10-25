from rest_framework.views import exception_handler

dict_word = {
    "username": "ID",
    "real_name": "이름",
    "phone_number": "휴대폰 번호",
    "password": "비밀번호",
    "password_confirm": "비밀번호 확인",
    "old_password": "비밀번호",
    "new_password": "새 비밀번호",
    "new_password_confirm": "새 비밀번호 확인",
}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if hasattr(exc.detail, "items"):
            response.data = {}
            errors = []
            result = ""

            for key, value in exc.detail.items():
                if key in dict_word.keys():
                    key = dict_word[key]
                errors.append("{} : {}".format(key, "\n".join(value)))

            for s in errors:
                result += f"{s}\n"
            result = result[:-1]
            response.data["errors"] = result

    return response
