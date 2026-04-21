if sub_menu == "Атом физикасы":
        st.title("⚛️ Резерфордтың атом моделі")
        st.markdown("""
        Резерфорд моделі бойынша атом оң зарядталған ядродан және оны айнала қозғалатын электрондардан тұрады.
        **Бұл конструкторда өз атомыңызды жинап көріңіз:**
        """)

        # 1. БАСҚАРУ ПАНЕЛІ (Sidebar немесе бағандар)
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            protons = st.number_input("Протондар саны (Z):", min_value=1, max_value=10, value=1)
        with col_ctrl2:
            neutrons = st.number_input("Нейтрондар саны (N):", min_value=0, max_value=12, value=0)
        with col_ctrl3:
            electrons = st.number_input("Электрондар саны (e):", min_value=0, max_value=10, value=1)

        # 2. АТОМДЫ АНЫҚТАУ ЛОГИКАСЫ
        # Периодтық кесте (алғашқы 10 элемент)
        elements = {
            1: "Сутегі (H)", 2: "Гелий (He)", 3: "Литий (Li)", 4: "Бериллий (Be)", 5: "Бор (B)",
            6: "Көміртек (C)", 7: "Азот (N)", 8: "Оттегі (O)", 9: "Фтор (F)", 10: "Неон (Ne)"
        }
        
        element_name = elements.get(protons, "Белгісіз элемент")
        mass_number = protons + neutrons
        
        # Изотопты анықтау (ең көп таралған изотоптармен салыстыру)
        common_neutrons = {1: 0, 2: 2, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 8, 9: 10, 10: 10}
        is_isotope = neutrons != common_neutrons.get(protons, 0)
        
        # Ионды анықтау
        charge = protons - electrons
        charge_text = "Бейтарап" if charge == 0 else (f"Оң ион (+{charge})" if charge > 0 else f"Теріс ион ({charge})")

        # 3. АНИМАЦИЯЛЫҚ МОДЕЛЬ (Plotly арқылы)
        st.subheader(f"🔬 Модель: {element_name}")
        
        # Ақпараттық панель
        inf1, inf2, inf3 = st.columns(3)
        inf1.metric("Элемент", element_name)
        inf2.metric("Массалық сан (A)", mass_number)
        inf3.metric("Заряды", charge_text)
        
        if is_isotope:
            st.warning(f"⚠️ Бұл — {element_name} элементінің изотобы!")

        # Графикті құру
        fig_atom = go.Figure()

        # Ядро (Протондар мен Нейтрондар)
        # Протондар (Қызыл), Нейтрондар (Сұр)
        for i in range(protons):
            fig_atom.add_trace(go.Scatter(x=[np.random.uniform(-0.3, 0.3)], y=[np.random.uniform(-0.3, 0.3)],
                                         mode="markers", marker=dict(size=15, color="red"), name="Протон", showlegend=False))
        for i in range(neutrons):
            fig_atom.add_trace(go.Scatter(x=[np.random.uniform(-0.3, 0.3)], y=[np.random.uniform(-0.3, 0.3)],
                                         mode="markers", marker=dict(size=15, color="gray"), name="Нейтрон", showlegend=False))

        # Электрондық орбиталар мен электрондар
        t = np.linspace(0, 2*np.pi, 100)
        orbits = [2, 4, 6] # Орбита радиустары
        
        for i in range(electrons):
            orbit_idx = 0 if i < 2 else (1 if i < 8 else 2)
            r = orbits[orbit_idx]
            # Электронның орбитадағы қозғалысын сипаттау (визуалды)
            angle = (2 * np.pi / min(electrons, 8)) * i
            ex = r * np.cos(angle)
            ey = r * np.sin(angle)
            
            # Орбита сызығы
            fig_atom.add_trace(go.Scatter(x=r*np.cos(t), y=r*np.sin(t), mode="lines", 
                                         line=dict(color="silver", width=1, dash="dot"), showlegend=False))
            # Электрон
            fig_atom.add_trace(go.Scatter(x=[ex], y=[ey], mode="markers+text", 
                                         marker=dict(size=10, color="blue"), text=["e⁻"], textposition="top center", showlegend=False))

        fig_atom.update_layout(
            xaxis=dict(range=[-7, 7], visible=False),
            yaxis=dict(range=[-7, 7], visible=False),
            width=600, height=600,
            template="plotly_white",
            title=f"{element_name} атомының құрылымы"
        )
        st.plotly_chart(fig_atom, use_container_width=True)
        
        st.info("""
        **Нұсқаулық:** - Протон санын өзгертсеңіз — элемент өзгереді.
        - Нейтрон санын өзгертсеңіз — изотоптар түзіледі.
        - Электрон санын өзгертсеңіз — атом ионға айналады.
        """)