if sub_menu == "МКТ":
        st.title("🌡️ Молекулалық-кинетикалық теория (МКТ)")
        st.markdown("""
        Бұл бөлімде газ қысымының молекула параметрлеріне тәуелділігін зерттейміз.
        Формула: $p = n \cdot m \cdot v$ (мұндағы $n$ - концентрация, $m$ - масса, $v$ - жылдамдық)
        """)

        # 1. АНИМАЦИЯ (Ыдыстағы молекулалар қозғалысы)
        # Біз мұны Plotly арқылы "тірі" график ретінде жасаймыз
        st.subheader("🧪 Ыдыстағы молекулалардың моделі")
        
        # Молекулалар саны
        num_particles = 20
        # Кездейсоқ позициялар мен жылдамдықтар
        pos_x = np.random.rand(num_particles) * 10
        pos_y = np.random.rand(num_particles) * 10
        
        fig_atoms = go.Figure(
            data=[go.Scatter(x=pos_x, y=pos_y, mode="markers", 
                             marker=dict(size=12, color="royalblue", symbol="circle"))],
            layout=go.Layout(
                xaxis=dict(range=[0, 10], visible=False),
                yaxis=dict(range=[0, 10], visible=False),
                width=500, height=400,
                template="plotly_white",
                title="Ыдыс ішіндегі қозғалыс",
                margin=dict(l=20, r=20, t=40, b=20)
            )
        )
        st.plotly_chart(fig_atoms, use_container_width=True)

        # 2. ПАРАМЕТРЛЕРДІ БАСҚАРУ (Астында)
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            m_mol = st.number_input("Молекула массасы (m), кг:", value=1.0e-26, format="%.2e")
        with col2:
            n_mol = st.number_input("Концентрация (n), м⁻³:", value=1.0e25, format="%.2e")
        with col3:
            v_mol = st.number_input("Жылдамдық (v), м/с:", value=500.0, step=50.0)

        # 3. ЕСЕПТЕУЛЕР МЕН ГРАФИКТЕР
        p_current = n_mol * m_mol * v_mol
        
        m_range = np.linspace(1e-27, 1e-25, 100)
        v_range = np.linspace(0, 2000, 100)
        
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("**p мен m тәуелділігі**")
            fig_pm = go.Figure()
            fig_pm.add_trace(go.Scatter(x=m_range, y=n_mol * m_range * v_mol, name="p(m)", line=dict(color='blue')))
            fig_pm.add_trace(go.Scatter(x=[m_mol], y=[p_current], mode="markers", marker=dict(size=10, color="black")))
            fig_pm.update_layout(xaxis_title="Масса (m)", yaxis_title="Қысым (p)", height=350)
            st.plotly_chart(fig_pm, use_container_width=True)

        with g2:
            st.write("**p мен v тәуелділігі**")
            fig_pv = go.Figure()
            fig_pv.add_trace(go.Scatter(x=v_range, y=n_mol * m_mol * v_range, name="p(v)", line=dict(color='red')))
            fig_pv.add_trace(go.Scatter(x=[v_mol], y=[p_current], mode="markers", marker=dict(size=10, color="black")))
            fig_pv.update_layout(xaxis_title="Жылдамдық (v)", yaxis_title="Қысым (p)", height=350)
            st.plotly_chart(fig_pv, use_container_width=True)

        st.metric("Есептелген қысым (p):", f"{p_current:.2f} Па")
        st.info("💡 Қысым — бұл молекулалардың ыдыс қабырғасына соғылу күші. Масса немесе жылдамдық артса, соққы қуаты да артады.")