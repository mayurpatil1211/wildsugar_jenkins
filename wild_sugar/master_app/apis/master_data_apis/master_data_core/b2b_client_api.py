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

class B2bClientApiView(APIView):
    def save_bank_details(self, data, client):
        bank_details = data.get('bank_details')
        if bank_details:
            bank_details['client'] = client

            serializer = B2BclientBankDetailsSerializer(data=bank_details)
            if serializer.is_valid():
                serializer.save()
                return True, {}
            return False, serializer.errors
        return True, {}
    
    @authorize('register_b2b_client')
    def post(self, request):
        errors = []
        if request.data:
            pos = request.data.get('pos', [])
            cluster = request.data.get('cluster', [])
            brand = request.data.get('brand', [])
            
            if pos or brand or cluster:
                serializer = B2bClientSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    
                    if pos:
                        status, error = self.client_pos_mapping(pos, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            BtoBclient.objects.filter(id=serializer.data.get('id')).delete()
                            return JsonResponse({'message':'Error during mapping POS to B2B client.', 'status':False, 'status_code':400, 'error':errors}, status=400)
                    
                    if cluster:
                        status, error = self.client_cluster_mapping(cluster, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            BtoBclient.objects.filter(id=serializer.data.get('id')).delete()
                            return JsonResponse({'message':'Error during mapping Cluster to B2B client.', 'status':False, 'status_code':400, 'error':errors}, status=400)
                    
                    
                    if brand:
                        status, error = self.client_brand_mapping(brand, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            BtoBclient.objects.filter(id=serializer.data.get('id')).delete()
                            return JsonResponse({'message':'Error during mapping Brand to B2B client.', 'status':False, 'status_code':400, 'error':errors}, status=400)
                            
                    
                    status, error = self.save_bank_details(request.data, serializer.data['id'])
                    errors.extend(error)
                    serializer = B2bClientSerializer(BtoBclient.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'B2B client registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':errors}, status=201)
                return JsonResponse({'message':'Error during B2B client registration.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'POS or Brand or Cluster has to be linked.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    def client_cluster_mapping(self, cluster, client_id):
        errors = []
        for i in cluster:
            if not B2BclientClusterMapping.objects.filter(cluster=i, client=client_id).last():
                serializer = B2BclientClusterMappingSerializer(data={
                    'cluster':i,
                    'client':client_id
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
                    return False, errors 
        
        return True, errors
    
    def client_brand_mapping(self, brand, client_id):
        errors = []
        for i in brand:
            if not B2BclientBrandMapping.objects.filter(brand=i, client=client_id).last():
                serializer = B2BclientBrandMappingSerializer(data={
                    'brand':i,
                    'client':client_id
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
                    return False, errors 
        
        return True, errors 
    
    def client_pos_mapping(self, pos, client_id):
        errors = []
        for i in pos:
            if not B2BclientPOSMapping.objects.filter(pos=i, client=client_id).last():
                serializer = B2BclientPOSMappingSerializer(data={
                    'pos':i,
                    'client':client_id
                })
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
                    return False, errors 
        
        return True, errors 
    
    @authorize('update_b2b_client')
    def put(self, request):
        errors = []
        if request.data:
            pos = request.data.get('pos', [])
            cluster = request.data.get('cluster', [])
            brand = request.data.get('brand', [])
            id = request.data.get('id', [])
            
            client = BtoBclient.objects.filter(id=id).last()
            
            if client:
                serializer = B2bClientSerializer(client, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    
                    if pos:
                        status, error = self.client_pos_mapping(pos, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            
                    if cluster:
                        status, error = self.client_cluster_mapping(cluster, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            
                    
                    if brand:
                        status, error = self.client_brand_mapping(brand, serializer.data.get('id'))
                        if not status:
                            errors.extend(error)
                            
                    
                    status, error = self.save_bank_details(request.data, serializer.data['id'])
                    errors.extend(error)
                    return JsonResponse({'message':'B2B client updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                return JsonResponse({'message':'Error during B2B client update.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid B2B Client.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('list_b2b_client')
    def get(self, request):
        cluster = request.GET.get('cluster', None)
        brand = request.GET.get('brand', None)
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
        
        if cluster:
            if query:
                client_ids = B2BclientClusterMapping.objects.filter(cluster=cluster).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query))[start:end]
                count = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)).count()
            else:
                client_ids = B2BclientClusterMapping.objects.filter(cluster=cluster).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).all()[start:end]
                count = BtoBclient.objects.filter(id__in=client_ids).count()
            serializer = B2BClientReadSerializer(client, many=True)
            return JsonResponse({'message':'B2B Client List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        if brand:
            if query:
                client_ids = B2BclientBrandMapping.objects.filter(brand=brand).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query))[start:end]
                print(client)
                count = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)).count()
            else:
                client_ids = B2BclientBrandMapping.objects.filter(brand=brand).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).all()[start:end]
                count = BtoBclient.objects.filter(id__in=client_ids).count()
            serializer = B2BClientReadSerializer(client, many=True)
            return JsonResponse({'message':'B2B Client List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        if pos:
            if query:
                client_ids = B2BclientPOSMapping.objects.filter(pos=pos).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query))[start:end]
                count = BtoBclient.objects.filter(id__in=client_ids).filter(queue(client_code__icontains=query)|queue(client_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)).count()
            else:
                client_ids = B2BclientPOSMapping.objects.filter(pos=pos).all().distinct().values_list('client', flat=True)
                client = BtoBclient.objects.filter(id__in=client_ids).all()[start:end]
                count = BtoBclient.objects.filter(id__in=client_ids).count()
            serializer = B2BClientReadSerializer(client, many=True)
            return JsonResponse({'message':'B2B Client List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        return JsonResponse({'message':'Cluster, Brand or POS ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_b2b_client')
    def delete(self, request):
        id = request.data.get('id', None)
        if id:
            BtoBclient.objects.filter(id=id).delete()
            return JsonResponse({'message':'B2B client deleted successfully.', 'status':True, 'status_code':200}, status=200)