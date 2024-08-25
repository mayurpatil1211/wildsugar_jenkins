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



class PoPlanningAPIView(APIView):
    @authorize('create_po_planning')
    def post(self, request):
        errors = []
        if request.data:
            po_plan_material = request.data.get('po_plan_material')
            serializer = PoPlanningSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                error = self.save_po_plan_material(serializer.data['id'], po_plan_material)
                if error:
                    PoPlanning.objects.filter(id=serializer.data['id']).delete()
                    return JsonResponse({'message':'Error during creating PO plan.', 'status':False, 'status_code':400, 'error':error}, status=400)
                self.mark_un_planned(serializer.data['store'], po_plan_material)
                serializer = PoPlanningReadSerializer(PoPlanning.objects.filter(id=serializer.data['id']).last())
                return JsonResponse({'message':'Po Plan Created Successfully.', 'status':True, 'status_code':201, 'result':serializer.data, 'error':error}, status=201)
            
            return JsonResponse({'message':'Error during creating PO plan.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
    
    def mark_un_planned(self, store, materials):
        for material in materials:
            if material.get('planned'):
                serializer = UnplannedItemSerializer(data={
                    'store':store,
                    "item_code" : material.get('item_code'),
                    "item_name" : material.get('item_name')
                })
                if serializer.is_valid():
                    serializer.save()
            else:
                UnplannedItems.objects.filter(item_code=material.get('item_code'), store=store).last()
    
    def save_material_distribution(self, plan_material_id, material_distributions):
        errors = []
        for material_distribution in material_distributions:
            if material_distribution.get('id'):
                if material_distribution.get('delete'):
                    PlanningMaterialDistribution.objects.filter(id=material_distribution.get('id')).delete()
                else:
                    po_planning_distribution = PlanningMaterialDistribution.objects.filter(id=material_distribution.get('id')).last()
                    if po_planning_distribution:
                        material_distribution['planning_material_reference']=plan_material_id
                        serializer = PlanningMaterialDistributionSerializer(po_planning_distribution, data=material_distribution)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append(serializer.errors)
                    else:
                        po_planning_distribution = PlanningMaterialDistribution.objects.filter(store=material_distribution.get('store'), planning_material_reference=material_distribution.get('planning_material_reference')).last()
                        if po_planning_distribution:
                            serializer = PlanningMaterialDistributionSerializer(po_planning_distribution, data=material_distribution)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                errors.append(serializer.errors)
                        else:
                            print('saved')
                            material_distribution['planning_material_reference']=plan_material_id
                            print(material_distribution)
                            serializer = PlanningMaterialDistributionSerializer(data=material_distribution)
                            if serializer.is_valid():
                                serializer.save()
                                print('saved')
                            else:
                                errors.append(serializer.errors)
            else:
                if material_distribution.get('delete'):
                    PlanningMaterialDistribution.objects.filter(store=material_distribution.get('store'), planning_material_reference=material_distribution.get('planning_material_reference')).delete()
                else:
                    
                    po_planning_distribution = PlanningMaterialDistribution.objects.filter(store=material_distribution.get('store'), planning_material_reference=material_distribution.get('planning_material_reference')).last()
                    
                    if po_planning_distribution:
                        serializer = PlanningMaterialDistributionSerializer(po_planning_distribution, data=material_distribution)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append(serializer.errors)
                    else:
                        
                        material_distribution['planning_material_reference']=plan_material_id
                        serializer = PlanningMaterialDistributionSerializer(data=material_distribution)
                        if serializer.is_valid():
                            serializer.save()
                            print('saved')
                        else:
                            print(serializer.errors)
                            errors.append(serializer.errors)
        if errors:
            return False, errors
        return True, []
    
    def save_po_plan_material(self, plan_id, materials):
        errors = []
        for material in materials:
            planning_material_distribution_reference = material.get('planning_material_distribution_reference',[])
            if material.get('id'):
                if material.get('delete'):
                    PoPlanningMaterial.objects.filter(id=material.get('id')).delete()
                else:
                    po_plan_material = PoPlanningMaterial.objects.filter(id=material.get('id')).last()
                    if po_plan_material:
                        material['po_plan'] = plan_id
                        serializer = PoPlanningMaterialSerializer(po_plan_material, data=material)
                        if serializer.is_valid():
                            planning_material_distribution_reference_status, planning_material_distribution_reference_data = self.save_material_distribution(serializer.data['id'],planning_material_distribution_reference)
                            if not planning_material_distribution_reference_status:
                                errors.extend(planning_material_distribution_reference_data)
                            else:
                                serializer.save()             
                        else:
                            errors.append(serializer.errors)
                    else:
                        
                        po_plan_material = PoPlanningMaterial.objects.filter(po_plan=plan_id, raw_material=material.get('raw_material')).last()
                        if po_plan_material:
                            material['po_plan'] = plan_id
                            serializer = PoPlanningMaterialSerializer(po_plan_material, data=material)
                            if serializer.is_valid():
                                planning_material_distribution_reference_status, planning_material_distribution_reference_data = self.save_material_distribution(serializer.data['id'],planning_material_distribution_reference)
                                if not planning_material_distribution_reference_status:
                                    errors.extend(planning_material_distribution_reference_data)
                                else:
                                    serializer.save()
                            else:
                                errors.append(serializer.errors)
                        else:
                            material['po_plan'] = plan_id
                            serializer = PoPlanningMaterialSerializer(data=material)
                            if serializer.is_valid():
                                serializer.save()
                                planning_material_distribution_reference_status, planning_material_distribution_reference_data = self.save_material_distribution(serializer.data['id'],planning_material_distribution_reference)
                                if not planning_material_distribution_reference_status:
                                    errors.extend(planning_material_distribution_reference_data)
                                    PoPlanningMaterial.objects.filter(id=serializer.data.get('id')).delete()
                                else:
                                    pass
                                    
                            else:
                                errors.append(serializer.errors)
                
            else:
                if material.get('delete'):
                    PoPlanningMaterial.objects.filter(po_plan=plan_id,raw_material=material.get('raw_material')).delete()
                else:
                    po_plan_material = PoPlanningMaterial.objects.filter(po_plan=plan_id,raw_material=material.get('raw_material')).last()
                    if po_plan_material:
                        material['po_plan'] = plan_id
                        serializer = PoPlanningMaterialSerializer(po_plan_material, data=material)
                        if serializer.is_valid():
                            planning_material_distribution_reference_status, planning_material_distribution_reference_data = self.save_material_distribution(serializer.data['id'],planning_material_distribution_reference)
                            if not planning_material_distribution_reference_status:
                                errors.extend(planning_material_distribution_reference_data)
                            else:
                                serializer.save()
                        else:
                            errors.append(serializer.errors)
                    else:
                        material['po_plan'] = plan_id
                        serializer = PoPlanningMaterialSerializer(data=material)
                        if serializer.is_valid():
                            serializer.save()
                            planning_material_distribution_reference_status, planning_material_distribution_reference_data = self.save_material_distribution(serializer.data['id'],planning_material_distribution_reference)
                            # print(planning_material_distribution_reference_status, planning_material_distribution_reference_data)
                            if not planning_material_distribution_reference_status:
                                errors.extend(planning_material_distribution_reference_data)
                                PoPlanningMaterial.objects.filter(id=serializer.data.get('id')).delete()
                            else:
                                pass
                        else:
                            errors.append(serializer.errors)
            
        return errors
    
    @authorize('update_po_planning')
    def put(self, request):
        id = request.data.get('id')
        if id:
            po_plan = PoPlanning.objects.filter(id=id).last()
            if po_plan:
                serializer = PoPlanningSerializer(po_plan, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    error = self.save_po_plan_material(id, request.data.get('po_plan_material'))
                    self.mark_un_planned(serializer.data['store'], request.data.get('po_plan_material'))
                    serializer = PoPlanningReadSerializer(po_plan)
                    return JsonResponse({'message':'Updated PO plan.', 'status':True, 'status_code':200, 'result':serializer.data, 'error':error}, status=200)
                return JsonResponse({'message':'Error during updating PO plan.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid PO plan.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'PO plan ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_po_planning')
    def delete(self, request):
        id = request.data.get('id')
        if id:
            PoPlanning.objects.filter(id=id).delete()
            return JsonResponse({'message':'Po Plan deleted successfully.', 'status':True, 'status_code':200}, status=200)
        return JsonResponse({'message':'ID required.', 'status':False, 'status_code':400}, status=400)

    
    def get(self, request):
        id = request.GET.get('id')
        store = request.GET.get('store')
        expired = True if request.GET.get('expired', False) == 'true' else False
        count_per_page = request.GET.get('count_per_page', 10)
        page = request.GET.get('page', 1)
        
        if id:
            po_plan = PoPlanning.objects.filter(queue(id=id) | queue(po_planning_id=id)).last()
            if po_plan:
                serializer = PoPlanningReadSerializer(po_plan)
                return JsonResponse({'message':'PO plan details.', 'status':True, 'status_code':200, 'po_plan':serializer.data}, status=200)
            return JsonResponse({'message':'PO plan details.', 'status':True, 'status_code':200, 'po_plan':{}}, status=200)
        if store:
            try:
                end = int(count_per_page) * int(page)
            except(Exception)as e:
                end = 10*1
            
            start = end - int(count_per_page)
            
            PoPlanning.objects.filter(planned_date_to__lt=datetime.datetime.now().date()).update(expired=True)
                
            po_plans = PoPlanning.objects.filter(store=store, expired=expired)[start:end]
            count = PoPlanning.objects.filter(store=store, expired=expired).count()
            serializer = PoPlanningSerializer(po_plans, many=True)
            
            return JsonResponse({'message':'Po Plan list.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        return JsonResponse({'message':'PO plan ID or Store ID required.', 'status':False, 'status_code':400}, status=400)
        
    
    
    
    
    
    
    
    