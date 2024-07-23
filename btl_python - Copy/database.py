import mysql.connector
import pandas as pd
from datetime import datetime
from tkinter import ttk, messagebox
class CCCDExistsError(Exception):
    pass
def ketnoi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="quanlybanve"
    )
#khách Hàng
def Hien_Thi_KH():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM khachhang")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_employee(keyword):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "SELECT * FROM khachhang WHERE ho_ten LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ma_khach():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT ma_kh, ho_ten, cccd FROM khachhang")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_lowest_available_id(prefix, table, column):
    conn = ketnoi()
    cursor = conn.cursor()
    query = f"SELECT {column} FROM {table} ORDER BY {column}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    id_list = [int(row[0][len(prefix):]) for row in rows if row[0].startswith(prefix)]
    lowest_id = 1
    while lowest_id in id_list:
        lowest_id += 1
    return f"{prefix}{lowest_id}"

def check_cccd_exists(cccd):
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM khachhang WHERE cccd = %s", (cccd,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def them_kh(hoten, ngaysinh, sex, sdt, cccd, email, diachi):
    if check_cccd_exists(cccd):
        raise CCCDExistsError(f"Số CCCD {cccd} đã tồn tại trong hệ thống.")

    conn = ketnoi()
    cursor = conn.cursor()
    ma_kh = get_lowest_available_id('MKH', 'khachhang', 'ma_kh')
    sql = "INSERT INTO khachhang (ma_kh, ho_ten, ngay_sinh, gioi_tinh, sdt, cccd, email, dia_chi, ngaydangky) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ngaydangky = datetime.now().date()
    values = (ma_kh, hoten, ngaysinh, sex, sdt, cccd, email, diachi, ngaydangky)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
def sua_kh(ma_kh, hoten, ngaysinh, sex, sdt, cccd, email, diachi):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "UPDATE khachhang SET ho_ten=%s, ngay_sinh=%s, gioi_tinh=%s, sdt=%s, cccd=%s, email=%s, dia_chi=%s WHERE ma_kh=%s"
    values = (hoten, ngaysinh, sex, sdt, cccd, email, diachi, ma_kh)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def xoa_kh(ma_kh):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "DELETE FROM khachhang WHERE ma_kh=%s"
    cursor.execute(sql, (ma_kh,))
    conn.commit()
    conn.close()

#Chỗ Ngồi
def check_ma_tau_and_so_cho_ngoi_exist(ma_tau, so_cho_ngoi):
    conn = ketnoi()
    if conn is None:
        return False
    cursor = conn.cursor()
    query = "SELECT * FROM chongoi WHERE MaTau = %s AND SoChoNgoi = %s"
    cursor.execute(query, (ma_tau, so_cho_ngoi))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_lowest_available_id(prefix, table, column):
    conn = ketnoi()
    if conn is None:
        return None
    cursor = conn.cursor()
    query = f"SELECT {column} FROM {table} ORDER BY {column}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    id_list = [int(row[0][len(prefix):]) for row in rows if row[0].startswith(prefix)]
    lowest_id = 1
    while lowest_id in id_list:
        lowest_id += 1
    return f"{prefix}{lowest_id}"

def them_chongoi(ma_tau, so_cho_ngoi, hang_ghe, con_trong):
    conn = ketnoi()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        ma_cn = get_lowest_available_id('MCN', 'chongoi', 'MaChoNgoi')
        if ma_cn is None:
            return False

        # Chuyển đổi giá trị con_trong thành 1 hoặc 0
        con_trong_value = 1 if con_trong == "Có" else 0

        query = "INSERT INTO chongoi (MaChoNgoi, MaTau, SoChoNgoi, HangGhe, ConTrong) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (ma_cn, ma_tau, so_cho_ngoi, hang_ghe, con_trong_value))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Lỗi khi thêm chỗ ngồi: {str(e)}")
        return False
    finally:
        conn.close()

def get_ma_cn():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT MaChoNgoi, MaTau, SoChoNgoi, HangGhe, ConTrong FROM chongoi WHERE ConTrong = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ma_cnsua():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT MaChoNgoi, MaTau, SoChoNgoi, HangGhe, ConTrong FROM chongoi")
    rows = cursor.fetchall()
    conn.close()
    return rows

def sua_cn(ma_chon, ma_tau, so_cho_ngoi, hang_ghe, con_trong):
    conn = ketnoi()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        con_trong_value = 1 if con_trong == "Có" else 0
        query = "UPDATE chongoi SET MaTau = %s, SoChoNgoi = %s, HangGhe = %s, ConTrong = %s WHERE MaChoNgoi = %s"
        cursor.execute(query, (ma_tau, so_cho_ngoi, hang_ghe, con_trong_value, ma_chon))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Lỗi khi sửa chỗ ngồi: {str(e)}")
        return False
    finally:
        conn.close()

def xoa_cn(ma_chon):
    conn = ketnoi()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        query = "DELETE FROM chongoi WHERE MaChoNgoi = %s"
        cursor.execute(query, (ma_chon,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Lỗi", f"Lỗi khi xóa chỗ ngồi: {str(e)}")
        return False
    finally:
        conn.close()

def Hien_Thi_CN():
    conn = ketnoi()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM chongoi"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi hiển thị chỗ ngồi: {str(e)}")
        return []
    finally:
        conn.close()

def search_cn(keyword):
    conn = ketnoi()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM chongoi WHERE MaChoNgoi LIKE %s OR MaTau LIKE %s OR SoChoNgoi LIKE %s OR HangGhe LIKE %s OR ConTrong LIKE %s"
        keyword = f"%{keyword}%"
        cursor.execute(query, (keyword, keyword, keyword, keyword, keyword))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")
        return []
    finally:
        conn.close()

def get_ma_tau():
    conn = ketnoi()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        query = "SELECT MaTau FROM tau"
        cursor.execute(query)
        rows = cursor.fetchall()
        ma_tau_values = [row[0] for row in rows]
        return ma_tau_values
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy mã tàu: {str(e)}")
        return []
    finally:
        conn.close()
#Chuyến tàu
def Hien_Thi_Tau():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tau")
    rows = cursor.fetchall()
    conn.close()
    return rows
def search_tau(keyword):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "SELECT * FROM tau WHERE TenTau LIKE %s"  # Sửa đổi cú pháp SQL
    cursor.execute(sql, ('%' + keyword + '%',))  # Sửa đổi tham số truyền vào
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ma_tau():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT MaTau, SoHieuTau, TenTau FROM tau")
    rows = cursor.fetchall()
    conn.close()
    return rows



def them_tau(so_hieu_tau, ten_tau):
    conn = ketnoi()
    cursor = conn.cursor()
    ma_tau = get_lowest_available_id('MT', 'tau', 'MaTau')
    sql = "INSERT INTO tau (MaTau, SoHieuTau, TenTau) VALUES (%s, %s, %s)"
    values = (ma_tau, so_hieu_tau, ten_tau)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def sua_tau(MaTau,so_hieu_tau,ten_tau):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "UPDATE tau SET SoHieuTau=%s,TenTau=%s WHERE MaTau=%s"
    values = (so_hieu_tau,ten_tau,MaTau)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def xoa_tau(ma_tau):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "DELETE FROM tau WHERE MaTau=%s"
    cursor.execute(sql, (ma_tau,))
    conn.commit()
    conn.close()

#Lịch trình
def Hien_Thi_lichtrinh():
    conn = ketnoi()
    cursor = conn.cursor()
    query = """
        SELECT 
            lt.MaLichTrinh,
            lt.MaTau,
            t.TenTau,
            lt.GaKhoiHanh,
            lt.GaDen,
            lt.ThoiGianKhoiHanh,
            lt.ThoiGianDen,
            lt.NgayKhoiHanh,
            lt.NgayDen
        FROM 
            LichTrinh lt 
        JOIN 
            Tau t ON lt.MaTau = t.MaTau
        ORDER BY 
            lt.MaTau
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ma_lt():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT MaLichTrinh,MaTau, GaKhoiHanh, GaDen FROM LichTrinh")
    rows = cursor.fetchall()
    conn.close()
    return rows


def check_lichtrinh_exist(ma_tau, ga_khoi_hanh, ga_den):
    conn = ketnoi()
    cursor = conn.cursor()
    query = "SELECT * FROM LichTrinh WHERE MaTau = %s AND GaKhoiHanh = %s AND GaDen = %s"
    cursor.execute(query, (ma_tau, ga_khoi_hanh, ga_den))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def them_lichtrinh(ma_tau, ga_khoi_hanh, ga_den, thoi_gian_khoi_hanh, thoi_gian_den, NgayKhoiHanh, NgayDen):
    conn = ketnoi()
    cursor = conn.cursor()
    ma_lt = get_lowest_available_id('MLT', 'lichtrinh', 'MaLichTrinh')
    sql = """
        INSERT INTO LichTrinh (MaLichTrinh, MaTau, GaKhoiHanh, GaDen, ThoiGianKhoiHanh, ThoiGianDen, NgayKhoiHanh, NgayDen)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (ma_lt, ma_tau, ga_khoi_hanh, ga_den, thoi_gian_khoi_hanh, thoi_gian_den, NgayKhoiHanh, NgayDen)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return True

def search_lichtrinh(keyword):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = """
        SELECT 
            lt.MaLichTrinh,
            lt.MaTau,
            t.TenTau,
            lt.GaKhoiHanh,
            lt.GaDen,
            lt.ThoiGianKhoiHanh,
            lt.ThoiGianDen,
            lt.NgayKhoiHanh,
            lt.NgayDen
        FROM 
            LichTrinh lt
        JOIN 
            Tau t ON lt.MaTau = t.MaTau
        WHERE 
            lt.GaKhoiHanh LIKE %s OR lt.GaDen LIKE %s
        ORDER BY 
            lt.MaTau
    """
    cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def sua_lichtrinh(ma_lich_trinh, ma_tau_moi, ga_khoi_hanh_moi, ga_den_moi, thoi_gian_khoi_hanh_moi, thoi_gian_den_moi,NgayKhoiHanh,NgayDen):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = """
        UPDATE LichTrinh
        SET MaTau = %s, GaKhoiHanh = %s, GaDen = %s, ThoiGianKhoiHanh = %s, ThoiGianDen = %s,NgayKhoiHanh = %s,NgayDen = %s
        WHERE MaLichTrinh = %s
    """
    values = (ma_tau_moi, ga_khoi_hanh_moi, ga_den_moi, thoi_gian_khoi_hanh_moi, thoi_gian_den_moi,NgayKhoiHanh,NgayDen, ma_lich_trinh)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def xoa_lichtrinh(ma_lichtrinh):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "DELETE FROM LichTrinh WHERE MaLichTrinh=%s"
    cursor.execute(sql, (ma_lichtrinh,))
    conn.commit()
    conn.close()

#Vé Tàu
def Hien_Thi_Ve():
    conn = ketnoi()
    cursor = conn.cursor()
    sql = """
        SELECT Ve.MaVe, KhachHang.ma_kh,LichTrinh.MaLichTrinh, ChoNgoi.MaChoNgoi,KhachHang.ho_ten, Tau.TenTau, LichTrinh.GaKhoiHanh, LichTrinh.GaDen,
               LichTrinh.ThoiGianKhoiHanh, LichTrinh.NgayKhoiHanh, ChoNgoi.SoChoNgoi, Ve.NgayDatVe, Ve.GiaVe, Ve.TrangThai
        FROM Ve
        INNER JOIN KhachHang ON Ve.ma_kh = KhachHang.ma_kh
        INNER JOIN LichTrinh ON Ve.MaLichTrinh = LichTrinh.MaLichTrinh
        INNER JOIN ChoNgoi ON Ve.MaChoNgoi = ChoNgoi.MaChoNgoi
        INNER JOIN Tau ON ChoNgoi.MaTau = Tau.MaTau
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_ve(keyword):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = """
        SELECT Ve.MaVe, KhachHang.ma_kh,LichTrinh.MaLichTrinh, ChoNgoi.MaChoNgoi,KhachHang.ho_ten, Tau.TenTau, LichTrinh.GaKhoiHanh, LichTrinh.GaDen,
               LichTrinh.ThoiGianKhoiHanh, LichTrinh.NgayKhoiHanh, ChoNgoi.SoChoNgoi, Ve.NgayDatVe, Ve.GiaVe, Ve.TrangThai
        FROM Ve
        INNER JOIN KhachHang ON Ve.ma_kh = KhachHang.ma_kh
        INNER JOIN LichTrinh ON Ve.MaLichTrinh = LichTrinh.MaLichTrinh
        INNER JOIN ChoNgoi ON Ve.MaChoNgoi = ChoNgoi.MaChoNgoi
        INNER JOIN Tau ON ChoNgoi.MaTau = Tau.MaTau
        WHERE KhachHang.ho_ten LIKE %s OR KhachHang.ma_kh LIKE %s
    """
    keyword = '%' + keyword + '%'
    cursor.execute(sql, (keyword, keyword))
    rows = cursor.fetchall()
    conn.close()
    return rows

def them_ve(ma_kh, MaLichTrinh, MaChoNgoi, TrangThai):
    conn = ketnoi()
    cursor = conn.cursor()
    ma_ve = get_lowest_available_id('MV', 've', 'MaVe')

    try:
        cursor.execute("SELECT HangGhe FROM chongoi WHERE MaChoNgoi = %s", (MaChoNgoi,))
        hang_ghe = cursor.fetchone()[0]
        if hang_ghe == "Ghế thường":
            GiaVe = 1000000
        elif hang_ghe == "Ghế VIP":
            GiaVe = 2000000
        else:
            raise ValueError("Invalid seat type")
        NgayDatVe = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            INSERT INTO ve (MaVe, ma_kh, MaLichTrinh, MaChoNgoi, NgayDatVe, GiaVe, TrangThai)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (ma_ve, ma_kh, MaLichTrinh, MaChoNgoi, NgayDatVe, GiaVe, TrangThai)
        cursor.execute(sql, values)
        update_sql = "UPDATE chongoi SET ConTrong = 0 WHERE MaChoNgoi = %s"
        cursor.execute(update_sql, (MaChoNgoi,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def sua_ve(ma_ve, ma_kh, MaLichTrinh, MaChoNgoi, TrangThai):
    conn = ketnoi()
    cursor = conn.cursor()

    # Get the seat type for the given seat ID
    cursor.execute("SELECT HangGhe FROM chongoi WHERE MaChoNgoi = %s", (MaChoNgoi,))
    hang_ghe = cursor.fetchone()[0]

    # Set the price based on the seat type
    if hang_ghe == "Ghế thường":
        GiaVe = 1000000
    elif hang_ghe == "Ghế VIP":
        GiaVe = 2000000
    else:
        raise ValueError("Invalid seat type")

    NgayDatVe = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = """
        UPDATE ve
        SET ma_kh = %s, MaLichTrinh = %s, MaChoNgoi = %s, NgayDatVe = %s, GiaVe = %s, TrangThai = %s
        WHERE MaVe = %s
    """
    values = (ma_kh, MaLichTrinh, MaChoNgoi, NgayDatVe, GiaVe, TrangThai, ma_ve)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def xoa_ve(ma_ve):
    conn = ketnoi()
    cursor = conn.cursor()
    sql = "DELETE FROM Ve WHERE MaVe = %s"
    values = (ma_ve,)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def get_seat_stats():
    conn = ketnoi()
    cursor = conn.cursor()
    query = """
        SELECT t.TenTau,
               SUM(CASE WHEN cn.ConTrong = 1 THEN 1 ELSE 0 END) AS GheTrong,
               SUM(CASE WHEN cn.ConTrong = 0 THEN 1 ELSE 0 END) AS GheKhongTrong
        FROM chongoi cn
        JOIN tau t ON cn.MaTau = t.MaTau
        GROUP BY t.TenTau
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_ticket_price_by_month_year():
    conn = ketnoi()
    cursor = conn.cursor()
    query = """
        SELECT YEAR(NgayDatVe) AS Nam, MONTH(NgayDatVe) AS Thang, SUM(GiaVe) AS TongGiaVe
        FROM ve
        GROUP BY YEAR(NgayDatVe), MONTH(NgayDatVe)
        ORDER BY YEAR(NgayDatVe), MONTH(NgayDatVe)
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_customer_data():
    conn = ketnoi()
    cursor = conn.cursor()
    cursor.execute("SELECT ngaydangky FROM khachhang")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def analyze_customers_by_month():
    dates = get_customer_data()
    dates = pd.to_datetime(dates)  # Chuyển đổi dữ liệu ngày tháng

    # Tạo DataFrame
    df = pd.DataFrame(dates, columns=['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly_counts = df.groupby('month').size()

    return monthly_counts

def lay_ma_tau_tu_ma_chongoi(ma_chongoi):
    conn = ketnoi()
    cursor = conn.cursor()
    query = "SELECT MaTau FROM chongoi WHERE MaChoNgoi = %s"
    cursor.execute(query, (ma_chongoi,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Lấy mã tàu từ mã lịch trình
def lay_ma_tau_tu_ma_lichtrinh(ma_lichtrinh):
    conn = ketnoi()
    cursor = conn.cursor()
    query = "SELECT MaTau FROM lichtrinh WHERE MaLichTrinh = %s"
    cursor.execute(query, (ma_lichtrinh,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None