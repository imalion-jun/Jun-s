# 家乡助手 - 安卓应用

一个使用 Python (Kivy) 开发的安卓应用，帮助用户了解家乡的天气和新闻。

## ✨ 功能特点

1. **📍 输入家乡地址** - 输入地址后自动打开卫星地图查看
2. **🌤️ 查询家乡天气** - 实时查询家乡天气情况
3. **📰 家乡最新新闻** - 搜索家乡相关的最新资讯

## 🆓 使用的免费服务

**无需配置 API Key 即可使用！** 应用已集成以下免费服务：

| 功能 | 免费服务 | 说明 |
|-----|---------|------|
| 地理编码 | **Nominatim (OpenStreetMap)** | 完全免费，限制 1次/秒 |
| 天气查询 | **wttr.in** | 完全免费，无限制 |
| 卫星地图 | **高德/百度/腾讯/Google/天地图** | 通过浏览器打开 |
| 新闻搜索 | **百度新闻/微信搜索** | 通过浏览器打开 |

### 可选：配置高德地图 API（更好的国内体验）

如需更精准的国内地址解析和天气数据，可配置高德地图 API：

```python
# 在 main.py 中修改
AMAP_API_KEY = "你的高德API Key"
```

**获取高德 API Key**：https://lbs.amap.com/ → 注册 → 控制台 → 创建应用 → Web服务

免费额度：5,000次/天

## 技术栈

- **Python 3** - 主要编程语言
- **Kivy** - 跨平台 UI 框架
- **Buildozer** - 打包成 APK 工具

## 项目结构

```
hometown_app/
├── main.py              # 主应用代码
├── requirements.txt     # Python 依赖
├── buildozer.spec       # 打包配置
├── .github/workflows/   # GitHub Actions 自动构建
└── README.md            # 说明文档
```

## 🚀 快速开始

### Windows 开发调试

```bash
cd hometown_app
pip install -r requirements.txt
python main.py
```

### 打包成 APK

**重要**: Buildozer 只能在 Linux 环境下运行！

#### 方法一：GitHub Actions（推荐）

1. 将项目上传到 GitHub
2. 自动触发构建
3. 在 Actions → Artifacts 中下载 APK

#### 方法二：使用 WSL

```powershell
# 安装 WSL
wsl --install -d Ubuntu

# 进入 WSL
wsl

# 安装依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake

# 安装 Buildozer
pip3 install buildozer cython

# 打包
cd hometown_app
buildozer android debug
```

#### 方法三：使用 Docker

```bash
docker pull kivy/buildozer
docker run --rm -v "%cd%":/app kivy/buildozer android debug
```

## 📱 应用界面

```
┌────────────────────────┐
│                        │
│      🏠 家乡助手        │
│                        │
│    随时了解家乡动态     │
│                        │
│  ┌──────────────────┐  │
│  │ 📍 输入你的家乡   │  │
│  └──────────────────┘  │
│                        │
│  ┌──────────────────┐  │
│  │ 🌤️ 查询家乡天气   │  │
│  └──────────────────┘  │
│                        │
│  ┌──────────────────┐  │
│  │ 📰 家乡最新新闻   │  │
│  └──────────────────┘  │
│                        │
│   请先输入家乡地址      │
│                        │
└────────────────────────┘
```

## 🔐 权限说明

- `INTERNET` - 网络访问
- `ACCESS_FINE_LOCATION` - 精确位置（可选）
- `ACCESS_COARSE_LOCATION` - 大致位置（可选）

## ⚠️ 限制说明

1. **卫星视图**: 使用系统浏览器打开在线地图
2. **天气服务**: 使用 wttr.in 或高德 API，非手机自带天气
3. **新闻搜索**: 通过浏览器打开百度/微信搜索

## 🌐 支持的地图服务

点击"输入你的家乡"后，会依次尝试打开：

1. **高德地图** - 国内最佳，支持调起 APP
2. **百度地图** - 国内常用
3. **腾讯地图** - 国内常用
4. **Google Maps** - 国际通用
5. **OpenStreetMap** - 完全免费
6. **天地图** - 国家地理信息公共服务平台

## 💡 改进建议

如需更好的体验，建议：

1. **原生开发** (Kotlin/Java) - 可直接调用系统组件
2. **Flutter** - 跨平台性能更好，插件丰富

## 许可证

MIT License
