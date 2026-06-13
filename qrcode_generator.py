import tkinter as tk
from tkinter import messagebox, filedialog, ttk, colorchooser
import qrcode
from PIL import Image, ImageTk, ImageDraw
import os
import threading
import time


class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("二维码生成器")
        self.root.configure(bg="#f5f5f5")
        
        self.current_qr_image = None
        self.current_text = ""
        self.dynamic_running = False
        self.dynamic_thread = None
        
        # 样式设置
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.logo_path = None
        self.border_width = 2
        self.output_size = 200
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ===== 输入区域 =====
        input_frame = tk.LabelFrame(main_frame, text="输入内容", bg="#f5f5f5", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 文本框
        self.entry = tk.Entry(input_frame, width=50, font=("Arial", 11))
        self.entry.pack(fill=tk.X, pady=(5, 10))
        
        # 输入按钮行
        btn_row = tk.Frame(input_frame, bg="#f5f5f5")
        btn_row.pack(fill=tk.X)
        
        tk.Button(btn_row, text="从剪贴板粘贴", command=self.paste_from_clipboard, 
                  width=12, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_row, text="复制文本", command=self.copy_text, 
                  width=12, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=5)
        
        # ===== 样式设置区域 =====
        style_frame = tk.LabelFrame(main_frame, text="样式设置", bg="#f5f5f5", padx=10, pady=10)
        style_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：颜色设置
        row1 = tk.Frame(style_frame, bg="#f5f5f5")
        row1.pack(fill=tk.X, pady=5)
        
        # 前景色
        tk.Label(row1, text="前景色：", bg="#f5f5f5").pack(side=tk.LEFT)
        self.fill_color_label = tk.Label(row1, text="  ", bg=self.fill_color, width=3, relief=tk.RAISED)
        self.fill_color_label.pack(side=tk.LEFT, padx=(5, 10))
        tk.Button(row1, text="选择", command=self.choose_fill_color, width=6, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT)
        
        # 背景色
        tk.Label(row1, text="背景色：", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20, 0))
        self.back_color_label = tk.Label(row1, text="  ", bg=self.back_color, width=3, relief=tk.RAISED)
        self.back_color_label.pack(side=tk.LEFT, padx=(5, 10))
        tk.Button(row1, text="选择", command=self.choose_back_color, width=6, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT)
        
        # Logo
        tk.Label(row1, text="Logo：", bg="#f5f5f5").pack(side=tk.LEFT, padx=(20, 0))
        self.logo_label = tk.Label(row1, text="未选择", bg="#f5f5f5", width=10)
        self.logo_label.pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="选择", command=self.choose_logo, width=6, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=2)
        tk.Button(row1, text="清除", command=self.clear_logo, width=6, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=2)
        
        # 第二行：参数设置
        row2 = tk.Frame(style_frame, bg="#f5f5f5")
        row2.pack(fill=tk.X, pady=5)
        
        # 边框宽度（输入框）
        tk.Label(row2, text="边框宽度 (0-10)：", bg="#f5f5f5").pack(side=tk.LEFT)
        self.border_entry = tk.Entry(row2, width=5, font=("Arial", 11))
        self.border_entry.insert(0, "2")
        self.border_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # 输出尺寸（输入框）
        tk.Label(row2, text="输出尺寸 (100-800)：", bg="#f5f5f5").pack(side=tk.LEFT)
        self.size_entry = tk.Entry(row2, width=6, font=("Arial", 11))
        self.size_entry.insert(0, "200")
        self.size_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # 容错级别
        tk.Label(row2, text="容错级别：", bg="#f5f5f5").pack(side=tk.LEFT)
        self.error_level_var = tk.StringVar(value="中")
        error_combobox = ttk.Combobox(row2, textvariable=self.error_level_var, 
                                       values=["低", "中", "高"], width=5, state="readonly")
        error_combobox.pack(side=tk.LEFT, padx=(5, 20))
        
        # 保存格式
        tk.Label(row2, text="保存格式：", bg="#f5f5f5").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="PNG")
        format_combobox = ttk.Combobox(row2, textvariable=self.format_var,
                                        values=["PNG", "JPG", "SVG", "PDF"], width=5, state="readonly")
        format_combobox.pack(side=tk.LEFT, padx=5)
        
        # ===== 功能按钮区域 =====
        func_frame = tk.Frame(main_frame, bg="#f5f5f5")
        func_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(func_frame, text="生成二维码", command=self.generate_qr, 
                  width=14, bg="#757575", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.dynamic_button = tk.Button(func_frame, text="启动动态监测", command=self.toggle_dynamic, 
                                         width=14, bg="#9E9E9E", fg="white")
        self.dynamic_button.pack(side=tk.LEFT, padx=5)
        tk.Button(func_frame, text="批量生成", command=self.open_batch_window, 
                  width=14, bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(func_frame, text="Wi-Fi二维码", command=self.open_wifi_window, 
                  width=14, bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=5)
        
        # ===== 预览区域 =====
        preview_frame = tk.LabelFrame(main_frame, text="二维码预览", bg="#f5f5f5", padx=10, pady=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 二维码显示区域
        self.qr_label = tk.Label(preview_frame, text="请输入内容并点击生成", 
                                  bg="white", relief=tk.SUNKEN, font=("Arial", 12))
        self.qr_label.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # ===== 底部区域 =====
        bottom_frame = tk.Frame(main_frame, bg="#f5f5f5")
        bottom_frame.pack(fill=tk.X)
        
        # 状态标签
        self.status_label = tk.Label(bottom_frame, text="", fg="#616161", bg="#f5f5f5", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT)
        
        # 保存按钮（初始禁用）
        self.save_button = tk.Button(bottom_frame, text="保存图片", command=self.save_image, 
                                      state=tk.DISABLED, width=12, bg="#BDBDBD", fg="#424242")
        self.save_button.pack(side=tk.RIGHT)
    
    def choose_fill_color(self):
        """选择前景色"""
        color = colorchooser.askcolor(title="选择前景色", initialcolor=self.fill_color)
        if color[1]:
            self.fill_color = color[1]
            self.fill_color_label.config(bg=self.fill_color)
    
    def choose_back_color(self):
        """选择背景色"""
        color = colorchooser.askcolor(title="选择背景色", initialcolor=self.back_color)
        if color[1]:
            self.back_color = color[1]
            self.back_color_label.config(bg=self.back_color)
    
    def choose_logo(self):
        """选择Logo图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"), ("所有文件", "*.*")]
        )
        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_label.config(text=filename[:8] + "..." if len(filename) > 8 else filename)
    
    def clear_logo(self):
        """清除Logo"""
        self.logo_path = None
        self.logo_label.config(text="未选择")
    
    def get_style_params(self):
        """获取样式参数"""
        # 边框宽度
        try:
            border = int(self.border_entry.get())
            if border < 0:
                border = 0
            elif border > 10:
                border = 10
            self.border_width = border
        except ValueError:
            messagebox.showwarning("提示", "边框宽度必须是数字！")
            return False
        
        # 输出尺寸
        try:
            size = int(self.size_entry.get())
            if size < 100:
                size = 100
            elif size > 800:
                size = 800
            self.output_size = size
        except ValueError:
            messagebox.showwarning("提示", "输出尺寸必须是数字！")
            return False
        
        return True
    
    def get_error_level(self):
        """获取容错级别"""
        error_level_map = {
            "低": qrcode.constants.ERROR_CORRECT_L,
            "中": qrcode.constants.ERROR_CORRECT_M,
            "高": qrcode.constants.ERROR_CORRECT_H
        }
        return error_level_map[self.error_level_var.get()]
    
    def create_qr_image(self, text):
        """创建二维码图片"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=self.get_error_level(),
            box_size=10,
            border=self.border_width
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
        
        # 添加Logo
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path)
                qr_width, qr_height = img.size
                logo_max_size = qr_width // 4
                logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
                
                logo_width, logo_height = logo.size
                x = (qr_width - logo_width) // 2
                y = (qr_height - logo_height) // 2
                
                logo_bg = Image.new('RGBA', (logo_width + 10, logo_height + 10), 'white')
                logo_bg_pos = ((logo_width + 10 - logo_width) // 2, (logo_height + 10 - logo_height) // 2)
                
                if logo.mode != 'RGBA':
                    logo = logo.convert('RGBA')
                
                logo_bg.paste(logo, logo_bg_pos, logo)
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                img.paste(logo_bg, (x - 5, y - 5), logo_bg)
            except Exception as e:
                print(f"Logo处理失败: {e}")
        
        img = img.resize((self.output_size, self.output_size), Image.Resampling.LANCZOS)
        return img
    
    def generate_qr(self):
        """生成二维码"""
        text = self.entry.get().strip()
        
        if not text:
            messagebox.showwarning("提示", "请输入文本或网址！")
            return
        
        if not self.get_style_params():
            return
        
        self.current_text = text
        qr_image = self.create_qr_image(text)
        
        display_size = min(300, self.output_size)
        display_image = qr_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(display_image)
        
        self.qr_label.config(image=photo, text="")
        self.qr_label.image = photo
        
        self.current_qr_image = qr_image
        
        self.save_button.config(state=tk.NORMAL, bg="#757575", fg="white")
        self.status_label.config(text=f"生成成功 ({self.output_size}x{self.output_size})")
    
    def save_image(self):
        """保存二维码图片"""
        if self.current_qr_image is None:
            return
        
        file_format = self.format_var.get().lower()
        file_types = {
            "png": ("PNG 图片", "*.png"),
            "jpg": ("JPG 图片", "*.jpg"),
            "svg": ("SVG 文件", "*.svg"),
            "pdf": ("PDF 文件", "*.pdf")
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_format}",
            filetypes=[file_types[file_format], ("所有文件", "*.*")],
            title="保存二维码"
        )
        
        if file_path:
            try:
                if file_format == "svg":
                    import qrcode.image.svg
                    factory = qrcode.image.svg.SvgImage
                    img_svg = qrcode.make(self.current_text, image_factory=factory,
                                          fill_color=self.fill_color, back_color=self.back_color)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        img_svg.save(f)
                elif file_format == "pdf":
                    if self.current_qr_image.mode == 'RGBA':
                        rgb_image = Image.new('RGB', self.current_qr_image.size, 'white')
                        rgb_image.paste(self.current_qr_image, mask=self.current_qr_image.split()[-1])
                        rgb_image.save(file_path, "PDF")
                    else:
                        self.current_qr_image.save(file_path, "PDF")
                else:
                    self.current_qr_image.save(file_path, file_format.upper())
                messagebox.showinfo("成功", f"二维码已保存为 {file_format.upper()} 格式！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
    
    def copy_text(self):
        """复制文本框内容到剪贴板"""
        text = self.entry.get()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("成功", "文本已复制到剪贴板！")
        else:
            messagebox.showwarning("提示", "文本框为空！")
    
    def paste_from_clipboard(self):
        """从剪贴板粘贴到文本框"""
        try:
            text = self.root.clipboard_get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text)
        except tk.TclError:
            messagebox.showwarning("提示", "剪贴板为空！")
    
    def toggle_dynamic(self):
        """切换动态监测"""
        if self.dynamic_running:
            self.dynamic_running = False
            self.dynamic_button.config(text="启动动态监测", bg="#9E9E9E")
            self.status_label.config(text="动态监测已停止")
        else:
            text = self.entry.get().strip()
            if not text:
                messagebox.showwarning("提示", "请先输入URL！")
                return
            
            if not (text.startswith("http://") or text.startswith("https://")):
                messagebox.showwarning("提示", "动态监测仅支持URL！")
                return
            
            if not self.get_style_params():
                return
            
            self.dynamic_running = True
            self.current_text = text
            self.dynamic_button.config(text="停止动态监测", bg="#E57373")
            self.status_label.config(text="动态监测运行中...")
            
            self.dynamic_thread = threading.Thread(target=self.dynamic_monitor, daemon=True)
            self.dynamic_thread.start()
    
    def dynamic_monitor(self):
        """动态监测线程"""
        import urllib.request
        last_content = ""
        
        while self.dynamic_running:
            try:
                with urllib.request.urlopen(self.current_text, timeout=5) as response:
                    content = response.read().decode('utf-8', errors='ignore')
                    
                    if content != last_content:
                        last_content = content
                        self.root.after(0, self.update_dynamic_qr)
            except Exception:
                pass
            
            time.sleep(5)
    
    def update_dynamic_qr(self):
        """更新动态二维码"""
        if self.dynamic_running:
            qr_image = self.create_qr_image(self.current_text)
            display_size = min(300, self.output_size)
            display_image = qr_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(display_image)
            self.qr_label.config(image=photo, text="")
            self.qr_label.image = photo
            self.current_qr_image = qr_image
            self.save_button.config(state=tk.NORMAL, bg="#757575", fg="white")
    
    def open_batch_window(self):
        """打开批量生成窗口"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("批量生成二维码")
        batch_window.configure(bg="#f5f5f5")
        
        frame = tk.Frame(batch_window, bg="#f5f5f5", padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="选择TXT或CSV文件，每行生成一个二维码", bg="#f5f5f5").pack(pady=(0, 10))
        
        # 文件路径
        file_frame = tk.Frame(frame, bg="#f5f5f5")
        file_frame.pack(fill=tk.X, pady=5)
        tk.Label(file_frame, text="文件路径：", bg="#f5f5f5").pack(side=tk.LEFT)
        file_entry = tk.Entry(file_frame, width=40)
        file_entry.pack(side=tk.LEFT, padx=5)
        
        def browse_file():
            file_path = filedialog.askopenfilename(
                filetypes=[("文本文件", "*.txt"), ("CSV文件", "*.csv"), ("所有文件", "*.*")]
            )
            if file_path:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, file_path)
        
        tk.Button(file_frame, text="浏览", command=browse_file, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=5)
        
        # 保存目录
        dir_frame = tk.Frame(frame, bg="#f5f5f5")
        dir_frame.pack(fill=tk.X, pady=5)
        tk.Label(dir_frame, text="保存目录：", bg="#f5f5f5").pack(side=tk.LEFT)
        dir_entry = tk.Entry(dir_frame, width=40)
        dir_entry.pack(side=tk.LEFT, padx=5)
        
        def browse_dir():
            dir_path = filedialog.askdirectory()
            if dir_path:
                dir_entry.delete(0, tk.END)
                dir_entry.insert(0, dir_path)
        
        tk.Button(dir_frame, text="浏览", command=browse_dir, bg="#E0E0E0", fg="#424242").pack(side=tk.LEFT, padx=5)
        
        # 结果标签
        result_label = tk.Label(frame, text="", fg="#616161", bg="#f5f5f5")
        result_label.pack(pady=10)
        
        def generate_batch():
            file_path = file_entry.get().strip()
            save_dir = dir_entry.get().strip()
            
            if not file_path or not save_dir:
                messagebox.showwarning("提示", "请选择文件和保存目录！")
                return
            
            if not os.path.exists(file_path):
                messagebox.showerror("错误", "文件不存在！")
                return
            
            if not self.get_style_params():
                return
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                
                if not lines:
                    messagebox.showwarning("提示", "文件为空！")
                    return
                
                count = 0
                for i, line in enumerate(lines, 1):
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=self.get_error_level(),
                        box_size=10,
                        border=self.border_width
                    )
                    qr.add_data(line)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
                    img = img.resize((self.output_size, self.output_size), Image.Resampling.LANCZOS)
                    
                    filename = f"qrcode_{i:03d}.png"
                    filepath = os.path.join(save_dir, filename)
                    img.save(filepath, "PNG")
                    count += 1
                
                result_label.config(text=f"成功生成 {count} 个二维码！")
                messagebox.showinfo("成功", f"已生成 {count} 个二维码！")
            except Exception as e:
                messagebox.showerror("错误", f"生成失败：{str(e)}")
        
        tk.Button(frame, text="开始生成", command=generate_batch, 
                  width=15, bg="#757575", fg="white").pack(pady=10)
    
    def open_wifi_window(self):
        """打开Wi-Fi二维码生成窗口"""
        wifi_window = tk.Toplevel(self.root)
        wifi_window.title("Wi-Fi 二维码生成器")
        wifi_window.configure(bg="#f5f5f5")
        
        frame = tk.Frame(wifi_window, bg="#f5f5f5", padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # SSID
        tk.Label(frame, text="网络名称 (SSID)：", bg="#f5f5f5").pack(anchor=tk.W, pady=(0, 5))
        ssid_entry = tk.Entry(frame, width=30, font=("Arial", 11))
        ssid_entry.pack(fill=tk.X, pady=(0, 10))
        
        # 密码
        tk.Label(frame, text="密码：", bg="#f5f5f5").pack(anchor=tk.W, pady=(0, 5))
        password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 11))
        password_entry.pack(fill=tk.X, pady=(0, 5))
        
        show_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="显示密码", variable=show_var, bg="#f5f5f5",
                       command=lambda: password_entry.config(show="" if show_var.get() else "*")).pack(anchor=tk.W, pady=(0, 10))
        
        # 加密类型
        tk.Label(frame, text="加密类型：", bg="#f5f5f5").pack(anchor=tk.W, pady=(0, 5))
        encryption_var = tk.StringVar(value="WPA/WPA2")
        encryption_combo = ttk.Combobox(frame, textvariable=encryption_var, 
                                        values=["WPA/WPA2", "WEP", "无密码"], width=15, state="readonly")
        encryption_combo.pack(anchor=tk.W, pady=(0, 10))
        
        # 隐藏网络
        hidden_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="隐藏网络", variable=hidden_var, bg="#f5f5f5").pack(anchor=tk.W, pady=(0, 10))
        
        # 二维码显示
        qr_label = tk.Label(frame, text="点击生成按钮预览", bg="white", relief=tk.SUNKEN)
        qr_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        saved_image = [None]
        
        def generate_wifi_qr():
            ssid = ssid_entry.get().strip()
            password = password_entry.get()
            
            if not ssid:
                messagebox.showwarning("提示", "请输入网络名称！")
                return
            
            encryption_map = {
                "WPA/WPA2": "WPA",
                "WEP": "WEP",
                "无密码": "nopass"
            }
            encryption = encryption_map[encryption_var.get()]
            
            hidden = "H:true;" if hidden_var.get() else ""
            if encryption == "nopass":
                wifi_string = f"WIFI:T:nopass;S:{ssid};{hidden};;"
            else:
                wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};{hidden};;"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=2
            )
            qr.add_data(wifi_string)
            qr.make(fit=True)
            img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            qr_label.config(image=photo, text="")
            qr_label.image = photo
            saved_image[0] = img
        
        def save_wifi_qr():
            if saved_image[0] is None:
                messagebox.showwarning("提示", "请先生成二维码！")
                return
            
            ssid = ssid_entry.get().strip()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=f"wifi_{ssid}.png",
                filetypes=[("PNG 图片", "*.png"), ("所有文件", "*.*")],
                title="保存Wi-Fi二维码"
            )
            
            if file_path:
                saved_image[0].save(file_path, "PNG")
                messagebox.showinfo("成功", "Wi-Fi二维码已保存！")
        
        # 按钮
        btn_frame = tk.Frame(frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="生成二维码", command=generate_wifi_qr, 
                  width=12, bg="#757575", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="保存图片", command=save_wifi_qr, 
                  width=12, bg="#BDBDBD", fg="#424242").pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()