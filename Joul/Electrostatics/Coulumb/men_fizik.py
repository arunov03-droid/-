import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Беттің тақырыбы мен макеті
st.set_page_config(page_title="Кулон заңы визуализациясы", layout="wide")

st.title("⚡ Кулон заңы: Интерактивті веб-визуализация")
st.markdown("""
Бұл бағдарлама **Python** тілінде жазылған. Сол жақтағы параметрлерді өзгерту арқылы 
зарядтардың өзара әрекеттесуін бақылай аласыз.
""")

# 2. Бүйірлік панельдегі слайдерлер (Параметрлер)
st.sidebar.header("Физикалық шамалар")
q1 = st.sidebar.slider("1-заряд (q1), мкКл:", -10.0, 10.0, 5.0)
q2 = st.sidebar.slider("2-заряд (q2), мкКл:", -10.0, 10.0, 5.0)
r = st.sidebar.slider("Арақашықтық (r), метр:", 1.0, 20.0, 5.0)

# 3. Есептеу бөлімі
k = 8.99e9 # Кулон тұрақтысы
# Күшті есептеу: F = k * |q1 * q2| / r^2
force = k * (abs(q1)*1e-6 * abs(q2)*1e-6) / (r**2)

# 4. Экранды екі бағанға бөлу
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Зарядтардың кеңістіктегі орны")
    
    # Зарядтардың суретін салу (Plotly)
    fig_positions = go.Figure()
    
    # 1-заряд (көк немесе қызыл шар)
    fig_positions.add_trace(go.Scatter(
        x=[-r/2], y=[0],
        mode="markers+text",
        marker=dict(size=abs(q1)*5+15, color="red" if q1 > 0 else "blue", line=dict(width=2, color='black')),
        text=[f"q1 = {q1}μC"], textposition="top center",
        name="Заряд 1"
    ))
    
    # 2-заряд
    fig_positions.add_trace(go.Scatter(
        x=[r/2], y=[0],
        mode="markers+text",
        marker=dict(size=abs(q2)*5+15, color="red" if q2 > 0 else "blue", line=dict(width=2, color='black')),
        text=[f"q2 = {q2}μC"], textposition="top center",
        name="Заряд 2"
    ))
    
    # Центрлік сызық
    fig_positions.add_shape(type="line", x0=-r/2, y0=0, x1=r/2, y1=0, line=dict(color="Gray", dash="dash"))

    fig_positions.update_layout(
        xaxis=dict(range=[-15, 15], title="Қашықтық (м)"),
        yaxis=dict(range=[-5, 5], visible=False),
        height=400, showlegend=False, template="plotly_white"
    )
    st.plotly_chart(fig_positions, use_container_width=True)

with col2:
    st.subheader("📈 Күштің қашықтыққа тәуелділігі")
    
    # График үшін деректер дайындау
    r_range = np.linspace(1, 25, 100)
    f_range = k * (abs(q1)*1e-6 * abs(q2)*1e-6) / (r_range**2)
    
    fig_graph = go.Figure()
    fig_graph.add_trace(go.Scatter(x=r_range, y=f_range, name="F(r) қисығы", line=dict(color='green', width=3)))
    
    # Қазіргі нүктені белгілеу
    fig_graph.add_trace(go.Scatter(
        x=[r], y=[force], mode="markers",
        marker=dict(color="black", size=12, symbol="circle"),
        name="Қазіргі күй"
    ))
    
    fig_graph.update_layout(
        xaxis_title="r (метр)", yaxis_title="Күш F (Ньютон)",
        height=400, template="plotly_white"
    )
    st.plotly_chart(fig_graph, use_container_width=True)

# 5. Қорытынды нәтиже
st.info(f"💡 Есептелген өзара әрекеттесу күші: **{force:.4f} Ньютон**")