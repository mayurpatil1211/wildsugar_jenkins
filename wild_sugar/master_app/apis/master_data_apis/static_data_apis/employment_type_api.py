
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class EmploymentTypeApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            serializer = EmploymentTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Employment registered successfully', 'status_code':201}, status=201)
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
            queryset = EmploymentTypes.objects.filter(id=id).last()
            serializer=EmploymentTypeSerializer(queryset)
            return JsonResponse({'message':'Employment Type', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if query:
            queryset = EmploymentTypes.objects.filter(queue(employment_type__icontains=query)|queue(employment_type_description__icontains=query))[start:end]
            count = EmploymentTypes.objects.filter(queue(employment_type__icontains=query)|queue(employment_type_description__icontains=query)).count()
        else:
            queryset = EmploymentTypes.objects.all()[start:end]
            count = EmploymentTypes.objects.count()
        serializer = EmploymentTypeSerializer(queryset, many=True)
        return JsonResponse({'message':'Employment list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
    
    @authorize('register_types')
    def put(self, request):
        employment_id=request.data.get("id")
        employment_info = EmploymentTypes.objects.filter(id=employment_id).last()
        if employment_info:
            serializer = EmploymentTypeSerializer(employment_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Employment type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('register_types')
    def delete(self, request):
        employment_id=request.data.get("id")
        employment_info = EmploymentTypes.objects.filter(id=employment_id)
        if employment_info:
            employment_info.delete()
            return JsonResponse({'message':'Employment type deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
