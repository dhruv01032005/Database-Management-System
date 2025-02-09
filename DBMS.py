#PROGRAM STARTS
print("****SALES AND PUCHASES MANAGEMENT****")

#CREATING DATABASES
import mysql.connector as myc
import random

password=input("Enter the password of the root::") #dhruv123

mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8")
cur=mydb.cursor()
cur.execute("create database if not exists sale_invoice")
cur.execute("create database if not exists purchase_invoice")
cur.execute("create database if not exists stock")
mydb.close()

#CREATING NEW SALE INVOICE:
def cnsi(password):
    reciept_no=random.randint(100000,200000)
    company_name=input("enter the company name(a_b_c)::")
    date=input("enter the date(dd_mm_yyyy)::")
    table_name=str(reciept_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    cur.execute(f"create table if not exists {table_name}(product_id int primary key,product_name varchar(100),selling_price int,qty int,total_price int)") #inserting fields in table
    num=int(input("enter the number of different products::"))
    for k in range(num):
        product_id=int(input("enter product id(of 7 nos.)::"))
        product_name=input("enter the name of the product::")
        selling_price=int(input("enter the price of the product::"))
        qty=int(input("enter the qty of the product::"))
        total_price=int(selling_price*qty)
        sql=f"insert into {table_name}(product_id,product_name,selling_price,qty,total_price)values(%s,%s,%s,%s,%s)"
        val=[product_id,product_name,selling_price,qty,total_price] # inserting values in table
        cur.execute(sql,val)
        mydb.commit()
        mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
        cur_2=mydb_2.cursor()
        cur_2.execute(f"update stock set qty=qty-{qty} where product_id='{product_id}'")
        mydb_2.commit()
        mydb_2.close()
    mydb.close()    
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    print("RECIEPT NO =",reciept_no)
    print("COMPANY NAME =",company_name)
    print("DATE =",date)
    cur.execute(f"select * from {table_name}") # displaying table values
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#DELETING EXISTING SALE INVOICE
def desi(password):
    reciept_no=int(input("enter the reciept no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(reciept_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    cur.execute(f"select * from {table_name}")
    data=cur.fetchall()
    for i in data:
        mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
        cur_2=mydb_2.cursor()
        cur_2.execute(f"update stock set qty=qty+{i[3]} where product_id={i[0]}")
        mydb_2.commit()
        mydb_2.close()
    cur.execute(f"drop table {table_name}") #drop table statement 
    print(f"***{table_name} is deleted***")
    mydb.close()
    
#CUSTOMISING EXISTING SALE INVOICE
def cesi(password):
    reciept_no=int(input("enter the reciept no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(reciept_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    existing_product_id=int(input("enter the product id in which there is a change(of 7 nos.)::"))
    changed_selling_price=int(input("enter the changed value of selling price::"))
    changed_qty=int(input("enter the changed value of qty::"))
    changed_total_price=int(changed_selling_price*changed_qty)
    cur.execute(f"select * from {table_name}")
    data=cur.fetchall()
    for k in data:
        if k[0]==existing_product_id:
            old_qty=k[3]
        else:
            continue
    mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
    cur_2=mydb_2.cursor()
    cur_2.execute(f"update stock set qty=qty+{old_qty}-{changed_qty} where product_id={existing_product_id}")
    mydb_2.commit()
    mydb_2.close()
    cur.execute(f"update {table_name} set selling_price={changed_selling_price} where product_id={existing_product_id}") #SELLING PRICE CHANGE STATEMENT
    cur.execute(f"update {table_name} set qty={changed_qty} where product_id={existing_product_id}") #QTY CHANGE STATEMENT
    cur.execute(f"update {table_name} set total_price={changed_total_price} where product_id={existing_product_id}") #TOTAL PRICE CHANGE STATEMENT
    mydb.commit()
    cur.execute(f"select * from {table_name}") #DISPLAYING NEW TABLE VALUES
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    print("***table has been customised***")
    mydb.close()
    
#CREATING NEW PURCHASE INVOICE:
def cnpi(password):
    purchase_no=random.randint(200000,300000)
    company_name=input("enter the company name(a_b_c)::")
    date=input("enter the date(dd_mm_yyyy)::")
    table_name=str(purchase_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    cur.execute(f"create table if not exists {table_name}(product_id int primary key,product_name varchar(100),cost_price int,qty int,total_price int)") #inserting fields in table
    num=int(input("enter the number of different products::"))
    for k in range(num):
        product_id=int(input("enter product id(of 7 nos.)::"))
        product_name=input("enter the name of the product::")
        cost_price=int(input("enter the price of the product::"))
        qty=int(input("enter the qty of the product::"))
        total_price=int(cost_price*qty)
        sql=f"insert into {table_name}(product_id,product_name,cost_price,qty,total_price)values(%s,%s,%s,%s,%s)"
        val=[product_id,product_name,cost_price,qty,total_price] # inserting values in table
        cur.execute(sql,val)
        mydb.commit()
        l=[]
        mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
        cur_2=mydb_2.cursor()
        cur_2.execute("create table if not exists stock(product_id int primary key,product_name varchar(100),qty int)") #inserting fields in table
        cur_2.execute("select * from stock")
        data=cur_2.fetchall()
        for j in data:
            l.append(j[0])
        if product_id in l:
            cur_2.execute(f"update stock set qty=qty+{qty} where product_id='{product_id}'")
            mydb_2.commit()
        else:
            sql_2="insert into stock(product_id,product_name,qty)values(%s,%s,%s)"
            val_2=[product_id,product_name,qty] # inserting values in table
            cur_2.execute(sql_2,val_2)
            mydb_2.commit()
        mydb_2.close()
    mydb.close()    
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    print("PURCHASE NO =",purchase_no)
    print("COMPANY NAME =",company_name)
    print("DATE =",date)
    cur.execute(f"select * from {table_name}") # displaying table values
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#DELETING EXISTING PURCHASE INVOICE
def depi(password):
    purchase_no=int(input("enter the purchase no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(purchase_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    cur.execute(f"select * from {table_name}")
    data=cur.fetchall()
    for i in data:
        mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
        cur_2=mydb_2.cursor()
        cur_2.execute(f"update stock set qty=qty-{i[3]} where product_id={i[0]}")
        mydb_2.commit()
        mydb_2.close()
    cur.execute(f"drop table {table_name}") #drop table statement 
    print(f"***{table_name} is deleted***")
    mydb.close()
    
#CUSTOMISING EXISTING PURCHASE INVOICE
def cepi(password):
    purchase_no=int(input("enter the purchase no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(purchase_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    existing_product_id=int(input("enter the product id in which there is a change(of 7 nos.)::"))
    changed_cost_price=int(input("enter the changed value of cost price::"))
    changed_qty=int(input("enter the changed value of qty::"))
    changed_total_price=int(changed_cost_price*changed_qty)
    cur.execute(f"select * from {table_name}")
    data=cur.fetchall()
    for k in data:
        if k[0]==existing_product_id:
            old_qty=k[3]
        else:
            continue
    mydb_2=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
    cur_2=mydb_2.cursor()
    cur_2.execute(f"update stock set qty=qty+{changed_qty}-{old_qty} where product_id={existing_product_id}")
    mydb_2.commit()
    mydb_2.close()
    cur.execute(f"update {table_name} set cost_price={changed_cost_price} where product_id={existing_product_id}") #SELLING PRICE CHANGE STATEMENT
    cur.execute(f"update {table_name} set qty={changed_qty} where product_id={existing_product_id}") #QTY CHANGE STATEMENT
    cur.execute(f"update {table_name} set total_price={changed_total_price} where product_id={existing_product_id}") #TOTAL PRICE CHANGE STATEMENT
    mydb.commit()
    cur.execute(f"select * from {table_name}") #DISPLAYING NEW TABLE VALUES
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    print("***table has been customised***")
    mydb.close()
    
#SHOWING ALL EXISTING SALE INVOICE
def saesi(password):
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    print("***THESE ARE EXISTING SALE INVOICE***")
    cur.execute("show tables") #TO SHOW TABLE STATEMENT 
    for table_name in cur:
        print(table_name)
    mydb.close()
    
#SHOWING ANY ONE EXISTING SALE INVOICE
def soesi(password):
    reciept_no=int(input("enter the reciept no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(reciept_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    print(f"***THIS IS {table_name}***")
    cur.execute(f"select * from {table_name}") #DISPLAYING TABLE VALUES
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#SHOWING SALE INVOICE ON PARTICULAR DAY
def srtd(password):
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="sale_invoice")
    cur=mydb.cursor()
    cur.execute(f"show tables like '%{date}';")
    data=cur.fetchall()
    for i in data:
        table_name=i[0]
        print("***THIS IS",table_name,"***")
        cur.execute(f"select * from {table_name}") #DISPLAYING TABLE VALUES
        data=cur.fetchall()
        for j in data:
            print(j)
        cur.execute(f"select sum(total_price) from {table_name}")
        print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#SHOWING EXISTING ALL PURCHASE INVOICE
def saepi(password):
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    print("***THESE ARE EXISTING PURCHASE INVOICE***")
    cur.execute("show tables") #TO SHOW TABLE STATEMENT 
    for table_name in cur:
        print(table_name)
    mydb.close()
    
#SHOWING ANY ONE EXISTING PURCHASE INVOICE
def soepi(password):
    purchase_no=int(input("enter the purchase no. of the desired table::"))
    company_name=input("enter the company name of the desired table(a_b_c)::")
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    table_name=str(purchase_no)+"_"+company_name+"_"+date
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    print(f"***THIS IS {table_name}***")
    cur.execute(f"select * from {table_name}") #DISPLAYING TABLE VALUES
    data=cur.fetchall()
    for i in data:
        print(i)
    cur.execute(f"select sum(total_price) from {table_name}")
    print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#SHOWING PURCHASE INVOICE ON PARTICULAR DAY
def prtd(password):
    date=input("enter the date of the desired table(dd_mm_yyyy)::")
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="purchase_invoice")
    cur=mydb.cursor()
    cur.execute(f"show tables like '%{date}';")
    data=cur.fetchall()
    for i in data:
        table_name=i[0]
        print("***THIS IS",table_name,"***")
        cur.execute(f"select * from {table_name}") #DISPLAYING TABLE VALUES
        data=cur.fetchall()
        for j in data:
            print(j)
        cur.execute(f"select sum(total_price) from {table_name}")
        print("total bill =",cur.fetchall()[0][0])
    mydb.close()
    
#SHOW STOCK
def ss(password):
    mydb=myc.connect(host="localhost",user="root",passwd=password,charset="utf8",database="stock")
    cur=mydb.cursor()
    print("***STOCK***")
    cur.execute("select * from stock") #TO SHOW TABLE STATEMENT 
    data=cur.fetchall()
    for i in data:
        print(i)
    mydb.close()
    
#MAIN PROGRAM
#CREATING OPTIONS
while True:
    print("1=FUNCTIONS ON SALE INVOICE")
    print("2=FUNCTIONS ON PURSHASE INVOICE")
    print("3=DISPLAY SALE INVOICE")
    print("4=DISPLAY PURCHASE INVOICE")
    print("5=DISPLAY STOCK")
    print("6=EXIT")
    ch=int(input("Enter your choice::"))
    
#FIRST OPTION FUNCTIONS ON SALE INVOICE
    if ch==1:
        print("1=CREATE NEW SALE INVOICE")
        print("2=DELETE EXISTING SALE INVOICE")
        print("3=CUSTOMISE EXISTING SALE INVOICE")
        print("4=EXIT")
        ch_1=int(input("Enter your choice::"))

#FIRST OPTION FIRST CHOICE CREATING NEW SALE INVOICE
        if ch_1==1:
            cnsi(password)
#FIRST OPTION SECOND CHOICE DELETING EXISTING SALE INVOICE
        elif ch_1==2:
            desi(password)
#FIRST OPTION THIRD CHOICE CUSTOMISING EXISTING SALE INVOICE
        elif ch_1==3:
            cesi(password)
#FIRST OPTION FORTH CHOICE
        else:
            continue
            
#SECOND OPTION FUNCTIONS ON PURCHASE INVOICE
    elif ch==2:
        print("1=CREATE NEW PURCHASE INVOICE")
        print("2=DELETE EXISTING PURCHASE INVOICE")
        print("3=CUSTOMISE EXISTING PURCHASE INVOICE")
        print("4=EXIT")
        ch_2=int(input("Enter your choice::"))
        
#SECOND OPTION FIRST CHOICE CREATING NEW PURCHASE INVOICE
        if ch_2==1:
            cnpi(password)
#SECOND OPTION SECOND CHOICE DELETING EXISTING PURCHASE INVOICE
        elif ch_2==2:
            depi(password)
#SECOND OPTION THIRD CHOICE CUSTOMISING EXISTING PURCHASE INVOICE
        elif ch_2==3:
            cepi(password)
#SECOND OPTION FORTH CHOICE
        else:
            continue

#THIRD OPTION DISPLAYING SALE INVOICE
    elif ch==3:
        print("1=SHOW ALL EXISTING SALE INVOICE NAME")
        print("2=SHOW ANY ONE EXISTING SALE INVOICE NAME")
        print("3=SHOW SALE INVOICE NAME WITH RESPECT TO DATE")
        print("4=EXIT")
        ch_3=int(input("enter your choice::"))

#THIRD OPTION FIRST CHOICE SHOWING ALL EXISTING SALE INVOICE NAME
        if ch_3==1:
            saesi(password)
#THIRD OPTION SECOND CHOICE SHOWING ANY ONE EXISTING SALE INVOICE NAME        
        elif ch_3==2:
            soesi(password)
#THIRD OPTION THIRD CHOICE SHOWING SALE INVOICE WITH RESPECT TO DATE
        elif ch_3==3:
            srtd(password)
#THIRD OPTION FORTH CHOICE
        else:
            continue

    
    elif ch==4:
        print("1=SHOW ALL EXISTING PURCHASE INVOICE")
        print("2=SHOW ANY ONE EXISTING PURCHASE INVOICE")
        print("3=SHOW PURCHASE INVOICE NAME WITH RESPECT TO DATE")
        print("4=EXIT")
        ch_4=int(input("enter your choice::"))
        
#FORTH OPTION FIRST CHOICE SHOWING ALL EXISTING PURCHASE INVOICE NAME
        if ch_4==1:
            saepi(password)
#FORTH OPTION SECOND CHOICE SHOWING ANY ONE EXISTING PURCHASE INVOICE NAME        
        elif ch_4==2:
            soepi(password)
#FORTH OPTION THIRD CHOICE SHOWING PURCHASE INVOICE WITH RESPECT TO DATE
        elif ch_4==3:
            prtd(password)
#FORTH OPTION FORTH CHOICE SHOWING SALE INVOICE WITH RESPECT TO DATE
        else:
            continue

#FIFTH OPTION TO SHOW STOCK
    elif ch==5:
        ss(password)

    else:
        break