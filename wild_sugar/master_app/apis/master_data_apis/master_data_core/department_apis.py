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


class DepartmentApiView(APIView):
    @authorize('register_department')
    def post(self, request):
        cluster = request.data.get('cluster', None)
        brand = request.data.get('brand', None)
        department_cluster_food_cost = request.data.get('department_cluster_food_cost', None)
        sub_departments = request.data.get('sub_departments')
        errors = []
        if brand:
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                

                # dept_serializer = DepartmentClusterMappingSerializer(data={
                #     "department" : serializer.data['id'],
                #     "cluster" : cluster,
                #     "food_cost":department_cluster_food_cost
                # })
                
                # dept_serializer = DepartmentBrandMappingSerializer(data={
                #     "department" : serializer.data['id'],
                #     "brand" : brand,
                #     "food_cost":department_cluster_food_cost
                # })

                # if dept_serializer.is_valid():
                #     dept_serializer.save()
                for sub_dept in sub_departments:
                    sub_dept['parent_department'] = serializer.data['id']
                    sub_serializer = SubDepartmentSerializer(data=sub_dept)
                    if sub_serializer.is_valid():
                        sub_serializer.save()
                    else:
                        errors.append(sub_serializer.errors)
                        
                serializer = DepartmentReadSerializer(Department.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Department Registered Successfully', 'status':True, 'status_code':201, 'result':serializer.data, 'error':errors}, status=201)
                # Department.objects.filter(id=serializer.data['id']).delete()
                # return JsonResponse({'message':'Error during registering department, Please check details you are sending.', 'status':False, 'status_code':400, 'error':dept_serializer.errors}, status=400)
            return JsonResponse({'message':'Error during registering department, Please check details you are sending.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Brand ID.', 'status':False, 'status_code':400}, status=400)


    def get(self, request):
        id = request.GET.get('id')
        dept_uid = request.GET.get('uid')
        cluster = request.GET.get('cluster')
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
            dept = Department.objects.filter(id=id).last()
            print('koooooooooo')
            serializer = DepartmentReadSerializer(dept)
            return JsonResponse({'message':'Department Information.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if dept_uid:
            dept = Department.objects.filter(department_uid=dept_uid).last()
            serializer = DepartmentReadSerializer(dept)
            return JsonResponse({'message':'Department Information.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if cluster:
            dept_cluster = DepartmentClusterMapping.objects.filter(cluster=cluster).all().distinct().values_list('department', flat=True)
            dept = Department.objects.filter(id__in=dept_cluster).filter(queue(department_uid__icontains=query)| queue(department_name__icontains=query)| queue(department_type__icontains=query)).all()[start:end]
            count = Department.objects.filter(id__in=dept_cluster).filter(queue(department_uid__icontains=query)| queue(department_name__icontains=query)| queue(department_type__icontains=query)).count()
            serializer = DepartmentSerializer(dept, many=True)
            return JsonResponse({'message':'Department List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        if brand:
            dept = Department.objects.filter(brand=brand).all()[start:end]
            count = Department.objects.filter(brand=brand).count()
            serializer = DepartmentSerializer(dept, many=True)
            return JsonResponse({'message':'Department List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':200}, status=200)


    @authorize('update_department')
    def put(self, request):
        id = request.data.get('id', None)
        sub_departments = request.data.get('sub_departments')
        errors = []
        if id:
            dept = Department.objects.filter(id=id).last()
            serializer = DepartmentSerializer(dept, data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                for sub_dept in sub_departments:
                    sub_d = SubDepartment.objects.filter(id=sub_dept.get('id')).last()
                    if sub_d:
                        sub_serializer = SubDepartmentSerializer(sub_d, data=sub_dept)
                        if sub_serializer.is_valid():
                            sub_serializer.save()
                        else:
                            errors.append(sub_serializer.errors)
                
                serializer = DepartmentReadSerializer(Department.objects.filter(id=serializer.data['id']).last())
                
                return JsonResponse({'message':'Department updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'message':'Error during updating Department.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request. Department ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('delete_department')
    def delete(self, request):
        id = request.data.get('id', None)
        if id:
            Department.objects.filter(id=id).delete()
            return JsonResponse({'message':'Department Deleted Successfully.', 'status':False, 'status_code':200}, status=200)
        return JsonResponse({'message':'Invalid request. Department ID required.', 'status':False, 'status_code':400}, status=400)
    
    
class SubDepartmentApiView(APIView):
    @authorize('register_department')
    def post(self, request):
        if request.data:
            serializer = SubDepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializer = SubDepartmentSerializer(SubDepartment.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Sub Department registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering sub department.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        department = request.GET.get('department')
        id = request.GET.get('id')
        
        if department:
            sub_department = SubDepartment.objects.filter(parent_department=department).all()
            serializer = SubDepartmentSerializer(sub_department, many=True)
            return JsonResponse({'message':'Sub Department list by department.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if id:
            sub_department = SubDepartment.objects.filter(id=id).last()
            serializer = SubDepartmentReadSerializer(sub_department)
            return JsonResponse({'message':'Sub Department Details.', 'status':False, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'Department ID or Sub Department ID required.', 'status':False, 'status_code':200}, status=400)
    
    def put(self, request):
        id = request.data.get('id')
        
        if id:
            sub_department = SubDepartment.objects.filter(id=id).last()
            if sub_department:
                serializer = SubDepartmentSerializer(sub_department, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Sub Department Updated Successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating sub department.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid sub department.', 'status':False, 'status_code':404}, status=404)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            sub_department = SubDepartment.objects.filter(id=id).delete()
            return JsonResponse({'message':'Sub Department Deleted Successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)