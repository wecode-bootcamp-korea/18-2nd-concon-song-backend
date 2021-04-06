import json,bcrypt,jwt

from django.http    import JsonResponse

from account.models import Account
from my_settings    import SECRET_KEY, ALGORITHM


def login_required (func):
    def wrapper (self, request, *args, **kwargs):
        try:
            conconsong_token = request.headers.get('Authorization')
            decoded_token    = jwt.decode(conconsong_token, SECRET_KEY, algorithms= ALGORITHM)

            if not Account.objects.filter(id=decoded_token['id']).exists():
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

            request.account  = Account.objects.get(id=decoded_token['id'])
            return func(self, request, *args,**kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=401)

    return wrapper