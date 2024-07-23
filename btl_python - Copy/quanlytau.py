from tkinter.ttk import *
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import database

def show_Tau(frame_noidung):
    def clear_entries():
        input_ten_tau.delete(0, END)
        input_loai_tau.delete(0, END)

    def ChonDuLieuBang(event):
        selected_row = table_kh.focus()
        data = table_kh.item(selected_row, 'values')
        clear_entries()
        input_loai_tau.insert(0, data[1])
        input_ten_tau.insert(0, data[2])

    def search_tau():
        try:
            rows = database.search_tau(input_timkiem_kh.get())
            update_table(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    def them_tau(input_loai_tau, input_ten_tau, addThem):
        try:
            loai_tau = input_loai_tau.get()
            ten_tau = input_ten_tau.get()

            if loai_tau == "" or ten_tau == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            if len(loai_tau) < 5:
                messagebox.showerror("Lỗi", "Số hiệu tàu phải có ít nhất 5 ký tự")
                return

            database.them_tau(loai_tau, ten_tau)
            messagebox.showinfo("Thông báo", "Thêm tàu thành công")
            clear_entries()
            display_data()
            addThem.destroy()
        except ValueError as ve:
            messagebox.showerror("Lỗi", str(ve))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm tàu: {str(e)}")

    def fromThem():
        def center_window(window, width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        addThem = Toplevel()
        addThem.title('Thêm Tàu')
        addThem.geometry('700x400')
        center_window(addThem, 700, 400)
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
        frame = Frame(addThem, bg="white", width=400, height=300)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        lb = Label(frame, text="Thêm Tàu", fg="gray", font=("Arial", 18, "bold"), bg='White')
        lb.place(x=150, y=30)

        lb_tk = Label(frame, text="Tên Tàu", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_tk.place(x=50, y=100)

        lb_mk = Label(frame, text="Số Hiệu Tàu", fg="gray", font=("Arial", 10, "bold"), bg='White')
        lb_mk.place(x=50, y=160)
        noot = Label(frame, fg="gray", text="nhập trên 5 kí tự", font=("Arial", 8, "italic"), bg='White')
        noot.place(x=150, y=190)
        input_ten_tau = Entry(frame, font=("Arial", 12), highlightbackground="light blue", highlightthickness=1,
                              borderwidth=0)
        input_ten_tau.place(x=150, y=100)

        input_loai_tau = Entry(frame, font=("Arial", 12), highlightbackground="light blue", highlightthickness=1,
                            borderwidth=0)
        input_loai_tau.place(x=150, y=160)

        btn_them = Button(frame, text="Thêm", command=lambda:them_tau(input_loai_tau, input_ten_tau, addThem), bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=30, pady=3,
                          borderwidth=0)
        btn_them.place(x=50, y=250)

        btn_dangky = Button(frame, text="Hủy", command=addThem.destroy, bg="#57a1f8", fg="White", font=("Arial", 10, "bold"), padx=45, pady=3,
                            borderwidth=0)
        btn_dangky.place(x=215, y=250)

        addThem.mainloop()

    def sua_tau():
        try:
            if input_loai_tau.get() == "" or input_ten_tau.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            if len(input_loai_tau.get()) < 5:
                messagebox.showerror("Lỗi", "Số hiệu tàu phải có ít nhất 5 ký tự")
                return
            selected_row = table_kh.focus()
            data = table_kh.item(selected_row, 'values')
            ma_chon = data[0]
            database.sua_tau(ma_chon, input_loai_tau.get(), input_ten_tau.get())
            messagebox.showinfo("Thông báo", "Cập nhật tàu thành công")
            clear_entries()
            display_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật tàu: {str(e)}")

    def xoa_tau():
        try:
            selected_row = table_kh.focus()
            data = table_kh.item(selected_row, 'values')
            ma_chon = data[0]
            database.xoa_tau(ma_chon)
            messagebox.showinfo("Thông báo", "Xóa tàu thành công")
            clear_entries()
            display_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa tàu: {str(e)}")

    def display_data():
        try:
            rows = database.Hien_Thi_Tau()
            update_table(rows)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị dữ liệu: {str(e)}")

    def update_table(rows):
        table_kh.delete(*table_kh.get_children())
        for row in rows:
            table_kh.insert("", END, values=row)

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

        rows = database.Hien_Thi_Tau()
        filtered_rows = [row for row in rows if
                         input_text in row[0].lower() or input_text in row[
                             1].lower() or input_text in row[
                             2].lower()]  # Lọc dữ liệu theo ga khởi hành và ga đến

        update_table(filtered_rows)

    input_timkiem_kh = ttk.Combobox(frame_timkiem, font=("Arial", 11)
                                    , width=30)
    input_timkiem_kh.grid(row=0, column=0, padx=10, pady=10)
    input_timkiem_kh.bind('<KeyRelease>', update_suggestions)

    anh = Image.open("img/icontim.png")
    size = anh.resize((20, 20), Image.LANCZOS)
    global img
    img = ImageTk.PhotoImage(size)
    btn_timkiem_tau = Button(frame_timkiem, image=img, command=search_tau, borderwidth=0)
    btn_timkiem_tau.grid(row=0, column=1, padx=(0, 10))

    columns = ("Mã tàu", "Số hiệu tàu", "Tên tàu")
    table_kh = ttk.Treeview(frame_tb, columns=columns, show="headings")
    table_kh.heading("Mã tàu", text="Mã tàu")
    table_kh.heading("Số hiệu tàu", text="Số hiệu tàu")
    table_kh.heading("Tên tàu", text="Tên tàu")
    table_kh.column("Mã tàu", minwidth=0, width=300)
    table_kh.column("Số hiệu tàu", minwidth=0, width=300)
    table_kh.column("Tên tàu", minwidth=0, width=300)
    table_kh.pack(fill="both", expand=True)

    for col in columns:
        table_kh.column(col, anchor='center')

    table_kh.bind("<<TreeviewSelect>>", ChonDuLieuBang)
    table_kh.pack(padx=10, pady=10, fill=BOTH, expand=True)

    ma_chon = None
    display_data()

    btn_them = Button(frame_chucnang, command=fromThem, text="Thêm", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                      bg="#57a1f8", pady=6, padx=45)
    btn_them.place(x=5, y=30)
    btn_sua = Button(frame_chucnang, command=sua_tau, text="Sửa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_sua.place(x=150, y=30)
    btn_xoa = Button(frame_chucnang, command=xoa_tau, text="Xóa", font=("Arial", 8, "bold"), fg="White", borderwidth=0,
                     bg="#57a1f8", pady=6, padx=45)
    btn_xoa.place(x=290, y=30)

    lb_ten_tau = Label(frame_chucnang, bg="White", text="Tên tàu", fg="black", font=("Arial", 10, "bold"))
    lb_ten_tau.place(x=5, y=70)
    input_ten_tau = Entry(frame_chucnang, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                         borderwidth=0, width=20)
    input_ten_tau.place(x=5, y=90)

    lb_loai_tau = Label(frame_chucnang, bg="White", text="Số hiệu tàu", fg="black", font=("Arial", 10, "bold"))
    lb_loai_tau.place(x=200, y=70)
    input_loai_tau = Entry(frame_chucnang, font=("Arial", 11), highlightbackground="light blue", highlightthickness=1,
                          borderwidth=0, width=20)
    input_loai_tau.place(x=200, y=90)

