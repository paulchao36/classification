import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class TextClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文字分類器")
        self.category_entries = {}

        # 資料夾選擇
        self.folder_path = tk.StringVar()
        tk.Label(root, text="選擇資料夾：").grid(row=0, column=0, sticky="w")
        tk.Entry(root, textvariable=self.folder_path, width=40).grid(row=0, column=1)
        tk.Button(root, text="瀏覽", command=self.browse_folder).grid(row=0, column=2)

        # 類別輸入區
        self.category_frame = tk.Frame(root)
        self.category_frame.grid(row=1, column=0, columnspan=3, pady=10)
        tk.Label(self.category_frame, text="類別名稱").grid(row=0, column=0)
        tk.Label(self.category_frame, text="關鍵字（用逗號分隔）").grid(row=0, column=1)
        self.add_category_row()

        tk.Button(root, text="新增分類", command=self.add_category_row).grid(row=2, column=0, pady=5)
        tk.Button(root, text="開始分類", command=self.classify_files).grid(row=2, column=2, pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def add_category_row(self):
        row = len(self.category_entries) + 1
        cat_var = tk.StringVar()
        kw_var = tk.StringVar()
        tk.Entry(self.category_frame, textvariable=cat_var).grid(row=row, column=0)
        tk.Entry(self.category_frame, textvariable=kw_var, width=40).grid(row=row, column=1)
        self.category_entries[row] = (cat_var, kw_var)

    def classify_files(self):
        base_folder = self.folder_path.get()
        if not base_folder or not os.path.isdir(base_folder):
            messagebox.showerror("錯誤", "請選擇有效的資料夾。")
            return

        # 取得分類關鍵字設定
        category_keywords = {}
        for cat_var, kw_var in self.category_entries.values():
            category = cat_var.get().strip()
            keywords = [kw.strip() for kw in kw_var.get().split(',') if kw.strip()]
            if category and keywords:
                category_keywords[category] = keywords

        if not category_keywords:
            messagebox.showerror("錯誤", "請輸入至少一個分類與對應關鍵字。")
            return

        # 建立排除關鍵字的正則式
        exclusion_patterns = []
        all_keywords = set(sum(category_keywords.values(), []))
        for keyword in all_keywords:
            pattern = re.compile(r'(和|與)?' + re.escape(keyword) + r'無關')
            exclusion_patterns.append((keyword, pattern))

        # 處理檔案
        files = [f for f in os.listdir(base_folder) if f.endswith('.txt') and os.path.isfile(os.path.join(base_folder, f))]
        for file_name in files:
            file_path = os.path.join(base_folder, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

            excluded_keywords = {kw for kw, pat in exclusion_patterns if pat.search(content)}

            # 分類
            matched = False
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword in excluded_keywords:
                        continue
                    if keyword in file_name or keyword in content:
                        target_folder = os.path.join(base_folder, category)
                        os.makedirs(target_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_folder, file_name))
                        matched = True
                        break
                if matched:
                    break

        messagebox.showinfo("完成", "分類完成！")

# 啟動 GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TextClassifierGUI(root)
    root.mainloop()
