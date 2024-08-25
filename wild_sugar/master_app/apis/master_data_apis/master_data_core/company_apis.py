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

class CompanyApiView(APIView):
    # @authorize('register_company')
    def get(self, request):
        shareholder = request.GET.get('shareholder', None)
        cluster = request.GET.get('cluster', None)
        brand = request.GET.get('brand', None)
        id = request.GET.get('id', None)
        pos = request.GET.get('pos', None)
        
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

        if shareholder:
            if query:
                
                company_shareholder = CompanyShareholder.objects.filter(user=shareholder).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).count()
            else:
                company_shareholder = CompanyShareholder.objects.filter(user=shareholder).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).count()
                
            serializer = CompanyInfoSerializer(companies, many=True)
            return JsonResponse({'message':'Company Info.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            companies = Company.objects.filter(id=id).last()
            serializer = CompanyInfoSerializer(companies)
            return JsonResponse({'message':'Company Info.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)

        if cluster:
            if query:
                company_shareholder = CompanyCluserMapping.objects.filter(cluster=cluster).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).count()
            else:
                company_shareholder = CompanyCluserMapping.objects.filter(cluster=cluster).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).count()
            serializer = CompanyInfoSerializer(companies, many=True)
            return JsonResponse({'message':'Company Info.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        
        if brand:
            if query:
                company_shareholder = CompanyBrandMapping.objects.filter(brand=brand).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).count()
            else:
                company_shareholder = CompanyBrandMapping.objects.filter(brand=brand).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_shareholder).all()[start:end]
                count = Company.objects.filter(id__in=company_shareholder).count()
            serializer = CompanyInfoSerializer(companies, many=True)
            return JsonResponse({'message':'Company Info.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if pos:
            if query:
                company_pos = PosCompanyMapping.objects.filter(pos=pos).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_pos).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query))[start:end]
                count = Company.objects.filter(id__in=company_pos).filter(queue(company_name__icontains=query) | queue(company_type__icontains=query) | queue(gstn__icontains=query) | queue(pan__icontains=query) | queue(purchase_email__icontains=query) | queue(purchase_contact_number__icontains=query) | queue(accounts_email__icontains=query) | queue(accounts_contact_number__icontains=query)).count()
            else:
                company_pos = PosCompanyMapping.objects.filter(pos=pos).all().distinct().values_list('company', flat=True)
                companies = Company.objects.filter(id__in=company_pos).all()[start:end]
                count = Company.objects.filter(id__in=company_pos).count()
            serializer = CompanyInfoSerializer(companies, many=True)
            return JsonResponse({'message':'Company Info.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        return JsonResponse({'message':'Bad Request. Shareholder ID, Company ID or Cluster ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('register_company')
    def post(self, request):
        errors = []
        cluster = request.data.get('cluster')
        brand = request.data.get('brand')
        shareholder = request.data.get('shareholder')
        pos = request.data.get('pos')
        
        if request.data:
            if brand and (pos or shareholder):
                serializer = CompanySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    
                    # if cluster:
                    #     status, error = self.map_cluster(cluster, serializer.data['id'])
                    #     errors.extend(error)
                    
                    if brand:
                        status, error = self.map_brand(brand, serializer.data['id'])
                        errors.extend(error)
                        

                    
                    if shareholder:
                        status, error = self.save_shareholder(shareholder, serializer.data['id'])
                        errors.extend(error)
                    
                    
                    if pos:
                        status, error = self.save_pos(pos, serializer.data['id'])
                        errors.extend(error)
                        
                    serializer = CompanyInfoSerializer(Company.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Company Registered Successfully.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':errors}, status=201)

                
                return JsonResponse({'message':'Error during registering company.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)         
            return JsonResponse({'message':'Cannot register company, please provide Cluster ID or Shareholder or POS ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    def map_brand(self, brand, company_id):
        errors = []
        company_brand = CompanyBrandMappingSerializer(data={
                'brand' : brand,
                'company' : company_id
            })
        
        if company_brand.is_valid():
            company_brand.save()
        else:
            errors.append(company_brand.errors)
        return True, errors
    
    
    def map_cluster(self, cluster, company_id):
        errors = []
        company_cluster = CompanyCluserMappingSerializer(data={
                'cluster' : cluster,
                'company' : company_id
            })
        
        if company_cluster.is_valid():
            company_cluster.save()
        else:
            errors.append(company_cluster.errors)
        return True, errors
        

    def save_pos(self, pos, company_id):
        errors = []
        for po in pos:
            serializer = PosCompanyMappingSerializer(data={
                "pos" : po,
                "company" :company_id
            })
            
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
        return True, errors
    
    def save_shareholder(self, shareholders, company_id):
        errors = []
        for shareholder in shareholders:
            shareholder['user_type'] = 'shareholder'
            shareholder['username'] = shareholder.get('email')
            is_exists = User.objects.filter(email=shareholder.get('email')).last()
            if not is_exists:
                try:
                    serializer = ShareholderUserSerializer(data=shareholder)
                    if serializer.is_valid():
                        serializer.save()
                        
                        company_shareholder = CompanyShareholderCreateSerializer(data={
                            'company' : company_id,
                            'user' : serializer.data['id']
                        })

                        if company_shareholder.is_valid():
                            company_shareholder.save()
                        else:
                            errors.append({'data':shareholder,'error':company_shareholder.errors})
                    else:
                        errors.append({'data':shareholder,'error':serializer.errors})
                except(Exception) as e:
                    logger.error(e)
            else:
                
                company_shareholder = CompanyShareholderCreateSerializer(data={
                    'company' : company_id,
                    'user' : is_exists.id
                })

                if company_shareholder.is_valid():
                    company_shareholder.save()
                else:
                    errors.append({'data':shareholder,'error':company_shareholder.errors})
        
        if errors:
            return False, errors
        return True, errors

    @authorize('update_company')
    def put(self, request):
        errors = []
        company_id = request.data.get('id', None)
        shareholder = request.data.get('shareholder')
        cluster = request.data.get('cluster')
        pos = request.data.get('pos')

        if company_id:
            company = Company.objects.filter(id=company_id).last()
        
            if company:
                serializer = CompanySerializer(company, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    
                    # if cluster:
                    #     status, error = self.map_cluster(cluster, serializer.data['id'])
                    #     errors.extend(error)
                        

                    
                    if shareholder:
                        status, error = self.save_shareholder(shareholder, serializer.data['id'])
                        errors.extend(error)
                    
                    
                    if pos:
                        status, error = self.save_pos(pos, serializer.data['id'])
                        errors.extend(error)

                    # status, errors = self.save_shareholder(shareholder, serializer.data['id'])
                    # if status:
                    #     serializer = CompanyInfoSerializer(Company.objects.filter(id=serializer.data['id']).last())
                    #     return JsonResponse({'message':'Comapny registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
                    # else:
                    #     serializer = CompanyInfoSerializer(Company.objects.filter(id=serializer.data['id']).last())
                    #     return JsonResponse({'message':'Comapny registered successfully. Error during registering shareholder.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':errors}, status=201)
                    serializer = CompanyInfoSerializer(Company.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Comapny registered successfully. Error during registering shareholder.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                return JsonResponse({'message':'Error during registering company.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)         
            return JsonResponse({'message':'Invalid Company Selected.', 'status':False, 'status_code':False}, status=200)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)

    @authorize('delete_company')
    def delete(self, request):
        company_id = request.data.get('id')
        if company_id:
            Company.objects.filter(id=company_id).delete()
            return JsonResponse({'message':'Company Deleted Successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'COmpany ID required.', 'status':False, 'status_code':400}, status=400)
    



# CompanyAddress

class CompanyAddressApiView(APIView):
    @authorize('register_company_address')
    def post(self, request):
        if request.data:
            serializer = CompanyAddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Company Address saved successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering company address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_company_address')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                add = CompanyAddress.objects.filter(id=id).last()
                if add:        
                    serializer = CompanyAddressSerializer(add, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Company Address saved successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating company address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid ID could not find record.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    @authorize('update_company_address')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                CompanyAddress.objects.filter(id=id).delete()
                return JsonResponse({'message':'Company Address deleted successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        company = request.GET.get('company')
        address_type = request.GET.get('address_type')
        id = request.GET.get('id')
        if company:
            if address_type:
                add = CompanyAddress.objects.filter(company=company, address_type=address_type).all()
            else:
                add = CompanyAddress.objects.filter(company=company).all()
            serializer = CompanyAddressReadSerializer(add, many=True)
            return JsonResponse({'message':'Company Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if id:
            add = CompanyAddress.objects.filter(id=id).last()
            serializer = CompanyAddressReadSerializer(add)
            return JsonResponse({'message':'Company Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'ID of Company ID required.', 'status':False, 'status_code':400}, status=400)