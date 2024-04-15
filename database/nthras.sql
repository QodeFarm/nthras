/*
Nthras Product ERP System Database Schema
This schema is optimized for MySQL, focusing on performance, scalability, and data integrity for an Enterprise Resource Planning system. It includes comprehensive structures for managing companies, branches, users, roles, permissions, and other essential entities.

--- Recommendations for Developers ---

1. Indexing:
   - Always ensure to index foreign keys and columns frequently used in WHERE clauses, JOIN conditions, or as part of a foreign key relationship to enhance query performance.
   - Consider creating composite indexes for queries that span multiple columns frequently.

2. Data Types:
   - Choose the most appropriate data types for each column to optimize storage and performance. For instance, use INT UNSIGNED for identifiers, ENUM for columns with a limited set of predefined values, and appropriate VARCHAR lengths.
   - Use DECIMAL for precise arithmetic operations, especially for financial data.

3. Security:
   - Sensitive data such as passwords should be stored securely. Use hashing algorithms like bcrypt for passwords. Avoid storing plain-text passwords.
   - Consider field-level encryption for highly sensitive data like personal identification numbers or financial information.

4. Large Objects:
   - For large binary objects (BLOBs), such as images or documents, prefer storing them in an external storage solution (e.g., AWS S3) and save the reference URL in the database. This approach keeps the database size manageable and improves performance.

5. Data Integrity:
   - Use foreign key constraints to enforce relational integrity across tables.
   - Utilize transaction controls to ensure data consistency, particularly for operations that span multiple tables.

6. Normalization:
   - Adhere to normalization principles to reduce data redundancy and ensure data integrity. However, be mindful of over-normalization, which can lead to complex queries and affect performance.

7. Performance Optimization:
   - Use EXPLAIN to analyze and optimize query performance.
   - Consider partitioning large tables to improve query performance and management.

8. Auditing:
   - Include `created_at` and `updated_at` timestamps in all tables to track data creation and modifications.
   - Implement soft deletion (`is_deleted`) to maintain historical data without permanently removing records from the database.

9. Application-Level Considerations:
   - Where possible, offload data processing and business logic to the application level to leverage application caching and reduce database load.
   - Regularly review and optimize SQL queries used by the application, especially those that are executed frequently or involve large datasets.

10. Database Maintenance:
    - Regularly perform database maintenance tasks such as analyzing tables, optimizing indexes, and cleaning up unused data or tables to ensure optimal performance.
    - Plan for regular backups and establish a robust disaster recovery plan to safeguard your data.

By following these best practices, developers can ensure that the database layer of the Nthras Product ERP system remains robust, performant, and scalable to support the evolving needs of the business.

*/

/* Country Table */
-- Stores all countries info
CREATE TABLE IF NOT EXISTS country (
    country_id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL
) ENGINE=InnoDB;

/* State Table */
-- Stores all states info
CREATE TABLE IF NOT EXISTS state (
    state_id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT,
    state_name VARCHAR(100) NOT NULL,
    state_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_country_id FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* City Table */
-- Stores all city info
CREATE TABLE IF NOT EXISTS city (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    state_id INT,
    city_name VARCHAR(100) NOT NULL,
    city_code VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_state_id FOREIGN KEY (state_id) REFERENCES state(state_id) ON DELETE CASCADE
) ENGINE=InnoDB;


/* Companies Table */
-- Stores comprehensive information about each company, including contact info, identification numbers, and social media links.
CREATE TABLE IF NOT EXISTS companies (
    company_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    print_name VARCHAR(255),
    short_name VARCHAR(100),
    code VARCHAR(50),
    num_branches INT DEFAULT 0,
    num_employees INT,
    logo VARCHAR(255), -- URL to logo image stored externally
    address VARCHAR(255),
    city_id INT,
    pin_code VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    longitude DECIMAL(9, 6),
    latitude DECIMAL(9, 6),
    print_address VARCHAR(255),
    website VARCHAR(255),
    facebook_url VARCHAR(255),
    skype_id VARCHAR(50),
    twitter_handle VARCHAR(50),
    linkedin_url VARCHAR(255),
    pan VARCHAR(50),
    tan VARCHAR(50),
    cin VARCHAR(50),
    gst_tin VARCHAR(50),
    establishment_code VARCHAR(50),
    esi_no VARCHAR(50),
    pf_no VARCHAR(50),
    authorized_person VARCHAR(255),
    iec_code VARCHAR(50),
    eway_username VARCHAR(100),
    eway_password VARCHAR(100),
    gstn_username VARCHAR(100),
    gstn_password VARCHAR(100),
    vat_gst_status ENUM('Active', 'Inactive', 'Pending'),
    gst_type ENUM('Goods', 'Service', 'Both'),
    einvoice_approved_only TINYINT(1) DEFAULT 0,
    marketplace_url VARCHAR(255),
    drug_license_no VARCHAR(50),
    other_license_1 VARCHAR(50),
    other_license_2 VARCHAR(50),
    turnover_less_than_5cr TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) DEFAULT 0,
    CONSTRAINT fk_city_code FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* Statuses Table */
-- Defines various statuses that can be applied to records within the system, such as Active, Inactive, Pending Approval.
CREATE TABLE IF NOT EXISTS statuses (
    status_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

/* Roles Table */
-- Lists the roles that can be assigned to users, determining permissions and access levels within the ERP system.
CREATE TABLE IF NOT EXISTS roles (
    role_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

/* Branches Table */
-- Represents individual branches or offices of a company, including basic contact information.
CREATE TABLE IF NOT EXISTS branches (
    branch_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    company_id INT UNSIGNED NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    party VARCHAR(255),  -- This will be changed later
    gst_no VARCHAR(50) UNIQUE,
    status_id INT UNSIGNED NOT NULL,
    allowed_warehouse VARCHAR(255), -- Consider changing data type based on actual usage
    e_way_username VARCHAR(255),
    e_way_password VARCHAR(255), -- Securely store and encrypt this field
    gstn_username VARCHAR(255),
    gstn_password VARCHAR(255), -- Securely store and encrypt this field
    other_license_1 VARCHAR(255),
    other_license_2 VARCHAR(255),
    picture VARCHAR(255), -- URL to picture image stored externally
    address VARCHAR(255),
    country VARCHAR(50),
    state VARCHAR(50),
    city VARCHAR(50),
    pin_code VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    longitude DECIMAL(10, 7),
    latitude DECIMAL(10, 7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_company_id (company_id),
    CONSTRAINT fk_branches_company_id FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    CONSTRAINT fk_branches_status_id FOREIGN KEY (status_id) REFERENCES statuses(status_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* Branch Bank Details Table */
-- Stores sensitive bank information related to each branch, including bank name, account numbers, and branch details. 
CREATE TABLE IF NOT EXISTS branch_bank_details (
    bank_detail_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    branch_id INT UNSIGNED NOT NULL,
    bank_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(255) NOT NULL, -- Consider application-level encryption
    branch_name VARCHAR(255),
    ifsc_code VARCHAR(100),
    swift_code VARCHAR(100),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_bank_details_branch_id FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE CASCADE
) ENGINE=InnoDB;


/* Users Table */
-- Contains user profiles, including authentication details, contact information, and role within the ERP system.
CREATE TABLE IF NOT EXISTS users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    branch_id INT UNSIGNED,
    company_id INT UNSIGNED NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash CHAR(60) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    mobile VARCHAR(20) UNIQUE NOT NULL,
    otp_required TINYINT(1) DEFAULT 0,
    role_id INT UNSIGNED NOT NULL,
    status_id INT UNSIGNED NOT NULL,
    profile_picture_url VARCHAR(255),
    bio TEXT,
    timezone VARCHAR(100),
    language VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other', 'Prefer Not to Say') DEFAULT 'Prefer Not to Say',
    INDEX idx_branch_id (branch_id),
    INDEX idx_company_id (company_id),
    INDEX idx_role_id (role_id),
    INDEX idx_status_id (status_id),
    CONSTRAINT fk_users_branch_id FOREIGN KEY (branch_id) REFERENCES branches(branch_id) ON DELETE SET NULL,
    CONSTRAINT fk_users_company_id FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    CONSTRAINT fk_users_role_id FOREIGN KEY (role_id) REFERENCES roles(role_id),
    CONSTRAINT fk_users_status_id FOREIGN KEY (status_id) REFERENCES statuses(status_id)
) ENGINE=InnoDB;

/* user_time_restrictions Table */
-- Defines specific times during which users are allowed to access the ERP system, enhancing security and compliance.
CREATE TABLE IF NOT EXISTS user_time_restrictions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* user_allowed_weekdays Table */
-- Specifies the days of the week on which users are permitted to access the ERP system, further customizing access control.
CREATE TABLE IF NOT EXISTS user_allowed_weekdays (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    weekday ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* Permissions Table */
-- Defines specific actions or access rights that can be granted to roles, forming the basis of the ERP system's security model.
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

/* Role_Permissions Table */
-- Defines the relationship between roles and permissions, including the access level for each permission assigned to a role.
CREATE TABLE IF NOT EXISTS role_permissions (
    role_permission_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    role_id INT UNSIGNED NOT NULL,
    permission_id INT UNSIGNED NOT NULL,
    access_level VARCHAR(255) NOT NULL,
    UNIQUE (role_id, permission_id),
    CONSTRAINT fk_role_permissions_role_id FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_role_permissions_permission_id FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

/* Modules Table */
-- Stores information about different modules within the ERP system, such as HR, Finance, etc.
CREATE TABLE IF NOT EXISTS modules (
    module_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    module_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
) ENGINE=InnoDB;

/* Module_Sections Table */
-- Organizes modules into smaller sections for more granular access control and management.
CREATE TABLE IF NOT EXISTS module_sections (
    section_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    module_id INT UNSIGNED NOT NULL,
    section_name VARCHAR(255) NOT NULL,
    CONSTRAINT fk_module FOREIGN KEY (module_id) REFERENCES modules(module_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* Actions Table */
-- Lists the actions that can be performed within each module section, such as Create, Read, Update, Delete.
CREATE TABLE IF NOT EXISTS actions (
    action_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    action_name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
) ENGINE=InnoDB;

/* User_Permissions Table */
-- Connects users with specific permissions, denoting what actions a user can perform in different module sections.
CREATE TABLE IF NOT EXISTS user_permissions (
    user_permission_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    section_id INT UNSIGNED NOT NULL,
    action_id BIGINT UNSIGNED NOT NULL,
    description TEXT,
    CONSTRAINT fk_section FOREIGN KEY (section_id) REFERENCES module_sections(section_id) ON DELETE CASCADE,
    CONSTRAINT fk_action FOREIGN KEY (action_id) REFERENCES actions(action_id) ON DELETE CASCADE
) ENGINE=InnoDB;

/* Ledger Groups Table */
-- Stores information about ledger groups used in accounting.
CREATE TABLE IF NOT EXISTS ledger_groups (
    ledger_group_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(50),
    inactive BOOLEAN,
    under_group VARCHAR(255),
    nature VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Ledger Accounts Table */
-- Stores information about ledger accounts used in accounting.
CREATE TABLE IF NOT EXISTS ledger_accounts (
    ledger_account_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(50),
    is_subledger BOOLEAN,
    ledger_group_id INT,
    inactive BOOLEAN,
    type ENUM("customer", "Bank", "Cash"),
    account_no VARCHAR(50),
    rtgs_ifsc_code VARCHAR(50),
    classification VARCHAR(50),
    is_loan_account BOOLEAN,
    tds_applicable BOOLEAN,
    address VARCHAR(255),
    pan VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_group_id) REFERENCES ledger_groups(ledger_group_id)
);

/* Firm Statuses Table */
-- Stores information about different statuses of firms.
CREATE TABLE IF NOT EXISTS firm_statuses (
    firm_status_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Territory Table */
-- Stores information about territories.
CREATE TABLE IF NOT EXISTS territory (
    territory_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Customer Categories Table */
-- Stores information about customer categories.
CREATE TABLE IF NOT EXISTS customer_categories (
    customer_category_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* GST Categories Table */
-- Stores information about GST categories.
CREATE TABLE IF NOT EXISTS gst_categories (
    gst_category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Customer Payment Terms Table */
-- Stores information about payment terms for customers.
CREATE TABLE IF NOT EXISTS customer_payment_terms (
    payment_term_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(50),
    fixed_days INT,
    no_of_fixed_days INT,
    payment_cycle VARCHAR(255),
    run_on VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Price Categories Table */
-- Stores information about price categories.
CREATE TABLE IF NOT EXISTS price_categories (
    price_category_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Transporters Table */
-- Stores information about transporters.
CREATE TABLE IF NOT EXISTS transporters (
    transporter_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    gst_no VARCHAR(50),
    website_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Customers Table */
-- Stores information about customers.
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    print_name VARCHAR(255),
    identification VARCHAR(255),
    code VARCHAR(50),
    ledger_account_id INT,
    customer_common_for_sales_purchase BOOLEAN,
    is_sub_customer BOOLEAN,
    firm_status_id INT,
    territory_id INT,
    customer_category_id INT,
    contact_person VARCHAR(255),
    picture VARCHAR(255),
    gst VARCHAR(50),
    registration_date DATE,
    cin VARCHAR(50),
    pan VARCHAR(50),
    gst_category_id INT,
    gst_suspend BOOLEAN,
    tax_type ENUM('Inclusive', 'Exclusive') DEFAULT 'Inclusive',
    distance FLOAT,
    tds_on_gst_applicable BOOLEAN,
    tds_applicable BOOLEAN,
    website VARCHAR(255),
    facebook VARCHAR(255),
    skype VARCHAR(255),
    twitter VARCHAR(255),
    linked_in VARCHAR(255),
    payment_term_id INT,
    price_category_id INT,
    batch_rate_category VARCHAR(50),
    transporter_id INT,
    credit_limit DECIMAL(18,2),
    max_credit_days INT,
    interest_rate_yearly DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_account_id) REFERENCES ledger_accounts(ledger_account_id),
    FOREIGN KEY (firm_status_id) REFERENCES firm_statuses(firm_status_id),
    FOREIGN KEY (territory_id) REFERENCES territory(territory_id),
    FOREIGN KEY (customer_category_id) REFERENCES customer_categories(customer_category_id),
    FOREIGN KEY (gst_category_id) REFERENCES gst_categories(gst_category_id),
    FOREIGN KEY (payment_term_id) REFERENCES customer_payment_terms(payment_term_id),
    FOREIGN KEY (price_category_id) REFERENCES price_categories(price_category_id),
    FOREIGN KEY (transporter_id) REFERENCES transporters(transporter_id)
);

/* Customer Attachments Table */
-- Stores attachments associated with Customer.
CREATE TABLE IF NOT EXISTS customer_attachments (
    attachment_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    attachment_name VARCHAR(255),
    attachment_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

/* Customer Addresses Table */
-- Stores information about customer addresses.
CREATE TABLE IF NOT EXISTS customer_addresses (
    customer_address_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    address_type ENUM('Billing', 'Shipping'),
    address VARCHAR(255),
    country VARCHAR(255),
    state VARCHAR(255),
    city VARCHAR(255),
    pin_code VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(255),
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),
    route_map VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

/* Product Groups Table */
-- Stores information about different groups of products.
CREATE TABLE IF NOT EXISTS product_groups (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255),
    description TEXT,
    picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Categories Table */
-- Stores information about different categories of products.
CREATE TABLE IF NOT EXISTS product_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255),
    picture VARCHAR(255),
    code VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Types Table */
-- Stores information about different types of products.
CREATE TABLE IF NOT EXISTS product_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Unique Quantity Codes Table */
-- Stores information about unique quantity codes for products.
CREATE TABLE IF NOT EXISTS product_unique_quantity_codes (
    quantity_code_id INT AUTO_INCREMENT PRIMARY KEY,
    quantity_code_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Unit Options Table */
-- Stores information about unit options.
CREATE TABLE IF NOT EXISTS unit_options (
    unit_options_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


/* Product Stock Units Table */
-- Stores information about stock units for products.
CREATE TABLE IF NOT EXISTS product_stock_units (
    stock_unit_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_unit_name VARCHAR(255),
    description TEXT,
    quantity_code_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (quantity_code_id) REFERENCES product_unique_quantity_codes(quantity_code_id)
);

/* Product GST Classifications Table */
-- Stores information about GST classifications for products.
CREATE TABLE IF NOT EXISTS product_gst_classifications (
    gst_classification_id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('HSN', 'SAC'),
    code VARCHAR(50),
    hsn_or_sac_code VARCHAR(50),
    hsn_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Sales GL Table */
-- Stores information about sales GL accounts for products.
CREATE TABLE IF NOT EXISTS product_sales_gl (
    sales_gl_id INT AUTO_INCREMENT PRIMARY KEY,
    ledger_group_id INT,
    name VARCHAR(255),
    sales_accounts VARCHAR(255),
    code VARCHAR(50),
    is_subledger BOOLEAN,
    inactive BOOLEAN,
    type VARCHAR(255),
    account_no VARCHAR(255),
    rtgs_ifsc_code VARCHAR(255),
    classification VARCHAR(255),
    is_loan_account BOOLEAN,
    tds_applicable BOOLEAN,
    address VARCHAR(255),
    pan VARCHAR(50),
    employee BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_group_id) REFERENCES ledger_groups(ledger_group_id)
);

/* Product Drug Types Table */
-- Stores information about drug types for products.
CREATE TABLE IF NOT EXISTS product_drug_types (
    drug_type_id INT AUTO_INCREMENT PRIMARY KEY,
    drug_type_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Purchase GL Table */
-- Stores information about purchase GL accounts for products.
CREATE TABLE IF NOT EXISTS product_purchase_gl (
    purchase_gl_id INT AUTO_INCREMENT PRIMARY KEY,
    ledger_group_id INT,
    name VARCHAR(255),
    purchase_accounts VARCHAR(255),
    code VARCHAR(50),
    is_subledger BOOLEAN,
    inactive BOOLEAN,
    type VARCHAR(255),
    account_no VARCHAR(255),
    rtgs_ifsc_code VARCHAR(255),
    classification VARCHAR(255),
    is_loan_account BOOLEAN,
    tds_applicable BOOLEAN,
    address VARCHAR(255),
    pan VARCHAR(50),
    employee BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_group_id) REFERENCES ledger_groups(ledger_group_id)
);

/* Product Item Types Table */
-- Stores information about item types for products.
CREATE TABLE IF NOT EXISTS product_item_type (
    item_type_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Brand Salesman Table */
-- Stores information about salesmen for brands.
CREATE TABLE IF NOT EXISTS brand_salesman (
    brand_salesman_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    commission_rate DECIMAL(18,2),
    rate_on ENUM("Qty", "Amount"),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Product Brands Table */
-- Stores information about brands for products.
CREATE TABLE IF NOT EXISTS product_brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255),
    code VARCHAR(50),
    picture VARCHAR(255),
    brand_salesman_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_salesman_id) REFERENCES brand_salesman(brand_salesman_id)
);

/* Products Table */
-- Stores information about products.
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    ledger_group_id INT,
    category_id INT,
    type_id INT,
    code VARCHAR(50),
    barcode VARCHAR(50),
    unit_options_id INT,
    gst_input VARCHAR(255),
    stock_unit_id INT,
	print_barcode BOOLEAN,
    gst_classification_id INT,
    picture VARCHAR(255),
    sales_description TEXT,
    sales_gl_id INT,
    mrp DECIMAL(18,2),
    minimum_price DECIMAL(18,2),
    sales_rate DECIMAL(18,2),
    wholesale_rate DECIMAL(18,2),
    dealer_rate DECIMAL(18,2),
    rate_factor DECIMAL(18,2),
    discount DECIMAL(18,2),
    dis_amount DECIMAL(18,2),
    purchase_description TEXT,
    purchase_gl_id INT,
    purchase_rate DECIMAL(18,2),
    purchase_rate_factor DECIMAL(18,2),
    purchase_discount DECIMAL(18,2),
    item_type_id INT,
    minimum_level INT,
    maximum_level INT,
    salt_composition TEXT,
    drug_type_id INT,
    weighscale_mapping_code VARCHAR(50),
    brand_id INT,
    purchase_warranty_months INT,
    sales_warranty_months INT,
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_group_id) REFERENCES ledger_groups(ledger_group_id),
    FOREIGN KEY (category_id) REFERENCES product_categories(category_id),
    FOREIGN KEY (type_id) REFERENCES product_types(type_id),
    FOREIGN KEY (unit_options_id) REFERENCES unit_options(unit_options_id),
    FOREIGN KEY (stock_unit_id) REFERENCES product_stock_units(stock_unit_id),
    FOREIGN KEY (gst_classification_id) REFERENCES product_gst_classifications(gst_classification_id),
    FOREIGN KEY (sales_gl_id) REFERENCES product_sales_gl(sales_gl_id),
    FOREIGN KEY (purchase_gl_id) REFERENCES product_purchase_gl(purchase_gl_id),
    FOREIGN KEY (item_type_id) REFERENCES product_item_type(item_type_id),
    FOREIGN KEY (drug_type_id) REFERENCES product_drug_types(drug_type_id),
    FOREIGN KEY (brand_id) REFERENCES product_brands(brand_id)
);

/* Vendor Category Table */
-- Stores vendor categories, providing classification for vendors.
CREATE TABLE IF NOT EXISTS vendor_category (
    vendor_category_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Vendor Payment Terms Table */
-- Stores payment terms applicable to vendors.
CREATE TABLE IF NOT EXISTS vendor_payment_terms (
    payment_term_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(50),
    fixed_days INT,
    no_of_fixed_days INT,
    payment_cycle VARCHAR(255),
    run_on VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Vendor Agent Table */
-- Stores information about vendor agents, including commission rates and types.
CREATE TABLE IF NOT EXISTS vendor_agent (
    vendor_agent_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255),
    commission_rate DECIMAL(18, 2),
    rate_on ENUM("Qty", "Amount"),
    amount_type ENUM("Taxable", "BillAmount"),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

/* Vendor Table */
-- Stores information about vendors including their details, contacts, and financial information.
CREATE TABLE IF NOT EXISTS vendor (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    gst_no VARCHAR(255),
    name VARCHAR(255),
    print_name VARCHAR(255),
    identification VARCHAR(255),
    code VARCHAR(255),
    ledger_account_id INT,
    vendor_common_for_sales_purchase BOOLEAN,
    is_sub_vendor BOOLEAN,
    firm_status_id INT,
    territory_id INT,
    vendor_category_id INT,
    contact_person VARCHAR(255),
    picture VARCHAR(255),
    gst VARCHAR(255),
    registration_date DATE,
    cin VARCHAR(255),
    pan VARCHAR(255),
    gst_category_id INT,
    gst_suspend BOOLEAN,
    tax_type ENUM('Inclusive', 'Exclusive') DEFAULT 'Inclusive',
    distance DECIMAL(18, 2),
    tds_on_gst_applicable BOOLEAN,
    tds_applicable BOOLEAN,
    website VARCHAR(255),
    facebook VARCHAR(255),
    skype VARCHAR(255),
    twitter VARCHAR(255),
    linked_in VARCHAR(255),
    payment_term_id INT,
    price_category_id INT,
    vendor_agent_id INT,
    transporter_id INT,
    credit_limit DECIMAL(18, 2),
    max_credit_days INT,
    interest_rate_yearly DECIMAL(18, 2),
    rtgs_ifsc_code VARCHAR(255),
    accounts_number VARCHAR(255),
    bank_name VARCHAR(255),
    branch VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ledger_account_id) REFERENCES ledger_accounts(ledger_account_id),
    FOREIGN KEY (firm_status_id) REFERENCES firm_statuses(firm_status_id),
    FOREIGN KEY (territory_id) REFERENCES territory(territory_id),
    FOREIGN KEY (vendor_category_id) REFERENCES vendor_category(vendor_category_id),
    FOREIGN KEY (gst_category_id) REFERENCES gst_categories(gst_category_id),
    FOREIGN KEY (payment_term_id) REFERENCES vendor_payment_terms(payment_term_id),
    FOREIGN KEY (price_category_id) REFERENCES price_categories(price_category_id),
    FOREIGN KEY (vendor_agent_id) REFERENCES vendor_agent(vendor_agent_id),
    FOREIGN KEY (transporter_id) REFERENCES transporters(transporter_id)
);

/* Vendor Attachments Table */
-- Stores attachments associated with vendors.
CREATE TABLE IF NOT EXISTS vendor_attachments (
    attachment_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT,
    attachment_name VARCHAR(255),
    attachment_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id)
);

/* Vendor Addresses Table */
-- Stores addresses associated with vendors.
CREATE TABLE IF NOT EXISTS vendor_addresses (
    vendor_address_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT,
    address_type ENUM('Billing', 'Shipping'),
    address VARCHAR(255),
    country VARCHAR(255),
    state VARCHAR(255),
    city VARCHAR(255),
    pin_code VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(255),
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),
    route_map VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id)
);