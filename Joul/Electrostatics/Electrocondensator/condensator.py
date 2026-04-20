import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Бет тақырыбы
st.title("🔌 Электросыйымдылық және Конденсаторлар")
st.markdown("""
Бұл бөлімде өткізгіштердің электросыйымдылығы мен жазық конденсатордың параметрлерін зерттейміз.
Формулалар: $C = \\frac{q}{U}$ және $C = \\frac{\\varepsilon \cdot \\varepsilon_0 \cdot S}{d}$
""")

# 2. Параметрлерді енгізу (Sidebar)
st.sidebar.header("Параметрлер")
q_val = st.sidebar.number_input("Заряд (q), Кл:", value=1.0e-6, format="%.2e")
U_val = st.sidebar.number_input("Кернеу (U), В:", value=10.0, step=1.0)
S_val = st.sidebar.number_input("Аудан (S), м²:", value=0.01, step=0.001)
d_val = st.sidebar.number_input("Қашықтық (d), м:", value=0.001, min_value=0.0001, format="%.4f")
eps = st.sidebar.slider("Диэлектрлік өтімділік (ε):", 1, 10, 1)

# Тұрақтылар
eps0 = 8.85e-12

# 3. Негізгі есептеулер
C_general = q_val / U_val
C_flat = (eps * eps0 * S_val) / d_val

# 4. Графиктер үшін деректер
# А) C(q) мен C(U) - Сыйымдылық геометрияға тәуелді, q мен U-ға тәуелсіз (тұрақты)
# Бірақ оқушыларға бұл тұрақтылықты көрсету маңызды
q_range = np.linspace(1e-7, 1e-5, 100)
U_range = np.linspace(1, 100, 100)
S_range = np.linspace(0.001, 0.1, 100)
d_range = np.linspace(0.0001, 0.01, 100)

fig = make_subplots(rows=2, cols=2, 
                    subplot_titles=("C(q) тәуелділігі (U = const)", 
                                    "C(U) тәуелділігі (q = const)", 
                                    "C(S) тәуелділігі (Жазық конд.)", 
                                    "C(d) тәуелділігі (Жазық конд.)"))

# 1-график: C(q)
fig.add_trace(go.Scatter(x=q_range, y=[C_general]*100, name="C(q)", line=dict(color='blue')), row=1, col=1)
# 2-график: C(U)
fig.add_trace(go.Scatter(x=U_range, y=[C_general]*100, name="C(U)", line=dict(color='red')), row=1, col=2)
# 3-график: C(S) - тура пропорционал
fig.add_trace(go.Scatter(x=S_range, y=(eps * eps0 * S_range)/d_val, name="C(S)", line=dict(color='green')), row=2, col=1)
# 4-график: C(d) - кері пропорционал
fig.add_trace(go.Scatter(x=d_range, y=(eps * eps0 * S_val)/d_range, name="C(d)", line=dict(color='purple')), row=2, col=2)

fig.update_layout(height=700, showlegend=False, template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# 5. Мәліметтер панелі
col1, col2 = st.columns(2)
col1.metric("Жалпы сыйымдылық (C=q/U)", f"{C_general*1e12:.2f} пФ")
col2.metric("Жазық конд. сыйымдылығы", f"{C_flat*1e12:.2f} пФ")

st.info("**Ескерту:** Графиктерде көріп тұрғаныңыздай, өткізгіштің сыйымдылығы заряд пен кернеуге тәуелді емес (олар өзгерсе де, C тұрақты қалады). Ал жазық конденсатордың сыйымдылығы оның геометриялық өлшемдеріне (S, d) тікелей тәуелді.")