import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# KONFIGURASI
# ============================================================
st.set_page_config(
    page_title="Dashboard Statistik Mahasiswa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — DARK MODE
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a15 0%, #12121f 100%);
    }
    section[data-testid="stSidebar"] {
        background: rgba(30, 30, 55, 0.6);
        border-right: 1px solid rgba(150, 120, 255, 0.2);
    }
    div[data-testid="stMetric"] {
        background: rgba(30, 30, 55, 0.5);
        border: 1px solid rgba(150, 120, 255, 0.2);
        border-radius: 16px;
        padding: 16px;
        backdrop-filter: blur(20px);
        transition: all 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: rgba(167, 139, 250, 0.5);
        box-shadow: 0 0 30px rgba(167, 139, 250, 0.15);
    }
    div[data-testid="stMetric"] label {
        color: #8892b0 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    h1, h2, h3 { color: #e2e8f0 !important; }
    h1 {
        background: linear-gradient(135deg, #ffffff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    p, span, label, div { color: #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 30, 55, 0.4);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(150, 120, 255, 0.15);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #8892b0;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(34, 211, 238, 0.15)) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(167, 139, 250, 0.4);
    }
    div[data-baseweb="select"] > div {
        background: rgba(30, 30, 55, 0.6) !important;
        border-color: rgba(150, 120, 255, 0.3) !important;
        color: #e2e8f0 !important;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(30, 30, 55, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(150, 120, 255, 0.15);
    }
    hr { border-color: rgba(150, 120, 255, 0.15); }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.3);
        border-radius: 4px;
    }
    /* Alert boxes */
    .insight-box {
        background: rgba(139, 92, 246, 0.12);
        border-left: 4px solid #a78bfa;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .insight-box strong { color: #a78bfa; }
    .warning-box {
        background: rgba(251, 191, 36, 0.12);
        border-left: 4px solid #fbbf24;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .danger-box {
        background: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .success-box {
        background: rgba(52, 211, 153, 0.12);
        border-left: 4px solid #34d399;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    return pd.read_csv('latihan1.csv')

df = load_data()

numeric_cols = ['Age', 'Study_Hours', 'Sleep_Hours', 'Attendance',
                'Exam_Score', 'Monthly_Spending', 'Screen_Hours', 'Satisfaction']

# ============================================================
# HEADER
# ============================================================
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("📊 Dashboard Statistik Mahasiswa")
    st.caption("Analisis Statistik Deskriptif · Dataset latihan1.csv")
with col_head2:
    st.metric("Total Data", len(df), delta="100 mahasiswa", delta_color="off")

st.divider()

# ============================================================
# SIDEBAR — FILTER MULTI-KONDISI
# ============================================================
with st.sidebar:
    st.header("⚙️ Filter Data")

    # Filter Gender
    gender_filter = st.multiselect(
        "Gender",
        options=df['Gender'].unique().tolist(),
        default=df['Gender'].unique().tolist(),
        format_func=lambda x: "Perempuan (F)" if x == "F" else "Laki-laki (M)"
    )

    # Filter Usia
    age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.slider("Rentang Usia", age_min, age_max, (age_min, age_max))

    st.divider()
    st.markdown("### 🎯 Filter Lanjutan")

    # Filter Nilai
    score_range = st.slider(
        "Rentang Nilai Ujian",
        int(df['Exam_Score'].min()), int(df['Exam_Score'].max()),
        (int(df['Exam_Score'].min()), int(df['Exam_Score'].max()))
    )

    # Filter Kehadiran
    attendance_min = st.slider(
        "Kehadiran Minimal (%)",
        int(df['Attendance'].min()), int(df['Attendance'].max()),
        int(df['Attendance'].min())
    )

    st.divider()
    st.markdown("### 📌 Info")
    st.caption(f"**Dataset:** {len(df)} baris")
    st.caption(f"**Kolom:** {len(df.columns)} kolom")
    st.caption("© 2025 StatDashboard")

# Apply filter
df_filtered = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Age'].between(age_range[0], age_range[1])) &
    (df['Exam_Score'].between(score_range[0], score_range[1])) &
    (df['Attendance'] >= attendance_min)
]

if len(df_filtered) == 0:
    st.warning("⚠️ Tidak ada data yang sesuai filter. Ubah filter di sidebar.")
    st.stop()

st.info(f"🔍 **{len(df_filtered)}** dari **{len(df)}** data ditampilkan setelah filter.")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview", "📈 Distribusi", "🔗 Korelasi",
    "🏆 Ranking", "📋 Tabel Statistik", "🎓 Detail Mahasiswa"
])

# ============================================================
# TAB 1: OVERVIEW
# ============================================================
with tab1:
    st.subheader("📌 Ringkasan Statistik")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total", len(df_filtered))
    col2.metric("Avg Nilai", f"{df_filtered['Exam_Score'].mean():.1f}")
    col3.metric("Avg Belajar", f"{df_filtered['Study_Hours'].mean():.1f} jam")
    col4.metric("Avg Hadir", f"{df_filtered['Attendance'].mean():.1f}%")
    col5.metric("Avg Kepuasan", f"{df_filtered['Satisfaction'].mean():.1f}/10")
    col6.metric("Avg Spending", f"Rp {df_filtered['Monthly_Spending'].mean():,.0f}")

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Distribusi Gender")
        gender_counts = df_filtered['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Jumlah']
        gender_counts['Gender'] = gender_counts['Gender'].map(
            {'F': 'Perempuan (F)', 'M': 'Laki-laki (M)'}
        )
        fig_gender = px.pie(
            gender_counts, values='Jumlah', names='Gender',
            hole=0.65,
            color_discrete_sequence=['#f472b6', '#60a5fa']
        )
        fig_gender.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=20, b=20, l=20, r=20), height=320
        )
        fig_gender.update_traces(textfont_color='white', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)

    with col_b:
        st.markdown("#### Sebaran Nilai Ujian")
        fig_hist = px.histogram(
            df_filtered, x='Exam_Score', nbins=15,
            color_discrete_sequence=['#a78bfa']
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis_title="Exam Score", yaxis_title="Jumlah",
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20), height=320
        )
        fig_hist.update_xaxes(gridcolor='rgba(150,120,255,0.1)')
        fig_hist.update_yaxes(gridcolor='rgba(150,120,255,0.1)')
        st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    # Interactive Bar Chart
    st.markdown("#### Perbandingan Variabel Numerik (Interaktif)")

    col_ctrl1, col_ctrl2, _ = st.columns([1, 1, 2])
    with col_ctrl1:
        stat_choice = st.selectbox("Statistik", ["Mean", "Median", "Min", "Max", "Std"], index=0)
    with col_ctrl2:
        gender_choice = st.selectbox("Gender", ["Semua", "Perempuan (F)", "Laki-laki (M)"], index=0)

    stat_map = {"Mean": "mean", "Median": "median", "Min": "min", "Max": "max", "Std": "std"}
    stat_key = stat_map[stat_choice]

    if gender_choice == "Semua":
        data_source = df_filtered
        title_suffix = "Semua Gender"
    elif gender_choice == "Perempuan (F)":
        data_source = df_filtered[df_filtered['Gender'] == 'F']
        title_suffix = "Perempuan (F)"
    else:
        data_source = df_filtered[df_filtered['Gender'] == 'M']
        title_suffix = "Laki-laki (M)"

    values = [data_source[c].agg(stat_key) for c in numeric_cols]

    fig_bar = go.Figure(data=[
        go.Bar(
            x=[c.replace('_', ' ') for c in numeric_cols],
            y=values,
            marker=dict(
                color=['#818cf8', '#a78bfa', '#60a5fa', '#34d399',
                       '#fbbf24', '#f472b6', '#f87171', '#22d3ee'],
            ),
            text=[f"{v:,.0f}" if v > 100 else f"{v:.1f}" for v in values],
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=11)
        )
    ])
    fig_bar.update_layout(
        title=f"{stat_choice} per Variabel ({title_suffix})",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0', yaxis_type="log",
        yaxis_title=f"{stat_choice} (log scale)",
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40), height=420
    )
    fig_bar.update_xaxes(gridcolor='rgba(150,120,255,0.05)')
    fig_bar.update_yaxes(gridcolor='rgba(150,120,255,0.1)')
    st.plotly_chart(fig_bar, use_container_width=True)

    # ========== INSIGHT OTOMATIS ==========
    st.divider()
    st.markdown("### 💡 Insight Otomatis")

    corr_matrix = df_filtered[numeric_cols].corr()
    pair_corr = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    top_pairs = pair_corr.unstack().dropna().sort_values(key=abs, ascending=False).head(3)

    st.markdown(f"""
    <div class="insight-box">
        <strong>🔗 Korelasi Terkuat:</strong><br>
        1. <b>{top_pairs.index[0][0]}</b> ↔ <b>{top_pairs.index[0][1]}</b>: r = {top_pairs.values[0]:.3f}<br>
        2. <b>{top_pairs.index[1][0]}</b> ↔ <b>{top_pairs.index[1][1]}</b>: r = {top_pairs.values[1]:.3f}<br>
        3. <b>{top_pairs.index[2][0]}</b> ↔ <b>{top_pairs.index[2][1]}</b>: r = {top_pairs.values[2]:.3f}
    </div>
    """, unsafe_allow_html=True)

    # Deteksi mahasiswa berisiko
    at_risk = df_filtered[
        (df_filtered['Exam_Score'] < 65) |
        (df_filtered['Attendance'] < 80)
    ]
    if len(at_risk) > 0:
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ Mahasiswa Berisiko:</strong> {len(at_risk)} mahasiswa dengan nilai &lt; 65 ATAU kehadiran &lt; 80%.
            Cek tab <b>Detail Mahasiswa</b> untuk info lengkap.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# TAB 2: DISTRIBUSI
# ============================================================
with tab2:
    st.subheader("📈 Distribusi & Sebaran Data")

    # Bar charts
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Distribusi Kepuasan")
        sat_counts = df_filtered['Satisfaction'].value_counts().sort_index().reset_index()
        sat_counts.columns = ['Satisfaction', 'Jumlah']
        fig_sat = px.bar(
            sat_counts, x='Satisfaction', y='Jumlah',
            color_discrete_sequence=['#34d399'], text='Jumlah'
        )
        fig_sat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', showlegend=False,
            xaxis_title="Skor Kepuasan", yaxis_title="Jumlah",
            margin=dict(t=20, b=20, l=20, r=20), height=320
        )
        st.plotly_chart(fig_sat, use_container_width=True)

    with col_b:
        st.markdown("#### Distribusi Usia")
        age_counts = df_filtered['Age'].value_counts().sort_index().reset_index()
        age_counts.columns = ['Age', 'Jumlah']
        fig_age = px.bar(
            age_counts, x='Age', y='Jumlah',
            color_discrete_sequence=['#22d3ee'], text='Jumlah'
        )
        fig_age.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', showlegend=False,
            xaxis_title="Usia (tahun)", yaxis_title="Jumlah",
            margin=dict(t=20, b=20, l=20, r=20), height=320
        )
        st.plotly_chart(fig_age, use_container_width=True)

    st.divider()

    # ========== BOX PLOT (BARU) ==========
    st.markdown("#### 📦 Box Plot — Deteksi Outlier")
    box_cols = st.multiselect(
        "Pilih variabel untuk box plot:",
        numeric_cols,
        default=['Study_Hours', 'Sleep_Hours', 'Attendance', 'Exam_Score']
    )
    if box_cols:
        fig_box = go.Figure()
        for i, col in enumerate(box_cols):
            fig_box.add_trace(go.Box(
                y=df_filtered[col],
                name=col.replace('_', ' '),
                marker_color=['#818cf8', '#a78bfa', '#60a5fa', '#34d399',
                              '#fbbf24', '#f472b6', '#f87171', '#22d3ee'][i % 8],
                boxmean='sd'
            ))
        fig_box.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0', showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20), height=400
        )
        fig_box.update_yaxes(gridcolor='rgba(150,120,255,0.1)')
        st.plotly_chart(fig_box, use_container_width=True)

    st.divider()

    # ========== SCATTER INTERAKTIF ==========
    st.markdown("#### 🔍 Analisis Korelasi Variabel")
    st.caption("Pilih variabel untuk sumbu X dan Y — korelasi dihitung otomatis")

    col_x, col_y, col_c = st.columns(3)
    with col_x:
        x_col = st.selectbox("Sumbu X", numeric_cols, index=1)
    with col_y:
        y_col = st.selectbox("Sumbu Y", numeric_cols, index=4)
    with col_c:
        color_by = st.selectbox("Warna", ["Tidak ada", "Gender"], index=0)

    r = df_filtered[x_col].corr(df_filtered[y_col])

    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Koefisien Korelasi (r)", f"{r:.3f}")
    with col_info2:
        abs_r = abs(r)
        if abs_r >= 0.9: strength = "Sangat Kuat"
        elif abs_r >= 0.7: strength = "Kuat"
        elif abs_r >= 0.5: strength = "Sedang"
        elif abs_r >= 0.3: strength = "Lemah"
        else: strength = "Sangat Lemah"
        st.metric("Kekuatan", strength)
    with col_info3:
        direction = "↗ Positif" if r > 0.05 else "↘ Negatif" if r < -0.05 else "→ Tidak Ada"
        st.metric("Arah", direction)

    # Scatter manual dengan trendline numpy (TANPA statsmodels!)
    fig_scatter = go.Figure()

    if color_by == "Gender":
        for gender, color, label in [('F', '#f472b6', 'Perempuan (F)'), ('M', '#60a5fa', 'Laki-laki (M)')]:
            subset = df_filtered[df_filtered['Gender'] == gender]
            fig_scatter.add_trace(go.Scatter(
                x=subset[x_col], y=subset[y_col],
                mode='markers', name=label,
                marker=dict(size=10, color=color, opacity=0.75,
                            line=dict(width=1, color='rgba(255,255,255,0.3)'))
            ))
    else:
        fig_scatter.add_trace(go.Scatter(
            x=df_filtered[x_col], y=df_filtered[y_col],
            mode='markers', name='Mahasiswa',
            marker=dict(size=10, color='#a78bfa', opacity=0.75,
                        line=dict(width=1, color='rgba(255,255,255,0.3)'))
        ))

    # Trendline manual pakai numpy polyfit
    x_vals = df_filtered[x_col].values
    y_vals = df_filtered[y_col].values
    if len(x_vals) > 1:
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_line = slope * x_line + intercept
        fig_scatter.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode='lines', name='Trendline',
            line=dict(color='#fbbf24', width=2, dash='dash')
        ))

        # Tampilkan rumus
        st.markdown(f"""
        <div class="insight-box">
            <strong>📐 Persamaan Regresi:</strong> {y_col} = {slope:.3f} × {x_col} + {intercept:.3f}<br>
            <strong>Interpretasi:</strong> Setiap kenaikan 1 unit <b>{x_col}</b>,
            <b>{y_col}</b> berubah <b>{slope:+.3f}</b> unit.
        </div>
        """, unsafe_allow_html=True)

    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        xaxis_title=x_col.replace('_', ' '),
        yaxis_title=y_col.replace('_', ' '),
        margin=dict(t=20, b=40, l=40, r=20), height=500,
        legend=dict(orientation="h", y=-0.15),
        hovermode='closest'
    )
    fig_scatter.update_xaxes(gridcolor='rgba(150,120,255,0.08)')
    fig_scatter.update_yaxes(gridcolor='rgba(150,120,255,0.08)')
    st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================================
# TAB 3: KORELASI
# ============================================================
with tab3:
    st.subheader("🔗 Heatmap Korelasi")
    st.caption("Nilai korelasi Pearson antar variabel (-1 sampai +1)")

    corr = df_filtered[numeric_cols].corr().round(2)

    fig_corr = px.imshow(
        corr, text_auto=True, aspect="auto",
        color_continuous_scale=[
            [0.0, '#ef4444'],
            [0.5, '#1a1a2e'],
            [1.0, '#3b82f6']
        ],
        zmin=-1, zmax=1
    )
    fig_corr.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0', height=650,
        margin=dict(t=20, b=20, l=20, r=20)
    )
    fig_corr.update_xaxes(side="bottom", tickangle=-45)
    fig_corr.update_traces(textfont=dict(color='white', size=11))
    st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()

    # Tabel korelasi dengan Exam Score
    st.markdown("#### 📊 Korelasi Setiap Variabel dengan Exam Score")
    corr_with_score = df_filtered[numeric_cols].corr()['Exam_Score'].drop('Exam_Score').sort_values(key=abs, ascending=False)
    corr_df = corr_with_score.reset_index()
    corr_df.columns = ['Variabel', 'Korelasi dengan Exam Score']
    corr_df['Variabel'] = corr_df['Variabel'].str.replace('_', ' ')
    corr_df['Kekuatan'] = corr_df['Korelasi dengan Exam Score'].abs().apply(
        lambda x: 'Sangat Kuat' if x >= 0.9 else 'Kuat' if x >= 0.7 else 'Sedang' if x >= 0.5 else 'Lemah' if x >= 0.3 else 'Sangat Lemah'
    )
    st.dataframe(corr_df, use_container_width=True, hide_index=True)

# ============================================================
# TAB 4: RANKING
# ============================================================
with tab4:
    st.subheader("🏆 Ranking Mahasiswa")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🏆 Top 5 — Nilai Tertinggi")
        top5 = df_filtered.nlargest(5, 'Exam_Score')[
            ['Student_ID', 'Gender', 'Study_Hours', 'Attendance', 'Exam_Score', 'Satisfaction']
        ].reset_index(drop=True)
        top5.index = top5.index + 1
        st.dataframe(
            top5, use_container_width=True,
            column_config={
                "Student_ID": "ID",
                "Study_Hours": st.column_config.NumberColumn("Belajar", format="%.1f jam"),
                "Attendance": st.column_config.NumberColumn("Hadir", format="%d%%"),
                "Exam_Score": st.column_config.ProgressColumn("Nilai", min_value=0, max_value=100),
                "Satisfaction": st.column_config.NumberColumn("Kepuasan", format="%d/10")
            }
        )

    with col_b:
        st.markdown("#### ⚠️ Bottom 5 — Nilai Terendah")
        bottom5 = df_filtered.nsmallest(5, 'Exam_Score')[
            ['Student_ID', 'Gender', 'Study_Hours', 'Attendance', 'Exam_Score', 'Satisfaction']
        ].reset_index(drop=True)
        bottom5.index = bottom5.index + 1
        st.dataframe(
            bottom5, use_container_width=True,
            column_config={
                "Student_ID": "ID",
                "Study_Hours": st.column_config.NumberColumn("Belajar", format="%.1f jam"),
                "Attendance": st.column_config.NumberColumn("Hadir", format="%d%%"),
                "Exam_Score": st.column_config.ProgressColumn("Nilai", min_value=0, max_value=100),
                "Satisfaction": st.column_config.NumberColumn("Kepuasan", format="%d/10")
            }
        )

# ============================================================
# TAB 5: TABEL STATISTIK
# ============================================================
with tab5:
    st.subheader("📋 Tabel Statistik Deskriptif")

    stats_data = []
    for col in numeric_cols:
        s = df_filtered[col]
        stats_data.append({
            'Variabel': col.replace('_', ' '),
            'n': int(s.count()),
            'Mean': round(s.mean(), 2),
            'Median': round(s.median(), 2),
            'Mode': round(s.mode()[0], 2),
            'Std': round(s.std(), 2),
            'Var': round(s.var(), 2),
            'Min': round(s.min(), 2),
            'Q1': round(s.quantile(0.25), 2),
            'Q3': round(s.quantile(0.75), 2),
            'Max': round(s.max(), 2),
            'Range': round(s.max() - s.min(), 2),
            'IQR': round(s.quantile(0.75) - s.quantile(0.25), 2),
            'Skew': round(s.skew(), 2),
            'Kurtosis': round(s.kurtosis(), 2)
        })

    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    st.divider()

    # Download buttons
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = stats_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Statistik (CSV)",
            data=csv, file_name='statistik_deskriptif.csv', mime='text/csv'
        )
    with col_dl2:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Data Filter (CSV)",
            data=csv_data, file_name='data_filtered.csv', mime='text/csv'
        )

# ============================================================
# TAB 6: DETAIL MAHASISWA
# ============================================================
with tab6:
    st.subheader("🎓 Detail Mahasiswa")

    search_id = st.selectbox(
        "Pilih Mahasiswa (Student ID):",
        options=sorted(df_filtered['Student_ID'].unique().tolist()),
        format_func=lambda x: f"Mahasiswa #{x}"
    )

    student = df_filtered[df_filtered['Student_ID'] == search_id].iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h3 style="margin:0; color:#a78bfa;">Mahasiswa #{student['Student_ID']}</h3>
            <p style="margin:8px 0 0 0; color:#8892b0;">
                {('Perempuan' if student['Gender']=='F' else 'Laki-laki')} · {student['Age']} tahun
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Nilai Ujian", student['Exam_Score'])
        st.metric("Kepuasan", f"{student['Satisfaction']}/10")

    with col2:
        st.markdown("#### 📊 Profil Detail")

        detail_df = pd.DataFrame({
            'Aspek': ['Study Hours', 'Sleep Hours', 'Attendance',
                      'Monthly Spending', 'Screen Hours'],
            'Nilai': [
                f"{student['Study_Hours']} jam/minggu",
                f"{student['Sleep_Hours']} jam/hari",
                f"{student['Attendance']}%",
                f"Rp {student['Monthly_Spending']:,.0f}",
                f"{student['Screen_Hours']} jam/hari"
            ]
        })
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

        # Bandingkan dengan rata-rata
        st.markdown("#### 📈 Perbandingan dengan Rata-rata")
        compare_data = []
        for col in ['Study_Hours', 'Sleep_Hours', 'Attendance', 'Exam_Score']:
            avg = df_filtered[col].mean()
            diff = student[col] - avg
            compare_data.append({
                'Variabel': col.replace('_', ' '),
                'Mahasiswa': round(student[col], 2),
                'Rata-rata': round(avg, 2),
                'Selisih': f"{diff:+.2f}",
                'Status': '🟢 Di atas' if diff > 0 else '🔴 Di bawah'
            })
        st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("© 2025 Dashboard Statistik · Built with Streamlit 🎈")