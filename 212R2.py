import tkinter as tk

class ModeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("212r2找碴神器")
        self.root.attributes('-topmost', True)  # 視窗置頂
        self.root.geometry("700x250")  # 固定視窗大小
        #self.root.resizable(False, False)  # 禁止調整視窗大小

        self.mode = None
        self.sequence = []

        # Mode Buttons
        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack(pady=10)

        # Left, Middle, Right Buttons
        self.left_button = tk.Button(self.mode_frame, text="左", font=("Arial", 14), width=8, command=lambda: self.set_mode("左"))
        self.left_button.pack(side=tk.LEFT, padx=(125,5))

        self.middle_button = tk.Button(self.mode_frame, text="中", font=("Arial", 14), width=8, command=lambda: self.set_mode("中"))
        self.middle_button.pack(side=tk.LEFT, padx=5)

        self.right_button = tk.Button(self.mode_frame, text="右", font=("Arial", 14), width=8, command=lambda: self.set_mode("右"))
        self.right_button.pack(side=tk.LEFT, padx=(5,50))

        # Clear Button
        self.clear_button = tk.Button(self.mode_frame, text="清除", font=("Arial", 14), width=5, bg="red", fg="white", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Item Buttons
        self.items_frame = tk.Frame(root)
        self.items_frame.pack(pady=10)

        self.items = ["空", "椅", "沙", "壺", "鐘", "燈", "鏡"]
        for item in self.items:
            btn = tk.Button(self.items_frame, text=item, font=("Arial", 12), width=4, command=lambda i=item: self.add_item(i))
            btn.pack(side=tk.LEFT, padx=5)

        self.backspace_button = tk.Button(self.items_frame, text="倒退", font=("Arial", 12), command=self.backspace)
        self.backspace_button.pack(side=tk.LEFT, padx=5)

        # Display Sequence in 2x12 Table with 4-item groups
        self.sequence_frame = tk.Frame(root)
        self.sequence_frame.pack(pady=10)

        # First row: Numbers 1~12 with group separators
        self.number_labels = []
        for col in range(12):
            label = tk.Label(self.sequence_frame, text=f"{col + 1}", font=("Arial", 12), width=4, anchor="center")
            label.grid(row=0, column=col, padx=2, pady=2)  # Add spacing every 4 items
            self.number_labels.append(label)

        # Second row: Items with group separators
        self.sequence_labels = []
        for col in range(12):
            bg_color = "lightgray" if 4 <= col <= 7 else "white"  # Set background color for 6~9
            label = tk.Label(self.sequence_frame, text="", font=("Arial", 12), width=5, anchor="center", relief="solid", bg=bg_color)
            label.grid(row=1, column=col, padx=2, pady=2)  # Add spacing every 4 items
            self.sequence_labels.append(label)

        # Format Input and Copy Button
        self.format_frame = tk.Frame(root)
        self.format_frame.pack(pady=10)

        self.format_entry = tk.Entry(self.format_frame, width=30, font=("Arial", 12))
        self.format_entry.insert(0, "O：XXXX/XXXX/XXXX")
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
        self.left_button.config(bg="SystemButtonFace")
        self.middle_button.config(bg="SystemButtonFace")
        self.right_button.config(bg="SystemButtonFace")

        # Highlight the selected mode button
        if self.mode == "左":
            self.left_button.config(bg="lightblue")
        elif self.mode == "中":
            self.middle_button.config(bg="lightblue")
        elif self.mode == "右":
            self.right_button.config(bg="lightblue")

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

        if len(self.sequence) != 12:
            self.message_label.config(text="請輸入完整的12個物品！", fg="red")
            return

        format_string = self.format_entry.get()
        result = format_string.replace("O", self.mode).replace("X", "{}").format(*self.sequence)
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()  # 更新剪貼簿
        self.message_label.config(text="結果已複製到剪貼簿！", fg="green")

    def clear_all(self):      
        self.mode = None
        self.sequence = []
        self.update_mode_buttons()
        self.update_sequence_label()
        self.message_label.config(text="已清除所有內容！", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeApp(root)
    root.mainloop()