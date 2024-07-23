from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import database
import re

def show_ChoNgoi(frame_noidung):
    for widget in frame_noidung.winfo_children():
        widget.destroy()

    def clear_entries():
        input_ma_tau.set('')
        input_so_cho_ngoi.delete(0, END)
        input_hang_ghe.set('')
        input_con_trong.set('')

    def ChonDuLieuBang(event):
        selected_row = table_cn.focus()
        data = table_cn.item(selected_row, 'values')
        ma_chon = data[0]
        clear_entries()
        input_ma_tau.set(f"{data[1]} ({data[2]}) ({data[3]})")
        input_so_cho_ngoi.insert(0, data[2])
        input_hang_ghe.set(data[3])
        input_con_trong.set(data[4])

    def search_cn():
        try:
            rows = database.search_cn(input_timkiem_kh.get())
            update_table(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    def them_cn(input_ma_tau,input_so_cho_ngoi,input_hang_ghe,input_con_trong,addThem):
        ma_tau = input_ma_tau.get().split(' ')[0]
        so_cho_ngoi = input_so_cho_ngoi.get()
        hang_ghe = input_hang_ghe.get()
        con_trong = input_con_trong.get()

        if ma_tau == "" or so_cho_ngoi == "" or hang_ghe == "" or con_trong == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
        if hang_ghe not in ["Ghế thường", "Ghế VIP", "Khác"]:
            messagebox.showerror("Lỗi", "Hạng Ghế phải chọn từ danh sách: Ghế thường, Ghế VIP.")
            return
        if con_trong not in ["Có", "Không"]:
            messagebox.showerror("Lỗi", "Chọn trống phải chọn từ danh sách: Có, Không.")
            return
        pattern = r"^C\d{3}$"
        if not re.match(pattern, so_cho_ngoi):
            messagebox.showerror("Lỗi", "Số ghế phải theo định dạng 'Cxxx', ví dụ: 'C001'.")
            return

        try:
            if database.check_ma_tau_and_so_cho_ngoi_exist(ma_tau, so_cho_ngoi):
                messagebox.showerror("Lỗi", f"Số ghế {so_cho_ngoi} đã tồn tại cho mã tàu {ma_tau}.")
                return

            success = database.them_chongoi(ma_tau, so_cho_ngoi, hang_ghe, con_trong)
            if success:
                messagebox.showinfo("Thông báo", f"Đã thêm số ghế {so_cho_ngoi} cho mã tàu {ma_tau}.")
                clear_entries()
                display_data()
                addThem.destroy()
            else:
                messagebox.showerror("Lỗi", "Thêm số ghế không thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    def fromThem():
        def center_window(window, width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        addThem = Toplevel()
        addThem.title('Thêm Khách Hàng')
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
        frame = Frame(addThem, bg="white", width=400, height=330)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)



        lb = Label(frame, text="Thêm Chỗ Ngồi", fg="gray", font=("Arial", 18, "bold"), bg='White')
        lb.place(x=120, y=10)

        lb_ht = Label(frame, text="Mã Tàu", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_ht.place(x=52, y=70)

        lb_ns = Label(frame, text="Số Chỗ Ngồi", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_ns.place(x=52, y=120)

        lb_sex = Label(frame, text="Hạng Ghế", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_sex.place(x=52, y=170)

        lb_sdt = Label(frame, text="Còn Trống", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_sdt.place(x=52, y=220)
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
        input_ma_tau = ttk.Combobox(frame,values=ma_tau_values, font=("Arial", 11), width=18)
        input_ma_tau.place(x=160, y=70)
        listbox_ma_tau = tk.Listbox(frame, font=("Arial", 11))

        # Liên kết sự kiện nhập liệu với hàm update_listbox
        input_ma_tau.bind('<KeyRelease>', update_listbox)

        # Liên kết sự kiện chọn mục trong listbox với hàm on_listbox_select
        listbox_ma_tau.bind('<<ListboxSelect>>', on_listbox_select)
        input_so_cho_ngoi = Entry(frame, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                                  borderwidth=0, width=20)
        input_so_cho_ngoi.place(x=160, y=120)

        input_hang_ghe = ttk.Combobox(frame, font=("Arial", 11), state="readonly", values=["Ghế thường", "Ghế VIP"],
                                      width=18)
        input_hang_ghe.place(x=160, y=170)

        input_con_trong = ttk.Combobox(frame, font=("Arial", 11), state="readonly", values=["Có", "Không"], width=18)
        input_con_trong.place(x=160, y=220)

        btn_them = Button(frame, text="Thêm",command=lambda:them_cn(input_ma_tau,input_so_cho_ngoi,input_hang_ghe,input_con_trong,addThem) ,bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=30, pady=3,
                          borderwidth=0)
        btn_them.place(x=50, y=270)

        btn_dangky = Button(frame, text="Hủy", bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=45, pady=3,
                            borderwidth=0, command=addThem.destroy)
        btn_dangky.place(x=215, y=270)

        addThem.mainloop()

    def sua_cn():
        try:
            selected_row = table_cn.focus()
            data = table_cn.item(selected_row, 'values')
            ma_chon = data[0]
            database.sua_cn(ma_chon, input_ma_tau.get().split(' ')[0], input_so_cho_ngoi.get(), input_hang_ghe.get(), input_con_trong.get())
            messagebox.showinfo("Thông báo", "Cập nhật chỗ ngồi thành công")
            clear_entries()
            display_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật chỗ ngồi: {str(e)}")

    def xoa_cn():
        try:
            selected_row = table_cn.focus()
            data = table_cn.item(selected_row, 'values')
            ma_chon = data[0]
            database.xoa_cn(ma_chon)
            messagebox.showinfo("Thông báo", "Xóa chỗ ngồi thành công")
            clear_entries()
            display_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa chỗ ngồi: {str(e)}")

    def display_data():
        try:
            rows = database.Hien_Thi_CN()
            update_table(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị dữ liệu: {str(e)}")

    def update_table(rows):
        table_cn.delete(*table_cn.get_children())
        for row in rows:
            row = list(row)
            row[4] = "Có" if row[4] == 1 else "Không"
            table_cn.insert("", END, values=row)

    def validate_entries():
        if not input_ma_tau.get():
            messagebox.showerror("Lỗi","Trường 'Mã tàu' không được để trống")
        if not input_so_cho_ngoi.get():
            messagebox.showerror("Lỗi","Trường 'Số chỗ ngồi' không được để trống")
        if not input_hang_ghe.get():
            messagebox.showerror("Lỗi","Trường 'Hạng ghế' không được để trống")
        if not input_con_trong.get():
            messagebox.showerror("Lỗi","Trường 'Còn trống' không được để trống")

    for widget in frame_noidung.winfo_children():
        widget.destroy()

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

        rows = database.Hien_Thi_CN()
        filtered_rows = [row for row in rows if
                         input_text in row[0].lower() or input_text in row[
                             1].lower() or input_text in row[
                             2].lower() or input_text in row[
                             3].lower() or input_text in row[
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
    btn_timkiem_cn = Button(frame_timkiem, image=img, command=search_cn, borderwidth=0)
    btn_timkiem_cn.grid(row=0, column=1, padx=(0, 10))

    columns = ("Mã chỗ ngồi", "Mã tàu", "Số chỗ ngồi", "Hạng ghế", "Còn trống")
    table_cn = ttk.Treeview(frame_tb, columns=columns, show="headings")
    table_cn.heading("Mã chỗ ngồi", text="Mã chỗ ngồi")
    table_cn.heading("Mã tàu", text="Mã tàu")
    table_cn.heading("Số chỗ ngồi", text="Số chỗ ngồi")
    table_cn.heading("Hạng ghế", text="Hạng ghế")
    table_cn.heading("Còn trống", text="Còn trống")
    table_cn.column("Mã chỗ ngồi", minwidth=0, width=200)
    table_cn.column("Mã tàu", minwidth=0, width=200)
    table_cn.column("Số chỗ ngồi", minwidth=0, width=200)
    table_cn.column("Hạng ghế", minwidth=0, width=200)
    table_cn.column("Còn trống", minwidth=0, width=200)
    table_cn.pack(fill="both", expand=True)

    for col in columns:
        table_cn.column(col, anchor='center')

    table_cn.bind("<<TreeviewSelect>>", ChonDuLieuBang)
    table_cn.pack(padx=10, pady=10, fill=BOTH, expand=True)
    ma_chon = None
    display_data()

    btn_them = Button(frame_chucnang, command=fromThem, text="Thêm", font=("Arial", 8, "bold"),fg="White", borderwidth=0,
                      bg="#57a1f8", pady=6, padx=45)
    btn_them.place(x=5, y=30)
    btn_sua = Button(frame_chucnang, command=sua_cn, text="Sửa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_sua.place(x=150, y=30)
    btn_xoa = Button(frame_chucnang, command=xoa_cn, text="Xóa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_xoa.place(x=290, y=30)

    lb_ma_tau = Label(frame_chucnang, bg="White", text="Mã tàu", fg="black", font=("Arial", 10, "bold"))
    lb_ma_tau.place(x=5, y=70)

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
    ma_tau_values = ["{} ({}) ({})".format(row[0], row[1], row[2]) for row in database.get_ma_tau()]
    input_ma_tau = ttk.Combobox(frame_chucnang, font=("Arial", 11), values=ma_tau_values, width=18)
    input_ma_tau.place(x=5, y=90)
    listbox_ma_tau = tk.Listbox(frame_chucnang, font=("Arial", 11))

    # Liên kết sự kiện nhập liệu với hàm update_listbox
    input_ma_tau.bind('<KeyRelease>', update_listbox)

    # Liên kết sự kiện chọn mục trong listbox với hàm on_listbox_select
    listbox_ma_tau.bind('<<ListboxSelect>>', on_listbox_select)
    lb_so_cho_ngoi = Label(frame_chucnang, bg="White", text="Số chỗ ngồi", fg="black", font=("Arial", 10, "bold"))
    lb_so_cho_ngoi.place(x=200, y=70)
    input_so_cho_ngoi = Entry(frame_chucnang, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                          borderwidth=0, width=20)
    input_so_cho_ngoi.place(x=200, y=90)

    lb_hang_ghe = Label(frame_chucnang, bg="White", text="Hạng ghế", fg="black", font=("Arial", 10, "bold"))
    lb_hang_ghe.place(x=5, y=130)
    input_hang_ghe = ttk.Combobox(frame_chucnang, font=("Arial", 11), state="readonly", values=["Ghế thường", "Ghế VIP"], width=18)
    input_hang_ghe.place(x=5, y=150)

    lb_con_trong = Label(frame_chucnang, bg="White", text="Còn trống", fg="black", font=("Arial", 10, "bold"))
    lb_con_trong.place(x=200, y=130)
    input_con_trong = ttk.Combobox(frame_chucnang, font=("Arial", 11), state="readonly", values=["Có", "Không"], width=18)
    input_con_trong.place(x=200, y=150)
