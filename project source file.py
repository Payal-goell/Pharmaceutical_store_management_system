import mysql.connector
import datetime
from tabulate import tabulate
db=input("Enter name of database : ")
mydb=mysql.connector.connect(host="localhost",user="root",password="dstvtush04")
mycursor=mydb.cursor()
sql="CREATE DATABASE if not exists %s" %(db,)
mycursor.execute(sql)
print("Database being used is",db)
mycursor=mydb.cursor()
mycursor.execute("use "+db)
TableName=input("Enter name of the table which is to be created or whose records are to be fetched : ")
query="Create table if not exists "+TableName+"(Customer_ID int primary key,Name varchar(50) not null,Disease varchar(50),Medicine varchar(50),Balance float,Last_Purchase_Date varchar(15))" 
print("Table "+TableName+" fetched successfully")
mycursor.execute(query)
while True:
                print('\n\n\n')
                print("*_."*45)
                print('\t\t\t\t\t\t\tMAIN MENU')
                print("*_."*45)
                print('\t\t\t\t\t1. Add Customer Record')
                print('\t\t\t\t\t2. Display Record of all Customers')
                print('\t\t\t\t\t3. Display Record of particular Customer')
                print('\t\t\t\t\t4. Delete Record of all Customers')
                print('\t\t\t\t\t5. Delete Record of Particular Customer')
                print('\t\t\t\t\t6. Modify Record of  Customer')
                print('\t\t\t\t\t7. Exit')
                ch=int(input("Enter your choice : "))
                if ch==1:
                                print('Your choice is 1. Add Customer Record')
                                try:
                                                print('Enter customer details')
                                                cust_id=int(input('Enter customer ID : '))
                                                cust_name=input('Enter customer name : ')
                                                cust_dis=input(‘Enter the disease customer is suffering from :’)
                                                cust_med=input('Enter prescribed Medicine : ')
                                                cust_bal=input('Enter net balance of customer : ')
                                                cust_hist=input('Enter last purchase date(DD/MM/YYYY) : ')
                                                rec=(cust_id,cust_name,cust_dis,cust_med,cust_bal,cust_hist)
                                                query="insert into "+TableName+" values (%s,%s,%s,%s,%s,%s)"
                                                mycursor.execute(query,rec)
                                                mydb.commit()
                                                print("Record added successfully....")
                                except Exception as e:
                                                print('Something went wrong',e)
                elif ch==2:
                                print('Your choice is 2. Display Record of all Customers')
                                try:
                                                query='select * from ' +TableName
                                                mycursor.execute(query)
                                                print(tabulate(mycursor, headers=['Customer ID', 'Name','Disease','Prescribed Medicine','Net Balance','Last Purchase Date'],tablefmt='psql'))
                                except Exception as e:
                                                print('Something went wrong',e)
                elif ch==3:
                                print('Your choice is 3. Display Record of particular Customer')
                                try:
                                                cid=input("Enter Customer ID : ")
                                                query='select * from '+TableName+" where Customer_ID = %s"
                                                mycursor.execute(query,(cid,))
                                                myrecord=mycursor.fetchone()
                                                if myrecord is None:
                                                                print("No record found")
                                                else:
                                                                print("\n\nRecord of Customer ID:"+cid)
                                                                print(myrecord)
                                except Exception as e:
                                                print('Something went wrong',e)
                elif ch==4:
                                print('Your choice is 4. Delete Record of all Customers')
                                try:
                                                ch=input('Do you want to delete all the records(y/n)?')
                                                if ch=='y':
                                                                mycursor.execute('delete from '+TableName)
                                                                mydb.commit()
                                                                print('All the records deleted')
                                except Exception as e:
                                                print('Something went wrong',e)
                elif ch==5:
                                print('Your choice is 5. Delete Record of Particular Customer')
                                try:
                                                cid=input('Enter customer ID to be deleted : ')
                                                query='delete from '+TableName+' where Customer_ID = %s'
                                                mycursor.execute(query,(cid,))
                                                mydb.commit()
                                                c=mycursor.rowcount
                                                if c>0:
                                                                print('Deletion done')
                                                else:
                                                                print('Customer ID',cid,'not found')
                                except Exception as e:
                                                print('Something went wrong',e)
                elif ch==6:
                                print('Your choice is 6. Modify Record of  Customer')
                                try:
                                                cid=input('Enter customer ID of the record to be modified : ')
                                                query='select * from '+TableName+' where Customer_ID= %s'
                                                mycursor.execute(query,(cid,))
                                                myrecord=mycursor.fetchone()
                                                if myrecord is None:
                                                                print('Customer ID '+cid+' does not exist')
                                                else:
                                                                cust_med=myrecord[3]
                                                                cust_bal=myrecord[4]
                                                                cust_hist=myrecord[5]
                                                                print('ID                   :',myrecord[0])
                                                                print('Name                 :',myrecord[1])
                                                                print('Disease              :',myrecord[2])
                                                                print('Medicine             :',myrecord[3])
                                                                print('Balance              :',myrecord[4])
                                                                print('Last Purchase date   :',myrecord[5])
                                                                print('Type the new values or just press enter to have the same')
                                                                x=input('Enter Medicine : ')
                                                                if len(x)>0:
                                                                                cust_med=x
                                                                x=input('Enter Net Balance : ')
                                                                if len(x)>0:
                                                                                cust_bal=x
                                                                x=input('Enter Last Purchase Date : ')
                                                                if len(x)>0:
                                                                                cust_hist=x
                                                                query='update '+TableName+' set Medicine=%s, Balance=%s, Last_Purchase_Date=%s where Customer_ID=%s'
                                                                mycursor.execute(query,(cust_med,cust_bal,cust_hist,cid))
                                                                mydb.commit()
                                                                print('Records Updated')
                                except Exception as e:
                                                print('Something went wrong',e)
                                        
                elif ch==7:
                                print('Thank You for sparing your time')
                                break
                else:
                                print("Wrong Choice")
