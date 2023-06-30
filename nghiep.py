import sqlite3
from getpass import getpass

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Tạo bảng user để lưu thông tin người dùng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Tạo bảng product để lưu thông tin sản phẩm
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
''')

# Đăng ký người dùng
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
        menu(user[0])  # Chuyển đến menu với id của người dùng
    else:
        print("Thông tin đăng nhập không chính xác!")

# Thêm sản phẩm
def add_product(user_id):
    name = input("Tên sản phẩm: ")
    price = float(input("Giá tiền: "))
    # Thêm thông tin sản phẩm vào cơ sở dữ liệu
    cursor.execute("INSERT INTO product (name, price, user_id) VALUES (?, ?, ?)", (name, price, user_id))
    conn.commit()
    print("Thêm sản phẩm thành công!")

# Xóa sản phẩm
def delete_product(user_id):
    product_id = int(input("ID sản phẩm cần xóa: "))
    # Xóa thông tin sản phẩm từ cơ sở dữ liệu
    cursor.execute("DELETE FROM product WHERE id = ? AND user_id = ?", (product_id, user_id))
    conn.commit()
    print("Xóa sản phẩm thành công!")

# Hiển thị danh sách sản phẩm
def display_products(user_id):
    # Lấy thông tin sản phẩm từ cơ sở dữ liệu
    cursor.execute("SELECT * FROM product WHERE user_id = ?", (user_id,))
    products = cursor.fetchall()
    if products:
        for product in products:
            print("ID:", product[0])
            print("Tên sản phẩm:", product[1])
            print("Giá tiền:", product[2])
            print("------------")
    else:
        print("Không có sản phẩm nào!")

# Menu chức năng
def menu(user_id):
    while True:
        print("""
        ---- MENU ----
        1. Thêm sản phẩm
        2. Xóa sản phẩm
        3. Hiển thị sản phẩm
        4. Đăng xuất
        """)
        choice = input("Vui lòng chọn: ")
        if choice == "1":
            add_product(user_id)
        elif choice == "2":
            delete_product(user_id)
        elif choice == "3":
            display_products(user_id)
        elif choice == "4":
            break
        else:
            print("Lựa chọn không hợp lệ!")

# Chương trình chính
while True:
    print("""
    ----- ỨNG DỤNG QUẢN LÝ SẢN PHẨM -----
    1. Đăng ký
    2. Đăng nhập
    3. Thoát
    """)
    option = input("Vui lòng chọn: ")
    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Lựa chọn không hợp lệ!")

# Đóng kết nối cơ sở dữ liệu
conn.close()
