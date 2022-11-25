from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql

try:
    import Tkinter as tk
except:
    import tkinter as tk

#자신 localhost에 맞게 수정  
con = mysql.connect(user='root', password='@mysql0056', host='127.0.0.1',port="3307", database='dgu')  

#global variable
s_name = ''
s_phone = ''
s_addr = ''
s_email = ''
s_visit = ''

r_name = ''
r_phone = ''
r_addr = ''

p_name = ''
p_quantity = ''
p_cost = ''
p_size = ''
p_weight = ''

def logincheck(e_name, e_phone, e_mail):
    cursor = con.cursor(buffered=True)
    cursor.execute("select count(*) from users where user_name='"+ e_name.get() + "' and user_phone='"+e_phone.get() + "' and user_email='"+e_mail.get()+"'")
    rows = cursor.fetchall()

    for row in rows:
        if(row[0]==1):
            MessageBox.showinfo("Login Status", "Login Successful")
            app.switch_frame(Reservation)
            print("Logged IN Successfully")
        else:
            MessageBox.showinfo("Login Status", "Login Failed")
            e_name.delete(0, 'end')
            e_phone.delete(0, 'end')
            e_mail.delete(0, 'end')
            
def senderInfo(sender_name,sender_phonenum,sender_addr,sender_email,sender_visit):
    s_name = sender_name
    s_phone = sender_phonenum
    s_addr = sender_addr
    s_email = sender_email
    s_visit = sender_visit
    app.switch_frame(ReservationReceiver)

def receiverInfo(receiver_name,receiver_phonenum,receiver_addr):
    r_name = receiver_name
    r_phone = receiver_phonenum
    r_addr = receiver_addr
    app.switch_frame(ReservationProduct)

def productInfo(product_name,product_quantity ,product_cost ,product_size,product_weight):
    p_name = product_name
    p_quantity = product_quantity
    p_cost = product_cost
    p_size = product_size
    p_weight = product_weight
    enrollReserv()
    app.switch_frame(Complete)

#예약 DB로 전송
def enrollReserv(): 
    cursor = con.cursor(buffered=True)
    print('good')
    #cursor.execute("insert into sender values('"+ e_name.get() + "' and user_phone='"+e_phone.get() + "' and user_email='"+e_mail.get()+"'")
    #rows = cursor.fetchall()

def getSenderAddress():
    pass
             

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class): #화면 전환
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

#화면 레이아웃
        
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="LOGEN Delivery Service Reservations", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Member",font=('bold',10), padx=10,#회원일 경우 로그인 페이지로
                  command=lambda: master.switch_frame(Login)).pack(side="top",pady=10)
        tk.Button(self, text="Non-member",font=('bold',10),padx=10, #비회원일 경우 예약 페이지로
                  command=lambda: master.switch_frame(ReservationSender)).pack(side="top")

class Login(tk.Frame):
    #로그인 확인      
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Login", font=('Helvetica', 18, "bold")).grid(row=0, column=1, sticky="n", pady=10,padx=10)
        #login 입력창
        name = Label(self, text='Enter Name', font=('bold', 10))
        name.grid(row=1, column=1)

        phone = Label(self, text='Enter Phone', font=('bold', 10))
        phone.grid(row=3, column=1)

        email = Label(self, text='Enter Email', font=('bold', 10))
        email.grid(row=5, column=1)

        e_name = Entry(self,width=30)
        e_name.grid(row=2, column=1, pady=10,padx=10)
        
        e_phone = Entry(self,width=30)
        e_phone.grid(row=4, column=1, pady=10,padx=10)

        e_mail = Entry(self,width=30)
        e_mail.grid(row=6, column=1, pady=10,padx=10)

        login_btn = Button(self, text="login", font=("italic", 10), width=20, bg="white", command=lambda:logincheck(e_name, e_phone, e_mail))
        login_btn.grid(row=7, column=1, pady=10,padx=10)


class ReservationSender(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Sender Input", font=('Helvetica', 18, "bold")).grid(row=0, column=1, pady=10,padx=10)
        #input label
        Label(self, text="Name", font=('Helvetica', 14)).grid(row=1, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Mobile", font=('Helvetica', 14)).grid(row=2, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Address", font=('Helvetica', 14)).grid(row=3, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Email", font=('Helvetica', 14)).grid(row=4, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Visit date", font=('Helvetica', 14)).grid(row=5, column=0, sticky=W, pady=10,padx=10)
        #input text
        sender_name = Text(self,height=1,width=40)
        sender_name.grid(row=1, column=1, pady=10, padx=20)
        sender_phonenum = Text(self,height=1,width=40)
        sender_phonenum.grid(row=2, column=1, pady=10, padx=20)
        sender_addr = Text(self,height=3,width=40)
        sender_addr.grid(row=3, column=1, pady=10, padx=20)
        sender_email = Text(self,height=1,width=40)
        sender_email.grid(row=4, column=1, pady=10, padx=20)
        sender_visit = Text(self,height=1,width=40)
        sender_visit.grid(row=5, column=1, pady=10, padx=20)
        #get sender address btn
        addr_btn = Button(self, width=15, text='address book', font=('Times', 14), bg="white", command=lambda:getSenderAddress()).grid(row=3,column=3,padx=20);
        #next page btn + sender Info save
        reg_btn = Button(self, width=15, text='next', font=('Times', 14), bg="white",
                         command=lambda:senderInfo(sender_name,sender_phonenum,sender_addr,sender_email,sender_visit)).grid(row=6, column=3, pady=10, padx=10)

class ReservationReceiver(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Receiver Input", font=('Helvetica', 18, "bold")).grid(row=0, column=1, pady=10,padx=10)
        #input label
        Label(self, text="Name", font=('Helvetica', 14)).grid(row=1, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Mobile", font=('Helvetica', 14)).grid(row=2, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Address", font=('Helvetica', 14)).grid(row=3, column=0, sticky=W, pady=10,padx=10)
                #input text
        receiver_name = Text(self,height=1,width=40)
        receiver_name.grid(row=1, column=1, pady=10, padx=20)
        receiver_phonenum = Text(self,height=1,width=40)
        receiver_phonenum.grid(row=2, column=1, pady=10, padx=20)
        receiver_addr = Text(self,height=3,width=40)
        receiver_addr.grid(row=3, column=1, pady=10, padx=20)
        #input btn
        #next page btn + receiver Info save
        reg_btn = Button(self, width=15, text='next', font=('Times', 14), bg="white",
                         command=lambda:receiverInfo(receiver_name,receiver_phonenum,receiver_addr)).grid(row=6, column=3, pady=10, padx=10)


class ReservationProduct(tk.Frame):  
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Product Input", font=('Helvetica', 18, "bold")).grid(row=0, column=1, pady=10,padx=10)
        #input label
        Label(self, text="Name", font=('Helvetica', 14)).grid(row=1, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Quantity", font=('Helvetica', 14)).grid(row=2, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Cost", font=('Helvetica', 14)).grid(row=3, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Size", font=('Helvetica', 14)).grid(row=4, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="Weight", font=('Helvetica', 14)).grid(row=5, column=0, sticky=W, pady=10,padx=10)

        #input text
        product_name = Text(self,height=1,width=40)
        product_name.grid(row=1, column=1, pady=10, padx=20)
        product_quantity = Text(self,height=1,width=40)
        product_quantity.grid(row=2, column=1, pady=10, padx=20)
        product_cost = Text(self,height=1,width=40)
        product_cost.grid(row=3, column=1, pady=10, padx=20)
        product_size = Text(self,height=3,width=40)
        product_size.grid(row=4, column=1, pady=10, padx=20)
        product_weight = Text(self,height=1,width=40)
        product_weight.grid(row=5, column=1, pady=10, padx=20)
        #input btn
        #next page btn + product Info save
        reg_btn = Button(self, width=15, text='submit', font=('Times', 14), bg="white",
                         command=lambda:productInfo(product_name,product_quantity ,product_cost ,product_size,product_weight)).grid(row=6, column=3, pady=10, padx=10)

class Complete(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self, text="Reservation Complete", font=('Helvetica', 18, "bold")).grid(row=0, column=1, pady=10,padx=10)

#실행  
if __name__ == "__main__":
    app = SampleApp()
    app.title("LOGEN")
    app.geometry("900x500")
    app.mainloop()
    
