import tkinter as tk
import uuid
import sqlite3
from tkinter import messagebox
from userAuthentication import AuthenticationPage
from userResetPassword import ResetPasswordPage
from helper import helper
from chooseVehicle import ChooseVehicle
from operator_profile import operator
from Manager import Manager

hlp = helper()
windowWidth = 380
windowHeight = 580
jumpPageWidth = 380
jumpPageHeight = 500
popUpWidth = 250
popUpHeight = 100
formBackgroundColour = "#35608f"
headerBackgroundColour = "#000000"

sqlite3.register_adapter(uuid.UUID, lambda x: x.bytes)
sqlite3.register_converter("UUID", lambda x: uuid.UUID(bytes=x))

class loginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.mainFrame = tk.Frame(self.root, width=windowWidth, height=windowHeight)
        self.userList = []
        self.createLoginPage()

    def createLoginPage(self):
        # Header
        self.headerFrame = tk.Frame(self.mainFrame, bg=headerBackgroundColour, width=windowWidth, height=50)
        self.titleFrame = tk.Frame(self.headerFrame, padx=1, pady=1)
        self.labelTitle = tk.Label(self.titleFrame, text="Login", font=('verdana', 20), width=7, fg='#fff', padx=20, pady=5, bg='red')

        self.headerFrame.pack()
        self.titleFrame.pack()
        self.labelTitle.pack()

        self.titleFrame.place(y=26, relx=0.5, anchor=tk.CENTER)

        # Login Form
        self.loginFrame = tk.Frame(self.mainFrame, width=windowWidth, height=windowHeight)
        self.loginFormFrame = tk.Frame(self.loginFrame, padx=30, pady=150, bg=formBackgroundColour)

        self.loginLabelUserName = tk.Label(self.loginFormFrame, text=" email/ phone: ", font=('verdana', 12), bg=formBackgroundColour)
        self.loginEntryUserName = tk.Entry(self.loginFormFrame, font=('verdana', 12))
        self.loginLabelPassword = tk.Label(self.loginFormFrame, text=" Password: ", font=('verdana', 12), bg=formBackgroundColour)
        self.loginEntryPassword = tk.Entry(self.loginFormFrame, font=('verdana', 12), show='*')

        self.buttonFrame = tk.Frame(self.loginFormFrame, bg=formBackgroundColour)
        self.loginButton = tk.Button(self.buttonFrame, text=" Login ", font=('verdana', 12), highlightbackground=formBackgroundColour, command=self.login)
        self.resetPasswordButton = tk.Button(self.buttonFrame, text=" Reset Pwd ", font=('verdana', 12), highlightbackground=formBackgroundColour, command=self.goToResetPasswordPage)

        self.toRegisterLabel = tk.Label(self.loginFormFrame, text=">> forget your password? click here <<", font=('Verdana', 12), bg=formBackgroundColour, fg='red')

        self.mainFrame.pack(fill=tk.BOTH, expand=1)
        self.loginFrame.pack(fill=tk.BOTH, expand=1)
        self.loginFormFrame.pack(fill=tk.BOTH, expand=1)
        self.mainFrame.pack_propagate(False)

        self.loginEntryUserName.focus_set()

        self.loginLabelUserName.grid(row=0, column=0, sticky='e')
        self.loginEntryUserName.grid(row=0, column=1, pady=10)
        self.loginLabelPassword.grid(row=1, column=0, sticky='e')
        self.loginEntryPassword.grid(row=1, column=1, pady=10)

        self.buttonFrame.grid(row=2, column=0, columnspan=2)
        self.loginButton.grid(row=0, column=0, pady=5, padx=10)
        self.resetPasswordButton.grid(row=0, column=1, pady=5, padx=10)

        self.toRegisterLabel.grid(row=3, column=0, columnspan=2, pady=5)

        self.toRegisterLabel.bind("<Button-1>", lambda event: self.goToAuthenticationPage())

    def login(self):
        try:
            conn = sqlite3.connect('nextbike.db')
            cursor = conn.cursor()
        except sqlite3.Error as err:
            self.displayErrorMessage("Error while connecting to SQLite")
            print("Error while connecting to SQLite", err)

        userNameOrPhoneNumber = self.loginEntryUserName.get()
        password = self.loginEntryPassword.get()

        if userNameOrPhoneNumber.isdigit():
            query = "SELECT user_id, phone_number, password, role_type FROM user_details where phone_number = ?"
        else:
            query = "SELECT user_id, email_address, password, role_type FROM user_details where email_address = ?"

        cursor.execute(query, (userNameOrPhoneNumber,))
        self.userDetails = cursor.fetchone()

        if self.userDetails:
            decrypted_password = hlp.decrypt_password(self.userDetails[2])
            if password == decrypted_password:
                print("User is logged in")
                messagebox.showinfo("Logged", "User is logged in. The next page will be a login page.")
                self.userList.append(self.userDetails[0])
                print(self.userDetails)
                if self.userDetails[3] == 'Customer':
                    print(self.userDetails[3])
                    self.root.withdraw()
                    chooseVehiclePage = tk.Toplevel(self.root)
                    cv = ChooseVehicle(chooseVehiclePage, self.userDetails[0])
                    cv.run()
                elif self.userDetails[3] == 'Operator':
                    self.root.withdraw()
                    operatorProfilePage = tk.Toplevel(self.root)
                    operatorProfilePage = operator(operatorProfilePage)
                elif self.userDetails[3] == 'Manager':
                    self.root.withdraw()
                    managerPage = tk.Toplevel(self.root)
                    managerPage = Manager(managerPage)
                    managerPage.run()
            else:
                messagebox.showinfo("Logged", "Incorrect Password")
        else:
            messagebox.showinfo("Logged", "Incorrect email address/Phone number and password")

    def goToResetPasswordPage(self):
        try:
            conn = sqlite3.connect('nextbike.db')
            cursor = conn.cursor()
        except sqlite3.Error as err:
            self.displayErrorMessage("Error while connecting to SQLite")
            print("Error while connecting to SQLite", err)

        userNameOrPhoneNumber = self.loginEntryUserName.get()
        password = self.loginEntryPassword.get()
        if userNameOrPhoneNumber.isdigit():
            query = "SELECT * FROM user_details WHERE phone_number = ? AND password = ?;"
        else:
            query = "SELECT * FROM user_details WHERE user_name = ? AND password = ?;"

        try:
            cursor.execute(query, (userNameOrPhoneNumber, password))
            user = cursor.fetchone()

            if user:
                self.root.withdraw()
                resetPasswordWindow = tk.Toplevel(self.root)
                newResetPasswordPage = ResetPasswordPage(resetPasswordWindow, self.root, user[0])
                newResetPasswordPage.createResetPasswordPage()
                return "Fetch successful"
            else:
                self.displayErrorMessage("Invalid username/phone or password")
                return "Invalid username/phone or password"
        except sqlite3.Error as err:
            self.displayErrorMessage("Error: Unable to execute query")
            print("Error: Unable to execute query", err)
            return "Database error"
        finally:
            cursor.close()
            conn.close()

    def displayErrorMessage(self, message):
        errorWindow = tk.Toplevel(self.root, bg=formBackgroundColour)
        errorWindow.title("Error")
        labelError = tk.Label(errorWindow, text=message, font=('verdana', 12), bg=formBackgroundColour)
        labelError.pack(padx=20, pady=10)
        buttonOkay = tk.Button(errorWindow, text="Okay", font=('verdana', 12), highlightbackground=formBackgroundColour, command=errorWindow.destroy)
        buttonOkay.pack(pady=5)
        self.loginEntryUserName.focus_set()

    def goToAuthenticationPage(self):
        self.root.withdraw()
        authenticationWindow = tk.Toplevel(self.root)
        newAuthenticationPage = AuthenticationPage(authenticationWindow, self.root)
        newAuthenticationPage.createResetPasswordPage()

def main():
    window = tk.Tk()
    loginPage(window)
    window.mainloop()

if __name__ == "__main__":
    main()
