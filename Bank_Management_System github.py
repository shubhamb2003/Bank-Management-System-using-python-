import mysql.connector

connect=mysql.connector.connect(host='localhost',username='root',password='root',database='authsystem')

cur=connect.cursor()

def New_account():
    name=input("Enter a Account Holder Name: ")
    contact=int(input("Enter a  Contact Number:"))
    email=input("Enter a Email ID:").lower()
    Pan_card=input("Enter a Pan Card Number:").upper()
    Aadhar_card=int(input("Enter a 12 Digit Aadhar Card Number:"))
    Account_type=input("Enter a Account Type [S/C]:").upper()
    balance=float(input("Enter a Initial Balance:"))
    address=input("Enter a Address:")
    pin=int(input("Enter a Pin:"))

    query='''insert into accounts(Account_holder_name,Contact_no,Email,Pan_card_number,
    Aadhar_card_number,Account_type,Balance,Address,pin)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    value=(name,contact,email,Pan_card,Aadhar_card,Account_type,balance,address,pin)
    cur.execute(query,value)
    print(f"Welcome {name}! Your New Account Has Been Created.")
    connect.commit()

    main()

def Deposite_amount():
    entered_pin = int(input("Enter your PIN: "))
    cur.execute("select Pin from accounts where Pin = %s",(entered_pin,))
    r = cur.fetchone()
    if r:
        value=(entered_pin,)
        Deposite=int(input("Enter Your Deposite  Amount:"))
        if Deposite >=0:
            cur.execute("select Pin,Balance from  accounts where Pin=%s ",value)
        else:
            print("Deposite Amount is Invalid")

        result=cur.fetchone()
        if result:
            total=result[1]+Deposite
            print(f"Deposite Amount is {Deposite},Your Balance is {total}")

            cur.execute(f"update accounts set Balance={total} where pin={entered_pin} ")
            connect.commit()
        else:
            print("Pin not Match ")
    main()

def Withdarw_amount():
    entered_pin = int(input("Enter your PIN: "))

    cur.execute("select pin, Balance, Account_type from accounts where pin = %s", (entered_pin,))
    r = cur.fetchone()
    if r:
        Account_type = r[2] 
        if Account_type == 'S':
            min_balance = 500
        else:
            min_balance = 1500
        withdraw = int(input("Enter Your Withdraw Amount: "))
    
        if r[1] > withdraw and r[1] - withdraw >= min_balance:
            total = r[1] - withdraw
            print(f"Withdrawal Amount: {withdraw}, Your New Balance: {total}")
        
            cur.execute("update accounts set Balance = %s where Pin = %s", (total, entered_pin))
            connect.commit()
        else:
            print(f"Insufficient funds or balance cannot down below the minimum required {min_balance} for a {Account_type} account.")
    else:
        print("Pin Not Match")
    main()

def Balance_enquiry():
    entered_pin = int(input("Enter your PIN: "))
    value=(entered_pin,)
    cur.execute("select Pin,Balance from  atm where Pin=%s ",value)
    result=cur.fetchone()
    if result:
        print(f"Your Balance is :{result[1]}")
    else:
        print("Pin Do Not Exist")
    main()

def All_account_holder_list():
    cur.execute("select Account_holder_name, Contact_no, Email, Account_type, Balance from accounts")
    result = cur.fetchall()
    
    if result:
        print("\nAll Account Holder List:")
        print("---------------------------------------------------")
        print(''' Name |   Contact |   Email  |  Account Type  |  Balance ''')
        print("---------------------------------------------------")
        for row in result:
            print(f"{row[0]}   {row[1]}   {row[2]}      {row[3]}         {row[4]}")
        print("---------------------------------------------------")
    else:
        print("No accounts found.")
    main()

def Close_an_account():
    account_number=int(input("Enter a account number to closed the account: "))
    cur.execute("Select Account_number from accounts where Account_number=%s",(account_number,))
    r=cur.fetchone()
    if r:
        confirmation=input(f"Are you sure you want to close the account {account_number}? (y/n): ").lower()
        if  confirmation=='y':
            cur.execute(f"delete from accounts where Account_number = '{account_number}'")
            connect.commit()
            print(f"Account number of {account_number} hass beeen closed")
        else:
            print("Account closure canceled.")
    else:
        print("Account Number is not Exist!. Please Check the Account Number")

    
    main()

def Modify_an_account():
    account_number = int(input("Enter the Account Number to modify: "))

    cur.execute(f"select * from accounts where account_number = '{account_number}'")
    account = cur.fetchone()

    if account:
            print("Account found. Current details:")
            print(f"Account Number: {account[0]}")
            print(f"Account Holder Name: {account[1]}")
            print(f"Contact No: {account[2]}")
            print(f"Email: {account[3]}")
            print(f"Account Type: {account[6]}")
            print(f"Address: {account[8]}")
            print(f"Pin: {account[9]}")
            
            choice = input("What do you want to modify? (name/email/contact/type/pin): ").lower()

            if choice == 'name':
                new_name = input("Enter the new Account Holder Name: ")
                cur.execute(f"update accounts set Account_holder_name = '{new_name}' where account_number = '{account_number}'")
                connect.commit()
                print("Account holder name updated successfully.")

            elif choice == 'email':
                new_email = input("Enter the new Email ID: ")
                cur.execute(f"update accounts set Email = '{new_email}' where account_number = '{account_number}'")
                connect.commit()
                print("Email ID updated successfully.")

            elif choice == 'contact':
                new_contact = int(input("Enter the new Contact Number: "))
                cur.execute(f"update accounts set Contact_no = {new_contact} where account_number = '{account_number}'")
                connect.commit()
                print("Contact number updated successfully.")

            elif choice == 'type':
                new_type = input("Enter the new Account Type [S/C]: ").upper()
                cur.execute(f"update accounts set Account_type = '{new_type}' where account_number = '{account_number}'")
                connect.commit()
                print("Account type updated successfully.")

            elif choice == 'pin':
                new_pin = int(input("Enter the new Pin: "))
                cur.execute(f"update accounts set pin = {new_pin} where account_number = '{account_number}'")
                connect.commit()
                print("Pin updated successfully.")

            else:
                print("Invalid option. No changes made.")

    else:
            print(f"No account found with ID {account_number}.")

    main()

def main():
    while True:
        choice = int(input('''   
            BANK MANAGEMENT SYSTEM
                                                    
        MAIN MENU
        1. NEW ACCOUNT
        2. DEPOSIT AMOUNT
        3. WITHDRAW AMOUNT
        4. BALANCE ENQUIRY
        5. ALL ACCOUNT HOLDER LIST
        6. CLOSE AN ACCOUNT
        7. MODIFY AN ACCOUNT
        8. EXIT  
        Enter your choice: '''))

        if choice == 1:
            New_account()

        elif choice == 2:
            Deposite_amount()

        elif choice == 3:
            Withdarw_amount()

        elif choice == 4:
            Balance_enquiry()

        elif choice == 5:
            All_account_holder_list()

        elif choice == 6:
            Close_an_account()

        elif choice == 7:
            Modify_an_account()

        elif choice == 8:
            print("Exiting")
            break  # Exit the loop and the program

        else:
            print("Invalid choice")
main() 