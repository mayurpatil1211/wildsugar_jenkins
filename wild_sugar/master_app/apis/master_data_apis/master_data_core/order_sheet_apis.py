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


class OrderSheetApiView(APIView):
    @authorize('create_order_sheet')
    def post(self, request):
        if request.data:
            items = request.data.get('order_sheet_materials')
            if items:
                if request.data.get('submitted'):
                    request.data['status'] = 'ordered'
                serializer = OrderSheetSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    error, status = self.save_order_sheet_materials(items, serializer.data['id'])
                    if error:
                        OrderSheet.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during creating Order Sheet.', 'status':False, 'status_code':400, 'error':error}, status=400)
                    
                    serializer = OrderSheetReadSerializer(OrderSheet.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Order Sheet created successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                return JsonResponse({'message':'Error during creating Order Sheet.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Order Sheet Items required.', 'status_code':400, 'status':False}, status=400)
        return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
    
    def save_order_sheet_materials(self, items, order_sheet_id):
        errors = []
        ids = []
        
        
        
        for item in items:
            item['order_sheet'] = order_sheet_id
            serializer = OrderSheetItemSerializer(data=item)
            if serializer.is_valid():
                pass
            else:
                return serializer.errors, False
            
        
        for item in items:
            item['order_sheet'] = order_sheet_id
            if item.get('delete'):
                stissue = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
                if stissue:
                    ids.append(stissue.id)
                    
            stissue = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
            if stissue:
                serializer = OrderSheetItemSerializer(stissue, data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
            else:
                serializer = OrderSheetItemSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return serializer.errors, False
        if ids:
            OrderSheetItems.objects.filter(id__in = ids).delete()
        return {}, True
    
    def verify_data(self, items, order_sheet_id, status):
        order_sheet = OrderSheet.objects.filter(id=order_sheet_id).last()
        if order_sheet:
            # order_sheet_items = 
            print(order_sheet.status)
            if order_sheet.status == 'draft':
                for item in items:
                    item['order_sheet'] = order_sheet_id
                    if not item.get('delete'):
                        stissueitem = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
                        if stissueitem:
                            pass
                return True, {}
            
            if order_sheet.status == 'ordered':
                for item in items:
                    stissueitem = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
                    if stissueitem:
                        if stissueitem.ordered_quantity != item.get('ordered_quantity'):
                            return False, {'error':'Items already ordered. Cannot update order quantity.'}
                        else:
                            pass
                    else:
                        return False, {'error':'Items already ordered. Cannot add new items.'}
                return True, {}
            
            if order_sheet.status == 'issued':
                for item in items:
                    stissueitem = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
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
            
            if order_sheet.status == 'recieved':
                for item in items:
                    stissueitem = OrderSheetItems.objects.filter(order_sheet=order_sheet_id, item_code=item.get('item_code')).last()
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
                items = request.data.get('order_sheet_materials')
                
                order_sheet = OrderSheet.objects.filter(id=id).last()
                if order_sheet:
                    if not order_sheet.submitted:
                        if request.data.get('submitted'):
                            request.data['status'] = 'ordered'
                            request.data['submitted_on'] = datetime.datetime.now()
                            
                    if not order_sheet.issued:
                        if request.data.get('issued'):
                            request.data['status'] = 'issued'
                            request.data['issued_on'] = datetime.datetime.now()
                            
                            if request.data.get('submitted'):
                                del request.data['submitted']
                            
                            if request.data.get('submitted_on'):
                                del request.data['submitted_on']
                            
                    if not order_sheet.received:
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
                    
                    if order_sheet.status: # == 'draft' or order_sheet.status == 'ordered'
                        v_status, v_error = self.verify_data(items, id, order_sheet.status)
                        if v_error:
                            return JsonResponse({'message':'Error during updating ordered Order Sheet items.', 'status':False, 'status_code':400, 'error':v_error}, status=400)
                        
                        serializer = OrderSheetSerializer(order_sheet, data=request.data)
                        if serializer.is_valid():
                            error, status = self.save_order_sheet_materials(items, id)
                            if error:
                                return JsonResponse({'message':'Error during updating Order Sheet items.', 'status':False, 'status_code':400, 'error':error}, status=400)
                            
                            serializer.save()
                            serializer = OrderSheetReadSerializer(OrderSheet.objects.filter(id=serializer.data['id']).last())
                            return JsonResponse({'message':'Order Sheet updated Successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                        return JsonResponse({'message':'Error during updating Order Sheet.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                    return JsonResponse({'message':'Store request already ISSUED or RECIEVED.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid request. Order Sheet ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request', 'status':False, 'status_code':400}, status=400)
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            st = OrderSheet.objects.filter(id=id).last()
            if st:
                if st.status != 'issued' or st.status != 'recieved':
                    st.delete()
                    return JsonResponse({'message':'Order Sheet deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Request already Issued/Recived.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Ivalid ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        id = request.GET.get('id')
        # child_store = request.GET.get('child_store')
        # parent_store = request.GET.get('parent_store')
        # submitted = request.GET.get('submitted')
        # status = request.GET.get('status')
        
        
        from_b2b_client = request.GET.get('from_b2b_client')
        from_pos = request.GET.get('from_pos')
        from_department = request.GET.get('from_department')
        custom_order = request.GET.get('custom_order')
        submitted = request.GET.get('submitted')
        to_pos = request.GET.get('to_pos')
        to_department = request.GET.get('to_department')
        status = request.GET.get('status')
        
        issued  = request.GET.get('issued')
        received  = request.GET.get('received')
        
        
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 20)
        
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
                
        if from_b2b_client:
            obj['from_b2b_client'] = from_b2b_client
                
        if custom_order:
            if custom_order == 'true':
                obj['custom_order'] = True
            else:
                obj['custom_order'] = False
                
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
            order_sheet = OrderSheet.objects.filter(id=id).last()
            serializer = OrderSheetReadSerializer(order_sheet)
            return JsonResponse({'message':'Order Sheet Details.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if from_pos:
            if from_department:
                order_sheet = OrderSheet.objects.filter(from_pos=from_pos, from_department=from_department).filter(**obj).all()[start:end]
                count = OrderSheet.objects.filter(from_pos=from_pos, from_department=from_department).filter(**obj).count()
                
            else:
                order_sheet = OrderSheet.objects.filter(from_pos=from_pos).filter(**obj).all()[start:end]
                count = OrderSheet.objects.filter(from_pos=from_pos).filter(**obj).count()
                
            serializer = OrderSheetReadSerializer(order_sheet, many=True)
            return JsonResponse({'message':'Order Sheet Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        
        if to_pos:
            if to_department:
                order_sheet = OrderSheet.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).all()[start:end]
                count = OrderSheet.objects.filter(to_pos=to_pos, to_department=to_department).filter(**obj).count()
                
            else:
                order_sheet = OrderSheet.objects.filter(to_pos=to_pos).filter(**obj).all()[start:end]
                count = OrderSheet.objects.filter(to_pos=to_pos).filter(**obj).count()
                
            serializer = OrderSheetReadSerializer(order_sheet, many=True)
            return JsonResponse({'message':'Order Sheet Details.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        return JsonResponse({'message':'ID/Child Store/Parent Store ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    
    
    
class OrderSheetItemsFilterApiView(APIView):
    def post(self, request):
        to_pos = request.data.get('pos')
        dept = request.data.get('department')
        
        filters = request.data.get('filters', {})
        
        page = request.data.get('page', 1)
        count_per_page = request.data.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if to_pos and dept:
            order_sheet_items = OrderSheetItems.objects.filter(order_sheet__to_pos=to_pos, order_sheet__to_department=dept).all()
            print(order_sheet_items)
            if filters:
                category = filters.get('category', [])
                sub_category  = filters.get('sub_category', [])
                high_value_item  = filters.get('high_value_item')
                consumable  = filters.get('consumable')
                planned  = filters.get('planned')
                
                
                if order_sheet_items:
                    if category:
                        order_sheet_items = order_sheet_items.filter(queue(raw_material__category__in=category) | queue(final_product__category__in=category) | queue(semi_product__category__in=category)).all()
                    
                    if sub_category:
                        order_sheet_items = order_sheet_items.filter(queue(raw_material__sub_category__in=sub_category) | queue(final_product__sub_category__in=sub_category) | queue(semi_product__sub_category__in=sub_category)).all()
                    
                    if high_value_item is not None:
                        order_sheet_items = order_sheet_items.filter(queue(raw_material__high_value_item=high_value_item) | queue(final_product__high_value_item=high_value_item) | queue(semi_product__high_value_item=high_value_item)).all()
                    
                    if consumable is not None:
                        order_sheet_items = order_sheet_items.filter(raw_material__consumable=consumable).all()
                        
                    
                    
                    serializer = OrderSheetItemBriefReadSerializer(order_sheet_items, many=True)
                    count = order_sheet_items.count()
                    return JsonResponse({'message':'Order Sheet Items result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
                return JsonResponse({'message':'Order Sheet Items result.', 'status':True, 'status_code':200, 'result':[]}, status=200)
            serializer = OrderSheetItemBriefReadSerializer(order_sheet_items, many=True)
            count = order_sheet_items.count()
            return JsonResponse({'message':'Order Sheet Items result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'POS and Department ID required required.', 'status':True, 'status_code':400, 'result':[]}, status=400)
    
    
class OrderSheetRawMaterialEstimate(APIView):
    @authorize('estimate_raw_material')
    def post(self, request):
        ids = request.data.get('item_ids')
        
        if ids:
            print(ids)
            
            order_sheet_items = OrderSheetItems.objects.filter(id__in=ids).all()
            if order_sheet_items:
                print(order_sheet_items)
                self.start_estimation(order_sheet_items)
                return JsonResponse({'message':'Raw Material Estimation.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'Order Sheet Item IDs required.', 'status':False, 'status_code':400}, status=400)
    
    def get_recipe_materials(self, item_code, quantity, raw_materials={}):
        recipe_ingredients = RecipeIngredients.objects.filter(recipe__item_code=item_code).all()
        for ingredient in recipe_ingredients:
            if ingredient.raw_material:
                print(ingredient.quantity * quantity, ingredient.quantity , quantity)
                if ingredient.ingredient_code in raw_materials:
                    
                    raw_materials[ingredient.ingredient_code] += ingredient.quantity * quantity
                else:
                    raw_materials[ingredient.ingredient_code] = ingredient.quantity * quantity
            
            if ingredient.semi_product:
                raw_materials = self.get_recipe_materials(ingredient.ingredient_code, quantity, raw_materials)
        return raw_materials
    
    def start_estimation(self, order_sheet_items):
        raw_materials = {}
        for i in order_sheet_items:
            print(i)
            if i.raw_material:
                if i.item_code in raw_materials:
                    raw_materials[i.item_code] += i.default_uom_quantity * i.ordered_quantity
                else:
                    raw_materials[i.item_code] = i.default_uom_quantity * i.ordered_quantity
            
            elif i.final_product:
                materials = self.get_recipe_materials(i.item_code, i.ordered_quantity, {})
                print(materials)
            
            elif i.semi_product:
                materials = self.get_recipe_materials(i.item_code, i.ordered_quantity, {})
                print(materials)
    
    
    
    
    
    