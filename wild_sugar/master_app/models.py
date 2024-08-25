from django.db import models

from django.contrib.auth import get_user_model

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


User = get_user_model()

# Create your models here.

# constant
class CompanyTypes(models.Model):
    '''
        Model to store company types
    '''
    company_type = models.CharField(max_length=100, null=False, blank=False)
    company_type_description = models.CharField(max_length=250, null=True, blank=False)

    def __str__(self):
        return self.company_type

    class Meta:
        app_label = 'master_app'
        db_table = 'company_types'
        indexes = []


# constant
class EmploymentTypes(models.Model):
    '''
        Model to store Employment types
    '''
    employment_type = models.CharField(max_length=100, null=False, blank=False)
    employment_type_description = models.CharField(max_length=250, null=True, blank=False)

    class Meta:
        app_label = 'master_app'
        db_table = 'employment_types'
        indexes = []
    
    def __str__(self):
        return self.employment_type

# constant
class IndustryTypes(models.Model):
    '''
        Model to store Industry Types
    '''
    industry_type = models.CharField(max_length=50, null=False, blank=False)
    industry_type_description = models.CharField(max_length=500, null=True, blank=True)
    

    class Meta:
        app_label = 'master_app'
        db_table = 'industry_type'





#--------- Master-Data App related

class Brand(models.Model):
    brand_name = models.CharField(max_length=250, null=False, blank=False)
    industry_type = models.CharField(max_length=50, null=True, blank=True)
    required_sub_department = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'brand'


class BrandAddress(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_address')
    short_name = models.CharField(max_length=100, null=True)
    address = models.JSONField(null=False)
    address_type = models.CharField(max_length=20)
    use_for_all = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'brand_address'
    

class UserBrandMapping(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='brands')
    brand = models.ForeignKey(Brand, null=False, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'user_brand_mapping'
        unique_together = ('user', 'brand')


#----- Brand Level Static Data

# Brand level
class DepartmentTypes(models.Model):
    '''
        Model to store department types
    '''
    department_type = models.CharField(max_length=100, null=False, blank=False)
    department_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'department_types'
        indexes = []
    
    def __str__(self):
        return self.department_type
    
class StoreTypes(models.Model):
    '''
        Model to store store types
    '''
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    store_types = models.CharField(max_length=50, null=False, blank=False)
    store_type_description = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        app_label = 'master_app'
        db_table = 'store_type'

# brand level
class PosTypes(models.Model):
    '''
        Model to store POS types
    '''
    pos_type = models.CharField(max_length=100, null=False, blank=False)
    pos_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'pos_types'
        indexes = []
    
    def __str__(self):
        return self.pos_type


# brand level
class VendorTypes(models.Model):
    '''
        Model to store Vendor types
    '''
    vendor_type = models.CharField(max_length=100, null=False, blank=False)
    vendor_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_types'
        indexes = []
    
    def __str__(self):
        return self.vendor_type


#brand level
class ProductTypes(models.Model):
    '''
        Model to store Product types
    '''
    product_type = models.CharField(max_length=100, null=False, blank=False)
    product_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'product_types'
        indexes = []
    
    def __str__(self):
        return self.product_type


# brand level
class PrioritiyTypes(models.Model):
    '''
        Model to store Prioritie types
    '''
    priority_type = models.CharField(max_length=100, null=False, blank=False)
    priority_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'priority_types'
        indexes = []
    
    def __str__(self):
        return self.priority_type

# brand
class SeverityTypes(models.Model):
    '''
        Model to store Severity types
    '''
    severity_type = models.CharField(max_length=100, null=False, blank=False)
    severity_type_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'severity_types'
        indexes = []
    
    def __str__(self):
        return self.severity_type +' : '+self.severity_type_description

# brand
class HighValueItemTypes(models.Model):
    '''
        Model to store High Value Item types
    '''
    high_value_item_type = models.CharField(max_length=100, null=False, blank=False)
    high_value_item_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'high_value_item_types'
        indexes = []
    
    def __str__(self):
        return self.high_value_item_type

# brand
class UnitOfMeasurement(models.Model):
    '''
        Unit of measurments
    '''
    unit_name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    unit_description = models.CharField(max_length=250, null=True, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'unit_of_measurments'
    
    def __str__(self):
        return self.unit_name


class UnitOfMeasurementConversion(models.Model):
    source_unit = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE, null=False, related_name='source_unit_conversion')
    convert_to_unit = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE, null=False, related_name='convert_to_unit_conversion')
    source_unit_quantity = models.FloatField(null=False)
    convert_to_unit_quantity = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'unit_of_measurment_conversion'
        # unique
    
    def __str__(self):
        return self.source_unit.unit_name + '->' + self.convert_to_unit.unit_name

# brand
class CategoryList(models.Model):
    '''
        Model to store category
    '''
    category_name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    category_type = models.CharField(max_length=250, null=False, blank=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'category_list'


#brand 
class SubcategoryList(models.Model):
    '''
        Model to store category
    '''
    sub_category_name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    sub_category_type = models.CharField(max_length=250, null=False, blank=False)
    categories = models.ManyToManyField(CategoryList, related_name="sub_categories", blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'sub_category_list'


class AssetTypes(models.Model):
    asset_type = models.CharField(max_length=100, null=False)
    asset_type_description = models.CharField(max_length=240, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'asset_type_list'

class Clusters(models.Model):
    cluster_code = models.CharField(max_length=12, null=True, blank=False)
    cluster_name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'clusters'
    
    
@receiver(post_save, sender=Clusters)
def clusters_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = Clusters.objects.filter(id=instance.id).first()
        if dept:
            if not dept.cluster_code:
                dept.cluster_code = 'CLUSTER'+str(dept.id).zfill(3)
                dept.save() 


class ClusterAddress(models.Model):
    # brand
    cluster = models.ForeignKey(Clusters, null=False, on_delete=models.CASCADE, related_name='cluster_address')
    short_name = models.CharField(max_length=100, null=True)
    address = models.JSONField(null=False)
    address_type = models.CharField(max_length=20)
    use_for_all = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'cluster_address'
        

class BrandClusterMapping(models.Model):
    brand = models.ForeignKey(Brand, null=False, on_delete=models.CASCADE, related_name='clusters')
    cluster = models.ForeignKey(Clusters, null=False, on_delete=models.CASCADE, related_name='brands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'brand_cluster_mapping'
        unique_together = ('cluster', 'brand')  




class Company(models.Model):
    company_name = models.CharField(max_length=250, null=False, blank=False)
    company_type = models.CharField(max_length=100, null=False, blank=False)
    # address_line_1 = models.CharField(max_length=100, null=True, blank=False)
    # address_line_2 = models.CharField(max_length=100, null=True, blank=False)
    # landmark = models.CharField(max_length=100, null=True, blank=False)
    # city = models.CharField(max_length=100, null=True, blank=False)
    # state = models.CharField(max_length=100, null=True, blank=False)
    gstn = models.CharField(max_length=250, null=True, blank=False)
    pan = models.CharField(max_length=20, null=True, blank=False)
    number_of_shareholder = models.IntegerField(default=0)
    purchase_email = models.EmailField(max_length=250, null=True, blank=False)
    purchase_contact_number = models.CharField(max_length=20, null=True, blank=False)
    accounts_email = models.EmailField(max_length=250, null=True, blank=False)
    accounts_contact_number = models.CharField(max_length=20, null=True, blank=False)
    udyam_number = models.CharField(max_length=240, null=True)
    is_msme_registered = models.BooleanField(default=False)
    msme_registration_number = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'company'


class CompanyAddress(models.Model):
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE, related_name='company_address')
    # address = models.JSONField(null=False)
    # short_name = models.CharField(max_length=100, null=True)
    # address_type = models.CharField(max_length=20)
    address = models.ForeignKey(BrandAddress, null=True, on_delete=models.SET_NULL, related_name='brand_company_address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'company_address'

class CompanyShareholder(models.Model):
    # percentage
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE, related_name='shareholder')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='company')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'company_user_mapping'
        unique_together = ('user', 'company')


class CompanyCluserMapping(models.Model):
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE, related_name='cluster')
    cluster = models.ForeignKey(Clusters, null=False, on_delete=models.CASCADE, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'company_cluster_mapping'
        unique_together = ('cluster', 'company')  


class CompanyBrandMapping(models.Model):
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE, related_name='brand')
    brand = models.ForeignKey(Brand, null=False, on_delete=models.CASCADE, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'company_brand_mapping'
        unique_together = ('brand', 'company')  


class CompanyDocuments(models.Model):
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE, related_name='documents')
    document_key = models.CharField(max_length=250, null=False, blank=False)
    document_url = models.TextField(null=True)
    document_name = models.CharField(max_length=250, null=True, blank=False)
    document_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'company_document'



class Department(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    department_uid = models.CharField(max_length=20, null=True)
    department_name = models.CharField(max_length=250, null=False, blank=False)
    department_type = models.CharField(max_length=250, null=True, blank=False)
    target_food_cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'department'


@receiver(post_save, sender=Department)
def department_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = Department.objects.filter(id=instance.id).first()
        if dept:
            if not dept.department_uid:
                dept.department_uid = 'DP'+str(dept.id).zfill(3)
                dept.save() 


class SubDepartment(models.Model):
    parent_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='sub_departments')
    sub_department_uid = models.CharField(max_length=20, null=False, blank=False)
    sub_department_name = models.CharField(max_length=250, null=False, blank=False)
    sub_department_type = models.CharField(max_length=250, null=True, blank=False)
    target_food_cost = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'sub_department'


@receiver(post_save, sender=SubDepartment)
def subdepartment_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = SubDepartment.objects.filter(id=instance.id).first()
        if dept:
            if not dept.sub_department_uid:
                dept.sub_department_uid = 'SUBDP'+str(dept.id).zfill(3)
                dept.save() 


class DepartmentClusterMapping(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='cluster')
    cluster = models.ForeignKey(Clusters, on_delete=models.CASCADE, related_name='departments')
    food_cost = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'department_cluster_mapping'


# class DepartmentBrandMapping(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='brand')
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='departments')
#     food_cost = models.FloatField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         app_label = 'master_app'
#         db_table = 'department_brand_mapping'
    

#----------- POS
class POS(models.Model):
    pos_code = models.CharField(max_length=50, null=True, blank=False)
    pos_name = models.CharField(max_length=100, null=False, blank=False)
    pos_type = models.CharField(max_length=100, null=False, blank=False)
    # address = models.TextField(null=True)
    contact_number = models.CharField(max_length=20, null=True, blank=False)
    email = models.EmailField(max_length=250, null=True, blank=False)
    cluster = models.ForeignKey(Clusters, on_delete=models.SET_NULL, related_name='pos', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    billing_address = models.ForeignKey(BrandAddress, on_delete=models.SET_NULL, null=True, related_name='brand_pos_billing_address')
    shipping_address = models.ForeignKey(BrandAddress, on_delete=models.SET_NULL, null=True, related_name='brand_pos_shipping_address')

    class Meta:
        app_label = 'master_app'
        db_table = 'pos'


@receiver(post_save, sender=POS)
def pos_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = POS.objects.filter(id=instance.id).first()
        if dept:
            if not dept.pos_code:
                dept.pos_code = 'POS'+str(dept.id).zfill(3)
                dept.save() 

class PosDepartmentMapping(models.Model):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='pos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('pos', 'department')  
        app_label = 'master_app'
        db_table = 'pos_department_mapping'

class PosSubdepartmentMapping(models.Model):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='sub_departments')
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, related_name='pos')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pos', 'sub_department')  
        app_label = 'master_app'
        db_table = 'pos_sub_department_mapping'
        

class PosCompanyMapping(models.Model):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='pos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('pos', 'company')
        app_label = 'master_app'
        db_table = 'pos_company_mapping'


# POS Code
# POS Name
# POS Type - Cafe, Kiosk, Central Kitchen, Wholesale
# Company
# Cluster Mapping
# Address
# Department Mapping
# Contact No
# Email ID

#----------- Vendor
class Vendors(models.Model):
    vendor_code = models.CharField(max_length=50, null=True, blank=False)
    vendor_name = models.CharField(max_length=250, null=False, blank=False)
    address_line_1 = models.TextField(null=True)
    address_line_2 = models.TextField(True)
    landmark = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=250, null=True)
    pan = models.CharField(max_length=20, null=True)
    gstn = models.CharField(max_length=50, null=True)
    vendor_type = models.CharField(max_length=100, null=True)
    credit_period = models.FloatField(default=0)
    udyam_number = models.CharField(max_length=240, null=True)
    is_msme_registered = models.BooleanField(default=False)
    msme_registration_number = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendors'


@receiver(post_save, sender=Vendors)
def vendors_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = Vendors.objects.filter(id=instance.id).first()
        if dept:
            if not dept.vendor_code:
                dept.vendor_code = 'VENDOR'+str(dept.id).zfill(3)
                dept.save() 


class VendorBankDetails(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=240, null=True)
    account_name = models.CharField(max_length=240, null=True)
    account_number = models.CharField(max_length=240,null=True)
    ifsc = models.CharField(max_length=50, null=True)
    branch = models.CharField(max_length=240, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_bank_details'


class VendorDocuments(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='documents')
    document_key = models.CharField(max_length=250, null=False, blank=False)
    document_url = models.TextField(null=True)
    document_name = models.CharField(max_length=250, null=True, blank=False)
    document_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_documents'


class VendorbankDocuments(models.Model):
    vendor_bank = models.ForeignKey(VendorBankDetails, related_name='documents', on_delete=models.CASCADE)
    vendor_document = models.ForeignKey(VendorDocuments, related_name='bank', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_bank_documents'


class VendorClusterMapping(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='clusters')
    cluster = models.ForeignKey(Clusters, on_delete=models.CASCADE, related_name='vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_cluster_mapping'


class VendorBrandMapping(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='brands')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_brand_mapping'


class VendorPOSMapping(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_pos_mapping'


#--------- B2B client

class BtoBclient(models.Model):
    client_code = models.CharField(max_length=50, null=True, blank=False)
    client_name = models.CharField(max_length=250, null=False, blank=False)
    address_line_1 = models.TextField(null=True)
    address_line_2 = models.TextField(True)
    landmark = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=250, null=True)
    pan = models.CharField(max_length=20, null=True)
    gstn = models.CharField(max_length=50, null=True)
    billing_type = models.CharField(max_length=20, default='gst')
    credit_period_days = models.IntegerField(default=0)
    credit_period_date = models.DateField(null=True)
    udyam_number = models.CharField(max_length=240, null=True)
    is_msme_registered = models.BooleanField(default=False)
    msme_registration_number = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'b2b_client'
    

@receiver(post_save, sender=BtoBclient)
def b2b_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        final_prod = BtoBclient.objects.filter(id=instance.id).first()
        if final_prod:
            if not final_prod.client_code:
                final_prod.client_code = 'B2B'+str(final_prod.id).zfill(3)
                final_prod.save() 


class B2BclientBankDetails(models.Model):
    client = models.ForeignKey(BtoBclient, on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=240, null=True)
    account_name = models.CharField(max_length=240, null=True)
    account_number = models.CharField(max_length=240, unique=True,null=True)
    ifsc = models.CharField(max_length=50, null=True)
    branch = models.CharField(max_length=240, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'b2b_client_bank_details'



class B2BclientClusterMapping(models.Model):
    client = models.ForeignKey(BtoBclient, on_delete=models.CASCADE, related_name='clusters')
    cluster = models.ForeignKey(Clusters, on_delete=models.CASCADE, related_name='client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'client_cluster_mapping'


class B2BclientBrandMapping(models.Model):
    client = models.ForeignKey(BtoBclient, on_delete=models.CASCADE, related_name='brands')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'client_brand_mapping'


class B2BclientPOSMapping(models.Model):
    client = models.ForeignKey(BtoBclient, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='client')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'client_pos_mapping'
        


#----- Store
class Store(models.Model):
    store_uid = models.CharField(max_length=50, null=True, blank=False)
    store_type = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store'


@receiver(post_save, sender=Store)
def store_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        dept = Store.objects.filter(id=instance.id).first()
        if dept:
            if not dept.store_uid:
                dept.store_uid = 'STORE'+str(dept.id).zfill(3)
                dept.save() 

class StoreEmployee(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='employees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_employees'


class StoreClusterMapping(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='cluster')
    cluster = models.ForeignKey(Clusters, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_cluster_mapping'
        
class StoreBrandMapping(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='brand')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_brand_mapping'


class StorePosMapping(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_pos_mapping'
        
        
#------- HSN with Tax rates
class HSNtaxInformation(models.Model):
    '''
    HSN tax information
    '''
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_hsn_codes')
    hsn_code = models.CharField(max_length=240, null=False, blank=False)
    hsn_code_description = models.TextField(null=True)
    cgst = models.FloatField(default=0)
    sgst = models.FloatField(default=0)
    igst = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'hsn_codes'
    

class HSNcodeTags(models.Model):
    '''
    HSN code tags
    '''
    hsn = models.ForeignKey(HSNtaxInformation, related_name='hsn_code_tags', on_delete=models.CASCADE)
    tag = models.CharField(max_length=240, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'hsn_code_tags'
    


#------- Raw Material
class RawMaterialRegistrationModel(models.Model):
    '''
        model to store raw material
    '''
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brand_raw_material')
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    default_uom_quantity = models.FloatField(null=False, default=0) #newly
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    production = models.BooleanField(default=True)
    tax = models.FloatField(null=True)
    hsn_code = models.CharField(max_length=50, null=True, blank=False)
    category = models.CharField(max_length=50, null=True)
    sub_category = models.CharField(max_length=50, null=True)
    rate = models.FloatField(default=0)
    price = models.FloatField(default=0)
    recipe_unit = models.CharField(max_length=50, null=True)
    flag_recipe_conversion_ratio = models.BooleanField(default=True) # variable
    recipe_conversion_ratio = models.FloatField(null=True)
    recipe_rate = models.FloatField(default=0)
    recipe_price = models.FloatField(default=0)
    direct_selling = models.BooleanField(default=False)
    life_cycle = models.FloatField(null=True)
    expiry_date = models.DateField(null=True)
    high_value_item = models.BooleanField(null=True) # True/False
    priority = models.CharField(max_length=50, null=True)
    severity = models.CharField(max_length=50, null=True)
    available_for_cluster = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    consumable = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_registration'


@receiver(post_save, sender=RawMaterialRegistrationModel)
def rm_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        raw_mat = RawMaterialRegistrationModel.objects.filter(id=instance.id).first()
        if raw_mat:
            if not raw_mat.item_code:
                raw_mat.item_code = 'RM'+str(raw_mat.id).zfill(3)
                raw_mat.save() 
        
class RawMaterialTags(models.Model):
    tag = models.CharField(max_length=140, null=False)
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='raw_material_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_tags'


class RawMaterialAliases(models.Model):
    alias = models.CharField(max_length=240, null=False)
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='raw_material_alias')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_alias'


class VendorPricingRawMaterial(models.Model):
    vendor = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name='raw_material_pricing')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='vendors')
    rate = models.FloatField(default=0)
    price = models.FloatField(default=0)
    latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_raw_material_pricing'


class VendorPricingUpdateLog(models.Model):
    vendor_pricing = models.ForeignKey(VendorPricingRawMaterial, on_delete=models.CASCADE, related_name='pricing_log')
    old_value = models.JSONField(null=True)
    new_value = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'vendor_raw_material_pricing_log'
    


class RawMaterialPosMapping(models.Model):
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='raw_material')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_pos_mapping'
        unique_together = ('raw_material', 'pos')
        
class RawMaterialDeptMapping(models.Model):
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='raw_material')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_dept_mapping'
        unique_together = ('raw_material', 'department')
        
class RawMaterialUomModel(models.Model):
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, on_delete=models.CASCADE, related_name='raw_materials_uom')
    quantity = models.FloatField(null=False) #user defined
    uom = models.CharField(max_length = 20, null=False) #user defined
    recipe_conversion_ratio = models.CharField(max_length=20, null=False) #user defined
    recipe_unit = models.CharField(max_length=20, null=False) #from RM
    defalt_uom_quantity = models.FloatField(null=False) #from RM
    default_uom = models.CharField(max_length=20, null=False)
    new_uom_quantity = models.FloatField(null=False)
    new_uom = models.CharField(max_length=20)
    new_uom_to_default_uom_ratio = models.FloatField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'raw_material_uoms'
    
    
    
    
    
        
class SemiProductRegistrationModel(models.Model):
    '''
        model to store semi product
    '''
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brand_semi_product')
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    default_uom_quantity = models.FloatField(null=False, default=0) #newly
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    production_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='production_department_sm')
    category = models.CharField(max_length=50, null=True)
    sub_category = models.CharField(max_length=50, null=True)
    recipe_unit = models.CharField(max_length=50, null=True)
    cost_center_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='cost_center_department_sm')
    life_cycle = models.FloatField(null=True)
    expiry_date = models.DateField(null=True)
    high_value_item = models.BooleanField(null=True)
    priority = models.CharField(max_length=50, null=True)
    severity = models.CharField(max_length=50, null=True)
    available_for_cluster = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    yield_quantity = models.FloatField(null=True)
    yield_value = models.FloatField(null=True)
    food_cost = models.FloatField(null=True)
    packaging_cost = models.FloatField(null=True)
    variable_cost = models.FloatField(null=True)
    
    # food_cost / yeis
    
    class Meta:
        app_label = 'master_app'
        db_table = 'semi_product_registration'


@receiver(post_save, sender=SemiProductRegistrationModel)
def sp_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        semi_prod = SemiProductRegistrationModel.objects.filter(id=instance.id).first()
        if semi_prod:
            if not semi_prod.item_code:
                semi_prod.item_code = 'SP'+str(semi_prod.id).zfill(3)
                semi_prod.save() 
        
class SemiProductTags(models.Model):
    tag = models.CharField(max_length=140, null=False)
    semi_product = models.ForeignKey(SemiProductRegistrationModel, on_delete=models.CASCADE, related_name='semi_product_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'semi_product_tags'


class SemiProductPosMapping(models.Model):
    semi_product = models.ForeignKey(SemiProductRegistrationModel, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='semi_product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'semi_product_pos_mapping'
        unique_together = ('semi_product', 'pos')
        
class SemiProductDeptMapping(models.Model):
    semi_product = models.ForeignKey(SemiProductRegistrationModel, on_delete=models.CASCADE, related_name='departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='semi_product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'semi_product_dept_mapping'
        unique_together = ('semi_product', 'department')
        
        
        
class FinalProductRegistrationModel(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brand_final_product')
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    default_uom_quantity = models.FloatField(null=False, default=0) #newly
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    production_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='production_department_fp')
    production_cycle = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True)
    sub_category = models.CharField(max_length=50, null=True)
    recipe_unit = models.CharField(max_length=50, null=True)
    cost_center_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='cost_center_department_fp')
    life_cycle = models.FloatField(null=True)
    expiry_date = models.DateField(null=True)
    high_value_item = models.BooleanField(null=True)
    priority = models.CharField(max_length=50, null=True)
    severity = models.CharField(max_length=50, null=True)
    available_for_cluster = models.BooleanField(default=False)
    ratail_tax = models.FloatField(null=True)
    b2b_tax = models.FloatField(null=True)
    hsn_code = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    yield_quantity = models.FloatField(null=True)
    yield_value = models.FloatField(null=True)
    food_cost = models.FloatField(null=True)
    packaging_cost = models.FloatField(null=True)
    variable_cost = models.FloatField(null=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'final_product_registration'


@receiver(post_save, sender=FinalProductRegistrationModel)
def fp_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        final_prod = FinalProductRegistrationModel.objects.filter(id=instance.id).first()
        if final_prod:
            if not final_prod.item_code:
                final_prod.item_code = 'FP'+str(final_prod.id).zfill(3)
                final_prod.save() 


class FinalProductTags(models.Model):
    tag = models.CharField(max_length=140, null=False)
    final_product = models.ForeignKey(FinalProductRegistrationModel, on_delete=models.CASCADE, related_name='final_product_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'final_product_tags'
    
        
class FinalProductSellingPrice(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='dept_final_product_price', null=True)
    pos = models.ForeignKey(POS, on_delete=models.SET_NULL, related_name='pos_final_product_price', null=True)
    b2b_client = models.ForeignKey(BtoBclient, on_delete=models.SET_NULL, related_name='b2b_final_product_price', null=True)
    final_product = models.ForeignKey(FinalProductRegistrationModel, on_delete=models.CASCADE, related_name='final_product_pricing')
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'final_product_selling_price'


class FinalProductPriceForPOS(models.Model):
    final_product = models.ForeignKey(FinalProductRegistrationModel, on_delete=models.CASCADE, related_name='price_for_pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='raw_material_prices')
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'final_product_price_pos'
        unique_together = ('final_product', 'pos')
    
    


class B2BRatesDefinition(models.Model):
    final_product = models.ForeignKey(FinalProductRegistrationModel, null=False, on_delete=models.CASCADE, related_name='b2b_rate_definition')
    b2b_client = models.ForeignKey(BtoBclient, null=False, on_delete=models.CASCADE, related_name='rates_definition')
    uom = models.CharField(max_length=50, null=True)
    rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'b2b_rates_definition'
        



class AssetInvetoryRegistrationModel(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brand_asset_inventory')
    asset_type = models.CharField(max_length=100, null=False)
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=50, null=True)
    sub_category = models.CharField(max_length=50, null=True)
    yield_quantity = models.FloatField(null=True)
    yield_quantity_cost = models.FloatField(null=True)
    life_cycle = models.FloatField(null=True)
    expiry_date = models.DateField(null=True)
    high_value_item = models.BooleanField(null=True)
    priority = models.CharField(max_length=50, null=True)
    severity = models.CharField(max_length=50, null=True)
    available_for_cluster = models.BooleanField(default=False)
    hsn_code = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'asset_inventory_registration'


@receiver(post_save, sender=AssetInvetoryRegistrationModel)
def asset_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        final_prod = AssetInvetoryRegistrationModel.objects.filter(id=instance.id).first()
        if final_prod:
            if not final_prod.item_code:
                final_prod.item_code = 'AS'+str(final_prod.id).zfill(3)
                final_prod.save() 
        
        
class AssetInvetoryPosMapping(models.Model):
    asset_inventory = models.ForeignKey(AssetInvetoryRegistrationModel, on_delete=models.CASCADE, related_name='pos')
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='asset_inventory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'asset_inventory_pos_mapping'
        unique_together = ('asset_inventory', 'pos')
        
class AssetInvetoryDeptMapping(models.Model):
    asset_inventory = models.ForeignKey(AssetInvetoryRegistrationModel, on_delete=models.CASCADE, related_name='departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='asset_inventory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'asset_inventory_dept_mapping'
        unique_together = ('asset_inventory', 'department')


#------- Recipe

class DefaultVariableCharges(models.Model):
    brand = models.ForeignKey(Brand, null=False, related_name='brand_default_variable_charges', on_delete=models.CASCADE)
    variable_charge_code = models.CharField(max_length=240, null=False)
    variable_charge = models.FloatField(null=False)
    variable_charge_description = models.CharField(max_length=240, null=False, blank=False)
    latest = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'default_variable_charges'
        # unique_together = ('brand', '')
        
    

class RecipeRegistration(models.Model):
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brand_recipe_registrations')
    final_product = models.ForeignKey(FinalProductRegistrationModel, on_delete=models.SET_NULL, related_name='final_product_recipe', null=True)
    semi_product = models.ForeignKey(SemiProductRegistrationModel, on_delete=models.SET_NULL, related_name='semi_product_recipe', null=True)
    item_name = models.CharField(max_length=240, null=False)    #Item Name - 
    item_code = models.CharField(max_length=240, null=False)     #Item Code - 
    recipe_entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='recipe_entered', null=True)     #Recipe Entered By - 
    recipe_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='recipe_aprroved', null=True)     #Recipe Approved By - 
    production_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='production_department_recipe')    #Production Department - 
    product_type = models.CharField(max_length=240, null=True)     #Product Type -
    recipe_unit = models.CharField(max_length=50, null=False)
    approved = models.BooleanField(default=False)
    approved_on = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    yield_quantity = models.FloatField(null=True)
    yield_value = models.FloatField(null=True)
    food_cost = models.FloatField(null=True)
    packaging_cost = models.FloatField(null=True)
    variable_cost = models.FloatField(null=True)
    ingredient_cost = models.FloatField(null=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'recipe_registration'
        


class RecipeVariableCharges(models.Model):
    recipe = models.ForeignKey(RecipeRegistration, on_delete=models.CASCADE, related_name='recipe_variable_charges')
    variable_charge_code = models.CharField(max_length=240, null=False)
    variable_charge = models.FloatField(null=False)
    variable_charge_description = models.CharField(max_length=240, null=False, blank=False)
    latest = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'recipe_variable_charges'
        
class RecipePackaging(models.Model):
    raw_material = models.ForeignKey(RawMaterialRegistrationModel,null=True ,on_delete=models.SET_NULL, related_name='raw_material_as_packging')
    recipe = models.ForeignKey(RecipeRegistration, on_delete=models.CASCADE, related_name='recipe_packaging')
    package_code = models.CharField(max_length=240, null=False)
    package_name = models.CharField(max_length=240, null=False)
    uom = models.CharField(max_length=20)
    quantity = models.FloatField(default=0)  #Ingredient Qty as per Recipe Unit
    price = models.FloatField(default=0) #Ingredient Price (auto fetch, as per ingredient name)
    value = models.FloatField(default=0)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'recipe_packaging'
    
class RecipeIngredients(models.Model):
    raw_material = models.ForeignKey(RawMaterialRegistrationModel,null=True ,on_delete=models.SET_NULL, related_name='raw_material_as_ingredient')
    semi_product = models.ForeignKey(SemiProductRegistrationModel,null=True , on_delete=models.SET_NULL, related_name='semi_product_as_ingredient')
    recipe = models.ForeignKey(RecipeRegistration, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient_code = models.CharField(max_length=240, null=False)
    ingredient_name = models.CharField(max_length=240, null=False)
    uom = models.CharField(max_length=20)
    quantity = models.FloatField(default=0)  #Ingredient Qty as per Recipe Unit
    price = models.FloatField(default=0) #Ingredient Price (auto fetch, as per ingredient name)
    value = models.FloatField(default=0) #Ingredient Value in the recipe (Price * Qty)
    yield_qauntity = models.FloatField(default=0) #Yield Qty
    remark = models.CharField(max_length=250, null=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'recipe_ingredients'
        
        
#----------PO PLANNING

class PoPlanningTemplates(models.Model):
    store = models.ForeignKey(Store, null=False, on_delete=models.CASCADE, related_name='store_po_planing_templates')
    template_name = models.CharField(max_length=240, null=False, blank=False)
    filters = models.JSONField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_planning_templates', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_planning_templates'

class PoPlanning(models.Model):
    store = models.ForeignKey(Store, null=False, on_delete=models.CASCADE, related_name='store_po_planing')
    po_planning_id = models.CharField(max_length=50, null=True, blank=False)
    consumption_date_from = models.DateField(null=True)
    consumption_date_to = models.DateField(null=True)
    planned_date_from = models.DateField(null=False)
    planned_date_to = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_planning_master'
        


@receiver(post_save, sender=PoPlanning)
def po_planning_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        po_plan = PoPlanning.objects.filter(id=instance.id).first()
        if po_plan:
            if not po_plan.po_planning_id:
                po_plan.po_planning_id = 'PO_PLAN'+str(po_plan.id).zfill(3)
                po_plan.save() 
		

class PoPlanningMaterial(models.Model):
    po_plan = models.ForeignKey(PoPlanning, null=False, on_delete=models.CASCADE, related_name='po_plan_material')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=True, related_name='raw_material_planning', on_delete= models.SET_NULL)
    vendor = models.ForeignKey(Vendors, null=True, related_name = 'vendor_planning', on_delete=models.SET_NULL)
    category = models.CharField(max_length=50, null=True)
    sub_category = models.CharField(max_length=50, null=True)
    consumable = models.BooleanField(default=True)
    high_value_item = models.BooleanField(default=False)
    planned = models.BooleanField(default=True)
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    default_uom_quantity = models.FloatField(null=False, default=0)
    current_stock_during_planning = models.FloatField(default=0)
    ideal_order_qauntity = models.FloatField(default=0) #calculate from cusumption date
    # planned_qauntity -> to add user defined quantity
    current_stock = models.FloatField(default=0)
    remark = models.CharField(max_length=240, null=True)
    request_add_new_qauntity = models.BooleanField(default=False)
    allowed_quantity = models.FloatField(null=True)
    total_allowed_quantity = models.FloatField(null=True)
    extra_allowed_quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)
    already_ordered_quantity = models.FloatField(default=0)
    balance_qauntity = models.FloatField(default=0)
    not_received_qty = models.FloatField(default=0)
    received_beyond_limit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_planning_material'
        
class PlanningMaterialDistribution(models.Model):
    store = models.ForeignKey(Store, null=False, on_delete=models.CASCADE, related_name='planning_material_distribution_store')
    planning_material_reference = models.ForeignKey(PoPlanningMaterial, null=False, on_delete=models.CASCADE, related_name='planning_material_distribution_reference')
    request_add_new_qauntity = models.BooleanField(default=False)
    allowed_quantity = models.FloatField(null=True)
    total_allowed_quantity = models.FloatField(null=True)
    extra_allowed_quantity = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_planning_material_distribution'
    
    

class UnplannedItems(models.Model):
    store = models.ForeignKey(Store, null=False, on_delete=models.CASCADE, related_name='store_po_planing_unplanned_items')
    item_code = models.CharField(max_length=20, null=True, blank=False)
    item_name = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_unplanned_items'
    
# --
# to avoid rework save planned unplanned items to mark

# some items we dont plan for that we create open PO

# all items in planning list by default when we start new plan


# -------
# already ordered - real time from bills
# balance quantity - real time

class PoModel(models.Model):
    store = models.ForeignKey(Store, null=False, on_delete=models.CASCADE, related_name='store_po')
    po_id = models.CharField(max_length=50, null=True, blank=False)
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateField(null=True)
    billing_address = models.JSONField(null=False)
    shipping_address = models.JSONField(null=False)
    remark = models.CharField(null=True, max_length=240)
    send_approval = models.BooleanField(default=False)
    auto_approved = models.BooleanField(default=False)
    manual_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='po_created')
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='po_aproved')
    status = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_model'
        
@receiver(post_save, sender=PoModel)
def po_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        po_plan = PoModel.objects.filter(id=instance.id).first()
        if po_plan:
            if not po_plan.po_id:
                po_plan.po_id = 'PO'+str(po_plan.id).zfill(3)
                po_plan.save() 
        

class PoItems(models.Model):
    po = models.ForeignKey(PoModel, on_delete=models.CASCADE, related_name='po_items')
    item_code = models.CharField(max_length=100, null=False)
    item_name = models.CharField(max_length=100, null=False)
    default_uom_quantity = models.FloatField(null=False, default=0) #newly
    default_uom = models.CharField(max_length=20, null=True, blank=True) #change to UOM
    uom = models.CharField(max_length=20, null=False)
    quantity = models.FloatField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'po_items'



class Purchased(models.Model):
    po_reference = models.ForeignKey(PoModel, on_delete=models.SET_NULL, null=True, related_name='po_purchased')
    purchase_grn = models.CharField(max_length=50, null=True)
    invoice_number = models.CharField(max_length=240, null=True)
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True, related_name='vendor_purchased')
    vendor_name = models.CharField(max_length=240, null=False, blank=False)
    address_line_1 = models.TextField(null=True)
    address_line_2 = models.TextField(True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=20, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    grn_timestamp = models.DateTimeField(auto_now=True) #last modified time
    amount_in_words = models.TextField(null=False)
    grn_date = models.DateField(null=True) #submitted date
    invoice_date = models.DateField(null=False)
    invoice_value = models.FloatField(null=False)
    grn_value = models.FloatField(null=False) #summation of items value price
    tax_value = models.FloatField(default=0)
    grn_invoice_amount_diff = models.FloatField(default=0)
    gstn = models.CharField(max_length=50, null=True)
    gst_purchased = models.BooleanField(default=True)
    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'purchased'



class PurchasedItems(models.Model):
    purchased = models.ForeignKey(Purchased, on_delete=models.CASCADE, related_name='purchased_items')
    item_code = models.CharField(max_length=100, null=False)
    item_name = models.CharField(max_length=100, null=False)
    default_uom_quantity = models.FloatField(null=False, default=0) #newly
    default_uom = models.CharField(max_length=20, null=True, blank=True)
    hsn = models.CharField(max_length=240, null=True)
    tax = models.FloatField(null=True)
    rate = models.FloatField(null=False)
    price = models.FloatField(null=False)
    quantity = models.FloatField(null=False, default=1)
    uom = models.CharField(max_length=20, null=False)
    tax_amount = models.FloatField(default=0)
    without_tax_amount = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'purchased_items'
        


# Periodic Automatic Replacement

class PeriodicAutomaticReplacement(models.Model):
    pos = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='pos_par')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_par')
    final_product = models.ForeignKey(FinalProductRegistrationModel, null=True, on_delete=models.SET_NULL,related_name='final_product_par')
    semi_product = models.ForeignKey(SemiProductRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='semi_product_par')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='raw_material_par')
    item_name = models.CharField(max_length=200, null=False)
    item_code = models.CharField(max_length=200, null=False)
    default_uom = models.CharField(max_length=20, null=False)
    default_uom_quantity = models.FloatField(null=False, default=0)
    default_value_for_day = models.FloatField(null=False)
    value_for_week_day = models.JSONField(default={'Mon':None, 'Tue':None, 'Wed':None, 'Thu':None, 'Fri':None, 'Sat':None, 'Sun':None})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'periodic_automatic_replacement'
    
# 2.4.1.POS
# 2.4.2.Product Type
# 2.4.3.Department
# 2.4.3.1.Item Name
# 2.4.3.2.Default value for the day
# 2.4.3.3.Based on day of week

#----------Store Issue
class StoreIssue(models.Model):
    store_issue_id = models.CharField(max_length=100, null=True)
    child_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name='store_issue_request')
    to_pos = models.ForeignKey(POS, on_delete=models.SET_NULL, null=True, related_name='to_pos_store_issue')
    to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='to_department_store_issue')
    parent_store = models.ForeignKey(Store, on_delete=models.CASCADE, null=False, related_name='store_issue_issued')
    requested_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='store_issue_requested_by')
    issued_by = models.ForeignKey(User, null=True, on_delete = models.SET_NULL, related_name='store_issue_issued_by')
    status = models.CharField(max_length=50, null=False, default='draft')
    delivery_date = models.DateTimeField(null=False)
    submitted = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(null=True)
    received = models.BooleanField(default=False)
    received_on = models.DateTimeField(null=True)
    issued = models.BooleanField(default=False)
    issued_on = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_issue'
        
@receiver(post_save, sender=StoreIssue)
def store_issue_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        store_issue = StoreIssue.objects.filter(id=instance.id).first()
        if store_issue:
            if not store_issue.store_issue_id:
                store_issue.store_issue_id = 'ST_ISSUE'+str(store_issue.id).zfill(3)
                store_issue.save() 
        
class StoreIssueItems(models.Model):
    store_issue = models.ForeignKey(StoreIssue, null=False, on_delete=models.CASCADE, related_name='store_issue_materials')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=False, on_delete=models.CASCADE, related_name='items_store_issue')
    item_code = models.CharField(max_length=100, null=False, blank=False)
    item_name = models.CharField(max_length=240, null=False, blank=False)
    default_uom = models.CharField(null=False, blank=False, max_length=100)
    default_uom_quantity = models.FloatField(null=False)
    ordered_quantity = models.FloatField(null=False, default=0)
    issued_quantity = models.FloatField(null=False, default=0)
    received_quantity = models.FloatField(null=False, default=0)
    rejected = models.BooleanField(default=False)
    rejected_remark = models.CharField(max_length=240, null=True)
    remark = models.CharField(max_length=240, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'store_issue_items'
        
class StockTransfer(models.Model):
    stock_transfer_id = models.CharField(max_length=100, null=True)
    from_pos = models.ForeignKey(POS, null=False, on_delete=models.CASCADE, related_name='from_pos_stock_transfer')
    to_pos = models.ForeignKey(POS, null=False, on_delete=models.CASCADE, related_name='to_pos_stock_transfer')
    from_department = models.ForeignKey(Department, null=False, on_delete = models.CASCADE, related_name='from_department_stock_transfer')
    to_department = models.ForeignKey(Department, null=False, on_delete = models.CASCADE, related_name='to_department_stock_transfer')
    transfered_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name = 'transfered_by_stock_transfer')
    status = models.CharField(max_length=50, null=False, default='draft')
    submitted = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(null=True)
    received = models.BooleanField(default=False)
    received_on = models.DateTimeField(null=True)
    received_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name = 'received_by_stock_transfer')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'stock_transfer'
        
@receiver(post_save, sender=StockTransfer)
def stock_transfer_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        store_issue = StockTransfer.objects.filter(id=instance.id).first()
        if store_issue:
            if not store_issue.stock_transfer_id:
                store_issue.stock_transfer_id = 'STOCK_TRANSFER'+str(store_issue.id).zfill(3)
                store_issue.save() 


class StockTransferItems(models.Model):
    stock_transfer = models.ForeignKey(StockTransfer, null=False, on_delete=models.CASCADE, related_name='stock_transfer_materials')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='stock_transfer_raw_materials')
    final_product = models.ForeignKey(FinalProductRegistrationModel, null=True, on_delete=models.SET_NULL,related_name='stock_transfer_final_product')
    semi_product = models.ForeignKey(SemiProductRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='stock_transfer_semi_product')
    item_code = models.CharField(max_length=100, null=False, blank=False)
    item_name = models.CharField(max_length=240, null=False, blank=False)
    default_uom = models.CharField(null=False, blank=False, max_length=100)
    default_uom_quantity = models.FloatField(null=False)
    issued_quantity = models.FloatField(null=False, default=0)
    received_quantity = models.FloatField(null=False, default=0)
    remark = models.CharField(max_length=240, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'stock_transfer_items'
    
# 2.3.1.UID
# 2.3.2.From POS
# 2.3.3.To POS
# 2.3.4.From Department
# 2.3.5.To Department
# 2.3.6.Maker
# 2.3.7.Timestamp
# 2.3.8.Product Type
# 2.3.9.Item Name (common between both departments for the selected product type)
# 2.3.10.Sender Item Qty
# 2.3.11.Receiver Item Qty
# 2.3.12.Receiver Name


#---------- Order Sheet

# Advance Ordering - cake (open orders) fields can vary


# from ->
# either - b2b Client (only final product listing)
# or - dept, pos

# to -> 
# dept,pos

# 2 approach 
# 1. smart Cart using PAR
# 2. Direct

# all types of product

# ordered quantity

# status - 
# draft, order placed, issued, recieved , partially fullfilled, on hold, billed then dispatch  (b2b client).

# for raw material (category peritiable product) for these products genrate po.


class OrderSheet(models.Model):
    from_b2b_client = models.ForeignKey(BtoBclient, null=True, on_delete=models.SET_NULL, related_name='b2b_client_requested_order_sheet')
    from_pos = models.ForeignKey(POS, on_delete=models.SET_NULL, null=True, related_name='pos_requested_order_sheet')
    from_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='department_requested_order_sheet')
    custom_order = models.BooleanField(default=False)
    to_pos = models.ForeignKey(POS, on_delete = models.SET_NULL, null=True, related_name='pos_order_sheet')
    to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='department_order_sheet')
    status = models.CharField(null=False, max_length=50, default='draft')
    order_sheet_id = models.CharField(max_length=100, null=True)
    delivery_date = models.DateTimeField(null=False)
    created_by = models.ForeignKey(User, null=True, related_name='created_order_sheet', on_delete=models.SET_NULL)
    submitted = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(null=True)
    issued_by = models.ForeignKey(User, null=True, related_name='issued_order_sheet', on_delete=models.SET_NULL)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(null=True)
    received_by = models.ForeignKey(User, null=True, related_name='received_order_sheet', on_delete=models.SET_NULL)
    received_at = models.DateTimeField(null=True)
    received = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'order_sheet'
    
    
@receiver(post_save, sender=OrderSheet)
def order_sheet_id_maker(sender, instance=None, created=False, **kwargs):
    if created:
        store_issue = OrderSheet.objects.filter(id=instance.id).first()
        if store_issue:
            if not store_issue.order_sheet_id:
                store_issue.order_sheet_id = 'ORDER_SHEET_'+str(store_issue.id).zfill(3)
                store_issue.save() 

class OrderSheetItems(models.Model):
    order_sheet = models.ForeignKey(OrderSheet, null=False, on_delete=models.CASCADE, related_name='order_sheet_materials')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='order_sheet_raw_materials')
    final_product = models.ForeignKey(FinalProductRegistrationModel, null=True, on_delete=models.SET_NULL,related_name='order_sheet_final_product')
    semi_product = models.ForeignKey(SemiProductRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='order_sheet_semi_product')
    item_code = models.CharField(max_length=100, null=False, blank=False)
    item_name = models.CharField(max_length=240, null=False, blank=False)
    default_uom = models.CharField(null=False, blank=False, max_length=100)
    default_uom_quantity = models.FloatField(null=False)
    ordered_quantity = models.FloatField(null=False, default=0)
    issued_quantity = models.FloatField(null=False, default=0)
    received_quantity = models.FloatField(null=False, default=0)
    remark = models.CharField(max_length=240, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        app_label = 'master_app'
        db_table = 'order_sheet_items'
        
    
    
class ProductionDetails(models.Model):
    production_id = models.CharField(max_length=100, null=True)
    order_sheet_reference = models.ForeignKey(OrderSheet, on_delete=models.SET_NULL, null=True, related_name='order_sheet_productions')
    production_date = models.DateTimeField(null=True)
    from_b2b_client = models.ForeignKey(BtoBclient, null=True, on_delete=models.SET_NULL, related_name='b2b_client_production_data')
    from_pos = models.ForeignKey(POS, on_delete=models.SET_NULL, null=True, related_name='pos_requested_production')
    from_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL, related_name='department_requested_production')
    direct_order = models.BooleanField(default=False)
    to_pos = models.ForeignKey(POS, on_delete = models.SET_NULL, null=True, related_name='pos_productions')
    to_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='department_productions')
    production_type = models.CharField(max_length=100, null=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'productions'
        
class ProductionItems(models.Model):
    production = models.ForeignKey(OrderSheet, null=False, on_delete=models.CASCADE, related_name='production_items')
    raw_material = models.ForeignKey(RawMaterialRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='production_raw_materials')
    final_product = models.ForeignKey(FinalProductRegistrationModel, null=True, on_delete=models.SET_NULL,related_name='production_final_product')
    semi_product = models.ForeignKey(SemiProductRegistrationModel, null=True, on_delete=models.SET_NULL, related_name='production_semi_product')
    item_code = models.CharField(max_length=100, null=False, blank=False)
    item_name = models.CharField(max_length=240, null=False, blank=False)
    default_uom = models.CharField(null=False, blank=False, max_length=100)
    default_uom_quantity = models.FloatField(null=False)
    ordered_quantity = models.FloatField(null=False, default=0)
    produced_quantity = models.FloatField(null=False, default=0)
    remark = models.CharField(max_length=240, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'master_app'
        db_table = 'production_items'