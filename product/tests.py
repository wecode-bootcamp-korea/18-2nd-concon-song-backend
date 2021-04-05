from django.test import TestCase, Client
from .models     import Product, Collection, Size, ProductSize, Image, ProductDetail, Color


client = Client()

class ProductDetailTestCase(TestCase):
    def setUp(self):
        collection = Collection.objects.create(name='soo1902')
        color      = Color.objects.create(name='red')

        product    = Product.objects.create(
            collection   = collection,
            name         = 'chuck70',
            price        = 75000,
            color        = color)
        size = Size.objects.create(name=230)

        productsize = ProductSize.objects.create(
            product_id = product.id,
            size_id    = size.id
        )

        Image.objects.bulk_create(
            [
                Image(product_id = product.id, url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product_id = product.id, url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product_id = product.id, url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product_id = product.id, url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg'),
                Image(product_id = product.id, url='https://image.converse.co.kr/cmsstatic/menu/12751/Flyout_256x300_02-7.jpg')
            ]
        )
        ProductDetail.objects.create(
            product_id      = product.id,
            introduction = "모든 분위기에 어울리는 컬러로 출시된 최고의 아이콘",
            description  = "1970년대의 척테일러에서 영감 받은 척 70 컬렉션은 더욱 편안한 쿠셔닝과 견고한 캔버스 어퍼, 세련된 디테일을 더해 재해석되었습니다. 아이코닉한 디자인과 빈티지한 매력, 편안한 착화감을 동시에 선사하는 척 70 컬렉션과 함께 더욱 활기찬 일상을 맞이하세요."
        )

    def tearDown(self):
        Collection.objects.all().delete()
        Product.objects.all().delete()
        Size.objects.all().delete()
        ProductSize.objects.all().delete()
        Image.objects.all().delete()
        ProductDetail.objects.all().delete()

    def test_productdetail_get_success(self):
        response = client.get('/product/1')
        self.assertEqual(response.status_code, 200)  

    def test_productdetail_not_found(self):
        response = client.get('/product/101')
        self.assertEqual(response.status_code, 404)