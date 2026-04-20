import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Бет тақырыбы
st.title("🎾 Энергия түрлері және тәуелділіктер")
st.markdown("""
Бұл бөлімде кинетикалық, потенциалдық және жалпы жұмысты зерттейміз.
Формулалар: $A = mavt$, $E_k = \\frac{mv^2}{2}$, $E_p = mgh$
""")

# 2. ПАРАМЕТРЛЕРДІ ЕНГІЗУ (Төменде болуы үшін бағандарға бөлеміз)
st.divider()
col_inp1, col_inp2, col_inp3 = st.columns(3)
with col_inp1:
    m = st.number_input("Масса (m), кг:", min_value=0.1, value=2.0, step=0.5)
    a = st.number_input("Үдеу (a), м/с²:", value=2.0, step=0.1)
with col_inp2:
    v = st.number_input("Жылдамдық (v), м/с:", value=5.0, step=0.5)
    h = st.number_input("Биіктік (h), м:", value=10.0, step=1.0)
with col_inp3:
    t = st.number_input("Уақыт (t), с:", value=5.0, step=0.5)
    g = 9.8  # Еркін түсу үдеуі

# 3. Есептеулер
E_work = m * a * v * t   # Жалпы жұмыс/энергия
E_kin = (m * v**2) / 2   # Кинетикалық
E_pot = m * g * h        # Потенциалдық

# 4. АНИМАЦИЯ (Қызыл доптың қозғалысы - Беттің жоғарғы жағында)
# Анимацияны басында көрсету үшін контейнерді қолданамыз
anim_container = st.container()

with anim_container:
    # Доптың биіктігі мен қозғалысының визуализациясы
    t_plot = np.linspace(0, 2*np.pi, 50)
    # Биіктікті көрсету үшін y осін қолданамыз
    fig_ball = go.Figure(
        data=[go.Scatter(x=[0], y=[h], mode="markers+text",
                         marker=dict(size=30, color="red"),
                         text=["Қызыл доп"], textposition="top center")],
        layout=go.Layout(
            xaxis=dict(range=[-1, 1], visible=False),
            yaxis=dict(range=[0, h + 20], title="Биіктік (м)"),
            height=300,
            template="plotly_white",
            title=f"Доптың қазіргі биіктігі: {h} м",
            updatemenus=[dict(type="buttons", buttons=[dict(label="Қозғалысты көру", method="animate")])]
        ),
        frames=[go.Frame(data=[go.Scatter(x=[0], y=[h - (h/10)*i])]) for i in range(11)]
    )
    st.plotly_chart(fig_ball, use_container_width=True)

# 5. ГРАФИКТЕР (Үш тәуелділік)
st.divider()
st.subheader("📊 Энергия тәуелділіктерінің графиктері")

m_range = np.linspace(0.1, 20, 100)
v_range = np.linspace(0, 30, 100)
h_range = np.linspace(0, 50, 100)

fig_graphs = make_subplots(rows=1, cols=3, 
                           subplot_titles=("E(m) тәуелділігі", "E(v) тәуелділігі", "E(h) тәуелділігі"))

# E мен m (Тура пропорционал: E = m*a*v*t)
fig_graphs.add_trace(go.Scatter(x=m_range, y=m_range * a * v * t, name="E(m)", line=dict(color='blue')), row=1, col=1)
fig_graphs.add_trace(go.Scatter(x=[m], y=[E_work], mode="markers", marker=dict(size=10, color="black")), row=1, col=1)

# E мен v (Квадраттық: Ek = mv^2 / 2)
fig_graphs.add_trace(go.Scatter(x=v_range, y=(m * v_range**2)/2, name="E(v)", line=dict(color='green')), row=1, col=2)
fig_graphs.add_trace(go.Scatter(x=[v], y=[E_kin], mode="markers", marker=dict(size=10, color="black")), row=1, col=2)

# E мен h (Тура пропорционал: Ep = mgh)
fig_graphs.add_trace(go.Scatter(x=h_range, y=m * g * h_range, name="E(h)", line=dict(color='orange')), row=1, col=3)
fig_graphs.add_trace(go.Scatter(x=[h], y=[E_pot], mode="markers", marker=dict(size=10, color="black")), row=1, col=3)

fig_graphs.update_layout(height=400, showlegend=False, template="plotly_white")
st.plotly_chart(fig_graphs, use_container_width=True)

# 6. ҚОРЫТЫНДЫ
res1, res2, res3 = st.columns(3)
res1.metric("Жалпы жұмыс (A)", f"{E_work:.1f} Дж")
res2.metric("Кинетикалық энергия", f"{E_kin:.1f} Дж")
res3.metric("Потенциалдық энергия", f"{E_pot:.1f} Дж")