import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
# KONFIGURASI HALAMAN
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MindBalance",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    return pd.read_csv("Mental_Health_Cleaned.csv")

df_raw = load_data()

@st.cache_data
def get_pattern():
    import base64
    with open("Pattern.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

pattern_b64 = get_pattern()

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL STYLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Root ────────────────────────────────────────────────────── */
:root {
    --bg:       #F0FAF4;
    --surface:  #E4F5EB;
    --surface2: #D6EFE0;
    --border:   #B7DEC5;
    --text:     #1E3A2A;
    --muted:    #5A8A6A;
    --lav:      #3A8C5C;
    --sky:      #2E86AB;
    --sage:     #4CAF7D;
    --rose:     #C0534A;
    --amber:    #C87F2A;
    --lav-dim:  rgba(58,140,92,.10);
    --sky-dim:  rgba(46,134,171,.10);
    --sage-dim: rgba(76,175,125,.10);
}

/* ── App shell ───────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] { background: var(--bg); }
[data-testid="stHeader"]           { background: var(--bg); }

/* ── Global text ─────────────────────────────────────────────── */
html, body, [class*="css"], p, span, div, label, li {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
    line-height: 1.65 !important;
}
h1 { font-size: 2rem !important; font-weight: 800 !important; color: #14321F !important; letter-spacing: -.02em !important; text-align: center !important; }
h2 { font-size: 1.2rem !important; font-weight: 700 !important; color: #1E5C35 !important; letter-spacing: -.01em !important; }
h3 { font-size: 1rem !important; font-weight: 700 !important; color: #2E7A4A !important; }

/* ── Divider ─────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── Sidebar ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 2px solid #3A8C5C !important;
    padding-top: 1.5rem !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    font-size: .9rem !important;
    font-weight: 500 !important;
}

/* ── Metric cards ────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 2px solid #3A8C5C !important;
    border-radius: 14px !important;
    padding: 1.4rem 1.6rem !important;
    box-shadow: 0 2px 8px rgba(58,140,92,.15) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #14321F !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .09em !important;
    color: #3A8C5C !important;
}
[data-testid="stMetricDelta"] { color: var(--sage) !important; font-size: .8rem !important; }

/* ── Tabs ────────────────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: var(--muted) !important;
    font-size: .83rem !important;
    font-weight: 500 !important;
    padding: .45rem 1rem !important;
    transition: color .2s !important;
    flex: 1 !important;
    justify-content: center !important;
}
[aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--text) !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.15) !important;
}

/* ── Selectbox / inputs ──────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: .86rem !important;
}
[data-testid="stNumberInput"] input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: .86rem !important;
    padding: .45rem .75rem !important;
}
[data-testid="stSlider"] > div > div > div { background: var(--lav) !important; }

/* ── Alerts ──────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: var(--surface2) !important;
    border-left-width: 3px !important;
    border-radius: 10px !important;
    font-size: .86rem !important;
    padding: .75rem 1rem !important;
}

/* ── Button ──────────────────────────────────────────────────── */
[data-testid="stFormSubmitButton"] button {
    background: var(--lav) !important;
    border: none !important;
    border-radius: 9px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    letter-spacing: .02em !important;
    padding: .6rem 1.4rem !important;
    transition: opacity .2s !important;
}
[data-testid="stFormSubmitButton"] button:hover { opacity: .85 !important; }

/* ── Dataframe ───────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ── Form ────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.4rem !important;
}

/* ── Caption / small text ────────────────────────────────────── */
[data-testid="stCaptionContainer"] p {
    font-size: .78rem !important;
    color: var(--muted) !important;
    letter-spacing: .01em !important;
}

/* ── Section label ───────────────────────────────────────────── */
.section-label {
    font-size: .75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: var(--lav);
    margin-bottom: .3rem;
}
.bq-tag {
    display: inline-block;
    font-size: .68rem;
    font-weight: 600;
    background: var(--lav-dim);
    color: var(--lav);
    border: 1px solid rgba(58,140,92,.25);
    border-radius: 5px;
    padding: .15rem .5rem;
    letter-spacing: .05em;
    margin-bottom: .6rem;
}

/* ── Sidebar logo ────────────────────────────────────────────── */
.sidebar-logo {
    display: block;
    width: 120px;
    margin: 0 auto 0.5rem auto;
    mix-blend-mode: multiply;   /* ← putih jadi transparan */
}

/* ── Hide Streamlit chrome ───────────────────────────────────── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Background Pattern ────────────────────────────────────────────────────────
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/png;base64,{pattern_b64}");
    background-repeat: repeat;
    background-size: 400px;
    opacity: 0.9;
    pointer-events: none;
    z-index: 0;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PALET & HELPERS
# ══════════════════════════════════════════════════════════════════════════════
C = {
    "lav":    "#3A8C5C", "sky":    "#2E86AB",
    "sage":   "#4CAF7D", "rose":   "#C0534A",
    "amber":  "#C87F2A", "lav_l":  "#6DBF90",
    "sky_l":  "#74C0DC", "sage_l": "#80D4A8",
    "muted":  "#5A8A6A", "bg":     "#F0FAF4",
    "card":   "#E4F5EB", "card2":  "#D6EFE0",
    "border": "#B7DEC5",
}

CONDITION_COLORS = {"Anxiety": C["lav"], "Depression": C["sky"], "Ptsd": C["rose"], "Bipolar": C["sage"]}
STRESS_COLORS    = {"Low": C["sage"], "Moderate": C["amber"], "High": C["rose"]}
EXERCISE_COLORS  = {"Low": C["rose"], "Moderate": C["amber"], "High": C["sage"]}
PALETTE          = [C["lav"], C["sky"], C["rose"], C["sage"], C["amber"], C["lav_l"]]

def base_layout(**kw):
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(214,239,224,0.6)",
        font=dict(family="DM Sans, sans-serif", color="#1E3A2A", size=11),
        margin=dict(l=16, r=16, t=36, b=16),
        legend=dict(
            bgcolor="rgba(228,245,235,0.95)", bordercolor=C["border"], borderwidth=1,
            font=dict(size=10), itemsizing="constant",
        ),
        xaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"],
                   tickfont=dict(color=C["muted"], size=10),
                   title_font=dict(color=C["muted"], size=10), linecolor=C["border"]),
        yaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"],
                   tickfont=dict(color=C["muted"], size=10),
                   title_font=dict(color=C["muted"], size=10), linecolor=C["border"]),
    )
    d.update(kw)
    return d

def bq(n: str):
    st.markdown(f'<div class="bq-tag">BQ {n}</div>', unsafe_allow_html=True)

def section(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Logo.png", width=900)
    st.markdown("<p style='text-align:center; color:#5A8A6A; font-size:.95rem'>Analisis & Prediksi Tingkat Stres serta Rekomendasi Gaya Hidup</p>", unsafe_allow_html=True)
    st.divider()

    pilihan = st.selectbox(
        "Navigasi",
        ["Beranda", "Analisis Data", "Simulasi Prediksi"],
        label_visibility="collapsed",
    )

    st.divider()
    section("Pertanyaan Bisnis")
    st.markdown("""
<div style="font-size:.82rem; line-height:1.85; color:#3A6A4A">
<b style="color:#3A8C5C">BQ 1</b> &nbsp;Distribusi stres & kondisi mental<br>
<b style="color:#3A8C5C">BQ 2</b> &nbsp;Durasi tidur vs tingkat stres<br>
<b style="color:#3A8C5C">BQ 3</b> &nbsp;Olahraga vs happiness score<br>
<b style="color:#3A8C5C">BQ 4</b> &nbsp;Variabel numerik vs stres<br>
<b style="color:#3A8C5C">BQ 5</b> &nbsp;Pola harian per kondisi mental<br>
<b style="color:#3A8C5C">BQ 6</b> &nbsp;Diet vs happiness score
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.caption("Dataset  ·  3.000 responden")
    st.caption("7 negara  ·  12 variabel")


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1 — BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if pilihan == "Beranda":

    st.markdown("<h1 style='text-align:center; font-weight:800; font-size:2.2rem; color:#14321F'>MindBalance Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5A8A6A; font-size:.95rem'>Memahami hubungan gaya hidup digital dan kesehatan mental secara mendalam</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    # ── KPI ─────────────────────────────────────────────────────────────────
    # ── KPI ─────────────────────────────────────────────────────────────────
    kpi_data = [
        ("Total Responden", f"{len(df_raw):,}", "Dataset lengkap", "#3A8C5C"),
        ("Negara", str(df_raw["Country"].nunique()), "7 negara tercakup", "#2E86AB"),
        ("Kondisi Mental", str(df_raw["Mental Health Condition"].nunique()), "Kategori diagnosis", "#C0534A"),
        ("Variabel Dataset", str(len(df_raw.columns)), "Fitur analisis", "#C87F2A"),
    ]

    cols = st.columns(4, gap="small")
    for col, (label, value, badge, color) in zip(cols, kpi_data):
        col.markdown(f"""
<div style="background:#D6EFE0; border-radius:16px; padding:1.4rem 1.2rem 1.2rem 1.2rem;
    border-left:4px solid {color}; box-shadow:0 2px 10px rgba(58,140,92,.15);
    position:relative; overflow:hidden;">
    <div style="position:absolute; top:-10px; right:-10px; width:70px; height:70px;
        background:{color}22; border-radius:50%;"></div>
    <div style="font-size:.7rem; font-weight:700; text-transform:uppercase;
        letter-spacing:.1em; color:#5A8A6A; margin-bottom:.3rem;">{label}</div>
    <div style="font-size:2rem; font-weight:800; color:#14321F;
        font-family:'DM Mono',monospace; line-height:1.1; margin-bottom:.6rem;">{value}</div>
    <div style="display:inline-block; background:{color}22; color:{color};
        font-size:.72rem; font-weight:600; padding:.2rem .65rem;
        border-radius:20px; border:1px solid {color}55;">↑ {badge}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
    st.divider()

    col_a, col_spacer, col_b = st.columns([1, .04, 1], gap="small")


    # ── Kiri: Tentang ────────────────────────────────────────────────────────
    with col_a:
        section("Tentang Proyek")
        st.markdown("""
<p style="font-size:.88rem; color:#2E5A3A; margin-bottom:1rem">
MindBalance menganalisis hubungan antara gaya hidup digital dan kesehatan mental.
Dataset mencakup 3.000 responden dari 7 negara dengan variabel jam tidur, screen time,
pola makan, olahraga, dan skor kebahagiaan.
</p>
""", unsafe_allow_html=True)

        section("Variabel Dataset")
        vars_data = {
            "Variabel": [
                "Age", "Gender", "Country", "Exercise Level", "Diet Type",
                "Sleep Hours", "Stress Level", "Mental Health Condition",
                "Work Hours / Week", "Screen Time / Day",
                "Social Interaction Score", "Happiness Score",
            ],
            "Tipe": [
                "Numerik", "Kategori", "Kategori", "Kategori", "Kategori",
                "Numerik", "Kategori", "Kategori",
                "Numerik", "Numerik", "Numerik", "Numerik",
            ],
        }
        st.dataframe(
            pd.DataFrame(vars_data),
            use_container_width=True, hide_index=True,
            column_config={
                "Variabel": st.column_config.TextColumn(width="medium"),
                "Tipe":     st.column_config.TextColumn(width="small"),
            },
        )

    # ── Kanan: Charts ────────────────────────────────────────────────────────
    with col_b:
        section("Distribusi Kondisi Mental")
        cond_counts = df_raw["Mental Health Condition"].value_counts().reset_index()
        cond_counts.columns = ["Kondisi", "Jumlah"]
        fig_snap = go.Figure(go.Pie(
            labels=cond_counts["Kondisi"],
            values=cond_counts["Jumlah"],
            hole=0.6,
            marker=dict(
                colors=[CONDITION_COLORS.get(c, "#aaa") for c in cond_counts["Kondisi"]],
                line=dict(color=C["bg"], width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=11, color="#1E3A2A"),
            hovertemplate="<b>%{label}</b><br>%{value:,} orang (%{percent})<extra></extra>",
        ))
        fig_snap.add_annotation(
            text="<b>3,000</b><br><span style='font-size:11px'>responden</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#1E3A2A"), align="center",
        )
        fig_snap.update_layout(**base_layout(height=290, showlegend=True))
        st.plotly_chart(fig_snap, use_container_width=True)

        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        section("Responden per Negara")
        country_counts = df_raw["Country"].value_counts().reset_index()
        country_counts.columns = ["Negara", "Jumlah"]
        fig_country = go.Figure(go.Bar(
            x=country_counts["Negara"],
            y=country_counts["Jumlah"],
            marker=dict(
                color=country_counts["Jumlah"],
                colorscale=[[0, C["rose"]], [.5, C["lav"]], [1, C["sky"]]],
                showscale=False,
                line=dict(width=0),
            ),
            text=country_counts["Jumlah"],
            textposition="outside",
            textfont=dict(color="#3A6A4A", size=10),
            hovertemplate="<b>%{x}</b> · %{y:,}<extra></extra>",
        ))
        fig_country.update_layout(**base_layout(height=230, showlegend=False))
        st.plotly_chart(fig_country, use_container_width=True)

    st.divider()

    # ── Insight Utama ────────────────────────────────────────────────────────
    section("Insight Utama")
    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

    # Hitung insight dari data
    pct_high_stress   = (df_raw["Stress Level"] == "High").mean() * 100
    avg_sleep         = df_raw["Sleep Hours"].mean()
    avg_screen        = df_raw["Screen Time per Day (Hours)"].mean()
    avg_happiness     = df_raw["Happiness Score"].mean()
    top_condition     = df_raw["Mental Health Condition"].value_counts().idxmax()
    top_country       = df_raw["Country"].value_counts().idxmax()
    high_ex_hap       = df_raw[df_raw["Exercise Level"] == "High"]["Happiness Score"].mean()
    low_ex_hap        = df_raw[df_raw["Exercise Level"] == "Low"]["Happiness Score"].mean()
    sleep_low_stress  = df_raw[df_raw["Stress Level"] == "Low"]["Sleep Hours"].mean()
    sleep_high_stress = df_raw[df_raw["Stress Level"] == "High"]["Sleep Hours"].mean()

    insights = [
        {
            "icon": "😰",
            "title": f"{pct_high_stress:.0f}% Responden Stres Tinggi",
            "desc": f"Lebih dari sepertiga responden mengalami tingkat stres tinggi. Ini menjadi perhatian utama dalam analisis gaya hidup digital.",
            "color": "#C0534A",
        },
        {
            "icon": "😴",
            "title": f"Tidur & Stres Sangat Berkaitan",
            "desc": f"Responden stres rendah rata-rata tidur {sleep_low_stress:.1f} jam, sedangkan stres tinggi hanya {sleep_high_stress:.1f} jam — selisih {sleep_low_stress - sleep_high_stress:.1f} jam.",
            "color": "#2E86AB",
        },
        {
            "icon": "🏃",
            "title": f"Olahraga Tingkatkan Kebahagiaan",
            "desc": f"Mereka yang olahraga rutin (High) punya rata-rata Happiness Score {high_ex_hap:.2f}, dibandingkan {low_ex_hap:.2f} pada yang jarang olahraga (Low).",
            "color": "#4CAF7D",
        },
        {
            "icon": "📱",
            "title": f"Rata-rata Screen Time {avg_screen:.1f} Jam/Hari",
            "desc": f"Dengan rata-rata {avg_screen:.1f} jam per hari, penggunaan layar berlebih menjadi salah satu faktor risiko kesehatan mental.",
            "color": "#C87F2A",
        },
        {
            "icon": "🌍",
            "title": f"{top_country} Paling Banyak Responden",
            "desc": f"Data didominasi responden dari {top_country}. Kondisi mental terbanyak yang dilaporkan adalah {top_condition}.",
            "color": "#3A8C5C",
        },
        {
            "icon": "😊",
            "title": f"Rata-rata Happiness Score: {avg_happiness:.2f}/10",
            "desc": f"Skor kebahagiaan rata-rata {avg_happiness:.2f} dari skala 10. Terdapat variasi signifikan antar kondisi mental dan gaya hidup.",
            "color": "#1E5C35",
        },
    ]

    ins_cols = st.columns(3, gap="small")
    for i, ins in enumerate(insights):
        with ins_cols[i % 3]:
            st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-left:3px solid {ins['color']};
     border-radius:10px; padding:.85rem 1rem; margin-bottom:.6rem">
  <div style="font-size:1.1rem; margin-bottom:.3rem">{ins['icon']} <span style="font-size:.82rem; font-weight:600; color:{ins['color']}">{ins['title']}</span></div>
  <div style="font-size:.8rem; color:#3A6A4A; line-height:1.6">{ins['desc']}</div>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.caption("💡 Gunakan menu navigasi di sidebar untuk Analisis Data atau Simulasi Prediksi.")


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2 — ANALISIS DATA
# ══════════════════════════════════════════════════════════════════════════════
elif pilihan == "Analisis Data":

    st.markdown("<h1 style='text-align:center; font-weight:800; font-size:2.2rem; color:#14321F'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5A8A6A; font-size:.95rem'>Eksplorasi mendalam hubungan antar variabel kesehatan mental</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    # ── Filter Sidebar ───────────────────────────────────────────────────────
    with st.sidebar:
        st.divider()
        section("Filter Data")

        countries  = ["Semua"] + sorted(df_raw["Country"].unique().tolist())
        conditions = ["Semua"] + sorted(df_raw["Mental Health Condition"].unique().tolist())

        sel_country = st.selectbox("Negara",         countries)
        sel_cond    = st.selectbox("Kondisi Mental", conditions)
        sel_stress  = st.selectbox("Stres",          ["Semua", "Low", "Moderate", "High"])
        sel_gender  = st.selectbox("Gender",         ["Semua"] + sorted(df_raw["Gender"].unique().tolist()))

        age_min, age_max = int(df_raw["Age"].min()), int(df_raw["Age"].max())
        age_range = st.slider("Rentang Usia", age_min, age_max, (age_min, age_max))

    # ── Apply Filter ─────────────────────────────────────────────────────────
    df = df_raw.copy()
    if sel_country != "Semua": df = df[df["Country"] == sel_country]
    if sel_cond    != "Semua": df = df[df["Mental Health Condition"] == sel_cond]
    if sel_stress  != "Semua": df = df[df["Stress Level"] == sel_stress]
    if sel_gender  != "Semua": df = df[df["Gender"] == sel_gender]
    df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]
    n = len(df)

    # ── KPI ──────────────────────────────────────────────────────────────────
    kpi_eda = [
        ("Responden",     f"{n:,}",                                               "Total data",    "#3A8C5C"),
        ("Avg Happiness", f"{df['Happiness Score'].mean():.2f}",                  "Dari skala 10", "#2E86AB"),
        ("Avg Tidur",     f"{df['Sleep Hours'].mean():.1f} h",                    "Per malam",     "#4CAF7D"),
        ("Avg Screen",    f"{df['Screen Time per Day (Hours)'].mean():.1f} h",     "Per hari",      "#C87F2A"),
        ("Stres Tinggi",  f"{(df['Stress Level']=='High').mean()*100:.1f}%",      "Dari total",    "#C0534A"),
    ]

    cols_kpi = st.columns(5, gap="small")
    for col, (label, value, badge, color) in zip(cols_kpi, kpi_eda):
        col.markdown(f"""
<div style="
    background: #D6EFE0;
    border-radius: 16px;
    padding: 1.2rem 1rem 1rem 1rem;
    border-left: 4px solid {color};
    box-shadow: 0 2px 10px rgba(58,140,92,.15);
    position: relative;
    overflow: hidden;
">
    <div style="
        position:absolute; top:-10px; right:-10px;
        width:60px; height:60px;
        background: {color}22;
        border-radius: 50%;
    "></div>
    <div style="
        font-size:.68rem;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:.1em;
        color:#5A8A6A;
        margin-bottom:.25rem;
    ">{label}</div>
    <div style="
        font-size:1.7rem;
        font-weight:800;
        color:#14321F;
        font-family:'DM Mono', monospace;
        line-height:1.1;
        margin-bottom:.5rem;
    ">{value}</div>
    <div style="
        display:inline-block;
        background:{color}22;
        color:{color};
        font-size:.68rem;
        font-weight:600;
        padding:.15rem .55rem;
        border-radius:20px;
        border: 1px solid {color}55;
    ">↑ {badge}</div>
</div>
""", unsafe_allow_html=True)

    st.divider()


    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "  Demografi & Target  ",
        "  Gaya Hidup  ",
        "  Kondisi Mental  ",
        "  Korelasi  ",
    ])

    # ════════════════════════════════════════
    # TAB 1: DEMOGRAFI
    # ════════════════════════════════════════
    with tab1:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        row1_l, row1_r = st.columns(2, gap="medium")

        with row1_l:
            section("Distribusi Usia")
            fig_age = px.histogram(df, x="Age", nbins=25, color_discrete_sequence=[C["lav"]])
            fig_age.update_traces(marker_line_width=0, opacity=.8)
            fig_age.update_layout(**base_layout(height=280, showlegend=False, yaxis_title="Frekuensi"))
            st.plotly_chart(fig_age, use_container_width=True)

        with row1_r:
            bq("1")
            section("Proporsi Tingkat Stres")
            fig_stress_pie = go.Figure(go.Pie(
                labels=["Low", "Moderate", "High"],
                values=[(df["Stress Level"]==v).sum() for v in ["Low","Moderate","High"]],
                hole=0.55,
                marker=dict(colors=[C["sage"],C["amber"],C["rose"]], line=dict(color=C["bg"],width=2)),
                textinfo="label+percent",
                textfont=dict(size=11, color="#1E3A2A"),
            ))
            fig_stress_pie.update_layout(**base_layout(height=280))
            st.plotly_chart(fig_stress_pie, use_container_width=True)

        row2_l, row2_r = st.columns(2, gap="medium")

        with row2_l:
            section("Distribusi Gender")
            gc = df["Gender"].value_counts().reset_index()
            gc.columns = ["Gender", "Jumlah"]
            fig_gender = go.Figure(go.Bar(
                x=gc["Gender"], y=gc["Jumlah"],
                marker=dict(color=[C["lav"],C["rose"],C["sky"]], line=dict(width=0)),
                text=gc["Jumlah"], textposition="outside", textfont=dict(color="#3A6A4A",size=10),
            ))
            fig_gender.update_layout(**base_layout(height=260, showlegend=False, yaxis_title="Jumlah"))
            st.plotly_chart(fig_gender, use_container_width=True)

        with row2_r:
            section("Responden per Negara")
            cc = df["Country"].value_counts().reset_index()
            cc.columns = ["Negara","Jumlah"]
            fig_cnt = px.bar(cc, x="Negara", y="Jumlah", color="Jumlah",
                             color_continuous_scale=[C["rose"],C["lav"],C["sky"]])
            fig_cnt.update_traces(marker_line_width=0)
            fig_cnt.update_layout(**base_layout(height=260, showlegend=False, yaxis_title="Jumlah",
                                               coloraxis_showscale=False))
            st.plotly_chart(fig_cnt, use_container_width=True)

        # ── Kesimpulan Tab 1 ─────────────────────────────────────────────────
        st.divider()
        section("📌 Kesimpulan — Demografi & Target")
        pct_high = (df["Stress Level"] == "High").mean() * 100
        pct_mod  = (df["Stress Level"] == "Moderate").mean() * 100
        top_cond_tab1 = df["Mental Health Condition"].value_counts().idxmax()
        top_cnt_tab1  = df["Country"].value_counts().idxmax()
        st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-radius:12px; padding:1rem 1.2rem">
  <ul style="font-size:.86rem; color:#2E5A3A; line-height:2; margin:0; padding-left:1.2rem">
    <li>Distribusi usia cukup merata, menandakan masalah kesehatan mental <b style="color:#1E5C35">relevan di semua kelompok umur</b>.</li>
    <li>Sebanyak <b style="color:#C0534A">{pct_high:.1f}%</b> responden berada di level stres <b>High</b> dan <b style="color:#C87F2A">{pct_mod:.1f}%</b> di level <b>Moderate</b> — lebih dari separuh populasi mengalami tekanan mental signifikan.</li>
    <li>Kondisi mental yang paling banyak dilaporkan adalah <b style="color:#3A8C5C">{top_cond_tab1}</b>. Intervensi berbasis kondisi ini perlu diprioritaskan.</li>
    <li>Responden dari <b style="color:#2E86AB">{top_cnt_tab1}</b> mendominasi dataset. Interpretasi hasil perlu mempertimbangkan konteks budaya dan demografis negara tersebut.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # TAB 2: GAYA HIDUP
    # ════════════════════════════════════════
    with tab2:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        row1_l, row1_r = st.columns(2, gap="medium")

        with row1_l:
            bq("2")
            section("Jam Tidur vs Tingkat Stres")
            fig_sleep_box = px.box(
                df, x="Stress Level", y="Sleep Hours",
                color="Stress Level", color_discrete_map=STRESS_COLORS,
                category_orders={"Stress Level": ["Low","Moderate","High"]},
                points=False,
            )
            fig_sleep_box.update_traces(line_width=1.5)
            fig_sleep_box.update_layout(**base_layout(height=290, showlegend=False))
            st.plotly_chart(fig_sleep_box, use_container_width=True)

        with row1_r:
            bq("4")
            section("Screen Time vs Happiness Score")
            fig_scatter_sc = px.scatter(
                df, x="Screen Time per Day (Hours)", y="Happiness Score",
                color="Stress Level", color_discrete_map=STRESS_COLORS, opacity=.45,
            )
            fig_scatter_sc.update_traces(marker=dict(size=4, line=dict(width=0)))
            fig_scatter_sc.update_layout(**base_layout(height=290))
            st.plotly_chart(fig_scatter_sc, use_container_width=True)

        row2_l, row2_r = st.columns(2, gap="medium")

        with row2_l:
            bq("3 & 5")
            section("Level Olahraga per Kondisi Mental")
            ex_df = df.groupby(["Mental Health Condition","Exercise Level"]).size().reset_index(name="Count")
            fig_ex = px.bar(ex_df, x="Mental Health Condition", y="Count",
                            color="Exercise Level", color_discrete_map=EXERCISE_COLORS, barmode="group")
            fig_ex.update_traces(marker_line_width=0)
            fig_ex.update_layout(**base_layout(height=280, yaxis_title="Jumlah"))
            st.plotly_chart(fig_ex, use_container_width=True)

        with row2_r:
            section("Jam Kerja vs Happiness")
            fig_work = px.scatter(
                df, x="Work Hours per Week", y="Happiness Score",
                color="Mental Health Condition", color_discrete_map=CONDITION_COLORS, opacity=.45,
            )
            fig_work.update_traces(marker=dict(size=4, line=dict(width=0)))
            fig_work.update_layout(**base_layout(height=280))
            st.plotly_chart(fig_work, use_container_width=True)

        st.divider()
        bq("6")
        section("Diet vs Stres & Happiness")

        diet_l, diet_r = st.columns(2, gap="medium")

        with diet_l:
            diet_df = df.groupby(["Diet Type","Stress Level"]).size().reset_index(name="Count")
            fig_diet = px.bar(
                diet_df, x="Diet Type", y="Count", color="Stress Level",
                color_discrete_map=STRESS_COLORS, barmode="group",
                category_orders={"Stress Level":["Low","Moderate","High"]},
            )
            fig_diet.update_traces(marker_line_width=0)
            fig_diet.update_layout(**base_layout(height=270, yaxis_title="Jumlah"))
            st.plotly_chart(fig_diet, use_container_width=True)

        with diet_r:
            fig_diet_box = px.box(
                df, x="Diet Type", y="Happiness Score",
                color="Diet Type", color_discrete_sequence=PALETTE, points=False,
            )
            fig_diet_box.update_traces(line_width=1.5)
            fig_diet_box.update_layout(**base_layout(height=270, showlegend=False,
                                                      xaxis_title="Jenis Diet",
                                                      yaxis_title="Happiness Score"))
            st.plotly_chart(fig_diet_box, use_container_width=True)

        # ── Kesimpulan Tab 2 ─────────────────────────────────────────────────
        st.divider()
        section("📌 Kesimpulan — Gaya Hidup")
        sleep_low2  = df[df["Stress Level"]=="Low"]["Sleep Hours"].mean()
        sleep_high2 = df[df["Stress Level"]=="High"]["Sleep Hours"].mean()
        hap_high_ex = df[df["Exercise Level"]=="High"]["Happiness Score"].mean()
        hap_low_ex  = df[df["Exercise Level"]=="Low"]["Happiness Score"].mean()
        best_diet   = df.groupby("Diet Type")["Happiness Score"].mean().idxmax()
        worst_diet  = df.groupby("Diet Type")["Happiness Score"].mean().idxmin()
        corr_screen_hap = df["Screen Time per Day (Hours)"].corr(df["Happiness Score"])
        st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-radius:12px; padding:1rem 1.2rem">
  <ul style="font-size:.86rem; color:#2E5A3A; line-height:2; margin:0; padding-left:1.2rem">
    <li><b style="color:#2E86AB">Durasi tidur berkorelasi negatif dengan stres</b>: responden stres rendah tidur rata-rata {sleep_low2:.1f} jam vs hanya {sleep_high2:.1f} jam pada stres tinggi. Target ideal adalah 7–8 jam per malam.</li>
    <li>Level olahraga <b style="color:#4CAF7D">High</b> menghasilkan rata-rata happiness {hap_high_ex:.2f}, signifikan lebih tinggi dari level <b style="color:#C0534A">Low</b> ({hap_low_ex:.2f}). Aktivitas fisik terbukti meningkatkan kesejahteraan mental.</li>
    <li>Screen time memiliki korelasi <b style="color:#C87F2A">{corr_screen_hap:+.3f}</b> terhadap happiness — penggunaan layar berlebih cenderung menurunkan skor kebahagiaan.</li>
    <li>Diet <b style="color:#3A8C5C">{best_diet}</b> dikaitkan dengan skor kebahagiaan tertinggi, sementara <b style="color:#C0534A">{worst_diet}</b> menunjukkan nilai terendah. Pola makan sehat berperan nyata dalam kesehatan mental.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # TAB 3: KONDISI MENTAL
    # ════════════════════════════════════════
    with tab3:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        row1_l, row1_r = st.columns(2, gap="medium")

        with row1_l:
            bq("1")
            section("Distribusi Kondisi Mental")
            cond_df = df["Mental Health Condition"].value_counts().reset_index()
            cond_df.columns = ["Kondisi","Jumlah"]
            fig_cond_pie = go.Figure(go.Pie(
                labels=cond_df["Kondisi"], values=cond_df["Jumlah"], hole=0.58,
                marker=dict(colors=[CONDITION_COLORS.get(c,"#aaa") for c in cond_df["Kondisi"]],
                            line=dict(color=C["bg"],width=2)),
                textinfo="label+percent", textfont=dict(size=11, color="#1E3A2A"),
            ))
            fig_cond_pie.update_layout(**base_layout(height=300))
            st.plotly_chart(fig_cond_pie, use_container_width=True)

        with row1_r:
            section("Happiness Score per Kondisi")
            fig_hap_box = px.box(
                df, x="Mental Health Condition", y="Happiness Score",
                color="Mental Health Condition", color_discrete_map=CONDITION_COLORS, points=False,
            )
            fig_hap_box.update_traces(line_width=1.5)
            fig_hap_box.update_layout(**base_layout(height=300, showlegend=False))
            st.plotly_chart(fig_hap_box, use_container_width=True)

        row2_l, row2_r = st.columns(2, gap="medium")

        with row2_l:
            section("Rata-rata Jam Tidur per Kondisi")
            sleep_cond = df.groupby("Mental Health Condition")["Sleep Hours"].mean().reset_index()
            fig_sleep_cond = go.Figure(go.Bar(
                x=sleep_cond["Mental Health Condition"], y=sleep_cond["Sleep Hours"],
                marker=dict(color=[CONDITION_COLORS.get(c,"#aaa") for c in sleep_cond["Mental Health Condition"]],
                            line=dict(width=0)),
                text=[f"{v:.2f}h" for v in sleep_cond["Sleep Hours"]],
                textposition="outside", textfont=dict(color="#3A6A4A",size=10),
            ))
            fig_sleep_cond.update_layout(**base_layout(height=280, showlegend=False,
                                                       yaxis_title="Rata-rata Jam Tidur"))
            st.plotly_chart(fig_sleep_cond, use_container_width=True)

        with row2_r:
            section("Screen Time per Kondisi (Violin)")
            fig_violin = px.violin(
                df, x="Mental Health Condition", y="Screen Time per Day (Hours)",
                color="Mental Health Condition", color_discrete_map=CONDITION_COLORS,
                box=True, points=False,
            )
            fig_violin.update_layout(**base_layout(height=280, showlegend=False))
            st.plotly_chart(fig_violin, use_container_width=True)

        st.divider()
        section("Distribusi Stres per Kondisi  ·  Stacked %")
        stress_cond = df.groupby(["Mental Health Condition","Stress Level"]).size().unstack(fill_value=0)
        stress_pct  = stress_cond.div(stress_cond.sum(axis=1),axis=0)*100
        fig_stacked = go.Figure()
        for lvl, clr in STRESS_COLORS.items():
            if lvl in stress_pct.columns:
                fig_stacked.add_trace(go.Bar(
                    name=lvl, x=stress_pct.index, y=stress_pct[lvl],
                    marker=dict(color=clr, line=dict(width=0)),
                    hovertemplate=f"<b>%{{x}}</b><br>{lvl}: %{{y:.1f}}%<extra></extra>",
                ))
        fig_stacked.update_layout(**base_layout(barmode="stack", height=270, yaxis_title="Persentase (%)"))
        st.plotly_chart(fig_stacked, use_container_width=True)

        st.divider()
        section("Ringkasan Statistik per Kondisi")
        summary = (
            df.groupby("Mental Health Condition")
            .agg(
                Jumlah=("Happiness Score","count"),
                Avg_Happiness=("Happiness Score","mean"),
                Avg_Tidur=("Sleep Hours","mean"),
                Avg_Screen=("Screen Time per Day (Hours)","mean"),
                Avg_Social=("Social Interaction Score","mean"),
            )
            .round(2).reset_index()
        )
        summary.columns = ["Kondisi","Jumlah","Avg Happiness","Avg Tidur (jam)","Avg Screen (jam)","Avg Social"]
        st.dataframe(
            summary, use_container_width=True, hide_index=True,
            column_config={
                "Avg Happiness":    st.column_config.ProgressColumn("Avg Happiness",    min_value=0, max_value=10, format="%.2f"),
                "Avg Tidur (jam)":  st.column_config.ProgressColumn("Avg Tidur (jam)",  min_value=0, max_value=12, format="%.2f"),
                "Avg Screen (jam)": st.column_config.ProgressColumn("Avg Screen (jam)", min_value=0, max_value=12, format="%.2f"),
                "Avg Social":       st.column_config.ProgressColumn("Avg Social",       min_value=0, max_value=10, format="%.2f"),
            },
        )

        # ── Kesimpulan Tab 3 ─────────────────────────────────────────────────
        st.divider()
        section("📌 Kesimpulan — Kondisi Mental")
        hap_by_cond   = df.groupby("Mental Health Condition")["Happiness Score"].mean()
        best_cond_hap = hap_by_cond.idxmax()
        worst_cond_hap= hap_by_cond.idxmin()
        sleep_by_cond = df.groupby("Mental Health Condition")["Sleep Hours"].mean()
        best_sleep_c  = sleep_by_cond.idxmax()
        pct_cond_high_stress = df.groupby("Mental Health Condition").apply(
            lambda x: (x["Stress Level"]=="High").mean()*100
        ).idxmax()
        st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-radius:12px; padding:1rem 1.2rem">
  <ul style="font-size:.86rem; color:#2E5A3A; line-height:2; margin:0; padding-left:1.2rem">
    <li>Kondisi <b style="color:#3A8C5C">{best_cond_hap}</b> menunjukkan rata-rata happiness score tertinggi, sedangkan <b style="color:#C0534A">{worst_cond_hap}</b> memiliki skor terendah — mengindikasikan perbedaan dampak antar kondisi mental.</li>
    <li>Responden dengan kondisi <b style="color:#2E86AB">{best_sleep_c}</b> rata-rata tidur lebih lama, yang dapat mencerminkan pola gejala atau mekanisme coping yang berbeda.</li>
    <li>Kondisi <b style="color:#C0534A">{pct_cond_high_stress}</b> memiliki proporsi stres tinggi terbesar, menunjukkan beban psikologis yang lebih berat pada kelompok ini.</li>
    <li>Semua kondisi mental menunjukkan distribusi screen time yang serupa, mengisyaratkan bahwa <b style="color:#C87F2A">penggunaan layar merupakan faktor risiko universal</b>, tidak spesifik pada satu kondisi saja.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # ════════════════════════════════════════
    # TAB 4: KORELASI
    # ════════════════════════════════════════
    with tab4:
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        num_cols = ["Age","Sleep Hours","Work Hours per Week",
                    "Screen Time per Day (Hours)","Social Interaction Score","Happiness Score"]
        corr = df[num_cols].corr()

        row1_l, row1_r = st.columns([1.25, 1], gap="medium")

        with row1_l:
            bq("4")
            section("Heatmap Korelasi")
            fig_heat = go.Figure(go.Heatmap(
                z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
                colorscale=[[0,C["rose"]],[.25,"#3D2E5E"],[.5,C["card2"]],[.75,"#1E4060"],[1,C["sage"]]],
                zmin=-1, zmax=1,
                text=np.round(corr.values,2), texttemplate="%{text}",
                textfont=dict(size=9, color="#1E3A2A"),
                hovertemplate="<b>%{y} × %{x}</b><br>r = %{z:.3f}<extra></extra>",
            ))
            fig_heat.update_layout(**base_layout(height=380))
            st.plotly_chart(fig_heat, use_container_width=True)

        with row1_r:
            section("Social Score vs Happiness")
            fig_soc = px.scatter(
                df, x="Social Interaction Score", y="Happiness Score",
                color="Mental Health Condition", color_discrete_map=CONDITION_COLORS, opacity=.45,
            )
            fig_soc.update_traces(marker=dict(size=4, line=dict(width=0)))
            fig_soc.update_layout(**base_layout(height=380))
            st.plotly_chart(fig_soc, use_container_width=True)

        st.divider()
        section("Korelasi Variabel terhadap Happiness Score")
        corr_hap = (
            df[num_cols].corr()["Happiness Score"]
            .drop("Happiness Score")
            .sort_values(key=abs, ascending=False)
            .reset_index()
        )
        corr_hap.columns = ["Variabel","Korelasi"]
        st.dataframe(
            corr_hap, use_container_width=True, hide_index=True,
            column_config={
                "Korelasi": st.column_config.ProgressColumn(
                    "Korelasi dengan Happiness Score", min_value=-1, max_value=1, format="%.3f",
                )
            },
        )

        # ── Kesimpulan Tab 4 ─────────────────────────────────────────────────
        st.divider()
        section("📌 Kesimpulan — Korelasi")
        top_pos = corr_hap[corr_hap["Korelasi"] > 0].nlargest(1, "Korelasi")
        top_neg = corr_hap[corr_hap["Korelasi"] < 0].nsmallest(1, "Korelasi")
        top_pos_var = top_pos["Variabel"].values[0] if len(top_pos) else "-"
        top_pos_val = top_pos["Korelasi"].values[0] if len(top_pos) else 0
        top_neg_var = top_neg["Variabel"].values[0] if len(top_neg) else "-"
        top_neg_val = top_neg["Korelasi"].values[0] if len(top_neg) else 0
        st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-radius:12px; padding:1rem 1.2rem">
  <ul style="font-size:.86rem; color:#2E5A3A; line-height:2; margin:0; padding-left:1.2rem">
    <li><b style="color:#4CAF7D">{top_pos_var}</b> memiliki korelasi positif terkuat terhadap Happiness Score (r = {top_pos_val:+.3f}), menjadikannya <b>prediktor kebahagiaan paling signifikan</b> dalam dataset ini.</li>
    <li><b style="color:#C0534A">{top_neg_var}</b> memiliki korelasi negatif terkuat (r = {top_neg_val:+.3f}), mengindikasikan variabel ini paling berdampak menurunkan skor kebahagiaan.</li>
    <li>Heatmap korelasi menunjukkan sebagian besar variabel numerik <b style="color:#1E5C35">saling terkait dengan pola yang konsisten</b>, mendukung pendekatan analisis holistik gaya hidup.</li>
    <li>Korelasi moderat (bukan kuat) pada seluruh variabel mengingatkan bahwa kesehatan mental bersifat multifaktorial — tidak ada satu faktor tunggal yang menentukan sepenuhnya.</li>
  </ul>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3 — SIMULASI PREDIKSI
# ══════════════════════════════════════════════════════════════════════════════
elif pilihan == "Simulasi Prediksi":

    st.markdown("<h1 style='text-align:center; font-weight:800; font-size:2.2rem; color:#14321F'>Simulasi Prediksi Stres</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5A8A6A; font-size:.95rem'>Masukkan data gaya hidup untuk mendapatkan estimasi tingkat stres dan skor kebahagiaan</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    col_form, col_spacer, col_result = st.columns([1, .04, 1], gap="small")

    with col_form:
        section("Input Data Diri")
        st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

        with st.form("form_prediksi", border=False):
            c1, c2 = st.columns(2, gap="small")
            with c1:
                age    = st.number_input("Usia", 15, 80, 25)
                sleep  = st.slider("Jam Tidur / Malam", 0.0, 12.0, 7.0, 0.5)
                diet   = st.selectbox("Tipe Diet", ["Balanced","Vegan","Vegetarian","Keto","Junk Food"])
                gender = st.selectbox("Gender", ["Male","Female","Other"])
            with c2:
                screen   = st.slider("Screen Time (jam/hari)", 0.0, 16.0, 5.0, 0.5)
                work     = st.number_input("Jam Kerja / Minggu", 0, 100, 40)
                exercise = st.selectbox("Level Olahraga", ["Low","Moderate","High"])
                social   = st.slider("Skor Interaksi Sosial", 0.0, 10.0, 5.0, 0.5)

            st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Analisis Gaya Hidup", use_container_width=True)

    with col_result:
        section("Hasil Estimasi")
        st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

        if submitted:
            # ── Heuristik ───────────────────────────────────────────────────
            skor = 0
            if sleep < 5:            skor += 3
            elif sleep < 6.5:        skor += 1
            if screen > 8:           skor += 3
            elif screen > 5:         skor += 1
            if work > 55:            skor += 3
            elif work > 45:          skor += 1
            if exercise == "Low":    skor += 2
            elif exercise == "High": skor -= 1
            if diet == "Junk Food":  skor += 1
            if social < 3:           skor += 2
            elif social > 7:         skor -= 1

            if skor <= 2:
                level, icon = "Low",      "🟢"
                desc  = "Gaya hidupmu mendukung kesehatan mental yang baik."
            elif skor <= 5:
                level, icon = "Moderate", "🟡"
                desc  = "Ada beberapa faktor yang perlu diperhatikan."
            else:
                level, icon = "High",     "🔴"
                desc  = "Beberapa kebiasaan perlu diperbaiki segera."

            est_hap = round(min(10, max(1,
                5.5
                + (sleep  - 6) * 0.3
                - (screen - 5) * 0.15
                + (social - 5) * 0.2
                - (work   - 40)* 0.02
                + (1 if exercise=="High" else -0.5 if exercise=="Low" else 0)
            )), 2)

            m1, m2 = st.columns(2, gap="small")
            m1.metric(f"{icon} Estimasi Stres",    level)
            m2.metric("Happiness Score",            f"{est_hap} / 10")

            st.markdown("<div style='height:.2rem'></div>", unsafe_allow_html=True)

            if level == "Low":      st.success(f"✅ {desc}")
            elif level == "Moderate": st.warning(f"⚠️ {desc}")
            else:                   st.error(f"❗ {desc}")

            st.divider()
            section("Rekomendasi Personal")
            recs = []
            if sleep < 6.5:           recs.append("💤  Tingkatkan jam tidur minimal 7–8 jam per malam")
            if screen > 6:            recs.append("📱  Kurangi screen time — istirahatkan mata tiap 1 jam")
            if work > 50:             recs.append("💼  Pertimbangkan keseimbangan kerja-hidup yang lebih baik")
            if exercise == "Low":     recs.append("🏃  Mulai olahraga ringan 30 menit 3× seminggu")
            if diet == "Junk Food":   recs.append("🥗  Perbaiki pola makan ke diet yang lebih seimbang")
            if social < 4:            recs.append("🤝  Perbanyak interaksi sosial yang positif")

            if not recs:
                st.success("🎉 Semua aspek gaya hidupmu sudah baik! Pertahankan!")
            else:
                for r in recs:
                    st.markdown(
                        f"<p style='font-size:.86rem; color:#2E5A3A; margin:.3rem 0'>{r}</p>",
                        unsafe_allow_html=True
                    )

            st.divider()
            section("Profil Gaya Hidup")
            cats   = ["Tidur", "Screen\nControl", "Aktivitas", "Sosial", "Work-Life\nBalance"]
            vals   = [
                min(10, sleep/8*10),
                min(10, max(0, (12-screen)/12*10)),
                {"Low":3,"Moderate":6.5,"High":10}[exercise],
                social,
                min(10, max(0, (80-work)/80*10)),
            ]
            vc = vals + [vals[0]]
            cc2 = cats + [cats[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=vc, theta=cc2, fill="toself",
                fillcolor="rgba(58,140,92,.2)",
                line=dict(color=C["lav"],width=2), name="Kamu",
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[7]*6, theta=cc2,
                line=dict(color=C["sage"],width=1.2,dash="dash"),
                name="Ideal",
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(214,239,224,.8)",
                    radialaxis=dict(visible=True, range=[0,10],
                                   gridcolor=C["border"],
                                   tickfont=dict(color=C["muted"],size=8)),
                    angularaxis=dict(gridcolor=C["border"],
                                     tickfont=dict(color="#1E3A2A",size=10)),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#1E3A2A"),
                legend=dict(bgcolor="rgba(228,245,235,.95)", bordercolor=C["border"],
                            borderwidth=1, font=dict(size=10)),
                height=310, margin=dict(l=36,r=36,t=36,b=36),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            # ── Kesimpulan Simulasi ───────────────────────────────────────────
            st.divider()
            section("📋 Kesimpulan Analisis")

            # Identifikasi area kuat dan lemah
            area_kuat  = [cats[i].replace("\n"," ") for i, v in enumerate(vals) if v >= 7]
            area_lemah = [cats[i].replace("\n"," ") for i, v in enumerate(vals) if v < 5]
            overall    = sum(vals) / len(vals)

            if overall >= 7:
                ov_label, ov_color = "Baik", "#4CAF7D"
                ov_msg = "Secara keseluruhan, gaya hidupmu sudah mendukung kesehatan mental yang optimal."
            elif overall >= 5:
                ov_label, ov_color = "Cukup", "#C87F2A"
                ov_msg = "Ada beberapa aspek yang sudah baik, namun masih ada ruang untuk perbaikan."
            else:
                ov_label, ov_color = "Perlu Perhatian", "#C0534A"
                ov_msg = "Beberapa aspek gaya hidup perlu segera diperbaiki untuk menjaga kesehatan mental."

            kuat_str  = ", ".join(area_kuat)  if area_kuat  else "—"
            lemah_str = ", ".join(area_lemah) if area_lemah else "—"

            st.markdown(f"""
<div style="background:#D6EFE0; border:1px solid #B7DEC5; border-left:3px solid {ov_color}; border-radius:12px; padding:1rem 1.2rem">
  <div style="font-size:.8rem; font-weight:600; color:{ov_color}; text-transform:uppercase; letter-spacing:.06em; margin-bottom:.5rem">
    Status Keseluruhan: {ov_label}
  </div>
  <p style="font-size:.86rem; color:#2E5A3A; margin-bottom:.75rem">{ov_msg}</p>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:.75rem; font-size:.83rem">
    <div style="background:#E4F5EB; border-radius:8px; padding:.65rem .85rem">
      <div style="color:#4CAF7D; font-weight:600; margin-bottom:.3rem">✅ Area Kuat</div>
      <div style="color:#2E5A3A">{kuat_str}</div>
    </div>
    <div style="background:#E4F5EB; border-radius:8px; padding:.65rem .85rem">
      <div style="color:#C0534A; font-weight:600; margin-bottom:.3rem">⚠️ Perlu Ditingkatkan</div>
      <div style="color:#2E5A3A">{lemah_str}</div>
    </div>
  </div>
  <p style="font-size:.78rem; color:#5A8A6A; margin-top:.75rem; margin-bottom:0">
    💡 Estimasi ini bersifat indikatif berdasarkan pola data 3.000 responden. Konsultasikan dengan profesional kesehatan untuk evaluasi lebih lanjut.
  </p>
</div>
""", unsafe_allow_html=True)

        else:
            st.markdown("""
<div style="
    background:#D6EFE0; border:1px solid #B7DEC5; border-radius:12px;
    padding:2.5rem 2rem; text-align:center; color:#5A8A6A; font-size:.88rem; margin-top:.5rem
">
    👈 Isi form di sebelah kiri, lalu klik <b style='color:#3A8C5C'>Analisis Gaya Hidup</b>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='font-size:.72rem; color:#4A7A5A; text-align:center'>"
    "MindBalance Dashboard &nbsp;·&nbsp; Tema : Healthy Lives & Well-being &nbsp;·&nbsp; CC26 - PSU281"
    "</p>",
    unsafe_allow_html=True
)