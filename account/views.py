import json,requests,jwt

from django.http          import JsonResponse
from django.views         import View

from .models              import Account
from my_settings          import SECRET_KEY, ALGORITHM
from utils.decorators     import login_required


class SocialAccountView(View):
    def get(self, request):
        access_token = request.headers.get('Authorization')
        response_from_kakao = requests.get(
            'https://kapi.kakao.com/v2/user/me',
            headers={"Authorization": f'Bearer {access_token}'}
        )
        dict_response = response_from_kakao.json()
        kakao_id      = dict_response.get('id')
        nickname      = dict_response['properties']['nickname']
        email         = dict_response['kakao_account']['email']

        if Account.objects.filter(kakao_id=kakao_id).exists():
            account          = Account.objects.get(kakao_id=kakao_id)
            conconsong_token = jwt.encode({'kakao_id': account.kakao_id},SECRET_KEY,ALGORITHM)
            return JsonResponse({'message': 'User logged in.', 'conconsong_token': conconsong_token}, status=200)
            
        Account.objects.create(
            email    = email,
            kakao_id = kakao_id,
            nickname = nickname,
        )
        account          = Account.objects.get(kakao_id=kakao_id)
        conconsong_token = jwt.encode({'id': account.id},SECRET_KEY,ALGORITHM)

        return JsonResponse({'message': 'New account registered.', 'conconsong_token': conconsong_token}, status=201)