if sub_menu == "Менделеев - Клайперон теңдеу":
        st.title("🎈 Идеал газ күйінің теңдеуі")
        st.markdown("""
        Менделеев-Клайперон теңдеуі газдың қысымы, көлемі және температурасы арасындағы байланысты сипаттайды.
        Формула: $PV = nRT$
        """)

        # 1. ПАРАМЕТРЛЕРДІ ЕНГІЗУ (Басқару панелі)
        st.sidebar.header("Газ параметрлері")
        n_mol = st.sidebar.number_input("Зат мөлшері (n), моль:", min_value=0.1, value=1.0, step=0.1)
        T_gas = st.sidebar.slider("Температура (T), К:", 100, 1000, 300)
        V_gas = st.sidebar.slider("Көлем (V), м³:", 0.1, 10.0, 2.0)
        
        # Тұрақты
        R = 8.31
        # Қысымды есептеу: P = nRT / V
        P_gas = (n_mol * R * T_gas) / V_gas

        # 2. ВИЗУАЛИЗАЦИЯ (Поршеньді ыдыс моделі)
        st.subheader("📦 Газ толтырылған поршень моделі")
        
        # Газдың күйін поршень биіктігімен көрсету
        fig_piston = go.Figure()
        # Ыдыс
        fig_piston.add_shape(type="rect", x0=0, y0=0, x1=2, y1=10, line=dict(color="Black", width=3))
        # Поршень (Көлемге байланысты биіктігі өзгереді)
        fig_piston.add_shape(type="rect", x0=0, y0=V_gas, x1=2, y1=V_gas + 0.5, 
                             fillcolor="Grey", line=dict(color="Black"))
        # Газ молекулалары (Температураға байланысты түсі өзгереді: суық - көк, ыстық - қызыл)
        gas_color = f"rgb({min(255, T_gas/4)}, 0, {max(0, 255-T_gas/4)})"
        fig_piston.add_shape(type="rect", x0=0, y0=0, x1=2, y1=V_gas, 
                             fillcolor=gas_color, opacity=0.4, line=dict(width=0))
        
        fig_piston.update_layout(xaxis=dict(visible=False), yaxis=dict(range=[0, 11], title="Көлем (м³)"),
                                width=300, height=450, title="Поршень күйі")
        
        col_vis, col_metric = st.columns([1, 1])
        with col_vis:
            st.plotly_chart(fig_piston)
        with col_metric:
            st.metric("Есептелген Қысым (P):", f"{P_gas:.2f} Па")
            st.write(f"**Бұл күйде:**")
            st.write(f"- Температура: {T_gas} К")
            st.write(f"- Көлем: {V_gas} м³")
            st.write(f"- Зат мөлшері: {n_mol} моль")

        # 3. ГРАФИКТЕР (Үш негізгі тәуелділік)
        st.divider()
        st.subheader("📊 Изопроцестер графиктері")
        
        t_range = np.linspace(100, 1000, 100)
        v_range = np.linspace(0.1, 10, 100)
        
        g1, g2, g3 = st.columns(3)
        
        with g1:
            st.write("**P мен T (Изохора, V=const)**")
            fig_pt = go.Figure()
            fig_pt.add_trace(go.Scatter(x=t_range, y=(n_mol * R * t_range) / V_gas, line=dict(color='red')))
            fig_pt.add_trace(go.Scatter(x=[T_gas], y=[P_gas], mode="markers", marker=dict(size=10, color="black")))
            fig_pt.update_layout(xaxis_title="T (К)", yaxis_title="P (Па)", height=300)
            st.plotly_chart(fig_pt, use_container_width=True)

        with g2:
            st.write("**V мен T (Изобара, P=const)**")
            fig_vt = go.Figure()
            # V = nRT / P. Мұнда P-ны ағымдағы P_gas деп бекітеміз
            fig_vt.add_trace(go.Scatter(x=t_range, y=(n_mol * R * t_range) / P_gas, line=dict(color='blue')))
            fig_vt.add_trace(go.Scatter(x=[T_gas], y=[V_gas], mode="markers", marker=dict(size=10, color="black")))
            fig_vt.update_layout(xaxis_title="T (К)", yaxis_title="V (м³)", height=300)
            st.plotly_chart(fig_vt, use_container_width=True)

        with g3:
            st.write("**P мен V (Изотерма, T=const)**")
            fig_pv = go.Figure()
            # P = nRT / V. Кері пропорционал
            fig_pv.add_trace(go.Scatter(x=v_range, y=(n_mol * R * T_gas) / v_range, line=dict(color='green')))
            fig_pv.add_trace(go.Scatter(x=[V_gas], y=[P_gas], mode="markers", marker=dict(size=10, color="black")))
            fig_pv.update_layout(xaxis_title="V (м³)", yaxis_title="P (Па)", height=300)
            st.plotly_chart(fig_pv, use_container_width=True)