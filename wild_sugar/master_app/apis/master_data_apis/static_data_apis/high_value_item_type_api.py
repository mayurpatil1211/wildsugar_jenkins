from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class HighValueItemTypeApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer = HighValueItemTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'High value item registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

    def get(self, request):
        brand = request.GET.get('brand', None)
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = end - int(count_per_page)
        
        id = request.GET.get('id', None)
        
        if id:
            queryset = HighValueItemTypes.objects.filter(id=id).last()
            serializer=HighValueItemTypeSerializer(queryset)
            return JsonResponse({'message':'High value item', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            queryset = HighValueItemTypes.objects.filter(brand=brand).all()
            serializer = HighValueItemTypeSerializer(queryset, many=True)
            return JsonResponse({'message':'High value item list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':HighValueItemTypes.objects.filter(brand=brand).count()}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_types')
    def put(self, request):
        high_value_item_id=request.data.get("id")
        high_value_item_info = HighValueItemTypes.objects.filter(id=high_value_item_id).last()
        if high_value_item_info:
            serializer = HighValueItemTypeSerializer(high_value_item_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'High value item type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('register_types')
    def delete(self, request):
        high_value_item_id=request.data.get("id")
        high_value_item_info = HighValueItemTypes.objects.filter(id=high_value_item_id)
        if high_value_item_info:
            high_value_item_info.delete()
            return JsonResponse({'message':'High value item type deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)