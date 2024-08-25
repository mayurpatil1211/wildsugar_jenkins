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


class PurchasedApiView(APIView):
    def save_purchased_items(self, purchased_order_id, purchased_items):
        errors = []
        for item in purchased_items:
            item_code = item.get('item_code')
            item['purchased'] = purchased_order_id
            purchased_item = PurchasedItems.objects.filter(purchased=purchased_order_id, item_code=item_code).last()
            if purchased_item:
                serializer = PurchasedItemSerializer(purchased_item, data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
            else:
                serializer = PurchasedItemSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return errors
        
    @authorize('create_purchased_order')
    def post(self, request):
        purchased_items = request.data.get('purchased_items')
        if request.data:
            submitted = request.data.get('submitted')
            po_reference = request.data.get('po_reference')
            
            if submitted:
                po_model = PoModel.objects.filter(id=po_reference).last()
                if po_model:
                    count = Purchased.objects.filter(po_reference__store=po_model.store, submitted=True).count()+1
                    request.data['purchase_grn'] = 'PURCHASE_'+po_model.store.store_uid+'_'+str(count).zfill(3)
                    request.data['submitted_at'] = datetime.datetime.now()
                else:
                    return JsonResponse({'message':'Invalid PO ID.', 'status':False, 'status_code':400}, status=400)
            
            serializer = PurchasedSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                errors = self.save_purchased_items(serializer.data['id'], purchased_items)
                serializer = PurchasedOrderReadSerializer(Purchased.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Purchased Order saved Successfully.', 'status':True,'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during saving Purchased order.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=200)
    
    def put(self, request):
        id = request.data.get('id')
        purchased = Purchased.objects.filter(id=id).last()
        purchased_items = request.data.get('purchased_items')
        submitted = request.data.get('submitted')
        
        if purchased:
            if purchased.submitted:
                return JsonResponse({'message':'Submitted Purchased orders cannot be edited.', 'status':False, 'status_code':400}, status=400)
            
            if submitted:
                po_model = PoModel.objects.filter(id=purchased.po_reference.id).last()
                if po_model:
                    count = Purchased.objects.filter(po_reference__store=po_model.store, submitted=True).count()+1
                    request.data['purchase_grn'] = 'PURCHASE_'+po_model.store.store_uid+'_'+str(count).zfill(3)
                    request.data['submitted_at'] = datetime.datetime.now()
                else:
                    return JsonResponse({'message':'Invalid PO ID.', 'status':False, 'status_code':400}, status=400)
            
            serializer = PurchasedSerializer(purchased, data=request.data)
            if serializer.is_valid():
                serializer.save()
                errors = self.save_purchased_items(serializer.data['id'], purchased_items)
                serializer = PurchasedOrderReadSerializer(Purchased.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Purchased Order saved Successfully.', 'status':True,'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during saving Purchased order.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)        
        return JsonResponse({'message':'Invalid Purchased order.', 'status':False, 'status_code':400}, status=200)
    
    
    def get(self, request):
        store = request.GET.get('store')
        po = request.GET.get('po')
        id  = request.GET.get('id')
        submitted = request.GET.get('submitted', None)
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(count_per_page)*int(page)
        start = end - int(count_per_page)
        
        if store:
            if submitted == 'true':
                purchased = Purchased.objects.filter(po_reference__store=store, submitted=True).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference__store=store, submitted=True).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            
            if submitted == 'false':
                purchased = Purchased.objects.filter(po_reference__store=store, submitted=False).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference__store=store, submitted=False).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            
            else:
                purchased = Purchased.objects.filter(po_reference__store=store).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference__store=store).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if po:
            if submitted == 'true':
                purchased = Purchased.objects.filter(po_reference=po, submitted=True).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference=po, submitted=True).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            
            if submitted == 'false':
                purchased = Purchased.objects.filter(po_reference=po, submitted=False).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference=po, submitted=False).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
            
            else:
                purchased = Purchased.objects.filter(po_reference=po).all()[start:end]
                serializer = PurchasedSerializer(purchased, many=True)
                count = Purchased.objects.filter(po_reference=po).count()
                return JsonResponse({'message':'Purchased Order Listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            purchased = Purchased.objects.filter(id=id).last()
            serializer = PurchasedOrderReadSerializer(purchased)
            return JsonResponse({'message':'Purchased Order.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'Invalid request. Store ID, PO ID or Purchased Order ID required.', 'status':False, 'status_code':400}, status=400)