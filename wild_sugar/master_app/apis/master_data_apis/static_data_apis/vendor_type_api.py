from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class VendorTypeApiView(APIView):
    # permission_classes = (AllowAny,)
    
    @authorize('register_types')
    def post(self, request):
        if request.data:
            serializer = VendorTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Vendor type registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)

    def get(self, request):
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
        
        id = request.GET.get('id', None)
        
        if id:
            queryset = VendorTypes.objects.filter(id=id).last()
            serializer=VendorTypeSerializer(queryset)
            return JsonResponse({'message':'Vendor Type', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                queryset = VendorTypes.objects.filter(brand=brand).filter(queue(vendor_type__icontains=query)|queue(vendor_type_description__icontains=query))[start:end]
                count = VendorTypes.objects.filter(brand=brand).filter(queue(vendor_type__icontains=query)|queue(vendor_type_description__icontains=query)).count()
            else:
                queryset = VendorTypes.objects.filter(brand=brand).all()[start:end]
                count = VendorTypes.objects.filter(brand=brand).count()
            serializer = VendorTypeSerializer(queryset, many=True)
            return JsonResponse({'message':'Vendor list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
        
    @authorize('register_types')
    def put(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorTypes.objects.filter(id=vendor_id).last()
        if vendor_info:
            serializer = VendorTypeSerializer(vendor_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Vendor type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('register_types')
    def delete(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorTypes.objects.filter(id=vendor_id)
        if vendor_info:
            vendor_info.delete()
            return JsonResponse({'message':'Vendor type deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
