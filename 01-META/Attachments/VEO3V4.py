# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, simpledialog, messagebox
import threading
import time
import os
import json
from datetime import datetime
import queue
import uuid
import shutil

# --- PHẦN IMPORT SELENIUM ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

# --- CÁC HÀM LOGIC ---

def parse_cookies_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            cookie_string = content.split(';Dùng python')[0] if ';Dùng python' in content else content
        cookies_list = []
        for pair in cookie_string.split(';'):
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies_list.append({'name': name.strip(), 'value': value.strip()})
        return cookies_list
    except Exception:
        return None

def wait_for_download_and_get_filepath(directory, timeout):
    seconds = 0
    while seconds < timeout:
        files = os.listdir(directory)
        completed_downloads = [f for f in files if not f.endswith(('.crdownload', '.tmp')) and not f.startswith('.com.google.Chrome')]
        if completed_downloads:
            return os.path.join(directory, completed_downloads[0])
        time.sleep(1)
        seconds += 1
    return None

def run_single_automation_task(task_data, ui_callbacks):
    prompt_index = task_data['prompt_index']
    prompt_text = task_data['prompt_text']
    cookie_path = task_data['cookie_path']
    is_headless = task_data['is_headless']
    is_upscale = task_data['is_upscale']
    run_folder = task_data['run_folder']
    
    cookie_filename = os.path.basename(cookie_path)
    log = lambda msg: ui_callbacks['log'](f"[Prompt {prompt_index+1} | {cookie_filename}] {msg}")
    update_status = lambda status, link="": ui_callbacks['update_prompt_status'](task_data['item_id'], status, link)
    
    # --- START: Logic thử lại (Retry) mới ---
    MAX_PROMPT_RETRIES = 3
    RETRY_DELAY_SECONDS = 60

    for attempt in range(MAX_PROMPT_RETRIES):
        log(f"Bắt đầu xử lý... (Lần thử {attempt + 1}/{MAX_PROMPT_RETRIES})")
        if attempt > 0:
            update_status(f"Đang chạy (Thử lại {attempt})")
        else:
            update_status("Đang chạy...")

        driver = None
        temp_download_folder = os.path.join(run_folder, f"temp_prompt_{prompt_index + 1}_{uuid.uuid4().hex[:6]}")
        os.makedirs(temp_download_folder, exist_ok=True)

        try:
            options = ChromeOptions()
            prefs = {"download.default_directory": temp_download_folder, "download.prompt_for_download": False}
            options.add_experimental_option("prefs", prefs)
            if is_headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            else:
                options.add_argument("--start-maximized")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            URL = "https://labs.google/fx/vi/tools/flow"
            driver.get(URL)
            log("Đang nạp cookie...")
            cookies = parse_cookies_from_file(cookie_path)
            if not cookies: raise ValueError("Không đọc được cookie từ file.")
            for cookie in cookies: driver.add_cookie(cookie)
            
            log("Tải lại trang để áp dụng cookie...")
            driver.refresh()
            
            wait = WebDriverWait(driver, 40)
            log("Đang tìm nút 'Dự án mới'...")
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Dự án mới')]"))).click()
            except TimeoutException:
                log("Lỗi: Cookie không hợp lệ hoặc hết hạn. Tác vụ này sẽ không được thử lại.")
                update_status("Lỗi Cookie")
                return # Thoát hoàn toàn, không thử lại với cookie lỗi

            time.sleep(1)
            log("Đang cài đặt...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//i[text()='tune']]"))).click()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Câu trả lời đầu ra cho mỗi câu lệnh')]"))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@role='option'])[1]"))).click()
            time.sleep(1)
            log("Đang nhập câu lệnh...")
            prompt_textarea = wait.until(EC.presence_of_element_located((By.ID, "PINHOLE_TEXT_AREA_ELEMENT_ID")))
            prompt_textarea.send_keys(prompt_text)
            time.sleep(2)
            prompt_textarea.send_keys(Keys.ENTER)
            log("Đang chờ video được tạo (tối đa 5 phút)...")
            video_container = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-5ce3bf72-0') and .//video]")))
            actions = ActionChains(driver)
            actions.move_to_element(video_container).perform()
            log("Đang mở menu tải xuống...")
            download_icon_xpath = "//button[.//i[text()='download']]"
            wait.until(EC.element_to_be_clickable((By.XPATH, download_icon_xpath))).click()
            
            downloaded_filepath_temp = None
            max_download_retries = 3
            
            for download_attempt in range(max_download_retries):
                log(f"Bắt đầu quá trình tải xuống (lần thử {download_attempt + 1}/{max_download_retries})...")
                
                if is_upscale:
                    log("Chế độ 1080p được chọn...")
                    upscale_option_xpath = "//div[@role='menuitem' and contains(., 'Đã tăng độ phân giải (1080p)')]"
                    wait.until(EC.element_to_be_clickable((By.XPATH, upscale_option_xpath))).click()
                    log("Đang chờ tăng độ phân giải (tối đa 5 phút)...")
                    download_link_xpath = "//a[contains(@class, 'sc-3d001f83-0') and text()='Tải xuống']"
                    download_link = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.XPATH, download_link_xpath)))
                    download_link.click()
                else:
                    log("Chế độ 720p được chọn...")
                    size_option_xpath = "//div[@role='menuitem' and contains(., 'Kích thước gốc (720p)')]"
                    wait.until(EC.element_to_be_clickable((By.XPATH, size_option_xpath))).click()
                
                log("Chờ 5 giây để quá trình tải bắt đầu...")
                time.sleep(5)
                log(f"Bắt đầu quét thư mục tạm: '{os.path.basename(temp_download_folder)}'")
                downloaded_filepath_temp = wait_for_download_and_get_filepath(temp_download_folder, 120)

                if downloaded_filepath_temp:
                    log("Xác nhận tải file thành công vào thư mục tạm!")
                    break
                else:
                    log(f"Tải xuống không thành công trong lần thử {download_attempt + 1}. Chuẩn bị thử lại...")
                    if download_attempt < max_download_retries - 1:
                        time.sleep(10)
                        log("Mở lại menu tải xuống...")
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(1)
                        wait.until(EC.element_to_be_clickable((By.XPATH, download_icon_xpath))).click()
            
            if downloaded_filepath_temp:
                log(f"Đã tải xong: {os.path.basename(downloaded_filepath_temp)}")
                file_number = prompt_index + 1
                timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
                base_new_filename = f"{file_number:03d}_{timestamp_str}"
                new_filename = f"{base_new_filename}.mp4"
                final_filepath = os.path.join(run_folder, new_filename)
                counter = 1
                while os.path.exists(final_filepath):
                    new_filename = f"{base_new_filename}_({counter}).mp4"
                    final_filepath = os.path.join(run_folder, new_filename)
                    counter += 1
                
                try:
                    log(f"Di chuyển và đổi tên file thành '{new_filename}'...")
                    shutil.move(downloaded_filepath_temp, final_filepath)
                    log("Thành công.")
                    update_status("Hoàn thành", link=final_filepath)
                    return # Thành công, thoát khỏi hàm và vòng lặp thử lại
                except OSError as e:
                    log(f"Lỗi khi di chuyển/đổi tên file: {e}")
                    raise Exception("Lỗi đổi tên file.") # Gây ra lỗi để thử lại
            else:
                log("Lỗi: Tải xuống thất bại sau nhiều lần thử.")
                raise Exception("Lỗi tải file.") # Gây ra lỗi để thử lại

        except Exception as e:
            log(f"Lỗi ở lần thử {attempt + 1}: {e}")
            if attempt < MAX_PROMPT_RETRIES - 1:
                log(f"Sẽ thử lại sau {RETRY_DELAY_SECONDS} giây.")
                update_status(f"Lỗi, thử lại sau 1 phút...")
                time.sleep(RETRY_DELAY_SECONDS) # Chờ 1 phút trước khi thử lại
            else:
                log("Đã hết số lần thử lại. Hủy bỏ prompt này.")
                update_status("Lỗi")
        
        finally:
            if driver:
                driver.quit()
            if os.path.exists(temp_download_folder):
                try:
                    shutil.rmtree(temp_download_folder)
                except OSError as e:
                    log(f"Lỗi khi dọn dẹp thư mục tạm: {e}")
    # --- END: Logic thử lại (Retry) mới ---

# --- PHẦN GIAO DIỆN NGƯỜI DÙNG (TKINTER) ---
class AutomationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Công Cụ Tự Động Google Flow VEO3")
        self.master.geometry("1000x800")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.CONFIG_FILE = "config.json"
        self.load_config()
        
        self.current_prompts = []
        self.cookie_paths = []
        self.is_running = False
        self.task_queue = queue.Queue()
        
        self.interactive_widgets = []
        
        self.create_widgets()
        self.load_default_prompts()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)
        cookie_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(cookie_tab, text='1. Nạp & Quản lý Cookie')
        self.create_cookie_tab_widgets(cookie_tab)
        run_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(run_tab, text='2. Cấu hình & Chạy')
        self.create_run_tab_widgets(run_tab)

    def create_cookie_tab_widgets(self, parent_frame):
        cookie_list_frame = ttk.LabelFrame(parent_frame, text="Danh sách File Cookie đã nạp", padding="10")
        cookie_list_frame.pack(fill=tk.BOTH, expand=True)
        cookie_cols = ("#", "Đường dẫn File Cookie")
        self.cookie_tree = ttk.Treeview(cookie_list_frame, columns=cookie_cols, show="headings", height=5)
        self.cookie_tree.heading("#", text="#", anchor='center')
        self.cookie_tree.heading("Đường dẫn File Cookie", text="Đường dẫn File Cookie")
        self.cookie_tree.column("#", width=50, anchor='center')
        self.cookie_tree.column("Đường dẫn File Cookie", width=700)
        ysb_cookie = ttk.Scrollbar(cookie_list_frame, orient=tk.VERTICAL, command=self.cookie_tree.yview)
        xsb_cookie = ttk.Scrollbar(cookie_list_frame, orient=tk.HORIZONTAL, command=self.cookie_tree.xview)
        self.cookie_tree.configure(yscrollcommand=ysb_cookie.set, xscrollcommand=xsb_cookie.set)
        self.cookie_tree.grid(row=0, column=0, sticky='nsew')
        ysb_cookie.grid(row=0, column=1, sticky='ns')
        xsb_cookie.grid(row=1, column=0, sticky='ew')
        cookie_list_frame.grid_rowconfigure(0, weight=1)
        cookie_list_frame.grid_columnconfigure(0, weight=1)
        cookie_action_frame = ttk.Frame(parent_frame, padding=(0, 10))
        cookie_action_frame.pack(fill=tk.X)
        
        add_cookie_btn = ttk.Button(cookie_action_frame, text="Thêm File Cookie...", command=self.browse_cookie_files)
        add_cookie_btn.pack(side=tk.LEFT, padx=5)
        remove_selected_btn = ttk.Button(cookie_action_frame, text="Xóa Cookie đã chọn", command=self.remove_selected_cookie)
        remove_selected_btn.pack(side=tk.LEFT, padx=5)
        remove_all_btn = ttk.Button(cookie_action_frame, text="Xóa tất cả Cookie", command=self.remove_all_cookies)
        remove_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.interactive_widgets.extend([add_cookie_btn, remove_selected_btn, remove_all_btn])

    def create_run_tab_widgets(self, parent_frame):
        main_frame = ttk.Frame(parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        prompt_frame = ttk.Frame(main_frame)
        prompt_frame.pack(fill=tk.X, pady=2)
        ttk.Label(prompt_frame, text="Chọn file prompt (.txt):", width=22).pack(side=tk.LEFT)
        self.prompt_filepath_var = tk.StringVar()
        prompt_entry = ttk.Entry(prompt_frame, textvariable=self.prompt_filepath_var, state='readonly')
        prompt_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        browse_prompt_btn = ttk.Button(prompt_frame, text="Chọn File...", command=self.browse_prompt_file)
        browse_prompt_btn.pack(side=tk.LEFT)
        
        self.interactive_widgets.append(browse_prompt_btn)
        
        prompt_display_frame = ttk.LabelFrame(main_frame, text="Danh sách Prompts", padding="10")
        prompt_display_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        cols = ("#", "Prompt", "Cookie sử dụng", "Trạng thái", "Tên Videos")
        self.prompt_tree = ttk.Treeview(prompt_display_frame, columns=cols, show="headings", height=10)
        for col in cols: self.prompt_tree.heading(col, text=col)
        self.prompt_tree.column("#", width=40, anchor='center')
        self.prompt_tree.column("Prompt", width=400)
        self.prompt_tree.column("Cookie sử dụng", width=120, anchor='center')
        self.prompt_tree.column("Trạng thái", width=100, anchor='center')
        self.prompt_tree.column("Tên Videos", width=150)
        ysb = ttk.Scrollbar(prompt_display_frame, orient=tk.VERTICAL, command=self.prompt_tree.yview)
        xsb = ttk.Scrollbar(prompt_display_frame, orient=tk.HORIZONTAL, command=self.prompt_tree.xview)
        self.prompt_tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.prompt_tree.grid(row=0, column=0, sticky='nsew')
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        prompt_display_frame.grid_rowconfigure(0, weight=1)
        prompt_display_frame.grid_columnconfigure(0, weight=1)
        self.create_controls_and_log_widgets(main_frame)

    def create_controls_and_log_widgets(self, parent_frame):
        bottom_frame = ttk.Frame(parent_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        control_frame = ttk.Frame(bottom_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Label(control_frame, text="Số luồng:").grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.threads_var = tk.IntVar(value=self.config.get('threads', 4))
        self.threads_spinbox = ttk.Spinbox(control_frame, from_=1, to=20, textvariable=self.threads_var, width=5)
        self.threads_spinbox.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        # --- CHANGE: Headless Checkbutton REMOVED from UI ---
        
        self.upscale_var = tk.BooleanVar(value=self.config.get('upscale', False))
        upscale_check = ttk.Checkbutton(control_frame, text="Tải xuống 1080p (chậm hơn)", variable=self.upscale_var)
        upscale_check.grid(row=1, column=0, columnspan=2, sticky='w', padx=5)

        self.interactive_widgets.extend([self.threads_spinbox, upscale_check])

        action_frame = ttk.Frame(bottom_frame)
        action_frame.pack(side=tk.RIGHT)
        self.start_button = ttk.Button(action_frame, text="Bắt đầu chạy", command=self.start_automation, style="Accent.TButton")
        self.start_button.pack(ipadx=20, ipady=10)
        style = ttk.Style()
        style.configure("Accent.TButton", font=('Helvetica', 12, 'bold'))
        log_frame = ttk.LabelFrame(parent_frame, text="Nhật ký hoạt động", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10, state='disabled', font=("Courier New", 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def browse_cookie_files(self):
        filenames = filedialog.askopenfilenames(title="Chọn các file cookie", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if not filenames: return
        added_count = 0
        for fname in filenames:
            if fname not in self.cookie_paths:
                self.cookie_paths.append(fname)
                self.cookie_tree.insert("", "end", values=(len(self.cookie_paths), fname))
                added_count += 1
        if added_count > 0: self.log_message(f"Đã thêm {added_count} file cookie mới.")
        else: self.log_message("Không có file cookie mới nào được thêm (có thể đã tồn tại).")

    def remove_selected_cookie(self):
        selected_items = self.cookie_tree.selection()
        if not selected_items:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn cookie cần xóa từ danh sách.")
            return
        for item_id in selected_items:
            values = self.cookie_tree.item(item_id, 'values')
            path_to_remove = values[1]
            if path_to_remove in self.cookie_paths:
                self.cookie_paths.remove(path_to_remove)
        self._repopulate_cookie_tree()
        self.log_message(f"Đã xóa {len(selected_items)} cookie.")

    def remove_all_cookies(self):
        if not self.cookie_paths: return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả các cookie đã nạp?"):
            self.cookie_paths.clear()
            self._repopulate_cookie_tree()
            self.log_message("Đã xóa tất cả cookie.")

    def _repopulate_cookie_tree(self):
        for i in self.cookie_tree.get_children(): self.cookie_tree.delete(i)
        for i, path in enumerate(self.cookie_paths): self.cookie_tree.insert("", "end", values=(i + 1, path))

    def browse_prompt_file(self):
        filename = filedialog.askopenfilename(title="Chọn file prompt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.prompt_filepath_var.set(filename)
            self._populate_prompts_from_filepath(filename)
    
    def _populate_prompts_from_filepath(self, filepath):
        self.prompt_tree.delete(*self.prompt_tree.get_children())
        self.current_prompts = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                prompts = [line.strip() for line in f if line.strip()]
            if not prompts:
                self.log_message(f"Cảnh báo: File '{os.path.basename(filepath)}' trống.")
                return
            self.current_prompts = prompts
            for i, prompt in enumerate(self.current_prompts):
                display_prompt = prompt[:100] + '...' if len(prompt) > 100 else prompt
                self.prompt_tree.insert("", "end", values=(i+1, display_prompt, "Chưa phân", "Chờ", "-"))
            self.log_message(f"Đã tải {len(prompts)} prompts từ '{os.path.basename(filepath)}'.")
        except FileNotFoundError: self.log_message(f"Lỗi: Không tìm thấy file '{filepath}'.")

    # --- CHANGE: Default headless to True ---
    def load_config(self):
        try:
            with open(self.CONFIG_FILE, 'r') as f: self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError): 
            self.config = {'threads': 4, 'headless': True, 'upscale': False}

    # --- CHANGE: Don't save headless from a UI var, preserve the loaded value ---
    def save_config(self):
        self.config['threads'] = self.threads_var.get()
        self.config['upscale'] = self.upscale_var.get()
        # The 'headless' key is preserved from when it was loaded.
        with open(self.CONFIG_FILE, 'w') as f: json.dump(self.config, f, indent=4)

    def load_default_prompts(self):
        if not os.path.exists("prompts.txt"):
            with open("prompts.txt", "w", encoding='utf-8') as f: pass
        self.prompt_filepath_var.set(os.path.abspath("prompts.txt"))
        self._populate_prompts_from_filepath("prompts.txt")

    def log_message(self, message):
        def _log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_area.see(tk.END)
            self.log_area.config(state='disabled')
        self.master.after(0, _log)
    
    def toggle_controls(self, enable=True):
        state = 'normal' if enable else 'disabled'
        self.start_button.config(state=state)
        self.notebook.tab(0, state=state)
        for widget in self.interactive_widgets:
            if isinstance(widget, ttk.Entry):
                widget.config(state='readonly' if not enable else 'normal')
            else:
                widget.config(state=state)

    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("Thoát", "Tác vụ đang chạy. Bạn có chắc muốn thoát?"):
                self.save_config()
                self.master.destroy()
        else:
            self.save_config()
            self.master.destroy()

    def start_automation(self):
        if not self.cookie_paths:
            messagebox.showerror("Thiếu thông tin", "Vui lòng nạp ít nhất một file cookie ở tab 1.")
            self.notebook.select(0)
            return
        if not self.current_prompts:
            messagebox.showerror("Thiếu thông tin", "Vui lòng chọn file prompt có nội dung.")
            return
            
        self.is_running = True
        self.toggle_controls(enable=False)
        
        setup_thread = threading.Thread(target=self._setup_and_run_tasks, daemon=True)
        setup_thread.start()

    def _setup_and_run_tasks(self):
        try:
            self.log_message("--- BẮT ĐẦU QUÁ TRÌNH TẠO VIDEO HÀNG LOẠT ---")
            
            base_download_folder = os.path.abspath("videos_downloaded")
            os.makedirs(base_download_folder, exist_ok=True)
            run_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            run_specific_folder = os.path.join(base_download_folder, f"run_{run_timestamp}")
            os.makedirs(run_specific_folder)
            
            self.log_message(f"Video cho lần chạy này sẽ được lưu vào: '{run_specific_folder}'")
            
            prompts_items = self.prompt_tree.get_children()
            num_cookies = len(self.cookie_paths)
            
            ui_updates_batch = []
            
            # --- CHANGE: Read headless value from self.config dictionary ---
            is_headless = self.config.get('headless', True)
            if is_headless:
                self.log_message("Chế độ chạy ẩn (Headless) đang được BẬT (theo file config).")
            else:
                self.log_message("Chế độ chạy ẩn (Headless) đang được TẮT (theo file config).")


            for i, item_id in enumerate(prompts_items):
                assigned_cookie_path = self.cookie_paths[i % num_cookies]
                
                task = {
                    'item_id': item_id, 'prompt_index': i, 
                    'prompt_text': self.current_prompts[i], 
                    'cookie_path': assigned_cookie_path,
                    'is_headless': is_headless, 
                    'is_upscale': self.upscale_var.get(), 
                    'run_folder': run_specific_folder
                } 
                self.task_queue.put(task)
                
                assigned_cookie_name = os.path.basename(assigned_cookie_path)
                ui_updates_batch.append((item_id, assigned_cookie_name))
            
            self.master.after(0, self._batch_update_ui, ui_updates_batch)

            num_threads = self.threads_var.get()
            self.log_message(f"Đã chuẩn bị {len(prompts_items)} tác vụ. Bắt đầu chạy với {num_threads} luồng...")

            self.threads = []
            for _ in range(num_threads):
                thread = threading.Thread(target=self.worker)
                thread.daemon = True
                self.threads.append(thread)
                thread.start()
            
            self.master.after(100, self.monitor_queue)
        except Exception as e:
            self.log_message(f"Lỗi nghiêm trọng khi thiết lập tác vụ: {e}")
            self.is_running = False
            self.master.after(0, self.toggle_controls, True)

    def _batch_update_ui(self, updates_list):
        try:
            for item_id, cookie_name in updates_list:
                current_values = list(self.prompt_tree.item(item_id, 'values'))
                current_values[2] = cookie_name
                self.prompt_tree.item(item_id, values=tuple(current_values))
        except tk.TclError:
            pass

    def worker(self):
        ui_callbacks = {'log': self.log_message, 'update_prompt_status': self.update_prompt_status_from_thread}
        while not self.task_queue.empty():
            try:
                task_data = self.task_queue.get_nowait()
                run_single_automation_task(task_data, ui_callbacks)
                self.task_queue.task_done()
            except queue.Empty: break
            except Exception as e: self.log_message(f"Lỗi nghiêm trọng trong worker: {e}")

    def monitor_queue(self):
        if not self.task_queue.empty() or any(t.is_alive() for t in self.threads):
            self.master.after(1000, self.monitor_queue)
        else:
            self.log_message("\n=== HOÀN THÀNH TẤT CẢ CÁC PROMPT! ===")
            self.is_running = False
            self.toggle_controls(enable=True)
            messagebox.showinfo("Hoàn thành", "Đã xử lý xong tất cả các prompt.")

    def update_prompt_status_from_thread(self, item_id, status, link=""):
        self.master.after(0, self.update_prompt_status, item_id, status, link)
    
    def update_prompt_status(self, item_id, status, link=""):
        try:
            current_values = list(self.prompt_tree.item(item_id, 'values'))
            current_values[3] = status
            if link:
                current_values[4] = os.path.basename(link)
            self.prompt_tree.item(item_id, values=tuple(current_values))
        except tk.TclError: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()
