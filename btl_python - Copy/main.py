import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from index import show_index
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def ketnoi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="quanlybanve"
    )

def verify(code):
    if not code:
        return "Mã xác nhận không hợp lệ", 400

    con = ketnoi()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM taikhoan WHERE verification_code=%s", (code,))
        result = cur.fetchone()
        if result:
            cur.execute("UPDATE taikhoan SET verified=%s WHERE verification_code=%s", (True, code))
            con.commit()
            return "Tài khoản của bạn đã được xác nhận thành công!"
        else:
            return "Mã xác nhận không hợp lệ", 400
    except mysql.connector.Error as err:
        return f"Lỗi kết nối tới cơ sở dữ liệu: {err}", 500
    finally:
        con.close()



def generate_verification_code(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_verification_email(receiver_email, code, sender_email, sender_password):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Xác nhận đăng ký tài khoản"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Mã xác nhận của bạn là: {code}"
    html = f"""
    <html>
    <body style="margin: 0;font-family: Arial, Helvetica, sans-serif;">
        <div style="background-image: linear-gradient( 109.6deg, rgba(156,252,248,1) 11.2%, rgba(110,123,251,1) 91.1% ); ;height: 500px;background-position: center; background-repeat: no-repeat;
          position: relative;">
            <img src="../logo1.png" alt="">
            <div style=" text-align: center;position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%); padding: 120px;border-radius: 10px;">
                <h1 style="font-size:30px; color: rgb(248, 248, 248);">Mã Đăng Ký Công Ty</h1>
                <h1 style="color: rgb(255, 11, 11);"><span style="color: rgb(100, 102, 101);">MR.</span>QK</h1>
                <br>
                <h3 style="background-color: rgb(255, 255, 255,0.8); display: inline; padding: 6px 16px;border-radius: 10px; color: rgb(105, 107, 107);">{code}</h3>
            </div>
        </div>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return code
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
        return None

def dangky_taikhoan(dangnhap_window, input_tk_dk, input_mk_dk, input_email_dk, input_maEmail_dk):
    dk_tk = input_tk_dk.get()
    dk_mk = input_mk_dk.get()
    dk_email = input_email_dk.get()
    dk_maemail = input_maEmail_dk.get()

    if not dk_tk or not dk_mk or not dk_email or not dk_maemail:
        messagebox.showerror("Thông báo", "Vui lòng điền đầy đủ thông tin!")
        return
    if len(dk_tk) < 10:
        messagebox.showerror("Thông báo", "Tài khoản phải có ít nhất 10 ký tự")
        return
    if len(dk_mk) < 5:
        messagebox.showerror("Thông báo", "Mật Khẩu phải có ít nhất 5 ký tự")
        return
    if not dk_mk[0].isupper():
        messagebox.showerror("Thông báo", "Mật Khẩu phải bắt đầu bằng chữ cái viết hoa")
        return
    if not re.search(r'[A-Za-z]', dk_mk) or not re.search(r'\d', dk_mk):
        messagebox.showerror("Thông báo", "Mật Khẩu phải chứa cả chữ và số")
        return
    if not dk_email.endswith("@gmail.com"):
        messagebox.showerror("Thông báo", "Email phải có đuôi @gmail.com!")
        return

    con = ketnoi()
    cur = con.cursor()
    try:
        cur.execute("SELECT tk FROM taikhoan WHERE tk = %s", (dk_tk,))
        result_tk = cur.fetchone()
        if result_tk:
            messagebox.showerror("Thông báo", "Tài khoản đã tồn tại!")
            return

        cur.execute("SELECT email FROM taikhoan WHERE email = %s", (dk_email,))
        result_email = cur.fetchone()
        if result_email:
            messagebox.showerror("Thông báo", "Email đã tồn tại!")
            return

        verification_code = generate_verification_code()

        if send_verification_email(dk_email, verification_code, dk_email, dk_maemail):
            show_verification_code_input(dk_tk, dk_mk, dk_email, verification_code,dk_maemail, dangnhap_window)
        else:
            messagebox.showerror("Lỗi", "Lỗi khi gửi email xác nhận. Vui lòng thử lại.")
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Lỗi kết nối tới cơ sở dữ liệu: {err}")
    finally:
        con.close()

def show_verification_code_input(dk_tk, dk_mk, dk_email, verification_code,dk_maEmail, dangnhap_window):
    code_input_window = Toplevel()
    code_input_window.title("Nhập mã xác nhận")
    code_input_window.geometry("300x200")
    center_window(code_input_window, 300, 200)

    lbl_instruction = Label(code_input_window, text="Nhập mã xác nhận đã gửi đến email của bạn:")
    lbl_instruction.pack(pady=20)

    input_code = Entry(code_input_window, width=30)
    input_code.pack(pady=10)

    def confirm_code():
        entered_code = input_code.get()
        if entered_code == verification_code:
            try:
                con = ketnoi()
                cur = con.cursor()
                cur.execute("INSERT INTO taikhoan (email, tk, mk, verified, verification_code,mkEmail) VALUES (%s,%s, %s, %s, %s, %s)",
                            (dk_email, dk_tk, dk_mk, True, verification_code,dk_maEmail))
                con.commit()
                messagebox.showinfo("Thông báo", "Tài khoản của bạn đã được xác nhận thành công!")
                code_input_window.destroy()
                dangnhap_window.deiconify()  # Mở lại cửa sổ đăng nhập
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi kết nối tới cơ sở dữ liệu: {err}")
            finally:
                con.close()
        else:
            messagebox.showerror("Lỗi", "Mã xác nhận không đúng!")

    btn_confirm = Button(code_input_window, text="Xác nhận", command=confirm_code)
    btn_confirm.pack(pady=10)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def dangky_window(dangnhap_window):
    dangnhap_window.withdraw()
    dangnhap_window.withdraw()
    dangky = Toplevel()
    dangky.title('Đăng ký')
    dangky.geometry('700x500')
    center_window(dangky, 700, 500)

    image_dk = Image.open("img/backgroud.jpg")
    background_image_dk = ImageTk.PhotoImage(image_dk)
    canvas_dk = Canvas(dangky, width=dangky.winfo_screenwidth(), height=dangky.winfo_screenheight())
    canvas_dk.pack(fill=BOTH, expand=YES)

    def resize_image_dk(event):
        new_width = event.width
        new_height = event.height
        resized_image_dk = image_dk.resize((new_width, new_height), Image.LANCZOS)
        background_image_resized_dk = ImageTk.PhotoImage(resized_image_dk)
        canvas_dk.create_image(0, 0, anchor=NW, image=background_image_resized_dk)
        canvas_dk.image = background_image_resized_dk

    canvas_dk.bind("<Configure>", resize_image_dk)

    frame_dk = Frame(dangky, bg="white", width=400, height=400)
    frame_dk.place(relx=0.5, rely=0.5, anchor=CENTER)

    lb_dk = Label(frame_dk, text="Đăng Ký", fg="gray", font=("Arial", 20, "bold"), bg='White')
    lb_dk.place(x=150, y=30)

    lb_tk_dk = Label(frame_dk, text="Tài Khoản", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_tk_dk.place(x=50, y=100)

    lb_mk_dk = Label(frame_dk, text="Mật Khẩu", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_mk_dk.place(x=50, y=160)

    lb_email_dk = Label(frame_dk, text="Email", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_email_dk.place(x=50, y=220)

    lb_maEmail_dk = Label(frame_dk, text="Mật khẩu ứng dụng (email)", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_maEmail_dk.place(x=50, y=280)
    # Thêm thông báo lỗi động
    error_tk_dk = Label(frame_dk, text="", fg="red", font=("Arial", 8, "italic"), bg='White')
    error_tk_dk.place(x=150, y=130)

    error_mk_dk = Label(frame_dk, text="", fg="red", font=("Arial", 8, "italic"), bg='White')
    error_mk_dk.place(x=150, y=190)

    error_email_dk = Label(frame_dk, text="", fg="red", font=("Arial", 8, "italic"), bg='White')
    error_email_dk.place(x=150, y=250)

    def validate_tk_dk(*args):
        tk = input_tk_dk.get()
        if len(tk) < 10:
            error_tk_dk.config(text="Tài khoản phải có ít nhất 10 ký tự")
        else:
            error_tk_dk.config(text="")

    def validate_mk_dk(*args):
        mk = input_mk_dk.get()
        if mk and not mk[0].isupper():
            error_mk_dk.config(text="Mật Khẩu phải bắt đầu bằng chữ cái viết hoa")
        elif len(mk) < 5:
            error_mk_dk.config(text="Mật Khẩu phải có ít nhất 5 ký tự")
        elif not re.search(r'[A-Za-z]', mk) or not re.search(r'\d', mk):
            error_mk_dk.config(text="Mật Khẩu phải chứa cả chữ và số")
        else:
            error_mk_dk.config(text="")

    def validate_email_dk(*args):
        email = input_email_dk.get()
        if not email.endswith("@gmail.com"):
            error_email_dk.config(text="Email phải có đuôi @gmail.com!")
        else:
            error_email_dk.config(text="")

    def on_enter_tk(e):
        input_tk_dk.delete(0, 'end')

    def on_leave_tk(e):
        name = input_tk_dk.get()
        if name == '':
            input_tk_dk.insert(0, 'Tài Khoản')
        validate_tk_dk()

    input_tk_dk = Entry(frame_dk, fg="gray", font=("Arial", 12), highlightbackground="light blue", highlightthickness=1,
                        borderwidth=0)
    input_tk_dk.place(x=150, y=100)
    input_tk_dk.insert(0, "Tài Khoản")
    input_tk_dk.bind('<FocusIn>', on_enter_tk)
    input_tk_dk.bind('<FocusOut>', on_leave_tk)
    input_tk_dk.bind('<KeyRelease>', validate_tk_dk)

    def on_enter_mk(e):
        input_mk_dk.delete(0, 'end')

    def on_leave_mk(e):
        name = input_mk_dk.get()
        if name == '':
            input_mk_dk.insert(0, 'Mật Khẩu')
        validate_mk_dk()

    input_mk_dk = Entry(frame_dk, fg="gray", font=("Arial", 12), highlightbackground="light blue", show="*",
                        highlightthickness=1, borderwidth=0)
    input_mk_dk.place(x=150, y=160)
    input_mk_dk.insert(0, "Mật Khẩu")
    input_mk_dk.bind('<FocusIn>', on_enter_mk)
    input_mk_dk.bind('<FocusOut>', on_leave_mk)
    input_mk_dk.bind('<KeyRelease>', validate_mk_dk)

    def on_enter_email(e):
        input_email_dk.delete(0, 'end')

    def on_leave_email(e):
        name = input_email_dk.get()
        if name == '':
            input_email_dk.insert(0, 'x@gmail.com')
        validate_email_dk()

    input_email_dk = Entry(frame_dk, fg="gray", font=("Arial", 12), highlightbackground="light blue",
                           highlightthickness=1, borderwidth=0)
    input_email_dk.place(x=150, y=220)
    input_maEmail_dk = Entry(frame_dk, fg="gray", font=("Arial", 12), highlightbackground="light blue",
                           highlightthickness=1, borderwidth=0)
    input_maEmail_dk.place(x=150, y=280)
    input_email_dk.insert(0, "x@gmail.com")
    input_email_dk.bind('<FocusIn>', on_enter_email)
    input_email_dk.bind('<FocusOut>', on_leave_email)
    input_email_dk.bind('<KeyRelease>', validate_email_dk)

    def hienthi_mk_dk():
        if input_mk_dk["show"] == "*":
            input_mk_dk.config(show="")
        else:
            input_mk_dk.config(show="*")

    anh_dk = Image.open("img/iconmk.webp")
    size_dk = anh_dk.resize((20, 10), Image.LANCZOS)
    img_dk = ImageTk.PhotoImage(size_dk)

    btn_mat_dk = Button(frame_dk, image=img_dk, command=hienthi_mk_dk, highlightbackground="black",
                        highlightthickness=1, borderwidth=0)
    btn_mat_dk.place(x=310, y=250)

    btn_dangnhap_dk = Button(frame_dk, text="Đăng ký", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=30,
                             pady=3, borderwidth=0,
                             command=lambda: dangky_taikhoan(dangnhap_window, input_tk_dk, input_mk_dk, input_email_dk,input_maEmail_dk))
    btn_dangnhap_dk.place(x=50, y=340)

    btn_huy_dk = Button(frame_dk, text="Hủy", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=46, pady=3,
                        borderwidth=0,  command=lambda: [dangky.destroy(), dangnhap_window.deiconify()])
    btn_huy_dk.place(x=215, y=340)
    dangky.protocol("WM_DELETE_WINDOW", lambda: (dangnhap_window.deiconify(), dangky.destroy()))
    def on_cancel(window, dangnhap_window):
        window.destroy()
        dangnhap_window.deiconify()

    dangky.mainloop()


def send_login_email(receiver_email, code, sender_email, sender_password):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Xác nhận đăng nhập tài khoản"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Mã xác nhận của bạn là: {code}"

    html = f"""
    <html>
    <body style="margin: 0;font-family: Arial, Helvetica, sans-serif;">
        <div style="background-image: linear-gradient( 109.6deg, rgba(156,252,248,1) 11.2%, rgba(110,123,251,1) 91.1% ); ;height: 500px;background-position: center; background-repeat: no-repeat;
          position: relative;">
            <img src="../logo1.png" alt="">
            <div style=" text-align: center;position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%); padding: 120px;border-radius: 10px;">
                <h1 style="font-size:30px; color: rgb(248, 248, 248);">Mã Đăng Nhập Công Ty</h1>
                <h1 style="color: rgb(255, 11, 11);"><span style="color: rgb(100, 102, 101);">MR.</span>QK</h1>
                <br>
                <h3 style="background-color: rgb(255, 255, 255,0.8); display: inline; padding: 6px 16px;border-radius: 10px; color: rgb(105, 107, 107);">{code}</h3>
            </div>
        </div>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return code
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
        return None

def login(input_tk, input_mk):
    taikhoan = input_tk.get()
    matkhau = input_mk.get()

    if not taikhoan or not matkhau:
        messagebox.showerror("Thông báo", "Tên đăng nhập và mật khẩu không được để trống!")
        return

    try:
        con = ketnoi()
        cur = con.cursor()
        cur.execute("SELECT email, mkEmail FROM taikhoan WHERE tk=%s AND mk=%s", (taikhoan, matkhau))
        result = cur.fetchone()
        if result:
            receiver_email = result[0]
            sender_email = result[0]
            sender_password = result[1]
            verification_code = generate_verification_code()
            if send_login_email(receiver_email, verification_code, sender_email, sender_password):
                show_login_code_input(verification_code)
            else:
                messagebox.showerror("Lỗi", "Không thể gửi email xác nhận.")
        else:
            messagebox.showerror("Thông báo", "Sai tên đăng nhập hoặc mật khẩu!")
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Lỗi kết nối tới cơ sở dữ liệu: {err}")
    finally:
        con.close()

def show_login_code_input(expected_code):
    code_input_window = Toplevel()
    code_input_window.title("Nhập mã xác nhận")
    code_input_window.geometry("300x200")
    center_window(code_input_window, 300, 200)
    code_input_window.attributes("-topmost", True)

    lbl_instruction = Label(code_input_window, text="Nhập mã xác nhận đã gửi đến email của bạn:")
    lbl_instruction.pack(pady=20)

    input_code = Entry(code_input_window, width=30)
    input_code.pack(pady=10)

    def confirm_code():
        entered_code = input_code.get()
        if entered_code == expected_code:
            try:
                messagebox.showinfo("Thông báo", "Tài khoản của bạn đã được xác nhận thành công!")
                code_input_window.destroy()
                show_index(dangnhap)
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi kết nối tới cơ sở dữ liệu: {err}")
        else:
            messagebox.showerror("Lỗi", "Mã xác nhận không đúng!")

    btn_confirm = Button(code_input_window, text="Xác nhận", command=confirm_code)
    btn_confirm.pack(pady=10)

if __name__ == "__main__":
    dangnhap = Tk()
    dangnhap.title('Đăng nhập')
    dangnhap.geometry('700x400')
    center_window(dangnhap, 700, 400)
    dangnhap.attributes("-topmost", True)

    image = Image.open("img/backgroud.jpg")
    background_image = ImageTk.PhotoImage(image)

    canvas = Canvas(dangnhap, width=dangnhap.winfo_screenwidth(), height=dangnhap.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=YES)


    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        background_image_resized = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=background_image_resized)
        canvas.image = background_image_resized


    canvas.bind("<Configure>", resize_image)

    frame = Frame(dangnhap, bg="white", width=400, height=350)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    lb = Label(frame, text="Đăng Nhập", fg="gray", font=("Arial", 20, "bold"), bg='White')
    lb.place(x=150, y=30)

    lb_tk = Label(frame, text="Tài Khoản", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_tk.place(x=50, y=100)

    lb_mk = Label(frame, text="Mật Khẩu", fg="gray", font=("Arial", 10, "bold"), bg='White')
    lb_mk.place(x=50, y=160)


    def on_enter(e):
        input_tk.delete(0, 'end')


    def on_leave(e):
        name = input_tk.get()
        if name == '':
            input_tk.insert(0, 'Tài Khoản')


    input_tk = Entry(frame, fg="gray", font=("Arial", 12), highlightbackground="light blue", highlightthickness=1,
                     borderwidth=0)
    input_tk.place(x=150, y=100)
    input_tk.insert(0, "Tài Khoản")
    input_tk.bind('<FocusIn>', on_enter)
    input_tk.bind('<FocusOut>', on_leave)


    def on_enter(e):
        input_mk.delete(0, 'end')


    def on_leave(e):
        name = input_mk.get()
        if name == '':
            input_mk.insert(0, 'Mật Khẩu')


    input_mk = Entry(frame, fg="gray", font=("Arial", 12), highlightbackground="light blue", show="*",
                     highlightthickness=1, borderwidth=0)
    input_mk.place(x=150, y=160)
    input_mk.insert(0, "Mật Khẩu")
    input_mk.bind('<FocusIn>', on_enter)
    input_mk.bind('<FocusOut>', on_leave)


    def hienthi_mk():
        if input_mk["show"] == "*":
            input_mk.config(show="")
        else:
            input_mk.config(show="*")


    anh = Image.open("img/iconmk.webp")
    size = anh.resize((20, 10), Image.LANCZOS)
    img = ImageTk.PhotoImage(size)

    btn_mat = Button(frame, image=img, command=hienthi_mk, highlightbackground="black", highlightthickness=1,
                     borderwidth=0)
    btn_mat.place(x=310, y=190)

    btn_dangnhap = Button(frame, text="Đăng nhập", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=30,
                          pady=3, borderwidth=0, command=lambda:login(input_tk,input_mk))
    btn_dangnhap.place(x=50, y=250)

    btn_dangky = Button(frame, text="Đăng ký", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=45, pady=3,
                        borderwidth=0, command=lambda: dangky_window(dangnhap))
    btn_dangky.place(x=215, y=250)

    dangnhap.mainloop()
