import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Бет баптаулары
st.set_page_config(page_title="Джоуль-Ленц заңы (Интерактивті)", layout="wide")

st.title("🔥 Джоуль-Ленц заңы: Сандық мәндерді енгізу модулі")
st.write("Шамаларды слайдермен де, қолмен жазып та өзгерте аласыз.")

# 2. Параметрлерді енгізу (Бүйірлік панель)
st.sidebar.header("Тізбек параметрлері")

# Шамаларды қолмен жазу және слайдермен реттеу мүмкіндігі
U = st.sidebar.number_input("Кернеу (U), Вольт:", min_value=0.0, max_value=500.0, value=220.0, step=1.0)
I = st.sidebar.number_input("Ток күші (I), Ампер:", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
t = st.sidebar.number_input("Уақыт (t), секунд:", min_value=0.0, max_value=3600.0, value=60.0, step=1.0)
R = st.sidebar.number_input("Кедергі (R), Ом:", min_value=0.1, max_value=1000.0, value=44.0, step=0.5)

# 3. Негізгі есептеулер
current_work = U * I * t  # A = UIt
q = I * t                 # q = It

# 4. Графиктер үшін диапазон дайындау
q_range = np.linspace(0, q * 2 if q > 0 else 100, 100)
I_range = np.linspace(0, I * 2 if I > 0 else 20, 100)
t_range = np.linspace(0, t * 2 if t > 0 else 120, 100)
U_range = np.linspace(0, U * 2 if U > 0 else 440, 100)

# 5. Графиктерді құру
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Жұмыс пен Заряд (A = U·q)", 
        "Жұмыс пен Ток күші (A = I²·R·t)",
        "Жұмыс пен Уақыт (A = P·t)", 
        "Жұмыс пен Кернеу (A = U²·t/R)"
    )
)

# Графиктерге деректер қосу
fig.add_trace(go.Scatter(x=q_range, y=U * q_range, name="A(q)", line=dict(color='#3366cc')), row=1, col=1)
fig.add_trace(go.Scatter(x=[q], y=[current_work], mode="markers", marker=dict(size=12, color="black")), row=1, col=1)

fig.add_trace(go.Scatter(x=I_range, y=(I_range**2) * R * t, name="A(I)", line=dict(color='#dc3912')), row=1, col=2)
fig.add_trace(go.Scatter(x=[I], y=[current_work], mode="markers", marker=dict(size=12, color="black")), row=1, col=2)

fig.add_trace(go.Scatter(x=t_range, y=(U * I) * t_range, name="A(t)", line=dict(color='#109618')), row=2, col=1)
fig.add_trace(go.Scatter(x=[t], y=[current_work], mode="markers", marker=dict(size=12, color="black")), row=2, col=1)

fig.add_trace(go.Scatter(x=U_range, y=(U_range**2 / R) * t, name="A(U)", line=dict(color='#ff9900')), row=2, col=2)
fig.add_trace(go.Scatter(x=[U], y=[current_work], mode="markers", marker=dict(size=12, color="black")), row=2, col=2)

fig.update_layout(height=700, showlegend=False, template="simple_white")
st.plotly_chart(fig, use_container_width=True)

# 6. Мәліметтер панелі
col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric("Жұмыс (A)", f"{current_work:.2f} Дж")
col_res2.metric("Заряд (q)", f"{q:.2f} Кл")
col_res3.metric("Қуат (P)", f"{(U*I):.2f} Вт")

st.info(f"💡 Сіз енгізген мәндер бойынша электр тогының жұмысы **{current_work:.2f} Дж** құрады.")