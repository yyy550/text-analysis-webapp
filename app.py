import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Line, Pie, Funnel, Radar, Scatter, HeatMap
from pyecharts import options as opts
from pyecharts.globals import ThemeType


st.set_page_config(
    page_title="智能文本词频分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecf7 100%);
    }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8faff 100%);
        border-right: 1px solid #e8ecf4;
    }
    section[data-testid="stSidebar"] > div:first-child {
        background-image: linear-gradient(180deg, #ffffff 0%, #f8faff 100%);
    }
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .app-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    .hero-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.35);
    }
    .hero-card h2 {
        color: white !important;
        margin-bottom: 0.3rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #eef1f7;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    .stat-card .label {
        color: #6b7280;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .stat-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-card .icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .section-title {
        font-size: 1.5rem !important;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
        display: inline-block;
    }
    .feature-item {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-bottom: 0.6rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .feature-item .feature-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.2rem;
    }
    .feature-item .feature-desc {
        color: #6b7280;
        font-size: 0.9rem;
    }
    div[role="alert"] {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.6rem 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    .stSelectbox > div > div > div > div {
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    div[data-testid="stTable"] {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        overflow-x: auto;
    }
    div[data-testid="stTable"] table {
        border-collapse: collapse;
        width: 100%;
    }
    div[data-testid="stTable"] th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 1rem !important;
        text-align: left !important;
    }
    div[data-testid="stTable"] td {
        padding: 0.7rem 1rem !important;
        border-bottom: 1px solid #f1f3f7 !important;
    }
    div[data-testid="stTable"] tr:hover td {
        background: #f8faff;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        margin-top: 1rem;
    }
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 1rem -1rem;
        color: white;
        border-radius: 0;
    }
    .sidebar-header h1, .sidebar-header h2, .sidebar-header h3 {
        color: white !important;
    }
    [data-testid="stMarkdownContainer"] p {
        line-height: 1.7;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #9ca3af;
        font-size: 0.9rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


STOPWORDS = {
    "的", "了", "是", "在", "和", "及", "与", "等", "为", "对", "将", "有", "无", "不", "都", "可",
    "能", "会", "要", "让", "使", "被", "从", "到", "于", "以", "按", "经", "由", "共", "每", "各",
    "个", "件", "篇", "号", "年", "月", "日", "时", "分", "秒", "我", "你", "他", "她", "它", "我们",
    "你们", "他们", "这", "那", "此", "彼", "之", "其", "也", "还", "又", "但", "而", "或", "且", "则",
    "就", "却", "并", "虽", "然", "因", "为", "所", "以", "着", "过", "啊", "呀", "吗", "呢", "吧", "啦",
    "地", "得", "登录", "注册", "首页", "通知公告", "媒体聚焦", "比赛入口", "回到官网", "可以",
    "这个", "那个", "这样", "那样", "如何", "什么", "哪些", "自己", "大家", "没有", "已经", "进行",
    "一个", "两个", "三个", "一些", "一种", "其中", "通过", "作为", "成为", "实现", "开始", "结束",
    "需要", "提供", "包括", "表示", "认为", "看到", "知道", "觉得", "来说", "对于", "但是", "同时",
    "如果", "因为", "所以", "虽然", "但是", "而且", "或者", "以及", "不仅", "只是", "还有", "一下",
    "一切", "所有", "现在", "以后", "以前", "今天", "昨天", "明天", "这里", "那里", "上面", "下面"
}


CHART_THEMES = {
    "🌌 极简科技": ThemeType.LIGHT,
    "🌙 暗夜模式": ThemeType.DARK,
    "🎨 活力多彩": ThemeType.ROMANTIC,
    "🖼️ 经典黑白": ThemeType.SHINE,
    "🌴 清新绿意": ThemeType.VINTAGE,
    "🔷 商务蓝调": ThemeType.MACARONS,
    "🌸 柔和粉紫": ThemeType.CHALK,
}


def render_sidebar():
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
        <h3 style="margin: 0; font-size: 1.3rem;">分析控制台</h3>
        <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 0.3rem;">配置您的分析参数</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 📝 输入数据源")
    url = st.sidebar.text_input(
        "文章链接 URL",
        placeholder="例如：https://cpc.people.com.cn/n1/...",
        help="请粘贴一篇中文网页文章的完整URL地址"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛️ 分析参数")

    min_freq = st.sidebar.slider(
        "最低词频阈值",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
        help="过滤掉词频低于此值的词汇，帮助提取更有意义的关键词"
    )

    top_n = st.sidebar.slider(
        "Top N 词汇展示",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="显示词频排名前N个词汇"
    )

    min_word_len = st.sidebar.slider(
        "最短词长",
        min_value=1,
        max_value=5,
        value=2,
        help="过滤短于该长度的词汇（中文建议2-3）"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 可视化设置")

    chart_type = st.sidebar.selectbox(
        "图表类型",
        [
            "☁️ 词云图",
            "📊 柱状图",
            "📈 折线图",
            "🥧 饼图",
            "🔻 漏斗图",
            "🕸️ 雷达图",
            "💫 散点图",
            "🔥 热力图",
        ],
        index=0,
        help="选择要展示的词频可视化图表"
    )

    theme_choice = st.sidebar.selectbox(
        "图表主题",
        list(CHART_THEMES.keys()),
        index=0,
        help="选择图表的配色风格"
    )

    chart_width = st.sidebar.slider("图表宽度 (px)", 800, 1400, 1100, 50)
    chart_height = st.sidebar.slider("图表高度 (px)", 400, 900, 650, 50)

    st.sidebar.markdown("---")
    analyze_btn = st.sidebar.button("🚀 开始智能分析")

    st.sidebar.markdown("""
    <div style="padding: 1rem; background: #f8faff; border-radius: 12px; margin-top: 1rem; font-size: 0.85rem; color: #6b7280; line-height: 1.6;">
        <strong>💡 使用提示</strong><br>
        • 粘贴新闻、博客等网页链接<br>
        • 调整阈值过滤低频词<br>
        • 切换图表查看不同视角<br>
        • 支持中英文混排内容分析
    </div>
    """, unsafe_allow_html=True)

    return url, min_freq, top_n, min_word_len, chart_type, theme_choice, chart_width, chart_height, analyze_btn


def fetch_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Referer": url,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = response.apparent_encoding
        if response.status_code != 200:
            st.error(f"❌ 请求失败，状态码：{response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript"]):
            tag.decompose()

        text_blocks = []
        for p in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "article"]):
            txt = p.get_text(strip=True)
            if len(txt) > 10:
                text_blocks.append(txt)

        if not text_blocks:
            if soup.body:
                text = soup.body.get_text(separator=" ")
            else:
                text = soup.get_text(separator=" ")
        else:
            text = " ".join(text_blocks)

        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except requests.exceptions.Timeout:
        st.error("⏱️ 请求超时，请检查网络连接或更换URL")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 无法连接到目标网站，请检查URL是否正确")
        return None
    except Exception as e:
        st.error(f"⚠️ 抓取失败：{str(e)}")
        return None


def segment_and_count(text, min_word_len=2):
    if not text:
        return None
    words = jieba.lcut(text, cut_all=False)
    filtered_words = [
        word for word in words
        if len(word) >= min_word_len
        and word not in STOPWORDS
        and not word.isdigit()
        and not all(c == ' ' for c in word)
    ]
    if not filtered_words:
        st.warning("😕 分词后未得到有效词汇，请尝试调整参数或更换文章")
        return None
    return Counter(filtered_words)


def filter_low_freq(word_freq, min_freq):
    filtered = {word: freq for word, freq in word_freq.items() if freq >= min_freq}
    if not filtered:
        return None
    return filtered


def generate_chart(chart_type, word_freq, theme_choice, top_n=20, width="1100px", height="650px"):
    theme = CHART_THEMES.get(theme_choice, ThemeType.LIGHT)
    sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_words = sorted_freq[:top_n]
    top5 = sorted_freq[:5]
    top10 = sorted_freq[:10]
    top50 = sorted_freq[:50]

    init_opts = opts.InitOpts(theme=theme, width=width, height=height)

    if chart_type.startswith("☁️"):
        chart = (
            WordCloud(init_opts=init_opts)
            .add("", sorted_freq[:100], word_size_range=[20, 100], shape="circle")
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="☁️ 文本词云图",
                    subtitle=f"共展示 {len(sorted_freq[:100])} 个高频词汇",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")
                ),
                tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {c}")
            )
        )
    elif chart_type.startswith("📊"):
        chart = (
            Bar(init_opts=init_opts)
            .add_xaxis([w for w, f in top_words])
            .add_yaxis("词频", [f for w, f in top_words],
                       color="#667eea",
                       label_opts=opts.LabelOpts(position="top"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"📊 词频 Top-{top_n} 柱状图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, font_size=12),
                                         name="词汇"),
                yaxis_opts=opts.AxisOpts(name="出现频次"),
                datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
            )
            .set_series_opts(
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="平均")])
            )
        )
    elif chart_type.startswith("📈"):
        chart = (
            Line(init_opts=init_opts)
            .add_xaxis([w for w, f in top_words])
            .add_yaxis("词频", [f for w, f in top_words],
                       color="#764ba2",
                       is_smooth=True,
                       symbol="circle",
                       symbol_size=10,
                       label_opts=opts.LabelOpts(is_show=True, position="top"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"📈 词频 Top-{top_n} 折线图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, font_size=12),
                                         name="词汇"),
                yaxis_opts=opts.AxisOpts(name="出现频次"),
                tooltip_opts=opts.TooltipOpts(trigger="axis")
            )
        )
    elif chart_type.startswith("🥧"):
        chart = (
            Pie(init_opts=init_opts)
            .add("", top_words, radius=["35%", "70%"], rosetype="radius")
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"🥧 词频 Top-{top_n} 饼图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")),
                legend_opts=opts.LegendOpts(orient="vertical", pos_left="5%", pos_top="middle")
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
        )
    elif chart_type.startswith("🔻"):
        chart = (
            Funnel(init_opts=init_opts)
            .add("词频", top_words[:20], 
                 label_opts=opts.LabelOpts(position="right", formatter="{b}: {c}", font_size=12),
                 gap=2)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"🔻 词频 Top-20 漏斗图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"))
            )
        )
    elif chart_type.startswith("🕸️"):
        if len(top5) < 3:
            st.warning("⚠️ 词频前5词汇不足，无法生成雷达图")
            return None
        chart = (
            Radar(init_opts=init_opts)
            .add_schema(
                schema=[opts.RadarIndicatorItem(name=w, max_=f + 5) for w, f in top5],
                splitarea_opt=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
            )
            .add("词频", [[f for w, f in top5]],
                 areastyle_opts=opts.AreaStyleOpts(opacity=0.4),
                 color="#667eea")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="🕸️ 词频 Top-5 雷达图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"))
            )
        )
    elif chart_type.startswith("💫"):
        chart = (
            Scatter(init_opts=init_opts)
            .add_xaxis([len(w) for w, f in top50])
            .add_yaxis("词频", [f for w, f in top50],
                       label_opts=opts.LabelOpts(is_show=False),
                       symbol_size=15,
                       color="#764ba2")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="💫 词汇长度 vs 词频散点图 (Top-50)",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")),
                xaxis_opts=opts.AxisOpts(name="词汇长度（字数）", min_=1),
                yaxis_opts=opts.AxisOpts(name="出现频次"),
                tooltip_opts=opts.TooltipOpts(formatter=lambda p: f"词长: {p['name']}<br>词频: {p['value'][1]}")
            )
        )
    elif chart_type.startswith("🔥"):
        if not top10:
            st.warning("⚠️ 词频前10词汇不足，无法生成热力图")
            return None
        max_freq = max(f for w, f in top10)
        data = [[i, 0, f] for i, (w, f) in enumerate(top10)]
        chart = (
            HeatMap(init_opts=init_opts)
            .add_xaxis([w for w, f in top10])
            .add_yaxis("词频", ["热度"], data)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="🔥 词频 Top-10 热力图",
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold")),
                visualmap_opts=opts.VisualMapOpts(max_=max_freq, min_=0, is_piecewise=True,
                                                  pos_right="5%", pos_top="middle")
            )
        )
    else:
        st.error("❌ 不支持的图表类型")
        return None

    try:
        return chart.render_embed()
    except Exception:
        try:
            chart.render("temp_chart.html")
            with open("temp_chart.html", "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None


def render_welcome():
    st.markdown("""
    <h1 class="app-title">📊 智能文本词频分析平台</h1>
    <p class="subtitle">✨ 基于 jieba 分词 + pyecharts 可视化的智能文本内容洞察工具</p>

    <div class="hero-card">
        <h2 style="color: white; font-size: 1.6rem; margin-bottom: 0.8rem;">🎯 一键分析，洞察文本核心信息</h2>
        <p style="font-size: 1.05rem; line-height: 1.8; opacity: 0.95; margin: 0;">
            只需输入一篇网页文章的URL，系统将自动抓取内容、智能分词、统计词频，
            并通过多种精美的可视化图表为您呈现文章的关键词汇与核心主题。
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">🌟 核心功能亮点</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">🔗</div>
            <div class="label">智能抓取</div>
            <div class="value">URL</div>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">一键抓取网页正文内容</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">✂️</div>
            <div class="label">中文分词</div>
            <div class="value">jieba</div>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">高精度中文分词引擎</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">📊</div>
            <div class="label">词频分析</div>
            <div class="value">Counter</div>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">智能过滤停用词低频词</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="icon">🎨</div>
            <div class="label">多维可视化</div>
            <div class="value">8种</div>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">词云/柱状/饼图等图表</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height: 2rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">📖 快速使用指南</h2>', unsafe_allow_html=True)

    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">① 输入文章链接</div>
            <div class="feature-desc">在左侧"输入数据源"中粘贴一篇中文网页文章的完整URL</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">② 调整分析参数</div>
            <div class="feature-desc">设置词频阈值、词汇长度、展示数量等参数过滤结果</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">③ 选择可视化方式</div>
            <div class="feature-desc">从8种图表中选择喜欢的展示方式，并自定义主题风格</div>
        </div>
        """, unsafe_allow_html=True)

    with guide_col2:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">④ 点击开始分析</div>
            <div class="feature-desc">系统自动抓取内容、分词、生成词频统计和可视化图表</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">⑤ 查看分析结果</div>
            <div class="feature-desc">查看词频排名表格、多维图表，快速掌握文章核心</div>
        </div>
        <div class="feature-item">
            <div class="feature-title">⑥ 交互式调整</div>
            <div class="feature-desc">随时调整参数，实时切换图表，深度挖掘文本信息</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height: 2rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">💡 适用场景</h2>', unsafe_allow_html=True)
    scene_col1, scene_col2, scene_col3 = st.columns(3)

    with scene_col1:
        st.markdown("""
        <div class="feature-item" style="border-left-color: #10b981;">
            <div class="feature-title">📰 新闻内容分析</div>
            <div class="feature-desc">快速提取新闻热点关键词，了解报道核心主题</div>
        </div>
        """, unsafe_allow_html=True)
    with scene_col2:
        st.markdown("""
        <div class="feature-item" style="border-left-color: #f59e0b;">
            <div class="feature-title">📚 学术论文概览</div>
            <div class="feature-desc">从论文链接中提取研究重点与关键术语</div>
        </div>
        """, unsafe_allow_html=True)
    with scene_col3:
        st.markdown("""
        <div class="feature-item" style="border-left-color: #ef4444;">
            <div class="feature-title">🔍 竞品内容调研</div>
            <div class="feature-desc">分析竞品博客与官网内容，识别差异化主题</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <div style="font-size: 1rem; margin-bottom: 0.3rem;">
            🌈 基于 Streamlit + jieba + pyecharts 构建 · 为中文文本分析而生
        </div>
        <div style="font-size: 0.8rem; opacity: 0.7;">
            👉 请在左侧栏输入文章URL并点击"开始智能分析"按钮开始使用
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_analysis_results(text, word_freq, filtered_freq, top_n, chart_type, theme_choice, chart_width, chart_height, url):
    st.markdown("""
    <h1 class="app-title">📊 智能文本词频分析平台</h1>
    <p class="subtitle">✨ 分析结果展示 · 洞察文本核心信息</p>
    """, unsafe_allow_html=True)

    total_chars = len(text) if text else 0
    total_words = sum(word_freq.values()) if word_freq else 0
    unique_words = len(word_freq) if word_freq else 0
    filtered_count = len(filtered_freq) if filtered_freq else 0

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem 2rem; border-radius: 16px; color: white; margin-bottom: 1.5rem;">
        <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">🔗 分析来源</div>
        <div style="font-size: 1rem; font-weight: 500; word-break: break-all;">""" + url + """</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">📈 分析概览</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="icon">📝</div>
            <div class="label">文本总字数</div>
            <div class="value">{total_chars:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="icon">🔤</div>
            <div class="label">分词总数</div>
            <div class="value">{total_words:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="icon">🆕</div>
            <div class="label">独立词汇</div>
            <div class="value">{unique_words:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="icon">🎯</div>
            <div class="label">过滤后词汇</div>
            <div class="value">{filtered_count:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height: 1rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown(f'<h2 class="section-title">🏆 词频排名 Top-{top_n} 词汇</h2>', unsafe_allow_html=True)
    top_words = sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]

    table_col1, table_col2 = st.columns([2, 1])

    with table_col1:
        table_data = [["排名", "词汇", "词频", "占比 (%)"]]
        total_filtered = sum(filtered_freq.values())
        for idx, (word, freq) in enumerate(top_words, 1):
            pct = round(freq / total_filtered * 100, 2) if total_filtered > 0 else 0
            table_data.append([f"#{idx}", word, freq, f"{pct}%"])
        st.table(table_data)

    with table_col2:
        st.markdown(f"""
        <div class="chart-container" style="padding: 1.5rem; margin-top: 0;">
            <div style="font-size: 1rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">📊 高频词汇速览</div>
        """, unsafe_allow_html=True)
        for idx, (word, freq) in enumerate(top_words[:10], 1):
            max_freq_item = top_words[0][1] if top_words else 1
            bar_width = int(freq / max_freq_item * 100)
            st.markdown(f"""
            <div style="margin-bottom: 0.6rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.2rem; color: #4b5563;">
                    <span>#{idx} <strong>{word}</strong></span>
                    <span style="font-weight: 600; color: #667eea;">{freq}</span>
                </div>
                <div style="background: #e5e7eb; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {bar_width}%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="height: 1.5rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<h2 class="section-title">🎨 词频可视化图表</h2>', unsafe_allow_html=True)
    chart_html = generate_chart(
        chart_type=chart_type,
        word_freq=filtered_freq,
        theme_choice=theme_choice,
        top_n=top_n,
        width=f"{chart_width}px",
        height=f"{chart_height}px"
    )

    if chart_html:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.components.v1.html(chart_html, width=chart_width + 40, height=chart_height + 80, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("😕 当前图表无法生成，请尝试其他图表类型")

    st.markdown("""
    <div style="height: 1.5rem;"></div>
    """, unsafe_allow_html=True)

    with st.expander("📄 查看抓取的原文内容预览（前500字）"):
        if text:
            preview = text[:500] + "..." if len(text) > 500 else text
            st.markdown(f"""
            <div style="background: #f8faff; padding: 1.5rem; border-radius: 12px; line-height: 1.8; color: #4b5563; font-size: 0.95rem;">
                {preview}
            </div>
            """, unsafe_allow_html=True)

    with st.expander("🔧 完整词频数据（下载）"):
        if filtered_freq:
            import pandas as pd
            df = pd.DataFrame(
                sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True),
                columns=["词汇", "词频"]
            )
            st.dataframe(df, width=800, height=400)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 下载词频数据 CSV",
                data=csv,
                file_name="词频分析结果.csv",
                mime="text/csv"
            )

    st.markdown("""
    <div class="footer">
        <div style="font-size: 1rem; margin-bottom: 0.3rem;">
            ✅ 分析完成 · 您可以在左侧调整参数或更换URL进行新一轮分析
        </div>
        <div style="font-size: 0.8rem; opacity: 0.7;">
            基于 Streamlit + jieba + pyecharts 构建 · 为中文文本分析而生
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    url, min_freq, top_n, min_word_len, chart_type, theme_choice, chart_width, chart_height, analyze_btn = render_sidebar()

    if analyze_btn and url:
        url_pattern = re.compile(
            r'^(https?://)'
            r'([\da-z\.-]+)'
            r'(\.[a-z\.]{2,6})'
            r'([/\.a-z0-9_-]*)*/*$',
            re.IGNORECASE
        )
        if not url_pattern.match(url.strip()):
            st.error("❌ URL格式不正确，请输入以 http:// 或 https:// 开头的有效网址")
            render_welcome()
            return

        with st.spinner("🔗 正在抓取网页文本内容，请稍候..."):
            text = fetch_text_from_url(url)
        if not text:
            render_welcome()
            return

        with st.spinner("✂️ 正在进行中文分词与词频统计..."):
            word_freq = segment_and_count(text, min_word_len)
        if not word_freq:
            render_welcome()
            return

        filtered_freq = filter_low_freq(word_freq, min_freq)
        if not filtered_freq:
            st.warning(f"😕 无词频 ≥ {min_freq} 的词汇，请尝试降低词频阈值或更换文章")
            render_welcome()
            return

        render_analysis_results(text, word_freq, filtered_freq, top_n, chart_type, theme_choice, chart_width, chart_height, url)

    elif analyze_btn and not url:
        st.warning("⚠️ 请先在左侧输入文章URL后再开始分析")
        render_welcome()

    else:
        render_welcome()


if __name__ == "__main__":
    main()
