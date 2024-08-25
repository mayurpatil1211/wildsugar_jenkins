from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

class AssetTypesApiView(APIView):
    @authorize('register_types')
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer =AssetTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Asset type registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

    def get(self, request):
        brand = request.GET.get('brand', None)
        
        id = request.GET.get('id', None)
        
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
            queryset = AssetTypes.objects.filter(id=id).last()
            serializer=AssetTypeSerializer(queryset)
            return JsonResponse({'message':'Asset list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                queryset = AssetTypes.objects.filter(brand = brand).filter(queue(asset_type__icontains=query)|queue(asset_type_description__icontains=query))[start:end]
                count = AssetTypes.objects.filter(brand = brand).filter(queue(asset_type__icontains=query)|queue(asset_type_description__icontains=query)).count()
            else:
                queryset = AssetTypes.objects.filter(brand = brand).all()[start:end]
                count =  AssetTypes.objects.filter(brand = brand).count()
            serializer = AssetTypeSerializer(queryset, many=True)
            return JsonResponse({'message':'Asset list', 'status':True, 'status_code':200, 'result':serializer.data, 'count' : count}, status=200)
        
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_types')
    def put(self, request):
        asset_type_id=request.data.get("id")
        asset_type_info = AssetTypes.objects.filter(id=asset_type_id).last()
        if asset_type_info:
            serializer = AssetTypeSerializer(asset_type_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Asset type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('register_types')
    def delete(self, request):
        asset_type_id=request.data.get("id")
        asset_type_info = AssetTypes.objects.filter(id=asset_type_id)
        if asset_type_info:
            asset_type_info.delete()
            return JsonResponse({'message':'Asset type deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
        