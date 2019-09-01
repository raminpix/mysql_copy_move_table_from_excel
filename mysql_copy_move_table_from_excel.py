import sys
import pymysql
import configparser
import xlrd 


def connect_mysql(host,user,password):
    try:
        conn = pymysql.connect(host,
                               user, password)    
        return conn
    except Exception as e:
        print("Error connecting database: " + str(e))    
        sys.exit(1)

def read_config_file(path):
    try:
        config = configparser.ConfigParser()
        config_file_name = "config.ini"
        config.read(config_file_name)
        return config
    except:
        print("Error reading file " + config_file_name)    
        return None
        

def copy_move_table(db,cursor,src_schema,dest_schema,operation,src_table,dest_table):
    
    src_table_full_name = src_schema + "." + src_table
    dest_table_full_name = dest_schema + "." + dest_table
    db.select_db(src_schema)    
    operation_msg = None
    operation_success_msg = None
    if operation.lower() == "move":
        operation_msg = "Moving"
        operation_success_msg = "Move"
    elif operation.lower() == "copy":
        operation_msg = "Copying"
        operation_success_msg = "Copy"
    else:
        raise ValueError("Operation type(copy or move) must be specified in Excel file.")
    print(operation_msg + " " + src_table_full_name + " to " + dest_table_full_name +" ...")

    try:
        cursor.execute("SHOW CREATE TABLE " + src_table_full_name)

        myresult = cursor.fetchone()
        create_table_sql = myresult[1].replace(src_table, dest_table,1)        
        #dest_table_remove = "DROP TABLE IF EXISTS "+ dest_table_full_name +";"        
        #cursor.execute(dest_table_remove)
        #print("Deleting " + dest_table_full_name)
        db.select_db(dest_schema)
        cursor.execute(create_table_sql)
        sql = "insert into "+ dest_table_full_name +" select * from "+ src_table_full_name + ";"
        cursor.execute(sql)

        if operation.lower() == "move":
            src_table_remove = "DROP TABLE IF EXISTS "+ src_table_full_name +";"            
            src_cursor.execute(src_table_remove)

        db.commit()        
        print(operation_success_msg + " " + src_table_full_name + " to " + dest_table_full_name + " " + "completed successfully.")
        return True
    except Exception as e:
        print(e)
        print("Error copying/moving tables")
        db.rollback()
        return False

############################################################

print("MySQL Copy Move Table Tool - v1.0.2 - 2019-09-01.r3")
db = None
src_schema = None
dest_schema = None
cursor = None
import_data = None
excel_file = None
try:
    config = read_config_file("config.ini")    
    excel_file = config["DB"]["excel_file"]    
except:
    print("Error reading file ")    
    sys.exit(1)

try:
    
    host = config["DB"]["host"]
    user = config["DB"]["user"]
    password = config["DB"]["passwd"]    
    db = connect_mysql(host,user,password)    
    cursor = db.cursor()       
    
    wb = xlrd.open_workbook(excel_file) 
    sheet = wb.sheet_by_index(0) 
    copy_count = 0
    copy_move_success = False
    table_count = sheet.nrows - 1
    print("Number of tables to be copied/moved: " + str(table_count))
    for i in range(table_count):
        src_schema = sheet.cell_value(i + 1 , 0)
        src_table = sheet.cell_value(i + 1 , 1)
        dest_schema = sheet.cell_value(i + 1 , 2)
        dest_table = sheet.cell_value(i + 1 , 3)        
        operation = sheet.cell_value(i + 1 , 4)                
        copy_move_success = copy_move_table(db,cursor,src_schema,dest_schema,operation,src_table,dest_table)
        if copy_move_success:
            copy_count += 1
except Exception as e:
    print("Error:" + str(e))
    sys.exit(1)
    
print("Copied/Moved tables: " + str(copy_count))
sys.exit(0)

