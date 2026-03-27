#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血糖监测记录系统 - Android版本 (Kivy)
功能：记录血糖数据、生成折线图、导出Excel
"""

import sqlite3
import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from io import BytesIO
import pandas as pd

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class Database:
    """数据库管理类"""
    
    def __init__(self):
        # Android和桌面环境使用不同的路径
        if 'ANDROID_STORAGE' in os.environ:
            db_dir = os.environ.get('ANDROID_APP_PATH', '/sdcard/healthcare')
        else:
            db_dir = os.path.dirname(os.path.abspath(__file__))
        
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, "healthcare.db")
        self.init_database()
    
    def init_database(self):
        """初始化SQLite数据库"""
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
        """保存血糖记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        column_map = {
            '早上空腹': 'morning_fasting',
            '早餐后两小时': 'after_breakfast',
            '午餐前': 'before_lunch',
            '午餐后两小时': 'after_lunch',
            '晚餐后两小时': 'after_dinner',
            '睡前': 'before_bed'
        }
        
        column = column_map.get(time_point, 'morning_fasting')
        
        # 检查是否已有该日期的记录
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
            values[columns.index(column)] = value
            
            cursor.execute('''
                INSERT INTO blood_sugar_records (record_date, morning_fasting, after_breakfast, 
                before_lunch, after_lunch, after_dinner, before_bed, note)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (date, *values, note))
        
        conn.commit()
        conn.close()
        return True
    
    def get_records(self, start_date=None, end_date=None, time_point=None):
        """获取记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        column_map = {
            '早上空腹': 'morning_fasting',
            '早餐后两小时': 'after_breakfast',
            '午餐前': 'before_lunch',
            '午餐后两小时': 'after_lunch',
            '晚餐后两小时': 'after_dinner',
            '睡前': 'before_bed'
        }
        
        if time_point and start_date and end_date:
            column = column_map.get(time_point, 'morning_fasting')
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
        """导出到Excel"""
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
    """数据录入界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text='血糖监测记录',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(title)
        
        # 表单区域
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=300)
        
        # 日期
        form_layout.add_widget(Label(text='日期:', size_hint_y=None, height=40))
        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d'),
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.date_input)
        
        # 时间点
        form_layout.add_widget(Label(text='测量时间点:', size_hint_y=None, height=40))
        self.time_spinner = Spinner(
            text='早上空腹',
            values=['早上空腹', '早餐后两小时', '午餐前', '午餐后两小时', '晚餐后两小时', '睡前'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.time_spinner)
        
        # 血糖值
        form_layout.add_widget(Label(text='血糖值 (mmol/L):', size_hint_y=None, height=40))
        self.value_input = TextInput(
            text='',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.value_input)
        
        # 备注
        form_layout.add_widget(Label(text='备注:', size_hint_y=None, height=40))
        self.note_input = TextInput(
            text='',
            multiline=True,
            size_hint_y=None,
            height=80
        )
        form_layout.add_widget(self.note_input)
        
        layout.add_widget(form_layout)
        
        # 按钮区域
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        save_btn = Button(
            text='保存记录',
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.save_record
        )
        btn_layout.add_widget(save_btn)
        
        chart_btn = Button(
            text='查看图表',
            background_color=(0.2, 0.6, 1, 1),
            on_press=lambda x: self.manager.current('chart')
        )
        btn_layout.add_widget(chart_btn)
        
        export_btn = Button(
            text='导出Excel',
            background_color=(1, 0.6, 0.2, 1),
            on_press=self.export_data
        )
        btn_layout.add_widget(export_btn)
        
        layout.add_widget(btn_layout)
        
        # 状态标签
        self.status_label = Label(
            text='就绪',
            size_hint_y=None,
            height=30,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def save_record(self, instance):
        """保存记录"""
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
            
            # 验证日期格式
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                self.show_popup('错误', '日期格式错误，请使用 YYYY-MM-DD 格式！')
                return
            
            if self.db.save_record(date, time_point, value, note):
                self.status_label.text = f'已保存: {date} {time_point} = {value}'
                self.value_input.text = ''
                self.note_input.text = ''
                self.show_popup('成功', f'血糖记录已保存！\n{date} {time_point}\n数值: {value} mmol/L')
            
        except Exception as e:
            self.show_popup('错误', f'保存失败: {str(e)}')
    
    def export_data(self, instance):
        """导出数据"""
        try:
            if 'ANDROID_STORAGE' in os.environ:
                filepath = '/sdcard/Download/血糖记录.xlsx'
            else:
                filepath = os.path.join(os.path.expanduser('~'), 'Downloads', 
                                       f'血糖记录_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
            
            if self.db.export_to_excel(filepath):
                self.status_label.text = f'已导出到: {filepath}'
                self.show_popup('成功', f'数据已导出到:\n{filepath}')
            else:
                self.show_popup('提示', '没有数据可导出')
        except Exception as e:
            self.show_popup('错误', f'导出失败: {str(e)}')
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


class ChartScreen(Screen):
    """图表界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='血糖趋势图',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(title)
        
        # 控制区域
        control_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=120)
        
        control_layout.add_widget(Label(text='测量点:', size_hint_y=None, height=35))
        self.time_spinner = Spinner(
            text='早上空腹',
            values=['早上空腹', '早餐后两小时', '午餐前', '午餐后两小时', '晚餐后两小时', '睡前'],
            size_hint_y=None,
            height=35
        )
        control_layout.add_widget(self.time_spinner)
        
        control_layout.add_widget(Label(text='开始日期:', size_hint_y=None, height=35))
        self.start_input = TextInput(
            text=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            multiline=False,
            size_hint_y=None,
            height=35
        )
        control_layout.add_widget(self.start_input)
        
        control_layout.add_widget(Label(text='结束日期:', size_hint_y=None, height=35))
        self.end_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d'),
            multiline=False,
            size_hint_y=None,
            height=35
        )
        control_layout.add_widget(self.end_input)
        
        layout.add_widget(control_layout)
        
        # 按钮
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        
        generate_btn = Button(
            text='生成图表',
            background_color=(0.2, 0.6, 1, 1),
            on_press=self.generate_chart
        )
        btn_layout.add_widget(generate_btn)
        
        back_btn = Button(
            text='返回录入',
            background_color=(0.6, 0.6, 0.6, 1),
            on_press=lambda x: setattr(self.manager, 'current', 'input')
        )
        btn_layout.add_widget(back_btn)
        
        layout.add_widget(btn_layout)
        
        # 图表显示区域
        self.chart_label = Label(
            text='点击"生成图表"查看趋势',
            size_hint_y=1
        )
        layout.add_widget(self.chart_label)
        
        self.add_widget(layout)
    
    def generate_chart(self, instance):
        """生成图表"""
        try:
            time_point = self.time_spinner.text
            start = self.start_input.text.strip()
            end = self.end_input.text.strip()
            
            # 验证日期
            try:
                datetime.strptime(start, '%Y-%m-%d')
                datetime.strptime(end, '%Y-%m-%d')
            except ValueError:
                self.show_popup('错误', '日期格式错误！')
                return
            
            # 获取数据
            data = self.db.get_records(start, end, time_point)
            
            if not data:
                self.chart_label.text = '所选时间段内没有数据'
                return
            
            dates = [row[0] for row in data]
            values = [row[1] for row in data]
            
            # 创建图表
            fig = Figure(figsize=(8, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='#2196F3')
            ax.fill_between(range(len(dates)), values, alpha=0.3, color='#2196F3')
            
            ax.set_title(f'{time_point} 血糖趋势', fontsize=12, pad=10)
            ax.set_xlabel('日期', fontsize=10)
            ax.set_ylabel('血糖值 (mmol/L)', fontsize=10)
            
            # 旋转x轴标签
            for label in ax.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
            
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # 添加参考线
            if '空腹' in time_point or '餐前' in time_point:
                ax.axhline(y=3.9, color='green', linestyle='--', alpha=0.5)
                ax.axhline(y=6.1, color='green', linestyle='--', alpha=0.5)
            else:
                ax.axhline(y=3.9, color='green', linestyle='--', alpha=0.5)
                ax.axhline(y=7.8, color='green', linestyle='--', alpha=0.5)
            
            fig.tight_layout()
            
            # 保存为图片
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            # 在Kivy中显示图片（简化版，实际应用需要Image控件）
            self.chart_label.text = f'图表已生成\n数据点: {len(dates)}个\n范围: {min(values):.1f} - {max(values):.1f}'
            
        except Exception as e:
            self.show_popup('错误', f'生成图表失败: {str(e)}')
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


class HealthcareApp(App):
    """主应用类"""
    
    def build(self):
        # 设置窗口背景色
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(ChartScreen(name='chart'))
        
        return sm


if __name__ == '__main__':
    HealthcareApp().run()
