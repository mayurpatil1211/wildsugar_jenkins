from rest_framework import serializers

from master_app.models import *
from auth_app.serializers import *

from django.conf import settings

# from django.contrib.auth.models import User


class CompanyTypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyTypes
		fields = '__all__'



class IndustryTypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = IndustryTypes
		fields = '__all__'
  

class StoreTypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = StoreTypes
		fields = '__all__'


class DepartmentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepartmentTypes
		fields = '__all__'


class PosTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = PosTypes
		fields = '__all__'

class VendorTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorTypes
		fields = '__all__'

class PrioritiyTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = PrioritiyTypes
		fields = '__all__'

class HighValueItemTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = HighValueItemTypes
		fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductTypes
		fields = '__all__'

class EmploymentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmploymentTypes
		fields = '__all__'

class SeverityTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = SeverityTypes
		fields = '__all__'


class UnitOfMeasurementSerializer(serializers.ModelSerializer):
	class Meta:
		model = UnitOfMeasurement
		fields = '__all__'
  
class UnitOfMeasurementConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurementConversion
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = CategoryList
		fields = '__all__'


class SubcategoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = SubcategoryList
		fields = ['id','sub_category_name','sub_category_type']

class CategorySubcategoryListSerializer(serializers.ModelSerializer):
	sub_categories = SubcategoryListSerializer(read_only=True, many=True)
	class Meta:
		model = CategoryList
		fields = '__all__'


class SubcategoryCategoryListSerializer(serializers.ModelSerializer):
	categories = CategoryListSerializer(many=True)
	class Meta:
		model = SubcategoryList
		fields = '__all__'


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetTypes
        fields = '__all__'

#------------ Master Data Real

class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
		fields = '__all__'


class BrandAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAddress
        fields = '__all__'


class UserBrandMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserBrandMapping
		fields = '__all__'

class ClusterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Clusters
		fields = '__all__'


class ClusterAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClusterAddress
		fields = '__all__'

class BrandClusterMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = BrandClusterMapping
		fields = '__all__'



class CompanyCluserMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyCluserMapping
		fields = '__all__'


class CompanyCluserInfoMappingSerializer(serializers.ModelSerializer):
	cluster = ClusterSerializer()
	class Meta:
		model = CompanyCluserMapping
		fields = '__all__'
  
class CompanyBrandMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyBrandMapping
		fields = '__all__'


class CompanyBrandInfoMappingSerializer(serializers.ModelSerializer):
	cluster = ClusterSerializer()
	class Meta:
		model = CompanyBrandMapping
		fields = '__all__'
  
  
  

class PosCompanyMapDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'

class CompanyPosMappingSerializer(serializers.ModelSerializer):
	pos = PosCompanyMapDetailSerializer()
	class Meta:
		model = PosCompanyMapping
		fields = ['pos']

class ClusterPosMappingSerializer(serializers.ModelSerializer):
    cluster = ClusterSerializer(many=False)
    billing_address = BrandAddressSerializer(many=False)
    shipping_address = BrandAddressSerializer(many=False)
    class Meta:
        model = POS
        fields = ['cluster', 'pos_code', 'pos_name', 'pos_type', 'billing_address', 'shipping_address', 'id']


class ShareholderUserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(allow_null=False, allow_blank=False)
	class Meta:
		model = User
		fields = [
			"id",
			"user_type",
			'username',
			"name",
			"email",
			"contact_number",
			"address",
			"city",
			"state",
			"country",
			"pan",
			"adhar"
			]
		

class CompanyShareholderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompanyShareholder
		fields = '__all__'

class CompanyShareholderSerializer(serializers.ModelSerializer):
	user = ShareholderUserSerializer(read_only=True)
	class Meta:
		model = CompanyShareholder
		fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
	# shareholder = CompanyShareholderSerializer(many=True, read_only=True)
	class Meta:
		model = Company
		depth = 1
		fields = '__all__'


class CompanyAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyAddress
        fields = '__all__'

class CompanyAddressReadSerializer(serializers.ModelSerializer):
    address = BrandAddressSerializer(many=False)
    class Meta:
        model = CompanyAddress
        fields = '__all__'

class CompanyInfoSerializer(serializers.ModelSerializer):
	shareholder = serializers.SerializerMethodField()
	# shareholder = CompanyShareholderSerializer(many=True, read_only=True)
	cluster = serializers.SerializerMethodField()
	pos = serializers.SerializerMethodField()

	class Meta:
		model = Company
		# depth = 1
		fields = '__all__'
	
	def get_shareholder(self, obj):
		return CompanyShareholderSerializer(CompanyShareholder.objects.filter(company=obj.id).all(), many=True).data
	
	def get_cluster(self, obj):
		return CompanyCluserInfoMappingSerializer(CompanyCluserMapping.objects.filter(company=obj.id).all(), many=True).data

	def get_pos(self, obj):
		return CompanyPosMappingSerializer(PosCompanyMapping.objects.filter(company=obj.id).all(), many=True).data



class DepartmentBriefSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = [
                "id",
                "department_uid",
                "department_name",
                "department_type",
                "target_food_cost",
        ]
  
  
class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'
  
  

class DepartmentClusterMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepartmentClusterMapping
		fields = '__all__'
  
# class DepartmentBrandMappingSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = DepartmentBrandMapping
# 		fields = '__all__'


class SubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDepartment
        fields = '__all__'


class SubDepartmentReadSerializer(serializers.ModelSerializer):
    parent_department = DepartmentSerializer(many=False)
    class Meta:
        model = SubDepartment
        fields = '__all__'


class DepartmentReadSerializer(serializers.ModelSerializer):
    sub_departments = SubDepartmentSerializer(read_only=True, many=True)
    class Meta:
        model = Department
        fields = '__all__'

#------------Vendors
class VendorBriefSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendors
		fields = [
			'id',
			'vendor_code',
			'vendor_name',
			'city',
			'state',
			'email',
			'vendor_type'
		]

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendors
		fields = '__all__'


class VendorBankDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorBankDetails
		fields = '__all__'

class VendorDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorDocuments
		fields = '__all__'

class VendorClusterMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorClusterMapping
		fields = '__all__'


class VendorBrandMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorBrandMapping
		fields = '__all__'


class VendorPOSMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorPOSMapping
		fields = '__all__'


class VendorReadSerializer(serializers.ModelSerializer):
	bank_details = serializers.SerializerMethodField()

	class Meta:
		model = Vendors
		fields = '__all__'
	
	def get_bank_details(self, obj):
		return VendorBankDetailSerializer(VendorBankDetails.objects.filter(vendor=obj.id).all(), many=True).data


#--------POS 
class PosBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = [	'id','pos_code',
					'pos_name',
					'pos_type',]

class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'


class PosDepartmentMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosDepartmentMapping
        fields = '__all__'


class PosSubdepartmentMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosSubdepartmentMapping
        fields = '__all__'

class PosCompanyMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosCompanyMapping
        fields = '__all__'

#----- POS Details

class PosDepartmentMappingDetailsSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False)
    class Meta:
        model = PosDepartmentMapping
        fields = ['department']

class PosSubdepartmentMappingDetailsSerializer(serializers.ModelSerializer):
    sub_department = SubDepartmentSerializer(many=False)
    class Meta:
        model = PosSubdepartmentMapping
        fields = ['sub_department']


class PosCompanyMappingDetailsSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False)
    class Meta:
        model = PosCompanyMapping
        fields = ['company']
        
        
class PosDetailSerializer(serializers.ModelSerializer):
    departments = PosDepartmentMappingDetailsSerializer(many=True)
    companies = PosCompanyMappingDetailsSerializer(many=True)
    billing_address = BrandAddressSerializer(many=False)
    shipping_address = BrandAddressSerializer(many=False)
    
    class Meta:
        model = POS
        fields = '__all__'
        
class PosDeprtmentMappingReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False)
    sub_department = serializers.SerializerMethodField()
    class Meta:
        model = PosDepartmentMapping
        fields = '__all__'
        
    def get_sub_department(self, obj):
        pos_sub_department = PosSubdepartmentMapping.objects.filter(pos=obj.pos, sub_department__parent_department=obj.department).all()
        
        return [{
            "sub_department_uid" : i.sub_department.sub_department_uid,
            "sub_department_name" : i.sub_department.sub_department_name,
            "sub_department_type" : i.sub_department.sub_department_type,
            "id" : i.sub_department.id,
            } for i in pos_sub_department]
        

#------- B2B Client Registration
class B2bClientBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = BtoBclient
        fields = ["id","client_code", "client_name", "city", "state", "contact_number", "email", "gstn"]


class B2bClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BtoBclient
        fields = '__all__'


class B2BclientBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BclientBankDetails
        fields = '__all__'
        
class B2BclientClusterMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = B2BclientClusterMapping
		fields = '__all__'


class B2BclientBrandMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = B2BclientBrandMapping
		fields = '__all__'


class B2BclientPOSMappingSerializer(serializers.ModelSerializer):
	class Meta:
		model = B2BclientPOSMapping
		fields = '__all__'

class B2BClientReadSerializer(serializers.ModelSerializer):
	bank_details = serializers.SerializerMethodField()

	class Meta:
		model = BtoBclient
		fields = '__all__'
	
	def get_bank_details(self, obj):
		return B2BclientBankDetailsSerializer(B2BclientBankDetails.objects.filter(client=obj.id).all(), many=True).data

class B2BRatesDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BRatesDefinition
        fields = '__all__'
        


#-------- Store Serializer
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        
        
class StoreEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreEmployee
        fields = '__all__'
        

class StoreClusterMappingSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = StoreClusterMapping
        fields = '__all__'
        
class StoreBrandMappingSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = StoreBrandMapping
        fields = '__all__'

class StorePosMappingSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = StorePosMapping
        fields = '__all__'
        
#---------STore Read

class StoreBrandMappingReadSeriaizer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False)
    class Meta:
        model = StoreBrandMapping
        fields = '__all__'
                
class StoreClusterMappingReadSeriaizer(serializers.ModelSerializer):
    cluster = ClusterSerializer(many=False)
    class Meta:
        model = StoreClusterMapping
        fields = '__all__'
        
class StoreEmployeeReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = StoreEmployee
        fields = '__all__'


class StoreDetailSerializer(serializers.ModelSerializer):
    employees = StoreEmployeeReadSerializer(many=True, read_only=True)
    cluster = StoreClusterMappingReadSeriaizer(many=True, read_only=True)
    brand = StoreBrandMappingReadSeriaizer(many=True)
    
    class Meta:
        model = Store
        fields = '__all__'

#------- HSN code serializer
class HSNcodeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSNcodeTags
        fields = "__all__"

class HSNtaxInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSNtaxInformation
        fields = '__all__'
        
class HSNtaxInformationReadSerializer(serializers.ModelSerializer):
    hsn_code_tags = HSNcodeTagSerializer(read_only=True, many=True)
    class Meta:
        model = HSNtaxInformation
        fields = '__all__'
        
#--------Material Serializer
class RawMaterialRegistrationBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialRegistrationModel
        # fields = [
        #             "id",
        #             "item_code",
        #             "item_name",
        #             "default_uom",
        #             "tax",
        #             "category",
        #             "sub_category",
        #             "rate",
        #             "price",
        #             "recipe_unit",
        #             "recipe_rate",
        #             "recipe_price",
        #             "life_cycle",
        #             "expiry_date",
        #             "available_for_cluster",
        # ]
        fields = '__all__'
        
class RawMaterialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialRegistrationModel
        fields = '__all__'


class RawMaterialTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialTags
        fields = '__all__'


class RawMaterialAliaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialAliases
        fields = '__all__'
        
class VendorPricingRawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPricingRawMaterial
        fields = '__all__'
        
class VendorPricingUpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPricingUpdateLog
        fields = '__all__'

class RawMaterialPosMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialPosMapping
        fields = '__all__'
        
        
class RawMaterialDeptMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialDeptMapping
        fields = '__all__'


class RawMaterialPosMapReadSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    raw_material = RawMaterialRegistrationBriefSerializer(many=False)
    class Meta:
        model = RawMaterialPosMapping
        fields = '__all__'
        
        
class RawMaterialDeptMappingReadSerializer(serializers.ModelSerializer):
    department = DepartmentBriefSerializer(many=False)
    raw_material = RawMaterialRegistrationBriefSerializer(many=False)
    class Meta:
        model = RawMaterialDeptMapping
        fields = '__all__'


class VendorPricingRawMaterialReadSerializer(serializers.ModelSerializer):
    vendor = VendorBriefSerializer(read_only=True, many=False)
    class Meta:
        model = VendorPricingRawMaterial
        fields = '__all__'


class RawMaterialPosMapReadBriefSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    class Meta:
        model = RawMaterialPosMapping
        fields = ['pos']
        
        
class RawMaterialDeptMapReadBriefSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False)
    class Meta:
        model = RawMaterialDeptMapping
        fields = ['department']
        
class RawMaterialRegistrationReadSerializer(serializers.ModelSerializer):
    pos = RawMaterialPosMapReadBriefSerializer(many=True)
    departments = RawMaterialDeptMapReadBriefSerializer(many=True)
    raw_material_tags = RawMaterialTagSerializer(many=True)
    raw_material_alias = RawMaterialAliaseSerializer(many=True)
    
    class Meta:
        model = RawMaterialRegistrationModel
        fields = '__all__'        
        
class RawMaterialUomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialUomModel
        fields = '__all__'
        
#-------------- Semi Product
class SemiProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiProductRegistrationModel
        # fields = ["id","item_code","item_name","default_uom","category","sub_category","recipe_unit","food_cost","life_cycle", "production_department", "yield_quantity", "yield_quantity_cost"]
        fields = '__all__'
        
class SemiProductRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiProductRegistrationModel
        fields = '__all__'


class SemiProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiProductTags
        fields = '__all__'
        
class SemiProductPosMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiProductPosMapping
        fields = '__all__'
        
        
class SemiProductDeptMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiProductDeptMapping
        fields = '__all__'
        
        
class SemiProductPosMappingDetailSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    class Meta:
        model = SemiProductPosMapping
        fields = ['pos']
        
        
class SemiProductDeptMappingDetailSerializer(serializers.ModelSerializer):
    department = DepartmentBriefSerializer(many=False)
    class Meta:
        model = SemiProductDeptMapping
        fields = ['department']
        
class SemiProductRegistrationReadSerializer(serializers.ModelSerializer):
    semi_product_tags = SemiProductTagSerializer(many=True)
    pos = SemiProductPosMappingDetailSerializer(many=True, read_only=True)
    departments = SemiProductDeptMappingDetailSerializer(many=True, read_only=True)
    production_department = DepartmentBriefSerializer(many=False)
    cost_center_department = DepartmentBriefSerializer(many=False)
    class Meta:
        model = SemiProductRegistrationModel
        fields = '__all__'



class SemiProductPosMapReadSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    semi_product = SemiProductBriefSerializer(many=False)
    class Meta:
        model = SemiProductPosMapping
        fields = '__all__'
        
        
class SemiProductDeptMappingReadSerializer(serializers.ModelSerializer):
    department = DepartmentBriefSerializer(many=False)
    semi_product = SemiProductBriefSerializer(many=False)
    class Meta:
        model = SemiProductDeptMapping
        fields = '__all__'
        
#----------- Final Product
class FinalProductBriefReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProductRegistrationModel
        fields = [
			"id",
			"item_code",
			"item_name",
            "default_uom_quantity",
			"default_uom",
			"production_cycle",
			"category",
			"sub_category",
		]
        
class FinalProductRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProductRegistrationModel
        fields ='__all__'


class FinalProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProductTags
        fields = '__all__'


class FinalProductSellingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProductSellingPrice
        fields = '__all__'


class FinalProductPriceForPOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalProductPriceForPOS
        fields = '__all__'
        
class FinalProductRegistrationReadSerializer(serializers.ModelSerializer):
    final_product_tags = FinalProductTagSerializer(read_only=True, many=True)
    production_department = DepartmentBriefSerializer(many=False)
    cost_center_department = DepartmentBriefSerializer(many=False)
    final_product_pricing = FinalProductSellingPriceSerializer(many=True)
    price_for_pos = FinalProductPriceForPOSSerializer(many=True)
    class Meta:
        model = FinalProductRegistrationModel
        fields ='__all__'



        
class B2BRatesDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BRatesDefinition
        fields = '__all__'


class B2bRatesDefinitionReadSerializer(serializers.ModelSerializer):
    b2b_client = B2bClientBriefSerializer(read_only=True, many=False)
    final_product = FinalProductBriefReadSerializer(read_only=True, many=False)
    class Meta:
        model = B2BRatesDefinition
        fields = '__all__'





class FinalProductPriceForPOSReadSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    final_product = FinalProductBriefReadSerializer(many=False)
    class Meta:
        model = FinalProductPriceForPOS
        fields = '__all__'
        
#----------Service material
class AssetInvetoryRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInvetoryRegistrationModel
        fields = '__all__'
        
        
class AssetInvetoryPosMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInvetoryPosMapping
        fields = '__all__'
        
        
class AssetInvetoryDeptMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInvetoryDeptMapping
        fields = '__all__'
        
class AssetInvetoryPosMapReadSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    class Meta:
        model = AssetInvetoryPosMapping
        fields = ['pos']
        
        
class AssetInvetoryDeptMapReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False)
    class Meta:
        model = AssetInvetoryDeptMapping
        fields = ['department']
        
class AssetInvetoryRegistrationReadSerializer(serializers.ModelSerializer):
    pos = AssetInvetoryPosMapReadSerializer(many=True)
    departments = AssetInvetoryDeptMapReadSerializer(many=True)
    
    class Meta:
        model = AssetInvetoryRegistrationModel
        fields = '__all__'  
        
#-------Default Variable Charges

class DefaultVariableChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultVariableCharges
        fields = '__all__'
        
#------- Recipe Registration
class RecipeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeRegistration
        fields = '__all__'


class RecipeVariableChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeVariableCharges
        fields = '__all__'


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredients
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    raw_material = RawMaterialRegistrationBriefSerializer(many=False)
    semi_product = SemiProductBriefSerializer(many=False)
    class Meta:
        model = RecipeIngredients
        fields = '__all__'
        
class RecipePackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipePackaging
        fields = '__all__'
        
class RecipeRegistrationReadSerializer(serializers.ModelSerializer):
    recipe_variable_charges = RecipeVariableChargeSerializer(many=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    recipe_packaging = RecipePackagingSerializer(many=True)
    class Meta:
        model = RecipeRegistration
        fields = '__all__'
        
        
#--------PO PLAN 

class PoPlanningTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoPlanningTemplates
        fields = '__all__'

class PoPlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoPlanning
        fields = '__all__'


class PlanningMaterialDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningMaterialDistribution
        fields = '__all__'
        
class PoPlanningMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoPlanningMaterial
        fields = '__all__'
        
class PoPlanningMaterialReadSerializer(serializers.ModelSerializer):
    planning_material_distribution_reference = PlanningMaterialDistributionSerializer(many=True)
    class Meta:
        model = PoPlanningMaterial
        fields = '__all__'
        
class PoPlanningReadSerializer(serializers.ModelSerializer):
    po_plan_material = PoPlanningMaterialReadSerializer(many=True)
    class Meta:
        model = PoPlanning
        fields = '__all__'


class UnplannedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnplannedItems
        fields = '__all__'
        
#------PO 

class PoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoModel
        fields = '__all__'
        
class PoItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoItems
        fields = '__all__'
        


class PoReadSerializer(serializers.ModelSerializer):
    po_items = PoItemsSerializer(many=True)
    class Meta:
        model = PoModel
        fields = '__all__'


#------Purchased Order

class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = '__all__'
        

class PurchasedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItems
        fields = '__all__'
        


class PurchasedOrderReadSerializer(serializers.ModelSerializer):
    purchased_items = PurchasedItemSerializer(many=True)
    class Meta:
        model = Purchased
        fields = '__all__'
        
#---PeriodicAutomaticReplacement

class PeriodicAutomaticReplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicAutomaticReplacement
        fields = '__all__'
        
class PeriodicAutomaticReplacementReadSerializer(serializers.ModelSerializer):
    pos = PosBriefSerializer(many=False)
    department = DepartmentBriefSerializer(many=False)
    final_product = FinalProductBriefReadSerializer(many=False)
    semi_product = SemiProductBriefSerializer(many=False)
    raw_material = RawMaterialRegistrationBriefSerializer(many=False)
    class Meta:
        model = PeriodicAutomaticReplacement
        fields = '__all__'
        
        
#-------Store Issue
class StoreIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreIssue
        fields = '__all__'
        
class StoreIssueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreIssueItems
        fields = '__all__'

class StoreIssueReadSerializer(serializers.ModelSerializer):
    store_issue_materials = StoreIssueItemSerializer(many=True)
    # child_store = StoreSerializer(many=False)
    to_pos = PosBriefSerializer(many=False)
    to_department = DepartmentBriefSerializer(many=False)
    parent_store = StoreSerializer(many=False)
    requested_by = UserSerializer(many=False)
    issued_by = UserSerializer(many=False)
    class Meta:
        model = StoreIssue
        fields = "__all__"



#--------StockTransfer
class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = '__all__'


class StockTransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransferItems
        fields = '__all__'


class StockTransferItemReadSerializer(serializers.ModelSerializer):
    final_product = FinalProductBriefReadSerializer(many=False)
    semi_product = SemiProductBriefSerializer(many=False)
    raw_material = RawMaterialRegistrationBriefSerializer(many=False)
    class Meta:
        model = StockTransferItems
        fields = '__all__'


class StockTransferReadSerializer(serializers.ModelSerializer):
    stock_transfer_materials = StockTransferItemReadSerializer(many=True)
    from_pos = PosBriefSerializer(many=False)
    to_pos = PosBriefSerializer(many=False)
    from_department = DepartmentBriefSerializer(many=False)
    to_department = DepartmentBriefSerializer(many=False)
    transfered_by = UserSerializer(many=False)
    received_by = UserSerializer(many=False)
    
    class Meta:
        model = StockTransfer
        fields = '__all__'
        
        
#--------------- ORDER SHEET

class OrderSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSheet
        fields = '__all__'
        
class OrderSheetBriefReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSheet
        fields = ["from_b2b_client",  "from_pos",  "from_department",  "custom_order",  "status",  "order_sheet_id",  "delivery_date",  "submitted",  "submitted_on",  "created_date"]
        
class OrderSheetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSheetItems
        fields = '__all__'
        
class OrderSheetItemBriefReadSerializer(serializers.ModelSerializer):
    order_sheet = OrderSheetBriefReadSerializer(many=False)
    class Meta:
        model = OrderSheetItems
        fields = '__all__'

class OrderSheetReadSerializer(serializers.ModelSerializer):
    order_sheet_materials = OrderSheetItemSerializer(many=True)
    from_b2b_client = B2bClientSerializer(many=False)
    from_pos = PosBriefSerializer(many=False)
    from_department = DepartmentBriefSerializer(many=False)
    issued_by = UserSerializer(many=False)
    to_pos = PosBriefSerializer(many=False)
    to_department = DepartmentBriefSerializer(many=False)
    created_by = UserSerializer(many=False)
    issued_by = UserSerializer(many=False)
    received_by = UserSerializer(many=False)
    
    class Meta:
        model = OrderSheet
        fields = "__all__"
