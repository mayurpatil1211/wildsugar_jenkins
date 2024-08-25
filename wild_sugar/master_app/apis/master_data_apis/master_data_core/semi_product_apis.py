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
import json

logger = logging.getLogger('debug_file')

User = get_user_model()


class SemiProductRegistrationApiView(APIView):
    def save_tags(self, semi_product, tags):
        errors = []
        for tag in tags:
            is_exists = SemiProductTags.objects.filter(semi_product=semi_product, tag=tag).last()
            if is_exists:
                pass
            else:
                serializer = SemiProductTagSerializer(data={
                    'semi_product':semi_product,
                    'tag' : tag
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_pos(self, semi_product, pos):
        errors = []
        for po in pos:
            if not SemiProductPosMapping.objects.filter(pos=po, semi_product=semi_product):
                serializer = SemiProductPosMapSerializer(data={
                    "pos" : po,
                    "semi_product" :semi_product
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_dept(self, semi_product, pos):
        errors = []
        for po in pos:
            if not SemiProductDeptMapping.objects.filter(department=po, semi_product=semi_product):
                serializer = SemiProductDeptMappingSerializer(data={
                    "department" : po,
                    "semi_product" :semi_product
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    @authorize('register_semi_product')
    def post(self, request):
        errors = []
        
        if request.data:
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            
            serializer = SemiProductRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                status, error = self.save_tags(serializer.data['id'], request.data.get('semi_product_tags', []))
                errors.extend(error)
                
                status, error = self.map_dept(serializer.data['id'], dept)
                errors.extend(error)
                status, error = self.map_pos(serializer.data['id'], pos)
                errors.extend(error)
                serializer = SemiProductRegistrationSerializer(SemiProductRegistrationModel.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Semi Product registered successfully.', 'status':True, 'status_code':201, 'result':201, 'result':serializer.data, 'errors':errors}, status=201)
            return JsonResponse({'message':'Error during Semi Product registration.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        brand = request.GET.get('brand')
        id = request.GET.get('id')
        query = request.GET.get('query', None)
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if brand:
            if not query:
                semi_products = SemiProductRegistrationModel.objects.filter(brand=brand)[start:end]
                serializer = SemiProductBriefSerializer(semi_products, many=True)
                count = SemiProductRegistrationModel.objects.filter(brand=brand).count()
                return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            else:
                semi_products = SemiProductRegistrationModel.objects.filter(brand=brand).filter(queue(item_code__icontains = query) | queue(item_name__icontains = query) | queue(category__icontains = query) | queue(sub_category__icontains = query) | queue(semi_product_tags__tag__icontains = query))[start:end]
                serializer = SemiProductBriefSerializer(semi_products, many=True)
                count = SemiProductRegistrationModel.objects.filter(brand=brand).filter(queue(item_code__icontains = query) | queue(item_name__icontains = query) | queue(category__icontains = query) | queue(sub_category__icontains = query) | queue(semi_product_tags__tag__icontains = query)).count()
                return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            semi_products = SemiProductRegistrationModel.objects.filter(id=id).last()
            serializer = SemiProductRegistrationReadSerializer(semi_products)
            return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        
        return JsonResponse({'message':'Brand ID or Product ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    
    @authorize('update_semi_product')
    def put(self, request):
        if request.data:
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            errors = []
            id = request.data.get('id')
            if id:
                raw = SemiProductRegistrationModel.objects.filter(id=id).last()
                if raw:
                    serializer = SemiProductRegistrationSerializer(raw, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        status, error = self.save_tags(serializer.data['id'], request.data.get('semi_product_tags'))
                        errors.extend(error)
                        
                        status, error = self.map_dept(serializer.data['id'], dept)
                        errors.extend(error)
                        status, error = self.map_pos(serializer.data['id'], pos)
                        errors.extend(error)
                        return JsonResponse({'message':'Semi Product updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                    return JsonResponse({'message':'Error updating Semi Product.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Semi Product ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_semi_product')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            SemiProductRegistrationModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'Semi Product deleted successfully.', 'status':True, 'status_code':200}, status=200)
    
        

class SemiProductTagsApiView(SemiProductRegistrationApiView):
    @authorize('register_semi_product_tags')
    def post(self, request):
        id = request.data.get('id')
        tags = request.data.get('semi_product_tags', [])
        
        errors = []
        if id and tags:
            status, error = self.save_tags(id, tags)
            errors.extend(error)
            if status:
                return JsonResponse({'message':'Tags registered to the Semi product successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during registering tags to the Semi product.', 'status':False, 'status_code':400, 'error':errors}, status=400)
        return JsonResponse({'message':'Semi product ID and Tag list required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_semi_product_tags')
    def delete(self, request):
        id = request.data.get('id')
        tags = request.data.get('semi_product_tags',[])
        tag_id = request.data.get('semi_product_tag_id',[])
        
        if id:
            
            if tags or tag_id:
                semi_products = SemiProductRegistrationModel.objects.filter(id=id).last()
                if semi_products:
                    SemiProductTags.objects.filter(semi_product=id).filter(queue(id__in=tag_id) | queue(tag__in=tags)).delete()
                    return JsonResponse({'message':'Tags deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Invalid Semi product or ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Tag list or Tag ID list required to delete.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Semi Product ID required.', 'status':False, 'status_code':400}, status=400)



class SemiProductDeptPosApiView(APIView):
    def map_pos(self, semi_product, pos):
        errors = []
        for po in pos:
            if not SemiProductPosMapping.objects.filter(pos=po, semi_product=semi_product):
                serializer = SemiProductPosMapSerializer(data={
                    "pos" : po,
                    "semi_product" :semi_product
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_dept(self, semi_product, pos):
        errors = []
        for po in pos:
            if not SemiProductDeptMapping.objects.filter(department=po, semi_product=semi_product):
                serializer = SemiProductDeptMappingSerializer(data={
                    "department" : po,
                    "semi_product" :semi_product
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    
    @authorize('semi_product_mapping')
    def post(self, request):
        if request.data:
            semi_product = request.data.get('semi_product', None)
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            errors = []
            if semi_product and (pos or dept):
                if pos:
                    status, error = self.map_pos(semi_product, pos)
                    errors.extend(error)
                
                if dept:
                    status, error = self.map_dept(semi_product, dept)
                    errors.extend(error)
                
                return JsonResponse({'message':'Semi Product mapped successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Invalid request. Semi Product ID and POS/Department required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    
    @authorize('semi_product_mapping')
    def delete(self, request):
        if request.data:
            semi_product = request.data.get('semi_product', None)
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            
            if semi_product and (pos or dept):
                if pos:
                    SemiProductPosMapping.objects.filter(pos__in=pos, semi_product=semi_product).delete()
                
                if dept:
                    SemiProductDeptMapping.objects.filter(department__in=dept, semi_product=semi_product).delete()
                    
                return JsonResponse({'message':'Semi Product mapping updated successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'Invalid request. Semi Product ID and POS/Department required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        pos = request.GET.get('pos', None)
        dept = request.GET.get('department', None)
        semi_product = request.GET.get('semi_product', None)
        
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = end-int(count_per_page)
        
        if pos:
            semi_product_instance = SemiProductPosMapping.objects.filter(pos=pos)[start:end]
            count = SemiProductPosMapping.objects.filter(pos=pos).count()
            serializer = SemiProductPosMapReadSerializer(semi_product_instance, many=True).data
            return JsonResponse({'message':'Semi Products of POS.', 'status':True, 'status_code':200, 'result':serializer, 'count':count}, status=200)
        
        if dept:
            semi_product_instance = SemiProductDeptMapping.objects.filter(department=dept)[start:end]
            count = SemiProductDeptMapping.objects.filter(department=dept).count()
            serializer = SemiProductDeptMappingReadSerializer(semi_product_instance, many=True)
            return JsonResponse({'message':"Semi Products of department.", 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if semi_product:
            semi_product = SemiProductRegistrationModel.objects.filter(id=semi_product).last()
            serializer = SemiProductRegistrationReadSerializer(semi_product, many=False)
            return JsonResponse({'message':'Semi Product detailed mapping.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'POS ID (OR) Department ID (OR) Semi Product ID required.', 'status':False, 'status_code':400}, status=400)
  



class SemiProductFilterApiVIew(APIView):
    def post(self, request):
        brand = request.data.get('brand')
        
        filters = request.data.get('filters', {})
        
        page = request.data.get('page', 1)
        count_per_page = request.data.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if brand:
            semi_product = SemiProductRegistrationModel.objects.filter(brand=brand).all()
            if filters:
                category = filters.get('category', [])
                sub_category  = filters.get('sub_category', [])
                high_value_item  = filters.get('high_value_item')
                # consumable  = filters.get('consumable')
                # planned  = filters.get('planned')
                
                
                if semi_product:
                    if category:
                        semi_product = semi_product.filter(category__in=category).all()
                    
                    if sub_category:
                        semi_product = semi_product.filter(sub_category__in=sub_category).all()
                    
                    if high_value_item is not None:
                        semi_product = semi_product.filter(high_value_item=high_value_item).all()
                    
                    
                    serializer = SemiProductRegistrationSerializer(semi_product, many=True)
                    count = semi_product.count()
                    return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
                return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':[]}, status=200)
            serializer = SemiProductRegistrationSerializer(semi_product, many=True)
            count = semi_product.count()
            return JsonResponse({'message':'Semi Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)  







