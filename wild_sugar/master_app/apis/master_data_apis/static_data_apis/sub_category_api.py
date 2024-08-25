from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

class SubcategoryListApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            serializer = SubcategoryListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Subcategory registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        brand = request.GET.get('brand', None)
        
        id = request.GET.get('id', None)
        if id:
            queryset = SubcategoryList.objects.filter(id=id).last()
            serializer=SubcategoryListSerializer(queryset)
            return JsonResponse({'message':'Subcategory info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            queryset = SubcategoryList.objects.all()
            serializer = SubcategoryListSerializer(queryset, many=True)
            return JsonResponse({'message':'Subcategory info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_types')
    def put(self, request):
        sub_category_id=request.data.get("id")
        sub_category_info = SubcategoryList.objects.get(id=sub_category_id)
        if sub_category_info:
            serializer = SubcategoryListSerializer(sub_category_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Subcategory info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)

    @authorize('register_types')
    def delete(self, request):
        sub_category_id=request.data.get("id")
        sub_category_info = SubcategoryList.objects.filter(id=sub_category_id)
        if sub_category_info:
            sub_category_info.delete()
            return JsonResponse({'message':'sub_categoryinfo deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)