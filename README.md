# 智能文本词频分析平台

一个基于 Streamlit + jieba + pyecharts 的智能中文文本词频分析 Web 应用。

## ✨ 功能特性

- 🔗 **智能网页抓取** - 输入任意中文网页 URL，自动提取正文内容
- ✂️ **jieba 中文分词** - 高精度中文分词引擎，支持中英文混排
- 📊 **词频统计分析** - 自动过滤停用词和低频词，精准提取关键词
- 🎨 **多维可视化** - 8 种精美图表（词云、柱状图、折线图、饼图、漏斗图、雷达图、散点图、热力图）
- 🎛️ **交互式参数** - 可调节词频阈值、词长限制、图表主题、展示数量等参数
- 📥 **数据导出** - 支持 CSV 格式完整词频数据下载

## 🛠️ 技术栈

- **Web 框架**: [Streamlit](https://streamlit.io/)
- **分词引擎**: [jieba](https://github.com/fxsjy/jieba)
- **可视化库**: [pyecharts](https://pyecharts.org/)
- **HTML 解析**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- **HTTP 请求**: [requests](https://requests.readthedocs.io/)

## 🚀 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone <your-repository-url>
cd <project-directory>

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux / macOS
# 或在 Windows 上:
# venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
streamlit run app.py
```

应用将在 `http://localhost:8501` 启动。

## 📁 项目结构

```
.
├── app.py              # 主应用文件
├── requirements.txt    # Python 依赖
├── runtime.txt         # Python 运行时版本
├── netlify.toml        # Netlify 部署配置
└── README.md           # 项目说明文档
```

## 🎯 使用方法

1. **输入文章链接**: 在左侧栏输入中文网页 URL
2. **调整分析参数**: 设置词频阈值、词长、展示数量等
3. **选择图表类型**: 从 8 种图表中选择可视化方式
4. **切换图表主题**: 7 种配色风格可选
5. **点击分析按钮**: 一键抓取、分词、生成分析报告

## 🌐 部署方案

### 方案一：Streamlit Community Cloud（推荐）

1. 将代码上传到 GitHub 仓库
2. 访问 [Streamlit Community Cloud](https://streamlit.io/cloud)
3. 连接 GitHub 仓库，选择 `app.py` 作为入口文件
4. 应用将自动部署，可通过公共 URL 访问

### 方案二：其他平台

本项目也支持部署到以下平台：

- **Railway** - 一键部署 Python 应用
- **Render** - 简单易用的云平台
- **Heroku** - 需要添加 `Procfile`

### 关于 Netlify

Netlify 主要用于静态网站部署，不直接支持 Streamlit 等需要 Python 运行时的应用。建议使用上述方案。

## 📝 注意事项

- 应用需要访问外网以抓取网页内容，部署时请确保网络访问正常
- 某些网站可能具有反爬虫机制，可能导致抓取失败
- 建议用于分析公开可访问的新闻、博客、文章等内容
- 首次运行时 jieba 会自动初始化词典，请耐心等待

## 📄 License

MIT License
