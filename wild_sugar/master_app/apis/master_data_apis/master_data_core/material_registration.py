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
import math

logger = logging.getLogger('debug_file')

User = get_user_model()


class RawMaterialFilterApiVIew(APIView):
    def post(self, request):
        brand = request.data.get('brand')
        
        filters = request.data.get('filters', {})
        
        page = request.data.get('page', 1)
        count_per_page = request.data.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if brand:
            raw_material = RawMaterialRegistrationModel.objects.filter(brand=brand).all()
            if filters:
                category = filters.get('category', [])
                sub_category  = filters.get('sub_category', [])
                high_value_item  = filters.get('high_value_item')
                consumable  = filters.get('consumable')
                planned  = filters.get('planned')
                
                
                if raw_material:
                    if category:
                        raw_material = raw_material.filter(category__in=category).all()
                    
                    if sub_category:
                        raw_material = raw_material.filter(sub_category__in=sub_category).all()
                    
                    if high_value_item is not None:
                        raw_material = raw_material.filter(high_value_item=high_value_item).all()
                    
                    if consumable is not None:
                        raw_material = raw_material.filter(consumable=consumable).all()
                        
                    
                    if planned == True:
                        stores = StoreBrandMapping.objects.filter(brand=brand).distinct().values_list('store', flat=True)
                        unplanned = UnplannedItems.objects.filter(store__in=stores).distinct().values_list('item_code', flat=True)
                        raw_material = raw_material.exclude(item_code__in=unplanned).all()
                    
                    if planned==False:
                        stores = StoreBrandMapping.objects.filter(brand=brand).distinct().values_list('store', flat=True)
                        unplanned = UnplannedItems.objects.filter(store__in=stores).distinct().values_list('item_code', flat=True)
                        raw_material = raw_material.filter(item_code__in=unplanned).all()
                    
                    serializer = RawMaterialRegistrationSerializer(raw_material, many=True)
                    count = raw_material.count()
                    return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
                return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':[]}, status=200)
            serializer = RawMaterialRegistrationSerializer(raw_material, many=True)
            count = raw_material.count()
            return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    

class RawMaterialApiView(APIView):
    def save_tags(self, raw_material, tags):
        errors = []
        for tag in tags:
            is_exists = RawMaterialTags.objects.filter(raw_material=raw_material, tag=tag).last()
            if is_exists:
                pass
            else:
                serializer = RawMaterialTagSerializer(data={
                    'raw_material':raw_material,
                    'tag' : tag
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_pos(self, raw_material, pos):
        errors = []
        for po in pos:
            if not RawMaterialPosMapping.objects.filter(pos=po, raw_material=raw_material):
                serializer = RawMaterialPosMapSerializer(data={
                    "pos" : po,
                    "raw_material" :raw_material
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_dept(self, raw_material, pos):
        errors = []
        for po in pos:
            if not RawMaterialDeptMapping.objects.filter(department=po, raw_material=raw_material):
                serializer = RawMaterialDeptMappingSerializer(data={
                    "department" : po,
                    "raw_material" :raw_material
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def save_alias(self, raw_material, aliases):
        errors = []
        for alias in aliases:
            if not RawMaterialAliases.objects.filter(raw_material=raw_material, alias=alias).last():
                serializer = RawMaterialAliaseSerializer(data={
                    "raw_material":raw_material,
                    "alias":alias
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
            
    
    @authorize('register_raw_material')
    def post(self, request):
        if request.data:
            errors = []
            
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            
            serializer = RawMaterialRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                status, error = self.map_dept(serializer.data['id'], dept)
                errors.extend(error)
                status, error = self.map_pos(serializer.data['id'], pos)
                errors.extend(error)
                status, error = self.save_tags(serializer.data['id'], request.data.get('raw_material_tags', []))
                errors.extend(error)
                status, error = self.save_alias(serializer.data['id'], request.data.get('raw_material_alias', []))
                errors.extend(error)
                serializer = RawMaterialRegistrationSerializer(RawMaterialRegistrationModel.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Raw material registered successfully.', 'status':True, 'status_code':201, 'result':201, 'result':serializer.data, 'error':errors}, status=201)
            return JsonResponse({'message':'Error during raw material registration.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    # @authorize('register_raw_material')
    def get(self, request):
        brand = request.GET.get('brand')
        id = request.GET.get('id')
        query = request.GET.get('query', None)
        consumable = request.GET.get('consumable', 'true')
        
        filters = request.data.get('filters', {})
        
        if consumable == 'false':
            consumable = False
        else:
            consumable = True
        
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if brand:
            if filters:
                category = filters.get('category')
                sub_category  = filters.get('sub_category')
                high_value_item  = filters.get('high_value_item')
                consumable  = filters.get('consumable')
                planned  = filters.get('planned')
                
                raw_material = RawMaterialRegistrationModel.objects.filter(brand=brand).all()
                if raw_material:
                    if category:
                        raw_material = raw_material.filter(category=category).all()
                    
                    if sub_category:
                        raw_material = raw_material.filter(sub_category=sub_category).all()
                    
                    if high_value_item:
                        raw_material = raw_material.filter(high_value_item=True).all()
                    
                    if planned == True:
                        stores = StoreBrandMapping.objects.filter(brand=brand).distinct().values_list('store', flat=True)
                        unplanned = UnplannedItems.objects.filter(store__in=stores).distinct().values_list('item_code', flat=True)
                        raw_material = raw_material.exclude(item_code__in=unplanned).all()
                    
                    if planned==False:
                        stores = StoreBrandMapping.objects.filter(brand=brand).distinct().values_list('store', flat=True)
                        unplanned = UnplannedItems.objects.filter(store__in=stores).distinct().values_list('item_code', flat=True)
                        raw_material = raw_material.filter(item_code__in=unplanned).all()
                    
                    serializer = RawMaterialRegistrationSerializer(raw_material, many=True)
                    count=  raw_material.count()
                    return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
                    
            if not query:
                raw_materials = RawMaterialRegistrationModel.objects.filter(brand=brand, consumable=consumable)[start:end]
                serializer = RawMaterialRegistrationSerializer(raw_materials, many=True)
                count = RawMaterialRegistrationModel.objects.filter(brand=brand, consumable=consumable).count()
                return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            else:
                raw_materials = RawMaterialRegistrationModel.objects.filter(brand=brand, consumable=consumable).filter(queue(item_code__icontains = query) | queue(item_name__icontains = query) | queue(hsn_code__icontains = query) | queue(category__icontains = query) | queue(sub_category__icontains = query) | queue(raw_material_tags__tag__icontains = query))[start:end]
                serializer = RawMaterialRegistrationSerializer(raw_materials, many=True)
                count = RawMaterialRegistrationModel.objects.filter(brand=brand, consumable=consumable).filter(queue(item_code__icontains = query) | queue(item_name__icontains = query) | queue(hsn_code__icontains = query) | queue(category__icontains = query) | queue(sub_category__icontains = query) | queue(raw_material_tags__tag__icontains = query)).count()
                return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            raw_materials = RawMaterialRegistrationModel.objects.filter(id=id).last()
            serializer = RawMaterialRegistrationReadSerializer(raw_materials)
            return JsonResponse({'message':'Raw Material result.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        
        return JsonResponse({'message':'Brand ID or Product ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    
    @authorize('update_raw_material')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            errors = []
            
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            
            if id:
                raw = RawMaterialRegistrationModel.objects.filter(id=id).last()
                if raw:
                    serializer = RawMaterialRegistrationSerializer(raw, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        
                        status, error = self.map_dept(serializer.data['id'], dept)
                        errors.extend(error)
                        status, error = self.map_pos(serializer.data['id'], pos)
                        errors.extend(error)
                        status, error = self.save_tags(serializer.data['id'], request.data.get('raw_material_tags', []))
                        errors.extend(error)
                        status, error = self.save_alias(serializer.data['id'], request.data.get('raw_material_alias', []))
                        errors.extend(error)
                        return JsonResponse({'message':'Raw material updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                    return JsonResponse({'message':'Error updating Raw material.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Raw material ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_raw_material')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            RawMaterialRegistrationModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'Raw material deleted successfully.', 'status':True, 'status_code':200}, status=200)



class RawMaterialAliasApiView(RawMaterialApiView):
    @authorize('register_raw_material_alias')
    def post(self, request):
        id = request.data.get('id')
        tags = request.data.get('raw_material_alias', [])
        
        errors = []
        if id and tags:
            status, error = self.save_alias(id, tags)
            errors.extend(error)
            if status:
                return JsonResponse({'message':'Alias registered to the Raw Material successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during registering alias to the Raw Material.', 'status':False, 'status_code':400, 'error':errors}, status=400)
        return JsonResponse({'message':'Raw Material ID and Alias list required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_raw_material_alias')
    def delete(self, request):
        id = request.data.get('id')
        aliases = request.data.get('raw_material_alias',[])
        alias_id = request.data.get('raw_material_alias_id',[])
        
        if id:
            
            if aliases or alias_id:
                raw_materials = RawMaterialRegistrationModel.objects.filter(id=id).last()
                if raw_materials:
                    RawMaterialAliases.objects.filter(raw_material=id).filter(queue(id__in=alias_id) | queue(alias__in=aliases)).delete()
                    return JsonResponse({'message':'Alias deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Invalid Raw Material or ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Alias list or Alias ID list required to delete.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Raw Material ID required.', 'status':False, 'status_code':400}, status=400)



class RawMaterialTagsApiView(RawMaterialApiView):
    @authorize('register_raw_material_tags')
    def post(self, request):
        id = request.data.get('id')
        tags = request.data.get('raw_material_tags', [])
        
        errors = []
        if id and tags:
            status, error = self.save_tags(id, tags)
            errors.extend(error)
            if status:
                return JsonResponse({'message':'Tags registered to the Raw Material successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during registering tags to the Raw Material.', 'status':False, 'status_code':400, 'error':errors}, status=400)
        return JsonResponse({'message':'Raw Material ID and Tag list required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_raw_material_tags')
    def delete(self, request):
        id = request.data.get('id')
        tags = request.data.get('raw_material_tags',[])
        tag_id = request.data.get('raw_material_tag_id',[])
        
        if id:
            
            if tags or tag_id:
                raw_materials = RawMaterialRegistrationModel.objects.filter(id=id).last()
                if raw_materials:
                    RawMaterialTags.objects.filter(raw_material=id).filter(queue(id__in=tag_id) | queue(tag__in=tags)).delete()
                    return JsonResponse({'message':'Tags deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Invalid Raw Material or ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Tag list or Tag ID list required to delete.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Raw Material ID required.', 'status':False, 'status_code':400}, status=400)



class RawMaterialVendorPricingApiView(APIView):
    @authorize('register_raw_material_vendor_pricing')
    def post(self, request):
        # VendorPricingRawMaterial
        if request.data:
            vendor = request.data.get('vendor')
            raw_material = request.data.get('raw_material')
            
            if vendor and raw_material:
                if request.data.get('rate', 0) and request.data.get('price', 0):
                    serializer = VendorPricingRawMaterialSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        VendorPricingRawMaterial.objects.filter(vendor=vendor, raw_material=raw_material, id__lt=serializer.data['id']).update(latest=False)
                        return JsonResponse({'message':'Vendor pricing for raw material updated.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                    return JsonResponse({'message':'Error during registering vendor raw material pricing.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Rate and Price should be greater than 0.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Vendor and Raw material ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        raw_material = request.GET.get('raw_material')
        vendor = request.GET.get('vendor')
        
        if raw_material and vendor:
            vendor_pricing = VendorPricingRawMaterial.objects.filter(raw_material=raw_material, vendor=vendor).all().order_by('-id')
            serializer = VendorPricingRawMaterialSerializer(vendor_pricing, many=True)
            return JsonResponse({'message':'Pricing and history for requested raw material and vendor.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            
        if raw_material:
            vendor_pricing = VendorPricingRawMaterial.objects.filter(raw_material=raw_material, latest=True).all().order_by('-id')
            serializer = VendorPricingRawMaterialReadSerializer(vendor_pricing, many=True)
            return JsonResponse({'message':'Vendor pricing for requested raw material.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
            
class RawMaterialVendorPricingUpdate(APIView):
    @authorize('update_vendor_pricing')
    def put(slf, request):
        vendor = request.data.get('vendor', None)
        raw_material = request.data.get('raw_material', None)
        if vendor and raw_material:
            vendor_pricing = VendorPricingRawMaterial.objects.filter(vendor=vendor, raw_material=raw_material, latest=True).last()
            
            if vendor_pricing:
                old_value = {
                    "rate" : vendor_pricing.rate,
                    "price": vendor_pricing.price
                }
                
                serializer = VendorPricingRawMaterialSerializer(vendor_pricing, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    new_value = {
                        "rate" : serializer.data['rate'],
                        "price":serializer.data['price']
                    }
                    
                    price_update_log = VendorPricingUpdateLogSerializer(data={
                        'vendor_pricing':vendor_pricing.id,
                        'old_value':old_value,
                        'new_value':new_value
                    })
                    if price_update_log.is_valid():
                        price_update_log.save()
                    else:
                        print(price_update_log.errors)
                    return JsonResponse({'message':'Pricing Updated Successfull.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Error during price update.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid Vendor Pricing.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Pricing ID required.', 'status':False, 'status_code':400}, status=400)
    
    
class RawMaterialDeptPosApiView(APIView):
    def map_pos(self, raw_material, pos):
        errors = []
        for po in pos:
            if not RawMaterialPosMapping.objects.filter(pos=po, raw_material=raw_material):
                serializer = RawMaterialPosMapSerializer(data={
                    "pos" : po,
                    "raw_material" :raw_material
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_dept(self, raw_material, pos):
        errors = []
        for po in pos:
            if not RawMaterialDeptMapping.objects.filter(department=po, raw_material=raw_material):
                serializer = RawMaterialDeptMappingSerializer(data={
                    "department" : po,
                    "raw_material" :raw_material
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    
    @authorize('raw_material_dept_mapping')
    def post(self, request):
        if request.data:
            raw_material = request.data.get('raw_material', None)
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            errors = []
            if raw_material and (pos or dept):
                if pos:
                    status, error = self.map_pos(raw_material, pos)
                    errors.extend(error)
                
                if dept:
                    status, error = self.map_dept(raw_material, dept)
                    errors.extend(error)
                
                return JsonResponse({'message':'Raw Material mapped successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Invalid request. Raw Material ID and POS/Department required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    
    @authorize('raw_material_dept_mapping')
    def delete(self, request):
        if request.data:
            raw_material = request.data.get('raw_material', None)
            pos = request.data.get('pos', [])
            dept = request.data.get('department', [])
            
            if raw_material and (pos or dept):
                if pos:
                    RawMaterialPosMapping.objects.filter(pos__in=pos, raw_material=raw_material).delete()
                
                if dept:
                    RawMaterialDeptMapping.objects.filter(department__in=dept, raw_material=raw_material).delete()
                    
                return JsonResponse({'message':'Raw Material mapping updated successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'Invalid request. Raw Material ID and POS/Department required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        pos = request.GET.get('pos', None)
        dept = request.GET.get('department', None)
        raw_material = request.GET.get('raw_material', None)
        
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = end-int(count_per_page)
        
        if pos:
            raw_material_instance = RawMaterialPosMapping.objects.filter(pos=pos)[start:end]
            count = RawMaterialPosMapping.objects.filter(pos=pos).count()
            serializer = RawMaterialPosMapReadSerializer(raw_material_instance, many=True).data
            return JsonResponse({'message':'Raw Materials of POS.', 'status':True, 'status_code':200, 'result':serializer, 'count':count}, status=200)
        
        if dept:
            raw_material_instance = RawMaterialDeptMapping.objects.filter(department=dept)[start:end]
            count = RawMaterialDeptMapping.objects.filter(department=dept).count()
            serializer = RawMaterialDeptMappingReadSerializer(raw_material_instance, many=True)
            return JsonResponse({'message':"Raw materials of department.", 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if raw_material:
            raw_material = RawMaterialRegistrationModel.objects.filter(id=raw_material).last()
            serializer = RawMaterialRegistrationReadSerializer(raw_material, many=False)
            return JsonResponse({'message':'Raw material detailed mapping.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'POS ID (OR) Department ID (OR) Raw material ID required.', 'status':False, 'status_code':400}, status=400)
    



class RawMaterialsExtraUomApiView(APIView):
    @authorize('register_raw_material_uom')
    def post(self, request):
        if request.data:
            serializer = RawMaterialUomModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Raw Material UOMs registered successfully.', 'status':True, 'status_code':True, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering UOMs.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request', 'status':False, 'status_code':400}, status=400)
    
    
    
    @authorize('update_raw_material_uom')
    def put(self, request):
        id = request.data.get('id')
        if id:
            uom = RawMaterialUomModel.objects.filter(id=id).last()

            if uom:
                serializer = RawMaterialUomModelSerializer(uom, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Raw material UOMs updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating Raw Material UOMs.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid record.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        id = request.GET.get('id')
        raw_material = request.GET.get('raw_material')
        brand = request.GET.get('brand', None)
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        if id:
            uoms = RawMaterialUomModel.objects.filter(id=id).last()
            serializer = RawMaterialUomModelSerializer(uoms)
            return JsonResponse({'message':'UOMs details.', 'status':True, 'status_code':200,'result':serializer.data}, status=200)
        
        elif raw_material:
            uoms = RawMaterialUomModel.objects.filter(raw_material=raw_material).all()
            serializer = RawMaterialUomModelSerializer(uoms, many=True)
            return JsonResponse({'message':'Raw Material UOMs.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        elif brand:
            try:
                end = int(page)*int(count_per_page)
            except(Exception)as e:
                end = 1*20
                
            try:
                start = end-int(count_per_page)
            except(Exception)as e:
                start = end-20
                
            uoms = RawMaterialUomModel.objects.filter(raw_material__brand=brand)[start:end]
            serializer = RawMaterialUomModelSerializer(uoms, many=True)
            count = RawMaterialUomModel.objects.filter(raw_material__brand=brand).count()
            return JsonResponse({'message':'Raw Material UOMs.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID, Raw Material ID or Instance ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_raw_material_uom')
    def delete(self, request):
        id = request.data.get('id')
        if id:
            RawMaterialUomModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'UOM deleted successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)