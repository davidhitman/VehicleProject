import tkinter as tk
import sqlite3

windowWidth = 380
windowHeight = 580
jumpPageWidth = 380
jumpPageHeight = 500
popUpWidth = 250
popUpHeight = 100
formBackgroundColour = "#35608f"
headerBackgroundColour = "#000000"

class ResetPasswordPage:
    def __init__(self, root, loginRoot, userID):
        self.root = root
        self.loginRoot = loginRoot
        self.userID = userID
        self.root.title("Reset Password")

    def createResetPasswordPage(self):
        self.root.geometry(f"{jumpPageWidth}x{jumpPageHeight}")
        self.mainFrame = tk.Frame(self.root, bg=formBackgroundColour, width=jumpPageWidth, height=jumpPageHeight)
        self.resetPasswordFrame = tk.Frame(self.mainFrame, padx=30, pady=175, bg=formBackgroundColour)
        self.mainFrame.pack(fill='both', expand=1)
        self.resetPasswordFrame.pack(fill='both', expand=1)
        self.resetPasswordFrame.pack_propagate(False)

        self.labelNewPassword = tk.Label(self.resetPasswordFrame, text="New Password:", font=('verdana', 12),
                                         bg=formBackgroundColour)
        self.EntryNewPassword = tk.Entry(self.resetPasswordFrame, font=('verdana', 12), show="*")
        self.labelComfirmPassword = tk.Label(self.resetPasswordFrame, text="Confirm Password:", font=('verdana', 12),
                                             bg=formBackgroundColour)
        self.EntryComfirmPassword = tk.Entry(self.resetPasswordFrame, font=('verdana', 12), show="*")
        buttonChangePassword = tk.Button(self.resetPasswordFrame, text="Change Password", font=('verdana', 12),
                                        highlightbackground=formBackgroundColour, command=self.changePassword)

        self.EntryNewPassword.focus_set()

        self.labelNewPassword.grid(row=0, column=0, sticky='e')
        self.EntryNewPassword.grid(row=0, column=1, pady=10)
        self.labelComfirmPassword.grid(row=1, column=0, sticky='e')
        self.EntryComfirmPassword.grid(row=1, column=1, pady=10)
        buttonChangePassword.grid(row=2, column=0, columnspan=2, pady=5)

    def changePassword(self):
        newPassword = self.EntryNewPassword.get()
        confirmPassword = self.EntryComfirmPassword.get()

        if newPassword == confirmPassword:
            try:
                connection = sqlite3.connect("nextbike.db")
                cursor = connection.cursor()

                cursor.execute("UPDATE user_details SET password = ? WHERE user_id = ?", (newPassword, self.userID))
                connection.commit()
                print("Password updated successfully")

            except sqlite3.Error as err:
                self.displayErrorMessage("Error while connecting to SQLite")
                print("Error while connecting to SQLite:", err)

            finally:
                cursor.close()
                connection.close()
        else:
            print("Passwords do not match")

    def displayErrorMessage(self, message):
        errorWindow = tk.Toplevel(self.root, bg=formBackgroundColour)
        errorWindow.title("Error")
        labelError = tk.Label(errorWindow, text=message, font=('verdana', 12), bg=formBackgroundColour)
        labelError.pack(padx=20, pady=10)
        buttonOkay = tk.Button(errorWindow, text="Okay", font=('verdana', 12), highlightbackground=formBackgroundColour,
                               command=errorWindow.destroy)
        buttonOkay.pack(pady=5)
        self.EntryNewPassword.focus_set()


