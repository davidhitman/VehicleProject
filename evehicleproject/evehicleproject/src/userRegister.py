import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import uuid
from userLogin import loginPage
from helper import helper
from tkinter import messagebox
import sqlite3
from userAuthentication import AuthenticationPage

hlp = helper()

windowWidth=380
windowHeight=580
formBackgroundColour="#35608f"
headerBackgroundColour="#000000"

sqlite3.register_adapter(uuid.UUID, lambda x: x.bytes)
sqlite3.register_converter("UUID", lambda x: uuid.UUID(bytes=x))

class registerPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration")
        self.mainFrame = tk.Frame(self.root, width=windowWidth, height=windowHeight)
        self.createRegisterPage()
    
    def createRegisterPage(self):
        #************************************Header************************************

        self.headerFrame=tk.Frame(self.mainFrame, bg=headerBackgroundColour, width=windowWidth, height=50)
        self.titleFrame=tk.Frame(self.headerFrame, padx=1, pady=1)
        self.labelTitle=tk.Label(self.titleFrame, text="Register", font=('verdana', 20), width=7, fg='#fff', padx=20, pady=5, bg='green')
    

        self.headerFrame.pack()
        self.titleFrame.pack()
        self.labelTitle.pack()

        self.titleFrame.place(y=26, relx=0.5, anchor=CENTER)

        #***********************************Register************************************

        self.registerFrame=tk.Frame(self.mainFrame, width=windowWidth, height=windowHeight)
        self.registerFormFrame=tk.Frame(self.registerFrame,padx=30,pady=100,bg=formBackgroundColour)

        self.registerLabelUserName=tk.Label(self.registerFormFrame, text=" User Name: ", font=('verdana',12), bg=formBackgroundColour)
        self.registerEntryUserName=tk.Entry(self.registerFormFrame, font=('verdana',12))

        self.registerlabelPhoneNumber=tk.Label(self.registerFormFrame, text=" Phone Number: ", font=('verdana',12), bg=formBackgroundColour)
        self.registerEnteyPhoneNumber=tk.Entry(self.registerFormFrame, font=('verdana',12))

        self.registerLabelEmailAddress=tk.Label(self.registerFormFrame, text=" Email: ", font=('verdana',12), bg=formBackgroundColour)
        self.registerEntryEmailAddress=tk.Entry(self.registerFormFrame, font=('verdana',12))

        self.registerLabelPassword=tk.Label(self.registerFormFrame, text=" Password: ", font=('verdana',12), bg=formBackgroundColour)
        self.registerEntryPassword=tk.Entry(self.registerFormFrame, font=('verdana',12))

        self.securityQuestions=self.getSecurityQuestions()
        if not self.securityQuestions:
            self.securityQuestions=["-------None-------"]

        self.registerLabelSecurity = tk.Label(self.registerFormFrame, text="Security Question:", font=('verdana', 12), bg=formBackgroundColour)
        self.securityQuestionVar = tk.StringVar(value=self.securityQuestions[0][1])
        self.registerDropdownSecurityQuestion = ttk.Combobox(self.registerFormFrame, textvariable=self.securityQuestionVar, values=[question[1] for question in self.securityQuestions], state="readonly")
        
        self.registerLabelAnswer = tk.Label(self.registerFormFrame, text="Question Answer:", font=('verdana', 12), bg=formBackgroundColour)
        self.registerEntryAnswer = tk.Entry(self.registerFormFrame, font=('verdana', 12))

        self.registerLabelGender=tk.Label(self.registerFormFrame, text=" Gender: ", font=('verdana',12), bg=formBackgroundColour)
        self.radioButtonsFrame=tk.Frame(self.registerFormFrame)
        self.gender=StringVar()
        self.gender.set('Male')
        self.registerRadioButtonMale=tk.Radiobutton(self.radioButtonsFrame, text='Male', font=('verdana',12), bg=formBackgroundColour, variable=self.gender, value='Male')
        self.registerRadioButtonFemale=tk.Radiobutton(self.radioButtonsFrame, text='Female', font=('verdana',12), bg=formBackgroundColour, variable=self.gender, value='Female')
        self.registerButton=tk.Button(self.registerFormFrame, text="Register", font=('verdana',12), highlightbackground=formBackgroundColour, command=self.register)
        self.toLoginLabel=tk.Label(self.registerFormFrame, text=">> already have an account? sign in", font=('Verdana',12), bg=formBackgroundColour, fg='red')

        self.mainFrame.pack(fill='both', expand=1)
        self.registerFrame.pack(fill='both', expand=1)
        self.registerFormFrame.pack(fill='both', expand=1)
        self.mainFrame.pack_propagate(FALSE)

        self.registerLabelUserName.grid(row=0, column=0, sticky='e')
        self.registerEntryUserName.grid(row=0, column=1, pady=10)

        self.registerlabelPhoneNumber.grid(row=1, column=0, sticky='e')
        self.registerEnteyPhoneNumber.grid(row=1, column=1, pady=10)

        self.registerLabelEmailAddress.grid(row=2, column=0, sticky='e')
        self.registerEntryEmailAddress.grid(row=2, column=1, pady=10)

        self.registerLabelPassword.grid(row=3, column=0, sticky='e')
        self.registerEntryPassword.grid(row=3, column=1, pady=10)

        self.registerLabelSecurity.grid(row=4, column=0, sticky='e')
        self.registerDropdownSecurityQuestion.grid(row=4, column=1, pady=10)
        self.registerDropdownSecurityQuestion.config(width=self.registerEntryUserName.winfo_reqwidth()//11)

        self.registerLabelAnswer.grid(row=5, column=0, sticky='e')
        self.registerEntryAnswer.grid(row=5, column=1, pady=10)

        self.registerLabelGender.grid(row=6, column=0, sticky='e')
        self.radioButtonsFrame.grid(row=6, column=1)
        self.registerRadioButtonMale.grid(row=0, column=0)
        self.registerRadioButtonFemale.grid(row=0, column=1)

        self.registerButton.grid(row=7, column=0, columnspan=2, pady=5)
        self.toLoginLabel.grid(row=8, column=0, columnspan=2, pady=5)

        self.toLoginLabel.bind("<Button-1>", lambda page: self.goToLoginPage())

    def register(self):  
        userID = uuid.uuid4()
        userName = self.registerEntryUserName.get()
        phoneNumber = self.registerEnteyPhoneNumber.get()
        emailAddress = self.registerEntryEmailAddress.get()
        password = self.registerEntryPassword.get()
        userGender = self.gender.get()
        selectedSecurityQuestion = self.securityQuestionVar.get()
        selectedSecurityQuestionIndex = None
        selectedSecurityQuestionAnswer = self.registerEntryAnswer.get()

        encryptedPassword = helper.encrypt_password(password)

        for index, questionText in self.securityQuestions:
            if questionText==selectedSecurityQuestion:
                selectedSecurityQuestionIndex= index
                break

        if not userName or not phoneNumber or not emailAddress or not password or not selectedSecurityQuestionAnswer:
            self.displayErrorMessage("All fields are required")
            return "All fields are required"
    
        try:
            conn = sqlite3.connect('nextbike.db')
            cursor = conn.cursor()
        except sqlite3.Error as err:
            self.displayErrorMessage("Error while connecting to SQLite")
            print("Error while connecting to SQLite", err)

        cursor.execute("SELECT * FROM user_details WHERE user_name = ? OR phone_number = ?;", (userName, phoneNumber))
        existingUser = cursor.fetchone()

        if existingUser:
            messagebox.showerror("ERROR", "Username or phone number already in use")

        try:
            cursor.execute('''
                INSERT INTO user_details (user_id, user_name, gender, phone_number, email_address, password, role_type)
                VALUES(?, ?, ?, ?, ?, ?, 'Operator')
            ''', (userID.bytes, userName, userGender, phoneNumber, emailAddress, encryptedPassword))
            cursor.execute('''
                INSERT INTO user_security_question (user_id, question_index, question_answer)
                VALUES(?, ?, ?)
            ''', (userID.bytes, selectedSecurityQuestionIndex, selectedSecurityQuestionAnswer))
            conn.commit()
            messagebox.showinfo("Registration", "Registration successful")
            self.goToLoginPage()
        except sqlite3.Error as err:
            self.displayErrorMessage("Error: Unable to execute queries")
            print("Error: Unable to execute queries", err)
            conn.rollback()
        finally:
            conn.close()
        

    def getSecurityQuestions(self):
        try:
            conn = sqlite3.connect('nextbike.db')
            cursor = conn.cursor()
        except sqlite3.Error as err:
            self.displayErrorMessage("Error while connecting to SQLite")
            print("Error while connecting to SQLite", err)
        try:
            cursor.execute("SELECT question_index, question_text FROM security_questions")
            securityQuestions = cursor.fetchall()
            conn.close()
            return securityQuestions
        except sqlite3.Error as err:
            self.displayErrorMessage("Error while fetching security questions from SQLite")
            print("Error while fetching security questions from SQLite:", err)
            return []

    def goToLoginPage(self):
        self.root.destroy()
        loginWindow = tk.Tk()
        loginPage(loginWindow)
        loginWindow.mainloop()

    def displayErrorMessage(self, message):
        errorWindow = tk.Toplevel(self.root, bg=formBackgroundColour)
        errorWindow.title("Error")
        labelError = tk.Label(errorWindow, text=message, font=('verdana', 12), bg=formBackgroundColour)
        labelError.pack(padx=20, pady=10)
        buttonOkay = tk.Button(errorWindow, text="Okay", font=('verdana', 12), highlightbackground=formBackgroundColour, command=errorWindow.destroy)
        buttonOkay.pack(pady=5)
        




