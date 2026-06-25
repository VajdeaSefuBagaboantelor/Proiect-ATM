import os
import sqlite3

print("---Welcome to the Python ATM---")

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'atm.db')


if not os.path.exists(db_path):
    print("Database not found")
    exit()


conn = sqlite3.connect(db_path)
c = conn.cursor()

Card_Number = input("Please enter your card number: ")

if len(Card_Number) != 16 or not Card_Number.isdigit():
    print("Invalid card number format")
    exit()

c.execute("SELECT card_number, pin, balance FROM accounts WHERE card_number=?", (Card_Number,))
user = c.fetchone()

if user:
    db_card, PIN, Balance = user
    PIN = str(PIN)
    Balance = float(Balance) 
else:
    print("Card number not found")
    conn.close()
    exit()

PIN_input = input("Please enter your PIN: ")
if PIN_input != PIN:
    print("Incorrect PIN")
    conn.close()
    exit()

print("\nPlease select an option:")
print("1. Check balance")
print("2. Withdraw")
print("3. Deposit")
print("4. Change PIN")
print("5. Transfer")
print("6. Transaction history")

option = input("Enter option number: ")

if option == "1":
    print("Your balance is: " + str(Balance) + " RON")

elif option == "2":
    amount_str = input("Enter amount to withdraw: ")


    try:
        amount = float(amount_str)
    except ValueError:
        print("Please enter a valid number")
        conn.close()
        exit()

    if amount <= 0:
        print("Amount must be positive")
    elif amount > Balance:
        print("Insufficient funds")
    else:
        Balance -= amount
        print("You have withdrawn: " + str(amount) + " RON")
        print("New balance: " + str(Balance) + " RON")

        c.execute("UPDATE accounts SET balance=? WHERE card_number=?", (Balance, Card_Number))
        conn.commit()

elif option == "3":
    amount_str = input("Enter amount to deposit: ")

    try:
        amount = float(amount_str)
    except ValueError:
        print("Please enter a valid number")
        conn.close()
        exit()

    if amount <= 0:
        print("Amount must be positive")
    else:
        Balance += amount
        print("You have deposited: " + str(amount) + " RON")
        print("New balance: " + str(Balance) + " RON")

        c.execute("UPDATE accounts SET balance=? WHERE card_number=?", (Balance, Card_Number))
        conn.commit()

elif option == "4":
    New_PIN = input("Enter new 4-digit PIN: ")
    if len(New_PIN) == 4 and New_PIN.isdigit():
        PIN = New_PIN

        c.execute("UPDATE accounts SET pin=? WHERE card_number=?", (PIN, Card_Number))
        conn.commit()

        print("PIN changed successfully")
    else:
        print("Invalid PIN format. Must be exactly 4 digits.")

elif option == "5":
    target_card = input("Enter the destination card number (16 digits): ")

    if len(target_card) != 16 or not target_card.isdigit():
        print("Invalid destination card number")
    elif target_card == Card_Number:
        print("You cannot transfer to your own card")
    else:
        c.execute("SELECT card_number, balance FROM accounts WHERE card_number=?", (target_card,))
        target_user = c.fetchone()

        if not target_user:
            print("Destination card not found")
        else:
            amount_str = input("Enter amount to transfer: ")
            try:
                amount = float(amount_str)
            except ValueError:
                print("Please enter a valid number")
                conn.close()
                exit()

            if amount <= 0:
                print("Amount must be positive")
            elif amount > Balance:
                print("Insufficient funds")
            else:
                target_balance = float(target_user[1])

                Balance -= amount
                c.execute("UPDATE accounts SET balance=? WHERE card_number=?", (Balance, Card_Number))

                # Add to receiver
                target_balance += amount
                c.execute("UPDATE accounts SET balance=? WHERE card_number=?", (target_balance, target_card))

                conn.commit()
                print("Transfer successful!")
                print("Your new balance: " + str(Balance) + " RON")

elif option == "6":
    print("Transaction history is not available yet.")
    print("Current balance: " + str(Balance) + " RON")

else:
    print("Invalid option. Please choose a number between 1 and 6.")

conn.close()
print("\nThank you for using the Python ATM. Goodbye!")