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
st.markdown("""
<style>
    /* --- Giao diện chung --- */
    body {
        background-color: #FFFFFF; /* Nền trắng */
    }
    .stApp {
        background-color: #FFFFFF !important; /* Nền trắng (buộc) */
        color: #111111 !important; /* Chữ đen (buộc) */
    }
    /* Buộc nhãn của ô nhập liệu có màu tối */
    .stTextInput > label, .stDateInput > label {
        color: #111111 !important;
    }
    /* SỬA LỖI: Buộc các ô input có nền trắng, chữ đen */
    .stTextInput input, .stDateInput div[data-testid="stDateInput"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 5px !important;
    }
    .stTextInput input:focus, .stDateInput div[data-testid="stDateInput"]:focus-within {
        border-color: #007BFF !important; /* Thêm highlight khi focus */
        box-shadow: 0 0 0 1px #007BFF !important;
    }

    /* --- Tùy chỉnh Sidebar --- */
    section[data-testid="stSidebar"] {
        background-color: #F0F2F6 !important; /* SỬA: Nền xám nhạt để nổi bật */
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem;
        background-color: #F0F2F6; /* SỬA: Nền xám nhạt */
        color: #333 !important; 
    }
    /* SỬA LỖI: Tiêu đề sidebar (Quản lý danh sách) */
    div[data-testid="stSidebarUserContent"] h1 {
        color: #111111 !important;
        background: none !important;
        padding: 0 !important;
        font-size: 1.75rem !important;
        text-align: left !important;
        margin: 0 !important; /* Reset margin */
    }
    /* SỬA LỖI: Buộc nhãn trong form sidebar có màu tối */
    div[data-testid="stSidebarUserContent"] .stTextInput > label {
        color: #333 !important;
    }
    /* SỬA LỖI: Nút bấm trong sidebar form */
    div[data-testid="stSidebarUserContent"] .stButton button {
        background-color: #007BFF !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 8px 0px !important;
        width: 100% !important;
    }
    div[data-testid="stSidebarUserContent"] .stButton button:hover {
        background-color: #0056b3 !important;
    }
    
    /* --- Tùy chỉnh st.radio trong sidebar để trông giống Menu --- */
    div[data-testid="stRadio"] label {
        display: block;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 5px;
        font-weight: 500;
        font-size: 1.1rem;
        color: #333 !important; /* SỬA LỖI: Buộc chữ màu tối */
        transition: background-color 0.2s, color 0.2s;
        /* MỚI: Cho phép tên dài xuống dòng */
        white-space: normal;
        word-break: break-word;
    }
    /* Khi một mục được chọn */
    div[data-testid="stRadio"] input:checked + label {
        background-color: #e6f7ff; 
        color: #007BFF !important; /* SỬA LỖI: Buộc chữ màu xanh */
        font-weight: bold;
    }
    /* SỬA: Khi di chuột qua (trên nền xám) */
    div[data-testid="stRadio"] label:hover {
        background-color: #FFFFFF; /* SỬA: Nền trắng khi di chuột */
        color: #007BFF !important; 
    }
    /* SỬA LỖI: Buộc ẩn dấu chấm tròn của radio button */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important; 
    }

    /* --- Tiêu đề chính (Header) --- */
    /* SỬA LỖI: Chỉ target h1 trong main content */
    div[data-testid="stAppViewContainer"] > div > section[data-testid="stBlock"] h1 {
        background-color: #003366; /* GIỮ NGUYÊN: Nền xanh đậm */
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        text-align: left;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: -50px; 
    }

    /* --- Form nhập liệu --- */
    div[data-testid="stForm"] {
        background-color: #F0F2F6; /* Nền xám nhạt */
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05); /* Giảm nhẹ shadow */
    }
            
    /* --- Nút bấm chính (Thêm công việc) --- */
    div[data-testid="stForm"] .stButton button {
        background-color: #007BFF; 
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 0px;
        width: 100%;
        font-weight: bold;
    }
    div[data-testid="stForm"] .stButton button:hover {
        background-color: #0056b3;
    }
    
    /* --- Tạo kiểu cho các card công việc (nền xám nhạt) --- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
         background-color: #F0F2F6; /* Nền xám nhạt */
         border: 1px solid #E0E0E0 !important; /* Border xám nhạt hơn */
         border-radius: 10px !important;
         padding: 0.5rem 1rem 1rem 1rem; /* Thêm padding bên trong card */
    }
    
    /* --- Class CSS cho Deadline --- */
    .deadline-overdue { color: #D32F2F; font-weight: bold; text-align: center; }
    .deadline-today { color: #F57C00; font-weight: bold; text-align: center; }
    .deadline-normal { color: #6c757d; text-align: center; }

    /* --- Gạch ngang chữ khi task hoàn thành --- */
    div[data-testid="stCheckbox"] input:checked + label {
        text-decoration: line-through;
        color: #6c757d; 
    }

    /* --- Tùy chỉnh st.info --- */
    div[data-testid="stInfo"] {
        background-color: #e6f7ff !important; 
        border: 1px solid #b0e0ff !important; 
        color: #003366 !important; /* SỬA LỖI: Buộc màu chữ ở đây */
        border-radius: 5px !important;
    }
    div[data-testid="stInfo"] p { 
        color: #003366 !important; /* ...và ở đây cho chắc */
    }
</style>
""", unsafe_allow_html=True)


# --- Khởi tạo Session State cho nhiều danh sách ---
if "projects" not in st.session_state:
    # Khởi tạo với 3 danh sách mẫu
    st.session_state.projects = {
        "Hôm nay": [],
        "Công việc": [],
        "Mua sắm": []
    }
if "current_project" not in st.session_state:
    st.session_state.current_project = "Hôm nay" # Đặt nhóm mặc định

# Thêm state để theo dõi công việc đang được chỉnh sửa
if "editing_task_key" not in st.session_state:
    st.session_state.editing_task_key = None

# --- ================== SIDEBAR ================== ---
st.sidebar.title("Nhóm công việc")

# Form để thêm nhóm mới
with st.sidebar.form("new_project_form"):
    new_project_name = st.text_input("Nhóm mới")
    submitted_project = st.form_submit_button("➕ Thêm nhóm")
    if submitted_project and new_project_name:
        if new_project_name not in st.session_state.projects:
            st.session_state.projects[new_project_name] = []
            st.sidebar.success(f"Đã thêm '{new_project_name}'!")
        else:
            st.sidebar.error("Nhóm này đã tồn tại.")

st.sidebar.write("---")

# === MỚI: Logic hiển thị st.radio với số lượng công việc ===
project_names_formatted = [] # Nhóm tên để hiển thị (ví dụ: "Công việc (3)")
project_names_clean = []     # Nhóm tên gốc (ví dụ: "Công việc")

# Đảm bảo `current_project` vẫn tồn tại, nếu không thì reset
if st.session_state.current_project not in st.session_state.projects:
    if st.session_state.projects:
        st.session_state.current_project = list(st.session_state.projects.keys())[0]
    else:
        st.session_state.current_project = None # Trường hợp không có dự án nào

# Tìm index của dự án hiện tại
current_project_index = 0
try:
    # Tạo Nhóm tên và đếm số công việc
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
    st.error(f"Lỗi khi tải nhóm: {e}") # Xử lý lỗi nếu có


if st.session_state.current_project:
    selected_project_formatted = st.sidebar.radio(
        "Chọn nhóm:",
        project_names_formatted,
        index=current_project_index, # Đặt mục đang chọn
        label_visibility="collapsed" # Ẩn nhãn "Chọn nhóm:"
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
    st.info("Hãy tạo nhóm đầu tiên của bạn ở thanh bên trái để bắt đầu.")
else:
    # Lấy danh sách công việc của dự án hiện tại
    current_tasks = st.session_state.projects[st.session_state.current_project]

    # Tiêu đề chính
    st.title(f"{st.session_state.current_project}")

    # --- Form nhập liệu công việc ---
    with st.form("task_form"):
        col1, col2 = st.columns([3, 1]) 
        with col1:
            new_task = st.text_input("Thêm công việc mới", placeholder="Ví dụ: Họp với đội Marketing")
        with col2:
            deadline = st.date_input("Hạn chót", value=date.today())

        submitted = st.form_submit_button("Thêm Công Việc")
        if submitted and new_task:
            # Thêm công việc vào nhóm hiện tại
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