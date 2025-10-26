import sqlite3

try:
    # Connect to SQLite Database and create a cursor
    connection = sqlite3.connect("./databases/products.db")
    conn_cursor = connection.cursor()
    print(conn_cursor)

    # Create product table
    conn_cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            SKU INTEGER PRIMARY KEY NOT NULL,
            PRODUCT_DESCRIPTION TEXT NOT NULL,
            PUBLIC_PRICE FLOAT NOT NULL,
            PUBLIC_PRICE_NO_TAX FLOAT NOT NULL,
            MEMBER_PRICE FLOAT NOT NULL,
            MEMBER_PRICE_NO_TAX FLOAT NOT NULL,
            RETAIL_BONUS_NO_TAX FLOAT NOT NULL,
            VCV FLOAT NOT NULL,
            VV FLOAT NOT NULL
        )
    ''')

    # Insert products
    conn_cursor.execute("""INSERT INTO products (SKU, 
                                                 PRODUCT_DESCRIPTION,
                                                 PUBLIC_PRICE,
                                                 PUBLIC_PRICE_NO_TAX,
                                                 MEMBER_PRICE,
                                                 MEMBER_PRICE_NO_TAX,
                                                 RETAIL_BONUS_NO_TAX,
                                                 VCV,
                                                 VV) 
                        VALUES (23130268,
                                'Kit LOI',
                                1464750.00,
                                1210537.19,
                                1323000.00,
                                1093388.43,
                                117148.76,
                                727650.00,
                                1000.00)""")
    # conn_cursor.execute("""INSERT INTO products (SKU, PRODUCT) 
    #                     VALUES (23130440,
    #                             'Kit Collagen Premium (12pk)')""")

    # Commit the data
    connection.commit()
    print("Data inserted successfully.")

    # Close the cursor after use
    conn_cursor.close()

except sqlite3.Error as error:
    print("Error occurred -", error)

finally:
    # Close the database connection
    if connection:
        connection.close()
        print("SQLite Connection closed.")
