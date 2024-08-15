import csv
from PIL import ImageTk, Image
import os
from datetime import datetime
import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText 
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, simpledialog


# Initiated a class-level variable for verification codes storing
verification_codes = {}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Login Page")
        self.root.geometry("600x500")  # window size
        self.root.resizable(False, False)  #  window resizing Disabled

        # background image
        self.background_img = Image.open("background1.jpg")
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_label = tk.Label(root, image=self.background_img)
        self.background_label.place(x=-0.1, y=-0.5, relwidth=1, relheight=1)  # Fit image to window

        # Title 
        self.title_label = tk.Label(root, text="My Advanced SE Bank", font=("Helvetica", 34), fg="darkblue")
        self.title_label.pack(pady=25)

        # Username label and entry
        self.username_label = tk.Label(root, text="Username:", fg="darkblue")
        self.username_label.place(relx=0.15, rely=0.3)
        self.username_entry = tk.Entry(root)
        self.username_entry.place(relx=0.35, rely=0.3)

        # Password label and entry
        self.password_label = tk.Label(root, text="Password:", fg="darkblue")
        self.password_label.place(relx=0.15, rely=0.4)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.place(relx=0.35, rely=0.4)

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.verify_credentials, fg="darkblue")
        self.login_button.place(relx=0.5, rely=0.55, anchor="center")

        # Sign up button
        self.signup_button = tk.Button(root, text="Click here to Sign Up", command=self.create_account_page, fg="darkblue")
        self.signup_button.place(relx=0.5, rely=0.65, anchor="center")

    def verify_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open('credentials.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username and row[1] == password:
                    # Perform 2FA
                    if self.perform_2fa(username):
                        messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
                        self.open_account_page()
                    
                        return
                    else:
                        messagebox.showerror("Login Failed", "Invalid verification code")
                        return
        messagebox.showerror("Login Failed", "Invalid username or password")

    def perform_2fa(self, username):
        # Get the entered verification code
        entered_code = simpledialog.askstring("Two-Factor Authentication", "Enter the 6-digit verification code:")

        # Check if the entered code matches the fixed code
        return entered_code == "090078"

    def send_verification_email(self, username, verification_code):
        # Email configuration
        sender_email = "your_email@example.com"
        receiver_email = "user_email@example.com"
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_username = "your_smtp_username"
        smtp_password = "your_smtp_password"

        # Email content
        subject = "Verification Code for Two-Factor Authentication"
        body = f"Your verification code is: {verification_code}"

        # Construct the email message
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            return True
        except Exception as e:
            print("Error sending email:", e)
            return False


    def save_transaction(self, username, transaction_type, amount):
        transaction_file = f"transactions/{username}_transactions.csv"
        if not os.path.exists("transactions"):
            os.makedirs("transactions")
        with open(transaction_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), transaction_type, amount])

    def open_account_page(self):
        account_window = tk.Toplevel(self.root)
        account_window.title("User Account")
        account_window.geometry("600x400")
        account_window.resizable(False, False)
        # Load background image
        self.background_img = Image.open("background1.jpg")
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_label = tk.Label(account_window, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fit image to window

        # Check balance button
        check_balance_button = tk.Button(account_window, text="Check Balance", command=self.check_balance)
        check_balance_button.pack(pady=10)

        # Withdraw button
        withdraw_button = tk.Button(account_window, text="Withdraw", command=self.withdraw)
        withdraw_button.pack(pady=10)

        # Deposit button
        deposit_button = tk.Button(account_window, text="Deposit", command=self.deposit)
        deposit_button.pack(pady=10)

        # Transfer button
        transfer_button = tk.Button(account_window, text="Transfer Funds", command=self.transfer_funds)
        transfer_button.pack(pady=10)

        # Transaction history button
        transaction_history_button = tk.Button(account_window, text="Transaction History", command=self.transaction_history)
        transaction_history_button.pack(pady=10)

        # Additional services buttons
        manage_services_button = tk.Button(account_window, text="Manage Services", command=self.manage_services)
        manage_services_button.pack(pady=10)

        recurring_payments_button = tk.Button(account_window, text="Recurring Payments", command=self.recurring_payments)
        recurring_payments_button.pack(pady=10)

    def check_balance(self):
        username = self.username_entry.get()
        with open('balance.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('UserName') == username:
                    messagebox.showinfo("Balance", f"Your current balance is: {row.get('Balance')}")
                    return
        messagebox.showerror("Error", "Balance information not found.")

    def withdraw(self):
        username = self.username_entry.get()
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None and amount > 0:
            with open('balance.csv', 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            with open('balance.csv', 'w', newline='') as file:
                fieldnames = ['UserName', 'Balance']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    if row['UserName'] == username:
                        balance = float(row['Balance'].replace('$', ''))
                        if balance >= amount:
                            balance -= amount
                            row['Balance'] = f"${balance:.2f}"
                            messagebox.showinfo("Withdraw", f"Withdrawal successful. Current balance: ${balance:.2f}")
                        else:
                            messagebox.showerror("Withdraw", "Insufficient balance.")
                    writer.writerow(row)
            self.save_transaction(username, "Withdraw", amount)

    def deposit(self):
        username = self.username_entry.get()
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None and amount > 0:
            with open('balance.csv', 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            with open('balance.csv', 'w', newline='') as file:
                fieldnames = ['UserName', 'Balance']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    if row['UserName'] == username:
                        balance = float(row['Balance'].replace('$', ''))
                        balance += amount
                        row['Balance'] = f"${balance:.2f}"
                        messagebox.showinfo("Deposit", f"Deposit successful. Current balance: ${balance:.2f}")
                    writer.writerow(row)
            self.save_transaction(username, "Deposit", amount)

    def transfer_funds(self):
        username = self.username_entry.get()
        recipient_username = simpledialog.askstring("Transfer Funds", "Enter recipient's username:")
        if not recipient_username:
            return
        amount = simpledialog.askfloat("Transfer Funds", "Enter the amount to transfer:")
        if not amount:
            return
        rows = []
        with open('balance.csv', 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        for row in rows:
            if row.get('UserName') == username:
                current_balance = float(row.get('Balance').replace('$', '').replace(',', ''))
                if current_balance >= amount:
                    row['Balance'] = f"${current_balance - amount}"
                    for recipient_row in rows:
                        if recipient_row.get('UserName') == recipient_username:
                            recipient_balance = float(recipient_row.get('Balance').replace('$', '').replace(',', ''))
                            recipient_row['Balance'] = f"${recipient_balance + amount}"
                            with open('balance.csv', 'w', newline='') as file:
                                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                                writer.writeheader()
                                writer.writerows(rows)
                            messagebox.showinfo("Transfer Successful", f"You have transferred ${amount} to {recipient_username}.")
                            return
                    else:
                        messagebox.showerror("Transfer Failed", "Recipient's account not found.")
                        return
                else:
                    messagebox.showerror("Transfer Failed", "Insufficient balance.")
                    return
        else:
            messagebox.showerror("Transfer Failed", "Your account balance information not found.")
        self.save_transaction(username, "Transfer (Out)", amount)
        self.save_transaction(recipient_username, "Transfer (In)", amount)

    def transaction_history(self):
        username = self.username_entry.get()
        transaction_history_file = f"transactions/{username}_transactions.csv"
        if not os.path.exists(transaction_history_file):
            messagebox.showerror("Error", "Transaction history not found.")
            return
        with open(transaction_history_file, 'r') as file:
            content = file.read()
        messagebox.showinfo("Transaction History", content)

    def manage_services(self):
        # Implement service management functionality here
        service_window = tk.Toplevel(self.root)
        service_window.title("Manage Services")
        service_window.geometry("600x400")
        self.root.resizable(False, False)  # Disable window resizing

        # Load background image
        self.background_img = Image.open("background1.jpg")
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_label = tk.Label(service_window, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Checkbook request button
        checkbook_button = tk.Button(service_window, text="Request Checkbook", command=self.request_checkbook)
        checkbook_button.pack(pady=10)

        # Debit/Credit card request button
        card_button = tk.Button(service_window, text="Request Debit/Credit Card", command=self.request_card)
        card_button.pack(pady=10)

    def request_checkbook(self):
        # Implement functionality to request a checkbook
        username = self.username_entry.get()
        # Code to request a checkbook goes here
        messagebox.showinfo("Checkbook Request", "Your checkbook request has been submitted.")

    def request_card(self):
        # Implement functionality to request a debit/credit card
        username = self.username_entry.get()
        # Code to request a card goes here
        messagebox.showinfo("Card Request", "Your card request has been submitted.")

    def recurring_payments(self):
        # Implement recurring payments functionality here
        recurring_window = tk.Toplevel(self.root)
        recurring_window.title("Recurring Payments")
        recurring_window.geometry("600x400")
        recurring_window.resizable(False, False)
        
        # Load background image
        self.background_img = Image.open("background1.jpg")
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_label = tk.Label(recurring_window, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Set up recurring payment button
        setup_button = tk.Button(recurring_window, text="Set Up Recurring Payment", command=self.setup_recurring_payment)
        setup_button.pack(pady=10)

        # Manage recurring payments button
        manage_button = tk.Button(recurring_window, text="Manage Recurring Payments", command=self.manage_recurring_payments)
        manage_button.pack(pady=10)

    def setup_recurring_payment(self):
        # Get the current username
        username = self.username_entry.get()

        # Prompt the user to enter recurring payment details
        recipient = simpledialog.askstring("Recurring Payment", "Enter recipient's username:")
        if not recipient:
            return

        amount = simpledialog.askfloat("Recurring Payment", "Enter the amount for the recurring payment:")
        if amount is None:
            return

        frequency = simpledialog.askinteger("Recurring Payment", "Enter the frequency of the payment (in days):")
        if frequency is None:
            return

        # Define the path for the user's recurring payments CSV file
        recurring_payments_file = f"recurring_payments/{username}_recurring_payments.csv"

        # Check if the recurring payments file exists, create if not
        if not os.path.exists("recurring_payments"):
            os.makedirs("recurring_payments")

        # Write recurring payment details to CSV
        with open(recurring_payments_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([recipient, amount, frequency])

        messagebox.showinfo("Recurring Payment", "Recurring payment has been set up.")

    def manage_recurring_payments(self):
        # Get the current username
        username = self.username_entry.get()

        # Define the path for the user's recurring payments CSV file
        recurring_payments_file = f"recurring_payments/{username}_recurring_payments.csv"

        # Check if the recurring payments file exists
        if not os.path.exists(recurring_payments_file):
            messagebox.showerror("Error", "Recurring payments not found.")
            return

        # Open the recurring payments file and display its content
        with open(recurring_payments_file, 'r') as file:
            content = file.read()

        messagebox.showinfo("Manage Recurring Payments", content)


    def create_account_page(self):
        # Create a new window for account creation
        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Create Account")
        create_account_window.geometry("600x400")  # Match login window size
        create_account_window.resizable(False, False)  # Disable window resizing
        # Load background image
        self.background_img = Image.open("background1.jpg")
        self.background_img = ImageTk.PhotoImage(self.background_img)
        self.background_label = tk.Label(create_account_window, image=self.background_img)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fit image to window
        # Username label and entry
        username_label = tk.Label(create_account_window, text="Username:")
        username_label.place(relx=0.25, rely=0.25)
        self.username_entry = tk.Entry(create_account_window)
        self.username_entry.place(relx=0.4, rely=0.25)
        # Password label and entry
        password_label = tk.Label(create_account_window, text="Password:")
        password_label.place(relx=0.25, rely=0.35)
        self.password_entry = tk.Entry(create_account_window, show="*")
        self.password_entry.place(relx=0.4, rely=0.35)
        # Account type radio buttons
        account_type_label = tk.Label(create_account_window, text="Account Type:")
        account_type_label.place(relx=0.25, rely=0.45)
        self.account_type = tk.StringVar()
        personal_radio = tk.Radiobutton(create_account_window, text="Personal", variable=self.account_type, value="Personal")
        personal_radio.place(relx=0.44, rely=0.45)
        business_radio = tk.Radiobutton(create_account_window, text="Business", variable=self.account_type, value="Business")
        business_radio.place(relx=0.62, rely=0.45)
        # Create account button
        create_button = tk.Button(create_account_window, text="Create Account", command=self.create_account)
        create_button.place(relx=0.37, rely=0.6)

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        account_type = self.account_type.get()
        if not username or not password or not account_type:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return
        with open('credentials.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password])
        with open('userdetails.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password, account_type])
        messagebox.showinfo("Account Created", "Your account has been created successfully!")

# Create Tkinter window
root = tk.Tk()
login_window = LoginWindow(root)
root.mainloop()
