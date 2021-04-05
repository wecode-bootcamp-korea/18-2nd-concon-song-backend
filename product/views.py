import json
from json import JSONDecodeError

from django.http      import JsonResponse, HttpResponse
from django.views     import View

from product.models        import Product


class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product  = Product.objects.get(id=product_id)

            results = [
                {
                    'id'                 : product.id,
                    'collection'         : product.collection.name,
                    'name'               : product.name,
                    'introduction'       : product.productdetail_set.get(id=product_id).introduction,
                    'price'              : product.price,
                    'size'               : [
                        size.size.name
                        for size in product.productsize_set.filter(product_id=product_id)
                    ],
                    'images'             : [
                        image.url 
                        for image in product.image_set.filter(product_id=product_id)
                        ],
                    'description'        : product.productdetail_set.get(id=product_id).description,
                    'related_collection' : [
                        {
                            'id'    : related_product.id,
                            'image' : related_product.image_set.filter(product_id=related_product.id).first().url 
                                        if related_product.image_set.filter(product_id=related_product.id) else ""
                        } for related_product in Product.objects.filter(collection_id = product.collection.id)]
                }
            ]
            
            return JsonResponse({'results':results}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product_DOES_NOT_EXIST'}, status=404)
