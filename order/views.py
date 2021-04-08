import json, jwt
from   json import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View

from account.models   import Account
from product.models   import Product, ProductSize, Image
from .models          import Order, Cart, Status

from utils.decorators import login_required


class OrderView(View):
    @login_required
    def post(self,request,product_id):
        try:
            data       = json.loads(request.body)
            account_id = request.account.id
            quantity   = data['quantity']
            size_id    = data['size_id']
            status_obj = Status.objects.get(id=1)
            product_size_obj   = ProductSize.objects.get(product_id=product_id,size_id=size_id)

            order = Order.objects.create(
                account_id = account_id,
                status_id  = status_obj.id,
            )

            Cart.objects.create(
                    product_size_id = product_size_obj.id,
                    order_id        = order.id,
                    quantity        = quantity
                )
            return JsonResponse({'message':'SUCCESSS'}, status=201)

            if Cart.objects.filter(product_size_id.product.id).exists():
                
                cart_updated_quantity = Cart(quantity=+int(quantity)).save()

                return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400) 

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)