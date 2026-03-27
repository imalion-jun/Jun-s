# 阿里云 Cloud Shell 快速构建指南

## 🚀 最快方式：复制粘贴执行

### 步骤 1：打开 Cloud Shell
访问 https://shell.aliyun.com/ 并登录

### 步骤 2：创建项目目录并上传代码

在 Cloud Shell 终端中执行：

```bash
# 创建项目目录
mkdir -p ~/healthcare_android && cd ~/healthcare_android

# 创建 main.py 文件（复制下面整个代码块粘贴）
cat > main.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血糖监测记录系统 - Android版本 (Kivy)
"""

import sqlite3
import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

class Database:
    def __init__(self):
        if 'ANDROID_STORAGE' in os.environ:
            db_dir = os.environ.get('ANDROID_APP_PATH', '/sdcard/healthcare')
        else:
            db_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, "healthcare.db")
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blood_sugar_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_date DATE NOT NULL,
                morning_fasting REAL,
                after_breakfast REAL,
                before_lunch REAL,
                after_lunch REAL,
                after_dinner REAL,
                before_bed REAL,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_record(self, date, time_point, value, note):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        column_map = {
            'morning_fasting': '早上空腹',
            'after_breakfast': '早餐后两小时',
            'before_lunch': '午餐前',
            'after_lunch': '午餐后两小时',
            'after_dinner': '晚餐后两小时',
            'before_bed': '睡前'
        }
        column = {v: k for k, v in column_map.items()}.get(time_point, 'morning_fasting')
        
        cursor.execute("SELECT id FROM blood_sugar_records WHERE record_date = ?", (date,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute(f'''
                UPDATE blood_sugar_records 
                SET {column} = ?, note = CASE WHEN note IS NULL OR note = '' THEN ? ELSE note || '; ' || ? END
                WHERE record_date = ?
            ''', (value, note, note, date))
        else:
            columns = ['morning_fasting', 'after_breakfast', 'before_lunch', 
                      'after_lunch', 'after_dinner', 'before_bed']
            values = [None] * 6
            idx = columns.index(column)
            values[idx] = value
            cursor.execute('''
                INSERT INTO blood_sugar_records (record_date, morning_fasting, after_breakfast, 
                before_lunch, after_lunch, after_dinner, before_bed, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, *values, note))
        
        conn.commit()
        conn.close()
        return True
    
    def get_records(self, start_date=None, end_date=None, time_point=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        column_map = {
            'morning_fasting': '早上空腹',
            'after_breakfast': '早餐后两小时',
            'before_lunch': '午餐前',
            'after_lunch': '午餐后两小时',
            'after_dinner': '晚餐后两小时',
            'before_bed': '睡前'
        }
        
        if time_point and start_date and end_date:
            column = {v: k for k, v in column_map.items()}.get(time_point, 'morning_fasting')
            cursor.execute(f'''
                SELECT record_date, {column} FROM blood_sugar_records
                WHERE record_date BETWEEN ? AND ? AND {column} IS NOT NULL
                ORDER BY record_date
            ''', (start_date, end_date))
        else:
            cursor.execute('''
                SELECT record_date, morning_fasting, after_breakfast, before_lunch,
                       after_lunch, after_dinner, before_bed, note
                FROM blood_sugar_records ORDER BY record_date
            ''')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def export_to_excel(self, filepath):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("""
            SELECT record_date as '日期', 
                   morning_fasting as '早上空腹', 
                   after_breakfast as '早餐后两小时', 
                   before_lunch as '午餐前', 
                   after_lunch as '午餐后两小时', 
                   after_dinner as '晚餐后两小时', 
                   before_bed as '睡前', 
                   note as '备注'
            FROM blood_sugar_records 
            ORDER BY record_date
        """, conn)
        conn.close()
        if not df.empty:
            df.to_excel(filepath, index=False, engine='openpyxl')
            return True
        return False

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='血糖监测记录', font_size='24sp', size_hint_y=None, height=50, color=(0.2, 0.6, 1, 1))
        layout.add_widget(title)
        
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=250)
        
        form_layout.add_widget(Label(text='日期:', size_hint_y=None, height=40))
        self.date_input = TextInput(text=datetime.now().strftime('%Y-%m-%d'), multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.date_input)
        
        form_layout.add_widget(Label(text='测量时间点:', size_hint_y=None, height=40))
        self.time_spinner = Spinner(text='早上空腹', values=['早上空腹', '早餐后两小时', '午餐前', '午餐后两小时', '晚餐后两小时', '睡前'], size_hint_y=None, height=40)
        form_layout.add_widget(self.time_spinner)
        
        form_layout.add_widget(Label(text='血糖值 (mmol/L):', size_hint_y=None, height=40))
        self.value_input = TextInput(text='', multiline=False, input_filter='float', size_hint_y=None, height=40)
        form_layout.add_widget(self.value_input)
        
        form_layout.add_widget(Label(text='备注:', size_hint_y=None, height=40))
        self.note_input = TextInput(text='', multiline=True, size_hint_y=None, height=60)
        form_layout.add_widget(self.note_input)
        
        layout.add_widget(form_layout)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = Button(text='保存记录', background_color=(0.2, 0.8, 0.2, 1), on_press=self.save_record)
        btn_layout.add_widget(save_btn)
        
        export_btn = Button(text='导出Excel', background_color=(1, 0.6, 0.2, 1), on_press=self.export_data)
        btn_layout.add_widget(export_btn)
        
        layout.add_widget(btn_layout)
        
        self.status_label = Label(text='就绪', size_hint_y=None, height=30, color=(0.5, 0.5, 0.5, 1))
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def save_record(self, instance):
        try:
            date = self.date_input.text.strip()
            time_point = self.time_spinner.text
            value_str = self.value_input.text.strip()
            note = self.note_input.text.strip()
            
            if not value_str:
                self.show_popup('错误', '请输入血糖数值！')
                return
            
            try:
                value = round(float(value_str), 1)
            except ValueError:
                self.show_popup('错误', '血糖数值必须是数字！')
                return
            
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                self.show_popup('错误', '日期格式错误！')
                return
            
            if self.db.save_record(date, time_point, value, note):
                self.status_label.text = f'已保存: {date} {time_point} = {value}'
                self.value_input.text = ''
                self.note_input.text = ''
                self.show_popup('成功', f'血糖记录已保存！')
            
        except Exception as e:
            self.show_popup('错误', f'保存失败: {str(e)}')
    
    def export_data(self, instance):
        try:
            if 'ANDROID_STORAGE' in os.environ:
                filepath = '/sdcard/Download/血糖记录.xlsx'
            else:
                filepath = os.path.join(os.path.expanduser('~'), 'Downloads', f'血糖记录_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
            
            if self.db.export_to_excel(filepath):
                self.status_label.text = f'已导出到: {filepath}'
                self.show_popup('成功', f'数据已导出！')
            else:
                self.show_popup('提示', '没有数据可导出')
        except Exception as e:
            self.show_popup('错误', f'导出失败: {str(e)}')
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

class HealthcareApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input'))
        return sm

if __name__ == '__main__':
    HealthcareApp().run()
PYEOF

echo "main.py 创建完成"
```

### 步骤 3：创建 buildozer.spec

```bash
cat > buildozer.spec << 'SPECEOF'
[app]
title = 血糖监测
package.name = healthcare
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.2.1,matplotlib==3.7.2,pandas==2.0.3,openpyxl==3.1.2,numpy==1.24.3,pillow==10.0.0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
orientation = portrait
fullscreen = 0
android.apptheme = "@android:style/Theme.NoTitleBar"
android.build_mode = release

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
bin_dir = ./bin
SPECEOF

echo "buildozer.spec 创建完成"
```

### 步骤 4：安装依赖并构建

```bash
# 安装系统依赖（约 2-3 分钟）
echo "安装系统依赖..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev automake

# 安装 Python 依赖（约 1 分钟）
echo "安装 Python 依赖..."
pip3 install --user buildozer cython

# 配置环境变量
export PATH=$PATH:~/.local/bin

# 开始构建（首次约 30-60 分钟）
echo "开始构建 APK..."
~/.local/bin/buildozer android debug
```

### 步骤 5：下载 APK

构建完成后，在 Cloud Shell 左侧文件浏览器中：
1. 进入 `bin/` 目录
2. 右键点击 `healthcare-1.0.0-arm64-v8a-debug.apk`
3. 选择"下载"

---

## 📋 完整一键脚本

如果想一次性执行所有步骤，保存以下内容为 `build.sh` 并在 Cloud Shell 中运行：

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "  血糖监测应用 - Cloud Shell 构建脚本"
echo "=========================================="

# 创建目录
mkdir -p ~/healthcare_android && cd ~/healthcare_android

# 创建 main.py
cat > main.py << 'PYEOF'
[上面步骤2中的 main.py 代码]
PYEOF

# 创建 buildozer.spec
cat > buildozer.spec << 'SPECEOF'
[上面步骤3中的 buildozer.spec 代码]
SPECEOF

# 安装依赖
echo "[1/3] 安装系统依赖..."
sudo apt-get update -qq
sudo apt-get install -y -qq python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev automake

echo "[2/3] 安装 Python 依赖..."
pip3 install --user buildozer cython
export PATH=$PATH:~/.local/bin

echo "[3/3] 开始构建 APK（约 30-60 分钟）..."
~/.local/bin/buildozer android debug

echo "=========================================="
echo "  构建完成！"
echo "=========================================="
echo "APK 位置: bin/healthcare-1.0.0-arm64-v8a-debug.apk"
echo "请在 Cloud Shell 文件浏览器中下载"
```

---

## ⚠️ 重要提示

1. **构建时间**：首次构建约 30-60 分钟，请耐心等待
2. **会话保持**：Cloud Shell 可能会超时，建议使用 `screen` 或 `tmux` 保持会话
3. **存储空间**：确保 Cloud Shell 有足够空间（建议至少 5GB）
4. **网络稳定**：构建过程中需要下载大量依赖，保持网络连接

## 🔧 故障排除

### 构建失败/内存不足
```bash
# 尝试减少并行任务
buildozer android debug -j1
```

### 下载超时
```bash
# 设置镜像源
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 找不到 buildozer 命令
```bash
export PATH=$PATH:~/.local/bin
```
