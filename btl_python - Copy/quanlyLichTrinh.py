
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from tkcalendar import DateEntry
import datetime
import database

def show_LichTrinh(frame_noidung):
    for widget in frame_noidung.winfo_children():
        widget.destroy()


    def clear_entries():
        input_ma_tau.delete(0, END)
        input_so_cho_ngoi.delete(0, END)
        input_hang_ghe.delete(0, END)
        input_con_trong.delete(0, END)
        input_timeden_lt.delete(0, END)
        input_ngaykh_ghe.delete(0, END)
        input_ngayden_ghe.delete(0, END)


    def validate_dates(input_ngaykh_ghe, input_ngayden_ghe):
        ngay_kh = input_ngaykh_ghe.get_date()
        ngay_den = input_ngayden_ghe.get_date()
        current_date = datetime.datetime.now().date()

        if ngay_kh < current_date:
            messagebox.showerror("Lỗi", "Ngày khởi hành không được trước ngày hiện tại.")
            return False

        if ngay_den < ngay_kh:
            messagebox.showerror("Lỗi", "Ngày đến phải bằng hoặc sau ngày khởi hành.")
            return False

        return True

    def them_lichtrinh(input_ma_tau, input_so_cho_ngoi, input_hang_ghe, input_con_trong, input_timeden_lt,
                       input_ngaykh_ghe, input_ngayden_ghe, addThem):
        if not validate_dates(input_ngaykh_ghe, input_ngayden_ghe):
            return
        try:
            ma_tau_full = input_ma_tau.get()
            ma_tau = ma_tau_full.split(' ')[0]  # Extract MaTau from the concatenated value
            ga_khoi_hanh = input_so_cho_ngoi.get()
            ga_den = input_hang_ghe.get()
            thoi_gian_khoi_hanh = input_con_trong.get()
            thoi_gian_den = input_timeden_lt.get()
            ngaykh_ghe = input_ngaykh_ghe.get_date().strftime('%Y-%m-%d')  # Convert to string
            ngayden_ghe = input_ngayden_ghe.get_date().strftime('%Y-%m-%d')  # Convert to string

            if thoi_gian_khoi_hanh not in ["01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM",
                                           "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM", "12:00 PM",
                                           "01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", "05:00 AM", "06:00 AM",
                                           "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 AM",
                                           "Khác"]:
                messagebox.showerror("Lỗi", "Chỉ được chọn giờ.")
                return
            if thoi_gian_den not in ["01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM",
                                     "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM", "12:00 PM",
                                     "01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", "05:00 AM", "06:00 AM",
                                     "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 AM", "Khác"]:
                messagebox.showerror("Lỗi", "Chỉ được chọn giờ.")
                return

            # Kiểm tra nếu ga khởi hành và ga đến giống nhau
            if ga_khoi_hanh == ga_den:
                messagebox.showerror("Lỗi", "Ga khởi hành và ga đến không được giống nhau.")
                return

            if database.check_lichtrinh_exist(ma_tau, ga_khoi_hanh, ga_den):
                messagebox.showerror("Lỗi", "Lịch trình này đã tồn tại trong cơ sở dữ liệu.")
                return

            database.them_lichtrinh(ma_tau, ga_khoi_hanh, ga_den, thoi_gian_khoi_hanh, thoi_gian_den, ngaykh_ghe,
                                    ngayden_ghe)
            messagebox.showinfo("Thông báo", "Thêm lịch trình thành công")
            clear_entries()
            display_data()
            addThem.destroy()
        except ValueError as ve:
            messagebox.showerror("Lỗi", str(ve))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def sua_lichtrinh():
        try:
            selected_row = table_cn.focus()
            data = table_cn.item(selected_row, 'values')
            print("Selected Row:", selected_row)
            print("Data:", data)

            if not data:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lịch trình để sửa.")
                return

            ma_chon = data[0]  # Lấy mã lịch trình từ dữ liệu đã chọn
            ma_tau_full = input_ma_tau.get()
            ma_tau_moi = ma_tau_full.split(' ')[0]  # Extract MaTau from the concatenated value
            ga_khoi_hanh_moi = input_so_cho_ngoi.get()
            ga_den_moi = input_hang_ghe.get()
            thoi_gian_khoi_hanh_moi = input_con_trong.get()
            thoi_gian_den_moi = input_timeden_lt.get()
            ngaykh_ghe = input_ngaykh_ghe.get_date().strftime('%Y-%m-%d')  # Convert to string
            ngayden_ghe = input_ngayden_ghe.get_date().strftime('%Y-%m-%d')  # Convert to string

            # Kiểm tra nếu ga khởi hành và ga đến giống nhau
            if ga_khoi_hanh_moi == ga_den_moi:
                messagebox.showerror("Lỗi", "Ga khởi hành và ga đến không được giống nhau.")
                return

            if database.check_lichtrinh_exist(ma_tau_moi, ga_khoi_hanh_moi, ga_den_moi):
                messagebox.showerror("Lỗi", "Lịch trình này đã tồn tại trong cơ sở dữ liệu.")
                return
            # Thực hiện cập nhật thông tin vào database
            database.sua_lichtrinh(ma_chon, ma_tau_moi, ga_khoi_hanh_moi, ga_den_moi, thoi_gian_khoi_hanh_moi,
                                   thoi_gian_den_moi, ngaykh_ghe, ngayden_ghe)

            messagebox.showinfo("Thông báo", "Cập nhật lịch trình thành công")
            clear_entries()
            display_data()

        except IndexError:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lịch trình để sửa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật lịch trình: {str(e)}")

    def update_listbox(event):
        value = input_ma_tau.get().lower()
        if value == '':
            listbox_ma_tau.place_forget()
            return

        new_values = [v for v in ma_tau_values if value in v.lower()]
        listbox_ma_tau.delete(0, tk.END)
        for item in new_values:
            listbox_ma_tau.insert(tk.END, item)

        if new_values:
            input_x = input_ma_tau.winfo_x()
            input_y = input_ma_tau.winfo_y() + input_ma_tau.winfo_height()
            listbox_ma_tau.place(x=input_x, y=input_y, width=input_ma_tau.winfo_width())
            listbox_ma_tau.lift()  # Đưa Listbox lên trên cùng
        else:
            listbox_ma_tau.place_forget()

    def on_listbox_select(event):
        if listbox_ma_tau.curselection():
            selection = listbox_ma_tau.get(listbox_ma_tau.curselection())
            input_ma_tau.set(selection)
            listbox_ma_tau.place_forget()
    def fromThem():
        def center_window(window, width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        addThem = Toplevel()
        addThem.title('Thêm Tàu')
        addThem.geometry('500x600')
        center_window(addThem, 500, 600)
        addThem.transient(frame_noidung.winfo_toplevel())  # Đảm bảo cửa sổ luôn ở trên cùng của ứng dụng chính
        addThem.attributes("-topmost", True)  # Đảm bảo nó trên tất cả các cửa sổ khác
        addThem.focus_force()  # Đặt trọng tâm vào cửa sổ này

        image = Image.open("img/backgroud.jpg")
        global background_image
        background_image = ImageTk.PhotoImage(image)
        canvas = Canvas(addThem, width=addThem.winfo_screenwidth(), height=addThem.winfo_screenheight())
        canvas.pack(fill=BOTH, expand=YES)

        def resize_image(event):
            new_width = event.width
            new_height = event.height
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            global background_image_resized
            background_image_resized = ImageTk.PhotoImage(resized_image)
            canvas.create_image(0, 0, anchor=NW, image=background_image_resized)
            canvas.image = background_image_resized

        canvas.bind("<Configure>", resize_image)
        frame = Frame(addThem, bg="white", width=400, height=500)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        lb = Label(frame, text="Thêm Lịch Trình", fg="gray", font=("Arial", 18, "bold"), bg='White')
        lb.place(x=88, y=10)

        lb_ht = Label(frame, text="Mã Tàu", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_ht.place(x=30, y=70)

        lb_ns = Label(frame, text="Ga Khời Hành", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_ns.place(x=30, y=120)

        lb_sex = Label(frame, text="Ga Đến", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_sex.place(x=30, y=170)

        lb_sdt = Label(frame, text="Thời gian khởi hành", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_sdt.place(x=30, y=220)

        lb_cccd = Label(frame, text="Thời gian Đến", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_cccd.place(x=30, y=270)

        lb_email = Label(frame, text="Ngày Khởi Hành", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_email.place(x=30, y=320)

        lb_diachi = Label(frame, text="Ngày Đến", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_diachi.place(x=30, y=370)

        def update_listbox(event):
            value = input_ma_tau.get().lower()
            if value == '':
                listbox_ma_tau.place_forget()
                return

            new_values = [v for v in ma_tau_values if value in v.lower()]
            listbox_ma_tau.delete(0, tk.END)
            for item in new_values:
                listbox_ma_tau.insert(tk.END, item)

            if new_values:
                input_x = input_ma_tau.winfo_x()
                input_y = input_ma_tau.winfo_y() + input_ma_tau.winfo_height()
                listbox_ma_tau.place(x=input_x, y=input_y, width=input_ma_tau.winfo_width())
                listbox_ma_tau.lift()  # Đưa Listbox lên trên cùng
            else:
                listbox_ma_tau.place_forget()

        def on_listbox_select(event):
            if listbox_ma_tau.curselection():
                selection = listbox_ma_tau.get(listbox_ma_tau.curselection())
                input_ma_tau.set(selection)
                listbox_ma_tau.place_forget()
        # Nhap
        ma_tau_values = ["{} ({}) ({})".format(row[0], row[1], row[2]) for row in database.get_ma_tau()]
        input_ma_tau = ttk.Combobox(frame,values=ma_tau_values ,font=("Arial", 11), width=18)
        input_ma_tau.place(x=150, y=70)
        listbox_ma_tau = tk.Listbox(frame, font=("Arial", 11))

        # Liên kết sự kiện nhập liệu với hàm update_listbox
        input_ma_tau.bind('<KeyRelease>', update_listbox)

        # Liên kết sự kiện chọn mục trong listbox với hàm on_listbox_select
        listbox_ma_tau.bind('<<ListboxSelect>>', on_listbox_select)
        input_so_cho_ngoi = Entry(frame, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                                  borderwidth=0, width=20)
        input_so_cho_ngoi.place(x=150, y=120)

        input_hang_ghe = Entry(frame, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                               borderwidth=0, width=20)
        input_hang_ghe.place(x=150, y=170)

        input_con_trong = ttk.Combobox(frame, font=("Arial", 11), state="readonly",
                                       values=["01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"
                                           , "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM", "12:00 PM"
                                           , "01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", "05:00 AM", "06:00 AM"
                                           , "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 AM"],
                                       width=18)
        input_con_trong.place(x=150, y=220)

        input_timeden_lt = ttk.Combobox(frame, font=("Arial", 11), state="readonly",
                                        values=["01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"
                                            , "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM", "12:00 PM"
                                            , "01:00 AM", "02:00 AM", "03:00 AM", "04:00 AM", "05:00 AM", "06:00 AM"
                                            , "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 AM"],
                                        width=18)
        input_timeden_lt.place(x=150, y=270)

        input_ngaykh_ghe = DateEntry(frame, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                                     borderwidth=0, width=20, state="readonly", date_pattern="dd/mm/yyyy")
        input_ngaykh_ghe.place(x=150, y=320)

        input_ngayden_ghe = DateEntry(frame, font=("Arial", 11), highlightbackground="light blue",
                                      highlightthickness=1,
                                      borderwidth=0, width=20, state="readonly", date_pattern="dd/mm/yyyy")
        input_ngayden_ghe.place(x=150, y=370)

        btn_them = Button(frame, text="Thêm",command=lambda:them_lichtrinh(input_ma_tau,input_so_cho_ngoi,input_hang_ghe,input_con_trong,input_timeden_lt,input_ngaykh_ghe,input_ngayden_ghe,addThem) ,bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=30, pady=3,
                          borderwidth=0)
        btn_them.place(x=50, y=430)

        btn_dangky = Button(frame, text="Hủy", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=45, pady=3,
                            borderwidth=0, command=addThem.destroy)
        btn_dangky.place(x=215, y=430)

        addThem.mainloop()
    def xoa_lichtrinh():
        try:
            selected_row = table_cn.focus()
            data = table_cn.item(selected_row, 'values')
            ma_chon = data[0]
            database.xoa_lichtrinh(ma_chon)
            messagebox.showinfo("Thông báo", "Xóa lịch trình thành công")
            clear_entries()
            display_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa lịch trình: {str(e)}")

    def ChonDuLieuBang(event):
        selected_row = table_cn.focus()
        data = table_cn.item(selected_row, 'values')
        ma_chon = data[0]

        input_ma_tau.set(f"{data[1]} ({data[2]}) ({data[3]})")  # Giả sử input_ma_tau là một StringVar hoặc tương t
        input_so_cho_ngoi.delete(0, tk.END)  # Xóa nội dung hiện tại
        input_so_cho_ngoi.insert(0, data[3])  # Đặt nội dung mới
        input_hang_ghe.delete(0, tk.END)
        input_hang_ghe.insert(0, data[4])
        input_con_trong.set(data[5])
        input_timeden_lt.set(data[6])
        input_ngaykh_ghe.set_date(data[7])  # Giả sử input_ngaykh_ghe là một DateEntry hoặc tương tự
        input_ngayden_ghe.set_date(data[8])  # Giả sử input_ngayden_ghe là một DateEntry hoặc tương tự


    def display_data():
        try:
            rows = database.Hien_Thi_lichtrinh()
            update_table(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {str(e)}")

    def update_table(rows):
        for row in table_cn.get_children():
            table_cn.delete(row)
        for row in rows:
            table_cn.insert("", tk.END, values=row)

    frame_tb = Frame(frame_noidung, bg="White")
    frame_tb.pack(side="top", fill="y")

    frame_chucnang = Frame(frame_noidung, width=300, height=200, bg="White")
    frame_chucnang.pack(side="bottom", fill="both", expand=True)

    frame_timkiem = Frame(frame_tb, bg="White")
    frame_timkiem.pack(side="top", pady=10)

    def update_suggestions(event):
        input_text = input_timkiem_kh.get().strip().lower()
        if input_text == "":
            display_data()  # Hiển thị lại toàn bộ dữ liệu nếu không có chuỗi tìm kiếm
            return

        rows = database.Hien_Thi_lichtrinh()
        filtered_rows = [row for row in rows if
                         input_text in row[3].lower() or input_text in row[
                             4].lower()]  # Lọc dữ liệu theo ga khởi hành và ga đến

        update_table(filtered_rows)
    input_timkiem_kh = ttk.Combobox(frame_timkiem, font=("Arial", 11)
                             , width=30)
    input_timkiem_kh.grid(row=0, column=0, padx=10, pady=10)
    input_timkiem_kh.bind('<KeyRelease>', update_suggestions)

    anh = Image.open("img/icontim.png")
    size = anh.resize((20, 20), Image.LANCZOS)
    global img
    img = ImageTk.PhotoImage(size)
    btn_timkiem_kh = Button(frame_timkiem, image=img, borderwidth=0)
    btn_timkiem_kh.grid(row=0, column=1, padx=(0, 10))

    columns = ("Mã lịch trình", "Mã tàu", "Tên tàu", "Ga khởi hành", "Ga đến", "Thời gian khởi hành", "Thời gian đến", "Ngày Khởi Hành", "Ngày Đến")
    table_cn = ttk.Treeview(frame_tb, columns=columns, show="headings")
    table_cn.heading("Mã lịch trình", text="Mã lịch trình")
    table_cn.heading("Mã tàu", text="Mã tàu")
    table_cn.heading("Tên tàu", text="Tên tàu")
    table_cn.heading("Ga khởi hành", text="Ga khởi hành")
    table_cn.heading("Ga đến", text="Ga đến")
    table_cn.heading("Thời gian khởi hành", text="Thời gian khởi hành")
    table_cn.heading("Thời gian đến", text="Thời gian đến")
    table_cn.heading("Ngày Khởi Hành", text="Ngày Khởi Hành")
    table_cn.heading("Ngày Đến", text="Ngày Đến")
    table_cn.column("Mã lịch trình", minwidth=0, width=50)
    table_cn.column("Mã tàu", minwidth=0, width=50)
    table_cn.column("Tên tàu", minwidth=0, width=80)
    table_cn.column("Ga khởi hành", minwidth=0, width=180)
    table_cn.column("Ga đến", minwidth=0, width=180)
    table_cn.column("Thời gian khởi hành", minwidth=0, width=120)
    table_cn.column("Thời gian đến", minwidth=0, width=120)
    table_cn.column("Ngày Khởi Hành", minwidth=0, width=120)
    table_cn.column("Ngày Đến", minwidth=0, width=120)
    table_cn.pack(fill="both", expand=True)
    for col in columns:
        table_cn.column(col, anchor='center')

    table_cn.bind("<<TreeviewSelect>>", ChonDuLieuBang)
    table_cn.pack(padx=10, pady=10, fill=BOTH, expand=True)


    # Add form to enter data

    ma_chon = None
    display_data()

    btn_them = Button(frame_chucnang, command=fromThem, text="Thêm", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                      bg="#57a1f8", pady=6, padx=45)
    btn_them.place(x=5, y=30)
    btn_sua = Button(frame_chucnang, command=sua_lichtrinh, text="Sửa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_sua.place(x=150, y=30)
    btn_xoa = Button(frame_chucnang, command=xoa_lichtrinh, text="Xóa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_xoa.place(x=290, y=30)

    lb_ma_tau = Label(frame_chucnang, bg="White", text="Mã tàu", fg="black", font=("Arial", 10, "bold"))
    lb_ma_tau.place(x=5, y=70)


    ma_tau_values = ["{} ({}) ({})".format(row[0], row[1], row[2]) for row in database.get_ma_tau()]
    input_ma_tau = ttk.Combobox(frame_chucnang, font=("Arial", 11), values=ma_tau_values, width=18)
    input_ma_tau.place(x=5, y=90)
    listbox_ma_tau = tk.Listbox(frame_chucnang, font=("Arial", 11))

    # Liên kết sự kiện nhập liệu với hàm update_listbox
    input_ma_tau.bind('<KeyRelease>', update_listbox)

    # Liên kết sự kiện chọn mục trong listbox với hàm on_listbox_select
    listbox_ma_tau.bind('<<ListboxSelect>>', on_listbox_select)
    lb_so_cho_ngoi = Label(frame_chucnang, bg="White", text="Ga Khởi Hành", fg="black", font=("Arial", 10, "bold"))
    lb_so_cho_ngoi.place(x=200, y=70)
    input_so_cho_ngoi = Entry(frame_chucnang, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                          borderwidth=0, width=20)
    input_so_cho_ngoi.place(x=200, y=90)

    lb_hang_ghe = Label(frame_chucnang, bg="White", text="Ga Đến", fg="black", font=("Arial", 10, "bold"))
    lb_hang_ghe.place(x=5, y=130)
    input_hang_ghe =  Entry(frame_chucnang, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                          borderwidth=0, width=20)
    input_hang_ghe.place(x=5, y=150)

    lb_con_trong = Label(frame_chucnang, bg="White", text="Thời gian khởi hành", fg="black", font=("Arial", 10, "bold"))
    lb_con_trong.place(x=200, y=130)
    input_con_trong = ttk.Combobox(frame_chucnang, font=("Arial", 11), values=["01:00 PM", "02:00 PM", "03:00 PM","04:00 PM", "05:00 PM", "06:00 PM"
                                                                               ,"07:00 PM", "08:00 PM", "09:00 PM","10:00 PM", "11:00 PM", "12:00 PM"
                                                                               ,"01:00 AM", "02:00 AM", "03:00 AM","04:00 AM", "05:00 AM", "06:00 AM"
                                                                               ,"07:00 AM", "08:00 AM", "09:00 AM","10:00 AM", "11:00 AM", "12:00 AM"], width=18)
    input_con_trong.place(x=200, y=150)

    lb_timeden_lt = Label(frame_chucnang, bg="White", text="Thời gian Đến", fg="black", font=("Arial", 10, "bold"))
    lb_timeden_lt.place(x=395, y=70)
    input_timeden_lt = ttk.Combobox(frame_chucnang, font=("Arial", 11), values=["01:00 PM", "02:00 PM", "03:00 PM","04:00 PM", "05:00 PM", "06:00 PM"
                                                                               ,"07:00 PM", "08:00 PM", "09:00 PM","10:00 PM", "11:00 PM", "12:00 PM"
                                                                               ,"01:00 AM", "02:00 AM", "03:00 AM","04:00 AM", "05:00 AM", "06:00 AM"
                                                                               ,"07:00 AM", "08:00 AM", "09:00 AM","10:00 AM", "11:00 AM", "12:00 AM"], width=18)
    input_timeden_lt.place(x=395, y=90)
    lb_ngaykh_ghe = Label(frame_chucnang, bg="White", text="Ngày Khởi Hành", fg="black", font=("Arial", 10, "bold"))
    lb_ngaykh_ghe.place(x=395, y=130)
    input_ngaykh_ghe =  DateEntry(frame_chucnang, font=("Arial", 11), date_pattern="y-mm-dd", highlightbackground="light blue", highlightthickness=1,
                          borderwidth=0, width=20)
    input_ngaykh_ghe.place(x=395, y=150)

    lb_ngayden_ghe = Label(frame_chucnang, bg="White", text="Ngày Đến", fg="black", font=("Arial", 10, "bold"))
    lb_ngayden_ghe.place(x=590, y=70)
    input_ngayden_ghe = DateEntry(frame_chucnang, font=("Arial", 11), date_pattern="y-mm-dd", highlightbackground="light blue",
                                 highlightthickness=1,
                                 borderwidth=0, width=20)
    input_ngayden_ghe.place(x=590, y=90)



