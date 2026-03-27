#!/bin/bash
# 一键部署到阿里云 Cloud Shell 脚本
# 在本地运行此脚本，自动上传代码到 Cloud Shell 并触发构建

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_NAME="healthcare_android"

echo "=========================================="
echo "  血糖监测应用 - Cloud Shell 部署工具"
echo "=========================================="
echo ""

# 检查必要文件
echo "[1/5] 检查项目文件..."
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo "错误: 未找到 main.py"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/buildozer.spec" ]; then
    echo "错误: 未找到 buildozer.spec"
    exit 1
fi

echo "项目文件检查通过"
echo ""

# 创建部署包
echo "[2/5] 创建部署包..."
cd "$PROJECT_DIR"
DEPLOY_PACKAGE="${PROJECT_NAME}_deploy_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$DEPLOY_PACKAGE" \
    --exclude='.git' \
    --exclude='.buildozer' \
    --exclude='bin' \
    --exclude='*.tar.gz' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    .

echo "部署包已创建: $DEPLOY_PACKAGE"
echo ""

# 生成 Cloud Shell 命令
echo "[3/5] 生成 Cloud Shell 构建命令..."
cat > "$PROJECT_DIR/cloud_shell_commands.txt" << 'EOF'
==========================================
  请在阿里云 Cloud Shell 中执行以下命令：
==========================================

# 1. 上传部署包到 Cloud Shell
# 在 Cloud Shell 界面中，点击"上传文件"按钮
# 选择本地的 healthcare_android_deploy_*.tar.gz 文件

# 2. 解压并进入项目目录
tar -xzf healthcare_android_deploy_*.tar.gz -d healthcare_android/
cd healthcare_android

# 3. 运行构建脚本
chmod +x cloud_shell_build.sh
./cloud_shell_build.sh

# 或者手动构建：
# sudo apt-get update
# sudo apt-get install -y python3-pip git zip unzip openjdk-17-jdk
# pip3 install --user buildozer cython
# export PATH=$PATH:~/.local/bin
# buildozer android debug

# 4. 下载 APK
# 构建完成后，在 Cloud Shell 左侧文件浏览器中：
# - 进入 bin/ 目录
# - 右键点击 healthcare-1.0.0-arm64-v8a-debug.apk
# - 选择"下载"

==========================================
EOF

cat "$PROJECT_DIR/cloud_shell_commands.txt"
echo ""

# 创建 Windows 批处理文件（方便 Windows 用户）
echo "[4/5] 创建 Windows 辅助脚本..."
cat > "$PROJECT_DIR/上传到CloudShell.bat" << 'EOF'
@echo off
chcp 65001 >nul
echo ==========================================
echo   血糖监测应用 - Cloud Shell 部署
echo ==========================================
echo.
echo 请按以下步骤操作：
echo.
echo 1. 打开阿里云 Cloud Shell：https://shell.aliyun.com/
echo.
echo 2. 在 Cloud Shell 中创建项目目录：
echo    mkdir healthcare_android ^&^& cd healthcare_android
echo.
echo 3. 上传文件：
echo    - 点击 Cloud Shell 界面的"上传文件"按钮
echo    - 选择当前目录下的 deploy_package.tar.gz
echo.
echo 4. 解压并构建：
echo    tar -xzf deploy_package.tar.gz
echo    chmod +x cloud_shell_build.sh
echo    ./cloud_shell_build.sh
echo.
echo 5. 下载 APK：
echo    构建完成后，在左侧文件浏览器中找到 bin/ 目录
echo    右键点击 APK 文件下载到本地
echo.
pause
EOF

echo "Windows 批处理脚本已创建: 上传到CloudShell.bat"
echo ""

# 创建部署包（简化版，不含构建缓存）
echo "[5/5] 准备部署包..."
tar -czf "$PROJECT_DIR/deploy_package.tar.gz" \
    --exclude='.git' \
    --exclude='.buildozer' \
    --exclude='bin' \
    --exclude='*.tar.gz' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='cloud_shell_commands.txt' \
    -C "$PROJECT_DIR" .

echo "=========================================="
echo "  部署准备完成！"
echo "=========================================="
echo ""
echo "部署包: deploy_package.tar.gz"
echo "文件大小: $(du -h "$PROJECT_DIR/deploy_package.tar.gz" 2>/dev/null | cut -f1 || echo '未知')"
echo ""
echo "下一步操作："
echo ""
echo "方式一：手动上传（推荐）"
echo "  1. 打开 https://shell.aliyun.com/"
echo "  2. 点击'上传文件'按钮"
echo "  3. 选择: $PROJECT_DIR/deploy_package.tar.gz"
echo "  4. 在 Cloud Shell 中执行:"
echo "     tar -xzf deploy_package.tar.gz -C healthcare_android"
echo "     cd healthcare_android"
echo "     chmod +x cloud_shell_build.sh"
echo "     ./cloud_shell_build.sh"
echo ""
echo "方式二：使用 OSS（大文件推荐）"
echo "  1. 将 deploy_package.tar.gz 上传到阿里云 OSS"
echo "  2. 在 Cloud Shell 中:"
echo "     wget [OSS文件URL]"
echo "     tar -xzf deploy_package.tar.gz -C healthcare_android"
echo "     cd healthcare_android && ./cloud_shell_build.sh"
echo ""
echo "详细说明请查看: README_CLOUD_SHELL.md"
echo ""

# 清理临时文件
rm -f "$PROJECT_DIR/cloud_shell_commands.txt"
rm -f "$PROJECT_DIR/${PROJECT_NAME}_deploy_"*.tar.gz

echo "完成！"
