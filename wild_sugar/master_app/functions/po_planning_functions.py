from master_app.models import *


class PoPlanningFunctions:
    def __ini__(self, po_planning_id=None, store=None):
        self.po_planning_id =po_planning_id
        self.store = store
    
    
    def add_balance_quantity(self, item_code, uom, quantity):
        item_planned_material = PoPlanningMaterial.objects.filter(po_plan__expired=False, item_code=item_code).last()
        if item_planned_material:
            if item_planned_material.raw_material.default_uom == uom:
                item_planned_material.balance_qauntity += quantity
                item_planned_material.save()
            else:
                extra_uom = RawMaterialUomModel.objects.filter(raw_material__item_code=item_code, uom=uom).last()
                if extra_uom:
                    default_qty = extra_uom.new_uom_to_default_uom_ratio*quantity
                    item_planned_material.balance_qauntity += default_qty
                    item_planned_material.save()
                    
    
    def decrease_balance_quantity(self, item_code, uom, quantity):
        item_planned_material = PoPlanningMaterial.objects.filter(po_plan__expired=False, item_code=item_code).last()
        if item_planned_material:
            if item_planned_material.raw_material.default_uom == uom:
                item_planned_material.balance_qauntity -= quantity
                item_planned_material.save()
            else:
                extra_uom = RawMaterialUomModel.objects.filter(raw_material__item_code=item_code, uom=uom).last()
                if extra_uom:
                    default_qty = extra_uom.new_uom_to_default_uom_ratio*quantity
                    item_planned_material.balance_qauntity -= default_qty
                    item_planned_material.save()
    
    
    def validate_po_items(self, po_items):
        errors = []
        items = []
        
        for item in po_items:
            # RawMaterialUomModel
            uom = item.get('uom')
            qty = item.get('quantity')
            
            if uom != item.get('default_uom'):
                extra_uom = RawMaterialUomModel.objects.filter(raw_material__item_code=item.get('item_code'), uom=uom).last()
                if extra_uom:
                    default_qty = extra_uom.new_uom_to_default_uom_ratio*qty
                    item_planned_material = PoPlanningMaterial.objects.filter(po_plan__expired=False, item_code=item.get('item_code')).last()
                    if item_planned_material:
                        if item_planned_material.planned:
                            if default_qty<=item_planned_material.balance_qauntity:
                                item['send_approval'] = False
                                items.append(item)
                            else:
                                errors.append({
                                    'error':'Item order quantity crossing the limits.',
                                    'default_uom' : item_planned_material.default_uom,
                                    'default_uom_quantity' : item_planned_material.default_uom_quantity,
                                    'allowed_quantity' : item_planned_material.total_allowed_quantity,
                                    'balance_qauntity' : item_planned_material.balance_qauntity
                                })
                        else:
                            # depends on configuration
                            pass
                    else:
                        # send for apprroval
                        pass
                else:
                    pass
            else:
                default_qty = 1*qty
                item_planned_material = PoPlanningMaterial.objects.filter(po_plan__expired=False, item_code=item.get('item_code')).last()
                if item_planned_material:
                    if item_planned_material.planned:
                        if default_qty<=item_planned_material.balance_qauntity:
                            item['send_approval'] = False
                            items.append(item)
                        else:
                            errors.append({
                                'error':'Item order quantity crossing the limits.',
                                'default_uom' : item_planned_material.default_uom,
                                'default_uom_quantity' : item_planned_material.default_uom_quantity,
                                'allowed_quantity' : item_planned_material.total_allowed_quantity,
                                'balance_qauntity' : item_planned_material.balance_qauntity
                            })
                    else:
                        pass
                else:
                    pass
        return errors, items