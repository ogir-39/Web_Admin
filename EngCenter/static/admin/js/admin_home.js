// TÊN FILE: custom_menu.js

// Chờ DOM (Document Object Model) tải xong
$(document).ready(function() {
    // 1. Tìm tất cả các mục menu con đang có class 'active'
    var activeMenuItem = $('.dropdown-item.active');

    // 2. Kiểm tra nếu tìm thấy mục active
    if (activeMenuItem.length > 0) {
        // 3. Tìm phần tử LI cha chứa toàn bộ dropdown (ví dụ: LI của "Quản lý dữ liệu")
        // .closest() tìm phần tử cha gần nhất khớp với selector
        var parentDropdown = activeMenuItem.closest('ul.dropdown-menu');

        // 4. Thêm class 'active' (hoặc 'open') vào LI cha để giữ nó mở
        if (parentDropdown.length > 0) {
            // Tùy thuộc vào theme của bạn, bạn cần thêm class 'active' hoặc 'show'/'open'
            parentDropdown.addClass('active show');
        }
    }
});