from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class UnitOfMeasurementApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer = UnitOfMeasurementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Unit Of Measurement type registered successfully', 'status_code':201}, status=201)
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
            queryset = UnitOfMeasurement.objects.filter(id=id).last()
            serializer=UnitOfMeasurementSerializer(queryset)
            return JsonResponse({'message':'Unit Of Measurement info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                queryset = UnitOfMeasurement.objects.filter(brand=brand).filter(queue(unit_name__icontains=query)|queue(unit_description__icontains=query)).all()[start:end]
                count = UnitOfMeasurement.objects.filter(brand=brand).filter(queue(unit_name__icontains=query)|queue(unit_description__icontains=query)).count()
            else:
                queryset = UnitOfMeasurement.objects.filter(brand=brand).all()[start:end]
                count = UnitOfMeasurement.objects.filter(brand=brand).count()
                
            serializer = UnitOfMeasurementSerializer(queryset, many=True)
            return JsonResponse({'message':'Unit Of Measurement list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('register_types')
    def put(self, request):
        unit_measurement_id=request.data.get("id")
        unit_measurement_info = UnitOfMeasurement.objects.filter(id=unit_measurement_id).last()
        if unit_measurement_info:
            serializer = UnitOfMeasurementSerializer(unit_measurement_info,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Unit Of Measurement type updated successfully', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
            return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400}, status=400)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
    

    @authorize('register_types')
    def delete(self, request):
        unit_measurement_id=request.data.get("id")
        unit_measurement_info = UnitOfMeasurement.objects.filter(id=unit_measurement_id)
        if unit_measurement_info:
            unit_measurement_info.delete()
            return JsonResponse({'message':'Unit Of Measurement details deleted', 'status':True, 'status_code':200, }, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)






class UnitOfMeasurementConversionApiView(APIView):
    def get(self, request):
        source_unit = request.GET.get('source_unit')
        
        units = UnitOfMeasurementConversion.objects.filter(source_unit=source_unit).all()
        serializer = UnitOfMeasurementConversionSerializer(units, many=True)
        return JsonResponse({'message':'Unit of measurement conversion.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
    
    def post(self, request):
        if request.data:
            serializer = UnitOfMeasurementConversionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Unit of measurement conversion saved.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering UOM conversion.', 'status':False, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)

    
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            if id:
                unit = UnitOfMeasurementConversion.objects.filter(id=id).last()
                if unit:
                    serializer = UnitOfMeasurementConversionSerializer(unit, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'UOM conversion updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating UOM conversion.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=200)
                return JsonResponse({'message':'Invalid UOM conversion ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'UOM conversion ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Invalid request.', 'status':False, 'status_code':400}, status=400)
    
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            UnitOfMeasurementConversion.objects.filter(id=id).delete()
            return JsonResponse({'message':'Unit of Measurement conversion deleted successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
# UnitOfMeasurementConversion