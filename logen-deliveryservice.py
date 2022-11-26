from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from random import *

try:
    import Tkinter as tk
except:
    import tkinter as tk

#자신 localhost에 맞게 수정  
con = mysql.connect(user='root', password='@mysql0056', host='127.0.0.1',port="3307", database='dgu')  

def isUser(s_name, s_phone, s_email):
    cursor = con.cursor(buffered=True)
    cursor.execute("select count(*) from users where user_name='"+ s_name.get()+ "' and user_phone='"+s_phone.get() + "' and user_email='"+s_email.get()+"'")
    row = cursor.fetchall()
    print(row[0][0])
    if(row[0][0]):
        return True
    else:
        return False


def logincheck(e_name, e_phone, e_mail):
    is_user = isUser(e_name, e_phone, e_mail)
    if(is_user == True):
        MessageBox.showinfo("Login Status", "Login Successful")
        app.switch_frame(ReservationReceiver)
        print("Logged IN Successfully")
    else:
        MessageBox.showinfo("Login Status", "Login Failed")
        e_name.delete(0, 'end')
        e_phone.delete(0, 'end')
        e_mail.delete(0, 'end')


def senderInfo(sender_name,sender_phonenum,sender_addr,sender_email,sender_visit):
    s_name = sender_name.get()
    s_phone = sender_phonenum.get()
    s_addr = sender_addr.get("1.0","end-1c")
    s_email = sender_email.get()
    s_visit = sender_visit.get()
    random_num = randint(10000000, 99999999)
    enrollSender(s_name,s_phone,s_addr,s_email, s_visit, random_num)
    app.switch_frame(Complete)
    

def receiverInfo(receiver_name,receiver_phonenum,receiver_addr):
    r_name = receiver_name.get()
    r_phone = receiver_phonenum.get()
    r_addr = receiver_addr.get("1.0","end-1c")
    enrollReceiver(r_name,r_phone,r_addr)
    app.switch_frame(ReservationProduct)
    

def productInfo(product_name,product_quantity ,product_cost ,product_size,product_weight):
    p_name = product_name.get()
    p_quantity = product_quantity.get()
    p_cost = product_cost.get()
    p_size = product_size.get()
    p_weight = product_weight.get()
    enrollProduct(p_name,p_weight,p_size,p_cost,p_quantity)
    app.switch_frame(ReservationSender)

#예약 DB로 전송
def enrollReceiver(r_name,r_phone,r_addr): 
    cursor = con.cursor(prepared=True)
    cursor.execute("select count(*) from sender")
    rows = cursor.fetchall()
    s_id = rows[0][0] + 1 #다음 sender id

    cursor.execute("select count(*) from receiver")
    rows = cursor.fetchall()
    r_id = rows[0][0] + 101 #다음 receiver id
    #insert receiver table
    cursor.execute("INSERT INTO receiver (receiver_id, receiver_name, receiver_phone, receiver_address) VALUES (" + "'"+str(r_id)+"'," + "'"+r_name+"',"+ "'"+r_phone+"'," + "'"+r_addr+"'" +")")
    con.commit()

def enrollProduct(p_name,p_weight,p_size,p_cost,p_quantity):
    cursor = con.cursor(prepared=True)
    cursor.execute("select count(*) from product")
    rows = cursor.fetchall()
    p_id = rows[0][0] + 1001 #다음 product id 
    #insert productr table
    cursor.execute("INSERT INTO product (product_id, product_name, product_weight, product_size, product_cost, product_quantity) VALUES (" + "'"+str(p_id)+"'," + "'"+p_name+"',"+ "'"+p_weight+"'," + "'"+p_size+"'," + "'"+p_cost+"'," + "'"+p_quantity+"'" +")")
    con.commit()

def enrollSender(s_name, s_phone, s_addr, s_email, s_visit, random_num):
    cursor = con.cursor(prepared=True)
    cursor.execute("select count(*) from product")
    rows = cursor.fetchall()
    p_id = rows[0][0] + 1000 #현재 product id 

    cursor.execute("select count(*) from sender")
    rows = cursor.fetchall()
    s_id = rows[0][0] + 1 #다음 sender id

    cursor.execute("select count(*) from receiver")
    rows = cursor.fetchall()
    r_id = rows[0][0] + 100#현재 receiver id
    
    cursor.execute("select count(*) from reservation")
    rows = cursor.fetchall()
    re_id = rows[0][0] + 1#현재 reservation id
    
    u_id = 1

   #insert sender table
    cursor.execute("INSERT INTO sender (sender_id, receiver_id, product_id, sender_name, sender_phone, sender_address, sender_email) VALUES (" + "'"+str(s_id)+"'," + "'"+str(r_id)+"',"+ "'"+str(p_id)+"'," + "'"+s_name+"'," + "'"+s_phone+"'," + "'"+s_addr+"'," + "'"+s_email+"'" +")")
    con.commit()

    #insert reservation table
    cursor.execute("INSERT INTO reservation (reservation_id, user_id, sender_id, receiver_id, product_id, visiting_date, reservation_number) VALUES (" + "'"+str(re_id)+"'," + "'"+str(u_id)+"',"+ "'"+str(s_id)+"'," + "'"+str(r_id)+"'," + "'"+str(p_id)+"'," + "'"+s_visit+"'," + "'"+str(random_num)+"'" +")")
    con.commit()

    cursor.execute("select * from reservation where reservation_number='"+str(random_num)+"'")
    rows = cursor.fetchall()
    global reservation_num
    reservation_num=rows[0][6]
    print(rows[0][6])

    cursor.execute("select sender_name from sender where sender_id='"+str(s_id)+"'")
    rows = cursor.fetchall()
    global sender_name
    sender_name = rows[0][0]

    cursor.execute("select receiver_name from receiver where receiver_id='"+str(r_id)+"'")
    rows = cursor.fetchall()
    global receiver_name
    receiver_name = rows[0][0]

    cursor.execute("select product_quantity from product where product_id='"+str(p_id)+"'")
    rows = cursor.fetchall()
    global product_quantity
    product_quantity = rows[0][0]

     #visidate
    cursor.execute("select visiting_date from reservation where reservation_id='"+str(re_id)+"'")
    rows = cursor.fetchall()
    global visiting_date
    visiting_date = rows[0][0]
  

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
                  command=lambda: master.switch_frame(ReservationReceiver)).pack(side="top")

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
        sender_name =  Entry(self,width=40)
        sender_name.grid(row=1, column=1, pady=10, padx=20)
        sender_phonenum =  Entry(self,width=40)
        sender_phonenum.grid(row=2, column=1, pady=10, padx=20)
        sender_addr = Text(self,height=3,width=35)
        sender_addr.grid(row=3, column=1, pady=10, padx=20)
        sender_email =  Entry(self,width=40)
        sender_email.grid(row=4, column=1, pady=10, padx=20)
        sender_visit =  Entry(self,width=40)
        sender_visit.grid(row=5, column=1, pady=10, padx=20)
        #next page btn + sender Info save
        reg_btn = Button(self, width=15, text='submit', font=('Times', 14), bg="white",
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
        receiver_name =  Entry(self,width=40)
        receiver_name.grid(row=1, column=1, pady=10, padx=20)
        receiver_phonenum =  Entry(self,width=40)
        receiver_phonenum.grid(row=2, column=1, pady=10, padx=20)
        receiver_addr = Text(self,height=3,width=35)
        receiver_addr.grid(row=3, column=1, pady=10, padx=20)
        #input btn
        #next page btn + receiver Info save
        reg_btn = Button(self, width=15, text='Next', font=('Times', 14), bg="white",
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
        product_name =  Entry(self,width=40)
        product_name.grid(row=1, column=1, pady=10, padx=20)
        product_quantity =  Entry(self,width=40)
        product_quantity.grid(row=2, column=1, pady=10, padx=20)
        product_cost =  Entry(self,width=40)
        product_cost.grid(row=3, column=1, pady=10, padx=20)
        product_size =  Entry(self,width=40)
        product_size.grid(row=4, column=1, pady=10, padx=20)
        product_weight =  Entry(self,width=40)
        product_weight.grid(row=5, column=1, pady=10, padx=20)

        #next page btn + product Info save
        reg_btn = Button(self, width=15, text='Next', font=('Times', 14), bg="white",
                         command=lambda:productInfo(product_name,product_quantity ,product_cost ,product_size,product_weight)).grid(row=6, column=3, pady=10, padx=10)

#reservatioin complete
class Complete(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self, text="Reservation Complete", font=('Helvetica', 18, "bold")).grid(row=0, column=0, pady=10,padx=10)
        Label(self, text="reservation id : "+ str(reservation_num),font=('Helvetica', 14)).grid(row=1, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="sender name : "+ str(sender_name),font=('Helvetica', 14)).grid(row=2, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="receiver name : "+ str(receiver_name),font=('Helvetica', 14)).grid(row=3, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="product quantity : "+ str(product_quantity),font=('Helvetica', 14)).grid(row=4, column=0, sticky=W, pady=10,padx=10)
        Label(self, text="visiting date : "+ str(visiting_date),font=('Helvetica', 14)).grid(row=5, column=0, sticky=W, pady=10,padx=10)

#Run  
if __name__ == "__main__":
    app = SampleApp()
    app.title("LOGEN")
    app.geometry("900x500")
    app.mainloop()
    
