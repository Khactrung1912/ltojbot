# Tổng quan
## Lưu ý: BOT sử dụng các api_v1 của DMOJ.
Bot gồm những chức năng sau
- Tạo các vai trò tương ứng với các rating trên OJ
- Liên kết tài khoản OJ với discord.
- Cập nhật rating của tất cả người dùng theo trên OJ
# Hướng dẫn
## Tạo môi trường ảo Python
```
python -m venv <tên venv>
. <tên venv>/bin/activate
```
## Tải mã nguồn và thư viện 
```
git clone https://github.com/Khactrung1912/ltojbot.git
cd ltojbot
pip install -r requirements.txt
```
## Sửa các thông tin cần thiết
Thêm token, domain web, thông tin database ở tệp settings.py

