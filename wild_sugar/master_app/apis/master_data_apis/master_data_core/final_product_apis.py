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




class FinalProductRegistrationApiView(APIView):
    def save_tags(self, final_product, tags):
        errors = []
        for tag in tags:
            is_exists = FinalProductTags.objects.filter(final_product=final_product, tag=tag).last()
            if is_exists:
                pass
            else:
                serializer = FinalProductTagSerializer(data={
                    'final_product':final_product,
                    'tag' : tag
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    @authorize('register_final_product')
    def post(self, request):
        if request.data:
            errors = []
            serializer = FinalProductRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                if request.data.get('final_product_tags'):
                    status, error = self.save_tags(serializer.data['id'], request.data.get('final_product_tags'))
                    errors.extend(error)
                
                new_ser = FinalProductRegistrationReadSerializer(FinalProductRegistrationModel.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Final Product registered successfully.', 'status':True, 'status_code':201, 'result':201, 'result':new_ser.data}, status=201)
            return JsonResponse({'message':'Error during Final Product registration.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
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
                final_products = FinalProductRegistrationModel.objects.filter(brand=brand)[start:end]
                serializer = FinalProductRegistrationReadSerializer(final_products, many=True)
                count = FinalProductRegistrationModel.objects.filter(brand=brand).count()
                return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            else:
                
                final_products = FinalProductRegistrationModel.objects.filter(brand=brand).filter(queue(item_name__icontains=query) | queue(item_code__icontains=query) | queue(final_product_tags__tag__icontains=query))[start:end]
                serializer = FinalProductRegistrationReadSerializer(final_products, many=True)
                count = FinalProductRegistrationModel.objects.filter(brand=brand).filter(queue(item_name__icontains=query) | queue(item_code__icontains=query) | queue(final_product_tags__tag__icontains=query)).count()
                return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            final_products = FinalProductRegistrationModel.objects.filter(id=id).last()
            serializer = FinalProductRegistrationReadSerializer(final_products)
            return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        
        return JsonResponse({'message':'Brand ID or Product ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    
    @authorize('update_final_product')
    def put(self, request):
        if request.data:
            errors = []
            id = request.data.get('id')
            if id:
                raw = FinalProductRegistrationModel.objects.filter(id=id).last()
                if raw:
                    serializer = FinalProductRegistrationSerializer(raw, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        
                        if request.data.get('final_product_tags'):
                            status, error = self.save_tags(serializer.data['id'], request.data.get('final_product_tags'))
                            errors.extend(error)
                        
                        new_ser = FinalProductRegistrationReadSerializer(FinalProductRegistrationModel.objects.filter(id=serializer.data['id']).last())
                        return JsonResponse({'message':'Final Product updated successfully.', 'status':True, 'status_code':200, 'result':new_ser.data}, status=200)
                    return JsonResponse({'message':'Error updating Final Product.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Final Product ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_final_product')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            FinalProductRegistrationModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'Final Product deleted successfully.', 'status':True, 'status_code':200}, status=200)

class FinalProductTagsApiView(FinalProductRegistrationApiView):
    @authorize('register_final_product_tags')
    def post(self, request):
        id = request.data.get('id')
        tags = request.data.get('final_product_tags', [])
        
        errors = []
        if id and tags:
            status, error = self.save_tags(id, tags)
            errors.extend(error)
            if status:
                return JsonResponse({'message':'Tags registered to the Final product successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during registering tags to the Final product.', 'status':False, 'status_code':400, 'error':errors}, status=400)
        return JsonResponse({'message':'Final product ID and Tag list required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_final_product_tags')
    def delete(self, request):
        id = request.data.get('id')
        tags = request.data.get('final_product_tags',[])
        tag_id = request.data.get('final_product_tag_id',[])
        
        if id:
            
            if tags or tag_id:
                final_products = FinalProductRegistrationModel.objects.filter(id=id).last()
                if final_products:
                    FinalProductTags.objects.filter(final_product=id).filter(queue(id__in=tag_id) | queue(tag__in=tags)).delete()
                    return JsonResponse({'message':'Tags deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Invalid Final product or ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Tag list or Tag ID list required to delete.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Final Product ID required.', 'status':False, 'status_code':400}, status=400)
    
class FinalProductSellingPriceApiView(APIView):
    def get(self, request):
        final_product = request.GET.get('final_product')
        if final_product:
            final_product_price = FinalProductSellingPrice.objects.filter(final_product=final_product).all()
            serializer = FinalProductSellingPriceSerializer(final_product_price, many=True)
            return JsonResponse({'message':'Final Product Pricing.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'Final Product ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_final_product_selling_price')
    def post(self, request):
        # FinalProductSellingPrice
        if request.data:
            department = request.data.get('department')
            pos = request.data.get('pos')
            b2b_client = request.data.get('b2b_client')
            final_product = request.data.get('final_product')
            
            errors = []
            result = []
            if final_product:
                final_product = FinalProductRegistrationModel.objects.filter(id=final_product).last()
                if final_product:
                    if department or pos or b2b_client:
                        if department:
                            final_product_price = FinalProductSellingPrice.objects.filter(final_product=final_product.id, department__isnull=False).last()
                            if final_product_price:
                                serializer = FinalProductSellingPriceSerializer(final_product_price, data=request.data)
                            else:
                                serializer = FinalProductSellingPriceSerializer(data=request.data)
                                
                            if serializer.is_valid():
                                serializer.save()
                                result.append(serializer.data)
                                # return JsonResponse({'message':'Final Product Selling Price registered successfully.', 'status':True, 'status_code':201}, status=201)
                            else:
                                errors.append(serializer.errors)
                            # return JsonResponse({'message':'Error during registering final product price.', 'status':False, 'status_code':400}, status = 400)
                        
                        elif pos:
                            final_product_price = FinalProductSellingPrice.objects.filter(final_product=final_product.id, pos__isnull=False).last()
                            if final_product_price:
                                serializer = FinalProductSellingPriceSerializer(final_product_price, data=request.data)
                            else:
                                serializer = FinalProductSellingPriceSerializer(data=request.data)
                                
                            if serializer.is_valid():
                                serializer.save()
                                result.append(serializer.data)
                                # return JsonResponse({'message':'Final Product Selling Price registered successfully.', 'status':True, 'status_code':201}, status=201)
                            else:
                                errors.append(serializer.errors)
                        
                        elif b2b_client:
                            final_product_price = FinalProductSellingPrice.objects.filter(final_product=final_product.id, b2b_client__isnull=False).last()
                            if final_product_price:
                                serializer = FinalProductSellingPriceSerializer(final_product_price, data=request.data)
                            else:
                                serializer = FinalProductSellingPriceSerializer(data=request.data)
                                
                            if serializer.is_valid():
                                serializer.save()
                                result.append(serializer.data)
                                # return JsonResponse({'message':'Final Product Selling Price registered successfully.', 'status':True, 'status_code':201}, status=201)
                            else:
                                errors.append(serializer.errors)
                        
                        if errors:
                            return JsonResponse({'message':'Error during registering final product price.', 'status':False, 'status_code':400, 'error':errors}, status=400)
                        else:
                            return JsonResponse({'message':'Final Product Price registered successfully.', 'status':True, 'status_code':201, 'result':result}, status=201)
                    return JsonResponse({'message':'Department ID , POS ID or B2B client ID required.', 'status':False, 'status_code':400}, status=400)
                return JsonResponse({'message':'Invalid Final Product ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':"Final Product ID required.", 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
class FinalProductPriceForPOSApiView(APIView):
    @authorize('register_final_product_selling_price')
    def post(self, request):
        if request.data:
            serializer = FinalProductPriceForPOSSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Final Product price for POS saved.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during saving price.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_final_product_selling_price')
    def put(self, request):
        if request.data:
            id_ = request.data.get('id')
            if id_:
                fpp = FinalProductPriceForPOS.objects.filter(id=id_).last()
                if fpp:
                    serializer = FinalProductPriceForPOSSerializer(fpp, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Final Product Price for POS Updated', 'status':False, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating price.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid ID provided.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Invalid request. ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)

    
    def get(self, request):
        pos = request.GET.get('pos')
        fp = request.GET.get('final_product')
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if pos:
            # FinalProductPriceForPOSReadSerializer
            fpp = FinalProductPriceForPOS.objects.filter(pos=pos).all()[start:end]
            serializer = FinalProductPriceForPOSReadSerializer(fpp, many=True)
            return JsonResponse({'message':'Final Product pricing for POS.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if fp:
            fpp = FinalProductPriceForPOS.objects.filter(final_product=fp).all()[start:end]
            serializer = FinalProductPriceForPOSReadSerializer(fpp, many=True)
            return JsonResponse({'message':'Final Product pricing for POS.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
    
    
    
    
    
class FinalProductDeptPosApiView(APIView):
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
  



class FinalProductFilterApiVIew(APIView):
    def post(self, request):
        brand = request.data.get('brand')
        
        filters = request.data.get('filters', {})
        
        page = request.data.get('page', 1)
        count_per_page = request.data.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if brand:
            final_product = FinalProductRegistrationModel.objects.filter(brand=brand).all()
            if filters:
                category = filters.get('category', [])
                sub_category  = filters.get('sub_category', [])
                high_value_item  = filters.get('high_value_item')
                # consumable  = filters.get('consumable')
                # planned  = filters.get('planned')
                
                
                if final_product:
                    if category:
                        final_product = final_product.filter(category__in=category).all()
                    
                    if sub_category:
                        final_product = final_product.filter(sub_category__in=sub_category).all()
                    
                    if high_value_item is not None:
                        final_product = final_product.filter(high_value_item=high_value_item).all()
                    
                    
                    serializer = FinalProductRegistrationSerializer(final_product, many=True)
                    count = final_product.count()
                    return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
                return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':[]}, status=200)
            serializer = FinalProductRegistrationSerializer(final_product, many=True)
            count = final_product.count()
            return JsonResponse({'message':'Final Product result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)    
    
    
    
