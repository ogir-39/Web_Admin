import sqlite3

# 1. KẾT NỐI SQLITE (tự tạo file nếu chưa có)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 2. ĐỌC FILE SQL
with open("insert_data.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# 3. CHẠY TOÀN BỘ FILE SQL
cursor.executescript(sql_script)

# 4. LƯU LẠI
conn.commit()

cursor.close()
conn.close()

print("🎉 Đã chạy xong file insert_data.sql vào database SQLite!")