import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Бет тақырыбы
st.title("🚀 Кинематика: Үдеудің қозғалысқа әсері")
st.markdown("""
Бұл бөлімде **үдеудің (a)** жүрілген жол мен соңғы жылдамдыққа әсерін зерттейміз.
Формулалар: $S = v_0 t + \\frac{at^2}{2}$ және $v = v_0 + at$
""")

# 2. Параметрлерді енгізу (Sidebar)
st.sidebar.header("Қозғалыс параметрлері")
v0 = st.sidebar.number_input("Бастапқы жылдамдық (v0), м/с:", value=0.0, step=1.0)
t = st.sidebar.number_input("Уақыт (t), с:", value=5.0, step=0.5)
a_current = st.sidebar.number_input("Үдеу (a), м/с²:", value=2.0, step=0.5)

# 3. Есептеулер мен Графиктер үшін деректер
a_range = np.linspace(0, 10, 100) # Үдеу 0-ден 10-ға дейін өзгереді
S_of_a = v0 * t + (a_range * t**2) / 2
v_of_a = v0 + a_range * t

# 4. Графиктерді шығару
col1, col2 = st.columns(2)

with col1:
    st.subheader("S пен a тәуелділігі")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=a_range, y=S_of_a, name="S(a)", line=dict(color='blue')))
    # Қазіргі нүкте
    current_S = v0 * t + (a_current * t**2) / 2
    fig1.add_trace(go.Scatter(x=[a_current], y=[current_S], mode="markers", 
                              marker=dict(color="black", size=10), name="Қазіргі күй"))
    fig1.update_layout(xaxis_title="Үдеу (a), м/с²", yaxis_title="Жол (S), м", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("v пен a тәуелділігі")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=a_range, y=v_of_a, name="v(a)", line=dict(color='red')))
    # Қазіргі нүкте
    current_v = v0 + a_current * t
    fig2.add_trace(go.Scatter(x=[a_current], y=[current_v], mode="markers", 
                              marker=dict(color="black", size=10), name="Қазіргі күй"))
    fig2.update_layout(xaxis_title="Үдеу (a), м/с²", yaxis_title="Жылдамдық (v), м/с", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# 5. ҚОЗҒАЛМАЛЫ АНИМАЦИЯ (Дененің қозғалысы)
st.divider()
st.subheader("🎬 Дененің қозғалыс модельдеуі")

# Анимация үшін уақытты бөлу
fps = 10
frames_count = int(t * fps)
t_anim = np.linspace(0, t, frames_count)
s_anim = v0 * t_anim + (a_current * t_anim**2) / 2

# Анимациялық график (Plotly)
fig_anim = go.Figure(
    data=[go.Scatter(x=[0], y=[0], mode="markers", 
                     marker=dict(symbol="bus", size=30, color="green"))], # Машина белгішесі
    layout=go.Layout(
        xaxis=dict(range=[0, max(s_anim) + 10], title="Жол (метр)"),
        yaxis=dict(range=[-1, 1], visible=False),
        updatemenus=[dict(type="buttons", buttons=[dict(label="Қозғалысты бастау", method="animate")])]
    ),
    frames=[go.Frame(data=[go.Scatter(x=[s_anim[i]], y=[0])]) for i in range(len(s_anim))]
)

st.plotly_chart(fig_anim, use_container_width=True)

# 6. Нәтиже
st.success(f"Есептелген жол: {current_S:.2f} м | Соңғы жылдамдық: {current_v:.2f} м/с")