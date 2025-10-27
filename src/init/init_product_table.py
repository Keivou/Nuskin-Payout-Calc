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
    conn_cursor.execute("""INSERT INTO 
                        products (SKU,
                                  MARKET_LOCATION,
                                  PRODUCT_DESCRIPTION,
                                  PUBLIC_PRICE,
                                  PUBLIC_PRICE_NO_TAX,
                                  MEMBER_PRICE,
                                  MEMBER_PRICE_NO_TAX,
                                  RETAIL_BONUS_NO_TAX,
                                  VCV,
                                  VV)
                        VALUES (23130268,
                                'ARGENTINA'
                                'Kit LOI',
                                1464750.00,
                                1210537.19,
                                1323000.00,
                                1093388.43,
                                117148.76,
                                727650.00,
                                1000.00)
                        """)
    conn_cursor.execute("""INSERT INTO 
                        products (SKU,
                                  MARKET_LOCATION,
                                  PRODUCT_DESCRIPTION,
                                  PUBLIC_PRICE,
                                  PUBLIC_PRICE_NO_TAX,
                                  MEMBER_PRICE,
                                  MEMBER_PRICE_NO_TAX,
                                  RETAIL_BONUS_NO_TAX,
                                  VCV,
                                  VV)
                        VALUES (50130478,
                                'COLOMBIA',
                                'Kit Belleza & Bienestar',
                                2940000.00,
                                2470588.00,
                                2630000.00,
                                2210084.00,
                                260504.00,
                                1392000.00,
                                500.00
                                )
                        """)

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
