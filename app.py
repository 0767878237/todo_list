import streamlit as st
from datetime import date

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Corporate To-Do App",
    page_icon="✅",
    layout="wide", # Chuyển sang layout rộng để có không gian cho sidebar
    initial_sidebar_state="expanded",
)

# --- CSS Tùy chỉnh để nâng cấp giao diện ---
def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Tệp CSS '{file_name}' không tìm thấy. Hãy chắc chắn rằng nó ở cùng thư mục với 'app.py'.")

local_css("style.css")


# --- Khởi tạo Session State cho nhiều danh sách ---
if "projects" not in st.session_state:
    # Khởi tạo với 3 danh sách mẫu
    st.session_state.projects = {
        "🗓️ Hôm nay": [],
        "💼 Công việc": [],
        "🛒 Mua sắm": []
    }
if "current_project" not in st.session_state:
    st.session_state.current_project = "🗓️ Hôm nay" # Đặt danh sách mặc định

# Thêm state để theo dõi công việc đang được chỉnh sửa
if "editing_task_key" not in st.session_state:
    st.session_state.editing_task_key = None

# --- ================== SIDEBAR ================== ---
st.sidebar.title("Quản lý danh sách") # Đây là 'h1' trong sidebar

# Form để thêm danh sách mới
with st.sidebar.form("new_project_form"):
    new_project_name = st.text_input("Tên danh sách mới")
    submitted_project = st.form_submit_button("➕ Thêm danh sách")
    if submitted_project and new_project_name:
        if new_project_name not in st.session_state.projects:
            st.session_state.projects[new_project_name] = []
            st.sidebar.success(f"Đã thêm '{new_project_name}'!")
        else:
            st.sidebar.error("Danh sách này đã tồn tại.")

st.sidebar.write("---")

# === MỚI: Logic hiển thị st.radio với số lượng công việc ===
project_names_formatted = [] # Danh sách tên để hiển thị (ví dụ: "Công việc (3)")
project_names_clean = []     # Danh sách tên gốc (ví dụ: "Công việc")

# Đảm bảo `current_project` vẫn tồn tại, nếu không thì reset
if st.session_state.current_project not in st.session_state.projects:
    if st.session_state.projects:
        st.session_state.current_project = list(st.session_state.projects.keys())[0]
    else:
        st.session_state.current_project = None # Trường hợp không có dự án nào

# Tìm index của dự án hiện tại
current_project_index = 0
try:
    # Tạo danh sách tên và đếm số công việc
    for i, (name, tasks) in enumerate(st.session_state.projects.items()):
        # Đếm số task chưa hoàn thành
        incomplete_tasks = sum(1 for task in tasks if not task['completed'])
        
        project_names_clean.append(name)
        
        if incomplete_tasks > 0:
            project_names_formatted.append(f"{name} ({incomplete_tasks})")
        else:
            project_names_formatted.append(name)
            
        # Tìm index của dự án đang được chọn
        if name == st.session_state.current_project:
            current_project_index = i
            
except Exception as e:
    st.error(f"Lỗi khi tải danh sách: {e}") # Xử lý lỗi nếu có


if st.session_state.current_project:
    selected_project_formatted = st.sidebar.radio(
        "Chọn danh sách:",
        project_names_formatted,
        index=current_project_index, # Đặt mục đang chọn
        label_visibility="collapsed" # Ẩn nhãn "Chọn danh sách:"
    )
    
    # Lấy index của lựa chọn mới
    selected_index = project_names_formatted.index(selected_project_formatted)
    # Dùng index đó để lấy tên "sạch" và cập nhật state
    st.session_state.current_project = project_names_clean[selected_index]
else:
    st.sidebar.info("Hãy thêm một danh sách mới để bắt đầu.")


# --- ================== TRANG CHÍNH ================== ---

# Kiểm tra nếu không có dự án nào được chọn (trường hợp danh sách trống)
if not st.session_state.current_project:
    st.title("Chào mừng!")
    st.info("Hãy tạo danh sách đầu tiên của bạn ở thanh bên trái để bắt đầu.")
else:
    # Lấy danh sách công việc của dự án hiện tại
    current_tasks = st.session_state.projects[st.session_state.current_project]

    # Tiêu đề chính
    st.title(f"{st.session_state.current_project}") # Đây là 'h1' trong trang chính


    # --- Form nhập liệu công việc ---
    with st.form("task_form"):
        col1, col2 = st.columns([3, 1]) 
        with col1:
            new_task = st.text_input("Thêm công việc mới", placeholder="Ví dụ: Họp với đội Marketing")
        with col2:
            deadline = st.date_input("Hạn chót", value=date.today())

        submitted = st.form_submit_button("Thêm Công Việc")
        if submitted and new_task:
            # Thêm công việc vào ĐÚNG danh sách hiện tại
            current_tasks.append({"task": new_task, "deadline": deadline, "completed": False})
            st.rerun()

    st.write("---")

    # --- Hiển thị danh sách công việc ---
    if not current_tasks:
        st.info("Danh sách công việc trống. Hãy bắt đầu một ngày làm việc hiệu quả!")
    else:
        for index, task_item in enumerate(current_tasks):
            # Key phải là duy nhất, kết hợp tên dự án và index
            task_key = f"{st.session_state.current_project}_{index}"
            
            # MỚI: Kiểm tra xem công việc này có đang ở chế độ chỉnh sửa không
            if st.session_state.editing_task_key == task_key:
                # --- Chế độ CHỈNH SỬA ---
                with st.form(key=f"edit_form_{task_key}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        edited_task_name = st.text_input("Sửa tên công việc", value=task_item['task'], label_visibility="collapsed")
                    with col2:
                        edited_deadline = st.date_input("Sửa hạn chót", value=task_item['deadline'], label_visibility="collapsed")
                    
                    # Nút Lưu và Hủy
                    save_col, cancel_col = st.columns([1, 1])
                    with save_col:
                        if st.form_submit_button("💾 Lưu", use_container_width=True):
                            # Cập nhật thông tin công việc
                            current_tasks[index]['task'] = edited_task_name
                            current_tasks[index]['deadline'] = edited_deadline
                            st.session_state.editing_task_key = None # Thoát chế độ chỉnh sửa
                            st.rerun()
                    with cancel_col:
                        if st.form_submit_button("❌ Hủy", use_container_width=True):
                            st.session_state.editing_task_key = None # Thoát chế độ chỉnh sửa
                            st.rerun()
            else:
                # --- Chế độ HIỂN THỊ (Bình thường) ---
                with st.container(border=True): 
                    # THAY ĐỔI: Thêm cột cho nút Sửa [Task, Deadline, Edit, Delete]
                    col1, col2, col3, col4 = st.columns([0.5, 0.25, 0.125, 0.125]) 
                    
                    with col1:
                        is_completed = st.checkbox(
                            f"**{task_item['task']}**", 
                            value=task_item['completed'], 
                            key=f"check_{task_key}"
                        )
                        if is_completed != task_item['completed']:
                            task_item['completed'] = is_completed
                            st.rerun()

                    with col2:
                        today = date.today()
                        deadline_str = task_item['deadline'].strftime('%d/%m/%Y')
                        
                        if task_item['completed']:
                            st.markdown(f"<p class='deadline-normal'>Hoàn thành</p>", unsafe_allow_html=True)
                        elif task_item['deadline'] < today:
                            st.markdown(f"<p class='deadline-overdue'>Trễ hạn: {deadline_str}</p>", unsafe_allow_html=True)
                        elif task_item['deadline'] == today:
                            st.markdown(f"<p classT='deadline-today'>Hôm nay: {deadline_str}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='deadline-normal'>Hạn: {deadline_str}</p>", unsafe_allow_html=True)

                    # MỚI: Cột Nút Sửa
                    with col3:
                        if st.button("✏️", key=f"edit_{task_key}", help="Sửa công việc này"):
                            st.session_state.editing_task_key = task_key # Vào chế độ chỉnh sửa
                            st.rerun()
                    
                    # THAY ĐỔI: Cột Nút Xóa (chuyển sang col4)
                    with col4:
                        if st.button("🗑️", key=f"del_{task_key}", help="Xóa công việc này"):
                            del current_tasks[index]
                            st.session_state.editing_task_key = None # Đảm bảo thoát edit mode nếu đang sửa task bị xóa
                            st.rerun()

    # --- Nút xóa tất cả ---
    if current_tasks:
        st.write("") 
        if st.button("🧹 Xóa tất cả công việc đã hoàn thành"):
            st.session_state.projects[st.session_state.current_project] = [
                task for task in current_tasks if not task['completed']
            ]
            st.rerun()
