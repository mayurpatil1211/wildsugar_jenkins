from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

class IndustryTypeApiView(APIView):
    permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            serializer = IndustryTypesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Industry type registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

    def get(self, request):
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = end - int(count_per_page)
        
        id = request.GET.get('id', None)
        
        query = request.GET.get('query', None)
        
        if id:
            queryset = IndustryTypes.objects.filter(id=id).last()
            serializer=IndustryTypesSerializer(queryset)
            return JsonResponse({'message':'Product Type', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if query:
            queryset = IndustryTypes.objects.filter(queue(industry_type__icontains=query)|queue(industry_type_description__icontains=query))[start:end]
            count = IndustryTypes.objects.filter(queue(industry_type__icontains=query)|queue(industry_type_description__icontains=query)).count()
        else:
            queryset = IndustryTypes.objects.all()[start:end]
            count = IndustryTypes.objects.count()
        serializer = IndustryTypesSerializer(queryset, many=True)
        return JsonResponse({'message':'Industry list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
    
    @authorize('register_types')
    def put(self, request):
        industry_type_id=request.data.get("id")
        industry_type_info = IndustryTypes.objects.filter(id=industry_type_id).last()
        if industry_type_info:
            serializer = IndustryTypesSerializer(industry_type_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Industry type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('register_types')
    def delete(self, request):
        industry_type_id=request.data.get("id")
        industry_type_info = IndustryTypes.objects.filter(id=industry_type_id)
        if industry_type_info:
            industry_type_info.delete()
            return JsonResponse({'message':'Industry type deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
