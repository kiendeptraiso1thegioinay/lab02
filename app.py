import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Sinh Viên")
        self.root.geometry("600x750")  # Điều chỉnh kích thước cửa sổ

        # Thông tin kết nối cơ sở dữ liệu
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='382004')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sinhvien')

        # Tạo các widget trong giao diện
        self.create_widgets()

    def create_widgets(self):
        # Kết nối cơ sở dữ liệu
        connection_frame = tk.LabelFrame(self.root, text="Kết nối Database", padx=10, pady=10)
        connection_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(connection_frame, text="Tên DB:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Mật khẩu:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=5, column=0, columnspan=2, pady=10)

        # Khu vực xử lý dữ liệu
        data_frame = tk.LabelFrame(self.root, text="Bảng dữ liệu", padx=10, pady=10)
        data_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(data_frame, text="Tên bảng:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(data_frame, textvariable=self.table_name).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(data_frame, text="Tải dữ liệu", command=self.load_data).grid(row=0, column=1, padx=5, pady=5)

        self.data_display = tk.Text(data_frame, height=10, width=70)
        self.data_display.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Thêm và xóa
        action_frame = tk.LabelFrame(self.root, text="Thêm / Xóa Sinh Viên", padx=10, pady=10)
        action_frame.pack(padx=10, pady=10, fill="x")

        self.mssv = tk.StringVar()
        self.hoten = tk.StringVar()

        tk.Label(action_frame, text="MSSV:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(action_frame, textvariable=self.mssv).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(action_frame, text="Họ và tên:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(action_frame, textvariable=self.hoten).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(action_frame, text="Thêm", command=self.insert_data).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(action_frame, text="Xóa", command=self.delete_data).grid(row=2, column=1, padx=5, pady=5)

        # Tìm kiếm
        search_frame = tk.LabelFrame(self.root, text="Tìm Kiếm Sinh Viên", padx=10, pady=10)
        search_frame.pack(padx=10, pady=10, fill="x")

        self.search_mssv = tk.StringVar()

        tk.Label(search_frame, text="MSSV:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(search_frame, textvariable=self.search_mssv).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(search_frame, text="Tìm Kiếm", command=self.search_data).grid(row=0, column=1, padx=5, pady=5)

        self.search_result = tk.Text(search_frame, height=5, width=70)
        self.search_result.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành Công", "Kết nối cơ sở dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi load dữ liệu: {e}")

    def insert_data(self):
        try:
            # Kiểm tra xem trường MSSV có được điền không
            if not self.mssv.get():
                messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập MSSV để nhập dữ liệu.")
                return
            
            query = sql.SQL("INSERT INTO {} (mssv, hoten) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query, (self.mssv.get(), self.hoten.get()))
            self.conn.commit()
            messagebox.showinfo("Thành Công", "Thêm dữ liệu thành công!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi thêm dữ liệu: {e}")

    def delete_data(self):
        try:
            # Kiểm tra xem trường MSSV có được điền không
            if not self.mssv.get():
                messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập MSSV để xóa dữ liệu.")
                return
            
            query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query, (self.mssv.get(),))
            self.conn.commit()
            if self.cur.rowcount == 0:
                messagebox.showwarning("Cảnh Báo", "Không tìm thấy MSSV để xóa.")
            else:
                messagebox.showinfo("Thành Công", "Xóa dữ liệu thành công!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi xóa dữ liệu: {e}")

    def search_data(self):
        try:
            # Kiểm tra xem trường MSSV có được điền không
            if not self.search_mssv.get():
                messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập MSSV để tìm dữ liệu.")
                return
            
            query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query, (self.search_mssv.get(),))
            row = self.cur.fetchone()
            self.search_result.delete(1.0, tk.END)
            if row:
                self.search_result.insert(tk.END, f"MSSV: {row[0]}\nHọ và tên: {row[1]}")
            else:
                self.search_result.insert(tk.END, "Không tìm thấy sinh viên với MSSV đã nhập.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()