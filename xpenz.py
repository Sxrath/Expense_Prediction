import mysql.connector
from email_validator import validate_email, EmailNotValidError
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sqlalchemy import create_engine




def database():
    mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306)
    tablecursor=mydb.cursor()
    tablecursor.execute('create database if not exists xpenz ')
    mydb.commit()
    tablecursor.close()
    print('Database created Successfully')
database() 
def tables():
    mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306,database="xpenz")
    usercursor=mydb.cursor()
    usercursor.execute('create table if not exists users(userid INT AUTO_INCREMENT PRIMARY KEY, username varchar(100),password varchar(20),user_password varchar(100),email varchar(100) unique)')
    mydb.commit()
    usercursor.close()
    print('Users Table Created Successfully')

    usercursor=mydb.cursor()
    usercursor.execute('create table if not exists expense (email varchar(100),Month Date,Expense float,FOREIGN KEY (email) REFERENCES users(email))')
    mydb.commit()
    usercursor.close()
    print('income_salary Table Created Successfully')
tables()



def SignUp():
    print("Enter your details to create an account")
    name=input("Enter Your Name : ")
    password=input("Enter your Password : ")
    user_password=name+password
    while True:
            try:
                print('----------------Welcome---------------------\n')
                email=input("Enter your Email Address : ")
                mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306,database="xpenz")
                usercursor=mydb.cursor()
                usercursor.execute('select * from users where email=%s',(email,))
                mail=usercursor.fetchone()

                mydb.commit()
                usercursor.close()
                if mail:               
                    print('email already exists...')
                    break
                valid=validate_email(email)
                if valid:
                    print('Valid Email Address ✔️')
                    mydb=mysql.connector.connect(host="localhost",user="root",password="Ramdevi#2",port=3306,database="xpenz")
                    signup_cursor=mydb.cursor()
                    signup_cursor.execute('insert into users(username,password,user_password,email)values(%s,%s,%s,%s)',(name,password,user_password,email))
                    mydb.commit()
                    signup_cursor.close
                    mydb.close()
                    print('Your Registration Completed Successfully .. :)')
                    user_main()
                   
                    
            except EmailNotValidError as e:
                if not valid:
                   print("Please Enter Valid Email Address..")

                
def LogIn():
    while True:
        name=input("Enter Your name : ")
        password=input("Enter your Password : ")
        user_password=name+password
        mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306,database="xpenz")
        usercursor=mydb.cursor()
        usercursor.execute('select * from users where user_password=%s',(user_password,))
        match=usercursor.fetchone()
        if match:
            print("LOGIN Successfull..")
            user_main()
        else:
            print('LOGIN Failed..')
        mydb.commit()
        usercursor.close() 

def tracking_Analysis():
    print("Month-Expense Analysis")
    mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306,database="xpenz")
    usercursor=mydb.cursor()
    email=(input("Enter Your Email Address :"))
    usercursor.execute('select monthname(Month),Expense from expense where email=%s',(email,))
    result=usercursor.fetchall()
    for i in result:
        print(i)
    
    

    print("---------------------------------------------------------")
    print("---------------------------------------------------------")
    expense_values = []
    min_cursor = mydb.cursor()

    min_cursor.execute("SELECT Expense FROM expense WHERE email = %s", (email,))
    result1 = min_cursor.fetchall()

    for i in result1:
        expense_values.append(i[0])  # Append the expense values

    if expense_values:
        max_value = max(expense_values)

        min_cursor.execute("SELECT MONTHNAME(Month) FROM expense WHERE Expense = %s", (max_value,))
        max_month_name = min_cursor.fetchone()
        
        if max_month_name:
            max_month_name_str = max_month_name[0]

            max_value_str = str(max_value)

            formatted_output = f"Maximum Expense Value: {max_value_str} in Month: {max_month_name_str}"
            print(formatted_output)
        else:
            print("Month name not found for the maximum expense value.")
    else:
        print("No expenses found for the specified email.")


    print("---------------------------------------------------------")

        
    expense_values = []
    min_cursor = mydb.cursor()

    
    min_cursor.execute("SELECT Expense FROM expense WHERE email = %s", (email,))
    result1 = min_cursor.fetchall()

    for i in result1:
        expense_values.append(i[0])  # Append the expense values

    if expense_values:
        min_value = min(expense_values)

        min_cursor.execute("SELECT MONTHNAME(Month) FROM expense WHERE Expense = %s", (min_value,))
        min_month_name = min_cursor.fetchone()
        
        if min_month_name:
            min_month_name_str = min_month_name[0]

            min_value_str = str(min_value)

            formatted_output = f"Minimum Expense Value: {min_value_str} in Month: {min_month_name_str}"
            print(formatted_output)
        else:
            print("Month name not found for the minimum expense value.")
    else:
        print("No expenses found for the specified email.")

    mydb.close()

    print("---------------------------------------------------------")

def tracking_visualization(): 
    email = input("Enter your email: ")
    params = [(email,)]
    query = "SELECT * FROM expense WHERE email=%s"
    engine = create_engine('mysql+mysqlconnector://root:Ramdevi#2@localhost:3306/xpenz')
    df = pd.read_sql_query(query, engine, params=params)
    if not df.empty:
            plt.figure(figsize=(10, 6))
            plt.pie(df["Expense"], labels=df["Month"], autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            plt.title('Expense-Month Tracking')
            plt.show()
    else:
        print("Enter Valid Email Address")
        print('----------------------------------------------------')

        
def Tracking():
    while True:
        choice=input(("Let's Track Your Expense\n 1.Analysis\n 2.Visualization\n 3.Exit\nEnter Your Choice : "))
        if choice=="1":
            tracking_Analysis()
        elif choice=="2":
            tracking_visualization()
        elif choice=='3':
                print('Exiting....')
                break
        else:
            print("Enter Valid Choice...")
            Tracking()  

def prediction():
    try:
        Trained_model = joblib.load('trained-model.pkl')
    except FileNotFoundError:
        print("Trained_model.pkl not found. Make sure the file exists.")
        return
    while True:
        print('**This Prediction Only Based on your Expense of Previous Month')
        print('Enter the Detals to Expense Prediction')
        try:
            email = input('Enter Your Email: ')
            month = input('Enter Date (YYYY-MM-DD): ')
            clothing = float(input("Enter The Expense For Clothing: "))
            Entertainment = float(input('Enter The Expense For Entertainment: '))
            food = float(input("Enter The Expense For Food: "))
            House_hold = float(input("Enter The Expense For Household: "))
            Shopping = float(input("Enter The Expense For Shopping: "))
            Transport = float(input("Enter The Expense For Transport: "))
            Additional = float(input("Enter The Expense Other Than These Categories: "))
        except ValueError:
            print("Invalid input. Please enter valid numeric values for expenses.")
            continue
        total =clothing+Entertainment+House_hold+Shopping+Transport+Additional+food
        mydb=mysql.connector.connect(host="localhost", user="root", password="Ramdevi#2", port=3306,database="xpenz")
        pedictioncursor=mydb.cursor()
        pedictioncursor.execute('insert into expense(email,Month,Expense)values(%s,%s,%s)',(email,month,total))
        mydb.commit()

        #prediction
        input_data=np.array([[clothing,Entertainment,food,House_hold,Shopping,Transport,Additional,total]])
        try:
            predicted_data=Trained_model.predict(input_data)
            print("\n_____________________________________________________\n")
            print(f'Predicted Expense for next Month: {predicted_data[0]}')
            print("\n_____________________________________________________")
            break
        except Exception as e:
             print(e,"Prediction Failed")

               
def user_main():
    while True:
            print("========================Xpenz=============================\n")
            print("Hey...Welcome")
            choice=input("Enter The Operation Do You Want To Perform: \n 1.Expense Prediction \n 2.Expense Tracking\n 3.Exit \nEnter Your Choice : ")
            if choice=='1':
                prediction()
            elif choice=='2':
                Tracking()
            elif choice=='3':
                print('Exiting....')
                break
            else:
              print('Enter Valid Choice..')



def main():
    while True:
            print("========================Xpenz=============================\n")
            print("Hey...Welcome\nprint('Beware of little expenses. A small leak will sink a great ship')")
            choice=input(" 1.Sign Up \n 2.Login\n 3.Exit\nEnter Your Choice:")
            if choice=='1':
                SignUp()
            elif choice=='2':
                LogIn()
            elif choice=='3':
                print('Exiting...')
                break
            else:
                print('Enter Valid Choice..')

main()