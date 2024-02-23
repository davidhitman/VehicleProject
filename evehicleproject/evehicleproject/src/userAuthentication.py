import tkinter as tk
import sqlite3
from userResetPassword import ResetPasswordPage

windowWidth = 380
windowHeight = 580
jumpPageWidth = 380
jumpPageHeight = 500
popUpWidth = 250
popUpHeight = 100
formBackgroundColour = "#35608f"
headerBackgroundColour = "#000000"


class AuthenticationPage:
    def __init__(self, root, loginRoot):
        self.root = root
        self.loginRoot = loginRoot
        self.root.title("Authentication")

    def createResetPasswordPage(self):
        self.root.geometry(f"{jumpPageWidth}x{jumpPageHeight}")
        self.mainFrame = tk.Frame(self.root, bg=formBackgroundColour, width=jumpPageWidth, height=jumpPageHeight)
        self.authenticationFrame = tk.Frame(self.mainFrame, padx=30, pady=175, bg=formBackgroundColour)
        self.mainFrame.pack(fill='both', expand=1)
        self.authenticationFrame.pack(fill='both', expand=1)
        self.authenticationFrame.pack_propagate(False)

        self.labelUserEmail = tk.Label(self.authenticationFrame, text=" email: ", font=('verdana', 12), bg=formBackgroundColour)
        self.EntryUserEmail = tk.Entry(self.authenticationFrame, font=('verdana', 12))
        self.labelUserPhoneNumber = tk.Label(self.authenticationFrame, text=" phone number: ", font=('verdana', 12), bg=formBackgroundColour)
        self.EntryUserPhoneNumber = tk.Entry(self.authenticationFrame, font=('verdana', 12))
        buttonAuthentication = tk.Button(self.authenticationFrame, text="Verify", font=('verdana', 12), highlightbackground=formBackgroundColour, command=self.authentication)

        self.EntryUserEmail.focus_set()

        self.labelUserEmail.grid(row=0, column=0, sticky='e')
        self.EntryUserEmail.grid(row=0, column=1, pady=10)
        self.labelUserPhoneNumber.grid(row=1, column=0, sticky='e')
        self.EntryUserPhoneNumber.grid(row=1, column=1, pady=10)
        buttonAuthentication.grid(row=2, column=0, columnspan=2, pady=5)

    def authentication(self):
        userEmail = self.EntryUserEmail.get()
        userPhoneNumber = self.EntryUserPhoneNumber.get()
        try:
            connection = sqlite3.connect("nextbike.db")
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user_details WHERE phone_number = ? AND email_address = ?;', (userPhoneNumber, userEmail))
            user = cursor.fetchone()

            if user:
                print("Verification success")
                self.root.withdraw()
                resetPasswordWindow = tk.Toplevel(self.root)
                newResetPasswordPage = ResetPasswordPage(resetPasswordWindow, self.root, user[0])
                newResetPasswordPage.createResetPasswordPage()
                return "Verification success"
            else:
                self.displayErrorMessage("User's email address and phone number don't match")
                return "User's email address and phone number don't match"

        except sqlite3.Error as err:
            self.displayErrorMessage("Error: Unable to execute query")
            print("Error: Unable to execute query", err)
            return "Database error"

        finally:
            cursor.close()
            connection.close()

    def displayErrorMessage(self, message):
        errorWindow = tk.Toplevel(self.root, bg=formBackgroundColour)
        errorWindow.title("Error")
        labelError = tk.Label(errorWindow, text=message, font=('verdana', 12), bg=formBackgroundColour)
        labelError.pack(padx=20, pady=10)
        buttonOkay = tk.Button(errorWindow, text="Okay", font=('verdana', 12), highlightbackground=formBackgroundColour, command=errorWindow.destroy)
        buttonOkay.pack(pady=5)
        self.EntryUserEmail.focus_set()

