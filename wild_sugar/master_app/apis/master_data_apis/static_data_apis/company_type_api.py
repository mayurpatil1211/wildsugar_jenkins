from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

# class CompanyTypeApiView(APIView):
#     # permission_classes = (AllowAny,)
#     @authorize('register_types')
#     def post(self, request):
#         if request.data:
#             serializer = CompanyTypesSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse({'result':serializer.data, 'status':True, 'message':'Company type registered successfully', 'status_code':201}, status=201)
#             return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
#         return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

#     def get(self, request):
#         id = request.GET.get('id', None)
#         queryset = CompanyTypes.objects.all()
#         serializer = CompanyTypesSerializer(queryset, many=True)
        
#         if id:
#             queryset = CompanyTypes.objects.filter(id=id).last()
#             serializer=CompanyTypesSerializer(queryset)
#             return JsonResponse({'message':'Company Type list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
#         return JsonResponse({'message':'Company Type list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
    
#     @authorize('register_types')
#     def put(self, request):
#         company_id=request.data.get("id")
#         company_info = CompanyTypes.objects.filter(id=company_id).last()
#         if company_info:
#             serializer = CompanyTypesSerializer(company_info,data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse({'message':'Company type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
#             return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
#         return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    
#     @authorize('register_types')
#     def delete(self, request):
#         company_id=request.data.get("id")
#         company_info = CompanyTypes.objects.filter(id=company_id)
#         if company_info:
#             company_info.delete()
#             return JsonResponse({'message':'Company type deleted', 'status':True, 'status_code':200 }, status=200)
#         return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

class CompanyTypeApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            serializer = CompanyTypesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Company type registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

    def get(self, request):
        
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
            queryset = CompanyTypes.objects.filter(id=id).last()
            serializer=CompanyTypesSerializer(queryset)
            return JsonResponse({'message':'Company Type list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)

        if query:
            queryset = CompanyTypes.objects.filter(queue(company_type__icontains=query) | queue(company_type_description__icontains=query))[start:end]
            count = CompanyTypes.objects.filter(queue(company_type__icontains=query) | queue(company_type_description__icontains=query)).count()
        else:
            queryset = CompanyTypes.objects.all()[start:end]
            count = CompanyTypes.objects.count()
        
        serializer = CompanyTypesSerializer(queryset, many=True)
        return JsonResponse({'message':'Company Type list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
    
    
    @authorize('register_types')
    def put(self, request):
        company_id=request.data.get("id")
        company_info = CompanyTypes.objects.filter(id=company_id).last()
        if company_info:
            serializer = CompanyTypesSerializer(company_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Company type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    
    @authorize('register_types')
    def delete(self, request):
        company_id=request.data.get("id")
        company_info = CompanyTypes.objects.filter(id=company_id)
        if company_info:
            company_info.delete()
            return JsonResponse({'message':'Company type deleted', 'status':True, 'status_code':200 }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)