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


class StoreApiView(APIView):
    @authorize('register_store')
    def post(self, request):
        errors = []
        if request.data:
            brand = request.data.get('brand')
            cluster = request.data.get('cluster')
            pos = request.data.get('pos')
            if brand or cluster or pos:
                serializer = StoreSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    
                    if brand:
                        brand_serializer = StoreBrandMappingSeriaizer(data={
                            'brand':brand,
                            'store':serializer.data['id']
                        })
                        if brand_serializer.is_valid():
                            brand_serializer.save()
                        else:
                            Store.objects.filter(id=serializer.data['id']).delete()
                            return JsonResponse({'message':'Error during mapping to brand.', 'status':False, 'status_code':400, 'error':brand_serializer.errors}, status=400)
                    
                    if cluster:
                        cluster_serializer = StoreClusterMappingSeriaizer(data={
                            'cluster':cluster,
                            'store':serializer.data['id']
                        })
                        if cluster_serializer.is_valid():
                            cluster_serializer.save()
                        else:
                            Store.objects.filter(id=serializer.data['id']).delete()
                            return JsonResponse({'message':'Error during mapping to cluster.', 'status':False, 'status_code':400, 'error':cluster_serializer.errors}, status=400)
                        
                    if pos:
                        pos_serializer = StorePosMappingSeriaizer(data={
                            'pos':pos,
                            'store':serializer.data['id']
                        })
                        if pos_serializer.is_valid():
                            pos_serializer.save()
                        else:
                            Store.objects.filter(id=serializer.data['id']).delete()
                            return JsonResponse({'message':'Error during mapping to pos.', 'status':False, 'status_code':400, 'error':pos_serializer.errors}, status=400)
                        
                    if request.data.get('employee'):
                        for employee in request.data.get('employee'):
                            emp_sers = StoreEmployeeSerializer(data={
                                'store':serializer.data.get('id'),
                                'user' : employee
                            })
                            if emp_sers.is_valid():
                                emp_sers.save()
                            else:
                                errors.append(emp_sers.errors)
                    
                    serializer = StoreSerializer(Store.objects.filter(id=serializer.data['id']).last())
                    return JsonResponse({'message':'Store registered successfully.', 'status':True, 'status_code':201, 'error':errors, 'result':serializer.data}, status=201)
                return JsonResponse({'message':'Error during registering store.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        brand = request.GET.get('brand', None)
        cluster = request.GET.get('cluster', None)
        pos = request.GET.get('pos', None)
        id = request.GET.get('id', None)
        
        page = request.GET.get('page',1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = end - int(count_per_page)
        
        if brand:
            brand_store = StoreBrandMapping.objects.filter(brand=brand).distinct().values_list('store', flat=True)
            count = len(brand_store)
            store = Store.objects.filter(id__in=brand_store).all().order_by('-id')[start:end]
            serializer = StoreSerializer(store, many=True)
            return JsonResponse({'message':'Store List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        elif cluster:
            brand_cluster = StoreClusterMapping.objects.filter(cluster=cluster).distinct().values_list('store', flat=True)
            count = len(brand_cluster)
            store = Store.objects.filter(id__in=brand_cluster).all().order_by('-id')[start:end]
            serializer = StoreSerializer(store, many=True)
            return JsonResponse({'message':'Store List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        elif pos:
            brand_pos = StorePosMapping.objects.filter(pos=pos).distinct().values_list('store', flat=True)
            count = len(brand_pos)
            store = Store.objects.filter(id__in=brand_pos).all().order_by('-id')[start:end]
            serializer = StoreSerializer(store, many=True)
            return JsonResponse({'message':'Store List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        elif id:
            store = Store.objects.filter(id=id).last()
            serializer = StoreDetailSerializer(store)
            return JsonResponse({'message':'Store List.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            
    
    def put(self, request):
        errors = []
        if request.data:
            id = request.data.get('id')
            
            if id:
                store = Store.objects.filter(id=id).last()
                if store:
                    
                    serializer = StoreSerializer(store,data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                    
                        if request.data.get('employee'):
                            for employee in request.data.get('employee'):
                                emp_sers = StoreEmployeeSerializer(data={
                                    'store':serializer.data.get('id'),
                                    'user' : employee
                                })
                                if emp_sers.is_valid():
                                    emp_sers.save()
                                else:
                                    errors.append(emp_sers.errors)
                        
                        if request.data.get('remove_employee'):
                            for employee in request.data.get('remove_employee'):
                                StoreEmployee.objects.filter(user=employee, store=serializer.data.get('id')).delete()
                                    
                        return JsonResponse({'message':'Store Updated successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
                    else:
                        return JsonResponse({'message':'Error during updating store.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            Store.objects.filter(id=id).delete()
        return JsonResponse({'message':'Store Deleted Successfully', 'status':True, 'status_code':200}, status=200)
    


class GetChildStores(APIView):
    def get(self, request):
        store = request.GET.get('store')
        
        mapp = []
        
        if store:
            brand_store = StoreBrandMapping.objects.filter(store=store).last()
            if brand_store:
                clusters = BrandClusterMapping.objects.filter(brand=brand_store.brand).all()
                for cluster in clusters:
                    cluster_stores = StoreClusterMapping.objects.filter(cluster=cluster.cluster.id).last()
                    if cluster_stores:
                        cluster_store_ser = StoreSerializer(cluster_stores.store).data
                        cluster_store_ser['level'] = 'cluster'
                        cluster_store_ser['cluster_code'] = cluster.cluster.cluster_code
                        cluster_store_ser['cluster_name'] = cluster.cluster.cluster_name
                        cluster_store_ser['pos_store'] = []
                        
                        poss = POS.objects.filter(cluster=cluster.cluster.id).all()
                        for pos in poss:
                            pos_stores = StorePosMapping.objects.filter(pos=pos.id).all()
                            for pos_store in pos_stores:
                                store_ser = StoreSerializer(pos_store.store).data
                                store_ser['level'] = 'pos'
                                store_ser['pos_code'] = pos.pos_code
                                store_ser['pos_name'] = pos.pos_name
                                store_ser['pos_type'] = pos.pos_type
                                cluster_store_ser['pos_store'].append(store_ser)
                        mapp.append(cluster_store_ser)
                return JsonResponse({'message':'Brand Child Stores.', 'status':True, 'status_code':200, 'result':mapp, 'current_level':'brand'}, status=200)
            
            cluster_store = StoreClusterMapping.objects.filter(store=store).last()
            if cluster_store:
                poss = POS.objects.filter(cluster=cluster_store.cluster.id).all()
                
                for pos in poss:
                    pos_stores = StorePosMapping.objects.filter(pos=pos.id).all()
                    for pos_store in pos_stores:
                        store_ser = StoreSerializer(pos_store.store).data
                        store_ser['level'] = 'pos'
                        store_ser['pos_code'] = pos.pos_code
                        store_ser['pos_name'] = pos.pos_name
                        store_ser['pos_type'] = pos.pos_type
                        mapp.append(store_ser)
                return JsonResponse({'message':'Cluster Store childs.', 'status':True, 'status_code':200, 'result':mapp, 'current_level':'cluster'}, status=200)
            
            pos_store = StorePosMapping.objects.filter(store=store).last()
            if pos_store:
                return JsonResponse({'message':'Store is at POS level it does not have any child store.', 'status':False, 'status_code':400}, status=400)
            
            return JsonResponse({'message':'Could not find store.', 'status':False, 'status_code':400}, status=400)



class GetParentStore(APIView):
    def get(self, request):
        store = request.GET.get('store')
        mapp = []
        if store:
            pos_store = StorePosMapping.objects.filter(store=store).last()
            if pos_store:
                cluster_stores = StoreClusterMapping.objects.filter(cluster=pos_store.pos.cluster.id).last()
                if cluster_stores:
                    cluster_store_ser = StoreSerializer(cluster_stores.store).data
                    cluster_store_ser['level'] = 'cluster'
                    cluster_store_ser['cluster_code'] = pos_store.pos.cluster.cluster_code
                    cluster_store_ser['cluster_name'] = pos_store.pos.cluster.cluster_name
                    cluster_store_ser['brand_store'] = []
                    
                    brand_cluster = BrandClusterMapping.objects.filter(cluster=pos_store.pos.cluster.id).last()
                    if brand_cluster:
                        brand_store = StoreBrandMapping.objects.filter(brand=brand_cluster.brand.id).last()
                        if brand_store:
                            brand_store_ser = StoreSerializer(brand_store.store).data
                            brand_store_ser['level'] = 'brand'
                            brand_store_ser['industry_type'] = brand_store.brand.industry_type
                            brand_store_ser['brand_name'] = brand_store.brand.brand_name
                            cluster_store_ser['brand_store'].append(brand_store_ser)
                    mapp.append(cluster_store_ser)
                return JsonResponse({'message':'POS Parent Stores.', 'status':True, 'status_code':200, 'result':mapp, 'current_level':'pos'}, status=200)
        
        
            cluster_store = StoreClusterMapping.objects.filter(store=store).last()
            if cluster_store:
                brand_cluster = BrandClusterMapping.objects.filter(cluster=cluster_store.cluster.id).last()
                if brand_cluster:
                    brand_store = StoreBrandMapping.objects.filter(brand=brand_cluster.brand.id).last()
                    if brand_store:
                        brand_store_ser = StoreSerializer(brand_store.store).data
                        brand_store_ser['industry_type'] = brand_store.brand.industry_type
                        brand_store_ser['brand_name'] = brand_store.brand.brand_name
                        mapp.append(brand_store_ser)
                return JsonResponse({'message':'Cluster Store parents.', 'status':True, 'status_code':200, 'result':mapp, 'current_level':'cluster'}, status=200)  

                            
            return JsonResponse({'message':'Invalid Store ID.', 'status':False, 'status_code':400, 'result':[]}, status=200)
            