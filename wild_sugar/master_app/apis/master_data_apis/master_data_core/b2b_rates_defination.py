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


class B2BRatesDefinitionApiView(APIView):
    @authorize('register_b2b_rates_definition')
    def post(self, request):
        if request.data:
            serializer = B2BRatesDefinitionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'B2B rate defination added.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during saving rates defination.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('list_b2b_rates_definition')
    def get(self, request):
        brand = request.GET.get('brand', None)
        query = request.GET.get('query', None)
        final_product = request.GET.get('final_product', None)
        b2b_client = request.GET.get('b2b_client', None)
        id = request.GET.get('id', None)
        
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 20)
        
        end = int(limit)*int(page)
        start = end - int(limit)
        
        if brand:
            if query:
                rate_defination = B2BRatesDefinition.objects.filter(final_product__brand = brand).filter(
                        queue(final_product__item_code=query) | queue(final_product__item_name=query) | queue(b2b_client__client_code=query) | queue(b2b_client__client_name=query)
                    )[start:end]
                serializer = B2bRatesDefinitionReadSerializer(rate_defination, many=True)
                count = B2BRatesDefinition.objects.filter(final_product__brand = brand).filter(
                        queue(final_product__item_code=query) | queue(final_product__item_name=query) | queue(b2b_client__client_code=query) | queue(b2b_client__client_name=query)
                    ).count()
            else:
                rate_defination = B2BRatesDefinition.objects.filter(final_product__brand = brand)[start:end]
                serializer = B2bRatesDefinitionReadSerializer(rate_defination, many=True)
                count = B2BRatesDefinition.objects.filter(final_product__brand = brand).count()
                print(serializer.data)
            return JsonResponse({'message':'B2B rates defination.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if final_product:
            rate_defination = B2BRatesDefinition.objects.filter(final_product = final_product).all()
            serializer = B2bRatesDefinitionReadSerializer(rate_defination, many=True)
            return JsonResponse({'message':'B2B rates defination.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if b2b_client:
            rate_defination = B2BRatesDefinition.objects.filter(b2b_client = b2b_client).all()
            serializer = B2bRatesDefinitionReadSerializer(rate_defination, many=True)
            return JsonResponse({'message':'B2B rates defination.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            rate_defination = B2BRatesDefinition.objects.filter(id=id).last()
            serializer = B2bRatesDefinitionReadSerializer(rate_defination)
            return JsonResponse({'message':'B2B rates defination.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'Invalid request. Brand ID or Product ID or B2B client ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_b2b_rates_definition')
    def put(self, request):
        id = request.data.get('id', None)
        if id:
            b2b_rate = B2BRatesDefinition.objects.filter(id=id).last()
            if b2b_rate:
                serializer = B2BRatesDefinitionSerializer(b2b_rate, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'B2B rate defination updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating B2B rate defination.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid ID. Rate defination could not find.', 'status':False, 'status_code':404}, status=404)
        return JsonResponse({'message':'Rate defination ID required.', 'status':False, 'status_code':400}, status=200)
    
    @authorize('delete_b2b_rates_definition')
    def delete(self, request):
        id = request.data.get('id', None)
        B2BRatesDefinition.objects.filter(id=id).delete()
        return JsonResponse({'message':'B2B rate defination deleted successfully.', 'status':True, 'status_code':200}, status=200)