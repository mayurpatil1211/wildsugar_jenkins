from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.db.models import Q as queue
from django.db.models import Count

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

import logging

logger = logging.getLogger('debug_file')

User = get_user_model()



class PoPlanningTemplateApiView(APIView):
    @authorize('create_po_planning_template')
    def post(self, request):
        if request.data:
            serializer = PoPlanningTemplateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Po Planning Template Saved.', 'status':True, 'status_code':200, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during creating template', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request', 'status':False, 'status_code':400}, status=400)
    
    def put(self, request):
        _id =request.data.get('id', None)
        if _id:
            po_planning_template = PoPlanningTemplates.objects.filter(id=_id).last()
            if po_planning_template:
                serializer = PoPlanningTemplateSerializer(po_planning_template, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Po Planning Template Updated.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating template.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid PO planning template.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Template ID required.', 'status':False, 'status_code':400}, status=400)
    
    def get(self, request):
        store = request.GET.get('store', None)
        cluster = request.GET.get('cluster', None)
        brand = request.GET.get('brand', None)
        _id = request.GET.get('id', None)
        
        if _id:
            planning_template = PoPlanningTemplates.objects.filter(id=_id).last()
            serializer = PoPlanningTemplateSerializer(planning_template)
            return JsonResponse({'message':'Planning Template', 'status':False, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            planning_template = PoPlanningTemplates.objects.filter(store__brand__id=brand).all()
            serializer = PoPlanningTemplateSerializer(planning_template, many=True)
            return JsonResponse({'message':'Po Planning templates.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if cluster:
            planning_template = PoPlanningTemplates.objects.filter(store__cluster__id=cluster).all()
            serializer = PoPlanningTemplateSerializer(planning_template, many=True)
            return JsonResponse({'message':'Po Planning templates.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        
        if store:
            planning_template = PoPlanningTemplates.objects.filter(store=store).all()
            serializer = PoPlanningTemplateSerializer(planning_template, many=True)
            return JsonResponse({'message':'Po Planning templates.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        return JsonResponse({'message':'ID, Store ID, Brand ID or Cluster ID any one of the ID required.', 'status':False, 'status_code':400}, status=400)