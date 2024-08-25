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


class StoreIssueApiView(APIView):
    @authorize('create_store_issue')
    def post(self, request):
        if request.data:
            items = request.data.get('store_issue_materials')
            if items:
                if request.data.get('submitted'):
                    request.data['status'] = 'ordered'
                    request.data['submitted_on'] = datetime.datetime.now()
                
                print(request.data)
                serializer = StoreIssueSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    error, status = self.save_store_issue_materials(items, serializer.data['id'])
                    if error:
                        StoreIssue.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during creating store issue.', 'status':False, 'status_code':400, 'error':error}, status=400)
                    
                    serializer = StoreIssueReadSerializer(StoreIssue.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Store Issue created successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                return JsonResponse({'message':'Error during creating store issue.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Store Issue Items required.', 'status_code':400, 'status':False}, status=400)
        return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
    
    def save_store_issue_materials(self, items, store_issue_id):
        errors = []
        ids = []
        
        
        
        for item in items:
            item['store_issue'] = store_issue_id
            serializer = StoreIssueItemSerializer(data=item)
            if serializer.is_valid():
                pass
            else:
                return serializer.errors, False
            
        
        for item in items:
            item['store_issue'] = store_issue_id
            if item.get('delete'):
                stissue = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
                if stissue:
                    ids.append(stissue.id)
                    
            stissue = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
            if stissue:
                serializer = StoreIssueItemSerializer(stissue, data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
            else:
                serializer = StoreIssueItemSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
        if ids:
            StoreIssueItems.objects.filter(id__in = ids).delete()
        return {}, True
    
    def verify_data(self, items, store_issue_id, status):
        store_issue = StoreIssue.objects.filter(id=store_issue_id).last()
        if store_issue:
            # store_issue_items = 
            print(store_issue.status)
            if store_issue.status == 'draft':
                for item in items:
                    item['store_issue'] = store_issue_id
                    if not item.get('delete'):
                        stissueitem = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
                        if stissueitem:
                            pass
                return True, {}
            
            if store_issue.status == 'ordered':
                for item in items:
                    stissueitem = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
                    if stissueitem:
                        if stissueitem.ordered_quantity != item.get('ordered_quantity'):
                            return False, {'error':'Items already ordered. Cannot update order quantity.'}
                        else:
                            pass
                    else:
                        return False, {'error':'Items already ordered. Cannot add new items.'}
                return True, {}
            
            if store_issue.status == 'issued':
                for item in items:
                    stissueitem = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
                    if stissueitem:
                        print(stissueitem.ordered_quantity , item.get('ordered_quantity'))
                        print(stissueitem.issued_quantity , item.get('issued_quantity'))
                        if stissueitem.ordered_quantity != item.get('ordered_quantity') or stissueitem.issued_quantity != item.get('issued_quantity'):
                            return False, {'error':'Items already ordered/Issued. Cannot update order/issued quantity.'}
                        else:
                            pass
                    else:
                        return False, {'error':'Items already ordered/Issued. Cannot add new items.'}
                return True, {}
            
            if store_issue.status == 'recieved':
                for item in items:
                    stissueitem = StoreIssueItems.objects.filter(store_issue=store_issue_id, item_code=item.get('item_code')).last()
                    if stissueitem:
                        if stissueitem.ordered_quantity != item.get('ordered_quantity') or stissueitem.issued_quantity != item.get('issued_quantity'):
                            return False, {'error':'Items already ordered/Issued. Cannot update order/issued quantity.'}
                        else:
                            pass
                    else:
                        return False, {'error':'Items already ordered/Issued. Cannot add new items.'}
                return True, {}
        else:
            return True, {}
                
    
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                items = request.data.get('store_issue_materials')
                
                store_issue = StoreIssue.objects.filter(id=id).last()
                if store_issue:
                    if not store_issue.submitted:
                        if request.data.get('submitted'):
                            request.data['status'] = 'ordered'
                            request.data['submitted_on'] = datetime.datetime.now()
                            
                    if not store_issue.issued:
                        if request.data.get('issued'):
                            request.data['status'] = 'issued'
                            request.data['issued_on'] = datetime.datetime.now()
                            
                            if request.data.get('submitted'):
                                del request.data['submitted']
                            
                            if request.data.get('submitted_on'):
                                del request.data['submitted_on']
                            
                    if not store_issue.received:
                        if request.data.get('received'):
                            request.data['status'] = 'received'
                            request.data['received_on'] = datetime.datetime.now()
                            
                            if request.data.get('submitted'):
                                del request.data['submitted']
                            
                            if request.data.get('submitted_on'):
                                del request.data['submitted_on']
                            
                            if request.data.get('issued'):
                                del request.data['issued']
                            
                            if request.data.get('issued_on'):
                                del request.data['issued_on']
                    
                    if store_issue.status: # == 'draft' or store_issue.status == 'ordered'
                        v_status, v_error = self.verify_data(items, id, store_issue.status)
                        if v_error:
                            return JsonResponse({'message':'Error during updating ordered store issue items.', 'status':False, 'status_code':400, 'error':v_error}, status=400)
                        
                        serializer = StoreIssueSerializer(store_issue, data=request.data)
                        if serializer.is_valid():
                            error, status = self.save_store_issue_materials(items, id)
                            if error:
                                return JsonResponse({'message':'Error during updating store issue items.', 'status':False, 'status_code':400, 'error':error}, status=400)
                            
                            serializer.save()
                            serializer = StoreIssueReadSerializer(StoreIssue.objects.filter(id=serializer.data['id']).last())
                            return JsonResponse({'message':'Store Issue updated Successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                        return JsonResponse({'message':'Error during updating store issue.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                    return JsonResponse({'message':'Store request already ISSUED or RECIEVED.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request. Store Issue ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request', 'status':False, 'status_code':400}, status=400)
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            st = StoreIssue.objects.filter(id=id).last()
            if st:
                if st.status != 'issued' or st.status != 'recieved':
                    st.delete()
                    return JsonResponse({'message':'Store Material Issue request deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Request already Issued/Recived.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Ivalid ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        id = request.GET.get('id')
        child_store = request.GET.get('child_store')
        
        parent_store = request.GET.get('parent_store')
        submitted = request.GET.get('submitted')
        received = request.GET.get('received')
        issued = request.GET.get('issued')
        status = request.GET.get('status')
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        to_pos = request.GET.get('to_pos')
        to_department = request.GET.get('to_department')
        
        obj = {}
        
        if submitted:
            if submitted == 'true':
                obj['submitted'] = True
            else:
                obj['submitted'] = False
        
        if issued:
            if issued == 'true':
                obj['issued'] = True
            else:
                obj['issued'] = False
        
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
            store_issue = StoreIssue.objects.filter(id=id).last()
            serializer = StoreIssueReadSerializer(store_issue)
            return JsonResponse({'message':'Store Issue Details.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if to_pos and to_department:
            store_issue = StoreIssue.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).all()
            serializer = StoreIssueReadSerializer(store_issue, many=True)
            count = StoreIssue.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).count()
            return JsonResponse({'message':'Store Issue Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        elif to_pos:
            store_issue = StoreIssue.objects.filter(to_pos=to_pos).filter(**obj).all()
            serializer = StoreIssueReadSerializer(store_issue, many=True)
            count = StoreIssue.objects.filter(to_pos=to_pos).filter(**obj).count()
            return JsonResponse({'message':'Store Issue Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if parent_store:
            store_issue = StoreIssue.objects.filter(parent_store=parent_store).filter(**obj).all()
            serializer = StoreIssueReadSerializer(store_issue, many=True)
            count = StoreIssue.objects.filter(parent_store=parent_store).filter(**obj).count()
            return JsonResponse({'message':'Store Issue Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'ID/Child Store/Parent Store ID required.', 'status':False, 'status_code':400}, status=400)
    
    