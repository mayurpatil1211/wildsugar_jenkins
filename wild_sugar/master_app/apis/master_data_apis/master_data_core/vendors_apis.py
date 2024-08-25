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


class VendorsApiView(APIView):
    @authorize('register_vendor')
    def post(self, request):
        cluster = request.data.get('cluster', None)
        brand = request.data.get('brand', None)
        pos = request.data.get('pos', None)
        if cluster or brand or pos:
            if cluster:
                cluster = Clusters.objects.filter(id=cluster).last()
            elif brand:
                brand = Brand.objects.filter(id=brand).last()
            elif pos:
                pos = POS.objects.filter(id=pos).last()
                
            if not brand:
                return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)


            if brand or cluster or pos:
                serializer = VendorSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    

                    if cluster:
                        vendor_cluster = VendorClusterMappingSerializer(data={
                            'vendor' : serializer.data['id'],
                            'cluster' : cluster.id
                        })
                        if vendor_cluster.is_valid():
                            vendor_cluster.save()
                            status, error = self.save_bank_details(request.data, serializer.data['id'])
                            if status:
                                serializer = VendorReadSerializer(Vendors.objects.filter(id=serializer.data['id']).last())
                                return JsonResponse({'message':'Vendor registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=200)
                            return JsonResponse({'message':'Vendor registered successfully, but could not register bank details for vendor.', 'status':True, 'status_code':201, 'error':error}, status=201)
                        Vendors.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during mapping cluster and vendor, please check cluster you have selected.', 'status':False, 'status_code':400, 'error':vendor_cluster.errors}, status=400)

                    elif brand:
                        
                        vendor_cluster = VendorBrandMappingSerializer(data={
                            'vendor' : serializer.data['id'],
                            'brand' : brand.id
                        })

                        if vendor_cluster.is_valid():
                            vendor_cluster.save()
                            status, error = self.save_bank_details(request.data, serializer.data['id'])
                            if status:
                                serializer = VendorReadSerializer(Vendors.objects.filter(id=serializer.data['id']).last())
                                return JsonResponse({'message':'Vendor registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=200)
                            return JsonResponse({'message':'Vendor registered successfully, but could not register bank details for vendor.', 'status':True, 'status_code':201, 'error':error}, status=201)
                        Vendors.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during mapping cluster and vendor, please check cluster you have selected.', 'status':False, 'status_code':400, 'error':vendor_cluster.errors}, status=400)

                    elif pos:
                        
                        vendor_cluster = VendorPOSMappingSerializer(data={
                            'vendor' : serializer.data['id'],
                            'pos' : pos.id
                        })

                        if vendor_cluster.is_valid():
                            vendor_cluster.save()
                            status, error = self.save_bank_details(request.data, serializer.data['id'])
                            if status:
                                serializer = VendorReadSerializer(Vendors.objects.filter(id=serializer.data['id']).last())
                                return JsonResponse({'message':'Vendor registered successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=200)
                            return JsonResponse({'message':'Vendor registered successfully, but could not register bank details for vendor.', 'status':True, 'status_code':201, 'error':error}, status=201)
                        Vendors.objects.filter(id=serializer.data['id']).delete()
                        return JsonResponse({'message':'Error during mapping cluster and vendor, please check cluster you have selected.', 'status':False, 'status_code':400, 'error':vendor_cluster.errors}, status=400)
                    
                return JsonResponse({'message':'Error during registering vendor.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid cluster, brand or POS.', 'status':False, 'status_code':400, 'error':[{'error':'Cluster not found.'}]}, status=400)
        return JsonResponse({'message':'Cluster, Brand or POS ID required.', 'status':False, 'status_code':400}, status=400)
    
    def save_bank_details(self, data, vendor_id):
        bank_details = data.get('bank_details')
        if bank_details:
            bank_details['vendor'] = vendor_id

            serializer = VendorBankDetailSerializer(data=bank_details)
            if serializer.is_valid():
                serializer.save()
                return True, {}
            return False, serializer.errors
        return True, {}
    

    def get(self, request):
        cluster = request.GET.get('cluster', None)
        brand = request.GET.get('brand', None)
        pos = request.GET.get('pos', None)
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
            
        if cluster:
            vendors_ids = VendorClusterMapping.objects.filter(cluster=cluster).all().distinct().values_list('vendor', flat=True)
            if query:
                vendors = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query))[start:end]
                count = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query)).count()
            else:
                vendors = Vendors.objects.filter(id__in=vendors_ids).all()
                count = Vendors.objects.filter(id__in=vendors_ids).count()
            serializer = VendorReadSerializer(vendors, many=True)
            return JsonResponse({'message':'Vendor List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        if brand:
            vendors_ids = VendorBrandMapping.objects.filter(brand=brand).all().distinct().values_list('vendor', flat=True)
            if query:
                vendors = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query))[start:end]
                count = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query)).count()
            else:
                vendors = Vendors.objects.filter(id__in=vendors_ids).all()[start:end]
                count = Vendors.objects.filter(id__in=vendors_ids).count()
            serializer = VendorReadSerializer(vendors, many=True)
            
            return JsonResponse({'message':'Vendor List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)

        if pos:
            vendors_ids = VendorPOSMapping.objects.filter(pos=pos).all().distinct().values_list('vendor', flat=True)
            if query:
                vendors = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query))[start:end]
                count = Vendors.objects.filter(id__in=vendors_ids).filter(queue(vendor_code__icontains=query)|queue(vendor_name__icontains=query)|queue(city__icontains=query)|queue(state__icontains=query)|queue(email__icontains=query)|queue(pan__icontains=query)|queue(gstn__icontains=query)|queue(vendor_type__icontains=query)).count()
            else:
                vendors = Vendors.objects.filter(id__in=vendors_ids).all()
                count = Vendors.objects.filter(id__in=vendors_ids).all()
            serializer = VendorReadSerializer(vendors, many=True)
            return JsonResponse({'message':'Vendor List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            vendors = Vendors.objects.filter(id=id).last()
            serializer = VendorReadSerializer(vendors)
            return JsonResponse({'message':'Vendor List.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)

        return JsonResponse({'message':'Cluster, Brand or POS ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('update_vendor')
    def put(self, request):
        id = request.data.get('id', None)
        if id:
            vendor = Vendors.objects.filter(id=id).last()
            if vendor:
                serializer = VendorSerializer(vendor, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Vendor Updated Successfully.', 'status':True, 'status_code':200, 'result': serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating vendor details.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Invalid Vendor ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_vendor')
    def delete(self, request):
        id = request.data.get('id', None)
        vendor = Vendors.objects.filter(id=id).delete()
        return JsonResponse({'message':'Vendor deleted successfully.', 'status':True, 'status_code':200}, status=200)