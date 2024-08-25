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

#----- PO Planning Functions
from master_app.functions.po_planning_functions import PoPlanningFunctions

import logging

logger = logging.getLogger('debug_file')

User = get_user_model()



class PoApiView(APIView):
    @authorize('create_po')
    def post(self, request):
        errors = []
        if request.data:
            po_items = request.data.get('po_items')
            
            self.po_planning_helper_functions = PoPlanningFunctions()
            planning_errors, planning_items = self.po_planning_helper_functions.validate_po_items(po_items)
            print(planning_errors)
            if not planning_errors:
                serializer = PoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    error = self.save_po_items(serializer.data['id'], po_items)
                    serializer = PoReadSerializer(PoModel.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Po Created Successfully.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':error}, status=201)
                return JsonResponse({'message':'Error during creating PO.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Error during raising Purchase Order.', 'status':False, 'status_code':400, 'error':planning_errors}, status=200)
        return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
    
    
                
                
                    
    def save_po_items(self, po_id, materials):
        errors = []
        for material in materials:
            if material.get('id'):
                if material.get('delete'):
                    item = PoItems.objects.filter(id=material.get('id')).last()
                    if item:
                        self.po_planning_helper_functions.add_balance_quantity(item.item_code, item.uom, item.quantity)
                        item.delete()
                else:
                    po_items = PoItems.objects.filter(id=material.get('id')).last()
                    if po_items:
                        material['po'] = po_id
                        
                        # if material['uom'] != po_items.uom:
                        #     self.po_planning_helper_functions.decrease_balance_quantity(po_items.item_code, po_items.uom, po_items.quantity)
                        # elif float(material['quantity']) != float(po_items.quantity):
                        #     self.po_planning_helper_functions.decrease_balance_quantity(po_items.item_code, po_items.uom, po_items.quantity)
                        
                        self.po_planning_helper_functions.add_balance_quantity(po_items.item_code, po_items.uom, po_items.quantity)
                            
                        serializer = PoItemsSerializer(po_items, data=material)
                        if serializer.is_valid():
                            serializer.save()
                            self.po_planning_helper_functions.decrease_balance_quantity(serializer.data['item_code'], serializer.data['uom'], serializer.data['quantity'])
                        else:
                            errors.append(serializer.errors)
                    else:
                        
                        po_items = PoItems.objects.filter(po=po_id, item_code=material.get('item_code')).last()
                        if po_items:
                            material['po'] = po_id
                            self.po_planning_helper_functions.add_balance_quantity(po_items.item_code, po_items.uom, po_items.quantity)
                            
                            serializer = PoItemsSerializer(po_items, data=material)
                            if serializer.is_valid():
                                serializer.save()
                                self.po_planning_helper_functions.decrease_balance_quantity(serializer.data['item_code'], serializer.data['uom'], serializer.data['quantity'])
                            else:
                                errors.append(serializer.errors)
                        else:
                            material['po'] = po_id
                            serializer = PoItemsSerializer(data=material)
                            if serializer.is_valid():
                                serializer.save()
                                self.po_planning_helper_functions.decrease_balance_quantity(serializer.data['item_code'], serializer.data['uom'], serializer.data['quantity'])
                            else:
                                errors.append(serializer.errors)
                
            else:
                if material.get('delete'):
                    PoItems.objects.filter(po=po_id, item_code=material.get('item_code')).delete()
                else:
                    po_items = PoItems.objects.filter(po=po_id, item_code=material.get('item_code')).last()
                    if po_items:
                        material['po'] = po_id
                        self.po_planning_helper_functions.add_balance_quantity(po_items.item_code, po_items.uom, po_items.quantity)
                        serializer = PoItemsSerializer(po_items, data=material)
                        if serializer.is_valid():
                            serializer.save()
                            self.po_planning_helper_functions.decrease_balance_quantity(serializer.data['item_code'], serializer.data['uom'], serializer.data['quantity'])
                        else:
                            errors.append(serializer.errors)
                    else:
                        material['po'] = po_id
                        serializer = PoItemsSerializer(data=material)
                        if serializer.is_valid():
                            serializer.save()
                            self.po_planning_helper_functions.decrease_balance_quantity(serializer.data['item_code'], serializer.data['uom'], serializer.data['quantity'])
                        else:
                            errors.append(serializer.errors)
            
        return errors
    
    
    @authorize('update_po')
    def put(self, request):
        id = request.data.get('id')
        if id:
            po = PoModel.objects.filter(id=id).last()
            if po:
                serializer = PoSerializer(po, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    error = self.save_po_items(id, request.data.get('po_items'))
                    serializer = PoReadSerializer(po)
                    return JsonResponse({'message':'Updated PO.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':error}, status=200)
                return JsonResponse({'message':'Error during updating PO.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid PO.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'PO ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    
    def get(self, request):
        id = request.GET.get('id')
        brand = request.GET.get('brand')
        store = request.GET.get('store')
        cluster = request.GET.get('cluster')
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        try:
            end = int(count_per_page)*int(page)
        except(Exception)as e:
            end = 1*20
        
        try:
            start = end-int(count_per_page)
        except(Exception)as e:
            start = end - 20
        
        
        if id:
            po = PoModel.objects.filter(id=id).last()
            serializer = PoReadSerializer(po)
            return JsonResponse({'message':'PO details', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            po = BrandClusterMapping.objects.filter(brand=brand).distinct().values_list('cluster__stores__store', flat=True)
            count = PoModel.objects.filter(store__id__in=po).count()
            po = PoModel.objects.filter(store__id__in=po).all().order_by('-created_at')[start:end]
            
            serializer = PoReadSerializer(po, many=True)
            return JsonResponse({'message':'Po List of brand.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if cluster:
            po = StoreClusterMapping.objects.filter(cluster=cluster).distinct().values_list('store', flat=True)
            count = PoModel.objects.filter(store__in=po).count()
            po = PoModel.objects.filter(store__in=po).order_by('-created_at')[start:end]
            serializer = PoReadSerializer(po, many=True)
            return JsonResponse({'message':'Po List of cluster.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if store:
            po = PoModel.objects.filter(store = store).order_by('-created_at')[start:end]
            count = PoModel.objects.filter(store = store).count()
            serializer = PoSerializer(po, many=True)
            return JsonResponse({'message':'Po List of store.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        return JsonResponse({'message':"Invalid request.", 'status':False, 'status_code':400}, status=200)
    
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            PoModel.objects.filter(id=id).delete()
            return JsonResponse({'message':'PO Deleted Successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=200)