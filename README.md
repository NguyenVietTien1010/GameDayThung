🔍 Tổng quan game đẩy hộp

🎮 Chế độ chơi
P: Người chơi điều khiển bằng bàn phím
A: AI tự động giải (sử dụng A* để tìm đường đi hộp đến đích)

🧠 Thuật toán sử dụng
A* (A-star) để tìm đường ngắn nhất từ hộp đến vị trí goal
Hill Climbing có trong code nhưng hiện không được dùng làm AI chính
Hệ thống đánh giá sử dụng heuristic Manhattan distance

🧩 Bản đồ & độ khó
Có 3 level: Dễ, Trung bình, Khó
Level khó được tạo ngẫu nhiên với số lượng tường, hộp và mục tiêu tùy chỉnh
# = tường, B = hộp, G = mục tiêu, P = người chơi

🖼️ Giao diện
Đồ họa đơn giản sử dụng hình ảnh: wall.png, crate.png, focus.png, mushroom.png, pawprint.png
Hiển thị hộp đã đặt đúng vị trí bằng tô màu xanh lá cây (GREEN)
Có hiệu ứng dấu chân khi AI giải (path visualization)
<p align="center"> 
  <img src="assets/menu.png" width="30%" style="margin-right:10px;"> 
  <img src="assets/playing.png" width="30%" style="margin-right:10px;"> 
  <img src="assets/solving.png" width="30%"> </p> <p align="center"> 
    <strong>Menu chọn chế độ | Người chơi điều khiển | AI tự động giải</strong> </p>
    
🧩 Biểu tượng trong game
Biểu tượng	Hình ảnh	Ý nghĩa
🧱 Wall	
Vật cản (không thể đi qua)
📦 Box	
Hộp cần đẩy vào mục tiêu
🎯 Goal	
Vị trí đích của hộp
🍄 Player	
Người chơi
🐾 AI path	
Đường đi AI đề xuất
✅ Khi hộp được đẩy đúng vị trí đích, nó sẽ được tô màu xanh lá cây.
