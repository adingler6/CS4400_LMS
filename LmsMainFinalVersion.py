from tkinter import *
import datetime
import tkinter as tk
import pymysql
import time
frames = {}

#main class holds the array of frames needed to run program
class LmsMain(tk.Tk):

    uName = ""
    sISBN = ""
    sAuthor = ""
    sTitle = ""
    isLibrarian = 0

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        
        global frames
        self.frames = frames

        for F in (LoginPage, RegistrationPage, SearchBooksPage, MakeProfilePage, RequestExtensionPage, FutureHoldRequestPage, TrackLocationPage, ReturnBookPage, HoldRequestPage, BookCheckout, LostDamagedBook, PopUserReportPage, PopBookReportPage, PopSubReportPage, DamagedBookReportPage, BookToShelfPage):            
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    @staticmethod
    def connect(self):
        try:
            global db
            db = pymysql.connect(host='academic-mysql.cc.gatech.edu',user='cs4400_Group_41',
            db='cs4400_Group_41',passwd='YIBz9hoA')

        except:
            messagebox.showwarning("Internet Connection Error!", "Please check your internet connection!")
            return None
        


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        l = tk.Label(self, text = "Login", bg = "yellow", relief = RAISED)
        l.grid(column=0, columnspan=5, stick = EW)

        tk.Label(self).grid(row=1, column=0)
        
        tk.Label(self, text = "Username").grid(row=2, column=0, sticky=E)
        self.e = Entry(self, width=30)
        self.e.grid(row=2,column=1,columnspan=2)
        tk.Label(self, text = "Password").grid(row=3, column=0, sticky=E)
        self.e1 = Entry(self,show='*', width=30)
        self.e1.grid(row=3,column=1,columnspan=2)

        tk.Label(self).grid(row=4, column=0)

        tk.Button(self, text = "Register", command = lambda: controller.show_frame(RegistrationPage)).grid(row=5,column=1,sticky=E)
        tk.Button(self, text = "Login", command = self.LoginCheck).grid(row=5,column=2,sticky=EW)
        self.continuebutton = tk.Button(self, text = "Continue",state=DISABLED, command= lambda: controller.show_frame(SearchBooksPage))
        self.continuebutton.grid(row=5,column=3,sticky=E)
        #tk.Button(self, text = "Lost/Damaged Book", command= lambda: controller.show_frame(LostDamagedBook)).grid(row=5,column=4,sticky=E)


    def LoginCheck(self):   # Method that checks to see if username/password combination already exists in database. If so, user is successfully "logged in".
        LmsMain.connect(self)
        LmsMain.uName = self.e.get()
        LmsMain.uPass = self.e1.get()
        
        cursor = db.cursor()
        user_sql = "SELECT * FROM User WHERE Username=%s AND Password=%s"
        user_counter = cursor.execute(user_sql, (LmsMain.uName,LmsMain.uPass))



        if user_counter == 0:
            self.continuebutton.config(state='disable')
            messagebox.showwarning("Username/Password Combination Error!", "Your username/password combination is incorrect!")
            cursor.close()
            db.close()
            return

        staff_sql = "SELECT isStaff FROM StudentFaculty WHERE Username=%s"
        cursor.execute(staff_sql, (LmsMain.uName))
        self.isLibrarian = cursor.fetchone()
        LmsMain.isLibrarian = self.isLibrarian[0]

        self.EnableContinue()

        if LmsMain.isLibrarian == 1:
            ldB.config(state='normal')
            dbrB.config(state='normal')
            pbrB.config(state='normal')
            furB.config(state='normal')
            psrB.config(state='normal')
            bcoB.config(state='normal')
            rbB.config(state='normal')
            butt.config(state='normal')
        elif LmsMain.isLibrarian == 0:
            ldB.config(state='disabled')
            dbrB.config(state='disabled')
            pbrB.config(state='disabled')
            furB.config(state='disabled')
            psrB.config(state='disabled')
            bcoB.config(state='disabled')
            rbB.config(state='disabled')
            butt.config(state='disabled')
        
        messagebox.showwarning("Success!", "Login successful!")

    def EnableContinue(self):
        self.continuebutton.config(state='normal')

    ##sql to query check if logged in user is faculty --> update isFaculty
            


class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        l1 = Label(self, text = "New User Registration", bg = "yellow", relief = RAISED)
        l1.grid(column=0, columnspan=5, stick = EW)

        tk.Label(self).grid(row=1, column=0)
        
        tk.Label(self, text = "Username").grid(row=2, column=0, sticky=W)
        self.e3 = Entry(self, width=30)
        self.e3.grid(row=2,column=1,columnspan=2)
        tk.Label(self, text = "Password").grid(row=3, column=0, sticky=W)
        self.e4 = Entry(self, width=30)
        self.e4.grid(row=3,column=1,columnspan=2)
        tk.Label(self, text = "Confirm Password").grid(row=4, column=0, sticky=W)
        self.e5 = Entry(self, width=30)
        self.e5.grid(row=4,column=1,columnspan=2)
        tk.Label(self, text = "").grid(row=5)

        tk.Button(self, text = "Cancel", command = lambda: controller.show_frame(LoginPage)).grid(row=6,column=2,sticky=EW)
        tk.Button(self, text = "Register", command = self.RegisterNew).grid(row=6,column=4)
        tk.Button(self, text = "Make Profile", command = lambda: controller.show_frame(MakeProfilePage)).grid(row=6,column=6)

    def RegisterNew(self):                                      
        LmsMain.connect(self)
        LmsMain.uName = self.e3.get()
        password = self.e4.get()
        password2 = self.e5.get()

        if LmsMain.uName == "":                                                                                               # Username entry must not be left blank.
            messagebox.showwarning("Username Error!", "Please enter a username!")
            return


        if password == "":                                                                                               # Password entry must not be left blank.
            messagebox.showwarning("Check password!", "Please enter a password!")
            return

        if password2 == "":                                                                                             # Password must be confirmed.
            messagebox.showwarning("Check password!", "Please confirm password!")
            return

        if password != password2:                                                                                       # Password and confirm password must match.
            messagebox.showwarning("Check password!", "Your password does not match your confirmation password!")
            return


        cursor = db.cursor()
        user_sql = "SELECT * FROM User WHERE Username=%s"
        counter = cursor.execute(user_sql, (LmsMain.uName,))

        if counter == 1:
            messagebox.showwarning("Username Error!", "Username already exists! Please pick another username.")         # Username must not already exist in database.
            cursor.close()
            db.close()
            return
                                                                                                    
        cursor = db.cursor()
        sql = "INSERT INTO User (Username, Password) VALUES (%s, %s)"                     
        cursor.execute( sql, ( LmsMain.uName, password) )
        cursor.close()
        db.commit()
        db.close()
        messagebox.showwarning("Congratulations!", "Successful Registration!")                                      # Successful Registration if you got this far! 


class MakeProfilePage(tk.Frame):

    #needs to get user info from lms main
    #insert attributes into appropriate tuple in User relation

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        f= Frame(self)
        f.grid(row=0,columnspan=100)
        Label(f, text = "Create Profile", bg = "yellow", width=105, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)

        frame = Frame(self)
        frame.grid(row=1, column=0)

        self.frame2 = Frame(self)
        self.frame2.grid(row=1, column=1)

        Label(frame, text = "First Name").grid(row=2, column=0, sticky=W)
        self.firstname = Entry(frame, width=30)
        self.firstname.grid(row=2,column=1,columnspan=2)

        Label(self.frame2, text = "Last Name").grid(row=2, column=2, sticky=W)
        self.lastname = Entry(self.frame2, width=30)
        self.lastname.grid(row=2,column=3,columnspan=2)
        
        Label(frame, text = "D.O.B. (YYYY-MM-DD)").grid(row=3, column=0, sticky=W)
        self.dob = Entry(frame, width=30)
        self.dob.grid(row=3,column=1,columnspan=2)

        Label(self.frame2, text = "Gender").grid(row=3, column=2, sticky=W)

        self.gVar = StringVar()
        self.gVar.set("")
        lst = ["","Male", "Female"]
        OptionMenu(self.frame2, self.gVar, *lst).grid(row=3, column=3, sticky=W)

        

        Label(frame, text = "Email").grid(row=4, column=0, sticky=W)
        self.email = Entry(frame, width=30)
        self.email.grid(row=4,column=1,columnspan=2)

        Label(self.frame2, text = "Are you a faculty member?").grid(row=4, column=2, sticky=W)

        try:
            if self.facultyVar.get()==1:
                pass
        except:
            self.facultyVar = IntVar()

        facultyCheck = Checkbutton(self.frame2, text = "Yes", variable=self.facultyVar, command= self.checkFaculty).grid(row=4, column=3, sticky=W)


        Label(self.frame2, text = "Associated Department").grid(row=5,column=2,sticky=W)

        self.dVar = StringVar()
        self.dVar.set("")
        lst = ["","Math","Science", "English", "Art"]
        self.deptmenu = OptionMenu(self.frame2, self.dVar, *lst)
        self.deptmenu.grid(row=5, column=3, sticky=W)
        self.deptmenu.config(state=DISABLED)



        Label(frame, text = "Address").grid(row=5, column=0, sticky=NW)
        self.address = Entry(frame, width=50)
        self.address.grid(row=5,column=1)


        
        Button(self.frame2, text="Submit", command=self.SubmitRegistration).grid(row=6, column=5)
        Button(self.frame2, text="Search Books", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=6, column=7)

    
    def SubmitRegistration(self):
        if self.firstname.get()=="" and self.lastname.get()=="":
            messagebox.showwarning("Silly you...","Please enter a name!")
            return
            
        
        LmsMain.connect(self)
        username = LmsMain.uName
        name = self.firstname.get() + " " + self.lastname.get()
        dob = self.dob.get()
        
        if self.gVar.get() == "Male":
            gender = "M"
        elif self.gVar.get() == "Female":
            gender = "F"
        else:
            gender = ""
        isDebarred = 0
        email = self.email.get()
        address = self.address.get()
        isFaculty = self.facultyVar.get()
        penalty = 0
        
        
        dept = self.dVar.get()
        sql = "INSERT INTO StudentFaculty (Username, Name, DOB, Gender, IsDebarred, Email, Address, IsFaculty, Penalty, Dept) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" 

        cursor = db.cursor()                    
        cursor.execute( sql, ( username, name, dob, gender, isDebarred, email, address, isFaculty, penalty, dept))
        messagebox.showwarning("Congratulations" + LmsMain.uName + "Profile is made!", "Please click Search Books")


    
    def checkFaculty(self): 

        if self.facultyVar.get() == 1:
            self.deptmenu.config(state=NORMAL)
        if self.facultyVar.get() == 0:
            self.deptmenu.config(state=DISABLED)
            

class SearchBooksPage(tk.Frame):
    result = ""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sbl1 = Label(self, text = "Search Books", bg = "yellow")
        self.sbl1.grid(column=0, columnspan=6, sticky = EW)

        self.sbl2 = Label(self, text='ISBN')
        self.sbl2.grid(row=1, column=0)

        self.sbl3 = Label(self, text='Title')
        self.sbl3.grid(row=2, column=0)

        self.sbl4 = Label(self, text='Author')
        self.sbl4.grid(row=3, column=0)

        self.sbsvISBN = StringVar()
        self.sbe1 = Entry(self, textvariable=self.sbsvISBN, width=18)
        self.sbe1.grid(row=1,column=1,columnspan=2)

        self.sbsvTitle = StringVar()
        self.sbe2 = Entry(self, textvariable=self.sbsvTitle, width=18)
        self.sbe2.grid(row=2,column=1,columnspan=2)

        self.sbsvAuthor = StringVar()
        self.sbe3 = Entry(self, textvariable=self.sbsvAuthor, width=18)
        self.sbe3.grid(row=3,column=1,columnspan=2)

        Button(self, text='Back', command = lambda: controller.show_frame(LoginPage)).grid(row=5,column=0)
        Button(self, text='Search',command= self.searchDatBook).grid(row=5,column=2) #holdRequest gui
        Button(self, text='Hold Request Page', command= lambda: controller.show_frame(HoldRequestPage)).grid(row=5,column=4)

        Label(self,text='                      ').grid(row=6,column=0)
        Label(self,text='Additional Functions for Students and Faculty').grid(row=7,column=1)
        Button(self, text='Request Extension',command= lambda: controller.show_frame(RequestExtensionPage)).grid(row=8,column=0)
        Button(self, text='Future Hold',command= lambda: controller.show_frame(FutureHoldRequestPage)).grid(row=8,column=1)
        Button(self, text='Track Location',command= lambda: controller.show_frame(TrackLocationPage)).grid(row=8,column=2)
               

        Label(self,text='                     ').grid(row=9,column=0)
        Label(self,text='Additional Functions for Staff').grid(row=10,column=1)
        
        global rbB 
        rbB = Button(self, text='Return Book',command= lambda: controller.show_frame(ReturnBookPage))
        rbB.grid(row=11,column=0)
        global ldB
        ldB = Button(self, text='Lost/Damaged Book',command= lambda: controller.show_frame(LostDamagedBook),state=DISABLED)
        ldB.grid(row=11,column=1)
        global bcoB
        bcoB = Button(self, text='Book Checkout',command= lambda: controller.show_frame(BookCheckout))
        bcoB.grid(row=11,column=2)
        global butt
        butt = Button(self, text='book 2 shelf',command= lambda: controller.show_frame(BookToShelfPage),state=DISABLED)
        butt.grid(row=11, column=3)


        Label(self,text='                      ').grid(row=12,column=1)
        Label(self,text='Reports').grid(row=13,column=1)
        global dbrB
        dbrB = Button(self, text='Damaged Book Reports',command= lambda: controller.show_frame(DamagedBookReportPage), state=DISABLED)
        dbrB.grid(row=14,column=0)
        global pbrB
        pbrB = Button(self, text='Popular Book Reports',command= lambda: controller.show_frame(PopBookReportPage), state=DISABLED)
        pbrB.grid(row=14,column=1)
        global furB
        furB = Button(self, text='Frequent User Reports',command= lambda: controller.show_frame(PopUserReportPage), state=DISABLED)
        furB.grid(row=14,column=2)
        global psrB
        psrB = Button(self, text='Popular Subject Reports',command= lambda: controller.show_frame(PopSubReportPage), state=DISABLED)
        psrB.grid(row=14,column=3)



    def searchDatBook(self):
        LmsMain.connect(self)
        LmsMain.sISBN = self.sbsvISBN.get()
        LmsMain.sTitle = self.sbsvTitle.get()
        LmsMain.sAuthor = self.sbsvAuthor.get()

        if LmsMain.sISBN != "":
            cursor = db.cursor()
            searchbook_sql = "SELECT Book.ISBN, Book.Title, Book.Edition, COUNT(BookCopy.ISBN) as CopiesAvailable, Book.IsBookOnReserve FROM Book, BookCopy WHERE Book.ISBN = BookCopy.ISBN AND Book.ISBN = '{}' and BookCopy.IsOnHold = 0 and BookCopy.IsCheckedOut = 0 AND BookCopy.IsDamaged = 0 GROUP BY ISBN".format(LmsMain.sISBN)
            cursor.execute(searchbook_sql)
            SearchBooksPage.result = cursor.fetchall()
            messagebox.showwarning(LmsMain.uName + " We have searched for your book!","Please click hold request to view results...")

        elif LmsMain.sTitle != "":
            cursor = db.cursor()
            searchbook_sql = "SELECT Book.ISBN, Book.Title, Book.Edition, COUNT(BookCopy.ISBN) as CopiesAvailable, Book.IsBookOnReserve FROM Book, BookCopy WHERE Book.ISBN = BookCopy.ISBN AND Book.Title LIKE '%{}%' AND BookCopy.IsOnHold = 0 and BookCopy.IsCheckedOut = 0 AND BookCopy.IsDamaged = 0 GROUP BY ISBN".format(LmsMain.sTitle)
            cursor.execute(searchbook_sql)
            SearchBooksPage.result = cursor.fetchall()
            messagebox.showwarning(LmsMain.uName + " We have searched for your book!","Please click hold request to view results...")


        elif LmsMain.sAuthor != "":
            cursor = db.cursor()
            searchbook_sql = "SELECT Book.ISBN, Book.Title, Book.Edition, COUNT(Distinct BookCopy.CopyNum) as CopiesAvailable, Book.IsBookOnReserve FROM Book NATURAL JOIN BookCopy NATURAL JOIN Author WHERE Book.ISBN = BookCopy.ISBN AND Book.ISBN AND Author.ISBN = Book.ISBN AND Author.Authors LIKE '%{}%' and BookCopy.IsOnHold = 0 and BookCopy.IsCheckedOut = 0 AND BookCopy.IsDamaged = 0 GROUP BY ISBN".format(LmsMain.sAuthor)
            cursor.execute(searchbook_sql)
            SearchBooksPage.result = cursor.fetchall()
            messagebox.showwarning(LmsMain.uName + " We have searched for your book!","Please click hold request to view results...")


        else:
            messagebox.showwarning("Oops!","Please enter searching criteria.")
        topTuple = []
        bottomTuple = []
        for i in SearchBooksPage.result:
            if i[4]==0:
                topTuple.append(i)
            elif i[4]==1:
                bottomTuple.append(i)
        frames[HoldRequestPage].makeframeswork(topTuple,bottomTuple)
        return

    #result = self.result
    

class BookToShelfPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Book To Shelf", bg = "yellow", relief = RAISED)
        l.grid(column=0, columnspan=5, stick = EW)

        tk.Label(self).grid(row=1, column=0)
        
        tk.Label(self, text = "ISBN").grid(row=2, column=0, sticky=E)
        self.e = Entry(self, width=30)
        self.e.grid(row=2,column=1,columnspan=2)
        tk.Label(self, text = "Copy Number").grid(row=3, column=0, sticky=E)
        self.e1 = Entry(self, width=30)
        self.e1.grid(row=3,column=1,columnspan=2)

        tk.Label(self).grid(row=4, column=0)

        Button(self, text = "Place Book on shelf", command = self.placeOnShelf).grid(row=5,column=1,sticky=E)
        Button(self, text = "Back", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=5,column=2,sticky=EW)

    def placeOnShelf(self):
        isbn = self.e.get()
        copyNum = self.e1.get()
        LmsMain.connect(self)
        cursor = db.cursor()

        toShelf_sql = "UPDATE BookCopy SET IsOnHold = 0 WHERE ISBN = %s AND copyNum = %s"
        cursor.execute(toShelf_sql,(isbn,copyNum))
        messagebox.showwarning("Congrats!","you returned the book to shelf")




class RequestExtensionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f= Frame(self)
        f.grid(row=0,columnspan=100)
        Label(f, text = "Request extension on a book", bg = "yellow", width=100, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)

        frame= Frame(self)
        frame.grid(row=1,column=0, columnspan=100)

        Label(frame).grid(row=0)

        Label(frame, text = "Enter your issue_id").grid(row=1, column=0, sticky=W)
        self.issue_id = Entry(frame, width=25)
        self.issue_id.grid(row=1,column=1,columnspan=2)

        Button(frame, text="Submit", command = self.RequestExtension).grid(row=1,column=3,sticky=W)

        Label(frame).grid(row=2)

        frame2= Frame(self)
        frame2.grid(row=2)

        Label(frame2, text = "Original Checkout Date").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert date, and change back to DISABLED.
        self.originalcheckoutdate = Entry(frame2, width=25, state=DISABLED)
        self.originalcheckoutdate.grid(row=0,column=1,columnspan=2)

        Label(frame2, text = "Current Extension Date").grid(row=1, column=0, sticky=W)
        self.currentextensiondate = Entry(frame2, width=25, state=DISABLED)
        self.currentextensiondate.grid(row=1,column=1,columnspan=2)

        Label(frame2, text = "New Extension Date").grid(row=2, column=0, sticky=W)
        self.newextensiondate = Entry(frame2, width=25, state=DISABLED)
        self.newextensiondate.grid(row=2,column=1,columnspan=2)


        frame3= Frame(self)
        frame3.grid(row=2, column=5, columnspan=100)

        Label(frame3).grid(row=0)

        Label(frame3, text = "Current Return Date").grid(row=1, column=0, sticky=W)
        self.currentreturndate = Entry(frame3, width=20, state=DISABLED)
        self.currentreturndate.grid(row=1,column=1,columnspan=2)

        Label(frame3, text = "New Estimated Return Date").grid(row=2, column=0, sticky=W)
        self.newestimatedreturndate = Entry(frame3, width=20, state=DISABLED)
        self.newestimatedreturndate.grid(row=2,column=1,columnspan=2)

        Label(frame3).grid(row=3)

        Button(frame, text='Back',command= lambda: controller.show_frame(SearchBooksPage)).grid(row=1, column=4,sticky=W)
        
    def RequestExtension(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        isdebarred_sql = "SELECT UserName,IsDebarred,IsFaculty FROM StudentFaculty WHERE Username = %s"
        cursor.execute(isdebarred_sql, (LmsMain.uName))

        isdebarred = cursor.fetchone()
        
        

        if isdebarred[1] == 1:
            messagebox.showwarning("Sorry!", "You can't request a future hold due to your debarred status.")
            return
        
        if isdebarred[0] == LmsMain.uName and self.issue_id.get()[0] == "C":

        
            if isdebarred[2] == 0:
                cursor = db.cursor()
                issue_sql = "SELECT UserName, ISBN, CopyNum, IssueID, DateOfIssue, CountOfExtension, ExtensionDate, LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 28 DAY))) as ExpectedReturnDate, CURDATE() as Date, LEAST(DATE_ADD(CURDATE(), INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 28 DAY))) as NewReturnDate FROM Issues WHERE IssueID = %s"
                cursor.execute(issue_sql, (self.issue_id.get()))
                issue = cursor.fetchone()
                if issue[0] != LmsMain.uName:
                    messagebox.showwarning("Sorry!", "This is not your book...")
                    return
                cursor = db.cursor()
                previousfuturerequest_sql = "SELECT FutureRequestor FROM BookCopy WHERE ISBN = %s AND CopyNum = %s"
                cursor.execute(previousfuturerequest_sql, (issue[1], issue[2]))
                previousfuturerequest = cursor.fetchone()
                
                if None not in previousfuturerequest:
                   messagebox.showwarning("Sorry!", "Another user requested a future extension. You cannot request the extension.")
                   return

                
    
                countofex = issue[5]
                currentdate = issue[8].strftime("%m %d %Y")
                expectedreturndate = issue[7]
                
                if countofex < 2 and currentdate < expectedreturndate:
                    cursor = db.cursor()
                    placeextension_sql = "UPDATE Issues SET ExtensionDate = CURDATE(), CountOfExtension = CountOfExtension + 1 WHERE IssueID = %s"
                    cursor.execute(placeextension_sql, (self.issue_id.get()))
                    messagebox.showwarning("Congratulations!", "You have successfully requested an extension!")
                else:
                    messagebox.showwarning("Sorry!", "You already have 2 extensions on this book")
                    return

                    
                    

            if isdebarred[2] == 1:
                cursor = db.cursor()
                issue_sql = "SELECT UserName, ISBN, CopyNum, IssueID, DateOfIssue, CountOfExtension, ExtensionDate, LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 56 DAY))) as ExpectedReturnDate, CURDATE() as Date, LEAST(DATE_ADD(CURDATE(), INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 56 DAY))) as NewReturnDate FROM Issues WHERE IssueID = %s"
                cursor.execute(issue_sql, (self.issue_id.get()))
                issue = cursor.fetchone()
                if issue[0] != LmsMain.uName:
                    messagebox.showwarning("Sorry!", "This is not your book...")
                    return
                cursor = db.cursor()
                previousfuturerequest_sql = "SELECT FutureRequestor FROM BookCopy WHERE ISBN = %s AND CopyNum = %s"
                cursor.execute(previousfuturerequest_sql, (issue[1], issue[2]))
                previousfuturerequest = cursor.fetchone()
                
                if None not in previousfuturerequest:
                   messagebox.showwarning("Sorry!", "Another user requested a future extension. You cannot request the extension.")
                   return
    
                countofex = issue[5]
                currentdate = issue[8].strftime("%m %d %Y")
                expectedreturndate = issue[7]
                
                if countofex < 5 and currentdate < expectedreturndate:
                    cursor = db.cursor()
                    placeextension_sql = "UPDATE Issues SET ExtensionDate = CURDATE(), CountOfExtension = CountOfExtension + 1 WHERE IssueID = %s"
                    cursor.execute(placeextension_sql, (self.issue_id.get()))
                    messagebox.showwarning("Congratulations!", "You have successfully requested an extension!")
                else:
                    messagebox.showwarning("Sorry!", "You already have 5 extensions on this book")
                    return

            
            self.originalcheckoutdate.config(state=NORMAL)
            self.originalcheckoutdate.insert(0,issue[4])
            self.originalcheckoutdate.config(state=DISABLED)

            self.currentextensiondate.config(state=NORMAL)
            self.currentextensiondate.insert(0,issue[6])
            self.currentextensiondate.config(state=DISABLED)


            self.newextensiondate.config(state=NORMAL)
            self.newextensiondate.insert(0,issue[8])
            self.newextensiondate.config(state=DISABLED)

            self.currentreturndate.config(state=NORMAL)
            self.currentreturndate.insert(0,issue[7])
            self.currentreturndate.config(state=DISABLED)

            self.newestimatedreturndate.config(state=NORMAL)
            self.newestimatedreturndate.insert(0,issue[9])
            self.newestimatedreturndate.config(state=DISABLED)   


        else:
            messagebox.showwarning("Sorry!", "You need to have the book checked out in order to request extension.")
            return


class HoldRequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.sbl1 = Label(self, text = "Hold Request for a Book", bg = "yellow")
        self.sbl1.grid(column=0, columnspan=6, sticky = EW)

        Label(self, text='Books Available Summary').grid(column=0,row=1)


        atuple=(('0321','funda','title','edition','copies'),('yoyoma','helloo','harry potter','water','5'))
        atuple = SearchBooksPage.result
        self.rbintvar = IntVar()


        self.f = Frame(self)
        self.f.grid(row=3,columnspan=5)

        
        Label(self,text='                  ').grid(row=4,column=0)
        
        Label(self,text='Hold Request Date').grid(row=5,column=0)

        self.hrsv1 = StringVar()
        self.hre2 = Entry(self, textvariable=self.hrsv1,state=DISABLED)
        self.hre2.grid(row=5,column=1)

        Label(self,text='Estimated Return Date').grid(row=5,column=2)

        self.hrsv2 = StringVar()
        self.hre2 = Entry(self, textvariable=self.hrsv2,state=DISABLED)
        self.hre2.grid(row=5,column=3)

        Label(self,text='                      ').grid(row=6,column=0)

        Button(self, text='Back', command = lambda: controller.show_frame(SearchBooksPage)).grid(row=7,column=2)
        Button(self, text='Submit',command=self.SubmitHoldRequest).grid(row=7,column=3)
        Button(self, text='Close').grid(row=7,column=4)

        Label(self,text='                      ').grid(row=8,column=0)
        Label(self,text='                      ').grid(row=9,column=0)
        Label(self,text='                      ').grid(row=10,column=0)

        Label(self,text='Books on Reserve').grid(row=11,column=0)

        self.f2 = Frame(self)
        self.f2.grid(row=12,column=0,columnspan=5)
        Label(self,text='                      ').grid(row=13,column=0)


        

    def makeframeswork(self,topTuple,bottomTuple):

        self.f.destroy()
        self.f2.destroy()
        self.f = Frame(self)
        self.f.grid(row=3,column=0,columnspan=5)
        self.f2 = Frame(self)
        self.f2.grid(row=12,column=0,columnspan=5)

        Label(self.f, text='Select').grid(row=0,column=0)
        Label(self.f, text='ISBN').grid(row=0, column=1)
        Label(self.f, text='Title of Book').grid(row=0,column=2)
        Label(self.f, text='Edition').grid(row=0, column=3)
        Label(self.f, text='# of Copies').grid(row=0, column=4)

        Label(self.f2, text='ISBN').grid(row=0, column=0)
        Label(self.f2, text='Title of Book').grid(row=0,column=1)
        Label(self.f2, text='Edition').grid(row=0, column=2)
        Label(self.f2, text='# of Copies').grid(row=0, column=3)

        for i in range(len(topTuple)):
            Radiobutton(self.f,variable=self.rbintvar,value=i+1,command=self.RadioButtonFunction).grid(row=i+1,column=0)
            e1 = Entry(self.f)
            e1.insert(0,topTuple[i][0])
            e1.grid(row=i+1,column=1)
            e1.configure(state=DISABLED)
            e2 = Entry(self.f)
            e2.insert(0,topTuple[i][1])
            e2.grid(row=i+1,column=2)
            e2.configure(state=DISABLED)
            e3 = Entry(self.f)
            e3.insert(0,topTuple[i][2])
            e3.grid(row=i+1,column=3)
            e3.configure(state=DISABLED)
            e4 = Entry(self.f)
            e4.insert(0,topTuple[i][3])
            e4.grid(row=i+1,column=4)
            e4.configure(state=DISABLED)



        for i in range(len(bottomTuple)):
            en1 = Entry(self.f2)
            en1.insert(0,bottomTuple[i][0])
            en1.grid(row=i+1,column=0)
            en1.configure(state=DISABLED)
            en2 = Entry(self.f2)
            en2.insert(0,bottomTuple[i][1])
            en2.grid(row=i+1,column=1)
            en2.configure(state=DISABLED)
            en3 = Entry(self.f2)
            en3.insert(0,bottomTuple[i][2])
            en3.grid(row=i+1,column=2)
            en3.configure(state=DISABLED)
            en4 = Entry(self.f2)
            en4.insert(0,bottomTuple[i][3])
            en4.grid(row=i+1,column=3)
            en4.configure(state=DISABLED)

        self.availablebooks = topTuple

    def RadioButtonFunction(self):
        self.bookyouwant = self.availablebooks[self.rbintvar.get()-1]
        holddate = datetime.datetime.now()
        estdate = str(holddate + datetime.timedelta(days=17))
        holddate = str(holddate)
        
        holddate = holddate[5:7]+'/'+holddate[8:10]+'/'+holddate[0:4]
        self.hrsv1.set(holddate)
        estdate = estdate[5:7]+'/'+estdate[8:10]+'/'+estdate[0:4]
        self.hrsv2.set(estdate)

    def SubmitHoldRequest(self):
        isbn = self.bookyouwant[0]
        username = LmsMain.uName

        LmsMain.connect(self)
        cursor = db.cursor()
        
        #Check if user is debarred:
        sql = "SELECT IsDebarred FROM StudentFaculty WHERE Username = '{}'".format(username)
        cursor.execute(sql)
        isdebarred = cursor.fetchone()

        if isdebarred[0] == 1:
            messagebox.showwarning("User is debarred!","Oh No! You're debarred! Too many penalties!")
            return


        sql8 = "SELECT UserName FROM Issues WHERE Issues.ISBN = '{}' AND Issues.UserName = '{}' AND Issues.DateOfIssue > ADDDATE(CURDATE(), -3) LIMIT 1".format(isbn,username)
        cursor.execute(sql8)
        r = cursor.fetchone()

        if r == None:
            pass
        else:
            messagebox.showwarning("Cannot Submit Request","You can only put one copy of a certain book on hold!")
            return



        #Grabs lowest copy num
        sql2 = "SELECT ISBN, MIN(CopyNum) FROM BookCopy WHERE ISBN = '{}' and IsCheckedOut = 0 AND IsOnHold = 0 AND IsDamaged = 0".format(isbn)
        cursor.execute(sql2)
        result = cursor.fetchone()
        copynum = result[1]

        #Update BookCopy tuple with ISBN and CopyNum from part b
        sql3 = "UPDATE BookCopy SET IsOnHold = 1 WHERE ISBN = '{}' AND CopyNum = '{}'".format(isbn,copynum)
        cursor.execute(sql3)

        #Insert into Issue table
        sql4 = "INSERT INTO Issues (IssueID, UserName, ISBN, CopyNum, DateOfIssue, ExtensionDate) VALUES (CONCAT('H', FLOOR(100000 + (RAND() * 999999))), '{}', '{}', '{}', CURDATE(), CURDATE())".format(username,isbn,copynum)
        cursor.execute(sql4)

        sql5 = "SELECT IssueID FROM Issues WHERE UserName = '{}' AND DateOfIssue = DATE(CURDATE()) AND ISBN = '{}' AND IssueID LIKE 'H%' LIMIT 1".format(username, isbn)
        cursor.execute(sql5)
        issueID = cursor.fetchone()
        issueID = issueID[0]

        messagebox.showwarning("Request Accepted!","Congrats! Your request was put into the system. Your issue ID is: " + issueID + " Please click Back to continue Searching.")

        
    def HoldRequesttoSearchBooks(self):
        self.holdrequestWin.withdraw()
        self.searchbookswin.deiconify()

class FutureHoldRequestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f= Frame(self)
        f.grid(row=0,columnspan=60)
        Label(f, text = "Future Hold Request for a Book", bg = "yellow", width=60, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)

        frame= Frame(self)
        frame.grid(row=1,column=0, columnspan=60)

        Label(frame).grid(row=0)

        Label(frame, text = "ISBN").grid(row=1, column=0, sticky=W)
        self.futureholdisbn = Entry(frame, width=25)
        self.futureholdisbn.grid(row=1,column=1,columnspan=2)

        Button(frame, text="Request", command = self.FutureHoldRequest).grid(row=1,column=3,sticky=W)

        Label(frame).grid(row=2)

        frame2= Frame(self)
        frame2.grid(row=2)

        Label(frame2, text = "Copy Number").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert copy number, and change back to DISABLED.
        self.copynumber = Entry(frame2, width=15, state=DISABLED)
        self.copynumber.grid(row=0,column=1,columnspan=2)

        Label(frame2, text = "Expected Available Date").grid(row=1, column=0, sticky=W)
        self.expectedavailabledate = Entry(frame2, width=25, state=DISABLED)
        self.expectedavailabledate.grid(row=1,column=1,columnspan=2)

        Button(frame2, text="OK").grid(row=2,column=7)
        Button(frame2, text='Back',command= lambda: controller.show_frame(SearchBooksPage)).grid(row=2, column=8,sticky=W)


    def FutureHoldRequest(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        isdebarred_sql = "SELECT IsDebarred FROM StudentFaculty WHERE Username = %s"
        cursor.execute(isdebarred_sql, (LmsMain.uName))

        isdebarred = cursor.fetchone()
        

        if isdebarred[0] == 1:
            messagebox.showwarning("Sorry!", "You can't request a future hold due to your debarred status.")
            return

        cursor = db.cursor()
        onreserve_sql = "SELECT IsBookOnReserve FROM Book WHERE ISBN = %s"
        cursor.execute(onreserve_sql, (self.futureholdisbn.get()))
        onreserve = cursor.fetchone()
        

        if onreserve[0] == 1:
            messagebox.showwarning("Sorry!", "This book is on reserve.")
            return

        cursor = db.cursor()
        student_sql = "SELECT StudentFaculty.Username, StudentFaculty.IsFaculty, Issues.DateOfIssue, Issues.ExtensionDate, Issues.CopyNum, LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 28 DAY))) as ExpectedReturnDate FROM Issues, StudentFaculty, BookCopy WHERE Issues.ISBN = %s and Issues.ReturnDate is NULL AND Issues.UserName = StudentFaculty.Username AND StudentFaculty.IsFaculty = 0 AND BookCopy.ISBN = Issues.ISBN and BookCopy.CopyNum = Issues.CopyNum and BookCopy.FutureRequestor is NULL ORDER BY ExpectedReturnDate ASC LIMIT 1"
        cursor.execute(student_sql, (self.futureholdisbn.get()))
        student = cursor.fetchone()

        

        cursor = db.cursor()
        faculty_sql = "SELECT StudentFaculty.Username, StudentFaculty.IsFaculty, Issues.DateOfIssue, Issues.ExtensionDate, Issues.CopyNum, LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 56 DAY))) as ExpectedReturnDate FROM Issues, StudentFaculty, BookCopy WHERE Issues.ISBN = %s and Issues.ReturnDate is NULL AND Issues.UserName = StudentFaculty.Username AND StudentFaculty.IsFaculty = 1 AND BookCopy.ISBN = Issues.ISBN and BookCopy.CopyNum = Issues.CopyNum and BookCopy.FutureRequestor is NULL ORDER BY ExpectedReturnDate ASC LIMIT 1"
        cursor.execute(faculty_sql, (self.futureholdisbn.get()))
        faculty = cursor.fetchone()

        

        if faculty != None and student != None:
            if student[5] < faculty[5]:
                
                cursor = db.cursor()
                bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
                cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), student[4]))
                self.copynumber.config(state=NORMAL)
                self.copynumber.delete(0,END)
                self.copynumber.insert(0,student[4])
                self.copynumber.config(state = DISABLED)

                self.expectedavailabledate.config(state=NORMAL)
                self.expectedavailabledate.delete(0,END)
                self.expectedavailabledate.insert(0, student[5])
                self.expectedavailabledate.config(state=DISABLED)
                messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")
                
            if faculty[5] < student[5]:
                
                cursor = db.cursor()
                bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
                cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), faculty[4]))
                self.copynumber.config(state=NORMAL)
                self.copynumber.delete(0,END)
                self.copynumber.insert(0,faculty[4])
                self.copynumber.config(state = DISABLED)

                self.expectedavailabledate.config(state=NORMAL)
                self.expectedavailabledate.delete(0,END)
                self.expectedavailabledate.insert(0, faculty[5])
                self.expectedavailabledate.config(state=DISABLED)
                messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")

            if faculty[5] == student[5]:
                
                if faculty[4] < student[4]:
                    
                    cursor = db.cursor()
                    bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
                    cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), faculty[4]))
                    self.copynumber.config(state=NORMAL)
                    self.copynumber.delete(0,END)
                    self.copynumber.insert(0,faculty[4])
                    self.copynumber.config(state = DISABLED)

                    self.expectedavailabledate.config(state=NORMAL)
                    self.expectedavailabledate.delete(0,END)
                    self.expectedavailabledate.insert(0, faculty[5])
                    self.expectedavailabledate.config(state=DISABLED)
                    messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")

                if student[4] < faculty[4]:
                    
                    cursor = db.cursor()
                    bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
                    cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), student[4]))
                    self.copynumber.config(state=NORMAL)
                    self.copynumber.delete(0,END)
                    self.copynumber.insert(0,student[4])
                    self.copynumber.config(state = DISABLED)

                    self.expectedavailabledate.config(state=NORMAL)
                    self.expectedavailabledate.delete(0,END)
                    self.expectedavailabledate.insert(0, student[5])
                    self.expectedavailabledate.config(state=DISABLED)
                    messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")
                    
                    
                

        elif faculty != None:
            
            cursor = db.cursor()
            bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
            cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), faculty[4]))
            self.copynumber.config(state=NORMAL)
            self.copynumber.delete(0,END)
            self.copynumber.insert(0,faculty[4])
            self.copynumber.config(state = DISABLED)

            self.expectedavailabledate.config(state=NORMAL)
            self.expectedavailabledate.delete(0,END)
            self.expectedavailabledate.insert(0, faculty[5])
            self.expectedavailabledate.config(state=DISABLED)
            messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")

        elif student != None:
            
            cursor = db.cursor()
            bookcopy_sql = "UPDATE BookCopy SET FutureRequestor = %s WHERE ISBN = %s AND CopyNum = %s"
            cursor.execute(bookcopy_sql, (LmsMain.uName, self.futureholdisbn.get(), student[4]))
            self.copynumber.config(state=NORMAL)
            self.copynumber.delete(0,END)
            self.copynumber.insert(0,student[4])
            self.copynumber.config(state = DISABLED)

            self.expectedavailabledate.config(state=NORMAL)
            self.expectedavailabledate.delete(0,END)
            self.expectedavailabledate.insert(0, student[5])
            self.expectedavailabledate.config(state=DISABLED)
            messagebox.showwarning("Congratulations!", "You have successfully placed a future request! Please click Back")

        elif student == None and faculty == None:
            messagebox.showwarning("Sorry!", "No books available to request a future hold.")
            return
        
class TrackLocationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        f= Frame(self)
        f.grid(row=0,columnspan=100)
        Label(f, text = "Track Book Location", bg = "yellow", width=100, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)

        frame= Frame(self)
        frame.grid(row=1,column=0, columnspan=100)

        Label(frame).grid(row=0)

        Label(frame, text = "ISBN").grid(row=1, column=0, sticky=W)
        self.tracklocationisbn = Entry(frame, width=25)
        self.tracklocationisbn.grid(row=1,column=1,columnspan=2)

        Button(frame, text="Locate", command=self.TrackLocation).grid(row=1,column=3,sticky=W)
        Button(frame, text='Back',command= lambda: controller.show_frame(SearchBooksPage)).grid(row=1, column=4,sticky=W)

    
        Label(frame).grid(row=2)

        frame2= Frame(self)
        frame2.grid(row=2)

        Label(frame2, text = "Floor Number").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert floor number, and change back to DISABLED.
        self.floornumber = Entry(frame2, width=25, state=DISABLED)
        self.floornumber.grid(row=0,column=1,columnspan=2)

        Label(frame2, text = "Aisle Number").grid(row=1, column=0, sticky=W)
        self.aislenumber = Entry(frame2, width=25, state=DISABLED)
        self.aislenumber.grid(row=1,column=1,columnspan=2)


        frame3= Frame(self)
        frame3.grid(row=2, column=5, columnspan=100)

        Label(frame3).grid(row=0)

        Label(frame3, text = "Shelf Number").grid(row=1, column=0, sticky=W)
        self.shelfnumber = Entry(frame3, width=10, state=DISABLED)
        self.shelfnumber.grid(row=1,column=1,columnspan=2)

        Label(frame3, text = "Subject").grid(row=2, column=0, sticky=W)
        self.subject = Entry(frame3, width=20, state=DISABLED)
        self.subject.grid(row=2,column=1,columnspan=2)

    def TrackLocation(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        track_sql = "SELECT Book.ShelfNum, Book.Subject, Shelf.FloorNum, Shelf.AisleNum FROM Book, Shelf WHERE Book.ISBN =%s AND Book.ShelfNum = Shelf.ShelfNum;"
        cursor.execute(track_sql, (self.tracklocationisbn.get()))

        row = cursor.fetchone()
        self.shelfnumber.config(state=NORMAL)
        self.shelfnumber.delete(0,END)
        self.shelfnumber.insert(0, row[0])
        self.shelfnumber.config(state=DISABLED)

        self.subject.config(state=NORMAL)
        self.subject.delete(0,END)
        self.subject.insert(0, row[1])
        self.subject.config(state=DISABLED)

        self.floornumber.config(state=NORMAL)
        self.floornumber.delete(0,END)
        self.floornumber.insert(0, row[2])
        self.floornumber.config(state=DISABLED)

        self.aislenumber.config(state=NORMAL)
        self.aislenumber.delete(0,END)
        self.aislenumber.insert(0, row[3])
        self.aislenumber.config(state=DISABLED)



class ReturnBookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Return Book", bg = "yellow", relief = RAISED)
        l.grid(column=0, columnspan=5, stick = EW)
        
        tk.Label(self, text = "Issue ID").grid(row=2, column=0, sticky=W)
        self.issueEntry = Entry(self, width=30)
        self.issueEntry.grid(row=2,column=1,columnspan=2)
        tk.Label(self, text = "ISBN").grid(row=3, column=0, sticky=W)
        self.isbnEntry = Entry(self, width=30,state=DISABLED)
        self.isbnEntry.grid(row=3,column=1,columnspan=2)
        tk.Label(self, text= "Copy Number").grid(row=2, column=3, columnspan=3)
        self.copyNumEntry = Entry(self, width=30,state=DISABLED)
        self.copyNumEntry.grid(row=2, column=7, columnspan=2)
        tk.Label(self, text= "Username").grid(row=3, column=3, columnspan=3)
        self.userEntry = Entry(self, width=30,state=DISABLED)
        self.userEntry.grid(row=3, column=7, columnspan=2)

        self.isDamaged = 0
        self.var = StringVar()
        self.var.set("No")
        lst = ["Yes", "No"]
        OptionMenu(self, self.var, *lst).grid(row=5,column=1)
        tk.Label(self, text= "Returned In Damaged Condition?").grid(row=5, column=0)
        
        tk.Button(self, text = "Return", command = lambda: self.ReturnBook()).grid(row=8,column=1,sticky=E)
        tk.Button(self, text='Back',command= lambda: controller.show_frame(SearchBooksPage)).grid(row=8, column=2,sticky=W)


    def ReturnBook(self):
        if self.var.get() == "Yes":
            self.isDamaged = 1
        if self.var.get() == "No":
            self.isDamaged = 0
            
        
        LmsMain.connect(self)
        cursor = db.cursor()

        user_sql = "SELECT UserName FROM Issues WHERE IssueID = %s"
        cursor.execute(user_sql, (self.issueEntry.get()))
        user = cursor.fetchone()

        isfaculty_sql = "SELECT IsFaculty FROM StudentFaculty WHERE Username = %s"
        cursor.execute(isfaculty_sql, (user[0]))

        

        isfaculty = cursor.fetchone()
        

        if isfaculty[0] == 0:
            cursor = db.cursor()
            bookinfo_sql = "SELECT Issues.ISBN, Issues.CopyNum, Book.Cost, DATEDIFF(CURDATE(), LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 28 DAY)))) as DaysLate FROM Issues, Book WHERE Issues.IssueID = %s AND Book.ISBN = Issues.ISBN"
            cursor.execute(bookinfo_sql, (self.issueEntry.get()))
            bookinfo = cursor.fetchone()

        if isfaculty[0] == 1:
            cursor = db.cursor()
            bookinfo_sql = "SELECT Issues.ISBN, Issues.CopyNum, Book.Cost, DATEDIFF(CURDATE(), LEAST(DATE_ADD(Issues.ExtensionDate, INTERVAL 14 DAY), (DATE_ADD(Issues.DateOfIssue, INTERVAL 56 DAY)))) as DaysLate FROM Issues, Book WHERE Issues.IssueID = %s AND Book.ISBN = Issues.ISBN"
            cursor.execute(bookinfo_sql, (self.issueEntry.get()))
            bookinfo = cursor.fetchone()

        if bookinfo[3] > 0:
            cursor = db.cursor()
            penalty_sql = "UPDATE StudentFaculty SET Penalty = Penalty + (%s * .5) WHERE Username = %s"
            cursor.execute(penalty_sql, (bookinfo[3], user[0]))

            cursor = db.cursor()
            debarredpenalty_sql = "UPDATE StudentFaculty SET IsDebarred = 1 WHERE Username = %s AND Penalty >= 100"
            cursor.execute(debarredpenalty_sql, (user[0]))

        cursor = db.cursor()
        update_sql = "UPDATE BookCopy, Issues SET BookCopy.IsCheckedOut = 0, Issues.ReturnDate = CURDATE(), BookCopy.IsDamaged = %s WHERE Issues.IssueId = %s AND Issues.ISBN = BookCopy.ISBN and Issues.CopyNum = BookCopy.CopyNum"
        cursor.execute(update_sql, (self.isDamaged,self.issueEntry.get()))
        self.isbnEntry.config(state=NORMAL)
        self.isbnEntry.delete(0,END)
        self.isbnEntry.insert(0,bookinfo[0])
        self.isbnEntry.config(state=DISABLED)
        self.copyNumEntry.config(state=NORMAL)
        self.copyNumEntry.delete(0,END)
        self.copyNumEntry.insert(0,bookinfo[1])
        self.copyNumEntry.config(state=DISABLED)
        self.userEntry.config(state=NORMAL)
        self.userEntry.delete(0,END)
        self.userEntry.insert(0,user[0])
        self.userEntry.config(state=DISABLED)


        messagebox.showwarning("Congratulations!","You have successfully returned a book!")
            


class BookCheckout(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        f= Frame(self)
        f.grid(row=0,columnspan=100)
        Label(f, text = "Book Checkout", bg = "yellow", width=120, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)


        frame= Frame(self)
        frame.grid(row=1)

        Label(frame).grid(row=0)

        Label(frame, text = "Issue ID").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert floor number, and change back to DISABLED.
        self.bookcheckoutissue_id = Entry(frame, width=25)
        self.bookcheckoutissue_id.grid(row=0,column=1,columnspan=2)

        Label(frame, text = "ISBN").grid(row=1, column=0, sticky=W)
        self.bookcheckoutisbn = Entry(frame, width=25, state=DISABLED)
        self.bookcheckoutisbn.grid(row=1,column=1,columnspan=2)

        Label(frame, text = "Check out Date").grid(row=2, column=0, sticky=W)
        self.bookcheckoutdate = Entry(frame, width=25, state=DISABLED)
        self.bookcheckoutdate.grid(row=2,column=1,columnspan=2)


        frame2= Frame(self)
        frame2.grid(row=1, column=5, columnspan=100)


        Label(frame2, text = "User Name").grid(row=1, column=0, sticky=W)
        self.bookcheckoutusername = Entry(frame2, width=25, state=DISABLED)
        self.bookcheckoutusername.grid(row=1,column=1,columnspan=2)

        Label(frame2, text = "Copy #").grid(row=2, column=0, sticky=W)
        self.bookcheckoutcopynum = Entry(frame2, width=25, state=DISABLED)
        self.bookcheckoutcopynum.grid(row=2,column=1,columnspan=2)

        Label(frame2, text = "Estimated Return Date").grid(row=3, column=0, sticky=W)
        self.bookcheckoutestimatedreturndate = Entry(frame2, width=20, state=DISABLED)
        self.bookcheckoutestimatedreturndate.grid(row=3,column=1,columnspan=2)

        frame3= Frame(self)
        frame3.grid(row=3,column=4,columnspan=100)

        Button(frame3, text="Confirm", command = self.CheckBookCheckout).grid(row=0)
        Button(frame3, text="Back",command=lambda: controller.show_frame(SearchBooksPage)).grid(row=1)


    def CheckBookCheckout(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        user_sql = "SELECT Username FROM Issues WHERE IssueID = %s"
        cursor.execute(user_sql, (self.bookcheckoutissue_id.get()))
        user = cursor.fetchone()

        isdebarred_sql = "SELECT IsDebarred FROM StudentFaculty WHERE Username = %s"
        cursor.execute(isdebarred_sql, (user[0]))

        isdebarred = cursor.fetchone()
        

        if isdebarred[0] == 1:
            messagebox.showwarning("Sorry!", "You can't request a check out a book due to your debarred status.")
            return

        cursor = db.cursor()
        bookcheckoutinfo_sql = "SELECT DATEDIFF(CURDATE() , DateOfIssue) AS DaysSinceHoldRequest, Issues.ISBN, Issues.CopyNum, (DATE_ADD(CURDATE() , INTERVAL 14 DAY)) AS ExpectedReturnDate, CURDATE() AS CheckoutDate, UserName FROM Issues WHERE IssueID =  %s"
        cursor.execute(bookcheckoutinfo_sql, (self.bookcheckoutissue_id.get()))

        bookcheckoutinfo = cursor.fetchone()
        isbn = bookcheckoutinfo[1]
        copyNum = bookcheckoutinfo[2]
        
        if bookcheckoutinfo[0] > 3:
            messagebox.showwarning("Sorry!", "The book needs to be placed on hold or future requested. Your 3 day grace period to checkout the book has passed.")
            return

        self.bookcheckoutisbn.config(state=NORMAL)
        self.bookcheckoutisbn.delete(0,END)
        self.bookcheckoutisbn.insert(0,bookcheckoutinfo[1])
        self.bookcheckoutisbn.config(state=DISABLED)

        
        self.bookcheckoutdate.config(state=NORMAL)
        self.bookcheckoutdate.delete(0,END)
        self.bookcheckoutdate.insert(0,bookcheckoutinfo[4].strftime("%Y, %m %d "))
        self.bookcheckoutdate.config(state=DISABLED)

        self.bookcheckoutusername.config(state=NORMAL)
        self.bookcheckoutusername.delete(0,END)
        self.bookcheckoutusername.insert(0,user[0])
        self.bookcheckoutusername.config(state=DISABLED)

        self.bookcheckoutcopynum.config(state=NORMAL)
        self.bookcheckoutcopynum.delete(0,END)
        self.bookcheckoutcopynum.insert(0,bookcheckoutinfo[2])
        self.bookcheckoutcopynum.config(state=DISABLED)

        self.bookcheckoutestimatedreturndate.config(state=NORMAL)
        self.bookcheckoutestimatedreturndate.delete(0,END)
        self.bookcheckoutestimatedreturndate.insert(0,bookcheckoutinfo[3].strftime("%Y, %m %d"))
        self.bookcheckoutestimatedreturndate.config(state=DISABLED)

        cursor = db.cursor()
        bookcheckout_sql = "UPDATE BookCopy, Issues SET BookCopy.IsCheckedOut =1, BookCopy.IsOnHold =0 WHERE BookCopy.isbn = Issues.isbn AND Issues.IssueID =  %s AND Issues.CopyNum = BookCopy.CopyNum"
        cursor.execute(bookcheckout_sql, (self.bookcheckoutissue_id.get()))

        cursor = db.cursor()
        insert_sql = "INSERT INTO Issues (IssueID, UserName, ISBN, CopyNum, DateOfIssue, ExtensionDate) VALUES (CONCAT('C', FLOOR(100000 + (RAND() * 999999))), %s, %s, %s, CURDATE(), CURDATE())"
        cursor.execute(insert_sql, (bookcheckoutinfo[5], bookcheckoutinfo[1], bookcheckoutinfo[2]))

        sql3 = "SELECT IssueID FROM Issues WHERE UserName = '{}' AND DateOfIssue = DATE(CURDATE()) AND ISBN = '{}' AND CopyNum = '{}' AND IssueID LIKE 'C%' LIMIT 1".format(bookcheckoutinfo[5],isbn,copyNum)
        cursor.execute(sql3)
        issueID = cursor.fetchone()
        issueID = issueID[0]

        messagebox.showwarning("Congrats!","You have successfully checked out your desired book! Your issue ID is: " + issueID + " Please Click Back")

class LostDamagedBook(tk.Frame):
   
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        f= Frame(self)
        f.grid(row=0,columnspan=100)
        Label(f, text = "Lost/Damaged Book", bg = "yellow", width=110, relief = RAISED).grid(column=0, columnspan=100, sticky = EW)


        frame= Frame(self)
        frame.grid(row=1)

        Label(frame).grid(row=0)

        Label(frame, text = "ISBN").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert floor number, and change back to DISABLED.
        self.lostdamagedbookisbn = Entry(frame, width=30)
        self.lostdamagedbookisbn.grid(row=0,column=1,columnspan=2)

        Label(frame, text = "Current Time").grid(row=1, column=0, sticky=W)
        date= StringVar()
        self.lostdamagedbookcurrenttime = Entry(frame, width=25, textvariable = date, state=DISABLED)
        date.set(str(datetime.datetime.now()))
        self.lostdamagedbookcurrenttime.grid(row=1,column=1,columnspan=2)


        frame2= Frame(self)
        frame2.grid(row=1, column=5, columnspan=100)


        Label(frame2, text = "Book Copy #").grid(row=1, column=0, sticky=W)
        self.var = StringVar()
        self.var.set('1')
        lst = ['1','2','3','4','5','6','7']
        OptionMenu(frame2, self.var,*lst).grid(row=1,column=1,columnspan=2)

        Label(frame2).grid(row=3, column=0)
 
        frame3= Frame(self)
        frame3.grid(row=2,column=1,columnspan=100,sticky=EW)

        Button(frame3, text="Look for the last user",command=self.LookForUser).grid(row=0,sticky=EW)

        Label(frame3).grid(row=1)
        Label(frame3).grid(row=2)

        frame4=Frame(self)
        frame4.grid(row=3)


        Label(frame4, text = "Last User of the Book").grid(row=0, column=0, sticky=W)      # After sql is committed, change state of entries to ACTIVE, insert last user, and change back to DISABLED.
        self.lostdamagedbooklastuser = Entry(frame4, width=25,state=DISABLED)
        self.lostdamagedbooklastuser.grid(row=0,column=1,columnspan=2)

        Label(frame4, text = "Amount to be charged").grid(row=1, column=0, sticky=W)
        self.lostdamagedbookpenalty = Entry(frame4, width=25)
        self.lostdamagedbookpenalty.grid(row=1,column=1,columnspan=2)

        Button(frame4, text="Submit",command=self.SubmitPenalty).grid(row=3,column=5,sticky=E)
        Button(frame4, text="Cancel",command=lambda: controller.show_frame(SearchBooksPage)).grid(row=3,column=7,sticky=E)

    def LookForUser(self):
        isbn = self.lostdamagedbookisbn.get()
        bookcopy = self.var.get()

        LmsMain.connect(self)
        cursor = db.cursor()
        
        #grab last user from $isbn and $copyNum
        sql = "SELECT UserName, DateOfIssue FROM Issues WHERE ISBN = '{}' and CopyNum = '{}' and IssueId LIKE 'C%' ORDER BY DateOfIssue DESC LIMIT 1".format(isbn,bookcopy)
        cursor.execute(sql)
        result = cursor.fetchone()
        self.name = result[0]
        self.lostdamagedbooklastuser.config(state=NORMAL)
        self.lostdamagedbooklastuser.delete(0,END)
        self.lostdamagedbooklastuser.insert(0,self.name)
        self.lostdamagedbooklastuser.config(state=DISABLED)
        

    def SubmitPenalty(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        
        #Charge the account based on what the faculty enter as $penalty
        sql = "SELECT Penalty FROM StudentFaculty WHERE Username = '{}'".format(self.name)
        cursor.execute(sql)
        res = cursor.fetchone()
        existpen = res[0]
        penalty = int(self.lostdamagedbookpenalty.get())
        newpen = existpen + penalty
        newpen = str(newpen)

        
        sql2 = "UPDATE StudentFaculty SET Penalty = '{}' WHERE Username = '{}'".format(newpen,self.name)
        cursor.execute(sql2)

        #Check if user needs to be disbarred
        sql3 = "UPDATE StudentFaculty SET IsDebarred = 1 WHERE Username = '{}' AND Penalty >= 100".format(self.name)
        cursor.execute(sql3)

class PopUserReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Frequent User Report", bg= "yellow", relief= RAISED)
        l.grid(columnspan= 7,sticky=EW)

        mList = ["","Jan", "Feb"]
        
        LmsMain.connect(self)
        cursor = db.cursor()
        popUser_sql = "(SELECT MONTH(Issues.DateOfIssue) as Month, StudentFaculty.Name, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Issues, StudentFaculty WHERE Issues.UserName = StudentFaculty.Username AND MONTH(Issues.DateOfIssue) = '01' AND Issues.IssueID LIKE 'C%' GROUP BY StudentFaculty.Name HAVING NumberOfCheckouts > 9 ORDER BY NumberOfCheckouts DESC LIMIT 5) UNION ALL (SELECT MONTH(Issues.DateOfIssue) as Month, StudentFaculty.Name, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Issues, StudentFaculty WHERE Issues.UserName = StudentFaculty.Username AND MONTH(Issues.DateOfIssue) = '02' AND Issues.IssueID LIKE 'C%' GROUP BY StudentFaculty.Name HAVING NumberOfCheckouts > 9 ORDER BY NumberOfCheckouts DESC LIMIT 5)"
        cursor.execute(popUser_sql)
        rowsP = cursor.fetchall()

        reportFrame = Frame(self)
        reportFrame.grid(row=1, column=1, columnspan=100)
        mE = tk.Entry(reportFrame)
        mE.grid(row= 2, column= 7, columnspan=3, sticky=EW)
        mE.insert(1, "Month")
        mE.config(state=DISABLED)
        self.mE1 = tk.Entry(reportFrame)
        self.mE1.grid(row= 3, column= 7, columnspan=3, sticky=EW)
        self.mE1.insert(0,mList[rowsP[0][0]])
        self.mE1.config(state=DISABLED)
        self.mE2 = tk.Entry(reportFrame)
        self.mE2.grid(row= 4, column= 7, columnspan=3, sticky=EW)
        self.mE2.insert(0,mList[rowsP[1][0]])
        self.mE2.config(state=DISABLED)
        self.mE3 = tk.Entry(reportFrame)
        self.mE3.grid(row= 5, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE3.insert(0,mList[rowsP[2][0]])
        except IndexError:
            pass
        self.mE3.config(state=DISABLED)
        self.mE4 = tk.Entry(reportFrame)
        self.mE4.grid(row= 6, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE4.insert(0,mList[rowsP[3][0]])
        except IndexError:
            pass
        self.mE4.config(state=DISABLED)
        self.mE5 = tk.Entry(reportFrame)
        self.mE5.grid(row= 7, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE5.insert(0,mList[rowsP[4][0]])
        except IndexError:
            pass
        self.mE5.config(state=DISABLED)
        self.mE6 = tk.Entry(reportFrame)
        self.mE6.grid(row= 8, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE6.insert(0,mList[rowsP[5][0]])
        except IndexError:
            pass
        self.mE6.config(state=DISABLED)
        self.mE7 = tk.Entry(reportFrame)
        self.mE7.grid(row= 9, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE7.insert(0,mList[rowsP[6][0]])
        except IndexError:
            pass
        self.mE7.config(state=DISABLED)
        self.mE8 = tk.Entry(reportFrame)
        self.mE8.grid(row= 10, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE8.insert(0,mList[rowsP[7][0]])
        except IndexError:
            pass
        self.mE8.config(state=DISABLED)
        self.mE9 = tk.Entry(reportFrame)
        self.mE9.grid(row= 11, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE9.insert(0,mList[rowsP[8][0]])
        except IndexError:
            pass
        self.mE9.config(state=DISABLED)
        self.mE10 = tk.Entry(reportFrame)
        self.mE10.grid(row= 12, column= 7, columnspan=3, sticky=EW)
        try:
            self.mE10.insert(0,mList[rowsP[9][0]])
        except IndexError:
            pass
        self.mE10.config(state=DISABLED)

        uE = tk.Entry(reportFrame)
        uE.grid(row= 2, column= 11, columnspan=3, sticky=EW)
        uE.insert(1, "User Name")
        uE.config(state=DISABLED)
        self.uE1 = tk.Entry(reportFrame)
        self.uE1.grid(row= 3, column= 11, columnspan=3, sticky=EW)
        self.uE1.insert(1, rowsP[0][1])
        self.uE1.config(state=DISABLED)
        self.uE2 = tk.Entry(reportFrame)
        self.uE2.grid(row= 4, column= 11, columnspan=3, sticky=EW)
        self.uE2.insert(1, rowsP[1][1])
        self.uE2.config(state=DISABLED)
        self.uE3 = tk.Entry(reportFrame)
        self.uE3.grid(row= 5, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE3.insert(0,rowsP[2][1])
        except IndexError:
            pass
        self.uE3.config(state=DISABLED)
        self.uE4 = tk.Entry(reportFrame)
        self.uE4.grid(row= 6, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE4.insert(0,rowsP[3][1])
        except IndexError:
            pass
        self.uE4.config(state=DISABLED)
        self.uE5 = tk.Entry(reportFrame)
        self.uE5.grid(row= 7, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE5.insert(0,rowsP[4][1])
        except IndexError:
            pass
        self.uE5.config(state=DISABLED)
        self.uE6 = tk.Entry(reportFrame)
        self.uE6.grid(row= 8, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE6.insert(0,rowsP[5][1])
        except IndexError:
            pass
        self.uE6.config(state=DISABLED)
        self.uE7 = tk.Entry(reportFrame)
        self.uE7.grid(row= 9, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE7.insert(0,rowsP[6][1])
        except IndexError:
            pass
        self.uE7.config(state=DISABLED)
        self.uE8 = tk.Entry(reportFrame)
        self.uE8.grid(row= 10, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE8.insert(0,rowsP[7][1])
        except IndexError:
            pass
        self.uE8.config(state=DISABLED)
        self.uE9 = tk.Entry(reportFrame)
        self.uE9.grid(row= 11, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE9.insert(0,rowsP[8][1])
        except IndexError:
            pass
        self.uE9.config(state=DISABLED)
        self.uE10 = tk.Entry(reportFrame)
        self.uE10.grid(row= 12, column= 11, columnspan=3, sticky=EW)
        try:
            self.uE10.insert(0,rowsP[9][1])
        except IndexError:
            pass
        self.uE10.config(state=DISABLED)
        

        self.nE = tk.Entry(reportFrame)
        self.nE.grid(row= 2, column= 14, columnspan=3, sticky=EW)
        self.nE.insert(1, "# of Checkouts")
        self.nE.config(state=DISABLED)
        self.nE1 = tk.Entry(reportFrame)
        self.nE1.grid(row= 3, column= 14, columnspan=3, sticky=EW)
        self.nE1.insert(1, rowsP[0][2])
        self.nE1.config(state=DISABLED)
        self.nE2 = tk.Entry(reportFrame)
        self.nE2.grid(row= 4, column= 14, columnspan=3, sticky=EW)
        self.nE2.insert(1, rowsP[1][2])
        self.nE2.config(state=DISABLED)
        self.nE3 = tk.Entry(reportFrame)
        self.nE3.grid(row= 5, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE3.insert(0,rowsP[2][2])
        except IndexError:
            pass
        self.nE3.config(state=DISABLED)
        self.nE4 = tk.Entry(reportFrame)
        self.nE4.grid(row= 6, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE4.insert(0,rowsP[3][2])
        except IndexError:
            pass
        self.nE4.config(state=DISABLED)
        self.nE5 = tk.Entry(reportFrame)
        self.nE5.grid(row= 7, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE5.insert(0,rowsP[4][2])
        except IndexError:
            pass
        self.nE5.config(state=DISABLED)
        self.nE6 = tk.Entry(reportFrame)
        self.nE6.grid(row= 8, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE6.insert(0,rowsP[5][2])
        except IndexError:
            pass
        self.nE6.config(state=DISABLED)
        self.nE7 = tk.Entry(reportFrame)
        self.nE7.grid(row= 9, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE7.insert(0,rowsP[6][2])
        except IndexError:
            pass
        self.nE7.config(state=DISABLED)
        self.nE8 = tk.Entry(reportFrame)
        self.nE8.grid(row= 10, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE8.insert(0,rowsP[7][2])
        except IndexError:
            pass
        self.nE8.config(state=DISABLED)
        self.nE9 = tk.Entry(reportFrame)
        self.nE9.grid(row= 11, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE9.insert(0,rowsP[8][2])
        except IndexError:
            pass
        self.nE9.config(state=DISABLED)
        self.nE10 = tk.Entry(reportFrame)
        self.nE10.grid(row= 12, column= 14, columnspan=3, sticky=EW)
        try:
            self.nE10.insert(0,rowsP[9][2])
        except IndexError:
            pass
        self.nE10.config(state=DISABLED)

        Button(self, text="Back", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=14, column=7)


class PopBookReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Popular Book Report", bg= "yellow", relief= RAISED)
        l.grid(columnspan= 7,sticky=EW)
        
        LmsMain.connect(self)
        cursor = db.cursor()
        popBook_sql = "(SELECT MONTH(Issues.DateOfIssue) as Month, Book.Title, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Book, Issues WHERE Book.ISBN = Issues.ISBN AND MONTH(Issues.DateOfIssue) = '01' AND Issues.IssueID LIKE 'C%' GROUP BY Book.Title ORDER BY NumberOfCheckouts DESC LIMIT 3) UNION ALL (SELECT MONTH(Issues.DateOfIssue) as Month, Book.Title, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Book, Issues WHERE Book.ISBN = Issues.ISBN AND MONTH(Issues.DateOfIssue) = '02' AND Issues.IssueID LIKE 'C%' GROUP BY Book.Title ORDER BY NumberOfCheckouts DESC LIMIT 3)"
        cursor.execute(popBook_sql)
        rowsP = cursor.fetchall()

        reportFrame = Frame(self)
        reportFrame.grid(row=1, column=1, columnspan=100)
        mE = tk.Entry(reportFrame)
        mE.grid(row= 2, column= 7, columnspan=3, sticky=EW)
        mE.insert(1, "Month")
        mE.config(state=DISABLED)
        self.mE1 = tk.Entry(reportFrame)
        self.mE1.grid(row= 3, column= 7, columnspan=3, sticky=EW)
        self.mE1.insert(0,"Jan")
        self.mE1.config(state=DISABLED)
        self.mE2 = tk.Entry(reportFrame)
        self.mE2.grid(row= 4, column= 7, columnspan=3, sticky=EW)
        self.mE3 = tk.Entry(reportFrame)
        self.mE3.grid(row= 5, column= 7, columnspan=3, sticky=EW)
        self.mE4 = tk.Entry(reportFrame)
        self.mE4.grid(row= 6, column= 7, columnspan=3, sticky=EW)
        self.mE4.insert(0,"Feb")
        self.mE4.config(state=DISABLED)
        self.mE5 = tk.Entry(reportFrame)
        self.mE5.grid(row= 7, column= 7, columnspan=3, sticky=EW)
        self.mE5 = tk.Entry(reportFrame)
        self.mE5.grid(row= 8, column= 7, columnspan=3, sticky=EW)
        self.mE5.config(state=DISABLED)    

        tE = tk.Entry(reportFrame)
        tE.grid(row= 2, column= 11, columnspan=3, sticky=EW)
        tE.insert(1, "Title")
        tE.config(state=DISABLED)
        self.tE1 = tk.Entry(reportFrame)
        self.tE1.grid(row= 3, column= 11, columnspan=3, sticky=EW)
        self.tE1.insert(1, rowsP[0][1])
        self.tE1.config(state=DISABLED)
        self.tE2 = tk.Entry(reportFrame)
        self.tE2.grid(row= 4, column= 11, columnspan=3, sticky=EW)
        self.tE2.insert(1, rowsP[1][1])
        self.tE2.config(state=DISABLED)
        self.tE3 = tk.Entry(reportFrame)
        self.tE3.grid(row= 5, column= 11, columnspan=3, sticky=EW)
        self.tE3.insert(1, rowsP[2][1])
        self.tE3.config(state=DISABLED)
        self.tE4 = tk.Entry(reportFrame)
        self.tE4.grid(row= 6, column= 11, columnspan=3, sticky=EW)
        self.tE4.insert(1, rowsP[3][1])
        self.tE4.config(state=DISABLED)
        self.tE5 = tk.Entry(reportFrame)
        self.tE5.grid(row= 7, column= 11, columnspan=3, sticky=EW)
        self.tE5.insert(1, rowsP[4][1])
        self.tE5.config(state=DISABLED)
        self.tE6 = tk.Entry(reportFrame)
        self.tE6.grid(row= 8, column= 11, columnspan=3, sticky=EW)
        self.tE6.insert(1, rowsP[5][1])
        self.tE6.config(state=DISABLED)

        self.nE = tk.Entry(reportFrame)
        self.nE.grid(row= 2, column= 14, columnspan=3, sticky=EW)
        self.nE.insert(1, "# of Checkouts")
        self.nE.config(state=DISABLED)
        self.nE1 = tk.Entry(reportFrame)
        self.nE1.grid(row= 3, column= 14, columnspan=3, sticky=EW)
        self.nE1.insert(1, rowsP[0][2])
        self.nE1.config(state=DISABLED)
        self.nE2 = tk.Entry(reportFrame)
        self.nE2.grid(row= 4, column= 14, columnspan=3, sticky=EW)
        self.nE2.insert(1, rowsP[1][2])
        self.nE2.config(state=DISABLED)
        self.nE3 = tk.Entry(reportFrame)
        self.nE3.grid(row= 5, column= 14, columnspan=3, sticky=EW)
        self.nE3.insert(1, rowsP[2][2])
        self.nE3.config(state=DISABLED)
        self.nE4 = tk.Entry(reportFrame)
        self.nE4.grid(row= 6, column= 14, columnspan=3, sticky=EW)
        self.nE4.insert(1, rowsP[3][2])
        self.nE4.config(state=DISABLED)
        self.nE4.config(state=DISABLED)
        self.nE5 = tk.Entry(reportFrame)
        self.nE5.grid(row= 7, column= 14, columnspan=3, sticky=EW)
        self.nE5.insert(1, rowsP[4][2])
        self.nE5.config(state=DISABLED)
        self.nE6 = tk.Entry(reportFrame)
        self.nE6.grid(row= 8, column= 14, columnspan=3, sticky=EW)
        self.nE6.insert(1, rowsP[5][2])
        self.nE6.config(state=DISABLED)

        Button(self, text="Back", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=9, column=7)


class PopSubReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Popular Subject Report", bg= "yellow", relief= RAISED)
        l.grid(columnspan= 7,sticky=EW)
        
        LmsMain.connect(self)
        cursor = db.cursor()
        pop_sql = "(SELECT MONTH(Issues.DateOfIssue) AS Month, Book.Subject, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Issues, Book WHERE Issues.ISBN = Book.ISBN and MONTH(Issues.DateOfIssue) = '01' AND Issues.IssueID LIKE 'C%' GROUP BY Book.Subject ORDER BY NumberOfCheckouts DESC LIMIT 3) UNION ALL (SELECT MONTH(Issues.DateOfIssue) AS Month, Book.Subject, COUNT(Issues.IssueID) as NumberOfCheckouts FROM Issues, Book WHERE Issues.ISBN = Book.ISBN and MONTH(Issues.DateOfIssue) = '02' AND Issues.IssueID LIKE 'C%' GROUP BY Book.Subject ORDER BY NumberOfCheckouts DESC LIMIT 3)"
        cursor.execute(pop_sql)
        rowsP = cursor.fetchall()

        reportFrame = Frame(self)
        reportFrame.grid(row=1, column=1, columnspan=100)
        mE = tk.Entry(reportFrame)
        mE.grid(row= 2, column= 7, columnspan=3, sticky=EW)
        mE.insert(1, "Month")
        mE.config(state=DISABLED)
        self.mE1 = tk.Entry(reportFrame)
        self.mE1.grid(row= 3, column= 7, columnspan=3, sticky=EW)
        self.mE1.insert(0,"Jan")
        self.mE1.config(state=DISABLED)
        self.mE2 = tk.Entry(reportFrame)
        self.mE2.grid(row= 4, column= 7, columnspan=3, sticky=EW)
        self.mE3 = tk.Entry(reportFrame)
        self.mE3.grid(row= 5, column= 7, columnspan=3, sticky=EW)
        self.mE4 = tk.Entry(reportFrame)
        self.mE4.grid(row= 6, column= 7, columnspan=3, sticky=EW)
        self.mE4.insert(0,"Feb")
        self.mE4.config(state=DISABLED)
        self.mE5 = tk.Entry(reportFrame)
        self.mE5.grid(row= 7, column= 7, columnspan=3, sticky=EW)
        self.mE5 = tk.Entry(reportFrame)
        self.mE5.grid(row= 8, column= 7, columnspan=3, sticky=EW)
        self.mE5.config(state=DISABLED)    

        sE = tk.Entry(reportFrame)
        sE.grid(row= 2, column= 11, columnspan=3, sticky=EW)
        sE.insert(1, "Top Subject")
        sE.config(state=DISABLED)
        self.sE1 = tk.Entry(reportFrame)
        self.sE1.grid(row= 3, column= 11, columnspan=3, sticky=EW)
        self.sE1.insert(1, rowsP[0][1])
        self.sE1.config(state=DISABLED)
        self.sE2 = tk.Entry(reportFrame)
        self.sE2.grid(row= 4, column= 11, columnspan=3, sticky=EW)
        self.sE2.insert(1, rowsP[1][1])
        self.sE2.config(state=DISABLED)
        self.sE3 = tk.Entry(reportFrame)
        self.sE3.grid(row= 5, column= 11, columnspan=3, sticky=EW)
        self.sE3.insert(1, rowsP[2][1])
        self.sE3.config(state=DISABLED)
        self.sE4 = tk.Entry(reportFrame)
        self.sE4.grid(row= 6, column= 11, columnspan=3, sticky=EW)
        self.sE4.insert(1, rowsP[3][1])
        self.sE4.config(state=DISABLED)
        self.sE5 = tk.Entry(reportFrame)
        self.sE5.grid(row= 7, column= 11, columnspan=3, sticky=EW)
        self.sE5.insert(1, rowsP[4][1])
        self.sE5.config(state=DISABLED)
        self.sE6 = tk.Entry(reportFrame)
        self.sE6.grid(row= 8, column= 11, columnspan=3, sticky=EW)
        self.sE6.insert(1, rowsP[5][1])
        self.sE6.config(state=DISABLED)

        self.nE = tk.Entry(reportFrame)
        self.nE.grid(row= 2, column= 14, columnspan=3, sticky=EW)
        self.nE.insert(1, "# of Checkouts")
        self.nE.config(state=DISABLED)
        self.nE1 = tk.Entry(reportFrame)
        self.nE1.grid(row= 3, column= 14, columnspan=3, sticky=EW)
        self.nE1.insert(1, rowsP[0][2])
        self.nE1.config(state=DISABLED)
        self.nE2 = tk.Entry(reportFrame)
        self.nE2.grid(row= 4, column= 14, columnspan=3, sticky=EW)
        self.nE2.insert(1, rowsP[1][2])
        self.nE2.config(state=DISABLED)
        self.nE3 = tk.Entry(reportFrame)
        self.nE3.grid(row= 5, column= 14, columnspan=3, sticky=EW)
        self.nE3.insert(1, rowsP[2][2])
        self.nE3.config(state=DISABLED)
        self.nE4 = tk.Entry(reportFrame)
        self.nE4.grid(row= 6, column= 14, columnspan=3, sticky=EW)
        self.nE4.insert(1, rowsP[3][2])
        self.nE4.config(state=DISABLED)
        self.nE4.config(state=DISABLED)
        self.nE5 = tk.Entry(reportFrame)
        self.nE5.grid(row= 7, column= 14, columnspan=3, sticky=EW)
        self.nE5.insert(1, rowsP[4][2])
        self.nE5.config(state=DISABLED)
        self.nE6 = tk.Entry(reportFrame)
        self.nE6.grid(row= 8, column= 14, columnspan=3, sticky=EW)
        self.nE6.insert(1, rowsP[5][2])
        self.nE6.config(state=DISABLED)

        Button(self, text="Back", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=9, column=7)

class DamagedBookReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        l = tk.Label(self, text = "Damaged Book Report", bg= "yellow", relief= RAISED)
        l.grid(columnspan= 7,sticky=EW)

        tk.Label(self, text= "Month").grid(row=2, column= 1)
        self.monthVar = IntVar()
        monthLst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.monthVar.set(1)
        OptionMenu(self, self.monthVar, *monthLst).grid(row=2, column=2, sticky= W)

        tk.Label(self, text= "Subject 1").grid(row=2, column= 4)
        self.sub1Var = StringVar()
        subList = ["Math", "History", "English", "Physics"]
        self.sub1Var.set("Math")
        OptionMenu(self, self.sub1Var, *subList).grid(row=2, column=5)

        tk.Label(self, text= "Subject 2").grid(row=3, column= 4)
        self.sub2Var = StringVar()
        self.sub2Var.set("English")
        OptionMenu(self, self.sub2Var, *subList).grid(row=3, column=5)

        tk.Label(self, text= "Subject 3").grid(row=4, column=4)
        self.sub3Var = StringVar()
        self.sub3Var.set("Science")
        OptionMenu(self, self.sub3Var, *subList).grid(row=4, column=5)

        Button(self, text="Show Report", command= self.showDamage).grid(row=5, column=3)

        reportFrame = Frame(self)
        reportFrame.grid(row=1, column=15, columnspan=100)
        mE = tk.Entry(reportFrame)
        mE.grid(row= 2, column= 7, columnspan=3, sticky=EW)
        mE.insert(1, "Month")
        mE.config(state=DISABLED)
        mE1 = tk.Entry(reportFrame)
        mE1.grid(row= 3, column= 7, columnspan=3, sticky=EW)
        mE1.config(state=DISABLED)
        mE2 = tk.Entry(reportFrame)
        mE2.grid(row= 4, column= 7, columnspan=3, sticky=EW)
        mE2.config(textvariable = self.monthVar)
        mE3 = tk.Entry(reportFrame)
        mE3.grid(row= 5, column= 7, columnspan=3, sticky=EW)
        mE3.config(state=DISABLED)

        sE = tk.Entry(reportFrame)
        sE.grid(row= 2, column= 11, columnspan=3, sticky=EW)
        sE.insert(1, "Subject")
        sE.config(state=DISABLED)
        sE1 = tk.Entry(reportFrame)
        sE1.grid(row= 3, column= 11, columnspan=3, sticky=EW)
        sE1.config(textvariable = self.sub1Var)
        sE2 = tk.Entry(reportFrame)
        sE2.grid(row= 4, column= 11, columnspan=3, sticky=EW)
        sE2.config(textvariable = self.sub2Var)
        sE3 = tk.Entry(reportFrame)
        sE3.grid(row= 5, column= 11, columnspan=3, sticky=EW)
        sE3.config(textvariable = self.sub3Var)

        self.nE = tk.Entry(reportFrame)
        self.nE.grid(row= 2, column= 14, columnspan=3, sticky=EW)
        self.nE.insert(1, "# of Checkouts")
        self.nE1 = tk.Entry(reportFrame)
        self.nE1.grid(row= 3, column= 14, columnspan=3, sticky=EW)
        self.nE2 = tk.Entry(reportFrame)
        self.nE2.grid(row= 4, column= 14, columnspan=3, sticky=EW)
        self.nE3 = tk.Entry(reportFrame)
        self.nE3.grid(row= 5, column= 14, columnspan=3, sticky=EW)
        Button(self, text="Back", command= lambda: controller.show_frame(SearchBooksPage)).grid(row=7, column=7)


    def showDamage(self):
        LmsMain.connect(self)
        cursor = db.cursor()
        damage_sql = "SELECT Book.Subject, COUNT(BookCopy.ISBN) AS damagedCount, MONTH(Issues.DateOfIssue) as Month FROM Book NATURAL JOIN BookCopy NATURAL JOIN Issues WHERE (Book.Subject = %s OR Book.Subject = %s OR Book.Subject = %s) AND Book.ISBN = BookCopy.ISBN AND Book.ISBN = Issues.ISBN AND MONTH(Issues.DateOfIssue) = %s AND BookCopy.IsDamaged = 1 GROUP BY Book.Subject"
        cursor.execute(damage_sql, (self.sub1Var.get(), self.sub2Var.get(), self.sub3Var.get(), self.monthVar.get()))
        rowsD = cursor.fetchall()

        self.nE1.delete(0,'end')
        self.nE2.delete(0,'end')
        self.nE3.delete(0,'end')
        
        try:
            self.nE1.insert(0,rowsD[0][1])
        except IndexError:
            pass

        try:
            self.nE2.insert(0,rowsD[1][1])
        except IndexError:
            pass
        
        try:
            self.nE3.insert(0,rowsD[2][1])
        except IndexError:
            pass
        


app = LmsMain()
app.mainloop()