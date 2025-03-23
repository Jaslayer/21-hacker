import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # 用於顯示圖片

class ModeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("21好玩遊戲")
        self.root.attributes('-topmost', True)  # 視窗置頂
        self.root.geometry("700x260")

        # Create a tab control
        self.tab_control = ttk.Notebook(root)

        # Create tabs
        self.tab_212r1 = ttk.Frame(self.tab_control)
        self.tab_212r2 = ttk.Frame(self.tab_control)
        self.tab_214r2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_212r1, text='小抄')
        self.tab_control.add(self.tab_212r2, text='212R2')
        self.tab_control.add(self.tab_214r2, text='214R2')

        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.select(self.tab_212r2)

        # Initialize the 212R1 functionality
        self.mode_app_note = ModeAppTabNote(self.tab_212r1)

        # Initialize the 212R2 functionality
        self.mode_app_212r2 = ModeAppTab212(self.tab_212r2)

        # Initialize the 214R2 functionality
        self.mode_app_214r2 = ModeAppTab214(self.tab_214r2)

        # Bind event to reload image when switching to 212R1 tab
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        # Check if the selected tab is 212R1
        selected_tab = self.tab_control.index(self.tab_control.select())
        if selected_tab == 0:  # 212R1 is the first tab
            self.mode_app_note.load_image()

import os  # 用於掃描目錄

class ModeAppTabNote:
    def __init__(self, frame):
        self.frame = frame

        # 初始化圖片列表與當前索引
        self.image_dir = os.path.dirname(os.path.abspath(__file__))  # 執行檔所在目錄
        self.image_files = []
        self.current_index = 0

        # 主框架，用於放置圖片
        self.main_frame = tk.Frame(frame)
        self.main_frame.pack(expand=True, fill='both')

        # 圖片顯示區域
        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(expand=True, fill='both')

        # 上下頁按鈕
        self.prev_button = tk.Button(self.main_frame, text="▲", font=("Arial", 14), bg="black", fg="white", command=self.show_prev_image)
        self.next_button = tk.Button(self.main_frame, text="▼", font=("Arial", 14), bg="black", fg="white", command=self.show_next_image)

        # 綁定滑鼠進入和離開事件
        self.main_frame.bind("<Enter>", self.show_buttons)
        self.main_frame.bind("<Leave>", self.delayed_hide_buttons)

        # 隱藏按鈕初始狀態
        self.buttons_visible = False  # 標誌按鈕是否可見
        self.hide_buttons(None)

        # 綁定視窗大小調整事件
        self.frame.bind("<Configure>", self.on_resize)

    def show_buttons(self, event):
        # 顯示按鈕，使用 place 方法定位在圖片左側
        if not self.buttons_visible:
            self.prev_button.place(relx=0.02, rely=0.4, anchor="center")
            self.next_button.place(relx=0.02, rely=0.6, anchor="center")
            self.buttons_visible = True

    def hide_buttons(self, event):
        # 隱藏按鈕
        if self.buttons_visible:
            self.prev_button.place_forget()
            self.next_button.place_forget()
            self.buttons_visible = False

    def delayed_hide_buttons(self, event):
        # 延遲隱藏按鈕，避免滑鼠快速移動到按鈕上時觸發
        self.frame.after(200, lambda: self.hide_buttons(event))

    def load_image(self):
        # 每次重新掃描執行檔所在目錄
        self.image_files = [f for f in os.listdir(self.image_dir) if f.endswith(".png")]
        self.current_index = 0  # 重置索引

        if not self.image_files:
            self.image_label.config(text="在同資料夾下放至png檔即可查看小抄", font=("Arial", 12), fg="red")
            return

        self.display_image()

    def display_image(self):
        try:
            # 開啟當前索引的圖片
            image_path = os.path.join(self.image_dir, self.image_files[self.current_index])
            image = Image.open(image_path)

            # 獲取框架大小
            frame_width = self.frame.winfo_width()
            frame_height = self.frame.winfo_height()

            # 確保框架大小有效
            if frame_width <= 1 or frame_height <= 1:
                frame_width, frame_height = 700, 260  # 預設大小

            # 調整圖片大小以適應框架
            image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)

            # 轉換為 Tkinter 可用的格式
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            self.image_label.config(text=f"無法載入圖片：{e}", font=("Arial", 12), fg="red")

    def show_prev_image(self):
        # 切換到上一張圖片
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.display_image()

    def show_next_image(self):
        # 切換到下一張圖片
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.display_image()

    def on_resize(self, event):
        # 當框架大小改變時重新載入圖片
        if self.image_files:
            self.display_image()

class ModeAppTab212:
    def __init__(self, frame):
        self.frame = frame
        self.mode = None
        self.sequence = []
        self.edit_mode = False  # Track if in edit mode
        self.item_buttons = []  # Store item buttons for dynamic updates
        self.region212 = ["左", "中", "右"]  # Labels for the region buttons

        # Mode Buttons
        self.mode_frame = tk.Frame(frame)
        self.mode_frame.pack(pady=10)

        self.settings_button = tk.Button(self.mode_frame, text="設定", font=("Arial", 14), width=5, command=self.toggle_edit_mode)
        self.settings_button.pack(side=tk.LEFT, padx=(5, 5))

        self.region_buttons = []  # Store region buttons for dynamic updates
        for region in self.region212:
            btn = tk.Button(self.mode_frame, text=region, font=("Arial", 14), width=8, command=lambda r=region: self.set_mode(r))
            btn.pack(side=tk.LEFT, padx=5)
            self.region_buttons.append(btn)

        self.clear_button = tk.Button(self.mode_frame, text="清除", font=("Arial", 14), width=5, bg="red", fg="white", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=(50, 5))

        # Item Buttons
        self.items_frame = tk.Frame(frame)
        self.items_frame.pack(pady=10)

        self.items = ["X", "椅", "沙", "壺", "鐘", "燈", "鏡"]
        for item in self.items:
            btn = tk.Button(self.items_frame, text=item, font=("Arial", 12), width=4, command=lambda i=item: self.add_item(i))
            btn.pack(side=tk.LEFT, padx=5)
            self.item_buttons.append(btn)

        self.backspace_button = tk.Button(self.items_frame, text="倒退", font=("Arial", 12), command=self.backspace)
        self.backspace_button.pack(side=tk.LEFT, padx=5)

        # Display Sequence in 2x12 Table with 4-item groups
        self.sequence_frame = tk.Frame(frame)
        self.sequence_frame.pack(pady=10)

        self.number_labels = []
        for col in range(12):
            label = tk.Label(self.sequence_frame, text=f"{col + 1}", font=("Arial", 12), width=4, anchor="center")
            label.grid(row=0, column=col, padx=2, pady=2) 
            self.number_labels.append(label)

        self.sequence_labels = []
        for col in range(12):
            bg_color = "lightgray" if 4 <= col <= 7 else "white"
            label = tk.Label(self.sequence_frame, text="", font=("Arial", 12), width=5, anchor="center", relief="solid", bg=bg_color)
            label.grid(row=1, column=col, padx=2, pady=2) 
            self.sequence_labels.append(label)

        # Format Input and Copy Button
        self.format_frame = tk.Frame(frame)
        self.format_frame.pack(pady=10)

        self.format_entry = tk.Entry(self.format_frame, width=30, font=("Arial", 12))
        self.format_entry.insert(0, "O：XXXX/XXXX/XXXX")
        self.format_entry.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(self.format_frame, text="複製結果", font=("Arial", 12), command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.message_label = tk.Label(self.format_frame, text="", font=("Arial", 12), fg="green")
        self.message_label.pack(side=tk.LEFT, padx=10)

    def set_mode(self, mode):
        self.mode = mode
        self.update_mode_buttons()
        self.update_sequence_label()

    def update_mode_buttons(self):
        for btn in self.region_buttons:
            btn.config(bg="SystemButtonFace")

        if self.mode in self.region212:
            index = self.region212.index(self.mode)
            self.region_buttons[index].config(bg="lightblue")

    def add_item(self, item):
        if len(self.sequence) < 12:
            self.sequence.append(item)
            self.update_sequence_label()
        else:
            self.message_label.config(text="最多只能輸入12個物品！", fg="red")

    def backspace(self):
        if self.sequence:
            self.sequence.pop()
            self.update_sequence_label()

    def update_sequence_label(self):
        for i, label in enumerate(self.sequence_labels):
            if i < len(self.sequence):
                label.config(text=self.sequence[i])
            else:
                label.config(text="")
        self.message_label.config(text="")

    def copy_to_clipboard(self):
        if not self.mode:
            self.message_label.config(text="請先選擇區域！", fg="red")
            return

        # Count the number of "X" placeholders in the format string
        format_string = self.format_entry.get()
        x_count = format_string.count("X")

        if len(self.sequence) < x_count:
            self.message_label.config(text=f"請至少輸入{x_count}個物品！", fg="red")
            return

        # Format the result using the entered sequence
        result = format_string.replace("O", self.mode).replace("X", "{}").format(*self.sequence[:x_count])
        self.frame.clipboard_clear()
        self.frame.clipboard_append(result)
        self.frame.update()  # Update clipboard
        self.message_label.config(text="結果已複製到剪貼簿！", fg="green")

    def clear_all(self):      
        self.mode = None
        self.sequence = []
        self.update_mode_buttons()
        self.update_sequence_label()
        self.message_label.config(text="已清除所有內容！", fg="green")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.mode = None
            self.settings_button.config(text="儲存")
            self.copy_button.config(state=tk.DISABLED)  # Disable the "複製結果" button

            # Replace region buttons with entry boxes
            for btn in self.region_buttons:
                btn.pack_forget()

            self.region_entries = []
            for region in self.region212:
                entry = tk.Entry(self.mode_frame, font=("Arial", 14), width=8)
                entry.insert(0, region)
                entry.pack(side=tk.LEFT, padx=5)
                self.region_entries.append(entry)

            self.clear_button.pack_forget()  # Remove the old "清除" button

            # Replace item buttons with entry boxes
            self.backspace_button.pack_forget()
            for i, btn in enumerate(self.item_buttons):
                btn.pack_forget()
                entry = tk.Entry(self.items_frame, font=("Arial", 12), width=4)
                entry.insert(0, self.items[i])
                entry.pack(side=tk.LEFT, padx=5)
                self.item_buttons[i] = entry
        else:
            self.settings_button.config(text="設定")
            self.copy_button.config(state=tk.NORMAL)  # Enable the "複製結果" button

            # Save changes and restore region buttons
            self.region212 = [entry.get() for entry in self.region_entries]
            for entry in self.region_entries:
                entry.pack_forget()

            self.region_buttons = []
            for region in self.region212:
                btn = tk.Button(self.mode_frame, text=region, font=("Arial", 14), width=8, command=lambda r=region: self.set_mode(r))
                btn.pack(side=tk.LEFT, padx=5)
                self.region_buttons.append(btn)

            # Add the "清除" button to the right of the last region button
            self.clear_button = tk.Button(self.mode_frame, text="清除", font=("Arial", 14), width=5, bg="red", fg="white", command=self.clear_all)
            self.clear_button.pack(side=tk.LEFT, padx=(50, 5))

            # Save changes and restore item buttons
            for i, entry in enumerate(self.item_buttons):
                self.items[i] = entry.get()
                entry.pack_forget()
                btn = tk.Button(self.items_frame, text=self.items[i], font=("Arial", 12), width=4, command=lambda i=self.items[i]: self.add_item(i))
                btn.pack(side=tk.LEFT, padx=5)
                self.item_buttons[i] = btn

            self.backspace_button = tk.Button(self.items_frame, text="倒退", font=("Arial", 12), command=self.backspace)
            self.backspace_button.pack(side=tk.LEFT, padx=5)

class ModeAppTab214:
    def __init__(self, frame):
        self.frame = frame
        self.mode = None
        self.sequence = []
        self.edit_mode = False  # Track if in edit mode
        self.item_buttons = []  # Store item buttons for dynamic updates
        self.region214 = ["上", "下"]  # Labels for the region buttons
        self.items = ["-", "1", "2", "3", "4", "5", "6", "7", "8"]

        # Mode Buttons
        self.mode_frame = tk.Frame(frame)
        self.mode_frame.pack(pady=10)

        self.settings_button = tk.Button(self.mode_frame, text="設定", font=("Arial", 14), width=5, command=self.toggle_edit_mode)
        self.settings_button.pack(side=tk.LEFT, padx=(5, 5))

        self.region_buttons = []  # Store region buttons for dynamic updates
        for region in self.region214:
            btn = tk.Button(self.mode_frame, text=region, font=("Arial", 14), width=8, command=lambda r=region: self.set_mode(r))
            btn.pack(side=tk.LEFT, padx=(5, 5))
            self.region_buttons.append(btn)

        self.clear_button = tk.Button(self.mode_frame, text="清除", font=("Arial", 14), width=5, bg="red", fg="white", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=(50, 5))

        # Item Buttons
        self.items_frame = tk.Frame(frame)
        self.items_frame.pack(pady=10)

        for item in self.items:
            btn = tk.Button(self.items_frame, text=item, font=("Arial", 12), width=4, command=lambda i=item: self.add_item(i))
            btn.pack(side=tk.LEFT, padx=5)
            self.item_buttons.append(btn)

        self.backspace_button = tk.Button(self.items_frame, text="倒退", font=("Arial", 12), command=self.backspace)
        self.backspace_button.pack(side=tk.LEFT, padx=5)

        # Display Sequence in 2x8 Table with group separators
        self.sequence_frame = tk.Frame(frame)
        self.sequence_frame.pack(pady=10)

        # First row: Numbers 1~8
        self.number_labels = []
        for col in range(8):
            label = tk.Label(self.sequence_frame, text=f"{col + 1}", font=("Arial", 12), width=4, anchor="center")
            label.grid(row=0, column=col, padx=2, pady=2)
            self.number_labels.append(label)

        # Second row: Items with group separators
        self.sequence_labels = []
        for col in range(8):
            bg_color = "lightgray" if col in [2, 3, 6, 7] else "white"  # Set background color for 3,4,7,8
            label = tk.Label(self.sequence_frame, text="", font=("Arial", 12), width=5, anchor="center", relief="solid", bg=bg_color)
            label.grid(row=1, column=col, padx=2, pady=2)
            self.sequence_labels.append(label)

        # Format Input and Copy Button
        self.format_frame = tk.Frame(frame)
        self.format_frame.pack(pady=10)

        self.format_entry = tk.Entry(self.format_frame, width=30, font=("Arial", 12))
        self.format_entry.insert(0, "O：XX/XX/XX/XX")
        self.format_entry.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(self.format_frame, text="複製結果", font=("Arial", 12), command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # Success/Error Message Label
        self.message_label = tk.Label(self.format_frame, text="", font=("Arial", 12), fg="green")
        self.message_label.pack(side=tk.LEFT, padx=10)

    def set_mode(self, mode):
        self.mode = mode
        self.update_mode_buttons()
        self.update_sequence_label()

    def update_mode_buttons(self):
        # Reset all buttons to default color
        for btn in self.region_buttons:
            btn.config(bg="SystemButtonFace")

        # Highlight the selected mode button
        if self.mode in self.region214:
            index = self.region214.index(self.mode)
            self.region_buttons[index].config(bg="lightblue")

    def add_item(self, item):
        if len(self.sequence) < 8:
            self.sequence.append(item)
            self.update_sequence_label()
        else:
            self.message_label.config(text="最多只能輸入8個數字！", fg="red")

    def backspace(self):
        if self.sequence:
            self.sequence.pop()
            self.update_sequence_label()

    def update_sequence_label(self):
        # Update table display
        for i, label in enumerate(self.sequence_labels):
            if i < len(self.sequence):
                label.config(text=self.sequence[i])
            else:
                label.config(text="")
        self.message_label.config(text="")  # Clear message

    def copy_to_clipboard(self):
        if not self.mode:
            self.message_label.config(text="請先選擇區域！", fg="red")
            return

        format_string = self.format_entry.get()
        x_count = format_string.count("X")

        if len(self.sequence) < x_count:
            self.message_label.config(text=f"請至少輸入{x_count}個數字！", fg="red")
            return

        result = format_string.replace("O", self.mode).replace("X", "{}").format(*self.sequence[:x_count])
        self.frame.clipboard_clear()
        self.frame.clipboard_append(result)
        self.frame.update()  # 更新剪貼簿
        self.message_label.config(text="結果已複製到剪貼簿！", fg="green")

    def clear_all(self):
        self.mode = None
        self.sequence = []
        self.update_mode_buttons()
        self.update_sequence_label()
        self.message_label.config(text="已清除所有內容！", fg="green")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.mode = None
            self.settings_button.config(text="儲存")
            self.copy_button.config(state=tk.DISABLED)  # Disable the "複製結果" button

            # Replace region buttons with entry boxes
            self.backspace_button.pack_forget()
            for btn in self.region_buttons:
                btn.pack_forget()

            self.region_entries = []
            for region in self.region214:
                entry = tk.Entry(self.mode_frame, font=("Arial", 14), width=8)
                entry.insert(0, region)
                entry.pack(side=tk.LEFT, padx=(5, 5))
                self.region_entries.append(entry)

            self.clear_button.pack_forget()  # Remove the old "清除" button

            # Replace item buttons with entry boxes
            for i, btn in enumerate(self.item_buttons):
                btn.pack_forget()
                entry = tk.Entry(self.items_frame, font=("Arial", 12), width=4)
                entry.insert(0, self.items[i])
                entry.pack(side=tk.LEFT, padx=5)
                self.item_buttons[i] = entry
        else:
            self.settings_button.config(text="設定")
            self.copy_button.config(state=tk.NORMAL)  # Enable the "複製結果" button

            # Save changes and restore region buttons
            self.backspace_button.pack_forget()
            self.region214 = [entry.get() for entry in self.region_entries]
            for entry in self.region_entries:
                entry.pack_forget()

            self.region_buttons = []
            for region in self.region214:
                btn = tk.Button(self.mode_frame, text=region, font=("Arial", 14), width=8, command=lambda r=region: self.set_mode(r))
                btn.pack(side=tk.LEFT, padx=(5, 5))
                self.region_buttons.append(btn)

            # Add the "清除" button to the right of the last region button
            self.clear_button = tk.Button(self.mode_frame, text="清除", font=("Arial", 14), width=5, bg="red", fg="white", command=self.clear_all)
            self.clear_button.pack(side=tk.LEFT, padx=(50, 5))

            # Save changes and restore item buttons
            for i, entry in enumerate(self.item_buttons):
                self.items[i] = entry.get()
                entry.pack_forget()
                btn = tk.Button(self.items_frame, text=self.items[i], font=("Arial", 12), width=4, command=lambda i=self.items[i]: self.add_item(i))
                btn.pack(side=tk.LEFT, padx=5)
                self.item_buttons[i] = btn
            self.backspace_button = tk.Button(self.items_frame, text="倒退", font=("Arial", 12), command=self.backspace)
            self.backspace_button.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeApp(root)
    root.mainloop()

# pyinstaller --onefile --noconsole --noupx --name=21-hacker --icon=icon.ico 21-hacker.py