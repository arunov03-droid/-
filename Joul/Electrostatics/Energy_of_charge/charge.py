import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Беттің тақырыбы
st.title("⚡ Конденсатор энергиясы (W)")
st.markdown("""
Бұл бөлімде конденсаторда жинақталған электр өрісінің энергиясын зерттейміз.
Формулалар: $W = \\frac{CU^2}{2}$ және $W = \\frac{q^2}{2C}$
""")

# 2. Параметрлерді енгізу
st.sidebar.header("Енгізу параметрлері")
U_fixed = st.sidebar.number_input("Тұрақты Кернеу (U), В:", value=10.0, step=1.0)
q_fixed = st.sidebar.number_input("Тұрақты Заряд (q), Кл:", value=1.0e-6, format="%.2e")
C_input = st.sidebar.number_input("Сыйымдылық (C), Ф:", value=1.0e-9, format="%.2e")

# 3. Графиктер үшін деректер дайындау
C_range = np.linspace(1e-10, 1e-8, 100)
U_range = np.linspace(0, 100, 100)
q_range = np.linspace(0, 1e-5, 100)

# 4. Төрт графикті құру
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "W(U) тәуелділігі (C=const)", 
        "W(q) тәуелділігі (C=const)",
        "W(C) тәуелділігі (U=const)", 
        "W(C) тәуелділігі (q=const)"
    )
)

# А) W мен U (Квадраттық: W = C*U^2 / 2)
fig.add_trace(go.Scatter(x=U_range, y=(C_input * U_range**2)/2, name="W(U)", line=dict(color='red')), row=1, col=1)

# Ә) W мен q (Квадраттық: W = q^2 / 2C)
fig.add_trace(go.Scatter(x=q_range, y=(q_range**2)/(2 * C_input), name="W(q)", line=dict(color='blue')), row=1, col=2)

# Б) W мен C (Тура пропорционал: W = C * U^2 / 2, егер U тұрақты болса)
fig.add_trace(go.Scatter(x=C_range, y=(C_range * U_fixed**2)/2, name="W(C)_U", line=dict(color='green')), row=2, col=1)

# В) W мен C (Кері пропорционал: W = q^2 / 2C, егер q тұрақты болса)
fig.add_trace(go.Scatter(x=C_range, y=(q_fixed**2)/(2 * C_range), name="W(C)_q", line=dict(color='orange')), row=2, col=2)

# Стильді баптау
fig.update_layout(height=750, showlegend=False, template="plotly_white")
fig.update_yaxes(title_text="Энергия W (Дж)")

st.plotly_chart(fig, use_container_width=True)

# 5. Мәліметтер панелі
energy_U = (C_input * U_fixed**2) / 2
energy_q = (q_fixed**2) / (2 * C_input)

col1, col2 = st.columns(2)
col1.metric("Энергия (U арқылы)", f"{energy_U*1e6:.4f} мкДж")
col2.metric("Энергия (q арқылы)", f"{energy_q*1e6:.4f} мкДж")

st.warning("""
**Физикалық парадоксқа назар аударыңыз:**
1. Егер **Кернеу (U)** тұрақты болса, сыйымдылық артқан сайын энергия **артады** ($W \sim C$).
2. Егер **Заряд (q)** тұрақты болса, сыйымдылық артқан сайын энергия **кемиді** ($W \sim 1/C$).
""")