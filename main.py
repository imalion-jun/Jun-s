"""
家乡助手 - 安卓应用
功能:
1. 输入家乡地址，显示卫星图
2. 查询家乡天气
3. 搜索家乡新闻

作者: Claude Assistant
"""

import os
import webbrowser
from datetime import datetime, timedelta
from urllib.parse import quote

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp

try:
    from plyer import gps, notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

import requests

# ==================== 配置 ====================
# 高德地图 Web API Key (可选，配置后可获得更好的国内支持)
AMAP_API_KEY = "YOUR_AMAP_API_KEY"

# 高德地图 Web 服务 API
AMAP_GEO_URL = "https://restapi.amap.com/v3/geocode/geo"
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"

# 免费的 OpenStreetMap Nominatim 地理编码服务 (无需 API Key)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# 免费的 wttr.in 天气服务 (无需 API Key)
WTTR_URL = "https://wttr.in"

# ==================== 工具类 ====================

class LocationService:
    """位置服务类"""

    def __init__(self):
        self.saved_address = ""
        self.saved_location = None  # (lng, lat)
        self.saved_adcode = ""  # 行政区划代码

    def geocode(self, address):
        """
        地址转经纬度
        优先使用高德地图 API，失败则使用免费的 Nominatim
        """
        # 如果配置了高德 API Key，优先使用高德
        if AMAP_API_KEY and AMAP_API_KEY != "YOUR_AMAP_API_KEY":
            return self._geocode_amap(address)

        # 使用免费的 Nominatim (OpenStreetMap)
        return self._geocode_nominatim(address)

    def _geocode_amap(self, address):
        """使用高德地图进行地理编码"""
        try:
            params = {
                "key": AMAP_API_KEY,
                "address": address
            }
            response = requests.get(AMAP_GEO_URL, params=params, timeout=10)
            data = response.json()

            if data.get("status") == "1" and data.get("geocodes"):
                geo = data["geocodes"][0]
                location = geo["location"].split(",")
                return {
                    "success": True,
                    "location": (float(location[0]), float(location[1])),
                    "formatted_address": geo.get("formatted_address", address),
                    "adcode": geo.get("adcode", ""),
                    "message": "成功 (高德地图)"
                }
            else:
                return {
                    "success": False,
                    "location": None,
                    "message": f"未找到地址: {address}"
                }
        except Exception as e:
            return {
                "success": False,
                "location": None,
                "message": f"网络错误: {str(e)}"
            }

    def _geocode_nominatim(self, address):
        """
        使用免费的 Nominatim (OpenStreetMap) 进行地理编码
        无需 API Key，限制：1次/秒
        """
        try:
            # 添加中国限制以提高准确性
            params = {
                "q": address,
                "format": "json",
                "limit": 1,
                "accept-language": "zh"
            }
            headers = {
                "User-Agent": "HometownApp/1.0",
                "Accept-Language": "zh-CN,zh;q=0.9"
            }
            response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()
                if data:
                    result = data[0]
                    lat = float(result["lat"])
                    lon = float(result["lon"])
                    display_name = result.get("display_name", address)
                    return {
                        "success": True,
                        "location": (lon, lat),
                        "formatted_address": display_name,
                        "adcode": "",
                        "message": "成功 (OpenStreetMap 免费服务)"
                    }
                else:
                    return {
                        "success": False,
                        "location": None,
                        "message": f"未找到地址: {address}"
                    }
            else:
                return {
                    "success": False,
                    "location": None,
                    "message": f"服务暂时不可用 (HTTP {response.status_code})"
                }
        except Exception as e:
            return {
                "success": False,
                "location": None,
                "message": f"网络错误: {str(e)}"
            }

    def get_weather(self, adcode):
        """
        获取天气信息
        优先使用高德 API，失败则使用免费的 wttr.in
        """
        if AMAP_API_KEY and AMAP_API_KEY != "YOUR_AMAP_API_KEY" and adcode:
            return self._get_weather_amap(adcode)

        # 使用免费的 wttr.in
        if self.saved_address:
            return self._get_weather_wttr(self.saved_address)

        return {"success": False, "message": "请先设置家乡地址"}

    def _get_weather_amap(self, adcode):
        """使用高德 API 获取天气"""
        try:
            params = {
                "key": AMAP_API_KEY,
                "city": adcode,
                "extensions": "base"
            }
            response = requests.get(AMAP_WEATHER_URL, params=params, timeout=10)
            data = response.json()

            if data.get("status") == "1" and data.get("lives"):
                live = data["lives"][0]
                return {
                    "success": True,
                    "weather": {
                        "city": live.get("city", ""),
                        "weather": live.get("weather", ""),
                        "temperature": live.get("temperature", ""),
                        "wind": f"{live.get('winddirection', '')}{live.get('windpower', '')}级",
                        "humidity": f"{live.get('humidity', '')}%"
                    },
                    "message": "成功 (高德地图)"
                }
            return {"success": False, "message": "获取天气失败"}
        except Exception as e:
            return {"success": False, "message": f"网络错误: {str(e)}"}

    def _get_weather_wttr(self, address):
        """
        使用免费的 wttr.in 获取天气
        无需 API Key
        """
        try:
            # 提取城市名称
            city = self._extract_city(address)

            # wttr.in API
            url = f"{WTTR_URL}/{quote(city)}?format=j1"
            headers = {"User-Agent": "HometownApp/1.0"}
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()
                current = data.get("current_condition", [{}])[0]

                return {
                    "success": True,
                    "weather": {
                        "city": city,
                        "weather": self._translate_weather(current.get("weatherDesc", [{}])[0].get("value", "未知")),
                        "temperature": current.get("temp_C", "--"),
                        "wind": f"{current.get('winddir16Point', '')} {current.get('windspeedKmph', '')}km/h",
                        "humidity": f"{current.get('humidity', '--')}%"
                    },
                    "message": "成功 (wttr.in 免费服务)"
                }
            return {"success": False, "message": "获取天气失败"}
        except Exception as e:
            return {"success": False, "message": f"网络错误: {str(e)}"}

    def _translate_weather(self, weather_en):
        """翻译天气描述"""
        translations = {
            "Clear": "晴", "Sunny": "晴", "Partly cloudy": "多云",
            "Cloudy": "阴", "Overcast": "阴", "Rain": "雨",
            "Light rain": "小雨", "Heavy rain": "大雨",
            "Snow": "雪", "Light snow": "小雪", "Heavy snow": "大雪",
            "Fog": "雾", "Mist": "薄雾", "Thunder": "雷"
        }
        for key, value in translations.items():
            if key.lower() in weather_en.lower():
                return value
        return weather_en

    def _extract_city(self, address):
        """从地址中提取城市名"""
        # 常见的地址分隔符
        for suffix in ["市", "县", "区"]:
            if suffix in address:
                parts = address.split(suffix)
                for part in parts:
                    if len(part) >= 2:
                        return part + suffix
        return address[:6] if len(address) >= 6 else address

    def open_satellite_map(self, lng, lat, address):
        """打开卫星地图视图 - 多种选择"""
        # 编码地址
        encoded_addr = quote(address)

        # 多种地图服务 URL
        map_urls = {
            # 高德地图 - 国内最佳，支持调起 APP
            "高德地图": f"https://uri.amap.com/marker?position={lng},{lat}&name={encoded_addr}&coordinate=gaode&callnative=1",

            # 百度地图 - 国内常用
            "百度地图": f"https://api.map.baidu.com/marker?location={lat},{lng}&title={encoded_addr}&output=html&coord_type=gcj02",

            # 腾讯地图 - 国内常用
            "腾讯地图": f"https://apis.map.qq.com/uri/v1/marker?marker=coord:{lat},{lng};title:{encoded_addr}",

            # Google Maps 卫星图 - 国际通用
            "Google卫星图": f"https://www.google.com/maps/@{lat},{lng},18z/data=!3m1!1e3",

            # OpenStreetMap - 完全免费
            "OpenStreetMap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=18/{lat}/{lng}",

            # 天地图 - 国家地理信息公共服务平台 (免费)
            "天地图": f"https://map.tianditu.gov.cn/?center={lng},{lat}&zoom=18"
        }

        # 按优先级尝试打开
        for name, url in map_urls.items():
            try:
                webbrowser.open(url)
                return {"success": True, "service": name}
            except:
                continue

        return {"success": False, "service": None}

    def search_local_news(self, address):
        """
        搜索家乡新闻
        使用搜索引擎或新闻 API
        """
        # 提取县/区名称
        county_name = self._extract_county(address)

        # 计算三天前的日期
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

        # 构建搜索链接（使用百度资讯搜索）
        search_query = f"{county_name} 新闻 资讯"
        baidu_news_url = f"https://www.baidu.com/s?wd={quote(search_query)}&tn=news&rtt=1&bsst=1"

        # 也可以使用微信文章搜索
        wechat_search_url = f"https://weixin.sogou.com/weixin?type=2&query={quote(search_query)}"

        return {
            "baidu_news": baidu_news_url,
            "wechat": wechat_search_url,
            "county": county_name
        }

    def _extract_county(self, address):
        """从地址中提取县/区名称"""
        # 简单提取逻辑
        for suffix in ["县", "区", "市"]:
            if suffix in address:
                parts = address.split(suffix)
                if len(parts) >= 1:
                    # 获取最后一个包含该后缀的部分
                    for part in address.split(suffix):
                        if len(part) >= 2:
                            return part + suffix
        return address[:4] if len(address) >= 4 else address


# ==================== UI 组件 ====================

class RoundedButton(Button):
    """圆角按钮组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.font_size = dp(18)
        self.size_hint_y = None
        self.height = dp(60)
        self.bold = True

        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)  # 蓝色
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class HomeScreen(Screen):
    """主页面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_service = LocationService()
        self.build_ui()

    def build_ui(self):
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))

        # 标题
        title = Label(
            text='🏠 家乡助手',
            font_size=dp(36),
            size_hint_y=0.2,
            bold=True,
            color=(0.1, 0.1, 0.1, 1)
        )

        # 副标题
        subtitle = Label(
            text='随时了解家乡动态',
            font_size=dp(18),
            size_hint_y=0.1,
            color=(0.4, 0.4, 0.4, 1)
        )

        # 按钮区域
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=0.5)

        # 按钮1: 输入家乡地址
        self.btn_address = RoundedButton(text='📍 输入你的家乡')
        self.btn_address.bind(on_press=self.show_address_input)
        with self.btn_address.canvas.before:
            Color(0.98, 0.4, 0.4, 1)  # 红色
            self.btn_address.rect = RoundedRectangle(
                pos=self.btn_address.pos,
                size=self.btn_address.size,
                radius=[dp(15)]
            )
            self.btn_address.bind(
                pos=lambda i, v: setattr(self.btn_address.rect, 'pos', i.pos),
                size=lambda i, v: setattr(self.btn_address.rect, 'size', i.size)
            )

        # 按钮2: 查询天气
        self.btn_weather = RoundedButton(text='🌤️ 查询家乡天气')
        self.btn_weather.bind(on_press=self.show_weather)
        with self.btn_weather.canvas.before:
            Color(0.3, 0.7, 0.9, 1)  # 天蓝色
            self.btn_weather.rect = RoundedRectangle(
                pos=self.btn_weather.pos,
                size=self.btn_weather.size,
                radius=[dp(15)]
            )
            self.btn_weather.bind(
                pos=lambda i, v: setattr(self.btn_weather.rect, 'pos', i.pos),
                size=lambda i, v: setattr(self.btn_weather.rect, 'size', i.size)
            )

        # 按钮3: 查询新闻
        self.btn_news = RoundedButton(text='📰 家乡最新新闻')
        self.btn_news.bind(on_press=self.show_news)
        with self.btn_news.canvas.before:
            Color(0.4, 0.8, 0.4, 1)  # 绿色
            self.btn_news.rect = RoundedRectangle(
                pos=self.btn_news.pos,
                size=self.btn_news.size,
                radius=[dp(15)]
            )
            self.btn_news.bind(
                pos=lambda i, v: setattr(self.btn_news.rect, 'pos', i.pos),
                size=lambda i, v: setattr(self.btn_news.rect, 'size', i.size)
            )

        btn_layout.add_widget(self.btn_address)
        btn_layout.add_widget(self.btn_weather)
        btn_layout.add_widget(self.btn_news)

        # 状态标签
        self.status_label = Label(
            text='请先输入你的家乡地址',
            font_size=dp(14),
            size_hint_y=0.15,
            color=(0.5, 0.5, 0.5, 1)
        )

        # 底部信息
        footer = Label(
            text='© 2024 家乡助手',
            font_size=dp(12),
            size_hint_y=0.05,
            color=(0.7, 0.7, 0.7, 1)
        )

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(btn_layout)
        layout.add_widget(self.status_label)
        layout.add_widget(footer)

        # 设置背景
        with layout.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i, v: setattr(self.bg_rect, 'pos', i.pos),
                    size=lambda i, v: setattr(self.bg_rect, 'size', i.size))

        self.add_widget(layout)

    def show_address_input(self, instance):
        """显示地址输入弹窗"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # 提示标签
        hint_label = Label(
            text='请输入你的家乡地址\n请精确到村庄或街道',
            font_size=dp(16),
            size_hint_y=0.3,
            halign='center'
        )
        hint_label.bind(size=hint_label.setter('text_size'))

        # 地址输入框
        address_input = TextInput(
            hint_text='例如：山东省济南市历下区趵突泉街道',
            font_size=dp(16),
            size_hint_y=0.3,
            multiline=False
        )

        # 按钮布局
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=dp(10))

        cancel_btn = Button(text='取消', font_size=dp(16))
        confirm_btn = Button(text='完成', font_size=dp(16))

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(confirm_btn)

        content.add_widget(hint_label)
        content.add_widget(address_input)
        content.add_widget(btn_layout)

        popup = Popup(
            title='📍 输入家乡地址',
            content=content,
            size_hint=(0.9, 0.5),
            auto_dismiss=False
        )

        cancel_btn.bind(on_press=popup.dismiss)

        def on_confirm(btn):
            address = address_input.text.strip()
            if not address:
                self.show_toast("请输入地址")
                return
            popup.dismiss()
            self.process_address(address)

        confirm_btn.bind(on_press=on_confirm)

        popup.open()

    def process_address(self, address):
        """处理输入的地址"""
        self.show_toast("正在定位...")

        # 地理编码
        result = self.location_service.geocode(address)

        if result["success"]:
            self.location_service.saved_address = result["formatted_address"]
            self.location_service.saved_location = result["location"]
            self.location_service.saved_adcode = result.get("adcode", "")

            # 更新状态
            self.status_label.text = f"已设置: {result['formatted_address']}"

            # 打开卫星地图
            lng, lat = result["location"]
            map_result = self.location_service.open_satellite_map(lng, lat, result["formatted_address"])

            if map_result["success"]:
                self.show_toast(f"已打开{map_result['service']}\n{result['message']}")
            else:
                self.show_toast("无法打开地图应用")
        else:
            self.show_toast(f"定位失败: {result['message']}")

    def show_weather(self, instance):
        """显示天气信息"""
        if not self.location_service.saved_address:
            self.show_toast("请先输入家乡地址")
            return

        adcode = self.location_service.saved_adcode
        if not adcode:
            # 如果没有 adcode，尝试重新获取
            result = self.location_service.geocode(self.location_service.saved_address)
            if result["success"]:
                adcode = result.get("adcode", "")
                self.location_service.saved_adcode = adcode

        if adcode:
            result = self.location_service.get_weather(adcode)
        else:
            # 演示模式
            result = self.location_service.get_weather("")

        if result["success"]:
            weather = result["weather"]
            content_text = (
                f"🏙️ 城市: {weather['city']}\n\n"
                f"🌡️ 温度: {weather['temperature']}°C\n\n"
                f"☁️ 天气: {weather['weather']}\n\n"
                f"💨 风力: {weather['wind']}\n\n"
                f"💧 湿度: {weather['humidity']}"
            )
        else:
            content_text = f"获取天气失败\n{result['message']}"

        content = BoxLayout(orientation='vertical', padding=dp(20))
        weather_label = Label(
            text=content_text,
            font_size=dp(18),
            halign='left',
            valign='middle'
        )
        weather_label.bind(size=weather_label.setter('text_size'))
        content.add_widget(weather_label)

        popup = Popup(
            title=f'🌤️ {self.location_service.saved_address} 天气',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()

    def show_news(self, instance):
        """搜索并显示家乡新闻"""
        if not self.location_service.saved_address:
            self.show_toast("请先输入家乡地址")
            return

        result = self.location_service.search_local_news(self.location_service.saved_address)

        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        info_label = Label(
            text=f'将搜索"{result["county"]}"相关新闻\n（近3天内）',
            font_size=dp(16),
            size_hint_y=0.3
        )

        btn_layout = BoxLayout(size_hint_y=0.4, spacing=dp(10), orientation='vertical')

        baidu_btn = Button(text='📰 百度新闻搜索', font_size=dp(16))
        wechat_btn = Button(text='💬 微信公众号文章', font_size=dp(16))

        def open_baidu(btn):
            webbrowser.open(result["baidu_news"])
            self.show_toast("已打开百度新闻")

        def open_wechat(btn):
            webbrowser.open(result["wechat"])
            self.show_toast("已打开微信搜索")

        baidu_btn.bind(on_press=open_baidu)
        wechat_btn.bind(on_press=open_wechat)

        btn_layout.add_widget(baidu_btn)
        btn_layout.add_widget(wechat_btn)

        content.add_widget(info_label)
        content.add_widget(btn_layout)

        popup = Popup(
            title='📰 家乡新闻搜索',
            content=content,
            size_hint=(0.9, 0.6)
        )
        popup.open()

    def show_toast(self, message):
        """显示提示消息"""
        content = Label(text=message, font_size=dp(16))
        popup = Popup(
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()
        # 2秒后自动关闭
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)


# ==================== 主应用 ====================

class HometownApp(App):
    """主应用类"""

    def build(self):
        # 设置窗口大小（桌面调试用）
        Window.size = (360, 640)

        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))

        return sm

    def on_start(self):
        """应用启动时检查位置服务"""
        if HAS_PLYER:
            try:
                # 尝试获取 GPS 状态
                pass
            except:
                pass


# ==================== 入口 ====================

if __name__ == '__main__':
    HometownApp().run()
