from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class VendorTypesApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer = VendorTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Vendor type registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)
    

    def get(self, request):
        queryset = VendorTypes.objects.all()
        serializer = VendorTypeSerializer(queryset, many=True)
        return JsonResponse({'message':'Vendor info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
    

    def put(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorTypes.objects.get(id=vendor_id)
        if vendor_info:
            serializer = VendorTypeSerializer(vendor_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Vendor info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    

    def delete(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorTypes.objects.filter(id=vendor_id)
        if vendor_info:
            vendor_info.delete()
            return JsonResponse({'message':'Vendor info deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
