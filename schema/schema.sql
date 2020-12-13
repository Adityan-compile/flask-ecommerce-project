DROP TABLE IF EXISTS Products;
 
     CREATE TABLE Products(
            id integer PRIMARY KEY AUTOINCREMENT,
            product_name text NOT NULL,
            product_price text NOT NULL,
            product_brand text NOT NULL,
            product_image text NOT NULL,
            product_description text NOT NULL,
            stock_status text NOT NULL
     );


DROP TABLE IF EXISTS Users;

     CREATE TABLE Users(
            user_id integer PRIMARY KEY AUTOINCREMENT,
            user_name text NOT NULL,
            user_email text NOT NULL,
            user_address text NOT NULL,
            user_password text NOT NULL,
            user_phonenumber text NOT NULL,
            user_city text NOT NULL,
            user_state text NOT NULL,
            user_zip text NOT NULL
     );


DROP TABLE IF EXISTS Orders;

     CREATE TABLE Orders(
            order_id text NOT NULL,
            payment_id text NOT NULL,
            razorpay_signature text NOT NULL,
            order_date text NOT NULL,
            customer_name text NOT NULL,
            customer_email text NOT NULL,
            customer_address text NOT NULL,
            customer_zip text NOT NULL,
            customer_phone text NOT NULL,
            payment_status text NOT NULL,
            product_name text NOT NULL,
            total_order_price text NOT NULL
     );


DROP TABLE IF EXISTS Cart;

     CREATE TABLE Cart(
            serial_number integer PRIMARY KEY AUTOINCREMENT,
            product_name text NOT NULL,
            customer_name text NOT NULL,
            customer_email text NOT NULL,
            product_image text NOT NULL,
            product_price text NOT NULL
     );

DROP TABLE IF EXISTS Admins;

     CREATE TABLE Admins(
            id integer PRIMARY KEY AUTOINCREMENT,
            admin_name text NOT NULL,
            admin_password text NOT NULL
     );
