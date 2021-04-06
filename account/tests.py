import unittest
import requests,jwt

from unittest.mock  import MagicMock,patch

from django.test    import TestCase, Client

from .models        import Account


class AccountTest(TestCase):

#-----------fixture setting
    def setUp(self):
        client = Client()
        account_testing = Account(
            email    = 'nicky@gmail.com',
            nickname = 'nicky',
            kakao_id = '123456'
        )
        account_testing.save()

    def tearDown(self):
        Account.objects.all().delete()

#----------Test for sign-in
    @patch('account.views.requests')
    def test_get_signin(self,mock_request):
        client = Client()

        class MockResponse:
            def json(self):
                return  {
                    'kakao_account':{'email':'nicky@gmail.com'},
                    'properties' : {'nickname':'nicky'},
                    'id' : '123456'
                }

        mock_request.get = MagicMock(return_value=MockResponse())
        header = {'Authorization': 'access_token'}
        response = client.get(
            '/account/social-login',
            ContentType ='application/json',
            **header
            )
        self.assertEqual(response.status_code, 200)

    def test_get_not_found(self):
        client = Client()
        header = {'Authorization': 'access_token'}
        response = client.get(
            '/wrongwrong',
            ContentType ='application/json',
            **header
            )
        self.assertEqual(response.status_code, 404)