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


class POSApiView(APIView):
    @authorize('register_pos')
    def post(self, request):
        errors = []
        if request.data:
            serializer = PosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                department = request.data.get('departments')
                companies = request.data.get('companies')
                
                if department:
                    status, error = self.save_departments(serializer.data['id'], department)
                    errors.extend(error)
                
                if companies:
                    status, error = self.save_companies(serializer.data['id'], companies)
                    errors.extend(error)
                
                serializer = PosSerializer(POS.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'POS registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':errors}, status=201)
            return JsonResponse({'message':'Error during registering POS.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    
    def save_departments(self, pos_id, departments):
        errors = []
        for dept in departments: 
            serializer = PosDepartmentMappingSerializer(data={
                "department":dept,
                "pos":pos_id
            })
            
            if serializer.is_valid():
                serializer.save()
            else:
                # print(serializer.errors)
                errors.append(serializer.errors)
        return True, errors

    
    def save_companies(self, pos_id, companies):
        errors = []
        for company in companies:
            serializer = PosCompanyMappingSerializer(data={
                "pos" : pos_id,
                "company" :company
            })
            
            if serializer.is_valid():
                serializer.save()
            else:
                # print(serializer.errors)
                errors.append(serializer.errors)
        return True, errors
            
    
    def get(self, request):
        cluster = request.GET.get('cluster', None)
        id = request.GET.get('id', None)
        company = request.GET.get('company', None)
        
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
        
        if cluster:
            if query:
                pos = POS.objects.filter(cluster=cluster).filter(queue(pos_code__icontains=query) | queue(pos_name__icontains=query) | queue(pos_type__icontains=query) | queue(contact_number__icontains=query) | queue(email__icontains=query)).all()[start:end]
                count = POS.objects.filter(cluster=cluster).filter(queue(pos_code__icontains=query) | queue(pos_name__icontains=query) | queue(pos_type__icontains=query) | queue(contact_number__icontains=query) | queue(email__icontains=query)).count()
            else:
                pos = POS.objects.filter(cluster=cluster).all()[start:end]
                count = POS.objects.filter(cluster=cluster).count()
            serializer = PosSerializer(pos, many=True)
            return JsonResponse({'message':'POS for the requested cluster.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            pos = POS.objects.filter(id=id).last()
            serializer = PosDetailSerializer(pos)
            return JsonResponse({'message':'POS details.', 'status':True, 'status_code':200, 'result':serializer.data},status=200)
        
        if company:
            if query:
                pos_company = PosCompanyMapping.objects.filter(company=company).all().distinct().values_list('pos', flat=True)
                pos = POS.objects.filter(id__in=pos_company).filter(queue(pos_code__icontains=query) | queue(pos_name__icontains=query) | queue(pos_type__icontains=query) | queue(contact_number__icontains=query) | queue(email__icontains=query))[start:end]
                count = POS.objects.filter(id__in=pos_company).filter(queue(pos_code__icontains=query) | queue(pos_name__icontains=query) | queue(pos_type__icontains=query) | queue(contact_number__icontains=query) | queue(email__icontains=query)).count()
            else:
                pos_company = PosCompanyMapping.objects.filter(company=company).all().distinct().values_list('pos', flat=True)
                pos = POS.objects.filter(id__in=pos_company).all()[start:end]
                count = POS.objects.filter(id__in=pos_company).count()
            serializer = PosSerializer(pos, many=True)
            return JsonResponse({'message':'POS for the requested company.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Cluster or POS ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_pos')
    def put(self, request):
        id = request.data.get('id', None)
        errors = []
        
        if id:
            pos = POS.objects.filter(id=id).last()
            if pos:
                serializer = PosSerializer(pos, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    
                    department = request.data.get('departments')
                    companies = request.data.get('companies')
                    
                    if department:
                        status, error = self.save_departments(serializer.data['id'], department)
                        errors.extend(error)
                    
                    if companies:
                        status, error = self.save_companies(serializer.data['id'], companies)
                        errors.extend(error)
                    
                    serializer = PosDetailSerializer(pos)
                    return JsonResponse({'message':'POS updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                else:
                    return JsonResponse({'message':'Error during updating POS.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid POS selected.', 'status':False, 'status_code':404}, status=404)
        return JsonResponse({'message':'POS ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_pos')
    def delete(self, request):
        id = request.data.get('id', None)
        POS.objects.filter(id=id).delete()
        return JsonResponse({'message':'POS deleted successfully.', 'status':True, 'status_code':200}, status=200)
    
class PosDepartmentMappingApi(APIView):
    def get(self, request):
        pos = request.GET.get('pos')
        if pos:
            dept = PosDepartmentMapping.objects.filter(pos=pos).all()
            serializer = PosDeprtmentMappingReadSerializer(dept, many=True)
            return JsonResponse({'message':'Pos Department Mapping.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'POS ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('map_pos_department')
    def post(self, request):
        pos = request.data.get('pos')
        departments = request.data.get('departments', [])
        errors = []
        if pos and departments:
            for dept in departments:
                if "id" in dept:
                    print(dept)
                    if not PosDepartmentMapping.objects.filter(pos=pos, department=dept.get('id')).last():
                        serializer = PosDepartmentMappingSerializer(data={
                            "department":dept.get('id'),
                            "pos":pos
                        })
                        
                        if serializer.is_valid():
                            serializer.save()
                            if dept.get('sub_departments'):
                                for sub_dept in dept.get('sub_departments'):
                                    if not PosSubdepartmentMapping.objects.filter(pos=pos, sub_department=sub_dept).last():
                                        subserializer = PosSubdepartmentMappingSerializer(data={
                                            'sub_department' : sub_dept,
                                            'pos':pos
                                        })
                                        if subserializer.is_valid():
                                            subserializer.save()
                                        else:
                                            errors.append(subserializer.errors)
                                
                        else:
                            # print(serializer.errors)
                            errors.append(serializer.errors)
                    else:
                        print(dept)
                        if dept.get('sub_departments'):
                            for sub_dept in dept.get('sub_departments'):
                                if not PosSubdepartmentMapping.objects.filter(pos=pos, sub_department=sub_dept).last():
                                    subserializer = PosSubdepartmentMappingSerializer(data={
                                        'sub_department' : sub_dept,
                                        'pos':pos
                                    })
                                    if subserializer.is_valid():
                                        subserializer.save()
                                    else:
                                        errors.append(subserializer.errors)
            return JsonResponse({'message':'Department Mapped to the POS.', 'status':True, 'status_code':200, 'error':errors}, status=200)
        return JsonResponse({'message':'POS and Departments required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('map_pos_department')
    def delete(self, request):
        departments = request.data.get('departments')
        sub_department = request.data.get('sub_departments')
        
        pos = request.data.get('pos')
        if pos:
            if departments:
                PosDepartmentMapping.objects.filter(pos = pos, department__id__in=departments).delete()
                
            if sub_department:
                PosSubdepartmentMapping.objects.filter(pos=pos, sub_department__id__in=sub_department).delete()
            return JsonResponse({'message':'Department and POS mapping removed.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'POS ID required.', 'status':False, 'status_code':400}, status=400)