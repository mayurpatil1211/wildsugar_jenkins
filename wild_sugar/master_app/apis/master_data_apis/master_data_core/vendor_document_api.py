from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class VendorDocumentApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_vendor_documents')
    def post(self, request):
        if request.data:
            serializer = VendorDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Vendor document registered successfully', 'status_code':201}, status=201)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400,'errors':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request', 'status':False, 'status_code':400}, status=400)

    def get(self, request):
        queryset = VendorDocuments.objects.all()
        serializer = VendorDocumentSerializer(queryset, many=True)
        return JsonResponse({'message':'Vendor document list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
    @authorize('update_vendor_documents')
    def put(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorDocuments.objects.filter(id=vendor_id).last()
        if vendor_info:
            serializer = VendorDocumentSerializer(vendor_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Vendor document updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    
    @authorize('delete_vendor_documents')
    def delete(self, request):
        vendor_id=request.data.get("id")
        vendor_info = VendorDocuments.objects.filter(id=vendor_id)
        if vendor_info:
            vendor_info.delete()
            return JsonResponse({'message':'Vendor document deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
