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

class ClusterApiView(APIView):
    @authorize('register_cluster')
    def post(self, request):
        if request.data and request.data.get('brand'):
            
            serializer = ClusterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                brand_cluster = BrandClusterMappingSerializer(data={
                    'brand' : request.data.get('brand')[0],
                    'cluster' : serializer.data['id']
                })

                if brand_cluster.is_valid():
                    brand_cluster.save()
                else:
                    Clusters.objects.filter(id=serializer.data['id']).delete()
                    return JsonResponse({'message':'Error during cluster registration.', 'status':False, 'status_code':400, 'error':brand_cluster.errors}, status=400)
            serializer = ClusterSerializer(Clusters.objects.filter(id=serializer.data['id']).last())
            return JsonResponse({'message':'Cluster Create Successfully', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
        return JsonResponse({'message':'Invalid request. Brand not selected.', 'status':False, 'status_code':400}, status=400)


    def get(self, request):
        brand = request.GET.get('brand', None)
        company = request.GET.get('company', None)
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
        
        if brand:
            if query:
                brand_clusters = BrandClusterMapping.objects.filter(brand=brand).distinct().values_list('cluster', flat=True)
                print(brand_clusters)
                cluster = Clusters.objects.filter(id__in=brand_clusters).filter(queue(cluster_code__icontains=query)|queue(cluster_name__icontains=query)).all()[start:end]
                print(cluster)
                count = Clusters.objects.filter(id__in=brand_clusters).filter(queue(cluster_code__icontains=query)|queue(cluster_name__icontains=query)).count()
            else:
                brand_clusters = BrandClusterMapping.objects.filter(brand=brand).distinct().values_list('cluster', flat=True)
                cluster = Clusters.objects.filter(id__in=brand_clusters).all()[start:end]
                count = Clusters.objects.filter(id__in=brand_clusters).count()
                
            serializer = ClusterSerializer(cluster, many=True)
            return JsonResponse({'message':'Clusters list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        if company:
            if query:
                company_cluster = CompanyCluserMapping.objects.filter(company=company).distinct().values_list('cluster', flat=True)
                cluster = Clusters.objects.filter(id__in=company_cluster).filter(queue(cluster_code__icontains=query)|queue(cluster_name__icontains=query)).all()[start:end]
                count = Clusters.objects.filter(id__in=company_cluster).filter(queue(cluster_code__icontains=query)|queue(cluster_name__icontains=query)).count()
            else:
                company_cluster = CompanyCluserMapping.objects.filter(company=company).distinct().values_list('cluster', flat=True)
                cluster = Clusters.objects.filter(id__in=company_cluster).all()[start:end]
                count = Clusters.objects.filter(id__in=company_cluster).count()
                
            serializer = ClusterSerializer(cluster, many=True)
            return JsonResponse({'message':'Clusters list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        if id:
            cluster = Clusters.objects.filter(id=id).last()
            serializer = ClusterSerializer(cluster)
            return JsonResponse({'message':'Clusters list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)

        return JsonResponse({'message':'Invalid request. Brand ID or Company ID or Cluster ID Required.', 'status':False, 'status_code':200}, status=200)
    
    @authorize('update_cluster')
    def put(self, request):
        brand = request.data.get('brand', None)
        companies = request.data.get('company', None)

        errors = []

        if request.data:
            if request.data.get('id', None):
                cluster = Clusters.objects.filter(id=request.data.get('id', None)).last()
                serializer = ClusterSerializer(cluster, data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    if brand:
                        try:
                            for brand_id in brand:
                                brand_cluster = BrandClusterMappingSerializer(data={
                                    'brand' : brand_id,
                                    'cluster' : serializer.data['id']
                                })

                                if brand_cluster.is_valid():
                                    brand_cluster.save()
                                else:
                                    print(brand_cluster.errors)
                                    errors.append(brand_cluster.errors)
                        except(Exception)as e:
                            logger.error(e)
                    
                    if companies:
                        try:
                            for company in companies:
                                company_cluster = CompanyCluserMapping(data={
                                    'company' : company,
                                    'cluster' : serializer.data['id']
                                })

                                if company_cluster.is_valid():
                                    company_cluster.save()
                                else:
                                    errors.append(company_cluster.errors)
                        except(Exception)as e:
                            logger.error(e)
                    
                    return JsonResponse({'message':'Cluster Updated Successfully.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                else:
                    return JsonResponse({'message':'Error during updating Cluster.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Cluster ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_cluster')
    def delete(self, request):
        if request.data.get('id', None):
            Clusters.objects.filter(id=request.data.get('id')).delete()
            return JsonResponse({'message':'Cluster deleted successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'Invalid request, Cluster ID required.', 'status':False, 'status_code':400}, status=400)
    


# ClusterAddress

from django.db.models import Q as queue
class ClusterAddressApiView(APIView):
    @authorize('register_cluster_address')
    def post(self, request):
        if request.data:
            serializer = ClusterAddressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Cluster Address saved successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering cluster address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_cluster_address')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                add = ClusterAddress.objects.filter(id=id).last()
                if add:        
                    serializer = ClusterAddressSerializer(add, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Cluster Address saved successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating cluster address.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid ID could not find record.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    @authorize('update_cluster_address')
    def delete(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                ClusterAddress.objects.filter(id=id).delete()
                return JsonResponse({'message':'Cluster Address deleted successfully.', 'status':True, 'status_code':200}, status=200)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    def get(self, request):
        cluster = request.GET.get('cluster')
        id = request.GET.get('id')
        address_type = request.GET.get('address_type')
        brand = request.GET.get('brand')
        query = request.GET.get('query', None)
        
        if brand:
            cluster_ids = BrandClusterMapping.objects.filter(brand=brand).distinct().values_list('cluster', flat=True)
            if query:
                if address_type:
                    add = ClusterAddress.objects.filter(cluster__in=cluster_ids).filter(short_name__icontains=query).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = ClusterAddress.objects.filter(short_name__icontains=query).filter(cluster__in=cluster_ids).all()
            else:
                if address_type:
                    add = ClusterAddress.objects.filter(cluster__in=cluster_ids).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = ClusterAddress.objects.filter(cluster__in=cluster_ids).all()
            
            serializer = ClusterAddressSerializer(add, many=True)
            return JsonResponse({'message':'Brand Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            
        if cluster:
            if query:
                if address_type:
                    add = ClusterAddress.objects.filter(cluster=cluster).filter(short_name__icontains=query).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = ClusterAddress.objects.filter(cluster=cluster).filter(short_name__icontains=query).all()
            else:
                if address_type:
                    add = ClusterAddress.objects.filter(cluster=cluster).filter(queue(address_type=address_type) | queue(use_for_all=True)).all()
                else:
                    add = ClusterAddress.objects.filter(cluster=cluster).all()
            serializer = ClusterAddressSerializer(add, many=True)
            return JsonResponse({'message':'Cluster Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if id:
            add = ClusterAddress.objects.filter(id=id).last()
            serializer = ClusterAddressSerializer(add)
            return JsonResponse({'message':'Cluster Address.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'ID of Cluster ID required.', 'status':False, 'status_code':400}, status=400)


    
class ClusterPosMappingApiView(APIView):
    def get(self, request):
        brand = request.GET.get('brand')
        cluster = request.GET.get('cluster')
        pos = request.GET.get('pos')
        
        if brand:
            cluster_ids = BrandClusterMapping.objects.filter(brand=brand).all().distinct().values_list('cluster__id')
            pos = POS.objects.filter(cluster__in=cluster_ids).all()
            serializer = ClusterPosMappingSerializer(pos, many=True)
            return JsonResponse({'message':'Cluster and POS mapping.', 'status':True, 'status_code':'200', 'result':serializer.data}, status=200)
        
        if cluster:
            pos = POS.objects.filter(cluster=cluster).all()
            serializer = ClusterPosMappingSerializer(pos, many=True)
            return JsonResponse({'message':'Cluster and POS mapping.', 'status':True, 'status_code':'200', 'result':serializer.data}, status=200)
        
        if pos:
            pos = POS.objects.filter(id=pos).last()
            serializer = ClusterPosMappingSerializer(pos)
            return JsonResponse({'message':'Cluster and POS mapping.', 'status':True, 'status_code':'200', 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)