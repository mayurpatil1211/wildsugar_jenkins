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


class HsnCodeCrudApiView(APIView):
    @authorize('register_hsn_code')
    def post(self, request):
        errors = []
        if request.data:
            
            serializer = HSNtaxInformationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                if request.data.get('hsn_code_tags'):
                    status, error = self.save_tags(serializer.data['id'], request.data.get('hsn_code_tags'))
                    errors.extend(error)
                
                new_ser = HSNtaxInformationReadSerializer(HSNtaxInformation.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'HSN code information saved.', 'status':True, 'status_code':201, 'result':new_ser.data, 'error':errors}, status=201)
            return JsonResponse({'message':'Error during saving HSN code information.','status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_hsn_code')
    def put(self, request):
        if request.data:
            id = request.data.get('id')
            errors = []
            if id:
                hsn = HSNtaxInformation.objects.filter(id=id).last()
                if hsn:
                    serializer = HSNtaxInformationSerializer(hsn, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        if request.data.get('hsn_code_tags'):
                            status, error = self.save_tags(serializer.data['id'], request.data.get('hsn_code_tags'))
                            errors.extend(error)
                        
                        new_ser = HSNtaxInformationReadSerializer(HSNtaxInformation.objects.filter(id=serializer.data['id']).last())
                        return JsonResponse({'message':'HSN code updated.', 'status':True, 'status_code':200, 'result':new_ser.data, 'error':errors}, status=200)
                    return JsonResponse({'message':'Error during updating HSN code information.','status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid HSN id, Could not found.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)
    
    
    
    def save_tags(self, hsn_code_id, tags):
        errors = []
        for tag in tags:
            is_exists = HSNcodeTags.objects.filter(hsn=hsn_code_id, tag=tag).last()
            if is_exists:
                pass
            else:
                serializer = HSNcodeTagSerializer(data={
                    'hsn':hsn_code_id,
                    'tag' : tag
                })
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
        return True, errors
    
    
    def get(self, request):
        brand = request.GET.get('brand')
        id = request.GET.get('id')
        query = request.GET.get('query', None)
        
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 50)
        
        end = int(page)*int(count_per_page)
        start = int(end) - int(count_per_page)
        
        if id:
            hsn_codes = HSNtaxInformation.objects.filter(id=id).last()
            serializer = HSNtaxInformationReadSerializer(hsn_codes)
            return JsonResponse({'message':'HSN code result.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if not query:
            hsn_codes = HSNtaxInformation.objects.all()[start:end]
            serializer = HSNtaxInformationReadSerializer(hsn_codes, many=True)
            count = HSNtaxInformation.objects.count()
            return JsonResponse({'message':'HSN code result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        else:
            hsn_codes = HSNtaxInformation.objects.filter(queue(hsn_code__icontains=query) | queue(hsn_code_tags__tag__icontains=query))[start:end]
            serializer = HSNtaxInformationReadSerializer(hsn_codes, many=True)
            count = HSNtaxInformation.objects.filter(queue(hsn_code__icontains=query) | queue(hsn_code_tags__tag__icontains=query)).count()
            return JsonResponse({'message':'HSN code result.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        
    
    @authorize('delete_hsn_code')
    def delete(self, request):
        id = request.GET.get('id')
        HSNtaxInformation.objects.filter(id=id).delete()
        return JsonResponse({'message':'HSN code deleted successfully.', 'status':True, 'status_code':200}, status=200)
    


class HSNCodeTagsApiView(HsnCodeCrudApiView):
    @authorize('register_hsn_code_tag')
    def post(self, request):
        id = request.data.get('id')
        tags = request.data.get('hsn_code_tags')
        
        errors = []
        if id and tags:
            status, error = self.save_tags(id, tags)
            errors.extend(error)
            if status:
                return JsonResponse({'message':'Tags registered to the HSN code successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
            return JsonResponse({'message':'Error during registering tags to the HSN code.', 'status':False, 'status_code':400, 'error':errors}, status=400)
        return JsonResponse({'message':'HSN code ID and Tag list required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_hsn_code_tag')
    def delete(self, request):
        id = request.data.get('id')
        tags = request.data.get('hsn_code_tags',[])
        tag_id = request.data.get('tag_id',[])
        
        if id:
            
            if tags or tag_id:
                hsn_codes = HSNtaxInformation.objects.filter(queue(id=id) | queue(hsn_code=id)).last()
                if hsn_codes:
                    HSNcodeTags.objects.filter(hsn=id).filter(queue(id__in=tag_id) | queue(tag__in=tags)).delete()
                    return JsonResponse({'message':'Tags deleted successfully.', 'status':True, 'status_code':200}, status=200)
                return JsonResponse({'message':'Invalid HSN code or ID.', 'status':False, 'status_code':404}, status=404)
            return JsonResponse({'message':'Tag list or Tag ID list required to delete.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'HSN ID required.', 'status':False, 'status_code':400}, status=400)