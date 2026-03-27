# Google Colab 构建 APK 指南

## 优点
- ✅ 完全免费
- ✅ 无需安装任何软件
- ✅ 有 GPU/CPU 资源
- ✅ 浏览器里完成所有操作

---

## 使用步骤

### 第一步：打开 Colab

1. 访问 https://colab.research.google.com/
2. 登录 Google 账号（没有就注册一个）
3. 点击 **文件 → 上传笔记本**
4. 选择 `colab_build.ipynb` 文件上传

### 第二步：准备代码

1. 打开项目目录的 `main.py`，复制全部内容
2. 打开 `buildozer.spec`，复制全部内容
3. 回到 Colab，找到对应的代码块，把内容粘贴进去

### 第三步：运行构建

1. 点击菜单：**运行时 → 更改运行时类型 → 选择 CPU**
2. 按顺序点击每个代码块左侧的 **播放按钮** ▶️
3. 等待构建完成（约 30-60 分钟）
4. 最后一个代码块会自动下载 APK 文件

---

## 注意事项

- 构建过程中不要关闭浏览器标签页
- 如果断开连接，可以重新连接后继续
- Colab 免费版最长运行 12 小时，足够构建 APK

---

## 快速链接

- [Google Colab](https://colab.research.google.com/)
- [Kivy 官方文档](https://kivy.org/doc/stable/)
- [Buildozer 文档](https://buildozer.readthedocs.io/)
