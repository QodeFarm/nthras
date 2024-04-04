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


/* Companies Table */
-- Stores comprehensive information about each company, including contact info, identification numbers, and social media links.
CREATE TABLE IF NOT EXISTS companies (
    company_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    print_name VARCHAR(255),
    short_name VARCHAR(100),
    code VARCHAR(50),
    num_branches INT DEFAULT 0,
    logo VARCHAR(255), -- URL to logo image stored externally
    address TEXT,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    pin_code VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    longitude DECIMAL(9, 6),
    latitude DECIMAL(9, 6),
    print_address TEXT,
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
    gst_type ENUM('Goods', 'Service'),
    einvoice_approved_only TINYINT(1) DEFAULT 0,
    marketplace_url VARCHAR(255),
    drug_license_no VARCHAR(50),
    other_license_1 VARCHAR(50),
    other_license_2 VARCHAR(50),
    turnover_less_than_5cr TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) DEFAULT 0
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
    address TEXT,
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
    address TEXT,
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

