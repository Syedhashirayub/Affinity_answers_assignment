import mysql.connector

def connect_to_database():
    """Connect to the MySQL database"""
    connection = mysql.connector.connect(
        host="mysql-rfam-public.ebi.ac.uk",
        port=4497,
        user="rfamro",
        #password="",
        database="Rfam"
    )
    cursor = connection.cursor()
    return connection, cursor

def execute_query(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    print("\n")

def main():
    connection, cursor = connect_to_database()

    # Query for question a:
    print("Question a:")
    query_a1 = """
        SELECT COUNT(*) 
        FROM taxonomy 
        WHERE species LIKE '%Panthera tigris%';
    """
    execute_query(cursor, query_a1)
    
    query_a2 = """
        SELECT ncbi_id 
        FROM taxonomy 
        WHERE species LIKE '%Panthera tigris sumatrae%';
    """
    execute_query(cursor, query_a2)

    # Query for question b:
    print("Question b:")
    query_b = """
        SELECT 
        TABLE_NAME AS 'Table',
        COLUMN_NAME AS 'Column',
        REFERENCED_TABLE_NAME AS 'Referenced Table',
        REFERENCED_COLUMN_NAME AS 'Referenced Column'
        FROM 
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
        WHERE 
        TABLE_SCHEMA = 'Rfam' AND 
        REFERENCED_TABLE_NAME IS NOT NULL;
    """
    execute_query(cursor, query_b)


    # Query for question c:
    print("Question c:")
    query_c = """
        SELECT t.species, MAX(r.length) AS max_length
        FROM rfamseq r
        JOIN taxonomy t ON r.ncbi_id = t.ncbi_id
        WHERE t.species LIKE '%rice%'
        GROUP BY t.species
        ORDER BY max_length DESC
        LIMIT 1;

    """
    execute_query(cursor, query_c)

    # Query for question d:
    print("Question d:")
    query_d = """
        SELECT f.rfam_acc, f.rfam_id AS family_name, MAX(r.length) AS max_length
        FROM family f
        JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
        JOIN rfamseq r ON fr.rfamseq_acc = r.rfamseq_acc
        WHERE r.length > 1000000
        GROUP BY f.rfam_acc, f.rfam_id
        ORDER BY max_length DESC
        LIMIT 15 OFFSET 120;

    """
    execute_query(cursor, query_d)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
