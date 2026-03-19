[app]

# 应用名称
title = 家乡助手

# 包名
package.name = hometown

# 包域名
package.domain = com.imalion

# 源代码目录
source.dir = .

# 源代码包含的文件扩展名
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0.0

# 应用的依赖库
requirements = python3,kivy==2.3.0,requests,plyer

# 权限
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_NETWORK_STATE

# Android 应用主题
android.app_theme = Material

# 最低 Android SDK 版本
android.minapi = 21

# 目标 Android SDK 版本
android.api = 33

# NDK 版本
android.ndk = 25b

# 是否接受 Android SDK 许可
android.accept_sdk_license = True

# 应用图标 (需要提供 icon.png)
# icon.filename = icon.png

# 横屏或竖屏
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 启动入口
android.entrypoint = org.kivy.android.PythonActivity

# Android 配置
android.allow_backup = True

# 使用 android 的 wake lock
# android.wakelock = False

# 构建类型 (release 或 debug)
# release 模式需要签名
# android.release = False

[buildozer]

# 日志级别 (0-2)
log_level = 2

# 显示警告
show_warnings = True

# 构建目录
build_dir = ./.buildozer

# 二进制文件目录
bin_dir = ./bin
