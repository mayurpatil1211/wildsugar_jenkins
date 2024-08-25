from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue


#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

import logging

logger = logging.getLogger('debug_file')

User = get_user_model()

class BrandApiView(APIView):
    # permission_class = (AllowAny,) 
    @authorize('register_brand')
    def post(self, request):
        user = request.data.get('user', None)
        brand_name = request.data.get('brand_name', None)
        
        if user and brand_name:
            if User.objects.filter(id=user).last():
                serializer = BrandSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    user_brand = UserBrandMappingSerializer(data={
                        'user' : user,
                        'brand' : serializer.data['id'] 
                    })

                    if user_brand.is_valid():
                        user_brand.save()
                    else:
                        Brand.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during registering Brand.', 'status':False, 'status_code':400, 'error':user_brand.errors}, status=400)
                    return JsonResponse({'message':'Brand registered successfully', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                return JsonResponse({'message':'Error during registering Brand.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid request, User not found.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'User ID and Brand Name required.', 'status':False, 'status_code':400}, status=200)
    

    def get(self, request):
        user = request.GET.get('user')
        query = request.GET.get('query', None)

        if user:
            if query:
                user_brand = UserBrandMapping.objects.filter(user=user, brand__brand_name__icontains=query).distinct().values_list('brand', flat=True)
            else:
                user_brand = UserBrandMapping.objects.filter(user=user).distinct().values_list('brand', flat=True)
            brand = Brand.objects.filter(id__in=user_brand).all()
            serializer = BrandSerializer(brand, many=True)
            return JsonResponse({'message':'Brand List', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'User ID required.', 'status':False, 'status_code':400}, status=200)

    @authorize('update_brand')
    def put(self, request):
        users = request.data.get('users', None)

        if request.data.get('id', None):
            brand = Brand.objects.filter(id=request.data.get('id')).last()
            if brand:
                serializer = BrandSerializer(brand, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    if users:
                        for user in users:
                            try:
                                print(user)
                                user_brand = UserBrandMappingSerializer(data={
                                    'brand':brand.id,
                                    'user' : user
                                })
                                if user_brand.is_valid():
                                    user_brand.save()
                                else:
                                    logger.warning(user_brand.errors)
                            except(Exception)as e:
                                logger.error(e)
                    return JsonResponse({'message':'Brand updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating brand.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Invalid Brand ID', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_brand')
    def delete(self, request):
        if request.data.get('id', None):
            Brand.objects.filter(id=request.data.get('id')).delete()
            return JsonResponse({'message':'Brand Deleted Successfully', 'status':True, 'status_code':200}, status=200)
        
        
# BrandAddress

class BrandAddressApiView(APIView):
    @authorize('register_brand_address')
    def post(self, request):
        if request.data:
            serializer = BrandAddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Brand Address saved successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering brand address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_brand_address')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                add = BrandAddress.objects.filter(id=id).last()
                if add:        
                    serializer = BrandAddressSerializer(add, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Brand Address saved successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating brand address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid ID could not find record.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    @authorize('update_brand_address')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                BrandAddress.objects.filter(id=id).delete()
                return JsonResponse({'message':'Brand Address deleted successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        # brand = request.GET.get('brand')
        # id = request.GET.get('id')
        # address_type = request.GET.get('address_type')
        
        
        # if brand:
        #     if address_type:
        #         add = BrandAddress.objects.filter(brand=brand, address_type=address_type).all()
        #     else:
        #         add = BrandAddress.objects.filter(brand=brand).all()
        #     serializer = BrandAddressSerializer(add, many=True)
        #     return JsonResponse({'message':'Brand Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        # if id:
        #     add = BrandAddress.objects.filter(id=id).last()
        #     serializer = BrandAddressSerializer(add)
        #     return JsonResponse({'message':'Brand Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        # return JsonResponse({'message':'ID of Brand ID required.', 'status':False, 'status_code':400}, status=400)
        
        brand = request.GET.get('brand')
        id = request.GET.get('id')
        address_type = request.GET.get('address_type')
        brand = request.GET.get('brand')
        query = request.GET.get('query', None)
        
        if brand:
            if query:
                if address_type:
                    add = BrandAddress.objects.filter(brand=brand).filter(short_name__icontains=query).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = BrandAddress.objects.filter(short_name__icontains=query).filter(brand=brand).all()
            else:
                if address_type:
                    add = BrandAddress.objects.filter(brand=brand).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = BrandAddress.objects.filter(brand=brand).all()
            
            serializer = BrandAddressSerializer(add, many=True)
            return JsonResponse({'message':'Brand Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            
        
        if id:
            add = BrandAddress.objects.filter(id=id).last()
            serializer = BrandAddressSerializer(add)
            return JsonResponse({'message':'Cluster Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'ID of Cluster ID required.', 'status':False, 'status_code':400}, status=400)