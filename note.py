import sqlite3
from getpass import getpass

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('n.db')
cursor = conn.cursor()

# Tạo bảng user để lưu thông tin client
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Tạo bảng lưu ghi chú
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rep (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        ghichu TEXT NOT NULL,
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

#Ghi chú
def note(user_id):
    Day = input("Nhập ngày tháng năm: ")
    n = int(input("Nhập số dòng: "))
    for i in range(1,n+1):
        s = input(" ")
    cursor.execute("INSERT INTO rep (day,ghichu, user_id) VALUES (?, ?, ?)", (Day,s, user_id))
    conn.commit()
    print("Thành công")

# Hiển thị
def display(user_id):
    # Lấy thông tin từ cơ sở dữ liệu
    cursor.execute("SELECT * FROM rep WHERE user_id = ?", (user_id,))
    displays = cursor.fetchall()
    if displays:
        for display in displays:
            print("NGÀY THÁNG NĂM",display[1])
            print("Dòng: ", display[2])

    else:
        print("Không có gì cả!")
  
# chức năng
def menu(user_id):
    while True:
      # Phần khung
       print( '- {:-<6} - {:-^20}-'.format('', ''))
       print( '| {:<6} | {:^20} |'.format('ID', 'Chức năng'))
       print( '| {:<6} | {:^20} |'.format('1', 'Ghi chú'))
       print('| {:<6} | {:^20} |'.format('2', 'Hiển thị ghi chú'))
       print('| {:<6} | {:^20} |'.format('3', 'Đăng xuất'))
       print('- {:-<6} + {:-^20}-'.format('', ''))
       choice = input("Vui lòng chọn ID: ")
       if choice == "1":
          note(user_id)
       elif choice == "2":
          display(user_id)
       elif choice == "3":
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
    print('| {:<6} | {:^15} |'.format('3', 'Thoát'))
    print('- {:-<6} + {:-^15}-'.format('', ''))


    option = input("Vui lòng chọn ID: ")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3": 
       break 
    else:
        print("Vui lòng chọn lại!")

# Đóng kết nối cơ sở dữ liệu
conn.close()
