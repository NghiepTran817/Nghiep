import sqlite3
from getpass import getpass

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('m.db')
cursor = conn.cursor()

# Tạo bảng user để lưu thông tin client
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Tạo bảng lưu point
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sb TEXT NOT NULL,
        diem REAL NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
''')

# Đăng ký 
def register():
    username = input("Username: ")
    password = getpass("Password: ")
    # Thêm thông tin người dùng vào cơ sở dữ liệu
    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Đăng ký thành công!")

# Đăng nhập
def login():
    username = input("Username: ")
    password = getpass("Password: ")
    # Kiểm tra thông tin đăng nhập từ cơ sở dữ liệu
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print("Đăng nhập thành công!")
        menu(user[0]) 
    else:
        print("Thông tin đăng nhập không chính xác!")

# Nhập điểm
def subject(user_id):
    sb = input("Môn học: ")
    n = int(input("Nhập số cột điểm TX: "))
    points = []
    for i in range(1,n+1):
        point = float(input(f"Nhập điểm TX{i}: "))
        points.append(point)
    point1 = float(input("Nhập điểm giữa kỳ: "))
    point2 = float(input("Nhập điểm cuối kỳ: "))
    TB = (sum(points) + 2 * point1 + 3 * point2) / (n + 5)
    print(f"Tổng điểm: {TB}")
    # Thêm thông tin sản phẩm vào cơ sở dữ liệu
    cursor.execute("INSERT INTO product (sb, diem, user_id) VALUES (?, ?, ?)", (sb, TB, user_id))
    conn.commit()
    print("Nhập điểm thành công!")


# Hiển thị
def display(user_id):
    # Lấy thông tin từ cơ sở dữ liệu
    cursor.execute("SELECT * FROM product WHERE user_id = ?", (user_id,))
    displays = cursor.fetchall()
    if displays:
        for display in displays:
            print("ID:", display[0])
            print("Môn học:", display[1])
            print("Điểm:", display[2])
    else:
        print("Không có gì cả!")

#Quên mật khẩu
def forgetpassword():
    username = input("Username: ") 
    cursor.execute("SELECT password FROM user WHERE      username = ?", (username,)) 
    password = cursor.fetchone() 
    if password: 
        print(f"Mật khẩu của bạn là: {password[0]}") 
    else: 
        print("Username không tồn tại!") 

# xoá id, môn, điểm
def deleteall(user_id):
  cursor.execute("DELETE FROM product WHERE user_id = ?", (user_id,)) 
  conn.commit()
  print("Đã xoá tất cả")


# chức năng
def menu(user_id):
    while True:
      # Phần khung
       print( '- {:-<6} - {:-^20}-'.format('', ''))
       print( '| {:<6} | {:^20} |'.format('ID', 'Chức năng'))
       print( '| {:<6} | {:^20} |'.format('1', 'Nhập điểm học kỳ 1'))
       print('| {:<6} | {:^20} |'.format('2', 'Hiển thị tất cả điểm'))
       print('| {:<6} | {:^20} |'.format('3', 'Xoá tất cả'))
       print('| {:<6} | {:^20} |'.format('4', 'Đăng xuất'))
       print('- {:-<6} + {:-^20}-'.format('', ''))
       choice = input("Vui lòng chọn ID: ")
       if choice == "1":
            subject(user_id)
       elif choice == "2":
            display(user_id)
       elif choice == "3":
            deleteall(user_id)
       elif choice == "4":
            break
       else:
            print("Vui lòng chọn lại!")

# Chương trình chính
while True:
  # phần khung
    print( '- {:-<6} - {:-^15}-'.format('', ''))
    print( '| {:<6} | {:^15} |'.format('ID', 'Chức năng'))
    print( '| {:<6} | {:^15} |'.format('1', 'Đăng ký'))
    print('| {:<6} | {:^15} |'.format('2', 'Đăng nhập'))
    print('| {:<6} | {:^15} |'.format('3', 'Quên mật khẩu'))
    print('| {:<6} | {:^15} |'.format('4', 'Thoát'))
    print('- {:-<6} + {:-^15}-'.format('', ''))


    option = input("Vui lòng chọn ID: ")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3": 
        forgetpassword()
    elif option == "4": 
       break 
    else:
        print("Vui lòng chọn lại!")

# Đóng kết nối cơ sở dữ liệu
conn.close()
