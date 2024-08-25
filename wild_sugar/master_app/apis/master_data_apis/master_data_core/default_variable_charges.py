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


class DefaultVariableChargesApiView(APIView):
    @authorize('create_variable_charges')
    def post(self, request):
        if request.data:
            variable_charge_code = request.data.get('variable_charge_code', None)
            variable_charge = request.data.get('variable_charge', None)
            variable_charge_description = request.data.get('variable_charge_description', None)
            
            if variable_charge_code and variable_charge and variable_charge_description:
                old_variable = DefaultVariableCharges.objects.filter(variable_charge_code=variable_charge_code).last()
                if old_variable:
                    serializer = DefaultVariableChargeSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        old_variable.latest = False
                        old_variable.save()
                        return JsonResponse({"message":"Default Variable Charge Registered successfully.", 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                    else:
                        return JsonResponse({'message':'Error during creating default variable charge.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                    
                else:
                    serializer = DefaultVariableChargeSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"message":"Default Variable Charge Registered successfully.", 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                    else:
                        return JsonResponse({'message':'Error during creating default variable charge.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                    
            return JsonResponse({'message':'Variable charge code, Variable charge value and Variable charge description required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_variable_charges')
    def put(self, request):
        id = request.data.get('id', None)
        variable_charge_code = request.data.get('variable_charge_code', None)
        variable_charge = request.data.get('variable_charge', None)
        variable_charge_description = request.data.get('variable_charge_description', None)
        
        if id and variable_charge and variable_charge_code and variable_charge_description:
            old_variable = DefaultVariableCharges.objects.filter(id=id).last()
            if old_variable:
                serializer = DefaultVariableChargeSerializer(old_variable, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Variable charge updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating variable charge.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'ID, Variable Charge, Variable Charge Code and Variable Charge Description Required.', 'status':False, 'status_code':400}, status=400)

    def get(self, request):
        id = request.GET.get('id', None)
        brand = request.GET.get('brand', None)
        query = request.GET.get('query', None)
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        try:
            end = int(page)*int(count_per_page)
        except(Exception)as e:
            end = 1*20
        
        try:
            start = end - int(count_per_page)
        except(Exception)as e:
            start = end - 20
        
        if id:
            variable = DefaultVariableCharges.objects.filter(id=id).last()
            serializer = DefaultVariableChargeSerializer(variable)
            return JsonResponse({'message':'Default variable charge.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                variables = DefaultVariableCharges.objects.filter(latest=True, deleted=False, brand=brand).filter(queue(variable_charge_code__icontains=query)|queue(variable_charge__icontains=query)|queue(variable_charge_description__icontains=query)).all()[start:end]
                count = DefaultVariableCharges.objects.filter(latest=True, deleted=False, brand=brand).filter(queue(variable_charge_code__icontains=query)|queue(variable_charge__icontains=query)|queue(variable_charge_description__icontains=query)).count()
            else:
                variables = DefaultVariableCharges.objects.filter(latest=True, deleted=False, brand=brand).all()[start:end]
                count = DefaultVariableCharges.objects.filter(latest=True, deleted=False, brand=brand).count()
            serializer = DefaultVariableChargeSerializer(variables, many=True)
            return JsonResponse({'message':'Variable charges.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_variable_charges')
    def delete(self, request):
        id = request.data.get('id')
        
        if id:
            DefaultVariableCharges.objects.filter(id=id).delete()
            return JsonResponse({'message':'Default Variable Charge deleted successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400})