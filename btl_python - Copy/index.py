from tkinter import *
from PIL import ImageTk, Image
from quanlykh import show_KhachHang
from quanlyChoNgoi import show_ChoNgoi
from baocaothongke import show_ThongKe
from quanlytau import show_Tau
from quanlyLichTrinh import show_LichTrinh
from quanlyve import show_Ve

menu_visible = False


def show_index(dangnhap_window):
    def show_page(page_name):
        for widget in frame_noidung.winfo_children():
            widget.destroy()
        if page_name == "Tau":
            show_Tau(frame_noidung)
        elif page_name == "KhachHang":
            show_KhachHang(frame_noidung)
        elif page_name == "ChoNgoi":
            show_ChoNgoi(frame_noidung)
        elif page_name == "LichTrinh":
            show_LichTrinh(frame_noidung)
        elif page_name == "Ve":
            show_Ve(frame_noidung)
        elif page_name == "ThongKe":
            show_ThongKe(frame_noidung)

    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def toggle_menu():
        global menu_visible, frame_menu, frame_noidung
        if menu_visible:
            frame_menu.place_forget()
            frame_noidung.place_forget()
        else:
            frame_menu.place(x=0, y=50)
            frame_noidung.place(x=250, y=50)
        menu_visible = not menu_visible

    dangnhap_window.destroy()
    index = Tk()
    index.title('Trang Chủ')
    index.geometry('1000x600')
    index.attributes("-topmost", True)
    center_window(index, 1000, 600)

    image = Image.open("img/backgroudIndex.jpg")
    background_image = ImageTk.PhotoImage(image)
    canvas = Canvas(index, width=index.winfo_screenwidth(), height=index.winfo_screenheight())
    canvas.pack(fill=BOTH, expand=YES)

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        background_image_resized = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=background_image_resized)
        canvas.image = background_image_resized

    canvas.bind("<Configure>", resize_image)

    lb_nhom = Label(index, text="MR.", bg="white", fg="gray", font=("Arial", 20, "bold"))
    lb_nhom.place(x=0, y=0)
    lb_nhom1 = Label(index, text="QK", bg="white", fg="red", font=("Arial", 20, "bold"))
    lb_nhom1.place(x=50, y=0)

    global frame_menu  # Biến frame_menu cũng cần được khai báo là global để có thể sử dụng trong toggle_menu()
    frame_menu = Frame(index, bg="white", width=220, height=500)
    btn_nv = Button(frame_menu, command=lambda: show_page("Tau"), text="Quản Lý Tàu", font=("Arial", 14, "bold"),
                    fg="White", borderwidth=0,
                    bg="#57a1f8", pady=10, padx=40)
    btn_nv.place(x=5, y=10)
    btn_kh = Button(frame_menu, command=lambda: show_page("KhachHang"), text="Quản Lý Khách Hàng",
                    font=("Arial", 14, "bold"), fg="White", borderwidth=0,
                    bg="#57a1f8", pady=10, padx=1)
    btn_kh.place(x=5, y=72)
    btn_tau = Button(frame_menu, command=lambda: show_page("ChoNgoi"), text="Quản Chỗ Ngồi", font=("Arial", 14, "bold"),
                     fg="White", borderwidth=0,
                     bg="#57a1f8", pady=10, padx=29)
    btn_tau.place(x=5, y=130)
    btn_ve = Button(frame_menu, command=lambda: show_page("LichTrinh"), text="QL Lịch Trình",
                    font=("Arial", 14, "bold"), fg="White", borderwidth=0,
                    bg="#57a1f8", pady=10, padx=35)
    btn_ve.place(x=5, y=188)
    btn_baocao = Button(frame_menu, command=lambda: show_page("Ve"), text="Quản Lý Vé", font=("Arial", 14, "bold"),
                        fg="White", borderwidth=0,
                        bg="#57a1f8", pady=10, padx=45)
    btn_baocao.place(x=5, y=246)
    btn_dangxuat = Button(frame_menu, command=lambda: show_page("ThongKe"), text="Báo Cáo Thống Kê",
                          font=("Arial", 14, "bold"), fg="White", borderwidth=0,
                          bg="#57a1f8", pady=10, padx=11)
    btn_dangxuat.place(x=5, y=304)

    anh = Image.open("img/logo.png")
    size = anh.resize((122, 36), Image.LANCZOS)
    img = ImageTk.PhotoImage(size)
    btn_logo = Button(index, image=img, borderwidth=0, bg='White', command=toggle_menu)
    btn_logo.place(x=96, y=0)

    global frame_noidung
    frame_noidung = Frame(index,bg="white")
    frame_noidung.place(x=230, y=50)

    index.mainloop()
