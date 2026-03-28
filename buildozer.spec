[app]
# 应用标题
title = 血糖监测

# 包名
package.name = healthcare

# 包域名
package.domain = org.example

# 源代码目录
source.dir = .

# 主程序文件
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0.0

# 精简依赖，减少构建时间和内存占用
requirements = python3,kivy==2.2.1,matplotlib==3.7.2,pandas==2.0.3,openpyxl==3.1.2,numpy==1.24.3,pillow==10.0.0

# 添加权限
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# Android API版本
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 架构 - 只构建 arm64-v8a 减少构建时间
android.archs = arm64-v8a

# 应用图标（可选）
# icon.filename = %(source.dir)s/icon.png

# 方向
orientation = portrait

# 全屏
fullscreen = 0

# Android应用标签
android.apptheme = "@android:style/Theme.NoTitleBar"

# 构建模式
android.build_mode = debug

[buildozer]
# 日志级别
log_level = 2

# 警告模式
warn_on_root = 0

# 构建目录
build_dir = ./.buildozer

# 打包目录
bin_dir = ./bin
