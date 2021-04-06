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

from django.db.models import Prefetch

from django.http           import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views          import View
from django.db.models      import Q

from product.models        import Product, Collection, Color, Size
            

class ProductFilterView(View):
    def get(self, request):

        OFFSET = int(request.GET.get('limit', 8)) * int(request.GET.get('offset', 0))
        LIMIT  = int(request.GET.get('limit', 8)) + OFFSET

        collections = request.GET.getlist('collection_id', None)
        colors      = request.GET.getlist('color_id', None)
        sizes       = request.GET.getlist('size_id', None)

        q = Q()

        if collections:
            q &= Q(collection__in=collections)

        if colors:
            q &= Q(color__in=colors)

        if sizes:
            q &= Q(size__in=sizes)


        products = Product.objects.prefetch_related('productsize_set', 'size_set')\
                                  .filter(q)\
                                  .order_by('-created_at')[OFFSET:LIMIT]

        product = [
            {
                'id'        : product.id,
                'name'      : product.name,
                'price'     : product.price,
                'image'     : [image.url for image in product.image_set.filter(product_id=product.id)]
            }for product in products
        ]

        filter_detail = [
            {
                'collection' : [collection.name for collection in Collection.objects.all()] ,
                'color'      : [color.name for color in Color.objects.all()],
                'size'       : [size.name for size in Size.objects.all()]
            }
        ]

        return JsonResponse({'product' : product, 'filter_detail': filter_detail}, status=200)









