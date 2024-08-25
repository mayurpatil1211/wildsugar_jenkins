from django.urls import include, path, re_path
from master_app.views import TestApiView



from master_app.views import TestApiView

from master_app.apis.master_data_apis.static_data_apis import category_type_api, department_type_api, company_type_api, employment_type_api, high_value_item_type_api, \
    pos_type_api, priority_type_api, severity_type_api, vendor_type_api, unit_measurement_api, product_type_api, industry_types, store_types, asset_types

from master_app.apis.master_data_apis.master_data_core import brand_apis, cluster_apis, company_apis, department_apis, vendors_apis, pos_apis, b2b_client_api, b2b_rates_defination, \
    material_registration, hsn_code_apis, service_material,vendor_document_api,vendor_bank_detail_api, store_apis, default_variable_charges, recipe_registration, semi_product_apis, final_product_apis, \
        po_planning, po_create, purchased_apis, po_planning_template, par_apis, store_issue_apis, stock_transfer_apis, order_sheet_apis


from master_app.views import TestApiView


urlpatterns = [
	re_path(r'^test_swagger$', TestApiView.as_view(), name='swagger_test'),

	re_path(r'^type/company$', company_type_api.CompanyTypeApiView.as_view(), name='company'),
	re_path(r'^type/department$', department_type_api.DepartmentTypeApiView.as_view(), name='department'),
	re_path(r'^type/employment$', employment_type_api.EmploymentTypeApiView.as_view(), name='employment'),
    re_path(r'^type/highvalueitem$', high_value_item_type_api.HighValueItemTypeApiView.as_view(), name='highvalueitem'),
    re_path(r'^type/pos$', pos_type_api.PosTypeApiView.as_view(), name='postype'),
    
	re_path(r'^categories', category_type_api.CategoryTypeApiView.as_view(), name='category_type'),
    re_path(r'^sub-categories$', category_type_api.SubcategoryListApiView.as_view(), name='sub-category_type'),
    re_path(r'^type/priority$', priority_type_api.PrioritiyTypeApiView.as_view(), name='Prioritiy'),
    re_path(r'^type/product$', product_type_api.ProductTypeApiView.as_view(), name='product'),
    re_path(r'^type/severity$', severity_type_api.SeverityTypeApiView.as_view(), name='severity'),
    re_path(r'^type/vendor$', vendor_type_api.VendorTypeApiView.as_view(), name='vendor'),
    re_path(r'^type/industry$', industry_types.IndustryTypeApiView.as_view(), name='industry'),
    re_path(r'^type/store$', store_types.StoreTypesApiView.as_view(), name='store'),
    re_path(r'^type/asset$', asset_types.AssetTypesApiView.as_view(), name='asset_type'),
    
    re_path(r'^unit_measurement$', unit_measurement_api.UnitOfMeasurementApiView.as_view(), name='unit_measurement'),
    
    re_path(r'^unit_measurment/conversion$', unit_measurement_api.UnitOfMeasurementConversionApiView.as_view(), name='unit_of_measurement_conversion'),
    


    #------Master Data Core
    re_path(r'^brand$', brand_apis.BrandApiView.as_view(), name='brand_crud'),
    re_path(r'^brand/address$', brand_apis.BrandAddressApiView.as_view(), name='brand_address'),
    
    re_path(r'^cluster$', cluster_apis.ClusterApiView.as_view(), name='cluster_crud'),
    re_path(r'^cluster/address$', cluster_apis.ClusterAddressApiView.as_view(), name='cluster_address'),
    
    re_path(r'^company$', company_apis.CompanyApiView.as_view(), name='company_crud'),
    re_path(r'^company/address$', company_apis.CompanyAddressApiView.as_view(), name='company_address'),
    re_path(r'^department$', department_apis.DepartmentApiView.as_view(), name='department_crud'),
    re_path(r'^sub-department$', department_apis.SubDepartmentApiView.as_view(), name='sub_department'),
    
    re_path(r'^vendors$', vendors_apis.VendorsApiView.as_view(), name='vendors_crud'),
    re_path(r'^vendor/documents$', vendor_document_api.VendorDocumentApiView.as_view(), name='vendor_document'),
    re_path(r'^vendor/bank$', vendor_bank_detail_api.VendorBankDetailApiView.as_view(), name='vendor_bank'),

    re_path(r'^pos$', pos_apis.POSApiView.as_view(), name='pos_crud'),
    re_path(r'^pos/departments$', pos_apis.PosDepartmentMappingApi.as_view(), name='pos_department_mapping'),
    re_path(r'^pos/cluster$', cluster_apis.ClusterPosMappingApiView.as_view(), name='pos_clusters'),
    
    #----- B2B client
    re_path(r'^b2b-client$', b2b_client_api.B2bClientApiView.as_view(), name='b2b-client'),
    
    #----- B2B rate defination
    re_path(r'^b2b/rate/defination$', b2b_rates_defination.B2BRatesDefinitionApiView.as_view(), name='b2b_rate_defination'),
    
    #----- HSN CODE Apis
    re_path(r'^hsn-codes$', hsn_code_apis.HsnCodeCrudApiView.as_view(), name='hsn_code_api'),
    re_path(r'^hsn-codes/tags$', hsn_code_apis.HSNCodeTagsApiView.as_view(), name='hsn_code_tags_api'),
    
    #---- Raw Material
    re_path(r'^raw-material$', material_registration.RawMaterialApiView.as_view(), name='raw_material'),
    re_path(r'^raw-material/filters$', material_registration.RawMaterialFilterApiVIew.as_view(), name='raw_material'),
    
    re_path(r'^raw-material/tags$', material_registration.RawMaterialTagsApiView.as_view(), name='raw_material_tags'),
    re_path(r'^raw-material/aliases$', material_registration.RawMaterialAliasApiView.as_view(), name='raw_material_aliases'),
    re_path(r'^raw-material/vendor/pricing$', material_registration.RawMaterialVendorPricingApiView.as_view(), name='raw_material_vendor_pricing'),
    re_path(r'^raw-material/vendor/update/price$', material_registration.RawMaterialVendorPricingUpdate.as_view(), name='update_vendor_raw_material_pricing'),
    re_path(r'^raw-material/mappings$', material_registration.RawMaterialDeptPosApiView.as_view(), name='raw_material_mappings'),
    re_path(r'^raw-material/uoms$', material_registration.RawMaterialsExtraUomApiView.as_view(), name='raw_material_uoms'),
    
    re_path(r'^semi-product$', semi_product_apis.SemiProductRegistrationApiView.as_view(), name='semi_product'),
    re_path(r'^semi-product/tags$', semi_product_apis.SemiProductTagsApiView.as_view(), name='semi_product_tag'),
    re_path(r'^semi-product/mappings$', semi_product_apis.SemiProductDeptPosApiView.as_view(), name='semi_product_mapping'),
    re_path(r'^semi-product/filters$', semi_product_apis.SemiProductFilterApiVIew.as_view(), name='semi_product_filter'),
    
    
    
    
    re_path(r'^final-product$', final_product_apis.FinalProductRegistrationApiView.as_view(), name='final_product'),
    re_path(r'^final-product/tags$', final_product_apis.FinalProductTagsApiView.as_view(), name='final_product_tags'),
    re_path(r'^final-product/pricing$', final_product_apis.FinalProductSellingPriceApiView.as_view(), name='final_product_pricing'),
    re_path(r'^final-product/pos/pricing$', final_product_apis.FinalProductPriceForPOSApiView.as_view(), name='final_product_price_pos'),
    re_path(r'^final-product/filters$', final_product_apis.FinalProductFilterApiVIew.as_view(), name='final_product_filter'),
    
    #-----Service Material
    re_path(r'asset-inventory$', service_material.AssetInvetoryApiView.as_view(), name='asset_inventory'),
    
    #-----Store APIs
    re_path(r'^store$', store_apis.StoreApiView.as_view(), name='store'),
    re_path(r'^store/child$', store_apis.GetChildStores.as_view(), name='child_store'),
    re_path(r'^store/parent$', store_apis.GetParentStore.as_view(), name='parent_store'),
    
    #----Default Variable Charges
    re_path(r'^default/variable-charges$', default_variable_charges.DefaultVariableChargesApiView.as_view(), name='default_variabel_charges'),

    #----Recipe Registration
    re_path(r'^recipe$', recipe_registration.RecipeRegistrationApiView.as_view(), name='recipe_registration'),
    
    #--- PO Planning
    re_path(r'^po/planning/templates$', po_planning_template.PoPlanningTemplateApiView.as_view(), name='po_planning_template'),
    re_path(r'^po/planning$', po_planning.PoPlanningAPIView.as_view(), name='po_planning'),
    
    #--- PO
    re_path(r'^po$', po_create.PoApiView.as_view(), name='po'),
    
    #---- Purchased Order
    re_path(r'^purchased/orders$', purchased_apis.PurchasedApiView.as_view(), name='purchased_order'),
    
    #---- PAR
    re_path(r'^par$', par_apis.PeriodicAutomaticReplacementApiView.as_view(), name='par'),
    re_path(r'^copy/par$', par_apis.CopyParApiView.as_view(), name='copy_par_values'),
    
    #---Store Issue
    re_path(r'^store/issue$', store_issue_apis.StoreIssueApiView.as_view(), name='store_issue'),
    
    #---Stock Transfer APIs
    re_path(r'^stock/transfer$', stock_transfer_apis.StockTransferApiView.as_view(), name='stock_transfer'),
    
    #----ORDER SHEET
    re_path(r'^order/sheet$', order_sheet_apis.OrderSheetApiView.as_view(), name='order_sheet_apis'),
    
    re_path(r'^order/sheet/items$', order_sheet_apis.OrderSheetItemsFilterApiView.as_view(), name='order_sheet_items_filter'),
    
    re_path(r'^order/sheet/estimate/raw_material$', order_sheet_apis.OrderSheetRawMaterialEstimate.as_view(), name='order_sheet_estimate_raw_material'),

]
