{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "name": "Build Healthcare Android APK"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# 🏥 血糖监测 App - Android APK 构建\n",
        "\n",
        "在 Google Colab 中免费构建 Android APK\n",
        "\n",
        "**步骤：**\n",
        "1. 点击菜单：文件 → 在云端硬盘中保存副本\n",
        "2. 按顺序运行以下代码块\n",
        "3. 构建完成后下载 APK"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 第一步：安装依赖"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "!apt-get update -qq\n",
        "!apt-get install -qq -y \\\n",
        "    python3-pip python3-dev build-essential git zip unzip \\\n",
        "    openjdk-17-jdk autoconf libtool pkg-config \\\n",
        "    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \\\n",
        "    cmake libffi-dev libssl-dev automake"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 第二步：安装 Buildozer"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "!pip install -q buildozer cython"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 第三步：创建项目文件\n",
        "\n",
        "把 main.py 和 buildozer.spec 的内容粘贴到这里"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# 创建项目目录\n",
        "!mkdir -p /content/healthcare_android\n",
        "%cd /content/healthcare_android\n",
        "\n",
        "# 创建 main.py（请把 main.py 的完整内容粘贴到下面的三引号之间）\n",
        "main_py_content = '''\n",
        "# 请粘贴 main.py 的完整内容到这里\n",
        "'''\n",
        "\n",
        "with open('main.py', 'w', encoding='utf-8') as f:\n",
        "    f.write(main_py_content)\n",
        "\n",
        "print('main.py 已创建')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# 创建 buildozer.spec（请把 buildozer.spec 的完整内容粘贴到下面的三引号之间）\n",
        "buildozer_spec_content = '''\n",
        "# 请粘贴 buildozer.spec 的完整内容到这里\n",
        "'''\n",
        "\n",
        "with open('buildozer.spec', 'w', encoding='utf-8') as f:\n",
        "    f.write(buildozer_spec_content)\n",
        "\n",
        "print('buildozer.spec 已创建')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 第四步：构建 APK（约 30-60 分钟）"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# 开始构建\n",
        "!buildozer android debug"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## 第五步：下载 APK"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# 列出生成的 APK 文件\n",
        "!ls -la /content/healthcare_android/bin/"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# 下载 APK（运行后会提示下载）\n",
        "from google.colab import files\n",
        "import glob\n",
        "\n",
        "apk_files = glob.glob('/content/healthcare_android/bin/*.apk')\n",
        "if apk_files:\n",
        "    for apk in apk_files:\n",
        "        print(f'下载: {apk}')\n",
        "        files.download(apk)\n",
        "else:\n",
        "    print('未找到 APK 文件，请检查构建是否成功')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "---\n",
        "\n",
        "## ✅ 完成！\n",
        "\n",
        "APK 文件已下载到本地，可以安装到 Android 手机了。"
      ]
    }
  ]
}