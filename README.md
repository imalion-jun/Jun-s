# 血糖监测记录系统 - Android版本

## 项目说明
这是一个基于Kivy框架开发的Android血糖监测应用，支持数据录入、趋势图表查看和Excel导出功能。

## 功能特性
- ✅ 血糖数据录入（6个时间点）
- ✅ SQLite数据持久化存储
- ✅ 趋势折线图查看
- ✅ Excel数据导出
- ✅ 中文界面支持

## 自动构建APK

本项目使用 **GitHub Actions** 自动构建 Android APK。

### 构建状态
[![Build Android APK](https://github.com/imalion-jun/Jun-s/actions/workflows/build-apk.yml/badge.svg)](https://github.com/imalion-jun/Jun-s/actions/workflows/build-apk.yml)

### 如何获取APK

1. 点击上方徽章或进入仓库的 **Actions** 标签
2. 选择最新的工作流运行记录
3. 在页面底部的 **Artifacts** 区域下载 `healthcare-app-apk`
4. 解压ZIP文件即可获得 `.apk` 安装包

### 手动触发构建

1. 进入仓库的 **Actions** 标签
2. 点击 **Build Android APK**
3. 点击右侧 **Run workflow** → **Run workflow**

## 文件结构
```
.
├── main.py                    # 主程序
├── buildozer.spec             # Buildozer打包配置
├── .github/workflows/         # GitHub Actions配置
│   └── build-apk.yml
└── README.md                  # 本说明文档
```

## 技术栈
- Python 3.10
- Kivy 2.2.1
- Matplotlib 3.7.2
- Pandas 2.0.3
- Buildozer

## 本地开发

### 安装依赖
```bash
pip install kivy matplotlib pandas openpyxl
```

### 运行程序
```bash
python main.py
```

## 许可证
MIT License