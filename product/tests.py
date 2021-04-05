from django.test import TestCase, Client
from .models     import Product, Collection, Size, ProductSize, Image, ProductDetail

#임시 testDb 생김, 우리 schema 가지고! 알고 짜기
class ProductDetailTestCase(TestCase):
    def setUp(self):
        client = Client()
        Collection.objects.create(name='soo1902')
        Product.objects.create(
            id           = 1,
            collection   = Collection.objects.get(id=1),
            name         = 'chuck70',
            price        = 75000.00
        )
        Size.objects.bulk_create([
                Size(name=230),
                Size(name=240),
                Size(name=250),
                Size(name=260)
            ])
        ProductSize.objects.create(
            Product = Product.objects.get(id=1),
            Size = Size.objects.get(id=1)
        )
        ProductSize.objects.create(
            Product = Product.objects.get(id=1),
            Size = Size.objects.get(id=2)
        )
        ProductSize.objects.create(
            Product = Product.objects.get(id=1),
            Size = Size.objects.get(id=3)
        )
        ProductSize.objects.create(
            Product = Product.objects.get(id=1),
            Size = Size.objects.get(id=4)
        )
        Image.objects.bulk_create(
            [
                Image(product = Product.objects.get(id=1), url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product = Product.objects.get(id=1), url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product = Product.objects.get(id=1), url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product = Product.objects.get(id=1), url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product = Product.objects.get(id=1), url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg')
            ]
        )
        ProductDetail.objects.create(
            product = Product.objects.get(id=2),
            introduction = "모든 분위기에 어울리는 컬러로 출시된 최고의 아이콘",
            description = "1970년대의 척테일러에서 영감 받은 척 70 컬렉션은 더욱 편안한 쿠셔닝과 견고한 캔버스 어퍼, 세련된 디테일을 더해 재해석되었습니다. 아이코닉한 디자인과 빈티지한 매력, 편안한 착화감을 동시에 선사하는 척 70 컬렉션과 함께 더욱 활기찬 일상을 맞이하세요."
        )

    def tearDown(self):
        Collection.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Image.objects.all().delete()
        ProductDetail.objects.all().delete()

    def test_productdetail_get_success(self):
        client = Client()
        response = client.get('/product/1')
        self.assertEqual(response.json(),
            {
                "result": 
                [{
                    "collection": "soo1902",
                    "description": "척 70\n1970년대의 척테일러에서 영감 받은 척 70 컬렉션은 더욱 편안한 쿠셔닝과 견고한 캔버스 어퍼, 세련된 디테일을 더해 재해석되었습니다. 아이코닉한 디자인과 빈티지한 매력, 편안한 착화감을 동시에 선사하는 척 70 컬렉션과 함께 더욱 활기찬 일상을 맞이하세요.",
                    "id": 1,
                    "images": [
                        "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg",
                        "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg",
                        "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg",
                        "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg",
                        "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg"
                    ],
                    "introduction": "디자인 헤리티지를 더한 프리미엄 컴포트 스니커즈",
                    "name": "Heart Of The City Pro Leather",
                    "price": "85000",
                    "related_collection": [
                        {
                            "id": 1,
                            "image": "https://image.converse.co.kr/cmsstatic/menu/12723/Flyout_256x300_01-7.jpg"},
                        {
                            "id": 2,
                            "image": "https://image.converse.co.kr/cmsstatic/product/170463C_170463C_primary.jpg?browse"},
                        {
                            "id": 3,
                            "image": ""}],
                    "size": ["230", "240", "250", "260"]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)  

    def test_productdetail_get_fail(self):
        client = Client()
        response = client.get('/product/2')
        self.assertEqual(response.json(),
            {
                'message':'NO_Detail'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_productdetail_not_found(self):
        client = Client()
        response = client.get('/product/')
        self.assertEqual(response.status_code, 404)