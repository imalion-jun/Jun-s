name: Build Android APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # 允许手动触发

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          python3-pip \
          python3-dev \
          build-essential \
          git \
          zip \
          unzip \
          openjdk-17-jdk \
          autoconf \
          libtool \
          pkg-config \
          zlib1g-dev \
          libncurses5-dev \
          libncursesw5-dev \
          libtinfo5 \
          cmake \
          libffi-dev \
          libssl-dev \
          automake
        pip install buildozer cython
        
    - name: Build APK
      run: |
        buildozer android debug
      timeout-minutes: 120
      
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: healthcare-app-apk
        path: bin/*.apk
        if-no-files-found: error