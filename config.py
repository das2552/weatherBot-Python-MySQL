# натсройки подключения к бд
# config connection to database

host = ""
user = ""
password = ""
db_name = ""


# запросы на создание бд подобной моей 
# request to DB 


############################################################################################
# create table

# create_table_query = "CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY, \
#                         name varchar(32), \
#                         chatId varchar(64) UNIQUE);"
# cursor.execute(create_table_query)
# print("table create")

############################################################################################
# insert data

# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO Users (name, chatId) VALUES ('Алекс', '(здесь айди)');"
#     cursor.execute(insert_query)
#     print("aleks - inserted")

############################################################################################
# select from table

# with connection.cursor() as cursor:
#     select_query = "SELECT * FROM Users"
#     cursor.execute(select_query)
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)