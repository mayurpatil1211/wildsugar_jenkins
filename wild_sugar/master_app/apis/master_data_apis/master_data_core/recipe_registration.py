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


class RecipeRegistrationApiView(APIView):
    @authorize('delete_recipe')
    def delete(self, request):
        id = request.data.get('id')
        if id:
            RecipeRegistration.objects.filter(id=id).delete()
            return JsonResponse({'message':'Recipe Deleted Successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'Recipe ID required.', 'status':False, 'status_code':400}, status=400)
            
    def get(self, request):
        brand = request.GET.get('brand')
        id = request.GET.get('id')
        query = request.GET.get('query', None)
        
        count_per_page = request.GET.get('count_per_page', 20)
        page = request.GET.get('page', 1)
        
        end = int(count_per_page)*int(page)
        start = end - int(count_per_page)
        
        if brand:
            if query:
                recipes = RecipeRegistration.objects.filter(brand=brand).filter(queue(item_name__icontains=query) | queue(item_code__icontains=query)).all().order_by('-created_at')[start:end]
                count = RecipeRegistration.objects.filter(brand=brand).filter(queue(item_name__icontains=query) | queue(item_code__icontains=query)).count()
            else:
                recipes = RecipeRegistration.objects.filter(brand=brand).all().order_by('-created_at')[start:end]
                count = RecipeRegistration.objects.filter(brand=brand).count()
            serializer = RecipeRegistrationSerializer(recipes, many=True)
            return JsonResponse({'message':'Recipe List.', 'status':True, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
        
        if id:
            recipe = RecipeRegistration.objects.filter(id=id).last()
            serializer = RecipeRegistrationReadSerializer(recipe)
            return JsonResponse({'message':'Recipe Details.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'Brand ID or Recipe ID required.', 'status':False, 'status_code':400}, status=400)
        
    @authorize('register_recipe')
    def post(self, request):
        if request.data:
            errors = []
            serializer = RecipeRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                if request.data.get('recipe_ingredients'):
                    status, error = self.save_recipe_ingredients(request.data.get('recipe_ingredients'), serializer.data['id'])
                    errors.extend(error)
                
                if request.data.get('recipe_variable_charges'):
                    status, error = self.save_recipe_variable_charges(request.data.get('recipe_variable_charges'), serializer.data['id'])
                    errors.extend(error)
                    
                if request.data.get('recipe_packaging'):
                    status, error = self.save_recipe_packaging(request.data.get('recipe_packaging'), serializer.data['id'])
                    errors.extend(error)
                
                if errors:
                    RecipeRegistration.objects.filter(id=serializer.data['id']).delete()
                    return JsonResponse({'message':'Error during registering recipe.', 'status':False, 'status_code':400, 'error':errors}, status=400)
                return JsonResponse({'message':'Recipe Registered Successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering recipe.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)  
    
    def put(self, request):
        errors = []
        id = request.data.get('id')
        if id:
            recipe = RecipeRegistration.objects.filter(id=id).last()
            if recipe:
                serializer = RecipeRegistrationSerializer(recipe, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    if request.data.get('recipe_ingredients'):
                        status, error = self.save_recipe_ingredients(request.data.get('recipe_ingredients'), serializer.data['id'])
                        errors.extend(error)
                    
                    if request.data.get('recipe_variable_charges'):
                        status, error = self.save_recipe_variable_charges(request.data.get('recipe_variable_charges'), serializer.data['id'])
                        errors.extend(error)
                        
                    
                    if request.data.get('recipe_packaging'):
                        status, error = self.save_recipe_packaging(request.data.get('recipe_packaging'), serializer.data['id'])
                        errors.extend(error)
                    
                    if errors:
                        return JsonResponse({'message':'Partially Updated Recipe. Error during updating some data.', 'status':False, 'status_code':200, 'result':serializer.data, 'error':errors}, status=200)
                    
                    return JsonResponse({'message':'Recipe updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating recipe.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Invalid Recipe ID.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Recipe ID required.', 'status':False, 'status_code':400}, status=400)
    
    def save_recipe_packaging(self, packaging_items, recipe_id):
        errors = []
        
        for i in packaging_items:
            i['recipe'] = recipe_id
            if i.get('package_code') and i.get('package_name'):
                package = RecipePackaging.objects.filter(recipe=recipe_id, package_code=i.get('package_code')).last()
                if package:
                    serializer = RecipePackagingSerializer(package, data=i)
                    if serializer.is_valid():
                        serializer.save()
                        
                    else:
                        errors.append(serializer.errors)
                else:
                    serializer = RecipePackagingSerializer(data=i)
                    if serializer.is_valid():
                        serializer.save()
                        
                    else:
                        errors.append(serializer.errors)
            else:
                errors.append({'data':i,'error':"Package Code and Package Name required."})
        return True, errors 
        
    
    def save_recipe_ingredients(self, ingredients, recipe_id):
        # RecipeIngredients
        errors = []
        
        for i in ingredients:
            i['recipe'] = recipe_id
            if i.get('delete'):
                RecipeIngredients.objects.filter(recipe=recipe_id, ingredient_code=i.get('ingredient_code')).delete()
            else:
                if i.get('raw_material') or i.get('semi_product'):
                    recipe_ingredient = RecipeIngredients.objects.filter(recipe=recipe_id, ingredient_code=i.get('ingredient_code')).last()
                    if recipe_ingredient:
                        serializer = RecipeIngredientCreateSerializer(recipe_ingredient, data=i)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append(serializer.errors)
                    else:
                        serializer = RecipeIngredientCreateSerializer(data=i)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append(serializer.errors)
                else:
                    errors.append({'data':i,'error':"Semi Product ID or Raw Material ID, required as a ingredients"})
        return True, errors
    
    
    def save_recipe_variable_charges(self, charges, recipe_id):
        errors = []
        
        for i in charges:
            i['recipe'] = recipe_id
            if i.get('variable_charge_code') and i.get('variable_charge'):
                variable = RecipeVariableCharges.objects.filter(recipe=recipe_id, variable_charge_code=i.get('variable_charge_code')).last()
                if variable:
                    if not float(variable.variable_charge) == float(i.get('variable_charge')):
                        serializer = RecipeVariableChargeSerializer(variable, data=i)
                        if serializer.is_valid():
                            serializer.save()
                            variable.latest=False
                            variable.save()
                        else:
                            errors.append(serializer.errors)
                else:
                    serializer = RecipeVariableChargeSerializer(data=i)
                    if serializer.is_valid():
                        serializer.save()
                        
                    else:
                        errors.append(serializer.errors)
            else:
                errors.append({'data':i,'error':"Variable Charge Code and Variable Charge Value required."})
        return True, errors 