if sub_menu == "Кванттық теория":
        st.title("💡 Кванттық теория: Фотоэффект құбылысы")
        st.markdown("""
        Фотоэффект — жарық әсерінен заттан (металдан) электрондардың ұшып шығу құбылысы.
        **Эйнштейн теңдеуі:** $h\\nu = A_{шығу} + E_{к,max}$
        (мұнда $h\\nu$ - фотон энергиясы, $A_{шығу}$ - шығу жұмысы, $E_{к,max}$ - электронның макс. кинетикалық энергиясы)
        """)

        # 1. ПАРАМЕТРЛЕРДІ БАСҚАРУ (Sidebar)
        st.sidebar.header("Фотоэффект параметрлері")
        
        # Металды таңдау (Шығу жұмысы A_out өзгереді)
        metal = st.sidebar.selectbox("Металды таңдаңыз (A_шығу):", 
                                     ["Цезий (2.14 эВ)", "Натрий (2.36 эВ)", "Цинк (4.31 эВ)", "Платина (5.65 эВ)"])
        a_out_ev_dict = {"Цезий (2.14 эВ)": 2.14, "Натрий (2.36 эВ)": 2.36, "Цинк (4.31 эВ)": 4.31, "Платина (5.65 эВ)": 5.65}
        a_out_ev = a_out_ev_dict[metal]
        
        # Жарық жиілігі немесе толқын ұзындығы (Слайдер)
        wavelength_nm = st.sidebar.slider("Жарықтың толқын ұзындығы (λ), нм:", 200, 800, 400)
        
        # Жарық интенсивтілігі (Электрондар саны үшін)
        intensity = st.sidebar.slider("Жарық интенсивтілігі (Фотон саны):", 1, 20, 10)

        # Тұрақтылар
        h = 6.626e-34  # Планк тұрақтысы (Дж·с)
        c = 3.0e8      # Жарық жылдамдығы (м/с)
        e_charge = 1.602e-19 # Электрон заряды (эВ-тан Дж-ға көшу үшін)

        # Есептеулер
        wavelength_m = wavelength_nm * 1e-9
        frequency = c / wavelength_m
        e_photon_j = h * frequency
        e_photon_ev = e_photon_j / e_charge
        
        # Теңдеу: Ek = E_ph - A_out
        e_kin_ev = e_photon_ev - a_out_ev

        # 2. ВИЗУАЛИЗАЦИЯ (Фотон мен Электрон анимациясы)
        st.subheader("🎬 Фотоэффекттің микроскопиялық моделі")
        
        # Фотоэффект шарты орындала ма?
        photoeffect_happens = e_kin_ev > 0
        
        # Анимациялық график (Plotly)
        fig_photo = go.Figure()
        
        # Металл беті (плита)
        fig_photo.add_shape(type="rect", x0=0, y0=0, x1=10, y1=2, fillcolor="Grey", line=dict(color="Black"))
        fig_photo.add_annotation(x=5, y=1, text=f"Металл: {metal}", showarrow=False, font=dict(color="White"))
        
        # Түскен фотондар (Интенсивтілікке байланысты саны өзгереді)
        photon_color = f"rgb({min(255, 800-wavelength_nm)}, 0, {min(255, wavelength_nm-200)})" # Түсі λ-ға байланысты
        for i in range(intensity):
            fig_photo.add_trace(go.Scatter(x=[2 + i*0.4, 1 + i*0.4], y=[8, 2.5], 
                                           mode="lines+markers", 
                                           line=dict(color=photon_color, width=3, dash="dash"),
                                           marker=dict(symbol="arrow", size=8, angleref="previous"),
                                           showlegend=False))

        # Ұшып шыққан электрондар (Егер Ek > 0 болса)
        if photoeffect_happens:
            st.success(f"✅ Фотоэффект жүріп жатыр! Фотондар энергиясы ({e_photon_ev:.2f} эВ) Шығу жұмысынан ({a_out_ev:.2f} эВ) үлкен.")
            # Электрондардың жылдамдығы Ek-ға байланысты (визуалды)
            electron_speed = min(10, e_kin_ev * 2) 
            for i in range(intensity):
                fig_photo.add_trace(go.Scatter(x=[1 + i*0.4, 1 + i*0.4 + electron_speed], y=[2.5, 2.5 + electron_speed],
                                               mode="markers+text", 
                                               marker=dict(size=12, color="LimeGreen", symbol="circle"),
                                               text=["e⁻"], textposition="top center",
                                               showlegend=False))
        else:
            st.error(f"❌ Фотоэффект жоқ. Фотондар энергиясы ({e_photon_ev:.2f} эВ) Шығу жұмысынан ({a_out_ev:.2f} эВ) кіші.")
            st.warning(f"💡 Кеңес: Жарықтың толқын ұзындығын (λ) азайтыңыз немесе басқа металл таңдаңыз.")

        fig_photo.update_layout(xaxis=dict(range=[0, 12], visible=False), yaxis=dict(range=[0, 10], visible=False),
                                width=600, height=400, template="plotly_white", title="Фотон түсуі және электрон ұшуы")
        st.plotly_chart(fig_photo, use_container_width=True)

        # 3. ЕКІ НЕГІЗГІ ГРАФИК (Тәуелділіктер)
        st.divider()
        st.subheader("📊 Фотоэффект графиктері")
        
        # Графиктер үшін диапазондар
        freq_range = np.linspace(3e14, 15e14, 100) # Жиілік 300 ТГц - 1500 ТГц
        wavelength_range_nm = np.linspace(200, 800, 100)
        
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("**Ek,max мен жиілік (ν) тәуелділігі**")
            # Ek = h*nu - A_out
            fig_ek_freq = go.Figure()
            ek_ev_range = (h * freq_range / e_charge) - a_out_ev
            fig_ek_freq.add_trace(go.Scatter(x=freq_range, y=ek_ev_range, name="Ek(ν)", line=dict(color='LimeGreen')))
            # "Қызыл шекара" (Ek=0 болатын жиілік)
            red_boundary_freq = (a_out_ev * e_charge) / h
            fig_ek_freq.add_shape(type="line", x0=red_boundary_freq, y0=-2, x1=red_boundary_freq, y1=6, 
                                  line=dict(color="Red", dash="dash"))
            
            # Ағымдағы нүкте
            if photoeffect_happens:
                fig_ek_freq.add_trace(go.Scatter(x=[frequency], y=[e_kin_ev], mode="markers", 
                                               marker=dict(size=10, color="black"), name="Қазіргі күй"))

            fig_ek_freq.update_layout(xaxis_title="Жиілік (ν), Гц", yaxis_title="Ek,max (эВ)", yaxis=dict(range=[0, 6]), height=350)
            st.plotly_chart(fig_ek_freq, use_container_width=True)

        with g2:
            st.write("**Фоототок пен Уақыт (t) (Интенсивтілікке тәуелділік)**")
            # Фототок интенсивтілікке тура пропорционал (қанығу тогы)
            # Бұл график тек интенсивтіліктің әсерін көрсетеді (визуалды)
            fig_current_int = go.Figure()
            fig_current_int.add_trace(go.Scatter(x=[0, 1, 2, 3, 4, 5], y=[0, intensity, intensity, intensity, intensity, intensity], 
                                               name="Фототок", line=dict(color='LimeGreen', width=3)))
            fig_current_int.update_layout(xaxis_title="Уақыт", yaxis_title="Фототок (визуалды)", yaxis=dict(range=[0, 25]), height=350)
            st.plotly_chart(fig_current_int, use_container_width=True)

        st.metric("Фотон энергиясы (E_ph):", f"{e_photon_ev:.2f} эВ")
        st.metric("Электрон энергиясы (E_k,max):", f"{max(0, e_kin_ev):.2f} эВ")