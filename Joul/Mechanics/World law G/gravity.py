import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Бет тақырыбы
st.title("🌌 Гравитация және Бүкіл әлемдік тартылыс заңы")
st.markdown("""
Бұл бөлімде денелердің өзара тартылыс күшін және ауырлық күшін зерттейміз.
Формулалар: $F = G \\frac{m_1 m_2}{r^2}$ және $F = mg$
""")

# 2. Параметрлерді енгізу (Sidebar)
st.sidebar.header("Физикалық параметрлер")

# Бүкіл әлемдік тартылыс үшін
m1 = st.sidebar.number_input("1-дененің массасы (m1), кг:", min_value=1.0, value=1e6, format="%.1e")
m2 = st.sidebar.number_input("2-дененің массасы (m2), кг:", min_value=1.0, value=1e6, format="%.1e")
r_current = st.sidebar.number_input("Арақашықтық (r), м:", min_value=0.1, value=10.0, step=0.5)

# Ауырлық күші үшін
m_body = st.sidebar.number_input("Дене массасы (m), кг:", min_value=0.1, value=70.0, step=1.0)
g_val = st.sidebar.slider("Еркін түсу үдеуі (g), м/с²:", 0.0, 30.0, 9.8)

# Тұрақтылар
G = 6.674e-11

# 3. Есептеулер
F_grav = G * (m1 * m2) / (r_current**2)
F_weight = m_body * g_val

# Графиктер үшін деректер
r_range = np.linspace(1, 100, 200)
F_of_r = G * (m1 * m2) / (r_range**2)

m_range = np.linspace(1, 1e7, 100)
F_of_m = G * (m_range * m2) / (r_current**2)

g_range = np.linspace(0, 30, 100)
F_of_g = m_body * g_range

# 4. Графиктерді шығару
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "F пен r тәуелділігі (Кері квадраттық)", 
        "F пен m1 тәуелділігі (Тура пропорционал)",
        "F пен g тәуелділігі (Ауырлық күші)",
        "Тартылыс күшінің масштабы"
    )
)

# F(r) - Гипербола
fig.add_trace(go.Scatter(x=r_range, y=F_of_r, name="F(r)", line=dict(color='red')), row=1, col=1)
fig.add_trace(go.Scatter(x=[r_current], y=[F_grav], mode="markers", marker=dict(size=10, color="black")), row=1, col=1)

# F(m) - Түзу
fig.add_trace(go.Scatter(x=m_range, y=F_of_m, name="F(m1)", line=dict(color='blue')), row=1, col=2)
fig.add_trace(go.Scatter(x=[m1], y=[F_grav], mode="markers", marker=dict(size=10, color="black")), row=1, col=2)

# F(g) - Түзу (Ауырлық күші)
fig.add_trace(go.Scatter(x=g_range, y=F_of_g, name="F(g)", line=dict(color='green')), row=2, col=1)
fig.add_trace(go.Scatter(x=[g_val], y=[F_weight], mode="markers", marker=dict(size=10, color="black")), row=2, col=1)

fig.update_layout(height=800, showlegend=False, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# 5. АНИМАЦИЯ (Екі дененің тартылысы)
st.divider()
st.subheader("🎬 Денелердің өзара тартылыс визуализациясы")

# Денелердің өлшемі массасына байланысты
size1 = np.log10(m1) * 5
size2 = np.log10(m2) * 5

fig_anim = go.Figure()
fig_anim.add_trace(go.Scatter(
    x=[-r_current/2, r_current/2], y=[0, 0],
    mode="markers+text",
    marker=dict(size=[size1, size2], color=["blue", "orange"]),
    text=[f"m1: {m1:.1e} кг", f"m2: {m2:.1e} кг"],
    textposition="top center"
))

# Күш векторын көрсету (көрсеткіштер)
fig_anim.add_annotation(x=-r_current/2 + 1, y=0, ax=-r_current/2, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor="red")
fig_anim.add_annotation(x=r_current/2 - 1, y=0, ax=r_current/2, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=2, arrowcolor="red")

fig_anim.update_layout(xaxis=dict(range=[-70, 70]), yaxis=dict(range=[-10, 10], visible=False), height=300)
st.plotly_chart(fig_anim, use_container_width=True)

# 6. Нәтижелер
res1, res2 = st.columns(2)
res1.metric("Тартылыс күші (F_grav)", f"{F_grav:.4f} Н")
res2.metric("Ауырлық күші (F_weight)", f"{F_weight:.2f} Н")