SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE IF NOT EXISTS `asset_inventory_dept_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `asset_inventory_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_inventory_dept_map_asset_inventory_id_depar_3e595d86_uniq` (`asset_inventory_id`,`department_id`),
  KEY `asset_inventory_dept_department_id_106186e1_fk_departmen` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `asset_inventory_pos_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `asset_inventory_id` bigint NOT NULL,
  `pos_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asset_inventory_pos_mapp_asset_inventory_id_pos_i_ac92948c_uniq` (`asset_inventory_id`,`pos_id`),
  KEY `asset_inventory_pos_mapping_pos_id_09f5ed80_fk_pos_id` (`pos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `asset_inventory_pos_mapping` (`id`, `created_at`, `updated_at`, `asset_inventory_id`, `pos_id`) VALUES
(1, '2023-12-02 16:38:29.995616', '2023-12-02 16:38:29.995632', 1, 1);

CREATE TABLE IF NOT EXISTS `asset_inventory_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_code` varchar(20) DEFAULT NULL,
  `item_name` varchar(250) NOT NULL,
  `default_uom` varchar(20) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `sub_category` varchar(50) DEFAULT NULL,
  `yield_quantity` double DEFAULT NULL,
  `yield_quantity_cost` double DEFAULT NULL,
  `life_cycle` double DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `high_value_item` tinyint(1) DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `available_for_cluster` tinyint(1) NOT NULL,
  `hsn_code` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  `asset_type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_inventory_registration_brand_id_aa37bdff_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `asset_inventory_registration` (`id`, `item_code`, `item_name`, `default_uom`, `category`, `sub_category`, `yield_quantity`, `yield_quantity_cost`, `life_cycle`, `expiry_date`, `high_value_item`, `priority`, `severity`, `available_for_cluster`, `hsn_code`, `created_at`, `updated_at`, `brand_id`, `asset_type`) VALUES
(1, 'Modified_SERVICE_1', 'Service Material 1', 'KG', 'non-production', 'non-production', 80, 50, 180, '2023-09-01', 1, 'P1', 'S1', 1, '9h9h9dj9w9w9', '2023-12-02 16:38:29.982662', '2023-12-02 16:38:48.617181', 1, 'asset_type');

CREATE TABLE IF NOT EXISTS `asset_type_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `asset_type` varchar(100) NOT NULL,
  `asset_type_description` varchar(240) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_type_list_brand_id_28d347a2_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add blacklisted token', 6, 'add_blacklistedtoken'),
(22, 'Can change blacklisted token', 6, 'change_blacklistedtoken'),
(23, 'Can delete blacklisted token', 6, 'delete_blacklistedtoken'),
(24, 'Can view blacklisted token', 6, 'view_blacklistedtoken'),
(25, 'Can add outstanding token', 7, 'add_outstandingtoken'),
(26, 'Can change outstanding token', 7, 'change_outstandingtoken'),
(27, 'Can delete outstanding token', 7, 'delete_outstandingtoken'),
(28, 'Can view outstanding token', 7, 'view_outstandingtoken'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add permissions', 9, 'add_permissions'),
(34, 'Can change permissions', 9, 'change_permissions'),
(35, 'Can delete permissions', 9, 'delete_permissions'),
(36, 'Can view permissions', 9, 'view_permissions'),
(37, 'Can add role permission', 10, 'add_rolepermission'),
(38, 'Can change role permission', 10, 'change_rolepermission'),
(39, 'Can delete role permission', 10, 'delete_rolepermission'),
(40, 'Can view role permission', 10, 'view_rolepermission'),
(41, 'Can add roles', 11, 'add_roles'),
(42, 'Can change roles', 11, 'change_roles'),
(43, 'Can delete roles', 11, 'delete_roles'),
(44, 'Can view roles', 11, 'view_roles'),
(45, 'Can add user roles', 12, 'add_userroles'),
(46, 'Can change user roles', 12, 'change_userroles'),
(47, 'Can delete user roles', 12, 'delete_userroles'),
(48, 'Can view user roles', 12, 'view_userroles'),
(49, 'Can add brand', 13, 'add_brand'),
(50, 'Can change brand', 13, 'change_brand'),
(51, 'Can delete brand', 13, 'delete_brand'),
(52, 'Can view brand', 13, 'view_brand'),
(53, 'Can add category list', 14, 'add_categorylist'),
(54, 'Can change category list', 14, 'change_categorylist'),
(55, 'Can delete category list', 14, 'delete_categorylist'),
(56, 'Can view category list', 14, 'view_categorylist'),
(57, 'Can add clusters', 15, 'add_clusters'),
(58, 'Can change clusters', 15, 'change_clusters'),
(59, 'Can delete clusters', 15, 'delete_clusters'),
(60, 'Can view clusters', 15, 'view_clusters'),
(61, 'Can add company', 16, 'add_company'),
(62, 'Can change company', 16, 'change_company'),
(63, 'Can delete company', 16, 'delete_company'),
(64, 'Can view company', 16, 'view_company'),
(65, 'Can add company types', 17, 'add_companytypes'),
(66, 'Can change company types', 17, 'change_companytypes'),
(67, 'Can delete company types', 17, 'delete_companytypes'),
(68, 'Can view company types', 17, 'view_companytypes'),
(69, 'Can add department', 18, 'add_department'),
(70, 'Can change department', 18, 'change_department'),
(71, 'Can delete department', 18, 'delete_department'),
(72, 'Can view department', 18, 'view_department'),
(73, 'Can add department types', 19, 'add_departmenttypes'),
(74, 'Can change department types', 19, 'change_departmenttypes'),
(75, 'Can delete department types', 19, 'delete_departmenttypes'),
(76, 'Can view department types', 19, 'view_departmenttypes'),
(77, 'Can add employment types', 20, 'add_employmenttypes'),
(78, 'Can change employment types', 20, 'change_employmenttypes'),
(79, 'Can delete employment types', 20, 'delete_employmenttypes'),
(80, 'Can view employment types', 20, 'view_employmenttypes'),
(81, 'Can add high value item types', 21, 'add_highvalueitemtypes'),
(82, 'Can change high value item types', 21, 'change_highvalueitemtypes'),
(83, 'Can delete high value item types', 21, 'delete_highvalueitemtypes'),
(84, 'Can view high value item types', 21, 'view_highvalueitemtypes'),
(85, 'Can add industry types', 22, 'add_industrytypes'),
(86, 'Can change industry types', 22, 'change_industrytypes'),
(87, 'Can delete industry types', 22, 'delete_industrytypes'),
(88, 'Can view industry types', 22, 'view_industrytypes'),
(89, 'Can add pos types', 23, 'add_postypes'),
(90, 'Can change pos types', 23, 'change_postypes'),
(91, 'Can delete pos types', 23, 'delete_postypes'),
(92, 'Can view pos types', 23, 'view_postypes'),
(93, 'Can add prioritiy types', 24, 'add_prioritiytypes'),
(94, 'Can change prioritiy types', 24, 'change_prioritiytypes'),
(95, 'Can delete prioritiy types', 24, 'delete_prioritiytypes'),
(96, 'Can view prioritiy types', 24, 'view_prioritiytypes'),
(97, 'Can add product types', 25, 'add_producttypes'),
(98, 'Can change product types', 25, 'change_producttypes'),
(99, 'Can delete product types', 25, 'delete_producttypes'),
(100, 'Can view product types', 25, 'view_producttypes'),
(101, 'Can add severity types', 26, 'add_severitytypes'),
(102, 'Can change severity types', 26, 'change_severitytypes'),
(103, 'Can delete severity types', 26, 'delete_severitytypes'),
(104, 'Can view severity types', 26, 'view_severitytypes'),
(105, 'Can add unit of measurement', 27, 'add_unitofmeasurement'),
(106, 'Can change unit of measurement', 27, 'change_unitofmeasurement'),
(107, 'Can delete unit of measurement', 27, 'delete_unitofmeasurement'),
(108, 'Can view unit of measurement', 27, 'view_unitofmeasurement'),
(109, 'Can add vendor types', 28, 'add_vendortypes'),
(110, 'Can change vendor types', 28, 'change_vendortypes'),
(111, 'Can delete vendor types', 28, 'delete_vendortypes'),
(112, 'Can view vendor types', 28, 'view_vendortypes'),
(113, 'Can add subcategory list', 29, 'add_subcategorylist'),
(114, 'Can change subcategory list', 29, 'change_subcategorylist'),
(115, 'Can delete subcategory list', 29, 'delete_subcategorylist'),
(116, 'Can view subcategory list', 29, 'view_subcategorylist'),
(117, 'Can add company documents', 30, 'add_companydocuments'),
(118, 'Can change company documents', 30, 'change_companydocuments'),
(119, 'Can delete company documents', 30, 'delete_companydocuments'),
(120, 'Can view company documents', 30, 'view_companydocuments'),
(121, 'Can add user brand mapping', 31, 'add_userbrandmapping'),
(122, 'Can change user brand mapping', 31, 'change_userbrandmapping'),
(123, 'Can delete user brand mapping', 31, 'delete_userbrandmapping'),
(124, 'Can view user brand mapping', 31, 'view_userbrandmapping'),
(125, 'Can add company shareholder', 32, 'add_companyshareholder'),
(126, 'Can change company shareholder', 32, 'change_companyshareholder'),
(127, 'Can delete company shareholder', 32, 'delete_companyshareholder'),
(128, 'Can view company shareholder', 32, 'view_companyshareholder'),
(129, 'Can add company cluser mapping', 33, 'add_companyclusermapping'),
(130, 'Can change company cluser mapping', 33, 'change_companyclusermapping'),
(131, 'Can delete company cluser mapping', 33, 'delete_companyclusermapping'),
(132, 'Can view company cluser mapping', 33, 'view_companyclusermapping'),
(133, 'Can add brand cluster mapping', 34, 'add_brandclustermapping'),
(134, 'Can change brand cluster mapping', 34, 'change_brandclustermapping'),
(135, 'Can delete brand cluster mapping', 34, 'delete_brandclustermapping'),
(136, 'Can view brand cluster mapping', 34, 'view_brandclustermapping'),
(137, 'Can add department cluster mapping', 35, 'add_departmentclustermapping'),
(138, 'Can change department cluster mapping', 35, 'change_departmentclustermapping'),
(139, 'Can delete department cluster mapping', 35, 'delete_departmentclustermapping'),
(140, 'Can view department cluster mapping', 35, 'view_departmentclustermapping'),
(141, 'Can add pos', 36, 'add_pos'),
(142, 'Can change pos', 36, 'change_pos'),
(143, 'Can delete pos', 36, 'delete_pos'),
(144, 'Can view pos', 36, 'view_pos'),
(145, 'Can add vendors', 37, 'add_vendors'),
(146, 'Can change vendors', 37, 'change_vendors'),
(147, 'Can delete vendors', 37, 'delete_vendors'),
(148, 'Can view vendors', 37, 'view_vendors'),
(149, 'Can add vendor documents', 38, 'add_vendordocuments'),
(150, 'Can change vendor documents', 38, 'change_vendordocuments'),
(151, 'Can delete vendor documents', 38, 'delete_vendordocuments'),
(152, 'Can view vendor documents', 38, 'view_vendordocuments'),
(153, 'Can add vendor bank details', 39, 'add_vendorbankdetails'),
(154, 'Can change vendor bank details', 39, 'change_vendorbankdetails'),
(155, 'Can delete vendor bank details', 39, 'delete_vendorbankdetails'),
(156, 'Can view vendor bank details', 39, 'view_vendorbankdetails'),
(157, 'Can add vendor cluster mapping', 40, 'add_vendorclustermapping'),
(158, 'Can change vendor cluster mapping', 40, 'change_vendorclustermapping'),
(159, 'Can delete vendor cluster mapping', 40, 'delete_vendorclustermapping'),
(160, 'Can view vendor cluster mapping', 40, 'view_vendorclustermapping'),
(161, 'Can add vendor pos mapping', 41, 'add_vendorposmapping'),
(162, 'Can change vendor pos mapping', 41, 'change_vendorposmapping'),
(163, 'Can delete vendor pos mapping', 41, 'delete_vendorposmapping'),
(164, 'Can view vendor pos mapping', 41, 'view_vendorposmapping'),
(165, 'Can add vendor brand mapping', 42, 'add_vendorbrandmapping'),
(166, 'Can change vendor brand mapping', 42, 'change_vendorbrandmapping'),
(167, 'Can delete vendor brand mapping', 42, 'delete_vendorbrandmapping'),
(168, 'Can view vendor brand mapping', 42, 'view_vendorbrandmapping'),
(169, 'Can add pos department mapping', 43, 'add_posdepartmentmapping'),
(170, 'Can change pos department mapping', 43, 'change_posdepartmentmapping'),
(171, 'Can delete pos department mapping', 43, 'delete_posdepartmentmapping'),
(172, 'Can view pos department mapping', 43, 'view_posdepartmentmapping'),
(173, 'Can add pos company mapping', 44, 'add_poscompanymapping'),
(174, 'Can change pos company mapping', 44, 'change_poscompanymapping'),
(175, 'Can delete pos company mapping', 44, 'delete_poscompanymapping'),
(176, 'Can view pos company mapping', 44, 'view_poscompanymapping'),
(177, 'Can add bto bclient', 45, 'add_btobclient'),
(178, 'Can change bto bclient', 45, 'change_btobclient'),
(179, 'Can delete bto bclient', 45, 'delete_btobclient'),
(180, 'Can view bto bclient', 45, 'view_btobclient'),
(181, 'Can add b2 bclient bank details', 46, 'add_b2bclientbankdetails'),
(182, 'Can change b2 bclient bank details', 46, 'change_b2bclientbankdetails'),
(183, 'Can delete b2 bclient bank details', 46, 'delete_b2bclientbankdetails'),
(184, 'Can view b2 bclient bank details', 46, 'view_b2bclientbankdetails'),
(185, 'Can add b2 bclient pos mapping', 47, 'add_b2bclientposmapping'),
(186, 'Can change b2 bclient pos mapping', 47, 'change_b2bclientposmapping'),
(187, 'Can delete b2 bclient pos mapping', 47, 'delete_b2bclientposmapping'),
(188, 'Can view b2 bclient pos mapping', 47, 'view_b2bclientposmapping'),
(189, 'Can add b2 bclient cluster mapping', 48, 'add_b2bclientclustermapping'),
(190, 'Can change b2 bclient cluster mapping', 48, 'change_b2bclientclustermapping'),
(191, 'Can delete b2 bclient cluster mapping', 48, 'delete_b2bclientclustermapping'),
(192, 'Can view b2 bclient cluster mapping', 48, 'view_b2bclientclustermapping'),
(193, 'Can add b2 bclient brand mapping', 49, 'add_b2bclientbrandmapping'),
(194, 'Can change b2 bclient brand mapping', 49, 'change_b2bclientbrandmapping'),
(195, 'Can delete b2 bclient brand mapping', 49, 'delete_b2bclientbrandmapping'),
(196, 'Can view b2 bclient brand mapping', 49, 'view_b2bclientbrandmapping'),
(197, 'Can add store', 50, 'add_store'),
(198, 'Can change store', 50, 'change_store'),
(199, 'Can delete store', 50, 'delete_store'),
(200, 'Can view store', 50, 'view_store'),
(201, 'Can add store employee', 51, 'add_storeemployee'),
(202, 'Can change store employee', 51, 'change_storeemployee'),
(203, 'Can delete store employee', 51, 'delete_storeemployee'),
(204, 'Can view store employee', 51, 'view_storeemployee'),
(205, 'Can add store cluster mapping', 52, 'add_storeclustermapping'),
(206, 'Can change store cluster mapping', 52, 'change_storeclustermapping'),
(207, 'Can delete store cluster mapping', 52, 'delete_storeclustermapping'),
(208, 'Can view store cluster mapping', 52, 'view_storeclustermapping'),
(209, 'Can add store brand mapping', 53, 'add_storebrandmapping'),
(210, 'Can change store brand mapping', 53, 'change_storebrandmapping'),
(211, 'Can delete store brand mapping', 53, 'delete_storebrandmapping'),
(212, 'Can view store brand mapping', 53, 'view_storebrandmapping'),
(213, 'Can add semi product registration model', 54, 'add_semiproductregistrationmodel'),
(214, 'Can change semi product registration model', 54, 'change_semiproductregistrationmodel'),
(215, 'Can delete semi product registration model', 54, 'delete_semiproductregistrationmodel'),
(216, 'Can view semi product registration model', 54, 'view_semiproductregistrationmodel'),
(217, 'Can add raw material registration model', 55, 'add_rawmaterialregistrationmodel'),
(218, 'Can change raw material registration model', 55, 'change_rawmaterialregistrationmodel'),
(219, 'Can delete raw material registration model', 55, 'delete_rawmaterialregistrationmodel'),
(220, 'Can view raw material registration model', 55, 'view_rawmaterialregistrationmodel'),
(221, 'Can add final product registration model', 56, 'add_finalproductregistrationmodel'),
(222, 'Can change final product registration model', 56, 'change_finalproductregistrationmodel'),
(223, 'Can delete final product registration model', 56, 'delete_finalproductregistrationmodel'),
(224, 'Can view final product registration model', 56, 'view_finalproductregistrationmodel'),
(225, 'Can add vendor pricing raw material', 57, 'add_vendorpricingrawmaterial'),
(226, 'Can change vendor pricing raw material', 57, 'change_vendorpricingrawmaterial'),
(227, 'Can delete vendor pricing raw material', 57, 'delete_vendorpricingrawmaterial'),
(228, 'Can view vendor pricing raw material', 57, 'view_vendorpricingrawmaterial'),
(229, 'Can add final product selling price', 58, 'add_finalproductsellingprice'),
(230, 'Can change final product selling price', 58, 'change_finalproductsellingprice'),
(231, 'Can delete final product selling price', 58, 'delete_finalproductsellingprice'),
(232, 'Can view final product selling price', 58, 'view_finalproductsellingprice'),
(233, 'Can add final product tags', 59, 'add_finalproducttags'),
(234, 'Can change final product tags', 59, 'change_finalproducttags'),
(235, 'Can delete final product tags', 59, 'delete_finalproducttags'),
(236, 'Can view final product tags', 59, 'view_finalproducttags'),
(237, 'Can add hs ntax information', 60, 'add_hsntaxinformation'),
(238, 'Can change hs ntax information', 60, 'change_hsntaxinformation'),
(239, 'Can delete hs ntax information', 60, 'delete_hsntaxinformation'),
(240, 'Can view hs ntax information', 60, 'view_hsntaxinformation'),
(241, 'Can add hs ncode tags', 61, 'add_hsncodetags'),
(242, 'Can change hs ncode tags', 61, 'change_hsncodetags'),
(243, 'Can delete hs ncode tags', 61, 'delete_hsncodetags'),
(244, 'Can view hs ncode tags', 61, 'view_hsncodetags'),
(245, 'Can add b2b rates definition', 62, 'add_b2bratesdefinition'),
(246, 'Can change b2b rates definition', 62, 'change_b2bratesdefinition'),
(247, 'Can delete b2b rates definition', 62, 'delete_b2bratesdefinition'),
(248, 'Can view b2b rates definition', 62, 'view_b2bratesdefinition'),
(249, 'Can add raw material pos mapping', 63, 'add_rawmaterialposmapping'),
(250, 'Can change raw material pos mapping', 63, 'change_rawmaterialposmapping'),
(251, 'Can delete raw material pos mapping', 63, 'delete_rawmaterialposmapping'),
(252, 'Can view raw material pos mapping', 63, 'view_rawmaterialposmapping'),
(253, 'Can add raw material dept mapping', 64, 'add_rawmaterialdeptmapping'),
(254, 'Can change raw material dept mapping', 64, 'change_rawmaterialdeptmapping'),
(255, 'Can delete raw material dept mapping', 64, 'delete_rawmaterialdeptmapping'),
(256, 'Can view raw material dept mapping', 64, 'view_rawmaterialdeptmapping'),
(257, 'Can add final product price for pos', 65, 'add_finalproductpriceforpos'),
(258, 'Can change final product price for pos', 65, 'change_finalproductpriceforpos'),
(259, 'Can delete final product price for pos', 65, 'delete_finalproductpriceforpos'),
(260, 'Can view final product price for pos', 65, 'view_finalproductpriceforpos'),
(261, 'Can add service material registration model', 66, 'add_servicematerialregistrationmodel'),
(262, 'Can change service material registration model', 66, 'change_servicematerialregistrationmodel'),
(263, 'Can delete service material registration model', 66, 'delete_servicematerialregistrationmodel'),
(264, 'Can view service material registration model', 66, 'view_servicematerialregistrationmodel'),
(265, 'Can add service material pos mapping', 67, 'add_servicematerialposmapping'),
(266, 'Can change service material pos mapping', 67, 'change_servicematerialposmapping'),
(267, 'Can delete service material pos mapping', 67, 'delete_servicematerialposmapping'),
(268, 'Can view service material pos mapping', 67, 'view_servicematerialposmapping'),
(269, 'Can add service material dept mapping', 68, 'add_servicematerialdeptmapping'),
(270, 'Can change service material dept mapping', 68, 'change_servicematerialdeptmapping'),
(271, 'Can delete service material dept mapping', 68, 'delete_servicematerialdeptmapping'),
(272, 'Can view service material dept mapping', 68, 'view_servicematerialdeptmapping'),
(273, 'Can add default variable charges', 69, 'add_defaultvariablecharges'),
(274, 'Can change default variable charges', 69, 'change_defaultvariablecharges'),
(275, 'Can delete default variable charges', 69, 'delete_defaultvariablecharges'),
(276, 'Can view default variable charges', 69, 'view_defaultvariablecharges'),
(277, 'Can add recipe registration', 70, 'add_reciperegistration'),
(278, 'Can change recipe registration', 70, 'change_reciperegistration'),
(279, 'Can delete recipe registration', 70, 'delete_reciperegistration'),
(280, 'Can view recipe registration', 70, 'view_reciperegistration'),
(281, 'Can add recipe variable charges', 71, 'add_recipevariablecharges'),
(282, 'Can change recipe variable charges', 71, 'change_recipevariablecharges'),
(283, 'Can delete recipe variable charges', 71, 'delete_recipevariablecharges'),
(284, 'Can view recipe variable charges', 71, 'view_recipevariablecharges'),
(285, 'Can add recipe ingredients', 72, 'add_recipeingredients'),
(286, 'Can change recipe ingredients', 72, 'change_recipeingredients'),
(287, 'Can delete recipe ingredients', 72, 'delete_recipeingredients'),
(288, 'Can view recipe ingredients', 72, 'view_recipeingredients'),
(289, 'Can add store types', 73, 'add_storetypes'),
(290, 'Can change store types', 73, 'change_storetypes'),
(291, 'Can delete store types', 73, 'delete_storetypes'),
(292, 'Can view store types', 73, 'view_storetypes'),
(293, 'Can add semi product tags', 74, 'add_semiproducttags'),
(294, 'Can change semi product tags', 74, 'change_semiproducttags'),
(295, 'Can delete semi product tags', 74, 'delete_semiproducttags'),
(296, 'Can view semi product tags', 74, 'view_semiproducttags'),
(297, 'Can add raw material tags', 75, 'add_rawmaterialtags'),
(298, 'Can change raw material tags', 75, 'change_rawmaterialtags'),
(299, 'Can delete raw material tags', 75, 'delete_rawmaterialtags'),
(300, 'Can view raw material tags', 75, 'view_rawmaterialtags'),
(301, 'Can add sub department', 76, 'add_subdepartment'),
(302, 'Can change sub department', 76, 'change_subdepartment'),
(303, 'Can delete sub department', 76, 'delete_subdepartment'),
(304, 'Can view sub department', 76, 'view_subdepartment'),
(305, 'Can add pos subdepartment mapping', 77, 'add_possubdepartmentmapping'),
(306, 'Can change pos subdepartment mapping', 77, 'change_possubdepartmentmapping'),
(307, 'Can delete pos subdepartment mapping', 77, 'delete_possubdepartmentmapping'),
(308, 'Can view pos subdepartment mapping', 77, 'view_possubdepartmentmapping'),
(309, 'Can add vendorbank documents', 79, 'add_vendorbankdocuments'),
(310, 'Can change vendorbank documents', 79, 'change_vendorbankdocuments'),
(311, 'Can delete vendorbank documents', 79, 'delete_vendorbankdocuments'),
(312, 'Can view vendorbank documents', 79, 'view_vendorbankdocuments'),
(313, 'Can add store pos mapping', 80, 'add_storeposmapping'),
(314, 'Can change store pos mapping', 80, 'change_storeposmapping'),
(315, 'Can delete store pos mapping', 80, 'delete_storeposmapping'),
(316, 'Can view store pos mapping', 80, 'view_storeposmapping'),
(317, 'Can add vendor pricing update log', 81, 'add_vendorpricingupdatelog'),
(318, 'Can change vendor pricing update log', 81, 'change_vendorpricingupdatelog'),
(319, 'Can delete vendor pricing update log', 81, 'delete_vendorpricingupdatelog'),
(320, 'Can view vendor pricing update log', 81, 'view_vendorpricingupdatelog'),
(321, 'Can add asset invetory dept mapping', 82, 'add_assetinvetorydeptmapping'),
(322, 'Can change asset invetory dept mapping', 82, 'change_assetinvetorydeptmapping'),
(323, 'Can delete asset invetory dept mapping', 82, 'delete_assetinvetorydeptmapping'),
(324, 'Can view asset invetory dept mapping', 82, 'view_assetinvetorydeptmapping'),
(325, 'Can add asset invetory pos mapping', 83, 'add_assetinvetoryposmapping'),
(326, 'Can change asset invetory pos mapping', 83, 'change_assetinvetoryposmapping'),
(327, 'Can delete asset invetory pos mapping', 83, 'delete_assetinvetoryposmapping'),
(328, 'Can view asset invetory pos mapping', 83, 'view_assetinvetoryposmapping'),
(329, 'Can add asset invetory registration model', 84, 'add_assetinvetoryregistrationmodel'),
(330, 'Can change asset invetory registration model', 84, 'change_assetinvetoryregistrationmodel'),
(331, 'Can delete asset invetory registration model', 84, 'delete_assetinvetoryregistrationmodel'),
(332, 'Can view asset invetory registration model', 84, 'view_assetinvetoryregistrationmodel'),
(333, 'Can add asset types', 85, 'add_assettypes'),
(334, 'Can change asset types', 85, 'change_assettypes'),
(335, 'Can delete asset types', 85, 'delete_assettypes'),
(336, 'Can view asset types', 85, 'view_assettypes');

CREATE TABLE IF NOT EXISTS `b2b_client` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_code` varchar(50) NOT NULL,
  `client_name` varchar(250) NOT NULL,
  `address_line_1` longtext,
  `address_line_2` longtext NOT NULL,
  `landmark` longtext,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `pan` varchar(20) DEFAULT NULL,
  `gstn` varchar(50) DEFAULT NULL,
  `billing_type` varchar(20) NOT NULL,
  `credit_period_days` int NOT NULL,
  `credit_period_date` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `b2b_client` (`id`, `client_code`, `client_name`, `address_line_1`, `address_line_2`, `landmark`, `city`, `state`, `contact_number`, `email`, `pan`, `gstn`, `billing_type`, `credit_period_days`, `credit_period_date`, `created_at`, `updated_at`) VALUES
(2, 'CLI_CODE_1', 'Client 1', 'Address Line 1', 'Address Line 2', 'landmark', 'City', 'State', '9019802163', 'mayur.patil1211@gmail.com', 'EAGPP3527K', '28101909100101', 'gst', 180, NULL, '2023-09-16 15:55:16.663817', '2023-09-16 15:55:16.722377'),
(5, 'CLI_CODE_1', 'Client 1', 'Address Line 1', 'Address Line 2', 'landmark', 'City', 'State', '9019802163', 'mayur.patil1211@gmail.com', 'EAGPP3527K', '28101909100101', 'gst', 180, NULL, '2023-09-16 15:55:16.663817', '2023-09-16 15:55:16.722377');

CREATE TABLE IF NOT EXISTS `b2b_client_bank_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(240) DEFAULT NULL,
  `account_name` varchar(240) DEFAULT NULL,
  `account_number` varchar(240) DEFAULT NULL,
  `ifsc` varchar(50) DEFAULT NULL,
  `branch` varchar(240) DEFAULT NULL,
  `client_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `b2b_client_bank_details_client_id_2329542c_fk_b2b_client_id` (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `b2b_client_bank_details` (`id`, `bank_name`, `account_name`, `account_number`, `ifsc`, `branch`, `client_id`, `created_at`, `updated_at`) VALUES
(1, 'HDFC', 'Current', '590119019802163', 'HDFCISN90909', 'Boxite Road', 2, '2023-09-16 15:55:15.949314', '2023-09-16 15:55:15.985699');

CREATE TABLE IF NOT EXISTS `b2b_rates_definition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uom` varchar(50) DEFAULT NULL,
  `rate` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `b2b_client_id` bigint NOT NULL,
  `final_product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `b2b_rates_definition_b2b_client_id_b7ebc6ac_fk_b2b_client_id` (`b2b_client_id`),
  KEY `b2b_rates_definition_final_product_id_6675053c_fk_final_pro` (`final_product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `b2b_rates_definition` (`id`, `uom`, `rate`, `created_at`, `updated_at`, `b2b_client_id`, `final_product_id`) VALUES
(1, 'KG', 24, '2023-09-21 11:31:28.509541', '2023-09-21 11:32:50.840962', 2, 2);

CREATE TABLE IF NOT EXISTS `brand` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(250) NOT NULL,
  `industry_type` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `required_sub_department` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `brand` (`id`, `brand_name`, `industry_type`, `created_at`, `updated_at`, `required_sub_department`) VALUES
(1, 'Wild Sugar', 'Retail', '2023-09-16 15:55:16.423286', '2023-09-16 15:55:16.492052', 0);

CREATE TABLE IF NOT EXISTS `brand_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_id` bigint NOT NULL,
  `cluster_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `brand_cluster_mapping_cluster_id_brand_id_27d722af_uniq` (`cluster_id`,`brand_id`),
  KEY `brand_cluster_mapping_brand_id_2dab1878_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `brand_cluster_mapping` (`id`, `brand_id`, `cluster_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-09-16 15:55:16.554715', '2023-09-16 15:55:16.610694');

CREATE TABLE IF NOT EXISTS `category_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_name` varchar(250) NOT NULL,
  `category_type` varchar(250) NOT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`),
  KEY `category_list_brand_id_317e419d_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `client_brand_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_id` bigint NOT NULL,
  `client_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_brand_mapping_brand_id_949405a8_fk_brand_id` (`brand_id`),
  KEY `client_brand_mapping_client_id_62f23759_fk_b2b_client_id` (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `client_brand_mapping` (`id`, `brand_id`, `client_id`, `created_at`, `updated_at`) VALUES
(1, 1, 2, '2023-09-16 15:55:16.033280', '2023-09-16 15:55:16.100235');

CREATE TABLE IF NOT EXISTS `client_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` bigint NOT NULL,
  `cluster_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_cluster_mapping_client_id_771bdb69_fk_b2b_client_id` (`client_id`),
  KEY `client_cluster_mapping_cluster_id_3bd69803_fk_clusters_id` (`cluster_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `client_cluster_mapping` (`id`, `client_id`, `cluster_id`, `created_at`, `updated_at`) VALUES
(1, 5, 1, '2023-09-16 15:55:16.167643', '2023-09-16 15:55:16.214051'),
(2, 2, 1, '2023-09-16 15:55:16.167643', '2023-09-16 15:55:16.214051');

CREATE TABLE IF NOT EXISTS `client_pos_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `client_id` bigint NOT NULL,
  `pos_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_pos_mapping_client_id_9d11c53b_fk_b2b_client_id` (`client_id`),
  KEY `client_pos_mapping_pos_id_12711a82_fk_pos_id` (`pos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `client_pos_mapping` (`id`, `client_id`, `pos_id`, `created_at`, `updated_at`) VALUES
(2, 2, 1, '2023-09-16 15:55:16.268262', '2023-09-16 15:55:16.309129');

CREATE TABLE IF NOT EXISTS `clusters` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cluster_code` varchar(12) NOT NULL,
  `cluster_name` varchar(250) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `clusters` (`id`, `cluster_code`, `cluster_name`, `created_at`, `updated_at`) VALUES
(1, 'C1', 'Cluster 1', '2023-09-16 15:55:16.855506', '2023-09-16 15:55:16.915133');

CREATE TABLE IF NOT EXISTS `company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(250) NOT NULL,
  `company_type` varchar(100) NOT NULL,
  `address_line_1` varchar(100) DEFAULT NULL,
  `address_line_2` varchar(100) DEFAULT NULL,
  `landmark` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `gstn` varchar(250) DEFAULT NULL,
  `pan` varchar(20) DEFAULT NULL,
  `number_of_shareholder` int NOT NULL,
  `purchase_email` varchar(250) DEFAULT NULL,
  `purchase_contact_number` varchar(20) DEFAULT NULL,
  `accounts_email` varchar(250) DEFAULT NULL,
  `accounts_contact_number` varchar(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `company` (`id`, `company_name`, `company_type`, `address_line_1`, `address_line_2`, `landmark`, `city`, `state`, `gstn`, `pan`, `number_of_shareholder`, `purchase_email`, `purchase_contact_number`, `accounts_email`, `accounts_contact_number`, `created_at`, `updated_at`) VALUES
(1, 'Company 1', 'llp', 'Address Line 1', 'Address Line 2', 'Jain college', 'Belgaum', 'karnataka', 'GSTIN9809900i990j0', 'EAGPP3527K', 0, NULL, '9019802163', NULL, '9019802163', '2023-09-16 15:55:16.953082', '2023-09-16 15:55:17.005750'),
(2, 'Company 1', 'llp', 'Address Line 1', 'Address Line 2', 'Jain college', 'Belgaum', 'karnataka', 'GSTIN9809900i990j0', 'EAGPP3527K', 0, 'mayur.patil1211@gmail.com', '9019802163', 'mayur.patil1211@gmail.com', '9019802163', '2023-09-16 15:55:16.953082', '2023-09-16 15:55:17.005750'),
(4, 'Company 1', 'llp', 'Address Line 1', 'Address Line 2', 'Jain college', 'Belgaum', 'karnataka', 'GSTIN9809900i990j0', 'EAGPP3527K', 0, 'mayur.patil1211@gmail.com', '9019802163', 'mayur.patil1211@gmail.com', '9019802163', '2023-09-16 15:55:16.953082', '2023-09-16 15:55:17.005750'),
(5, 'Company 1', 'llp', 'Address Line 1', 'Address Line 2', 'Jain college', 'Belgaum', 'karnataka', 'GSTIN9809900i990j0', 'EAGPP3527K', 0, 'mayur.patil1211@gmail.com', '9019802163', 'mayur.patil1211@gmail.com', '9019802163', '2023-09-16 15:55:16.953082', '2023-09-16 15:55:17.005750'),
(6, 'Company 1', 'llp', 'Address Line 1', 'Address Line 2', 'Jain college', 'Belgaum', 'karnataka', 'GSTIN9809900i990j0', 'EAGPP3527K', 0, 'mayur.patil1211@gmail.com', '9019802163', 'mayur.patil1211@gmail.com', '9019802163', '2023-09-16 15:55:16.953082', '2023-09-16 15:55:17.005750');

CREATE TABLE IF NOT EXISTS `company_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cluster_id` bigint NOT NULL,
  `company_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_cluster_mapping_cluster_id_company_id_408a6a8b_uniq` (`cluster_id`,`company_id`),
  KEY `company_cluster_mapping_company_id_36a5bd63_fk_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `company_cluster_mapping` (`id`, `cluster_id`, `company_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-09-16 15:55:17.075345', '2023-09-16 15:55:17.113849'),
(2, 1, 2, '2023-09-16 15:55:17.075345', '2023-09-16 15:55:17.113849'),
(4, 1, 4, '2023-09-16 15:55:17.075345', '2023-09-16 15:55:17.113849'),
(5, 1, 5, '2023-09-16 15:55:17.075345', '2023-09-16 15:55:17.113849'),
(6, 1, 6, '2023-09-16 15:55:17.075345', '2023-09-16 15:55:17.113849');

CREATE TABLE IF NOT EXISTS `company_document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `document_key` varchar(250) NOT NULL,
  `document_url` longtext,
  `document_name` varchar(250) DEFAULT NULL,
  `document_description` longtext,
  `company_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_document_company_id_dc57b340_fk_company_id` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `company_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_type` varchar(100) NOT NULL,
  `company_type_description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `company_user_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_user_mapping_user_id_company_id_6eb40562_uniq` (`user_id`,`company_id`),
  KEY `company_user_mapping_company_id_954f327e_fk_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `company_user_mapping` (`id`, `company_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 2, 2, '2023-09-16 15:55:17.212716', '2023-09-16 15:55:17.246794'),
(2, 4, 2, '2023-09-16 15:55:17.212716', '2023-09-16 15:55:17.246794'),
(3, 5, 2, '2023-09-16 15:55:17.212716', '2023-09-16 15:55:17.246794'),
(4, 2, 3, '2023-09-16 15:55:17.212716', '2023-09-16 15:55:17.246794'),
(5, 6, 2, '2023-09-16 15:55:17.212716', '2023-09-16 15:55:17.246794');

CREATE TABLE IF NOT EXISTS `default_variable_charges` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variable_charge_code` varchar(240) NOT NULL,
  `variable_charge` double NOT NULL,
  `variable_charge_description` varchar(240) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `latest` tinyint(1) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `variable_charge_code` (`variable_charge_code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `default_variable_charges` (`id`, `variable_charge_code`, `variable_charge`, `variable_charge_description`, `created_at`, `deleted`, `latest`, `updated_at`) VALUES
(2, 'Fuel-Charge', 5, 'Fuel Charge', '2023-11-04 04:26:25.997060', 0, 1, '2023-11-04 04:26:25.997093');

CREATE TABLE IF NOT EXISTS `department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_uid` varchar(20) NOT NULL,
  `department_name` varchar(250) NOT NULL,
  `department_type` varchar(250) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `target_food_cost` double NOT NULL,
  `brand_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `department_uid` (`department_uid`),
  KEY `department_brand_id_e15182a7_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `department` (`id`, `department_uid`, `department_name`, `department_type`, `created_at`, `updated_at`, `target_food_cost`, `brand_id`) VALUES
(2, 'DEPT_Kitchen', 'Kitchen', 'non-production', '2023-09-16 15:55:17.274878', '2023-09-16 15:55:17.321054', 0, NULL),
(3, 'DEPT1_Kitchen', 'Kitchen', 'non-production', '2023-10-06 18:26:51.657244', '2023-10-06 18:26:51.657280', 10, NULL),
(4, 'DEPT2_Kitchen', 'Kitchen', 'non-production', '2023-10-13 16:12:47.453543', '2023-10-13 16:12:47.453581', 10, 1),
(5, 'DEPT3_Kitchen', 'Kitchen', 'non-production', '2023-10-13 16:15:57.656773', '2023-10-13 16:15:57.656805', 10, 1);

CREATE TABLE IF NOT EXISTS `department_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cluster_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `food_cost` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_app_departmen_cluster_id_5d0fb170_fk_clusters_` (`cluster_id`),
  KEY `master_app_departmen_department_id_801b6e73_fk_departmen` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `department_cluster_mapping` (`id`, `cluster_id`, `department_id`, `created_at`, `updated_at`, `food_cost`) VALUES
(2, 1, 2, '2023-09-16 15:55:17.374376', '2023-09-16 15:55:17.427738', NULL),
(3, 1, 3, '2023-10-06 18:26:51.666625', '2023-10-06 18:26:51.666647', NULL),
(4, 1, 4, '2023-10-13 16:12:47.477450', '2023-10-13 16:12:47.477480', NULL),
(5, 1, 5, '2023-10-13 16:15:57.664966', '2023-10-13 16:15:57.664994', 12);

CREATE TABLE IF NOT EXISTS `department_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_type` varchar(100) NOT NULL,
  `department_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `department_types_brand_id_1e8413da_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_id` (`user_id`)
) ;

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(9, 'auth_app', 'permissions'),
(10, 'auth_app', 'rolepermission'),
(11, 'auth_app', 'roles'),
(8, 'auth_app', 'user'),
(12, 'auth_app', 'userroles'),
(4, 'contenttypes', 'contenttype'),
(82, 'master_app', 'assetinvetorydeptmapping'),
(83, 'master_app', 'assetinvetoryposmapping'),
(84, 'master_app', 'assetinvetoryregistrationmodel'),
(85, 'master_app', 'assettypes'),
(46, 'master_app', 'b2bclientbankdetails'),
(49, 'master_app', 'b2bclientbrandmapping'),
(48, 'master_app', 'b2bclientclustermapping'),
(47, 'master_app', 'b2bclientposmapping'),
(62, 'master_app', 'b2bratesdefinition'),
(13, 'master_app', 'brand'),
(34, 'master_app', 'brandclustermapping'),
(45, 'master_app', 'btobclient'),
(14, 'master_app', 'categorylist'),
(15, 'master_app', 'clusters'),
(16, 'master_app', 'company'),
(33, 'master_app', 'companyclusermapping'),
(30, 'master_app', 'companydocuments'),
(32, 'master_app', 'companyshareholder'),
(17, 'master_app', 'companytypes'),
(69, 'master_app', 'defaultvariablecharges'),
(18, 'master_app', 'department'),
(35, 'master_app', 'departmentclustermapping'),
(19, 'master_app', 'departmenttypes'),
(20, 'master_app', 'employmenttypes'),
(65, 'master_app', 'finalproductpriceforpos'),
(56, 'master_app', 'finalproductregistrationmodel'),
(58, 'master_app', 'finalproductsellingprice'),
(59, 'master_app', 'finalproducttags'),
(21, 'master_app', 'highvalueitemtypes'),
(61, 'master_app', 'hsncodetags'),
(60, 'master_app', 'hsntaxinformation'),
(22, 'master_app', 'industrytypes'),
(36, 'master_app', 'pos'),
(44, 'master_app', 'poscompanymapping'),
(43, 'master_app', 'posdepartmentmapping'),
(77, 'master_app', 'possubdepartmentmapping'),
(23, 'master_app', 'postypes'),
(24, 'master_app', 'prioritiytypes'),
(25, 'master_app', 'producttypes'),
(64, 'master_app', 'rawmaterialdeptmapping'),
(63, 'master_app', 'rawmaterialposmapping'),
(55, 'master_app', 'rawmaterialregistrationmodel'),
(75, 'master_app', 'rawmaterialtags'),
(72, 'master_app', 'recipeingredients'),
(70, 'master_app', 'reciperegistration'),
(71, 'master_app', 'recipevariablecharges'),
(54, 'master_app', 'semiproductregistrationmodel'),
(74, 'master_app', 'semiproducttags'),
(68, 'master_app', 'servicematerialdeptmapping'),
(67, 'master_app', 'servicematerialposmapping'),
(66, 'master_app', 'servicematerialregistrationmodel'),
(26, 'master_app', 'severitytypes'),
(50, 'master_app', 'store'),
(53, 'master_app', 'storebrandmapping'),
(52, 'master_app', 'storeclustermapping'),
(51, 'master_app', 'storeemployee'),
(80, 'master_app', 'storeposmapping'),
(73, 'master_app', 'storetypes'),
(29, 'master_app', 'subcategorylist'),
(76, 'master_app', 'subdepartment'),
(27, 'master_app', 'unitofmeasurement'),
(31, 'master_app', 'userbrandmapping'),
(39, 'master_app', 'vendorbankdetails'),
(79, 'master_app', 'vendorbankdocuments'),
(42, 'master_app', 'vendorbrandmapping'),
(40, 'master_app', 'vendorclustermapping'),
(38, 'master_app', 'vendordocuments'),
(41, 'master_app', 'vendorposmapping'),
(57, 'master_app', 'vendorpricingrawmaterial'),
(81, 'master_app', 'vendorpricingupdatelog'),
(37, 'master_app', 'vendors'),
(28, 'master_app', 'vendortypes'),
(5, 'sessions', 'session'),
(6, 'token_blacklist', 'blacklistedtoken'),
(7, 'token_blacklist', 'outstandingtoken');

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-11-25 06:24:56.383176'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-11-25 06:24:56.544523'),
(3, 'auth', '0001_initial', '2023-11-25 06:24:57.423237'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-11-25 06:24:57.563797'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-11-25 06:24:57.583929'),
(6, 'auth', '0004_alter_user_username_opts', '2023-11-25 06:24:57.602741'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-11-25 06:24:57.614094'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-11-25 06:24:57.621985'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-11-25 06:24:57.633737'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-11-25 06:24:57.643236'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-11-25 06:24:57.653599'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-11-25 06:24:57.677227'),
(13, 'auth', '0011_update_proxy_permissions', '2023-11-25 06:24:57.686913'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-11-25 06:24:57.696635'),
(15, 'auth_app', '0001_initial', '2023-11-25 06:24:58.658089'),
(16, 'admin', '0001_initial', '2023-11-25 06:24:59.025535'),
(17, 'admin', '0002_logentry_remove_auto_add', '2023-11-25 06:24:59.053843'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-25 06:24:59.081758'),
(19, 'auth_app', '0002_permissions_rolepermission_roles_userroles_and_more', '2023-11-25 06:25:00.611605'),
(20, 'auth_app', '0003_rolepermission_created_at_rolepermission_updated_at_and_more', '2023-11-25 06:25:00.875912'),
(21, 'master_app', '0001_initial', '2023-11-25 06:25:03.953427'),
(22, 'master_app', '0002_departmentclustermapping', '2023-11-25 06:25:04.272506'),
(23, 'master_app', '0003_pos_vendors_alter_departmentclustermapping_table_and_more', '2023-11-25 06:25:04.826668'),
(24, 'master_app', '0004_vendorclustermapping', '2023-11-25 06:25:05.142539'),
(25, 'master_app', '0005_alter_vendorbankdetails_vendor', '2023-11-25 06:25:05.175938'),
(26, 'master_app', '0006_vendorposmapping_vendorbrandmapping', '2023-11-25 06:25:05.849509'),
(27, 'master_app', '0007_pos_cluster_posdepartmentmapping_poscompanymapping', '2023-11-25 06:25:06.662314'),
(28, 'master_app', '0007_alter_vendorbankdetails_account_number', '2023-11-25 06:25:06.677424'),
(29, 'master_app', '0008_merge_20230902_0655', '2023-11-25 06:25:06.689542'),
(30, 'master_app', '0009_btobclient_alter_poscompanymapping_unique_together_and_more', '2023-11-25 06:25:07.098621'),
(31, 'master_app', '0010_alter_vendorbankdetails_account_number_and_more', '2023-11-25 06:25:08.115259'),
(32, 'master_app', '0011_b2bratesdefination', '2023-11-25 06:25:08.177234'),
(33, 'master_app', '0012_store_alter_b2bratesdefination_item_code_and_more', '2023-11-25 06:25:08.613770'),
(34, 'master_app', '0013_storeclustermapping_storebrandmapping_and_more', '2023-11-25 06:25:10.411965'),
(35, 'master_app', '0014_categorylist_brand_departmenttypes_brand_and_more', '2023-11-25 06:25:11.949656'),
(36, 'master_app', '0015_remove_finalproductregistrationmodel_b2b_selling_price_and_more', '2023-11-25 06:25:20.413999'),
(37, 'master_app', '0016_finalproductregistrationmodel_brand_and_more', '2023-11-25 06:25:21.335868'),
(38, 'master_app', '0017_hsntaxinformation_hsncodetags', '2023-11-25 06:25:21.768101'),
(39, 'master_app', '0018_alter_finalproducttags_final_product', '2023-11-25 06:25:21.807650'),
(40, 'master_app', '0019_b2bratesdefinition_delete_b2bratesdefination', '2023-11-25 06:25:22.240234'),
(41, 'master_app', '0020_remove_finalproductregistrationmodel_product_type_and_more', '2023-11-25 06:25:24.559218'),
(42, 'master_app', '0021_servicematerialregistrationmodel_and_more', '2023-11-25 06:25:25.682784'),
(43, 'master_app', '0022_department_brand_departmentclustermapping_food_cost_and_more', '2023-11-25 06:25:26.145140'),
(44, 'master_app', '0023_rename_created_date_store_created_at_and_more', '2023-11-25 06:25:26.342207'),
(45, 'master_app', '0024_defaultvariablecharges_reciperegistration_and_more', '2023-11-25 06:25:28.360080'),
(46, 'master_app', '0025_defaultvariablecharges_created_at_and_more', '2023-11-25 06:25:28.615036'),
(47, 'master_app', '0026_reciperegistration_approved_and_more', '2023-11-25 06:25:28.887706'),
(48, 'master_app', '0027_storetypes', '2023-11-25 06:25:29.101426'),
(49, 'master_app', '0028_semiproducttags_rawmaterialtags', '2023-11-25 06:25:29.522628'),
(50, 'master_app', '0029_subdepartment', '2023-11-25 06:25:29.730328'),
(51, 'sessions', '0001_initial', '2023-11-25 06:25:29.910387'),
(52, 'token_blacklist', '0001_initial', '2023-11-25 06:25:30.355749'),
(53, 'token_blacklist', '0002_outstandingtoken_jti_hex', '2023-11-25 06:25:30.415008'),
(54, 'token_blacklist', '0003_auto_20171017_2007', '2023-11-25 06:25:30.447532'),
(55, 'token_blacklist', '0004_auto_20171017_2013', '2023-11-25 06:25:30.655023'),
(56, 'token_blacklist', '0005_remove_outstandingtoken_jti', '2023-11-25 06:25:30.801794'),
(57, 'token_blacklist', '0006_auto_20171017_2113', '2023-11-25 06:25:30.906671'),
(58, 'token_blacklist', '0007_auto_20171017_2214', '2023-11-25 06:25:31.355920'),
(59, 'token_blacklist', '0008_migrate_to_bigautofield', '2023-11-25 06:25:32.014895'),
(60, 'token_blacklist', '0010_fix_migrate_to_bigautofield', '2023-11-25 06:25:32.067225'),
(61, 'token_blacklist', '0011_linearizes_history', '2023-11-25 06:25:32.075423'),
(62, 'token_blacklist', '0012_alter_outstandingtoken_user', '2023-11-25 06:25:32.108900'),
(63, 'master_app', '0030_possubdepartmentmapping', '2023-12-02 06:45:26.368249'),
(64, 'master_app', '0031_brand_required_sub_department_vendorbankdocuments_and_more', '2023-12-02 11:41:55.192478'),
(65, 'master_app', '0032_remove_hsntaxinformation_brand_and_more', '2023-12-02 16:19:37.502488'),
(66, 'master_app', '0033_assetinvetorydeptmapping_assetinvetoryposmapping_and_more', '2023-12-02 16:33:11.358447'),
(67, 'master_app', '0034_assettypes', '2023-12-02 16:50:01.165882'),
(68, 'master_app', '0035_assetinvetoryregistrationmodel_asset_type', '2023-12-02 16:55:18.324476');

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('dirnwuh0fbt7k7b41djn6nwoiq9h4py8', '.eJxVjDsOwjAQBe_iGln-fyjpOYO1u7ZxADlSnFSIu0OkFNC-mXkvlmBbW9pGWdKU2ZlJdvrdEOhR-g7yHfpt5jT3dZmQ7wo_6ODXOZfn5XD_DhqM9q1tiaSqNNU6oyUU4RTpoGUkmQVm5Z0lI6I3gIpMxuhLDRBkrdpqhYG9P9NRN6E:1qqxoj:5Rga-P3txuoCahnJKqnis6jSiJ5QnIHHlDWTl1V_nJU', '2023-10-26 15:41:41.578752');

CREATE TABLE IF NOT EXISTS `employment_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employment_type` varchar(100) NOT NULL,
  `employment_type_description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `final_product_price_pos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `final_product_id` bigint NOT NULL,
  `pos_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `final_product_price_pos_final_product_id_pos_id_fb3b307f_uniq` (`final_product_id`,`pos_id`),
  KEY `final_product_price_pos_pos_id_7e383ac5_fk_pos_id` (`pos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `final_product_price_pos` (`id`, `price`, `created_at`, `updated_at`, `final_product_id`, `pos_id`) VALUES
(1, 110, '2023-10-06 17:55:15.520651', '2023-10-06 17:57:41.394748', 2, 1);

CREATE TABLE IF NOT EXISTS `final_product_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_code` varchar(20) DEFAULT NULL,
  `item_name` varchar(250) NOT NULL,
  `default_uom` varchar(20) DEFAULT NULL,
  `production_cycle` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `sub_category` varchar(50) DEFAULT NULL,
  `recipe_unit` varchar(50) DEFAULT NULL,
  `yield_quantity` double DEFAULT NULL,
  `yield_quantity_cost` double DEFAULT NULL,
  `food_cost` double DEFAULT NULL,
  `life_cycle` double DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `high_value_item` tinyint(1) DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `available_for_cluster` tinyint(1) NOT NULL,
  `ratail_tax` double DEFAULT NULL,
  `b2b_tax` double DEFAULT NULL,
  `hsn_code` varchar(50) DEFAULT NULL,
  `cost_center_department_id` bigint DEFAULT NULL,
  `production_department_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `final_product_regist_cost_center_departme_abdef765_fk_departmen` (`cost_center_department_id`),
  KEY `final_product_regist_production_departmen_9455aff7_fk_departmen` (`production_department_id`),
  KEY `final_product_registration_brand_id_8086abd2_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `final_product_registration` (`id`, `item_code`, `item_name`, `default_uom`, `production_cycle`, `category`, `sub_category`, `recipe_unit`, `yield_quantity`, `yield_quantity_cost`, `food_cost`, `life_cycle`, `expiry_date`, `high_value_item`, `priority`, `severity`, `available_for_cluster`, `ratail_tax`, `b2b_tax`, `hsn_code`, `cost_center_department_id`, `production_department_id`, `created_at`, `updated_at`, `brand_id`) VALUES
(2, 'FP_001', 'Final Product update 1', 'KG', 'Local', 'Category 1', 'Subscategory 1', 'KG', 10, 100, 150, 30, '2023-04-19', 1, 'P2', 'S3', 1, 15, 16, 'HSN_939939030', 2, 2, '2023-09-17 06:24:54.509387', '2023-09-17 06:25:51.873683', 1);

CREATE TABLE IF NOT EXISTS `final_product_selling_price` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `b2b_client_id` bigint DEFAULT NULL,
  `department_id` bigint DEFAULT NULL,
  `final_product_id` bigint NOT NULL,
  `pos_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `final_product_sellin_b2b_client_id_f5ecb4a8_fk_b2b_clien` (`b2b_client_id`),
  KEY `final_product_sellin_department_id_b72f2aa3_fk_departmen` (`department_id`),
  KEY `final_product_sellin_final_product_id_eb4bcbc9_fk_final_pro` (`final_product_id`),
  KEY `final_product_selling_price_pos_id_c48314ff_fk_pos_id` (`pos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `final_product_selling_price` (`id`, `price`, `created_at`, `updated_at`, `b2b_client_id`, `department_id`, `final_product_id`, `pos_id`) VALUES
(1, 100, '2023-09-17 08:06:03.501621', '2023-09-17 08:08:08.976416', NULL, 2, 2, NULL),
(2, 100, '2023-09-17 08:08:18.039135', '2023-09-17 08:08:18.039156', NULL, NULL, 2, 1),
(3, 100, '2023-09-17 08:09:17.800696', '2023-09-17 08:09:17.800715', 2, NULL, 2, NULL);

CREATE TABLE IF NOT EXISTS `final_product_tags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag` varchar(140) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `final_product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `final_product_tags_final_product_id_670fe1fc_fk_final_pro` (`final_product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `final_product_tags` (`id`, `tag`, `created_at`, `updated_at`, `final_product_id`) VALUES
(1, 'Milk', '2023-09-17 06:24:54.522250', '2023-09-17 06:24:54.522278', 2),
(2, 'Raw Milk', '2023-09-17 06:24:54.527889', '2023-09-17 06:24:54.527909', 2),
(3, 'Cow Milk', '2023-09-17 06:25:51.881205', '2023-09-17 06:25:51.881223', 2);

CREATE TABLE IF NOT EXISTS `high_value_item_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `high_value_item_type` varchar(100) NOT NULL,
  `high_value_item_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `high_value_item_types_brand_id_5b4ec85e_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `hsn_codes` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hsn_code` varchar(240) NOT NULL,
  `hsn_code_description` longtext,
  `cgst` double NOT NULL,
  `sgst` double NOT NULL,
  `igst` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `hsn_codes` (`id`, `hsn_code`, `hsn_code_description`, `cgst`, `sgst`, `igst`, `created_at`, `updated_at`) VALUES
(1, 'hsn09j0i0u098', 'chocolate, choco', 12, 18, 15, '2023-09-17 05:02:41.530693', '2023-09-17 05:02:41.530712'),
(2, 'hsn09j0i0u098', 'chocolate, choco', 12, 18, 15, '2023-09-17 05:05:52.666166', '2023-09-17 05:46:28.435177');

CREATE TABLE IF NOT EXISTS `hsn_code_tags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag` varchar(240) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `hsn_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hsn_code_tags_hsn_id_b06e5cf6_fk_hsn_codes_id` (`hsn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `hsn_code_tags` (`id`, `tag`, `created_at`, `updated_at`, `hsn_id`) VALUES
(1, 'chocolate', '2023-09-17 05:02:41.538419', '2023-09-17 05:02:41.538439', 1),
(2, 'choco', '2023-09-17 05:02:41.542701', '2023-09-17 05:02:41.542717', 1),
(3, 'chocolate', '2023-09-17 05:05:52.672324', '2023-09-17 05:05:52.672342', 2),
(4, 'choco', '2023-09-17 05:05:52.677401', '2023-09-17 05:05:52.677419', 2),
(5, 'black forest', '2023-09-17 05:46:28.442208', '2023-09-17 05:46:28.442224', 2),
(6, 'milkcake', '2023-09-17 05:46:28.446834', '2023-09-17 05:46:28.446851', 2);

CREATE TABLE IF NOT EXISTS `industry_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `industry_type` varchar(50) NOT NULL,
  `industry_type_description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `permission_description` varchar(240) NOT NULL,
  `permission_code` varchar(240) NOT NULL,
  `in_action` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_permission_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `permissions_permiss_b856ed_idx` (`permission_code`,`parent_permission_id`),
  KEY `permissions_permiss_fee52e_idx` (`permission_code`),
  KEY `permissions_parent__78f9f6_idx` (`parent_permission_id`),
  KEY `permissions_permiss_82cf6d_idx` (`permission_description`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `permissions` (`id`, `permission_description`, `permission_code`, `in_action`, `created_at`, `updated_at`, `parent_permission_id`) VALUES
(1, 'permission description update', 'register_types', 0, '2023-08-15 06:11:01.234780', '2023-10-12 15:52:46.632294', NULL),
(2, 'Register B2B client', 'register_b2b_client', 1, '2023-08-15 06:11:01.234780', '2023-08-15 06:11:01.234780', NULL),
(3, 'Update B2B client', 'update_b2b_client', 1, '2023-08-15 06:11:01.234780', '2023-08-15 06:11:01.234780', NULL),
(4, 'List B2B client', 'list_b2b_client', 1, '2023-08-15 06:11:01.234780', '2023-08-15 06:11:01.234780', NULL),
(5, 'Delete B2B client', 'delete_b2b_client', 1, '2023-08-15 06:11:01.234780', '2023-08-15 06:11:01.234780', NULL);

CREATE TABLE IF NOT EXISTS `pos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pos_code` varchar(50) NOT NULL,
  `pos_name` varchar(100) NOT NULL,
  `pos_type` varchar(100) NOT NULL,
  `address` longtext,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `cluster_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_cluster_id_5fad0e30_fk_clusters_id` (`cluster_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `pos` (`id`, `pos_code`, `pos_name`, `pos_type`, `address`, `contact_number`, `email`, `cluster_id`, `created_at`, `updated_at`) VALUES
(1, 'CK_BGM', 'Central Kitchen', 'Cafe', 'Tilakwadi, Belgaum', '9019802163', 'mayur.patil1211@gmail.com', 1, '2023-09-16 15:55:17.721358', '2023-09-16 15:55:17.766840'),
(3, 'CK_BGM', 'Central Kitchen', 'Cafe', 'Tilakwadi, Belgaum', '9019802163', 'mayur.patil1211@gmail.com', 1, '2023-09-16 15:55:17.721358', '2023-09-16 15:55:17.766840'),
(4, 'CK_BGM', 'Central Kitchen', 'Cafe', 'Tilakwadi, Belgaum', '9019802163', 'mayur.patil1211@gmail.com', 1, '2023-09-16 15:55:17.721358', '2023-09-16 15:55:17.766840'),
(5, 'CK_BGM', 'Central Kitchen', 'Cafe', 'Tilakwadi, Belgaum', '9019802163', 'mayur.patil1211@gmail.com', 1, '2023-09-16 15:55:17.721358', '2023-09-16 15:55:17.766840'),
(6, 'CK_BGM', 'Central Kitchen', 'Cafe', 'Tilakwadi, Belgaum', '9019802163', 'mayur.patil1211@gmail.com', 1, '2023-09-16 15:55:17.721358', '2023-09-16 15:55:17.766840');

CREATE TABLE IF NOT EXISTS `pos_company_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` bigint NOT NULL,
  `pos_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pos_company_mapping_pos_id_company_id_09560fb3_uniq` (`pos_id`,`company_id`),
  KEY `pos_company_mapping_company_id_1ffbc0e9_fk_company_id` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `pos_company_mapping` (`id`, `company_id`, `pos_id`, `created_at`, `updated_at`) VALUES
(1, 1, 5, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377'),
(2, 2, 5, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377'),
(3, 2, 1, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377'),
(4, 4, 1, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377'),
(5, 6, 5, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377'),
(6, 6, 4, '2023-09-16 15:55:17.824726', '2023-09-16 15:55:17.856377');

CREATE TABLE IF NOT EXISTS `pos_department_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_id` bigint NOT NULL,
  `pos_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pos_department_mapping_pos_id_department_id_69c3f26d_uniq` (`pos_id`,`department_id`),
  KEY `pos_department_mapping_department_id_563fcd02_fk_department_id` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `pos_department_mapping` (`id`, `department_id`, `pos_id`, `created_at`, `updated_at`) VALUES
(1, 2, 5, '2023-09-16 15:55:17.883205', '2023-09-16 15:55:17.932714'),
(2, 2, 1, '2023-09-16 15:55:17.883205', '2023-09-16 15:55:17.932714'),
(3, 3, 1, '2023-12-02 11:16:44.384011', '2023-12-02 11:16:44.384026');

CREATE TABLE IF NOT EXISTS `pos_sub_department_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `pos_id` bigint NOT NULL,
  `sub_department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pos_sub_department_mappi_pos_id_sub_department_id_721501a6_uniq` (`pos_id`,`sub_department_id`),
  KEY `pos_sub_department_m_sub_department_id_40c9472b_fk_sub_depar` (`sub_department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `pos_sub_department_mapping` (`id`, `created_date`, `updated_date`, `pos_id`, `sub_department_id`) VALUES
(1, '2023-12-02 11:16:44.361614', '2023-12-02 11:16:44.361633', 1, 1),
(2, '2023-12-02 11:16:44.373007', '2023-12-02 11:16:44.373023', 1, 2),
(3, '2023-12-02 11:16:44.394022', '2023-12-02 11:16:44.394042', 1, 5);

CREATE TABLE IF NOT EXISTS `pos_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pos_type` varchar(100) NOT NULL,
  `pos_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pos_types_brand_id_f87e01da_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `priority_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `priority_type` varchar(100) NOT NULL,
  `priority_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `priority_types_brand_id_1d03d200_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `product_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_type` varchar(100) NOT NULL,
  `product_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_types_brand_id_8161fd42_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `raw_material_dept_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `department_id` bigint NOT NULL,
  `raw_material_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raw_material_dept_mappin_raw_material_id_departme_6526e241_uniq` (`raw_material_id`,`department_id`),
  KEY `raw_material_dept_ma_department_id_c39722a4_fk_departmen` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `raw_material_dept_mapping` (`id`, `created_at`, `updated_at`, `department_id`, `raw_material_id`) VALUES
(1, '2023-10-06 17:28:40.956366', '2023-10-06 17:28:40.956390', 2, 6),
(2, '2023-11-17 11:35:26.748935', '2023-11-17 11:35:26.748961', 2, 8),
(3, '2023-11-18 14:21:56.805927', '2023-11-18 14:21:56.805970', 2, 9),
(4, '2023-11-18 14:22:33.398964', '2023-11-18 14:22:33.399006', 2, 10),
(5, '2023-11-18 14:24:44.046373', '2023-11-18 14:24:44.046425', 2, 11);

CREATE TABLE IF NOT EXISTS `raw_material_pos_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pos_id` bigint NOT NULL,
  `raw_material_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raw_material_pos_mapping_raw_material_id_pos_id_20bd434e_uniq` (`raw_material_id`,`pos_id`),
  KEY `raw_material_pos_mapping_pos_id_bbe1dc26_fk_pos_id` (`pos_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `raw_material_pos_mapping` (`id`, `created_at`, `updated_at`, `pos_id`, `raw_material_id`) VALUES
(1, '2023-10-06 17:23:54.037660', '2023-10-06 17:23:54.037683', 1, 6),
(2, '2023-11-17 11:35:16.508091', '2023-11-17 11:35:16.508111', 1, 7),
(3, '2023-11-17 11:35:26.757255', '2023-11-17 11:35:26.757277', 1, 8),
(4, '2023-11-18 14:21:56.815837', '2023-11-18 14:21:56.815876', 1, 9),
(5, '2023-11-18 14:22:33.406910', '2023-11-18 14:22:33.406938', 1, 10),
(6, '2023-11-18 14:24:44.110041', '2023-11-18 14:24:44.110084', 1, 11);

CREATE TABLE IF NOT EXISTS `raw_material_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_code` varchar(20) DEFAULT NULL,
  `item_name` varchar(250) NOT NULL,
  `default_uom` varchar(20) DEFAULT NULL,
  `tax` double DEFAULT NULL,
  `hsn_code` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `sub_category` varchar(50) DEFAULT NULL,
  `rate` double NOT NULL,
  `price` double NOT NULL,
  `recipe_unit` varchar(50) DEFAULT NULL,
  `flag_recipe_conversion_ratio` tinyint(1) NOT NULL,
  `recipe_conversion_ratio` double DEFAULT NULL,
  `recipe_rate` double NOT NULL,
  `recipe_price` double NOT NULL,
  `direct_selling` tinyint(1) NOT NULL,
  `life_cycle` double DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `high_value_item` tinyint(1) DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `available_for_cluster` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  `production` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `raw_material_registration_brand_id_c38edc0f_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `raw_material_registration` (`id`, `item_code`, `item_name`, `default_uom`, `tax`, `hsn_code`, `category`, `sub_category`, `rate`, `price`, `recipe_unit`, `flag_recipe_conversion_ratio`, `recipe_conversion_ratio`, `recipe_rate`, `recipe_price`, `direct_selling`, `life_cycle`, `expiry_date`, `high_value_item`, `priority`, `severity`, `available_for_cluster`, `created_at`, `updated_at`, `brand_id`, `production`) VALUES
(3, 'SM_001', 'Semi product 1', 'KG', NULL, NULL, 'category1', 'subcategory1', 0, 0, 'KG', 1, NULL, 0, 0, 0, 20, '2023-12-01', 1, 'P1', 'S1', 0, '2023-09-16 15:55:18.152576', '2023-09-16 15:55:18.197918', 1, 1),
(4, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-09-17 13:29:09.490066', '2023-09-17 13:29:09.490092', 1, 1),
(5, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-10-06 17:22:31.553741', '2023-10-06 17:22:31.553765', 1, 1),
(6, 'RM_001', 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, NULL, 'P1', 'S1', 0, '2023-10-06 17:23:54.023379', '2023-10-06 17:28:40.948544', 1, 1),
(7, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-11-17 11:35:16.488302', '2023-11-17 11:35:16.488322', 1, 1),
(8, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-11-17 11:35:26.740082', '2023-11-17 11:35:26.740104', 1, 1),
(9, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-11-18 14:21:56.790330', '2023-11-18 14:21:56.790361', 1, 1),
(10, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-11-18 14:22:33.386987', '2023-11-18 14:22:33.387032', 1, 1),
(11, NULL, 'Raw Material 1', 'KG', 18, 'HSN800979790', 'Category1', 'Subcategory1', 100, 120, 'KG', 1, 10, 100, 100, 1, 20, NULL, 1, 'P1', 'S1', 0, '2023-11-18 14:24:44.012558', '2023-11-18 14:24:44.012608', 1, 1);

CREATE TABLE IF NOT EXISTS `raw_material_tags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag` varchar(140) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `raw_material_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `raw_material_tags_raw_material_id_23fe5af3_fk_raw_mater` (`raw_material_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `raw_material_tags` (`id`, `tag`, `created_at`, `updated_at`, `raw_material_id`) VALUES
(1, 'tag1', '2023-11-17 11:35:16.513295', '2023-11-17 11:35:16.513316', 7),
(2, 'tag2', '2023-11-17 11:35:16.517256', '2023-11-17 11:35:16.517278', 7),
(3, 'tag1', '2023-11-17 11:35:26.762689', '2023-11-17 11:35:26.762711', 8),
(4, 'tag2', '2023-11-17 11:35:26.771730', '2023-11-17 11:35:26.771766', 8),
(7, 'tag1', '2023-11-18 14:21:56.825570', '2023-11-18 14:21:56.825612', 9),
(8, 'tag2', '2023-11-18 14:21:56.833088', '2023-11-18 14:21:56.833128', 9);

CREATE TABLE IF NOT EXISTS `recipe_ingredients` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ingredient_code` varchar(240) NOT NULL,
  `ingredient_name` varchar(240) NOT NULL,
  `uom` varchar(20) NOT NULL,
  `quantity` double NOT NULL,
  `price` double NOT NULL,
  `value` double NOT NULL,
  `yield_qauntity` double NOT NULL,
  `yield_production_value` double NOT NULL,
  `raw_material_id` bigint DEFAULT NULL,
  `recipe_id` bigint NOT NULL,
  `semi_product_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recipe_ingredients_raw_material_id_2340283a_fk_raw_mater` (`raw_material_id`),
  KEY `recipe_ingredients_recipe_id_f1590b33_fk_recipe_registration_id` (`recipe_id`),
  KEY `recipe_ingredients_semi_product_id_d227fb59_fk_semi_prod` (`semi_product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `recipe_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(240) NOT NULL,
  `item_code` varchar(240) NOT NULL,
  `product_type` varchar(240) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  `final_product_id` bigint DEFAULT NULL,
  `production_department_id` bigint DEFAULT NULL,
  `recipe_approved_by_id` bigint DEFAULT NULL,
  `recipe_entered_by_id` bigint DEFAULT NULL,
  `semi_product_id` bigint DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `approved_on` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recipe_registration_brand_id_0eb2cf58_fk_brand_id` (`brand_id`),
  KEY `recipe_registration_final_product_id_0a0f0042_fk_final_pro` (`final_product_id`),
  KEY `recipe_registration_production_departmen_7993934e_fk_departmen` (`production_department_id`),
  KEY `recipe_registration_recipe_approved_by_id_985d2b0c_fk_user_id` (`recipe_approved_by_id`),
  KEY `recipe_registration_recipe_entered_by_id_cfcf4221_fk_user_id` (`recipe_entered_by_id`),
  KEY `recipe_registration_semi_product_id_ec2360b5_fk_semi_prod` (`semi_product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `recipe_variable_charges` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variable_charge_code` varchar(240) NOT NULL,
  `variable_charge` double NOT NULL,
  `variable_charge_description` varchar(240) NOT NULL,
  `latest` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `recipe_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `recipe_variable_char_recipe_id_19cf0675_fk_recipe_re` (`recipe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(240) NOT NULL,
  `role_code` varchar(240) NOT NULL,
  `in_action` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `roles_role_co_bcb150_idx` (`role_code`,`role_name`),
  KEY `roles_role_co_be68ba_idx` (`role_code`),
  KEY `roles_role_na_cfef50_idx` (`role_name`),
  KEY `roles_in_acti_757fa7_idx` (`in_action`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `roles` (`id`, `role_name`, `role_code`, `in_action`, `created_at`, `updated_at`) VALUES
(1, 'Super admin', 'super_admin', 1, '2023-10-11 16:38:45.911448', '2023-10-11 16:44:36.925523'),
(2, 'admin', 'admin', 1, '2023-10-11 16:45:17.017813', '2023-10-11 16:45:17.017833');

CREATE TABLE IF NOT EXISTS `role_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `permission_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `role_permis_role_id_0ea48f_idx` (`role_id`),
  KEY `role_permis_permiss_96a6c9_idx` (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `role_permissions` (`id`, `permission_id`, `role_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-10-12 15:58:00.236117', '2023-10-12 15:58:00.236146'),
(2, 2, 1, '2023-10-12 15:58:00.242246', '2023-10-12 15:58:00.242274'),
(3, 1, 1, '2023-10-12 16:03:10.489075', '2023-10-12 16:03:10.489100'),
(4, 2, 1, '2023-10-12 16:03:10.496713', '2023-10-12 16:03:10.496753');

CREATE TABLE IF NOT EXISTS `semi_product_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_code` varchar(20) DEFAULT NULL,
  `item_name` varchar(250) NOT NULL,
  `default_uom` varchar(20) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `sub_category` varchar(50) DEFAULT NULL,
  `recipe_unit` varchar(50) DEFAULT NULL,
  `yield_quantity` double DEFAULT NULL,
  `yield_quantity_cost` double DEFAULT NULL,
  `food_cost` double DEFAULT NULL,
  `life_cycle` double DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `high_value_item` tinyint(1) DEFAULT NULL,
  `priority` varchar(50) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `available_for_cluster` tinyint(1) NOT NULL,
  `cost_center_department_id` bigint DEFAULT NULL,
  `production_department_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `semi_product_registr_cost_center_departme_a95b6e7b_fk_departmen` (`cost_center_department_id`),
  KEY `semi_product_registr_production_departmen_d953b622_fk_departmen` (`production_department_id`),
  KEY `semi_product_registration_brand_id_135d7dfe_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `semi_product_registration` (`id`, `item_code`, `item_name`, `default_uom`, `category`, `sub_category`, `recipe_unit`, `yield_quantity`, `yield_quantity_cost`, `food_cost`, `life_cycle`, `expiry_date`, `high_value_item`, `priority`, `severity`, `available_for_cluster`, `cost_center_department_id`, `production_department_id`, `created_at`, `updated_at`, `brand_id`) VALUES
(1, 'SM_001', 'Semi product 1', 'KG', 'category1', 'subcategory1', 'KG', 10, 30, 100, 20, '2023-12-01', 1, 'P1', 'S1', 0, 2, 2, '2023-09-17 13:41:13.361029', '2023-09-17 13:41:13.361044', 1),
(2, 'SM_001', 'Semi product 1', 'KG', 'category1', 'subcategory1', 'KG', 10, 30, 100, 20, '2023-12-01', 0, 'P1', 'S1', 0, 2, 2, '2023-11-17 11:28:22.875236', '2023-11-17 11:29:22.065984', 1);

CREATE TABLE IF NOT EXISTS `semi_product_tags` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag` varchar(140) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `semi_product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `semi_product_tags_semi_product_id_ce603ef2_fk_semi_prod` (`semi_product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `semi_product_tags` (`id`, `tag`, `created_at`, `updated_at`, `semi_product_id`) VALUES
(1, 'tag1', '2023-11-17 11:28:22.886625', '2023-11-17 11:28:22.886663', 2),
(2, 'tag2', '2023-11-17 11:28:22.891941', '2023-11-17 11:28:22.891964', 2);

CREATE TABLE IF NOT EXISTS `severity_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `severity_type` varchar(100) NOT NULL,
  `severity_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `severity_types_brand_id_e4f51a23_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `store` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_uid` varchar(50) NOT NULL,
  `store_type` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `store` (`id`, `store_uid`, `store_type`, `created_at`, `updated_at`) VALUES
(2, 'STORE1', 'Retail', '2023-10-19 16:50:07.097469', '2023-10-19 16:50:07.097496'),
(3, 'STORE1', 'Retail', '2023-10-19 17:11:11.435948', '2023-10-19 17:11:11.435988'),
(4, 'STORE1', 'Retail', '2023-10-19 17:13:34.364345', '2023-10-19 17:13:34.364377'),
(5, 'STORE1', 'Retail', '2023-10-19 17:14:32.250462', '2023-10-19 17:14:32.250487'),
(6, 'STORE1', 'Retail', '2023-10-19 17:14:33.000779', '2023-10-19 17:14:33.000812'),
(7, 'STORE1', 'Retail', '2023-10-19 17:14:33.771609', '2023-10-19 17:26:54.550935'),
(8, 'STORE1', 'pos_level', '2023-12-02 11:41:31.959017', '2023-12-02 11:41:31.959063'),
(9, 'STORE1', 'pos_level', '2023-12-02 11:42:00.720068', '2023-12-02 11:42:00.720089'),
(10, 'STORE1', 'cluster_level', '2023-12-02 11:43:15.631708', '2023-12-02 11:43:15.631739'),
(11, 'STORE1', 'brand_level', '2023-12-02 11:44:10.363957', '2023-12-02 11:44:10.363977');

CREATE TABLE IF NOT EXISTS `store_brand_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_id` bigint NOT NULL,
  `store_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_brand_mapping_brand_id_9837b250_fk_brand_id` (`brand_id`),
  KEY `store_brand_mapping_store_id_dcb62132_fk_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `store_brand_mapping` (`id`, `brand_id`, `store_id`, `created_at`, `updated_at`) VALUES
(1, 1, 4, '2023-10-19 17:13:34.371115', '2023-10-19 17:13:34.371136'),
(2, 1, 5, '2023-10-19 17:14:32.257084', '2023-10-19 17:14:32.257117'),
(3, 1, 6, '2023-10-19 17:14:33.004994', '2023-10-19 17:14:33.005010'),
(4, 1, 7, '2023-10-19 17:14:33.777981', '2023-10-19 17:14:33.777997'),
(5, 1, 11, '2023-12-02 11:44:10.374671', '2023-12-02 11:44:10.374685');

CREATE TABLE IF NOT EXISTS `store_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cluster_id` bigint NOT NULL,
  `store_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_cluster_mapping_cluster_id_9b597d79_fk_clusters_id` (`cluster_id`),
  KEY `store_cluster_mapping_store_id_5626706b_fk_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `store_cluster_mapping` (`id`, `cluster_id`, `store_id`, `created_at`, `updated_at`) VALUES
(1, 1, 4, '2023-10-19 17:13:34.376234', '2023-10-19 17:13:34.376254'),
(2, 1, 5, '2023-10-19 17:14:32.260928', '2023-10-19 17:14:32.260947'),
(3, 1, 6, '2023-10-19 17:14:33.009803', '2023-10-19 17:14:33.009818'),
(4, 1, 7, '2023-10-19 17:14:33.784006', '2023-10-19 17:14:33.784026'),
(5, 1, 10, '2023-12-02 11:43:15.643744', '2023-12-02 11:43:15.643764');

CREATE TABLE IF NOT EXISTS `store_employees` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_employees_store_id_7b4c3b73_fk_store_id` (`store_id`),
  KEY `store_employees_user_id_e3bd6028_fk_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `store_employees` (`id`, `store_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 2, 1, '2023-10-19 16:50:07.124793', '2023-10-19 16:50:07.124817'),
(2, 3, 1, '2023-10-19 17:11:11.459540', '2023-10-19 17:11:11.459571'),
(3, 4, 1, '2023-10-19 17:13:34.381140', '2023-10-19 17:13:34.381159'),
(4, 5, 1, '2023-10-19 17:14:32.267185', '2023-10-19 17:14:32.267209'),
(5, 6, 1, '2023-10-19 17:14:33.013644', '2023-10-19 17:14:33.013661'),
(7, 7, 2, '2023-10-19 17:26:54.557606', '2023-10-19 17:26:54.557626'),
(8, 7, 3, '2023-10-19 17:26:54.562476', '2023-10-19 17:26:54.562490'),
(9, 9, 1, '2023-12-02 11:42:00.738115', '2023-12-02 11:42:00.738131'),
(10, 11, 1, '2023-12-02 11:44:10.384634', '2023-12-02 11:44:10.384650');

CREATE TABLE IF NOT EXISTS `store_pos_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `pos_id` bigint NOT NULL,
  `store_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_pos_mapping_pos_id_5338b3f7_fk_pos_id` (`pos_id`),
  KEY `store_pos_mapping_store_id_496b6a14_fk_store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `store_pos_mapping` (`id`, `created_at`, `updated_at`, `pos_id`, `store_id`) VALUES
(1, '2023-12-02 11:42:00.729663', '2023-12-02 11:42:00.729679', 1, 9);

CREATE TABLE IF NOT EXISTS `store_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_types` varchar(50) NOT NULL,
  `store_type_description` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `brand_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store_type_brand_id_0726ed3c_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `sub_category_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sub_category_name` varchar(250) NOT NULL,
  `sub_category_type` varchar(250) NOT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_category_name` (`sub_category_name`),
  KEY `sub_category_list_brand_id_688ca258_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `sub_category_list` (`id`, `sub_category_name`, `sub_category_type`, `brand_id`, `created_at`, `updated_at`) VALUES
(1, 'Sub Category2', 'Production', NULL, '2023-09-17 04:08:12.807674', '2023-09-17 04:08:12.807702');

CREATE TABLE IF NOT EXISTS `sub_category_list_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subcategorylist_id` bigint NOT NULL,
  `categorylist_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_category_list_catego_subcategorylist_id_categ_c4fa5672_uniq` (`subcategorylist_id`,`categorylist_id`),
  KEY `sub_category_list_ca_categorylist_id_149c5ae3_fk_category_` (`categorylist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `sub_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sub_department_uid` varchar(20) NOT NULL,
  `sub_department_name` varchar(250) NOT NULL,
  `sub_department_type` varchar(250) DEFAULT NULL,
  `target_food_cost` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `parent_department_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sub_department_parent_department_id_86c95392_fk_department_id` (`parent_department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `sub_department` (`id`, `sub_department_uid`, `sub_department_name`, `sub_department_type`, `target_food_cost`, `created_at`, `updated_at`, `parent_department_id`) VALUES
(1, 'DEPT3_Kitchen', 'Kitchen', 'non-production', 10, '2023-12-02 10:53:44.096920', '2023-12-02 10:53:44.096939', 2),
(2, 'DEPT3_Kitchen', 'Kitchen', 'non-production', 10, '2023-12-02 10:53:45.037014', '2023-12-02 10:53:45.037037', 2),
(3, 'DEPT3_Kitchen', 'Kitchen', 'non-production', 10, '2023-12-02 10:53:45.956126', '2023-12-02 10:53:45.956142', 2),
(4, 'DEPT3_Kitchen', 'Kitchen', 'non-production', 10, '2023-12-02 10:57:26.299920', '2023-12-02 10:57:26.299941', 3),
(5, 'DEPT3_Kitchen', 'Kitchen', 'non-production', 10, '2023-12-02 10:57:27.575085', '2023-12-02 10:57:27.575100', 3);

CREATE TABLE IF NOT EXISTS `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `token_blacklist_outstandingtoken` (`id`, `token`, `created_at`, `expires_at`, `user_id`, `jti`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NzU1NjIzMSwiaWF0IjoxNjk2OTUxNDMxLCJqdGkiOiJlYjQyMzc1ZTkyZDQ0NGJkOTc2ODA4YjAxZTEyODk3MCIsInVzZXJfaWQiOjF9.aQJlWYiYpVtCFWabHfnDB4Fr-7Df4gtr8FwgLdPX4Eo', '2023-10-10 15:23:51.741235', '2023-10-17 15:23:51.000000', 1, 'eb42375e92d444bd976808b01e128970');

CREATE TABLE IF NOT EXISTS `unit_of_measurments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unit_name` varchar(20) NOT NULL,
  `unit_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unit_name` (`unit_name`),
  KEY `unit_of_measurments_brand_id_d3c0d063_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contact_number` varchar(13) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `address` varchar(250) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `pan` varchar(20) DEFAULT NULL,
  `adhar` varchar(30) DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `login_count` int NOT NULL,
  `blocked` tinyint(1) NOT NULL,
  `profile_picture_link` longtext,
  `profile_picture_key` varchar(100) DEFAULT NULL,
  `record_date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `user_usernam_01b047_idx` (`username`,`email`,`active`,`record_date`),
  KEY `user_usernam_b79065_idx` (`username`),
  KEY `user_email_7bbb4c_idx` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `user` (`id`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `name`, `username`, `email`, `contact_number`, `user_type`, `password`, `active`, `address`, `city`, `state`, `country`, `pan`, `adhar`, `last_login`, `login_count`, `blocked`, `profile_picture_link`, `profile_picture_key`, `record_date`) VALUES
(1, 1, '', '', 1, 1, '2023-08-15 06:11:01.234780', '', 'mayur', NULL, NULL, NULL, 'pbkdf2_sha256$390000$67PjFlQv6OLzQrMJjhGcaF$9TtXEjtRyt67sCj/0ipbQy7O8Eykj464Z2hkZcu1BdA=', 1, NULL, NULL, NULL, 'India', NULL, NULL, '2023-10-12 15:41:41.575279', 0, 0, NULL, NULL, NULL),
(2, 0, '', '', 0, 1, '2023-08-15 06:19:21.703347', 'Shareholder Name', 'shareholder@gmail.com', 'shareholder@gmail.com', '9019802163', 'shareholder', NULL, 1, 'peeranwadi', 'Belgaum', 'karnataka', 'india', 'EAGPP3527K', '345323455677', NULL, 0, 0, NULL, NULL, NULL),
(3, 0, '', '', 0, 1, '2023-08-15 06:53:29.269526', 'Shareholder1 Name', 'shareholder1@gmail.com', 'shareholder1@gmail.com', '9019802163', 'shareholder', NULL, 1, 'peeranwadi', 'Belgaum', 'karnataka', 'india', 'EAGPP3527K', '345323455677', NULL, 0, 0, NULL, NULL, NULL);

CREATE TABLE IF NOT EXISTS `user_brand_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_brand_mapping_user_id_brand_id_980406b1_uniq` (`user_id`,`brand_id`),
  KEY `user_brand_mapping_brand_id_f10474af_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `user_brand_mapping` (`id`, `brand_id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-09-16 15:55:18.880340', '2023-09-16 15:55:18.926880');

CREATE TABLE IF NOT EXISTS `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `user_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_roles_role_id_0b583b_idx` (`role_id`),
  KEY `user_roles_user_id_05df60_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id_7dc6e2e0_uniq` (`user_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vendors` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vendor_code` varchar(50) NOT NULL,
  `vendor_name` varchar(250) NOT NULL,
  `address_line_1` longtext,
  `address_line_2` longtext NOT NULL,
  `landmark` longtext,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `pan` varchar(20) DEFAULT NULL,
  `gstn` varchar(50) DEFAULT NULL,
  `vendor_type` varchar(100) DEFAULT NULL,
  `credit_period` double NOT NULL,
  `is_msme_registered` tinyint(1) NOT NULL,
  `msme_registration_number` varchar(250) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendors` (`id`, `vendor_code`, `vendor_name`, `address_line_1`, `address_line_2`, `landmark`, `city`, `state`, `contact_number`, `email`, `pan`, `gstn`, `vendor_type`, `credit_period`, `is_msme_registered`, `msme_registration_number`, `created_at`, `updated_at`) VALUES
(1, 'Vendor1', 'Vendor name', 'Vendor Address line 1', 'Vendor Address line 2', 'Vendor landmark', 'Vendor City', 'Vendor State', '9019802163', 'mayur.patil1211@gmail.com', 'EAGPP3527K', 'GSTIN9j9j99789', 'cluster', 180, 0, NULL, '2023-09-16 15:55:19.308011', '2023-09-16 15:55:19.353354'),
(2, 'Vendor1', 'Vendor name', 'Vendor Address line 1', 'Vendor Address line 2', 'Vendor landmark', 'Vendor City', 'Vendor State', '9019802163', 'mayur.patil1211@gmail.com', 'EAGPP3527K', 'GSTIN9j9j99789', 'cluster', 180, 0, NULL, '2023-09-16 15:55:19.308011', '2023-09-16 15:55:19.353354'),
(3, 'Vendor1', 'Vendor name', 'Vendor Address line 1', 'Vendor Address line 2', 'Vendor landmark updated', 'Vendor City', 'Vendor State', '9019802163', 'mayur.patil1211@gmail.com', 'EAGPP3527K', 'GSTIN9j9j99789', 'cluster', 180, 0, NULL, '2023-09-16 15:55:19.308011', '2023-09-16 15:55:19.353354');

CREATE TABLE IF NOT EXISTS `vendor_bank_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(240) DEFAULT NULL,
  `account_name` varchar(240) DEFAULT NULL,
  `account_number` varchar(240) DEFAULT NULL,
  `ifsc` varchar(50) DEFAULT NULL,
  `branch` varchar(240) DEFAULT NULL,
  `vendor_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_bank_details_vendor_id_9e022d03_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_bank_details` (`id`, `bank_name`, `account_name`, `account_number`, `ifsc`, `branch`, `vendor_id`, `created_at`, `updated_at`) VALUES
(1, 'HDFC', 'Current', '590119019802163', 'HDFCISN90909', 'Boxite Road', 1, '2023-09-16 15:55:18.954725', '2023-09-16 15:55:18.990393'),
(2, 'HDFC', 'Current', '590119019802163', 'HDFCISN90909', 'Boxite Road', 2, '2023-09-16 15:55:18.954725', '2023-09-16 15:55:18.990393'),
(3, 'HDFC', 'Current', '590119019802163', 'HDFCISN90909', 'Boxite Road', 3, '2023-09-16 15:55:18.954725', '2023-09-16 15:55:18.990393');

CREATE TABLE IF NOT EXISTS `vendor_bank_documents` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vendor_bank_id` bigint NOT NULL,
  `vendor_document_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_bank_document_vendor_bank_id_800d7a50_fk_vendor_ba` (`vendor_bank_id`),
  KEY `vendor_bank_document_vendor_document_id_262a54c9_fk_vendor_do` (`vendor_document_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vendor_brand_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `brand_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_brand_mapping_brand_id_6c2b934d_fk_brand_id` (`brand_id`),
  KEY `vendor_brand_mapping_vendor_id_ca168f59_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_brand_mapping` (`id`, `brand_id`, `vendor_id`, `created_at`, `updated_at`) VALUES
(1, 1, 2, '2023-09-16 15:55:19.022440', '2023-09-16 15:55:19.062238');

CREATE TABLE IF NOT EXISTS `vendor_cluster_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cluster_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_cluster_mapping_cluster_id_c5239424_fk_clusters_id` (`cluster_id`),
  KEY `vendor_cluster_mapping_vendor_id_aca00740_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_cluster_mapping` (`id`, `cluster_id`, `vendor_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2023-09-16 15:55:19.101674', '2023-09-16 15:55:19.142781');

CREATE TABLE IF NOT EXISTS `vendor_documents` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `document_key` varchar(250) NOT NULL,
  `document_url` longtext,
  `document_name` varchar(250) DEFAULT NULL,
  `document_description` longtext,
  `vendor_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_documents_vendor_id_bdd3a402_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vendor_pos_mapping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pos_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_pos_mapping_pos_id_5d3c64b4_fk_pos_id` (`pos_id`),
  KEY `vendor_pos_mapping_vendor_id_945992fe_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_pos_mapping` (`id`, `pos_id`, `vendor_id`, `created_at`, `updated_at`) VALUES
(1, 1, 3, '2023-09-16 15:55:19.229587', '2023-09-16 15:55:19.270229');

CREATE TABLE IF NOT EXISTS `vendor_raw_material_pricing` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rate` double NOT NULL,
  `price` double NOT NULL,
  `latest` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `raw_material_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_raw_material__raw_material_id_c990c277_fk_raw_mater` (`raw_material_id`),
  KEY `vendor_raw_material_pricing_vendor_id_df0c9ea5_fk_vendors_id` (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_raw_material_pricing` (`id`, `rate`, `price`, `latest`, `created_at`, `updated_at`, `raw_material_id`, `vendor_id`) VALUES
(1, 100, 120, 0, '2023-09-17 13:22:27.587968', '2023-09-17 13:22:27.587990', 3, 1),
(2, 130, 150, 1, '2023-09-17 13:22:36.105148', '2023-12-02 16:24:30.964819', 3, 1);

CREATE TABLE IF NOT EXISTS `vendor_raw_material_pricing_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `old_value` json DEFAULT NULL,
  `new_value` json DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vendor_pricing_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_raw_material__vendor_pricing_id_c726387d_fk_vendor_ra` (`vendor_pricing_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `vendor_raw_material_pricing_log` (`id`, `old_value`, `new_value`, `created_at`, `updated_at`, `vendor_pricing_id`) VALUES
(1, '{\"rate\": 130.0, \"price\": 150.0}', '{\"rate\": 130.0, \"price\": 150.0}', '2023-12-02 16:24:30.975055', '2023-12-02 16:24:30.975070', 2);

CREATE TABLE IF NOT EXISTS `vendor_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vendor_type` varchar(100) NOT NULL,
  `vendor_type_description` varchar(250) DEFAULT NULL,
  `brand_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_types_brand_id_b1385d19_fk_brand_id` (`brand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE `asset_inventory_dept_mapping`
  ADD CONSTRAINT `asset_inventory_dept_asset_inventory_id_ca50418d_fk_asset_inv` FOREIGN KEY (`asset_inventory_id`) REFERENCES `asset_inventory_registration` (`id`),
  ADD CONSTRAINT `asset_inventory_dept_department_id_106186e1_fk_departmen` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

ALTER TABLE `asset_inventory_pos_mapping`
  ADD CONSTRAINT `asset_inventory_pos__asset_inventory_id_699d82b0_fk_asset_inv` FOREIGN KEY (`asset_inventory_id`) REFERENCES `asset_inventory_registration` (`id`),
  ADD CONSTRAINT `asset_inventory_pos_mapping_pos_id_09f5ed80_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `asset_inventory_registration`
  ADD CONSTRAINT `asset_inventory_registration_brand_id_aa37bdff_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `asset_type_list`
  ADD CONSTRAINT `asset_type_list_brand_id_28d347a2_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

ALTER TABLE `b2b_client_bank_details`
  ADD CONSTRAINT `b2b_client_bank_details_client_id_2329542c_fk_b2b_client_id` FOREIGN KEY (`client_id`) REFERENCES `b2b_client` (`id`);

ALTER TABLE `b2b_rates_definition`
  ADD CONSTRAINT `b2b_rates_definition_b2b_client_id_b7ebc6ac_fk_b2b_client_id` FOREIGN KEY (`b2b_client_id`) REFERENCES `b2b_client` (`id`),
  ADD CONSTRAINT `b2b_rates_definition_final_product_id_6675053c_fk_final_pro` FOREIGN KEY (`final_product_id`) REFERENCES `final_product_registration` (`id`);

ALTER TABLE `brand_cluster_mapping`
  ADD CONSTRAINT `brand_cluster_mapping_brand_id_2dab1878_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `brand_cluster_mapping_cluster_id_7527b926_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`);

ALTER TABLE `category_list`
  ADD CONSTRAINT `category_list_brand_id_317e419d_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `client_brand_mapping`
  ADD CONSTRAINT `client_brand_mapping_brand_id_949405a8_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `client_brand_mapping_client_id_62f23759_fk_b2b_client_id` FOREIGN KEY (`client_id`) REFERENCES `b2b_client` (`id`);

ALTER TABLE `client_cluster_mapping`
  ADD CONSTRAINT `client_cluster_mapping_client_id_771bdb69_fk_b2b_client_id` FOREIGN KEY (`client_id`) REFERENCES `b2b_client` (`id`),
  ADD CONSTRAINT `client_cluster_mapping_cluster_id_3bd69803_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`);

ALTER TABLE `client_pos_mapping`
  ADD CONSTRAINT `client_pos_mapping_client_id_9d11c53b_fk_b2b_client_id` FOREIGN KEY (`client_id`) REFERENCES `b2b_client` (`id`),
  ADD CONSTRAINT `client_pos_mapping_pos_id_12711a82_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `company_cluster_mapping`
  ADD CONSTRAINT `company_cluster_mapping_cluster_id_8e8d5a22_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`),
  ADD CONSTRAINT `company_cluster_mapping_company_id_36a5bd63_fk_company_id` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);

ALTER TABLE `company_document`
  ADD CONSTRAINT `company_document_company_id_dc57b340_fk_company_id` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);

ALTER TABLE `company_user_mapping`
  ADD CONSTRAINT `company_user_mapping_company_id_954f327e_fk_company_id` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`),
  ADD CONSTRAINT `company_user_mapping_user_id_46f216ce_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `department`
  ADD CONSTRAINT `department_brand_id_e15182a7_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `department_cluster_mapping`
  ADD CONSTRAINT `master_app_departmen_cluster_id_5d0fb170_fk_clusters_` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`),
  ADD CONSTRAINT `master_app_departmen_department_id_801b6e73_fk_departmen` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

ALTER TABLE `department_types`
  ADD CONSTRAINT `department_types_brand_id_1e8413da_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `final_product_price_pos`
  ADD CONSTRAINT `final_product_price__final_product_id_eb338284_fk_final_pro` FOREIGN KEY (`final_product_id`) REFERENCES `final_product_registration` (`id`),
  ADD CONSTRAINT `final_product_price_pos_pos_id_7e383ac5_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `final_product_registration`
  ADD CONSTRAINT `final_product_regist_cost_center_departme_abdef765_fk_departmen` FOREIGN KEY (`cost_center_department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `final_product_regist_production_departmen_9455aff7_fk_departmen` FOREIGN KEY (`production_department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `final_product_registration_brand_id_8086abd2_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `final_product_selling_price`
  ADD CONSTRAINT `final_product_sellin_b2b_client_id_f5ecb4a8_fk_b2b_clien` FOREIGN KEY (`b2b_client_id`) REFERENCES `b2b_client` (`id`),
  ADD CONSTRAINT `final_product_sellin_department_id_b72f2aa3_fk_departmen` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `final_product_sellin_final_product_id_eb4bcbc9_fk_final_pro` FOREIGN KEY (`final_product_id`) REFERENCES `final_product_registration` (`id`),
  ADD CONSTRAINT `final_product_selling_price_pos_id_c48314ff_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `final_product_tags`
  ADD CONSTRAINT `final_product_tags_final_product_id_670fe1fc_fk_final_pro` FOREIGN KEY (`final_product_id`) REFERENCES `final_product_registration` (`id`);

ALTER TABLE `high_value_item_types`
  ADD CONSTRAINT `high_value_item_types_brand_id_5b4ec85e_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `hsn_code_tags`
  ADD CONSTRAINT `hsn_code_tags_hsn_id_b06e5cf6_fk_hsn_codes_id` FOREIGN KEY (`hsn_id`) REFERENCES `hsn_codes` (`id`);

ALTER TABLE `permissions`
  ADD CONSTRAINT `permissions_parent_permission_id_d0250f1b_fk_permissions_id` FOREIGN KEY (`parent_permission_id`) REFERENCES `permissions` (`id`);

ALTER TABLE `pos`
  ADD CONSTRAINT `pos_cluster_id_5fad0e30_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`);

ALTER TABLE `pos_company_mapping`
  ADD CONSTRAINT `pos_company_mapping_company_id_1ffbc0e9_fk_company_id` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`),
  ADD CONSTRAINT `pos_company_mapping_pos_id_091ef822_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `pos_department_mapping`
  ADD CONSTRAINT `pos_department_mapping_department_id_563fcd02_fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `pos_department_mapping_pos_id_7b6429d0_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `pos_sub_department_mapping`
  ADD CONSTRAINT `pos_sub_department_m_sub_department_id_40c9472b_fk_sub_depar` FOREIGN KEY (`sub_department_id`) REFERENCES `sub_department` (`id`),
  ADD CONSTRAINT `pos_sub_department_mapping_pos_id_d6ab3f82_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `pos_types`
  ADD CONSTRAINT `pos_types_brand_id_f87e01da_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `priority_types`
  ADD CONSTRAINT `priority_types_brand_id_1d03d200_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `product_types`
  ADD CONSTRAINT `product_types_brand_id_8161fd42_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `raw_material_dept_mapping`
  ADD CONSTRAINT `raw_material_dept_ma_department_id_c39722a4_fk_departmen` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `raw_material_dept_ma_raw_material_id_f0163c1b_fk_raw_mater` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material_registration` (`id`);

ALTER TABLE `raw_material_pos_mapping`
  ADD CONSTRAINT `raw_material_pos_map_raw_material_id_d5e6bfbc_fk_raw_mater` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material_registration` (`id`),
  ADD CONSTRAINT `raw_material_pos_mapping_pos_id_bbe1dc26_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`);

ALTER TABLE `raw_material_registration`
  ADD CONSTRAINT `raw_material_registration_brand_id_c38edc0f_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `raw_material_tags`
  ADD CONSTRAINT `raw_material_tags_raw_material_id_23fe5af3_fk_raw_mater` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material_registration` (`id`);

ALTER TABLE `recipe_ingredients`
  ADD CONSTRAINT `recipe_ingredients_raw_material_id_2340283a_fk_raw_mater` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material_registration` (`id`),
  ADD CONSTRAINT `recipe_ingredients_recipe_id_f1590b33_fk_recipe_registration_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe_registration` (`id`),
  ADD CONSTRAINT `recipe_ingredients_semi_product_id_d227fb59_fk_semi_prod` FOREIGN KEY (`semi_product_id`) REFERENCES `semi_product_registration` (`id`);

ALTER TABLE `recipe_registration`
  ADD CONSTRAINT `recipe_registration_brand_id_0eb2cf58_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `recipe_registration_final_product_id_0a0f0042_fk_final_pro` FOREIGN KEY (`final_product_id`) REFERENCES `final_product_registration` (`id`),
  ADD CONSTRAINT `recipe_registration_production_departmen_7993934e_fk_departmen` FOREIGN KEY (`production_department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `recipe_registration_recipe_approved_by_id_985d2b0c_fk_user_id` FOREIGN KEY (`recipe_approved_by_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `recipe_registration_recipe_entered_by_id_cfcf4221_fk_user_id` FOREIGN KEY (`recipe_entered_by_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `recipe_registration_semi_product_id_ec2360b5_fk_semi_prod` FOREIGN KEY (`semi_product_id`) REFERENCES `semi_product_registration` (`id`);

ALTER TABLE `recipe_variable_charges`
  ADD CONSTRAINT `recipe_variable_char_recipe_id_19cf0675_fk_recipe_re` FOREIGN KEY (`recipe_id`) REFERENCES `recipe_registration` (`id`);

ALTER TABLE `role_permissions`
  ADD CONSTRAINT `role_permissions_permission_id_ad343843_fk_permissions_id` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`),
  ADD CONSTRAINT `role_permissions_role_id_216516f2_fk_roles_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);

ALTER TABLE `semi_product_registration`
  ADD CONSTRAINT `semi_product_registr_cost_center_departme_a95b6e7b_fk_departmen` FOREIGN KEY (`cost_center_department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `semi_product_registr_production_departmen_d953b622_fk_departmen` FOREIGN KEY (`production_department_id`) REFERENCES `department` (`id`),
  ADD CONSTRAINT `semi_product_registration_brand_id_135d7dfe_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `semi_product_tags`
  ADD CONSTRAINT `semi_product_tags_semi_product_id_ce603ef2_fk_semi_prod` FOREIGN KEY (`semi_product_id`) REFERENCES `semi_product_registration` (`id`);

ALTER TABLE `severity_types`
  ADD CONSTRAINT `severity_types_brand_id_e4f51a23_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `store_brand_mapping`
  ADD CONSTRAINT `store_brand_mapping_brand_id_9837b250_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `store_brand_mapping_store_id_dcb62132_fk_store_id` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`);

ALTER TABLE `store_cluster_mapping`
  ADD CONSTRAINT `store_cluster_mapping_cluster_id_9b597d79_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`),
  ADD CONSTRAINT `store_cluster_mapping_store_id_5626706b_fk_store_id` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`);

ALTER TABLE `store_employees`
  ADD CONSTRAINT `store_employees_store_id_7b4c3b73_fk_store_id` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`),
  ADD CONSTRAINT `store_employees_user_id_e3bd6028_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `store_pos_mapping`
  ADD CONSTRAINT `store_pos_mapping_pos_id_5338b3f7_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`),
  ADD CONSTRAINT `store_pos_mapping_store_id_496b6a14_fk_store_id` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`);

ALTER TABLE `store_type`
  ADD CONSTRAINT `store_type_brand_id_0726ed3c_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `sub_category_list`
  ADD CONSTRAINT `sub_category_list_brand_id_688ca258_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `sub_category_list_categories`
  ADD CONSTRAINT `sub_category_list_ca_categorylist_id_149c5ae3_fk_category_` FOREIGN KEY (`categorylist_id`) REFERENCES `category_list` (`id`),
  ADD CONSTRAINT `sub_category_list_ca_subcategorylist_id_4aa886f4_fk_sub_categ` FOREIGN KEY (`subcategorylist_id`) REFERENCES `sub_category_list` (`id`);

ALTER TABLE `sub_department`
  ADD CONSTRAINT `sub_department_parent_department_id_86c95392_fk_department_id` FOREIGN KEY (`parent_department_id`) REFERENCES `department` (`id`);

ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`);

ALTER TABLE `token_blacklist_outstandingtoken`
  ADD CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `unit_of_measurments`
  ADD CONSTRAINT `unit_of_measurments_brand_id_d3c0d063_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

ALTER TABLE `user_brand_mapping`
  ADD CONSTRAINT `user_brand_mapping_brand_id_f10474af_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `user_brand_mapping_user_id_52fb81e9_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user_groups`
  ADD CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `user_groups_user_id_abaea130_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user_roles`
  ADD CONSTRAINT `user_roles_role_id_816a4486_fk_roles_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  ADD CONSTRAINT `user_roles_user_id_9d9f8dbb_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user_user_permissions`
  ADD CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `user_user_permissions_user_id_ed4a47ea_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `vendor_bank_details`
  ADD CONSTRAINT `vendor_bank_details_vendor_id_9e022d03_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_bank_documents`
  ADD CONSTRAINT `vendor_bank_document_vendor_bank_id_800d7a50_fk_vendor_ba` FOREIGN KEY (`vendor_bank_id`) REFERENCES `vendor_bank_details` (`id`),
  ADD CONSTRAINT `vendor_bank_document_vendor_document_id_262a54c9_fk_vendor_do` FOREIGN KEY (`vendor_document_id`) REFERENCES `vendor_documents` (`id`);

ALTER TABLE `vendor_brand_mapping`
  ADD CONSTRAINT `vendor_brand_mapping_brand_id_6c2b934d_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`),
  ADD CONSTRAINT `vendor_brand_mapping_vendor_id_ca168f59_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_cluster_mapping`
  ADD CONSTRAINT `vendor_cluster_mapping_cluster_id_c5239424_fk_clusters_id` FOREIGN KEY (`cluster_id`) REFERENCES `clusters` (`id`),
  ADD CONSTRAINT `vendor_cluster_mapping_vendor_id_aca00740_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_documents`
  ADD CONSTRAINT `vendor_documents_vendor_id_bdd3a402_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_pos_mapping`
  ADD CONSTRAINT `vendor_pos_mapping_pos_id_5d3c64b4_fk_pos_id` FOREIGN KEY (`pos_id`) REFERENCES `pos` (`id`),
  ADD CONSTRAINT `vendor_pos_mapping_vendor_id_945992fe_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_raw_material_pricing`
  ADD CONSTRAINT `vendor_raw_material__raw_material_id_c990c277_fk_raw_mater` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_material_registration` (`id`),
  ADD CONSTRAINT `vendor_raw_material_pricing_vendor_id_df0c9ea5_fk_vendors_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendors` (`id`);

ALTER TABLE `vendor_raw_material_pricing_log`
  ADD CONSTRAINT `vendor_raw_material__vendor_pricing_id_c726387d_fk_vendor_ra` FOREIGN KEY (`vendor_pricing_id`) REFERENCES `vendor_raw_material_pricing` (`id`);

ALTER TABLE `vendor_types`
  ADD CONSTRAINT `vendor_types_brand_id_b1385d19_fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
