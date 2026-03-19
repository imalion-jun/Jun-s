# 家乡助手 - Android 应用

一款基于 Python Kivy 的安卓应用，让你随时了解家乡动态。

## 功能特性

- 🗺️ **卫星地图**: 输入家乡地址，查看卫星地图
- 🌤️ **天气查询**: 实时查询家乡天气
- 📰 **新闻资讯**: 搜索家乡最新新闻

## 技术栈

- **框架**: Python 3 + Kivy
- **构建工具**: Buildozer
- **地图服务**: 高德地图 / OpenStreetMap
- **天气服务**: wttr.in / 高德天气 API

## 构建 APK

### 方式一：GitHub Actions 自动构建（推荐）

1. 在 GitHub 仓库页面，点击 **Actions** 标签
2. 选择 **Build Android APK** 工作流
3. 点击 **Run workflow**
4. 等待构建完成（约 20-30 分钟）
5. 在 **Artifacts** 中下载 APK 文件

或者推送版本标签自动触发构建：
```bash
git tag v1.0.0
git push origin v1.0.0
```

### 方式二：本地构建（需要 Linux 环境）

```bash
# 安装依赖
pip install buildozer cython

# 初始化 buildozer
buildozer init

# 构建 APK
buildozer android debug

# 构建发布版 APK
buildozer android release
```

## 安装 APK

1. 下载生成的 APK 文件
2. 在安卓手机上允许"安装未知来源应用"
3. 安装 APK
4. 打开应用，输入家乡地址开始使用

## 项目结构

```
hometown_app/
├── main.py              # 主程序
├── buildozer.spec       # Buildozer 配置
├── requirements.txt     # Python 依赖
├── README.md           # 说明文档
└── .github/
    └── workflows/
        └── build_apk.yml  # GitHub Actions 配置
```

## 配置说明

### 高德地图 API（可选）

如需使用高德地图服务，请在 `main.py` 中配置 API Key：

```python
AMAP_API_KEY = "你的高德地图 API Key"
```

## 许可

MIT License

## 作者

imalion-jun
