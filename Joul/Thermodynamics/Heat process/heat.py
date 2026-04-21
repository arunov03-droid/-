if sub_menu == "Жылу процестері":
        st.title("🔥 Жылу құбылыстары: Меншікті жылу сыйымдылығы")
        st.markdown("""
        Затты қыздыруға қажетті жылу мөлшерін есептеу.
        Формула: $Q = c \cdot m \cdot \Delta T$
        """)

        # 1. ВИЗУАЛИЗАЦИЯ (Қыздыру процесі)
        st.subheader("☕ Суды қыздыру моделі")
        
        # Слайдер арқылы температураны басқару (анимация үшін)
        temp_val = st.slider("Температура өзгерісі (ΔT), °C:", 0, 100, 20)
        
        # Plotly арқылы термометр мен ыдысты көрсету
        fig_heat = go.Figure()
        # Ыдыс (бейнесі)
        fig_heat.add_shape(type="rect", x0=1, y0=0, x1=3, y1=temp_val, 
                           fillcolor="OrangeRed", opacity=0.6, line=dict(color="Red"))
        # Термометрдің сыртқы қабығы
        fig_heat.add_shape(type="rect", x0=0.5, y0=0, x1=0.8, y1=100, 
                           line=dict(color="Black"))
        # Термометр ішіндегі сынап
        fig_heat.add_shape(type="rect", x0=0.5, y0=0, x1=0.8, y1=temp_val, 
                           fillcolor="Red")
        
        fig_heat.update_layout(xaxis=dict(visible=False), yaxis=dict(title="Температура (°C)", range=[0, 110]),
                              width=400, height=400, title="Қыздыру деңгейі")
        st.plotly_chart(fig_heat)

        # 2. ПАРАМЕТРЛЕРДІ ЕНГІЗУ
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            m_heat = st.number_input("Масса (m), кг:", min_value=0.1, value=1.0, step=0.5)
            # Меншікті жылу сыйымдылығы үшін таңдау (c)
            substance = st.selectbox("Затты таңдаңыз (c):", 
                                    ["Су (4200)", "Мұз (2100)", "Темір (460)", "Алюминий (920)"])
            c_values = {"Су (4200)": 4200, "Мұз (2100)": 2100, "Темір (460)": 460, "Алюминий (920)": 920}
            c_val = c_values[substance]
        
        with col2:
            st.info(f"Таңдалған заттың жылу сыйымдылығы: {c_val} Дж/(кг·°C)")
            Q_total = c_val * m_heat * temp_val

        # 3. ГРАФИКТЕР
        st.subheader("📊 Тәуелділік графиктері")
        c_range = np.linspace(100, 5000, 100)
        t_range = np.linspace(0, 100, 100)
        
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("**Q мен c тәуелділігі (m, ΔT = const)**")
            fig_qc = go.Figure()
            fig_qc.add_trace(go.Scatter(x=c_range, y=c_range * m_heat * temp_val, name="Q(c)", line=dict(color='orange')))
            fig_qc.add_trace(go.Scatter(x=[c_val], y=[Q_total], mode="markers", marker=dict(size=12, color="black")))
            fig_qc.update_layout(xaxis_title="Меншікті жылу сыйымдылығы (c)", yaxis_title="Жылу мөлшері (Q), Дж")
            st.plotly_chart(fig_qc, use_container_width=True)

        with g2:
            st.write("**Q мен ΔT тәуелділігі (m, c = const)**")
            fig_qt = go.Figure()
            fig_qt.add_trace(go.Scatter(x=t_range, y=c_val * m_heat * t_range, name="Q(ΔT)", line=dict(color='red')))
            fig_qt.add_trace(go.Scatter(x=[temp_val], y=[Q_total], mode="markers", marker=dict(size=12, color="black")))
            fig_qt.update_layout(xaxis_title="Температура өзгерісі (ΔT)", yaxis_title="Жылу мөлшері (Q), Дж")
            st.plotly_chart(fig_qt, use_container_width=True)

        st.success(f"Есептелген жылу мөлшері: {Q_total:.1f} Дж (немесе {Q_total/1000:.2f} кДж)")