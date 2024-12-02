import datetime

def readAccounts():
    # Retruns list of lists of accounts in bank -> [[account1], [account2], [account3], ....]
    new_list1 = []
    accountsFile = open('accounts.csv','r')
    for line in accountsFile.readlines():
        accountsData = line[:-1].split(',')
        new_list1.append(accountsData)
    accountsFile.close()
    return new_list1

def readTrans():
    # Retruns list of lists of transaction -> [[trans1], [trans2], [trans3], ....]
    new_list2 = []
    transFile = open('transaction.csv','r')
    for line in transFile.readlines():
        transData = line[:-1].split(',')
        new_list2.append(transData)
    transFile.close()
    return new_list2

def init():
    readAcc = readAccounts()
    readTra = readTrans()
    return readAcc + readTra

def save_accounts(list):
    # Updates the list of accounts by overwriting it
    saveAccounts = open('accounts.csv', 'w')
    # Iterates through the list of list of account
    # Sublist holds each elemnt in list -> list -> [[account1], [account2], [account3], ....]
    # Sublist -> [account1], [account2], [account3], ....
    for sublist in list:
        # Gets the first element of an account, the account number -> [1111, Balacne, Name]
        # str cast, Turns to a string in order to split with join function later on
        sublist[0] = str(sublist[0])
        # Gets the seccond element of an account, the balance -> [Account number, 1555.0, Name]
        # str cast, Turns to a string in order to split with join function later on
        sublist[1] = str(sublist[1])
        # Writes in the file and splits with comma each elemnt in the list
        saveAccounts.write(','.join(sublist) +'\n')
    saveAccounts.close()

def save_transactions(list):
    save_trans = open('transaction.csv', 'w')
    # Iterates through the list of list of transactions
    # trans holds each elemnt in list -> list -> [[trans1], [trans2], [trans3], ....]
    # trans -> [trans1], [trans2], [trans3], ....
    for trans in list:
        # Writes in the file and splits with comma each elemnt in the list
        save_trans.write(','.join(trans) + '\n')
    save_trans.close()

def save(accounts, transactions):
        save_accounts(accounts)
        save_transactions(transactions)

def menu():
    print("1) Create a new account")
    print("2) Deposit to the account")
    print("3) Withdraw from the account")
    print("4) Balance inquiry")
    print("5) Account transaction report")
    print("6) Exit")
    choice = input("Enter your choice: ")

    # While input is not 6, not exit
    while choice != 6:
        try:
            choice = int(choice)
            if not(choice >= 1 and choice <= 6):
                choice = input("Enter your choice: ")
            else:
                return choice
        except ValueError:
            choice = input("Enter your choice: ")

def account_add():
    account_number = input("Enter the account number: ")
    owner_name = input("Enter the owner's name: ")

    accounts_list = readAccounts()
    # Iterates through the list of list of account
    for index in range(0, len(accounts_list)):
        # Gets the first element of an account, the account number -> [1111, Balacne, Name]
        # If found account, exit function because account already exists
        if accounts_list[index][0] == account_number:
            print("Error: Account with number",account_number,"already exists.")
            return
    # If didnt exited the function so far add account with balance 0 and inputs taken erlier via save_accounts function
    accounts_list.append([account_number, '0', owner_name])
    print("Account added successfully")
    save_accounts(accounts_list)

def deposit():
    account_number = input("Enter the account number: ")
    deposit_amount = int(input("Enter the deposit amount: "))
    found = 0

    # If deposit is negative print error and exit, deposit cannot be negative
    if deposit_amount < 0:
        print("Error: Deposit amount must be a positive.")
        return

    #account_list holds list of lists of account -> [[account1], [account2], [account3], ....]
    accounts_list = readAccounts()
    # Iterares through range of 0 until length of accounts_list, index needed later on
    for index in range(0, len(accounts_list)):
        # accounts_list[index] -> gets the index, from 0 - len(accounts_list)
        # Each index holds a single list from accounts_list
        # [0] -> takes the first element, in the inner list which is the account number
        if accounts_list[index][0] == account_number:
            # accounts_list[index] -> gets the index, from 0 - len(accounts_list)
            # Each index holds a single list from accounts_list
            # [1] -> takes the second element, in the inner list which is the balance
            # turn it to a float to add ammount
            accounts_list[index][1] = float(accounts_list[index][1])
            # Adds ammount to the balance
            accounts_list[index][1] += deposit_amount
            # Updates list with save_accounts
            save_accounts(accounts_list)
            found = 1
    # Error if account not found
    else:
           if found == 0:
            print("Error: Account with number", account_number, "was not found.")
            return
    #trans_list holds list of lists of transactions -> [[trans1], [trans2], [trans3], ....]
    trans_list = readTrans()
    # Append a list to trans_list
    trans_list.append([str(account_number), str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")), str(deposit_amount)])
    # Updates list with save_accounts
    save_transactions(trans_list)
    print(f"Deposit of {deposit_amount} made successfully to account {account_number}.")

def withdraw():
    account_number = input("Enter the account number: ")
    withdraw_amount = int(input("Enter the withdraw amount: "))
    found = 0

    # If withdrawl is positive print error and exit, withdrawl cannot be positive
    if withdraw_amount > 0:
        print("Error: Withdraw amount must be a negative.")
        return

    #account_list holds list of lists of account -> [[account1], [account2], [account3], ....]
    accounts_list = readAccounts()
    # Iterares through range of 0 until length of accounts_list, index needed later on
    for index in range(0, len(accounts_list)):
        # accounts_list[index] -> gets the index, from 0 - len(accounts_list)
        # Each index holds a single list from accounts_list
        # [0] -> takes the first element, in the inner list which is the account number
        if accounts_list[index][0] == account_number:
            # Gets the balance from each element in accounts_list
            accounts_list[index][1] = float(accounts_list[index][1])
            # If the withdrawl is smaller then the balance in account add withdrawl and update with save_accounts
            if (accounts_list[index][1] + withdraw_amount) >= 0:
                accounts_list[index][1] += withdraw_amount
                save_accounts(accounts_list)
                found = 1
                print("Withdraw successful.")
            # If the withdrawl is bigger then the balance in account print error and exit function
            else:
                print("Withdrawal not allowed, might go into negative balance")
                return
    else:
        if found == 0:
            print("Error: Account with number", account_number, "was not found.")
            return
       #print("Withdrawal !")
    #trans_list holds list of lists of transactions -> [[trans1], [trans2], [trans3], ....]
        trans_list = readTrans()
    # Append a list to trans_list
        trans_list.append([str(account_number), str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")), str(withdraw_amount)])
    # Updates list with save_accounts
        save_transactions(trans_list)

def balance():
    account_number = input("Enter the account number: ")
    #account_list holds list of lists of account -> [[account1], [account2], [account3], ....]
    account_list = readAccounts()
    # Iterares through range of 0 until length of accounts_list, index needed later on
    for index in range(0, len(account_list)):
        # accounts_list[index] -> gets the index, from 0 - len(accounts_list)
        # Each index holds a single list from accounts_list
        # [0] -> takes the first element, in the inner list which is the account number
        if account_list[index][0] == account_number:
            # Prints balance
            print("The ballance of account number " + account_number + " is " + account_list[index][1])
            return
    print("Error: Account not found")

def report():
    found = 0
    list_of_trans = []
    account_number = input("Enter the account number: ")
    #account_list holds list of lists of account -> [[account1], [account2], [account3], ....]
    account_list = readAccounts()
    #trans_list holds list of lists of transactions -> [[trans1], [trans2], [trans3], ....]
    trans_list = readTrans()
    # Iterares through range of 0 until length of accounts_list, index needed later on
    for index in range(0, len(account_list)):
        # accounts_list[index] -> gets the index, from 0 - len(accounts_list)
        # Each index holds a single list from accounts_list
        # [0] -> takes the first element, in the inner list which is the account number
        if account_list[index][0] == account_number:
            #Acount number found flag
            found = 1
            # Iterares through range of 0 until length of trans_list, index needed later on
            for j in range(0, len(trans_list)):
                # if the account number equal to account number in trans_list
                if trans_list[j][0] == account_number:
                    found = 1
                    # Add element from trans_list to new list
                    list_of_trans.append(trans_list[j])

    # print header
    print('Account, Date&Time, Transaction ammount')
    # print each elemnt in list_of_trans
    for trans in list_of_trans:
        print(','.join(trans))
    else:
        if found == 0:
            print("Error: Account with number", account_number, "was not found.")

def main():
    init()
    choice = 0
    while choice != 6:
        choice = menu()
        if choice == 1:
            account_add()
        elif choice == 2:
            deposit()
        elif choice == 3:
            withdraw()
        elif choice == 4:
            balance()
        elif choice == 5:
            report()
        elif choice == 6:
            print("Exiting menu.")
        else:
            print("Invalid option. Please enter a num between 1-6.")
main()
