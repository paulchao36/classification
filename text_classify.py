import os
import shutil
import re

def classify_txt_files(base_folder, category_keywords):
    base_folder = os.path.abspath(base_folder)
    txt_files = [f for f in os.listdir(base_folder) if f.endswith('.txt') and os.path.isfile(os.path.join(base_folder, f))]

    # 建立針對每個關鍵字的排除正則式 (無關語境)
    exclusion_patterns = []
    for keyword in set(sum(category_keywords.values(), [])):
        pattern = re.compile(r'(和|與)?' + re.escape(keyword) + r'無關')
        exclusion_patterns.append((keyword, pattern))

    for file_name in txt_files:
        file_path = os.path.join(base_folder, file_name)

        # 讀取內容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

        # 檢查是否有否定語句，收集被排除的關鍵字
        excluded_keywords = set()
        for keyword, pattern in exclusion_patterns:
            if pattern.search(content):
                excluded_keywords.add(keyword)

        # 正常分類流程
        matched = False
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in excluded_keywords:
                    continue  # 該關鍵字被排除
                if keyword in file_name or keyword in content:
                    category_folder = os.path.join(base_folder, category)
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_folder, file_name))
                    matched = True
                    break
            if matched:
                break

    print("分類完成。")
    
# 🔧 設定資料夾與分類關鍵字
base_folder = '../emails'  # <-- 修改為你的資料夾路徑

# 🔑 分類與關鍵字（依順序排列代表優先順序）
category_keywords = {
    '生活方式': ['兒子'],
    '配方': ['甜點'],
    '行銷': ['行銷']
}

# 🚀 執行分類
classify_txt_files(base_folder, category_keywords)
