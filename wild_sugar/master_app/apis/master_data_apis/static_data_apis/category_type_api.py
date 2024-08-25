from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q as queue

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize


class CategoryTypeApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer = CategoryListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                if request.data.get('sub_categories'):
                    category = CategoryList.objects.filter(id=serializer.data['id']).last()
                    for sub_category in request.data.get('sub_categories'):
                        category.sub_categories.add(SubcategoryList.objects.get(id=sub_category))
                        category.save()
                        res_serializer = CategorySubcategoryListSerializer(category)
                    return JsonResponse({'result':res_serializer.data, 'status':True, 'message':'Category registered successfully', 'status_code':201}, status=201)
                
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Category registered successfully', 'status_code':201}, status=201)
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
            queryset = CategoryList.objects.filter(id=id).last()
            serializer=CategorySubcategoryListSerializer(queryset)
            return JsonResponse({'message':'Category', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                queryset = CategoryList.objects.filter(brand=brand).filter(queue(category_name__icontains=query)|queue(category_type__icontains=query))[start:end]
                count = CategoryList.objects.filter(brand=brand).filter(queue(category_name__icontains=query)|queue(category_type__icontains=query)).count()
            else:
                queryset = CategoryList.objects.filter(brand=brand).all()[start:end]
                count = CategoryList.objects.filter(brand=brand).count()
            serializer = CategorySubcategoryListSerializer(queryset, many=True)
            return JsonResponse({'message':'Category List', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_types')
    def put(self, request):
        if request.data.get("id"):
            category_list_info = CategoryList.objects.get(id=request.data.get("id"))
            if category_list_info:
                serializer = CategoryListSerializer(category_list_info,data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    if request.data.get('sub_categories'):
                        category = CategoryList.objects.filter(id=serializer.data['id']).last()
                        for sub_category in request.data.get('sub_categories'):
                            category.sub_categories.add(SubcategoryList.objects.get(id=sub_category))
                            category.save()
                            res_serializer = CategorySubcategoryListSerializer(category)
                        return JsonResponse({'result':res_serializer.data, 'status':True, 'message':'Category updated successfully', 'status_code':200}, status=200)
                        
                    return JsonResponse({'message':'Category updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
            return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
        return JsonResponse({'message':'Category ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('register_types')
    def delete(self, request):
        category_list_id=request.data.get("id")
        category_list_info = CategoryList.objects.filter(id=category_list_id)
        if category_list_info:
            category_list_info.delete()
            return JsonResponse({'message':'Category type deleted successfully', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)






class SubcategoryListApiView(APIView):
    # permission_classes = (AllowAny,)
    @authorize('register_types')
    def post(self, request):
        if request.data:
            brand = request.data.get('brand', None)
            if not brand:
                return JsonResponse({'message':'Brand ID Required.', 'status':False, 'status_code':400}, status=400)
            
            serializer = SubcategoryListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                if request.data.get('categories'):
                    sub_category = SubcategoryList.objects.filter(id=serializer.data['id']).last()
                    for category in request.data.get('categories'):
                        sub_category.categories.add(CategoryList.objects.get(id=category))
                        sub_category.save()
                        res_serializer = SubcategoryCategoryListSerializer(sub_category)
                    return JsonResponse({'result':res_serializer.data, 'status':True, 'message':'Sub-category registered successfully', 'status_code':201}, status=201)
                    
                return JsonResponse({'result':serializer.data, 'status':True, 'message':'Subcategory registered successfully', 'status_code':201}, status=201)
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
            queryset = SubcategoryList.objects.filter(id=id).last()
            serializer=SubcategoryCategoryListSerializer(queryset)
            return JsonResponse({'message':'Subcategory', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        
        if brand:
            if query:
                queryset = SubcategoryList.objects.filter(queue(sub_category_name__icontains=query)|queue(sub_category_type__icontains=query))[start:end]
                count = SubcategoryList.objects.filter(queue(sub_category_name__icontains=query)|queue(sub_category_type__icontains=query)).count()
            else:
                queryset = SubcategoryList.objects.all()[start:end]
                count= SubcategoryList.objects.count()
            serializer = SubcategoryCategoryListSerializer(queryset, many=True)
            return JsonResponse({'message':'Sub-category list', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        return JsonResponse({'message':'Brand ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('register_types')
    def put(self, request):
        if request.data.get("id"):
            sub_category_info = SubcategoryList.objects.get(id=request.data.get("id"))
            if sub_category_info:
                serializer = SubcategoryListSerializer(sub_category_info,data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    if request.data.get('categories'):
                        sub_category = SubcategoryList.objects.filter(id=serializer.data['id']).last()
                        for category in request.data.get('categories'):
                            sub_category.categories.add(CategoryList.objects.get(id=category))
                            sub_category.save()
                            res_serializer = SubcategoryCategoryListSerializer(sub_category)
                        return JsonResponse({'result':res_serializer.data, 'status':True, 'message':'Sub-category registered successfully', 'status_code':200}, status=200)
                    
                    return JsonResponse({'message':'Sub-category info', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'status':False, 'message':'Error during register', 'status_code':400, 'errors':serializer.errors}, status=400)
            return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
        return JsonResponse({'message':'Sub-category ID required.', 'status':False, 'status_code':400}, status=400)

    @authorize('register_types')
    def delete(self, request):
        sub_category_id=request.data.get("id")
        if sub_category_id:
            sub_category_info = SubcategoryList.objects.filter(id=sub_category_id)
            if sub_category_info:
                sub_category_info.delete()
                return JsonResponse({'message':'Sub-category deleted', 'status':True, 'status_code':200, }, status=200)
            return JsonResponse({'status':False,'message':'No valid information', 'status_code':404}, status=404)
        return JsonResponse({'message':'Sub-category ID required.', 'status':False, 'status_code':400}, status=400)
