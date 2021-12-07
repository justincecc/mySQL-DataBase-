#importing the sql api connector
import mysql.connector

#from the connector we imported the Error to be able to determine what kind of
#Error we run into while trying to connect to our server
from mysql.connector import Error

#the IPython package I installed is to be able to get our database tables presented in a nice user firendly way
#we import display from it to be able to use becuase that function is what displays the table for us
from IPython.display import display

#the pandas package I installed is to be able to put our database in a nice dataframe so it's easy to read for users
#then I just wanted to be able to refrence the library easily so I imported it as pd 
import pandas as pd

#This function is  a main function we use to be able to create a connection with our server
# It takes 3 parameters my host name, my user name, and my password for the server
# At the beginning of the function it sets connection to none that way we never have an open connection when we 
# want to connect to the server. It will always close it then open it.
# In the try block it trys to connect using the mysql connect function on the mysql connector object
# We set the host, user, password to their respective parameters
# If we connect succesfully it prints a message saying we have successfully connected
# If we dont connect it prints out our Error as to why we were unable to connect
# After the try, except block it then returns our connection either the server connection or none depending on if it worked or not
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#This function is our main function we use to be able to create a connection with our database it takes
# 4 parameters my host name, my user name, my password for the server, and then the database name we want to work on
#At the beginning of the function it sets connection to none that way we never have an open connection when we 
# want to connect to the server. It will always close it then open it.
#In the try block it trys to connect using the mysql connect function on the mysql connector object
#We set the host, user, password and database name respectively to their parametes
#If we connect succesfully it prints a message saying we have successfully 
#If we dont connect it prints out our Error as to why we were unable to connect
#After the try, except block it then returns our connection either the server connection or none depending on if it worked or not
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error:  '{err}'")
    
    return connection

# This function creates a new database for us
# It takes two parameters our open connection object and the new database name we want
# first I create a sql vairable that has the porper SQL syntax to create a new database
# Then it calls the create database function with our connection parameter and the sql variabke
def create_database_query(connection, database_name):
    sql = 'CREATE DATABASE ' + database_name
    create_database(connection, sql)

# This function lets us select from our table seeing what exactly is in our table
# It takes two parameters our connection which we get from the previous function and the table name we want to see
# The cursor variable is then assigned to our connection cursor and then I wrote an sql commmand to be able
# to get the table info for the desired table
# the cursor then executes the SQL I wrote and we fetch all the data from the table using the fetchall function
# then we just loop through all the items we recieved in our fetch all call and print them to be able to see them 
def select_from_table(connection, table_name):
    cursor = connection.cursor()
    sql = 'SELECT * FROM ' + table_name
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

# This function lets us select a specific column from the table we want to view
# This function takes 3 parameters the open connection we have to the database the column name we want to see
# and the table name we want to see. It starts with creating the cursor object by calling the mysql cursor function
# on our open connection. Then I assigned a sql variable gave it the proper syntax it'd need to make changes
# I then have the cursor execute the sql I wrote with the parameters in it, then have the cursor fetch all the data
# Finally I loop through all the data from the fetch all and print it to the console
def select_column(connection, column_name, table_name):
    cursor = connection.cursor()
    sql = 'SELECT ' + column_name + ' FROM ' + table_name
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

# This function is very similar to the previous one except this function just returns one single piece of data from the column
# It takes the same parameters connection, column name and table name
# The only difference here is instead of using the fetch all function on the cursor object we user the fetch one function
# Then I print the one thing we got returned from that function
def select_one_column(connection, column_name, table_name):
    cursor = connection.cursor()
    sql = 'SELECT ' + column_name + ' FROM ' + table_name
    cursor.execute(sql)
    myresult = cursor.fetchone()
    print(myresult)

# This function lets me be able to select a specific result from the column given an identifier
# It takes 4 parameters the open connection, table name we want to see, column name we want to see
# then the specific identifier within the column that we want to see
# This function starts similarly to the other creates a cursor objecct with the connection
# Then I manipulate the column ID because it needs to have the ' ' around it in the sql syntax to work
# The sql variable is then made using proper SQL syntax while using the parameters passed into the function
# The cursor executes the sql variable and then I have the cursor fetch all the results
# Finally I loop through the results and print all the results to the console
def select_with_filter(connection, table_name, column_name, column_id):
    cursor = connection.cursor()
    column_id = "'" + column_id + "'"
    sql = 'SELECT * FROM ' + table_name + ' WHERE ' + column_name + ' = ' + column_id
    cursor.execute(sql)
    myresults = cursor.fetchall()
    for x in myresults:
        print(x)

# This function is similar to the last except this one is more broad and less specific 
# It takes the 4 same parameters as the last one but this time we do something different
# It creates a cursor object again, but when I manipulate the column ID this time I add 
# the '% '% around it. That's because the % is a wild card so when I use it in my SQL variable
# it selects anything that contains the column ID. Then I do the same thing fetch all the results
# And finally loop through and print all the results to the console
def select_with_broad_filter(connection, table_name, column_name, column_id):
    cursor = connection.cursor()
    column_id = "'%" + column_id + "'%"
    sql = 'SELECT * FROM ' + table_name + ' WHERE ' + column_name + ' LIKE ' + column_id
    cursor.execute(sql)
    myresults = cursor.fetchall()
    for x in myresults:
        print(x)

# This function is a very simple one it's whole purpose is to just show you which databases
# you have on the server that you're connected to
# It takes one parameter, the open connection that we have to the server, then it creates
# a cursor object with the cursor function on the connection
# Then I just have the cursor exectute the Show Databases command giving us all the databases
# I then loop through the cursor and print all the databases that were returned
def check_databases(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    for x in cursor:
        print(x)

# This function is very similar to the last function except this function returns all the tables we have
# in a specific database. It takes the same parameter just the connection object we have to our server
# It again creates a cursor object off that connection parameter. 
# I then have the cursor execute the SQL command Show Tables so we can get all the tables returned
# Finally I loop through all the tables that were returned and print them to the console 
def check_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    for x in cursor:
        print(x)

# This function creates a database from a given query that we send to it
# It takes two parameters the opne connection we have and the query we want to create a database from
# We start by creating the cursor object from our connection
# Then we try to execute the query with our cursor object and if it works we print that it was succesful
# If it doesn't work we throw the error that was returned so we knwo how to fix the issue
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

# This function is similar to the last one except in this one we are executing the query to the database
# It takes two parameters our open connection and the query that we want to execute
# I then again create a cursor object from using the cursor function on the connection parameter
# I start my try block using the cursor execute function on the query we want to execute
# Then after that with our open connection we use the commit function to push it into our database
# If this all works we then print a message saying that the query was succesful
# If not we go to our except block and print out the error that we encountered while trying to do it
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}")

# This function simply reads our query and then lets us know exactly what is in that specific query
# This takes two parameters our open connection to the databse and the query that we'd like to read
# I then again create a cursor object from the cursor function on our connection
# I created a result variable and set it to None at the top that way every time this function is called the result resets
# Then we enter the try block where it first uses the execute function on the query parameter
# Then i update my result variable to the cursor fetch all to get everything from that query
# It then returns our result variable giving us all the data from that query
# If that does not work it goes to the except block where it print out the error we ran into while trying 
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# This function is just a helper function for the read_query function so that you can see what was returned
# This takes one parameter the results from the read_query function
# Then it loops the results and prints off each item to the console
def print_results(results):
    for result in results:
        print(result)

# This function is similar to the last where it's more of a helper function but this one formatts the result
# It takes the same parameter jus the results from your query
# The first line I initialize and empty list so that everytime we run the function the list gets cleared first
# Next I loop through each result that is in the results we pass to the function
# I then turned each result into a list sense it'll have multiple parts i.e teach_id, first_name, last_name, etc.
# Then that result list gets appeneded to the empty list we initialized in the first line
# Then finally I just return the list and we get a list of lists as our output
def format_output(results):
    db_output = []
    for result in results:
        result = list(result)
        db_output.append(result)
    return db_output

# This function gives us a really clean and user friendly display of our data, it's similar to the last one but better
# This function uses the pandas library and the IPython library to display the data in a more digestable way
# It takes our list we made from the previous function as the parameter
# Then in the first line it creates a columns list, in this specifc columns list I assign the column names I want
# Then I create a dataFrame variable that is set to the pandas data frame function
# In this function it uses our list from the parameter to get the data then I set the columns to equal our columns list
# finally I use IPythons display function to be able to display the datafram I just created
def display_output(db_output):
    columns = ["course_id", "course_name", "language", "clinet_name", "address"]
    dataFrame = pd.DataFrame(db_output, columns = columns)
    display(dataFrame)

# This function is similar to our execute query function except this will execute a python list to the database
# It takes 3 parameters the open connection parameter, the SQL syntax, and the list of values we want to add
# It starts off with creating a cursor object from our open connection
# Then we enter the try block where I call the execute many function on the cursor instead of the just execute function
# This is where the first big difference comes in now the execute function takes the sql and the list of values
# Then I have the connection object commit the changes to the database
# If all of that goes well it will then print that the query was succesful in doing so
# If it does not work we enter the except block where we print the error that occured
def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql,val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error : '{err}'")

# This function is used to create a new table in our database
# It takes 2 parameters our open connection object and the name for the table that we want
# I first create a cursor object from the open connection object that is passed to the function
# I then create a list of column names and contraints for the column, this is more of an example
# the list can take however many column names wanted and any contraints as long as they are in SQL syntax
# then I create a sql variable that is given a SQL command in SQL syntax with our table name parameter and our columns list
# Finally the cursor uses the execute command using the sql variable adding the table to the database
def create_table(connection, table_name):
    cursor = connection.cursor()
    columns = ['first_name VARCHAR(60)', 'last_name VARCHAR(60)', 'personal_id INT', 'address VARCHAR(60)']
    sql = 'CREATE TABLE ' + table_name +  ' (' + ', '.join(columns) + ');'
    cursor.execute(sql)

# This function adds a new entry to a specified table we want to add to (This was by far my favorite function I was really proud of my work around and how to make it a bit dynamic)
# It takes 3 parameters the connection we have to the database the table name we want to add to and
# a list of values that will be added to the table
# The first thing I did in this function was create an empty list called table info so that it will always be empty when we call the function
# Then I do the same thing with an empty values list becuase we will need to add place holders to it
# I then like usual create the cursor object from the connection that was passed to the function
# After that I have the cursor execute the Describe SQL command on the given table
# This was so I could get all the column names from the given table
# I then loop through the column names and append the first index of each column to our table info array
# I chose the first index because that was where the identifier was for each column
# After that I created a columns variable and assigned that to the table info list we just created
# Then I loop the length of the columns array becuase I'm going to need a place holder for each item in the column
# I then append a %s (The SQL syntax for placeholder) to the values array so I have the correct amount of place holder for the table
# Then i create an sql variable where I write the proper SQL syntax to add an item to the table with our parameters
# I use the .join command to make sure each column name and value is joined into the syntax properly
# Then I call the execute list query function to have it added to the with our connection parameter, the sql variable, and the list of values passed into the function
def add_to_table(connection, table_name, val):
    table_info = []
    values = []    
    cursor = connection.cursor()
    cursor.execute("DESCRIBE " + table_name)
    for x in cursor:
        table_info.append(x[0])
    columns = table_info
    for i in range(len(columns)):
        values.append('%s')
    sql = 'INSERT INTO ' + table_name + ' (' + ', '.join(columns) + ') VALUES ' + '(' + ', '.join(values) + ')'
    execute_list_query(connection, sql, val)

# This function adds a constraint to a specified column in a specified table
# It takes 4 parameters our open connection, the table name, the contraint we want added and the column we want it done to
# The first thing I do like most of these functions is create a cursor object from our connection we passed to the function
# Then I create an sql variable that hold the proper SQL syntax with the parameters to add the constraint to the column
# Finally I just use the cursor execute function on the sql variable to execute the syntax
def add_constraint(connection, table_name, constraint, column):
    cursor = connection.cursor()
    sql = 'ALTER TABLE ' + table_name + ' ADD CONTRAINT ' + constraint + ' PRIMARY KEY ' + column + ';'
    cursor.execute(sql)

# This function is pretty simple one it just adds a column to a specified table
# It takes 4 parameters the open connnection to the database, the table you want an add a column to 
# the name of the new column you're adding and the type of entry it's going to be i.e VARCHAR, INT, BOOLEAN, etc.
# Again the first thing I do is create a cursor object from the connection parameter 
# Then i create the sql variable with the proper SQL syntax with our parameters to be able to add a new column
# Finally I use the cursor execute function on the sql variable to apply the column being added to the table
def add_column(connection, table_name, column_name, type_of_entry):
    cursor = connection.cursor()
    sql = 'ALTER TABLE ' + table_name + ' ADD ' + column_name + ' ' + type_of_entry + ';'
    cursor.execute(sql)

# This function is similar to the last one but it just changes the type of information in a specific column
# This takes 4 parameters the open connection to the database, the table you want to change a column in
# the column you want to change and the the new type of data you want to put in that column
# The first line creates a cursor object from the connection parameter
# I then create the sql variable that is set to the proper SQL syntax with the given parameters
# Finally I use the cursor execute function on the sql variable to apply the changes to the table
def alter_column (connection, table_name, column_name, new_type):
    cursor = connection.cursor()
    sql = 'ALTER TABLE ' + table_name + ' ALTER COLUMN ' + column_name + ' ' + new_type + ';'
    cursor.execute(sql)

# This function deletes an entire specified database
# It takes two parameters our open connection object and the name of the database
# I then create a cursor object with the open connection parameter
# Then I create an sql variable with proper SQL syntax with the databse parameter
# Finally I call the cursor execute function with the sql to apply the changes
def delete_databse(connection, database):
    cursor = connection.cursor()
    sql = 'DROP DATABASE ' + database + ';'
    cursor.execute(sql)

# This function deletes an entry from a specifed table with a specified identifier
# This takes 4 parameters an open connection to the database, the specified tables name that we want to delete from
# The id/column name that we want to delete from and then the specifc datas information that we want to delete
# I first create a cursor object from the connection parameter passed to the function
# Then i create a sql variable with the proper SQL syntax with the parameters given
# Then I use the cursor objects execute function with the sql variable to apply the changes to the table
def delete_entry(connection, table_name, id_name, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM ' + table_name + ' WHERE ' + id_name + ' = ' + id + ';'
    cursor.execute(sql)

# This function is used to delete an entire tables entries 
# It takes two parameters the open connection object and the specifed tables name
# I then create a cursor object from the connection parameter 
# Then i create a sql variable with the SQL syntax with our table name parameter
# Then i use the cursor execute function with the sql to apply the changes to the table
def delete_all_table_entires(connection, table_name):
    cursor = connection.cursor()
    sql = 'DELETE FROM ' + table_name + ";"
    cursor.execute(sql)

# This function deletes a column from a specifed
# It takes 3 parameters the open connection object, the specified table name, and the specified column name
# I then create a cursor object from the connection parameter
# I created a sql variable that has the SQL syntax to delete a column using our parameters
# Finally I use the cursor execute function to apply the changes to the table
def delete_column(connection, table_name, column_name):
    cursor = connection.cursor()
    sql = 'ALTER TABLE ' + table_name + ' DROP COLUMN ' + column_name + ';'
    cursor.execute(sql)

# This function deletes a whole table from the database
# It takes two parameters our open connection object and the specified table we want deleted
# I create a cursor object from the connection parameter given
# Then created a sql variable with SQL syntax with our table name parameter
# Finally use the cursor execute function with the sql to apply the changes to the table
def delete_table(connection, table_name):
    cursor = connection.cursor()
    sql = 'DROP TABLE ' + table_name + ';'
    cursor.execute(sql)

# This function deletes a unique constraint from a specified table
# It takes 3 parameters our open connection object, the specified table, and the specifed constraint
# I create a curosr object from our connection parameter that was passed to the function
# I create a sql variable that holds our proper SQL syntax with our parameters
# Finally I use the cursor execute function to apply the changes to the table
def delete_unqiue_constraint(connection, table_name, constraint):
    cursor = connection.cursor()
    sql = 'ALTER TABLE ' + table_name + ' DROP CONSTRAINT ' + constraint + ';'
    cursor.execute(sql)

# This function updates a specified entry with a whatever new value you want to asssign to it
# This takes 6 parameters our open connection object, the specified tables name, the identifier we want to change
# the new value we want for the identifier, the specific id to look for and then the original value of the idnetifier
# I first create a cursor object from our connection parameter we're given
# Then I have to modify the new identifier variable because we need it to have '' around it for SQL syntax
# Next I created a sql variable with the proper SQL syntax to update with our given parameters
# Finally I use the cursor execute function on the sql to apply the changes to the table 
def update_entry (connection, table_name, change_id, new_id, specific_id, id):
    cursor = connection.cursor()
    new_id = "'" + new_id + "'"
    sql = 'UPDATE ' + table_name + ' SET ' + change_id + " = " + new_id +  ' WHERE ' + specific_id + ' = ' + id + ';'
    cursor.execute(sql)

# This function orders a specified table by a specified column ascendingly
# This takes 3 parameters our open connection object, the specifed table name, and the specified column
# I first create a cursor object from our connection parameter
# Then I create a sql variable that holds the proper SQL syntax to order the table with our parameters
# Next I use the cursor execute function on the sql variable to apply the changes
# Then i have my cursor fetch all the information we just changes and store it in a variable
# I loop through all the fetch all information and print each result now ordered ascendinly  
def order_table(connection, table_name, column):
    cursor = connection.cursor()
    sql = 'SELECT * FROM '  + table_name +  ' ORDER BY ' + column
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x) 

# This function is similar to the last but it orders it in descending order
# It takes 3 parameters the open connection object, the specifed table name, the specifed column we want to order by
# I first create the cursor object from the connection parameter passed to the function
# The sql variable is declared and set to the proper SQL syntax with our parameters
# Then I use the cursor execute function with the sql varibale to apply to the changes
# I store the cursor fetch all function in a variable
# Then I loop through the variable printing all the data that was returned by the fetch all
def order_table_desc(connection, table_name, column):
    cursor = connection.cursor()
    sql = 'SELECT * FROM ' + table_name + ' ORDER BY ' + column + ' DESC'
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

# This function limits the amount of data we get returned to a specified number
# It takes 3 parameters the open connection object, the specified table name and the specified amount we want returned
# I created a cursor object with our connection parameter that was passed to the function
# I created a sql variable that holds the proper SQL syntax to make this possible with our parameters
# Inside the vsql variable I had to make the limit number a str because the SQL syntax does not take integers
# Then I have my cursor use the execute function with the sql variable
# I then have the cursor fetch all the data and store it in a variable
# I loop over the variable for every piece of data in it
# I then print out each peice of data in the variable to the console
def limit_search(connection, table_name, limit_num):
    cursor = connection.cursor()
    sql = 'SELECT * FROM ' + table_name + ' LIMIT ' + str(limit_num)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

# This function is similar to the last function but this lets you choose what positoin to start at
# It takes 4 parameters the open connection object, the specified table we want to search in
# the specified amount of data we want to retunr and the number entry we want to start at
# I first create a cursor object from our connection parameter
# Then I create a sql variable that stores our proper SQL syntax with our parameters
# Again I had to make the limit number a string and the offset number a string
# I then use the cursor execute function on the sql variable to apply changes
# Then I use the cursor fetch all function and store the returned data in a variable
# I then loop over every piece of data in the variable it's stored in
# Finally I print out all the data that was returned
def choose_position(connection, table, limit_num, offset_num):
    cursor = connection.cursor()
    sql = 'SELECT * FROM ' + table + ' LIMIT ' + str(limit_num) + ' OFFSET ' + str(offset_num)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x) 

#This is where I create my first table the teacher table
# I used pythons multiline string syntax so I could put it in a more readable way
# I Initialize the table creation in the first line with the CREATE TABLE then name the table teacher
# My first Column created is the teacher id which i made an int primary key
# Then figured I need their first name so i did that and made it a VARCHAR and sense they need a name it cant be null
# Then their last name similar to the first name i made it a VARCHAR and sense everyone has a last name made it not null
# Then I figured I'd get their language they speak and made it a VARCHAR and sense everyone speaks at least one the first can't be null
# Then I made a second language option so if they spoke two made it a VARCHAR but this one could be null
# Then their date of birth and just made it a DATE 
# Then their tax id sense everyone has to pay taxes and made it an INT but because everyones is different this one had to be unique
# Finally had them put in their phone number and just made it a VARCHAR 
create_teacher_table = """
CREATE TABLE teacher (
    teacher_id INT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    language_1 VARCHAR(3) NOT NULL,
    language_2 VARCHAR(3),
    dob DATE,
    tax_id INT UNIQUE,
    phone_no VARCHAR(30)
    
);
"""

# This is where I created the table for the parents of the students at the school
# I used pythons multi line string syntax to make this easier to read and understand
# The first line I declare the creation of the table and name it parent
# Then I gave the parents an id as that has to be an INT and made it a primary key
# Then the first_name is entered and has to be a VARCHAR and cannot be null
# This is the same for the last name has to be a VARCHAR and cannot be null
# I then figured the parents should speak a language too made it a VARCHAR and couldn't be null
# I added a birthdate as well and just made it a DATE
# Then because the parents also pay taxes they have a tax id and made it be an INT that has to be unique to them
# Then the parents also have a phone number that is set to be a VARCHAR 
create_parent_table = """
CREATE TABLE parent (
    parent_id INT PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    language_1 VARCHAR(3) NOT NULL,
    dob DATE,
    tax_id INT UNIQUE,
    phone_no VARCHAR(30)
    
);
"""

# This is where I created the table for the school clients i.e the vendors at the school
# Pythons multi line string syntax is used for reading ease
# I then declared the table and named it client
# The clients also need an ID which I made an INT PRIMARY KEY
# the clients needed a name so i made that a VARCHAR that cannot be null
# The clients also need to put the address of their company so i made that  a VARCHAR that couldn't be null
# Then I had the clients put what industry they work in 
create_client_table = """
CREATE TABLE client (
  client_id INT PRIMARY KEY,
  client_name VARCHAR(40) NOT NULL,
  address VARCHAR(60) NOT NULL,
  industry VARCHAR(20)
);
"""

# This is where I made a table for the students at the school
# Python multiline syntax was used for reading ease
# The first line was where i decalred the table to be made and named it student
# I then made the students need an ID and made it an INT and a PRIMARY KEY
# The students also need a first name I made a VARCHAR that cannot be null
# The students also need a last name I made a VARCHAR that cannot be null
# Then the students can also put in their phone number if theyd like it's also a VARCHAR
# Then the students can put in their parents id which is an INT
create_student_table = """
CREATE TABLE student (
  student_id INT PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  phone_no VARCHAR(20),
  parent INT
);
"""

# This is where i created the courses table so that we can see which courses are offered at the school
# Python multiline string syntax is used for ease of reading
# The first line I declare the table to be created then name it course
# The first entry is the course ID which is a INT PRIMARY KEY
# Then the courses name is a VARCHAR that can't be null
# Then the course specifies what language it's in which is a VARCHAR and can't be null
# Then the level of the course is put in and is also a VARCHAR
# Then we specify the course length as an INT
# Then the date is put in as a DATE
# Then we specifiy if the class is in person or not with a BOOLEAN
# The amount of teachers is the next column which is an INT
# Finally we say how many students can attend the class as an INT
create_course_table = """
CREATE TABLE course (
  course_id INT PRIMARY KEY,
  course_name VARCHAR(40) NOT NULL,
  language VARCHAR(3) NOT NULL,
  level VARCHAR(3),
  course_length_weeks INT,
  start_date DATE,
  in_person BOOLEAN,
  teacher INT,
  student INT
);
"""

# This is where I create the table for the sports offered by the school
# Python multiline string syntax is used for reading ease
# The first line I declare the table and name it sport
# The first column created is the sport id that is an INT PRIMARY KEY
# Then the sports name is next which is a VARCHAR and cannot be null
# Then the team size is added and has to be an INT
# Then which gender the sports team is which I made a single VARCHAR(Im sorry for not including more this was just easier to include 2)
# Then the length of how long the sport goes which is an INT
# then the start date of the sport which I made a DATE
# then I put if it was after school which is a BOOLEAN
# Then how many coaches coach the team which I made an INT
# Finally the teams rank in the sport which is an INT
create_sport_table = """
CREATE TABLE sport (
  sport_id INT PRIMARY KEY,
  sport_name VARCHAR(40) NOT NULL,
  team_size INT,
  gender VARCHAR(1),
  sport_length_weeks INT,
  start_date DATE,
  after_school BOOLEAN,
  coach INT,
  team_rank INT
);
"""

#This is where I created the lunch table which shows what kind of lunch is offered
# Python multiline string syntax was used for ease of reading
# The first line i decalred the table to be created and named it lunch
# The first column is the lunch id which has to be an INT PRIMARY KEY
# Then the kind of meal it is entered which has to be a VARCHAR and cant be null
# Then what kind of ethnicity the food is whihc is also a VARCHAR and can't be null
# Then the amount of protein that's in the meal which is also a VARCHAR and can't be null
# Next I have the amount available which is an INT
# I also have the date it will be served which is just a DATE
# Then it says if it's a hot lunch or not which is BOOLEAN
# Finally the last column is the cost for the lunch which is an INT
create_lunch_table = """
CREATE TABLE lunch (
  lunch_id INT PRIMARY KEY,
  lunch_meal VARCHAR(40) NOT NULL,
  food_ethnicity VARCHAR(40) NOT NULL,
  amount_of_protein VARCHAR(40) NOT NULL,
  amount_available INT,
  serving_date DATE,
  hot_lunch BOOLEAN,
  cost_amount INT
);
"""

# This is where I create the takescourse table 
# This table handles the M:M relationship between students and course
# Python multiline string syntax is used for ease of reading
# The first line is where I declare the table to be made and named it takes_course
# Then the first column I get the student ID which is an INT
# Then i get the course id which is an INT
# Then I set the PRIMARY KEY to be student id, course id
# Then the FOREIGN KEY for student id is pointed to refrence the student table student id and on delete it will cascade
# Then similarly the FOREGIN KEY course id is pointed to refrence the course table course id and on delete it will cascade
create_takescourse_table = """
CREATE TABLE takes_course (
  student_id INT,
  course_id INT,
  PRIMARY KEY(student_id, course_id),
  FOREIGN KEY(student_id) REFERENCES student(student_id) ON DELETE CASCADE,
  FOREIGN KEY(course_id) REFERENCES course(course_id) ON DELETE CASCADE
);
"""

# This is where I alter the student table
# Python multiline syntax is usedd for ease of reading
# The first line i declare the table to be altered and say the student table
# Then I add a FOREIGN KEY for the table that is the parent table
# This then refrences the parent id in the parent table
# Finally I declare that on Delete it sets it to null
alter_student = """
ALTER TABLE student
ADD FOREIGN KEY(parent)
REFERENCES parent(parent_id)
ON DELETE SET NULL;
"""

# This is where I alter the course table
# Python multiline syntax is used for ease of reading 
# The first line i declare the table to be altered and specify the course table
# Then i add a FOREIGN KEY which is the teacher table
# Then i point the refrence to teacher id in the teacher table
# Finally I say that on delete set it to null
alter_course = """
ALTER TABLE course
ADD FOREIGN KEY(teacher)
REFERENCES teacher(teacher_id)
ON DELETE SET NULL;
"""

#This is where I alter the course table again
# Python multiline string syntax is sued for eas of reading
# The first line I declare the table to be altered and say the course table
# Then I add a Foreign Key which is the student table
# I point the refrence to the student id in the student table
# Finally I say on delete set it to null
alter_course_again = """
ALTER TABLE course
ADD FOREIGN KEY(student)
REFERENCES student(student_id)
ON DELETE SET NULL;
"""

# This is where I populate the teacher Table 
# Python multiline syntax is used for ease of reading
# In the first line I declare to insert the values in the teacher table in the values
# I then add the first person
# Each person has their own one digit ID
# Each person has their own unique tax ID i.e 11111, 11112
# You can see that the values that can be null have a NULL value there and it's ok
# The DATE type is entered in there as year month day and is accepted as only that
# I put a + in front of the phone numbers that way it visually shows you its a phone number
# Each entry has to have a comma at the end of it unless it's the last one which has to have a semi colon
# I could've added as many as I wanted into the table but I decided to stop at 8 for ease
add_teacher = """
INSERT INTO teacher VALUES
(1,  'Margaret', 'Grump', 'ENG', NULL, '1976-03-07', 11111, '+4805151978'),
(2, 'Ben', 'Wazowski', 'ENG', 'SPA', '1984-11-06', 11112, '+4806784563'),
(3, 'John', 'Shoeman', 'FRA', 'ENG', '1999-12-19', 11113, '+4783459870'),
(4, 'Michael', 'Fillino', 'JAP', 'ENG', '1967-01-18', 11114, '+5678903456'),
(5, 'Chris', 'Lesher', 'MAN', 'FRA', '1945-04-22', 11115, '+7653459876'),
(6, 'Lauren', 'Johnson', 'ENG', NULL, '1900-05-14', 11116, '+8765789098'),
(7, 'Annie', 'Dwayne', 'FRA', 'ENG', '1978-04-20', 11117, '+6025404234'),
(8, 'Jill', 'Baractio', 'GER', 'FRA', '1966-10-28', 11118, '+5678768909');
"""

# This is where I populate the client table 
# Python multiline string syntax is used here for ease of reading
# The first line i declare this gets inserted into the client table in values
# you can see each client has their own 3 digit id
# The first string is the comapny they own
# The second is their address for their company
# Then finally what they're product is
# Again you can see each entry ends with a comma except for the final one ending in a semi colon
# I couldv'e added more than this but for ease I stopped here
add_client = """
INSERT INTO client VALUES
(101, 'Mommas Cookies', '345 W Forest St', 'Cookies'),
(102, 'Super Soda', '466 N Cool Rd', 'Soda'),
(103, 'Computers Inc', '677 E Road Rd', 'Tech'),
(104, 'Art Force', '678 W Milton St', 'Art'),
(105, 'Space Raiders', '455 E Riding Dr', 'Clothing'),
(106, 'PogoSticks', '567 N Mountain Blvd', 'Pogo');
"""

# This is where I populate the student table
# Python multiline string syntax is used here for ease
# The first line I declare this to be inserted into the participant table in values
# You can see Each student has their own ID number 
# Each student also has their parents ID number (ignore that their last names aren't the same)
# The students name is seen being a string and can repeat it just doesnt happen to repeat here
# This is the same for their last name doesnt have to be unique but just happens to be
# I put a + in front of their phone numbers because I thought it made it stand out as a phone number
# instead of some random line of digits in a row
# Again notice each entry ends with a comma except for the final one that ends with a semicolon
# We also could've had a null value in the phone numbers but there just happens to not be one
# I could've added more entries into the table but decided to stop here 
add_student = """
INSERT INTO student VALUES
(101, 'Greg', 'Jerimiah', '+5674897890', 100),
(102, 'Ben', 'Rocks', '+8764784657', 101),
(103, 'Josh', 'Gremionie', '+8737894567', 102),
(104, 'Alex', 'Potter', '+2356745673', 103),
(105, 'Hunter', 'Drakings', '+1848943678', 104),
(106, 'Kyle', 'Helere', '+5904789023', 105),
(107, 'Will', 'Junsting', '+4683464567', 106),
(108, 'Nick', 'Solone', '+5890983575', 107),
(109, 'Lauren', 'Serenu', '+4785901235', 108),
(110, 'Olivia', 'Linings', '+2895673890', 109),
(111, 'Annah', 'Grosce', '+3903564789', 110),
(112, 'Vanessa', 'Miller', '+9870983456', 111);
"""

# This is where I populate the parent table 
# Python multiline String syntax is used for ease of reading
# In the first line i declare that this be insert into the parent table in values
# You'll see that each parent has own 3 digit id
# The parents also have their first names in a string of characters
# This is also the same with theirnlast names
# Then we have that 3 character abreiviation of what language they speak
# Next their date of birth is insert in in date form which is year month day with dashes in between
# Then they all have their own unique 5 digit tax id
# It's important to know that this i sunique becuase we cannot have any repeats of the id in the table
# Then I have their phone numbers with a + to show it's a phone number and not just some random number
# each entry is followed by a comma except the last one followed by a semi colon
add_parent = """
INSERT INTO parent VALUES
(100, 'George', 'Finnigan', 'ENG', '1980-08-10', 11111, '+3783569000'),
(101, 'Henry', 'Shamrock', 'ENG', '1966-09-09', 11112, '+6358987654'),
(102, 'Jacob', 'Chairs', 'FRA', '1963-12-23', 11113, '+9089876567'),
(103, 'Mark', 'Larkin', 'GER', '1982-07-06', 11114, '+9809098777'),
(104, 'Doug', 'Dravin', 'FRA', '1976-03-25', 11115, '+4798973649'),
(105, 'Maureen', 'Frongle', 'MAN', '1978-02-13', 11116, '+3784684783'),
(106, 'Laura', 'Shalamoo', 'ENG', '1965-12-10', 11117, '+378947585'),
(107, 'Sharon', 'Sydney', 'SPA', '1974-07-26', 11118, '+3456278467'),
(108, 'Karen', 'Smith', 'ENG', '1978-11-16', 11119, '+2789463759'),
(109, 'Gertrude', 'Jenkins', 'SPA', '1984-09-11', 12111, '+3658356489'),
(110, 'Bob', 'Rodgers', 'GER', '1990-05-14', 12112, '+4678594652'),
(111, 'Jessica', 'Manning', 'FRA', '1991-10-27', 12113, '+6093795789');
"""

# This is where I populate the courses table
# Python multiline syntax is used here for ease of reading
# The first line I declare that it gets inserted into the course table in values
# Each course has its own unqiue 2 digit id
# Then we have the string of characters saying what kind of course it is
# Then I have the 3 character abrieviation for what language it's taught in
# Then I have the 3 character string that shows what level the course is
# Then I have the INT that shows how many weeks long the course is
# Next is the start date for the course which is in DATE form
# Then we have the boolean value to say wether it's in person or not
# Then the final int is the number of seats available
# Each entry ends in a comma except for the final ending in a semicolon
# I could've kept adding course but creativity ran out
add_course = """
INSERT INTO course VALUES
(12, 'Theoretical Mathmatics', 'ENG', '400', 16, '2021-08-22', TRUE, 1, 101),
(13, 'Intro Mathmatics', 'ENG', '100', 16, '2021-08-22', TRUE, 1, 102),
(14, 'Geometry Mathmatics', 'FRA', '200', 8, '2021-10-10', FALSE, 1, 103),
(15, 'Trigonometry Mathmatics', 'MAN', '200', 4, '2021-11-10', FALSE, 1, 104),
(16, 'Calculus I Mathmatics', 'ENG', '200', 8, '2021-10-10', TRUE, 1, 105),
(17, 'Calculus II Mathmatics', 'GER', '300', 10, '2021-09-14', TRUE, 1, 106),
(18, 'Calculus III Mathmatics', 'SPA', '400', 16, '2021-08-22', FALSE, 1, 107),
(19, 'Discrete Mathmatics', 'FRA', '300', 10, '2021-09-14', TRUE, 1, 108),
(20, 'Linear Algebra Mathmatics', 'ENG', '300', 4, '2021-11-20', TRUE, 1, 109),
(21, 'Statistics Mathmatics', 'GER', '200', 8, '2021-10-10', FALSE, 1, 110);
"""

# This is where I populate the sports table
# Python multiline syntax is used for ease of reading
# The first line i declare to insert it into the sport table in values
# Each sport has their own 2 digit id
# Then we have the string of characters for the sport name
# Next we have an INT for how many people are on the team
# I have a single char to describe if it's a girls sport a guys sport
# The next int tells us how many weeks the sport goes for
# the next entry into the table will be the start date for the sport which is in DATE form
# Then we have the boolean value for if it's after school or not
# The next int is to say how many coaches the team has
# Finally the final int is the rank of the team (The Badminton team is number 1)
add_sports = """
INSERT INTO sport VALUES
(10, 'Soccer', 10, 'M', 16, '2021-08-22', TRUE, 1, 12),
(20, 'Football', 32, 'M', 16, '2021-08-22', TRUE, 1, 16),
(30, 'Baseball', 26, 'M', 8, '2021-10-10', TRUE, 1, 16),
(40, 'Basketball', 35, 'M', 16, '2021-11-10', TRUE, 1, 20),
(50, 'Lacrosse', 35, 'M', 8, '2021-10-10', FALSE, 1, 19),
(60, 'Badminton', 18, 'F', 8, '2021-09-14', FALSE, 1, 1),
(70, 'Golf', 8, 'F', 12, '2021-08-22', FALSE, 1, 10),
(80, 'Softball', 30, 'F', 10, '2021-09-14', TRUE, 1, 9),
(90, 'Hockey', 29, 'M', 4, '2021-11-20', TRUE, 1, 5),
(11, 'Volleyball', 25, 'F', 8, '2021-10-10', FALSE, 1, 12);
"""

# This is where i populate the lunch tabler
# Python multiline syntax is used for ease of reading
# The first line i decalre to insert into the lunch table in values
# Each lunch meal has it's own id and can be any int
# The lunch meal is then shown in a string saying what it is
# The ethnicity is also a string of chars saying what kind of food it is
# After that we have the string of chars that tells you how much protein is in the meal
# The quanity of the meal is then inserted into the table in INT form
# Then the date it's served will be entered after in DATE form
# Next the boolean value for if the lunch is hot or not is entered
# Then finally the price for the meal is inserted in INT form
# Each entry ends in a comma except for the last one ends in a semi colon
add_lunch = """
INSERT INTO lunch VALUES
(1, 'Meatloaf', 'American', '20g', 35, '2021-08-22', TRUE, 4),
(2, 'Grilled Cheese', 'American', '5g', 40, '2021-08-23', TRUE, 3),
(3, 'Orange Chicken', 'Asian', '25g', 20, '2021-08-24', TRUE, 5),
(4, 'Burrito', 'Mexican', '30g', 27, '2021-08-25', TRUE, 1, 2),
(5, 'Pizza', 'Itallian', '10g', 17, '2021-08-26', TRUE, 1, 4),
(6, 'Chicken Nuggets', 'American', '18g', 11, '2021-08-27', TRUE, 3),
(7, 'Hummus', 'Greek', '8g', 29, '2021-08-28', FALSE, 2),
(8, 'Asian Salad', 'Asian', '6g', 38, '2021-08-29', FALSE, 3),
(9, 'Meatball Sub', 'Itallian', '21g', 10, '2021-08-30', TRUE, 5),
(10, 'Nachos', 'Mexican', '6g', 8, '2021-08-31', TRUE, 3);
"""

# This is where we populate the takes course table
# Python multiline string syntax is used for ease of reading
# The first line i declare that it's inserted into the takes course table values
# The first INT to be inserted will be the student ID 
# The other INT is the course ID
# Each entry is followed by a comma except the final one is followed by a semicolon
add_takescourse = """
INSERT INTO takes_course VALUES
(101, 16),
(102, 12),
(104, 14),
(102, 15),
(105, 20),
(103, 16),
(101, 12),
(103, 13),
(102, 13),
(101, 17),
(105, 21),
(104, 18),
(102, 15),
(102, 14),
(103, 13),
(102, 14),
(105, 15),
(104, 20);
"""

# This is my first query
# This is used with the read_query function
# it returns all the entries from the teacher table
q1 = """
SELECT *
FROM teacher;
"""

# This is my second query
# This is used with the read_query function
# it returns all the entries from the course table
q2 = """
SELECT *
FROM course;
"""

# This is my third query
# This is used with the read_query function
# it returns all the entries from the client table
q3 = """
SELECT *
FROM client;
"""

# This is my fourth query
# This is used with the read_query function
# it returns all the entries from the student table
q4 = """
SELECT *
FROM student;
"""

# This is my fifth query
# This is used with the read_query function
# it returns all the entries from the parent table
q5 = """
SELECT *
FROM parent;
"""

# This is my sixth query
# This is used with the read_query function
# it returns all the entries from the sport table
q6 = """
SELECT *
FROM sport;
"""

# This is my seventh query
# This is used with the read_query function
# it returns all the entries from the lunch table
q7 = """
SELECT *
FROM lunch;
"""
#This is the host name for the server
host = "localhost"

#This is the username for the server
username = "root"

#This is the password for the server
password = "Compl3xity!"

#This is the database name
database = "school"

#This variable stores the connection we make in the create db connection function
connection = create_db_connection(host, username, password, database)

#This adds the teacher table to the database
execute_query(connection, create_teacher_table)

#This adds the client table to the database
execute_query(connection, create_client_table)

#This adds the student table to the database
execute_query(connection, create_student_table)

#This adds the course table to the database
execute_query(connection, create_course_table)

#This adds the parent table to the database
execute_query(connection, create_parent_table)

#This adds the lunch table to the database
execute_query(connection, create_lunch_table)

#This adds the sport table to the database
execute_query(connection, create_sport_table)

#This alters the student table
execute_query(connection, alter_student)

#This alters the student table
execute_query(connection, alter_course)

#This alters the student table
execute_query(connection, alter_course_again)

#This adds the takes course table to the database
execute_query(connection, create_takescourse_table)

#This populates the teacher table
execute_query(connection, add_sports)

#This populates the course table
execute_query(connection, add_course)

#This populates the takescourse table
execute_query(connection, add_takescourse)

#This populates the parent table
execute_query(connection, add_parent)

#This populates the lunch table
execute_query(connection, add_lunch)

#This populates the client table
execute_query(connection, add_client)

#This populates the student table
execute_query(connection, add_student)





