from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.db.models import Q as queue
from django.db.models import Count

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

import logging

logger = logging.getLogger('debug_file')

User = get_user_model()


class AssetInvetoryApiView(APIView):
    
    def map_pos(self, asset_inventory, pos):
        errors = []
        for po in pos:
            if not AssetInvetoryPosMapping.objects.filter(pos=po, asset_inventory=asset_inventory):
                serializer = AssetInvetoryPosMapSerializer(data={
                    "pos" : po,
                    "asset_inventory" :asset_inventory
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    def map_dept(self, asset_inventory, pos):
        errors = []
        for po in pos:
            if not AssetInvetoryDeptMapping.objects.filter(department=po, asset_inventory=asset_inventory):
                serializer = AssetInvetoryDeptMappingSerializer(data={
                    "department" : po,
                    "asset_inventory" :asset_inventory
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    @authorize('register_service_items')
    def post(self, request):
        if request.data:
            errors = []
            
            pos = request.data.get('pos')
            dept = request.data.get('department')
            
            serializer = AssetInvetoryRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                status, error = self.map_dept(serializer.data['id'], dept)
                errors.extend(error)
                status, error = self.map_pos(serializer.data['id'], pos)
                errors.extend(error)
                serializer = AssetInvetoryRegistrationSerializer(AssetInvetoryRegistrationModel.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Service Material registered successfully.', 'status':True, 'status_code':201, 'result':201, 'result':serializer.data, 'error':error}, status=201)
            return JsonResponse({'message':'Error during Service Material registration.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        brand = request.GET.get('brand')
        pos = request.GET.get('pos')
        dept = request.GET.get('department')
         
        id = request.GET.get('id')
        query = request.GET.get('query', None)
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        count = 0
        
        if brand or pos or dept:
            if brand:
                if not query:
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(brand=brand)[start:end]
                    count = AssetInvetoryRegistrationModel.objects.filter(brand=brand).count()
                else:
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(brand=brand).filter(queue(item_code__icontains = query) | queue(item_name__icontains = query) | queue(hsn_code__icontains = query) | queue(category__icontains = query) | queue(sub_category__icontains = query))[start:end]
                    count = AssetInvetoryRegistrationModel.objects.filter(brand=brand).count()
            
            if pos:
                if not query:
                    pos_service = AssetInvetoryPosMapping.objects.filter(pos=pos).distinct().values_list('asset_inventory__id', flat=True)
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(id__in=pos_service)[start:end]
                    count = AssetInvetoryPosMapping.objects.filter(pos=pos).count()
                else:
                    pos_service = AssetInvetoryPosMapping.objects.filter(pos=pos).filter(queue(asset_inventory__item_code__icontains = query) | queue(asset_inventory__item_name__icontains = query) | queue(asset_inventory__hsn_code__icontains = query) | queue(asset_inventory__category__icontains = query) | queue(asset_inventory__sub_category__icontains = query)).distinct().values_list('asset_inventory', flat=True)
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(id__in=pos_service)[start:end]
                    count = AssetInvetoryPosMapping.objects.filter(pos=pos).filter(queue(asset_inventory__item_code__icontains = query) | queue(asset_inventory__item_name__icontains = query) | queue(asset_inventory__hsn_code__icontains = query) | queue(asset_inventory__category__icontains = query) | queue(asset_inventory__sub_category__icontains = query)).count()
            
            if dept:
                if not query:
                    dept_service = AssetInvetoryDeptMapping.objects.filter(department=dept).distinct().values_list('asset_inventory__id', flat=True)
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(id__in=dept_service)[start:end]
                    count = AssetInvetoryDeptMapping.objects.filter(department=dept).count()
                else:
                    dept_service = AssetInvetoryDeptMapping.objects.filter(department=dept).filter(queue(asset_inventory__item_code__icontains = query) | queue(asset_inventory__item_name__icontains = query) | queue(asset_inventory__hsn_code__icontains = query) | queue(asset_inventory__category__icontains = query) | queue(asset_inventory__sub_category__icontains = query)).distinct().values_list('asset_inventory__id', flat=True)
                    asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(id__in=dept_service)[start:end]
                    count = AssetInvetoryDeptMapping.objects.filter(department=dept).filter(queue(asset_inventory__item_code__icontains = query) | queue(asset_inventory__item_name__icontains = query) | queue(asset_inventory__hsn_code__icontains = query) | queue(asset_inventory__category__icontains = query) | queue(asset_inventory__sub_category__icontains = query)).count()
            
            serializer = AssetInvetoryRegistrationSerializer(asset_inventorys, many=True)
            # count = 0
            return JsonResponse({'message':'Service Material result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            asset_inventorys = AssetInvetoryRegistrationModel.objects.filter(id=id).last()
            serializer = AssetInvetoryRegistrationReadSerializer(asset_inventorys)
            return JsonResponse({'message':'Service Material result.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        
        return JsonResponse({'message':'Brand ID or Product ID required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    
    @authorize('update_service_items')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            errors = []
            
            pos = request.data.get('pos')
            dept = request.data.get('department')
            
            if id:
                raw = AssetInvetoryRegistrationModel.objects.filter(id=id).last()
                if raw:
                    serializer = AssetInvetoryRegistrationSerializer(raw, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        
                        status, error = self.map_dept(serializer.data['id'], dept)
                        errors.extend(error)
                        status, error = self.map_pos(serializer.data['id'], pos)
                        errors.extend(error)
                        return JsonResponse({'message':'Service Material updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':error}, status=200)
                    return JsonResponse({'message':'Error updating Service Material.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Service Material ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_service_items')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            AssetInvetoryRegistrationModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'Service Material deleted successfully.', 'status':True, 'status_code':200}, status=200)

