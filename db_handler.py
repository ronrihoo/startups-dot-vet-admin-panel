# db_handler.py
#
# -- NOT CURRENTLY A PART OF CODEBASE --
#
# Brief: creates a database and a table within that database
# 	     using PostgreSQL and Python.
#
# Note: borrowed from github.com/ronrihoo/Create_a_Database_with_Postgres_and_Python/createdb.py
#
# Author: Ron Rihoo

import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import subprocess

# This is the setup section and the only part that requires modification for basic use ####

# Username (as needed)
username = "user"

# May also consider to take a string argument, dbname, from createDatabase()
dbname = "database"

# May also consider to take a string argument, table_1, from createDatabase() to pass to createTable()
table_1 = "posts"

# Change this query based on database needs.
db_query = "CREATE DATABASE " + dbname + ";"

# Change this query based on table needs.
table_query = '''
	            CREATE TABLE post ( content TEXT,
				                    nickname TEXT,
			                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			                        id SERIAL
			                      );
	          '''

# End of setup ####


# Declaring Strings for Error Checking and State Management #


# State Names
state_0 = "main"
state_1 = "create_database()"
state_2 = "create_table()"

# Main Error Signaling Strings
err_con_0 = "Error: failed when connecting to default system database, postgres."
err_con_1 = "Error: failed when connecting to database."
err_con_2 = "Error: failed when switching autocommit on."
err_con_3 = "Error: failed when committing changes."
err_con_x = "Error: failed when closing connection."
err_cur_0 = "Error: failed when creating cursor."
err_cur_1 = "Error: failed when running query: "
err_jmp_1 = "Error: failed when jumping to " + state_1 + "."
err_jmp_2 = "Error: failed when jumping to " + state_2 + "."
err_jmp_n = "Error: failed when jumping to next state."
err_gen_0 = "Failed to begin."
err_gen_1 = "Failed to create database."
err_gen_2 = "Failed to create table."

# Main Operation State Signaling Strings
op_con_0 = "Connected to default system database, postgres."
op_con_1 = "Connected to database."
op_con_2 = "Autocommit has been turned on."
op_con_3 = "Changes have been committed."
op_con_x = "Connection has been closed."
op_cur_0 = "Cursor instance has been created."
op_cur_1 = "Query has been executed."
op_jmp_1 = "Jumped to " + state_1 + "."
op_jmp_2 = "Jumped to " + state_2 + "."
op_jmp_n = "Jumped to next state"
op_jmp_x = "End of script."
op_gen_0 = "Script has started."
op_gen_1 = "Database '" + dbname + "' has been created."
op_gen_2 = "Table '" + table_1 + "' has been created."


# Beginning Main ####

# Create a database
def create_database():
    # the low confidence method: it's going to "try" to do everything.
    try:
        # change user to 'postgres'
        try:
            # subprocess.call(["sudo", "-u", "postgres", "-i"])
            subprocess.call(["echo", "''", "|", "sudo", "- S", "-u", "postgres", "-i"])
        except:
            print "Could not switch user to 'postgres'"
            return

        # connect to default system database, postgres.
        try:
            con = psycopg2.connect(dbname='postgres')
            print op_con_0
        except:
            print err_con_0
            return

        # turn autocommit on
        try:
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print op_con_2
        except:
            print err_con_2
            return

        # create instance of connection cursor
        try:
            cur = con.cursor()
            print op_cur_0
        except:
            print err_cur_0
            return

        # run query to build database
        try:
            cur.execute(db_query)
            print op_cur_1
        except:
            print err_cur_1 + db_query
            return

        # close cursor and connection, then print operation state
        try:
            cur.close()
            con.close()
            print op_gen_1
            print op_con_x
        except:
            print err_con_x
            return

        # jump to create_table()
        try:
            create_table()
        except:
            print err_jmp_2
            return
    except:
        print err_gen_1
        return


# creates a table
def create_table():
    print op_jmp_2

    try:
        # connect to database
        try:
            db = psycopg2.connect('dbname = ' + dbname)
            print op_con_1
        except:
            print err_con_1
            return

        # create instance of cursor
        try:
            c = db.cursor()
            print op_cur_0
        except:
            print err_cur_0
            return

        # run query to create table
        try:
            c.execute(table_query)
            print op_cur_1
        except:
            print err_cur_1 + table_query
            return

        try:
            db.commit()
            print op_con_3
        except:
            print err_con_3
            return

        # close connection, then print operation state
        try:
            db.close()
            print op_gen_2
            print op_con_x
        except:
            print err_con_x
            return
    except:
        print err_gen_2
        return

    # print final state message
    print op_jmp_x



# run state 1 (creating the database), which will proceed to creating an initial table in the database
create_database()
