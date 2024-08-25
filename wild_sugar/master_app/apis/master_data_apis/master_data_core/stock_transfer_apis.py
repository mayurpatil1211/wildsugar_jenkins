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


class StockTransferApiView(APIView):
    @authorize('create_stock_transfer')
    def post(self, request):
        if request.data:
            if request.data.get('submitted'):
                request.data['submitted_on'] = datetime.datetime.now()
                request.data['status'] = 'issued'
            
            stock_transfer_materials = request.data.get('stock_transfer_materials')
            
            serializer = StockTransferSerializer(data=request.data)
            if serializer.is_valid():
                
                serializer.save()
                error, status =self.save_stock_transfer_materials(stock_transfer_materials, serializer.data['id'])
                if error:
                    StockTransfer.objects.filter(id=serializer.data['id']).delete()
                    return JsonResponse({'message':'Error during creating stock transfer items.', 'status':False, 'status_code':400, 'error':error}, status=400)
                serializer = StockTransferReadSerializer(StockTransfer.objects.filter(id=serializer.data['id']).last(), many=False)
                return JsonResponse({'message':'Stock transfer saved successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during saving Stock Transfer records.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    def save_stock_transfer_materials(self, items, stock_transfer_id):
        ids=[]
        
        for item in items:
            if item.get('raw_material') or item.get('final_product') or item.get('semi_product'): 
                item['stock_transfer'] = stock_transfer_id
                serializer = StockTransferItemSerializer(data=item)
                if serializer.is_valid():
                    pass
                else:
                    return serializer.errors, False
            else:
                return {'error':'Raw Material/Semi Product/Final Product ID required.'}, False
        
        for item in items:
            item['stock_transfer'] = stock_transfer_id
            if item.get('delete'):
                stissue = StockTransferItems.objects.filter(stock_transfer=stock_transfer_id, item_code=item.get('item_code')).last()
                if stissue:
                    ids.append(stissue.id)
                    
            stissue = StockTransferItems.objects.filter(stock_transfer=stock_transfer_id, item_code=item.get('item_code')).last()
            if stissue:
                serializer = StockTransferItemSerializer(stissue, data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
            else:
                serializer = StockTransferItemSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
        
        if ids:
            StockTransferItems.objects.filter(id__in = ids).delete()
        return {}, True

    
    def verify_data(self, items, stock_transfer_id, status):
        stock_transfer = StockTransfer.objects.filter(id=stock_transfer_id).last()
        if stock_transfer:
            if stock_transfer.status == 'draft':
                for item in items:
                    item['stock_transfer'] = stock_transfer_id
                    if not item.get('delete'):
                        stocktransitem = StockTransferItems.objects.filter(stock_transfer=stock_transfer_id, item_code=item.get('item_code')).last()
                        if stocktransitem:
                            serializer = StockTransferItemSerializer(stocktransitem, data=item)
                            if serializer.is_valid():
                                pass
                            else:
                                return False, serializer.errors
                        else:
                            serializer = StockTransferItemSerializer(data=item)
                            if serializer.is_valid():
                                pass
                            else:
                                return False, serializer.errors
                return True, {}
            
            
            if stock_transfer.status == 'issued':
                for item in items:
                    item['stock_transfer'] = stock_transfer_id
                    stocktransitem = StockTransferItems.objects.filter(stock_transfer=stock_transfer_id, item_code=item.get('item_code')).last()
                    if stocktransitem:
                        
                        if stocktransitem.issued_quantity != item.get('issued_quantity'):
                            return False, {'error':'Items already Issued. Cannot update issued quantity.'}
                        else:
                            serializer = StockTransferItemSerializer(stocktransitem, data=item)
                            if serializer.is_valid():
                                pass
                            else:
                                return False, serializer.errors
                    else:
                        return False, {'error':'Items already Issued. Cannot add new items.'}
                return True, {}
            
            if stock_transfer.status == 'received':
                
                for item in items:
                    item['stock_transfer'] = stock_transfer_id
                    stocktransitem = StockTransferItems.objects.filter(stock_transfer=stock_transfer_id, item_code=item.get('item_code')).last()
                    if stocktransitem:
                        if stocktransitem.received_quantity != item.get('received_quantity') or stocktransitem.issued_quantity != item.get('issued_quantity'):
                            return False, {'error':'Items already Issued. Cannot update issued quantity.'}
                        else:
                            serializer = StockTransferItemSerializer(stocktransitem, data=item)
                            if serializer.is_valid():
                                pass
                            else:
                                return False, serializer.errors
                    else:
                        return False, {'error':'Items already Issued. Cannot add new items.'}
                return True, {}
        else:
            return True, {}
                
    
    
    
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                items = request.data.get('stock_transfer_materials')
                
                store_issue = StockTransfer.objects.filter(id=id).last()
                if store_issue:
                    if not store_issue.submitted:
                        if request.data.get('submitted'):
                            request.data['status'] = 'issued'
                            request.data['submitted_on'] = datetime.datetime.now()
                            
                            
                    if not store_issue.received:
                        if request.data.get('received'):
                            request.data['status'] = 'received'
                            request.data['received_on'] = datetime.datetime.now()
                            
                            if request.data.get('submitted'):
                                del request.data['submitted']
                            
                            if request.data.get('submitted_on'):
                                del request.data['submitted_on']
                            
                    
                    if store_issue.status: # == 'draft' or store_issue.status == 'ordered'
                        v_status, v_error = self.verify_data(items, id, store_issue.status)
                        
                        if v_error:
                            return JsonResponse({'message':'Error during updating ordered Stock Transfer items.', 'status':False, 'status_code':400, 'error':v_error}, status=400)
                        
                        serializer = StockTransferSerializer(store_issue, data=request.data)
                        if serializer.is_valid():
                            error, status = self.save_stock_transfer_materials(items, id)
                            if error:
                                return JsonResponse({'message':'Error during updating Stock Transfer items.', 'status':False, 'status_code':400, 'error':error}, status=400)
                            
                            serializer.save()
                            serializer = StockTransferReadSerializer(StockTransfer.objects.filter(id=serializer.data['id']).last())
                            return JsonResponse({'message':'Stock Transfer updated Successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                        return JsonResponse({'message':'Error during updating Stock Transfer.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                    return JsonResponse({'message':'Store request already ISSUED or RECIEVED.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request. Stock Transfer ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        received = request.GET.get('received')
        submitted = request.GET.get('submitted')
        status = request.GET.get('status')
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 20)
        id = request.GET.get('id')
        from_pos = request.GET.get('from_pos')
        to_pos = request.GET.get('to_pos')
        from_department = request.GET.get('from_department')
        to_department = request.GET.get('to_department')
        
        obj = {}
        
        if submitted:
            if submitted == 'true':
                obj['submitted'] = True
            else:
                obj['submitted'] = False
        
        if received:
            if received == 'true':
                obj['received'] = True
            else:
                obj['received'] = False
                
        if status:
            obj['status__iexact'] = status
            
        try:
            end = int(page)*int(count_per_page)
        except(Exception)as e:
            end = 1*20
        
        try:
            start = end-int(count_per_page)
        except(Exception)as e:
            start = end-20
        
        if id:
            stock_transfer = StockTransfer.objects.filter(id=id).last()
            serializer = StockTransferReadSerializer(stock_transfer)
            return JsonResponse({'message':'Stock Transfer Details.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if from_pos and from_department:
            stock_transfer = StockTransfer.objects.filter(from_pos=from_pos, from_department=from_department).filter(**obj).all()
            serializer = StockTransferReadSerializer(stock_transfer, many=True)
            count = StockTransfer.objects.filter(from_pos=from_pos, from_department=from_department).filter(**obj).count()
            return JsonResponse({'message':'Stock Transfer Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if to_pos and to_department:
            stock_transfer = StockTransfer.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).all()
            serializer = StockTransferReadSerializer(stock_transfer, many=True)
            count = StockTransfer.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).count()
            return JsonResponse({'message':'Stock Transfer Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'POS and Department ID / Stock Transfer ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    def delete(self,request):
        id  = request.data.get('id')
        if id:
            st = StockTransfer.objects.filter(id=id).last()
            if st and st.submitted:
                return JsonResponse({'message':'Cannot delete records.', 'status':False, 'status_code':400}, status=400)
            elif st:
                st.delete()
                return JsonResponse({'message':'Stock Transfer records Deleted.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)