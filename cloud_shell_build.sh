# 血糖监测应用 - APK 构建状态

## 📋 当前状态

✅ **已完成配置**：
- [x] main.py - 主程序代码（支持血糖记录、Excel导出）
- [x] buildozer.spec - Buildozer 打包配置（已优化）
- [x] cloud_shell_build.sh - Cloud Shell 自动构建脚本
- [x] deploy_to_cloud_shell.sh - 本地部署辅助脚本
- [x] CLOUD_SHELL_QUICKSTART.md - 快速构建指南
- [x] README_CLOUD_SHELL.md - 详细说明文档
- [x] README.md - 项目说明（已更新）

## 🚀 下一步操作

### 方案一：阿里云 Cloud Shell（推荐）

**最简单的方式，无需本地配置**

1. **打开 Cloud Shell**
   - 访问 https://shell.aliyun.com/
   - 登录阿里云账号

2. **执行构建命令**
   
   打开 `CLOUD_SHELL_QUICKSTART.md` 文件，按顺序复制粘贴命令：
   
   ```bash
   # 步骤 1: 创建目录
   mkdir -p ~/healthcare_android && cd ~/healthcare_android
   
   # 步骤 2: 创建 main.py（复制文件中的代码块）
   # 步骤 3: 创建 buildozer.spec（复制文件中的代码块）
   # 步骤 4: 安装依赖并构建
   ```

3. **等待构建完成**
   - 首次构建约 30-60 分钟
   - 需要下载 Android SDK/NDK（约 1GB）

4. **下载 APK**
   - 构建完成后，在 Cloud Shell 左侧文件浏览器
   - 进入 `bin/` 目录
   - 右键点击 `healthcare-1.0.0-arm64-v8a-debug.apk`
   - 选择"下载"

### 方案二：本地 WSL/Docker（高级用户）

如果你有 Linux 环境或 WSL：

```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk
pip3 install buildozer cython

# 构建
cd D:/list/healthcare_android  # 或你的项目路径
buildozer android debug
```

## ⚠️ 重要提示

1. **构建时间**：首次构建约 30-60 分钟，请耐心等待
2. **Cloud Shell 限制**：
   - 免费额度可能有限
   - 会话可能会超时，建议使用 `screen` 或 `tmux`
3. **APK 大小**：约 50-100MB（包含 Python 运行时和依赖库）

## 📱 安装到手机

1. 将下载的 APK 传输到手机
2. 在手机上允许"安装未知来源应用"
   - 设置 → 安全 → 未知来源
3. 安装并打开应用

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| Cloud Shell 超时 | 使用 `screen` 保持会话：`screen -S build` |
| 构建失败/内存不足 | 尝试 `buildozer android debug -j1` |
| 下载依赖慢 | 设置 pip 镜像：`pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| 找不到 buildozer | 添加环境变量：`export PATH=$PATH:~/.local/bin` |

## 📞 需要帮助？

查看以下文档获取详细说明：
- `CLOUD_SHELL_QUICKSTART.md` - 快速开始指南
- `README_CLOUD_SHELL.md` - Cloud Shell 详细说明
- `README.md` - 项目完整说明

---

**最后更新**：2026年3月27日
**状态**：✅ 配置完成，等待构建
