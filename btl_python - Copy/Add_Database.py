# -- Tạo cơ sở dữ liệu
# CREATE DATABASE quanlybanve;
#
# -- Sử dụng cơ sở dữ liệu vừa tạo
# USE quanlybanve;
#
# -- Tạo bảng Tau (Tàu)
# CREATE TABLE tau (
#     MaTau VARCHAR(11) PRIMARY KEY,
#     SoHieuTau VARCHAR(10) UNIQUE,
#     TenTau VARCHAR(100)
# );
#
# -- Tạo bảng khachhang (Khách hàng)
# CREATE TABLE khachhang (
#     ma_kh VARCHAR(11) PRIMARY KEY,
#     ho_ten VARCHAR(255),
#     ngay_sinh DATE,
#     gioi_tinh VARCHAR(10),
#     sdt VARCHAR(15),
#     cccd INT,
#     email VARCHAR(255),
#     dia_chi VARCHAR(255),
#     ngaydangky DATE
# );
#
# -- Tạo bảng ChoNgoi (Chỗ ngồi)
# CREATE TABLE chongoi (
#     MaChoNgoi VARCHAR(11) PRIMARY KEY,
#     MaTau VARCHAR(11),
#     SoChoNgoi VARCHAR(10),
#     HangGhe VARCHAR(50),
#     ConTrong BOOLEAN DEFAULT TRUE,
#     FOREIGN KEY (MaTau) REFERENCES tau(MaTau)
# );
#
# -- Tạo bảng LichTrinh (Lịch trình)
# CREATE TABLE lichtrinh (
#     MaLichTrinh VARCHAR(11) PRIMARY KEY,
#     MaTau VARCHAR(11),
#     GaKhoiHanh VARCHAR(100),
#     GaDen VARCHAR(100),
#     ThoiGianKhoiHanh VARCHAR(100),
#     ThoiGianDen VARCHAR(100),
#     NgayKhoiHanh VARCHAR(100),
#     NgayDen VARCHAR(100),
#     FOREIGN KEY (MaTau) REFERENCES tau(MaTau)
# );
#
#
# CREATE TABLE ve (
#     MaVe VARCHAR(11),
#     ma_kh VARCHAR(11),
#     MaLichTrinh VARCHAR(11),
#     MaChoNgoi VARCHAR(11),
#     NgayDatVe VARCHAR(50),
#     GiaVe INT,
#     TrangThai VARCHAR(50) DEFAULT 'DaDat',
#     FOREIGN KEY (ma_kh) REFERENCES khachhang(ma_kh),
#     FOREIGN KEY (MaLichTrinh) REFERENCES lichtrinh(MaLichTrinh),
#     FOREIGN KEY (MaChoNgoi) REFERENCES chongoi(MaChoNgoi)
# );
#
# -- Tạo bảng taikhoan (Tài khoản)
# CREATE TABLE taikhoan (
#     ma_tk INT AUTO_INCREMENT PRIMARY KEY,
#     email VARCHAR(255) NOT NULL UNIQUE,
#     tk VARCHAR(50) NOT NULL UNIQUE,
#     mk VARCHAR(255) NOT NULL,
#     verified BOOLEAN DEFAULT FALSE,
#     verification_code VARCHAR(255)
# );
# eyav yqdr sjik pmnm
# emak nebj mopb oacy
#
#
