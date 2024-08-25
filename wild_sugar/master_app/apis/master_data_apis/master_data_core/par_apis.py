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



class PeriodicAutomaticReplacementApiView(APIView):
    @authorize('create_par')
    def post(self, request):
        if request.data:
            for i in request.data.get('par_values'):
                
                if i.get('final_product') or i.get('semi_product') or i.get('raw_material'):
                    print(i)
                    serializer = PeriodicAutomaticReplacementSerializer(data=i)
                    if serializer.is_valid():
                        pass
                    else:
                        return JsonResponse({'message':'Invalid request, "Final Product ID / Semi Product ID / Raw Material ID" required.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            
            serializer = PeriodicAutomaticReplacementSerializer(data=request.data.get('par_values'), many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'PAR values saved successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'message':'Invalid request, Please check the data you are sending.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request, Please check the data you are sending.', 'status':False, 'status_code':400}, status=400)
    
    
    def put(self, request):
        if request.data:
            errors = []
            for i in request.data.get('par_values'):
                if i.get('final_product') or i.get('semi_product') or i.get('raw_material'):
                    serializer = PeriodicAutomaticReplacementSerializer(data=i)
                    if serializer.is_valid():
                        pass
                    else:
                        return JsonResponse({'message':'Invalid request, "Final Product ID / Semi Product ID / Raw Material ID" required.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            for i in request.data.get('par_values'):
                par = PeriodicAutomaticReplacement.objects.filter(pos=i.get('pos'), department=i.get('department'), item_code=i.get('item_code')).last()
                if par:
                    serializer = PeriodicAutomaticReplacementSerializer(par, data=i)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        errors.append(serializer.errors)
                else:
                    serializer = PeriodicAutomaticReplacementSerializer(data=i)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        errors.append(serializer.errors)
            if not errors:
                return JsonResponse({'message':'PAR values updated successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'Error during updating PAR values.', 'status_code':400, 'status':False}, status=400)
        return JsonResponse({'message':'Invalid request, Please check the data you are sending.', 'status':False, 'status_code':400}, status=400)
    
    def delete(self, request):
        if request.data.get('id'):
            PeriodicAutomaticReplacement.objects.filter(id=request.data.get('id')).delete()
        return JsonResponse({'message':'PAR value deleted successfully.', 'status':True, 'status_code':200}, status=200)
    
    
    def get(self, request):
        pos_id = request.GET.get('pos')
        dept = request.GET.get('department')
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        try:
            end = int(page)*int(count_per_page)
        except(Exception) as e:
            end = 1*50
            
        try:
            start = end - int(count_per_page)
        except(Exception)as e:
            start = end-50
            
        if pos_id and dept:
            par = PeriodicAutomaticReplacement.objects.filter(pos=pos_id, department=dept).all()[start:end]
            serializer = PeriodicAutomaticReplacementReadSerializer(par, many=True)
            count = PeriodicAutomaticReplacement.objects.filter(pos=pos_id, department=dept).count()
            return JsonResponse({'message':'PAR values listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        elif pos_id:
            par = PeriodicAutomaticReplacement.objects.filter(pos=pos_id).all()[start:end]
            serializer = PeriodicAutomaticReplacementReadSerializer(par, many=True)
            count = PeriodicAutomaticReplacement.objects.filter(pos=pos_id).count()
            return JsonResponse({'message':'PAR values listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        elif dept:
            par = PeriodicAutomaticReplacement.objects.filter(department=dept).all()[start:end]
            serializer = PeriodicAutomaticReplacementReadSerializer(par, many=True)
            count = PeriodicAutomaticReplacement.objects.filter(department=dept).count()
            return JsonResponse({'message':'PAR values listing.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        else:
            return JsonResponse({'message':'POS ID and Department ID required.', 'status':False, 'status_code':400}, status=400)
        
class CopyParApiView(APIView):
    @authorize('copy_par_values')
    def post(self, request):
        copy_from_pos = request.data.get('pos')
        copy_from_dept = request.data.get('department')
        copy_tos = request.data.get('copy_to')
        errors = []
        if copy_from_pos and copy_tos and copy_from_dept:
            
            for copy_to in copy_tos: 
                if copy_to.get('pos') and copy_to.get('department'):
                    pars = PeriodicAutomaticReplacement.objects.filter(pos=copy_from_pos, department=copy_from_dept).all()
                    for par in pars:
                        serializer = PeriodicAutomaticReplacementSerializer(data={
                            "pos" : copy_to.get('pos') ,
                            "department" : copy_to.get('department') ,
                            "final_product" : par.final_product.id if par.final_product else None,
                            "semi_product" : par.semi_product.id if par.semi_product else None ,
                            "raw_material" : par.raw_material.id if par.raw_material else None ,
                            "item_name" : par.item_name ,
                            "item_code" : par.item_code ,
                            "default_uom" : par.default_uom ,
                            "default_uom_quantity" : par.default_uom_quantity ,
                            "default_value_for_day" : par.default_value_for_day ,
                            "value_for_week_day" : par.value_for_week_day 
                        })
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append(serializer.errors)
                            break
            return JsonResponse({'message':'PAR values coppied to POS and Departments.', 'status':True, 'status_code':200, 'error':errors}, status=200)
        return JsonResponse({'message':'POS ID with Department ID required.', 'status':False, 'status_code':400}, status=400)