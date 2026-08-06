# 🚀 局域网档案共享中心 (LAN File Share)

这是一个基于 Python Flask 开发的轻量级、高质感的局域网文件共享工具。无需任何复杂的配置，只需在主电脑上运行即可将设备化身为局域网内的“私有云盘”，让手机、平板、以及其他电脑通过浏览器跨平台进行文件的上传与下载。

本设计源于对CSDN中Python Flask - 实现本地文件的上传与下载https://blog.csdn.net/TomorrowAndTuture/article/details/118495072 ，
的学习并根据自身实际情况设计的内容。
<img width="1920" height="1016" alt="image" src="https://github.com/user-attachments/assets/d68dbf34-0a43-44e8-afa5-6f6493d4cad1" />

## ✨ 核心功能特性

* **🔌 即插即用 (零配置)**
  程序启动时会自动获取并打印本机的局域网 IP 地址。局域网内的任何设备无需安装客户端，直接使用浏览器访问该 IP 即可使用。
* **📁 智能文件分类**
  内置扩展名识别引擎，上传的文件将自动归档至对应的专属资料夹：
  * `🗂️ 文件` (PDF, Word, Excel, PPT, TXT, MD)
  * `🖼️ 图片` (JPG, PNG, GIF, WEBP, SVG)
  * `🎬 影音` (MP4, MKV, MP3, WAV 等)
  * `📦 压缩档` (ZIP, RAR, 7Z, TAR 等)
  * `📝 其他` (未识别格式)
* **✨ 丝滑的交互体验**
  支持原生 **拖拽上传 (Drag & Drop)**。底层采用 AJAX (XMLHttpRequest) 异步传输技术，并附带 **实时上传进度条**，传输 GB 级大文件时页面不卡顿、不白屏。
* **🛡️ 安全与防呆机制**
  * 完美支持 **中文文件名**。
  * 自动在文件名中追加时间戳（Timestamp），彻底解决同名文件互相覆盖的隐患。
  * 提供防误触的「一键删除」确认弹窗。
* **🎨 纯净的高质感 UI**
  前端采用纯原生 CSS 精心雕琢，拥有现代化的圆角卡片、阴影反馈与悬浮动画，不依赖任何庞大的外部前端框架。

---

## 💻 环境依赖

请确保你的系统已安装 Python 3.x，并安装 Flask 框架及其依赖：

```bash
pip install flask werkzeug
