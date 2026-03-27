# GitHub Actions 自动构建 APK 指南

## 优点
- ✅ 完全免费
- ✅ 无需本地配置
- ✅ 自动构建，稳定可靠
- ✅ 构建完成后自动下载 APK

---

## 使用步骤

### 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`healthcare-android`（或其他你喜欢的名字）
3. 选择 **Public**（公开）或 **Private**（私有）
4. 点击 **Create repository**

### 第二步：上传代码到 GitHub

在本地项目目录打开 PowerShell 或 CMD：

```powershell
cd D:\list\healthcare_android

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/healthcare-android.git

# 推送代码
git push -u origin main
```

### 第三步：触发构建

1. 打开 GitHub 仓库页面
2. 点击顶部 **Actions** 标签
3. 点击左侧 **Build Android APK**
4. 点击右侧 **Run workflow** → **Run workflow**

或者，直接修改任意文件并推送，会自动触发构建。

### 第四步：下载 APK

1. 等待构建完成（约 20-40 分钟）
2. 进入 **Actions** 页面
3. 点击最新的工作流运行记录
4. 滚动到底部，找到 **Artifacts** 区域
5. 点击 **healthcare-app-apk** 下载 ZIP 文件
6. 解压 ZIP，得到 `.apk` 文件

---

## 构建状态查看

在 GitHub 仓库页面：
- 绿色 ✅ = 构建成功
- 红色 ❌ = 构建失败（可点击查看日志）
- 黄色 🟡 = 正在构建中

---

## 常见问题

### Q: 构建失败怎么办？
点击失败的运行记录 → **build** → 查看日志，搜索 "error" 或 "Error" 找原因。

### Q: 如何修改构建配置？
编辑 `.github/workflows/build-apk.yml` 文件，推送后会自动生效。

### Q: 私有仓库能用吗？
可以，GitHub Actions 对私有仓库也有免费额度（每月 2000 分钟）。

---

## 文件说明

```
.github/workflows/build-apk.yml    # GitHub Actions 配置文件
main.py                             # 主程序
buildozer.spec                      # Buildozer 打包配置
```