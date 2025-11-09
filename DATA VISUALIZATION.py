import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Analítico Universitario",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('university_student_data.csv')
    return df

df = load_data()

# Header con información del equipo
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🎓 Dashboard Analítico Universitario")
    st.markdown("### Análisis de Datos de Admisiones, Matrícula y Retención Estudiantil")
with col2:
    st.markdown("#### 👥 Equipo")
    st.markdown("**Alejandro Escorcia**")
    st.markdown("**Ashley Urueta**")
    st.caption("Universidad de la Costa")

st.markdown("---")

# Métricas generales (sin filtros)
st.markdown("## 📊 Indicadores Generales del Sistema")
st.markdown("*Vista completa de todos los datos históricos (2015-2024)*")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg_retention = df['Retention Rate (%)'].mean()
    max_retention = df['Retention Rate (%)'].max()
    st.metric(
        label="📈 Retención Promedio",
        value=f"{avg_retention:.1f}%",
        delta=f"Máximo: {max_retention:.0f}%"
    )

with col2:
    avg_satisfaction = df['Student Satisfaction (%)'].mean()
    growth_satisfaction = df.groupby('Year')['Student Satisfaction (%)'].mean()
    satisfaction_growth = growth_satisfaction.iloc[-1] - growth_satisfaction.iloc[0]
    st.metric(
        label="😊 Satisfacción Media",
        value=f"{avg_satisfaction:.1f}%",
        delta=f"+{satisfaction_growth:.0f}% desde 2015"
    )

with col3:
    total_enrolled = df['Enrolled'].sum()
    st.metric(
        label="👥 Total Histórico",
        value=f"{total_enrolled:,}",
        delta="Estudiantes matriculados"
    )

with col4:
    avg_admission_rate = (df['Admitted'].sum() / df['Applications'].sum() * 100)
    st.metric(
        label="✅ Tasa de Admisión",
        value=f"{avg_admission_rate:.1f}%",
        delta="Media histórica"
    )

with col5:
    total_apps = df['Applications'].sum()
    growth_apps = ((df[df['Year']==2024]['Applications'].sum() / df[df['Year']==2015]['Applications'].sum() - 1) * 100)
    st.metric(
        label="📝 Aplicaciones Totales",
        value=f"{total_apps:,}",
        delta=f"+{growth_apps:.0f}% crecimiento"
    )

with st.expander("📖 ¿Qué significan estos indicadores?"):
    st.markdown("""
    - **Retención**: Porcentaje de estudiantes que permanecen año tras año. Valores >85% son excelentes.
    - **Satisfacción**: Percepción estudiantil sobre su experiencia. >80% indica alta calidad educativa.
    - **Tasa de Admisión**: Selectividad institucional. Refleja competitividad y estándares académicos.
    - **Crecimiento**: Indica la evolución y atractivo de la institución en el tiempo.
    """)

st.markdown("---")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Evolución Temporal", 
    "🆚 Análisis Comparativo", 
    "🏢 Departamentos", 
    "🎯 Análisis Profundo"
])

# ==================== TAB 1: EVOLUCIÓN TEMPORAL ====================
with tab1:
    st.header("📈 Evolución Temporal de Indicadores Clave")
    
    # Filtro específico para tendencias temporales
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### Selecciona el período de análisis")
    with col2:
        years_available = sorted(df['Year'].unique())
        year_filter = st.selectbox(
            "Filtrar desde el año:",
            options=['Todos'] + years_available,
            key="year_trend_filter"
        )
    
    # Aplicar filtro
    if year_filter != 'Todos':
        df_trend = df[df['Year'] >= year_filter].copy()
        st.info(f"📊 Mostrando datos desde {year_filter} hasta 2024 ({len(df_trend)} registros)")
    else:
        df_trend = df.copy()
    
    # Agrupar por año
    df_yearly = df_trend.groupby('Year').agg({
        'Retention Rate (%)': 'mean',
        'Student Satisfaction (%)': 'mean',
        'Enrolled': 'sum',
        'Applications': 'sum',
        'Admitted': 'sum'
    }).reset_index()
    
    # Gráfico principal: Retención y Satisfacción
    st.subheader("🎯 Retención y Satisfacción Estudiantil")
    
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig1.add_trace(
        go.Scatter(
            x=df_yearly['Year'], 
            y=df_yearly['Retention Rate (%)'], 
            name="Tasa de Retención",
            mode='lines+markers',
            line=dict(color='#0077B6', width=4),
            marker=dict(size=10, symbol='circle'),
            hovertemplate='<b>Año %{x}</b><br>Retención: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig1.add_trace(
        go.Scatter(
            x=df_yearly['Year'], 
            y=df_yearly['Student Satisfaction (%)'], 
            name="Satisfacción Estudiantil",
            mode='lines+markers',
            line=dict(color='#E63946', width=4),
            marker=dict(size=10, symbol='diamond'),
            hovertemplate='<b>Año %{x}</b><br>Satisfacción: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig1.update_xaxes(title_text="<b>Año Académico</b>", gridcolor='lightgray')
    fig1.update_yaxes(title_text="<b>Porcentaje (%)</b>", secondary_y=False, gridcolor='lightgray')
    fig1.update_layout(
        height=450, 
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Interpretación automática
    retention_trend = "ascendente ↗️" if df_yearly['Retention Rate (%)'].is_monotonic_increasing else "variable 📊"
    satisfaction_trend = "ascendente ↗️" if df_yearly['Student Satisfaction (%)'].is_monotonic_increasing else "variable 📊"
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"""
        **💡 Análisis de Retención:** 
        - Tendencia {retention_trend}
        - Valor inicial: {df_yearly['Retention Rate (%)'].iloc[0]:.1f}%
        - Valor final: {df_yearly['Retention Rate (%)'].iloc[-1]:.1f}%
        - Cambio total: {df_yearly['Retention Rate (%)'].iloc[-1] - df_yearly['Retention Rate (%)'].iloc[0]:+.1f} puntos porcentuales
        """)
    
    with col2:
        st.success(f"""
        **💡 Análisis de Satisfacción:**
        - Tendencia {satisfaction_trend}
        - Valor inicial: {df_yearly['Student Satisfaction (%)'].iloc[0]:.1f}%
        - Valor final: {df_yearly['Student Satisfaction (%)'].iloc[-1]:.1f}%
        - Cambio total: {df_yearly['Student Satisfaction (%)'].iloc[-1] - df_yearly['Student Satisfaction (%)'].iloc[0]:+.1f} puntos porcentuales
        """)
    
    st.markdown("---")
    
    # Gráfico de matrícula
    st.subheader("👥 Crecimiento de la Matrícula Estudiantil")
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=df_yearly['Year'],
        y=df_yearly['Enrolled'],
        name='Estudiantes Matriculados',
        marker_color='#06A77D',
        text=df_yearly['Enrolled'],
        textposition='outside',
        texttemplate='%{text:,}',
        hovertemplate='<b>%{x}</b><br>Matriculados: %{y:,}<extra></extra>'
    ))
    
    # Agregar línea de tendencia
    fig2.add_trace(go.Scatter(
        x=df_yearly['Year'],
        y=df_yearly['Enrolled'],
        mode='lines',
        name='Tendencia',
        line=dict(color='#023047', width=3, dash='dash'),
        hovertemplate='<b>Tendencia</b><br>%{y:,}<extra></extra>'
    ))
    
    fig2.update_layout(
        height=400,
        xaxis_title="<b>Año</b>",
        yaxis_title="<b>Número de Estudiantes</b>",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Cálculo de crecimiento
    enrollment_growth = ((df_yearly['Enrolled'].iloc[-1] / df_yearly['Enrolled'].iloc[0]) - 1) * 100
    total_growth = df_yearly['Enrolled'].iloc[-1] - df_yearly['Enrolled'].iloc[0]
    
    st.info(f"""
    **📊 Análisis de Crecimiento:**
    La matrícula ha crecido un **{enrollment_growth:.1f}%** en el período analizado, 
    pasando de **{df_yearly['Enrolled'].iloc[0]:,}** a **{df_yearly['Enrolled'].iloc[-1]:,}** estudiantes 
    (un incremento de **{total_growth:,}** estudiantes).
    """)
    
    st.markdown("---")
    
    # Embudo de admisión
    st.subheader("🎯 Embudo del Proceso de Admisión")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=df_yearly['Year'], 
            y=df_yearly['Applications'],
            name='Aplicaciones',
            mode='lines+markers',
            line=dict(color='#457B9D', width=3),
            fill='tonexty',
            fillcolor='rgba(69, 123, 157, 0.2)'
        ))
        
        fig3.add_trace(go.Scatter(
            x=df_yearly['Year'], 
            y=df_yearly['Admitted'],
            name='Admitidos',
            mode='lines+markers',
            line=dict(color='#F4A261', width=3),
            fill='tonexty',
            fillcolor='rgba(244, 162, 97, 0.2)'
        ))
        
        fig3.add_trace(go.Scatter(
            x=df_yearly['Year'], 
            y=df_yearly['Enrolled'],
            name='Matriculados',
            mode='lines+markers',
            line=dict(color='#2A9D8F', width=3),
            fill='tonexty',
            fillcolor='rgba(42, 157, 143, 0.2)'
        ))
        
        fig3.update_layout(
            height=400,
            xaxis_title="<b>Año</b>",
            yaxis_title="<b>Número de Estudiantes</b>",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Tasas de Conversión")
        
        conv_admission = (df_yearly['Admitted'].sum() / df_yearly['Applications'].sum() * 100)
        conv_enrollment = (df_yearly['Enrolled'].sum() / df_yearly['Admitted'].sum() * 100)
        conv_total = (df_yearly['Enrolled'].sum() / df_yearly['Applications'].sum() * 100)
        
        st.metric("📝 → ✅ Aplicación a Admisión", f"{conv_admission:.1f}%")
        st.metric("✅ → 🎓 Admisión a Matrícula", f"{conv_enrollment:.1f}%")
        st.metric("📝 → 🎓 Conversión Total", f"{conv_total:.1f}%")
        
        st.markdown(f"""
        **Interpretación:**
        
        De cada **100 aplicantes**:
        - **{int(conv_admission)}** son admitidos
        - **{int(conv_total)}** se matriculan finalmente
        
        La tasa de matrícula sobre admitidos del **{conv_enrollment:.0f}%** indica 
        un alto nivel de aceptación de las ofertas.
        """)

# ==================== TAB 2: ANÁLISIS COMPARATIVO ====================
with tab2:
    st.header("🆚 Análisis Comparativo Entre Períodos")
    
    # Filtro para comparación
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("#### Configura tu análisis comparativo")
    with col2:
        comparison_years = st.multiselect(
            "Años a comparar:",
            options=sorted(df['Year'].unique()),
            default=[2015, 2024],
            key="comparison_years"
        )
    with col3:
        comparison_metric = st.selectbox(
            "Métrica principal:",
            options=['Retention Rate (%)', 'Student Satisfaction (%)', 'Enrolled'],
            format_func=lambda x: {
                'Retention Rate (%)': 'Retención',
                'Student Satisfaction (%)': 'Satisfacción',
                'Enrolled': 'Matrícula'
            }[x],
            key="comparison_metric"
        )
    
    if len(comparison_years) < 2:
        st.warning("⚠️ Selecciona al menos 2 años para realizar la comparación")
    else:
        df_comparison = df[df['Year'].isin(comparison_years)]
        
        # Comparación Spring vs Fall
        st.subheader("📚 Comparación: Período Spring vs Fall")
        
        df_term = df_comparison.groupby('Term').agg({
            'Retention Rate (%)': 'mean',
            'Student Satisfaction (%)': 'mean',
            'Enrolled': 'sum',
            'Applications': 'sum',
            'Admitted': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig4 = go.Figure()
            
            metrics = ['Retention Rate (%)', 'Student Satisfaction (%)']
            colors = ['#0077B6', '#E63946']
            
            for idx, metric in enumerate(metrics):
                fig4.add_trace(go.Bar(
                    name=metric.replace(' (%)', '').replace('Student ', ''),
                    x=df_term['Term'],
                    y=df_term[metric],
                    marker_color=colors[idx],
                    text=df_term[metric].round(1),
                    textposition='outside',
                    texttemplate='%{text}%'
                ))
            
            fig4.update_layout(
                title="<b>Métricas de Calidad por Período</b>",
                barmode='group',
                height=400,
                xaxis_title="<b>Período Académico</b>",
                yaxis_title="<b>Porcentaje (%)</b>",
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            fig5 = px.pie(
                df_term,
                values='Enrolled',
                names='Term',
                title='<b>Distribución de Matrícula</b>',
                hole=0.5,
                color_discrete_sequence=['#2A9D8F', '#F4A261']
            )
            
            fig5.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=14
            )
            
            fig5.update_layout(height=400)
            
            st.plotly_chart(fig5, use_container_width=True)
        
        # Análisis de diferencias
        if len(df_term) == 2:
            spring = df_term[df_term['Term'] == 'Spring'].iloc[0]
            fall = df_term[df_term['Term'] == 'Fall'].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                diff_retention = fall['Retention Rate (%)'] - spring['Retention Rate (%)']
                st.metric(
                    "📊 Diferencia en Retención",
                    f"{abs(diff_retention):.2f}%",
                    delta="Fall vs Spring" if diff_retention > 0 else "Spring vs Fall"
                )
            
            with col2:
                diff_satisfaction = fall['Student Satisfaction (%)'] - spring['Student Satisfaction (%)']
                st.metric(
                    "😊 Diferencia en Satisfacción",
                    f"{abs(diff_satisfaction):.2f}%",
                    delta="Fall vs Spring" if diff_satisfaction > 0 else "Spring vs Fall"
                )
            
            with col3:
                diff_enrolled = fall['Enrolled'] - spring['Enrolled']
                st.metric(
                    "👥 Diferencia en Matrícula",
                    f"{abs(int(diff_enrolled)):,}",
                    delta="Fall vs Spring" if diff_enrolled > 0 else "Spring vs Fall"
                )
            
            st.info("""
            **💡 Conclusión:** Los datos muestran patrones muy similares entre ambos períodos académicos, 
            lo que indica **consistencia y estabilidad** en los procesos institucionales a lo largo del año.
            Esto facilita la planificación y asignación de recursos de manera equilibrada.
            """)
        
        st.markdown("---")
        
        # Comparación año a año
        st.subheader("📅 Evolución de la Métrica Seleccionada")
        
        df_year_comparison = df_comparison.groupby(['Year', 'Term']).agg({
            comparison_metric: 'mean' if '%' in comparison_metric else 'sum'
        }).reset_index()
        
        fig6 = px.line(
            df_year_comparison,
            x='Year',
            y=comparison_metric,
            color='Term',
            markers=True,
            title=f"<b>Evolución de {comparison_metric.replace(' (%)', '').replace('Student ', '')}</b>",
            color_discrete_map={'Spring': '#2A9D8F', 'Fall': '#F4A261'}
        )
        
        fig6.update_traces(line=dict(width=3), marker=dict(size=10))
        fig6.update_layout(
            height=450,
            xaxis_title="<b>Año</b>",
            yaxis_title=f"<b>{comparison_metric}</b>",
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig6, use_container_width=True)

# ==================== TAB 3: DEPARTAMENTOS ====================
with tab3:
    st.header("🏢 Análisis Detallado por Departamento")
    
    # Filtros para departamentos
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Analiza el desempeño departamental")
    with col2:
        dept_year_filter = st.select_slider(
            "Período de análisis:",
            options=sorted(df['Year'].unique()),
            value=(2015, 2024),
            key="dept_year_filter"
        )
    
    # Filtrar datos
    df_dept = df[(df['Year'] >= dept_year_filter[0]) & (df['Year'] <= dept_year_filter[1])]
    
    # Preparar datos departamentales
    dept_data = pd.DataFrame({
        'Departamento': ['Ingeniería', 'Negocios', 'Artes', 'Ciencias'],
        'Total Matriculados': [
            df_dept['Engineering Enrolled'].sum(),
            df_dept['Business Enrolled'].sum(),
            df_dept['Arts Enrolled'].sum(),
            df_dept['Science Enrolled'].sum()
        ],
        'Icono': ['⚙️', '💼', '🎨', '🔬']
    })
    
    dept_data['Porcentaje'] = (dept_data['Total Matriculados'] / dept_data['Total Matriculados'].sum() * 100).round(1)
    dept_data = dept_data.sort_values('Total Matriculados', ascending=False)
    
    # Tarjetas de departamentos
    st.subheader("📊 Resumen por Departamento")
    
    cols = st.columns(4)
    for idx, row in dept_data.iterrows():
        with cols[dept_data.index.get_loc(idx)]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; color: white; text-align: center;'>
                <h1>{row['Icono']}</h1>
                <h3>{row['Departamento']}</h3>
                <h2>{row['Total Matriculados']:,}</h2>
                <p style='font-size: 18px;'>{row['Porcentaje']}% del total</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizaciones departamentales
    col1, col2 = st.columns(2)
    
    with col1:
        fig7 = px.bar(
            dept_data,
            x='Departamento',
            y='Total Matriculados',
            title='<b>Matrícula por Departamento</b>',
            color='Total Matriculados',
            color_continuous_scale='Viridis',
            text='Total Matriculados'
        )
        
        fig7.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            textfont_size=14
        )
        
        fig7.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="<b>Departamento</b>",
            yaxis_title="<b>Estudiantes Matriculados</b>",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        fig8 = go.Figure(data=[go.Pie(
            labels=dept_data['Departamento'],
            values=dept_data['Total Matriculados'],
            hole=0.5,
            marker=dict(colors=['#0077B6', '#E63946', '#2A9D8F', '#F4A261']),
            textinfo='label+percent',
            textposition='outside',
            textfont_size=12
        )])
        
        fig8.update_layout(
            title='<b>Distribución Porcentual</b>',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig8, use_container_width=True)
    
    st.markdown("---")
    
    # Evolución temporal por departamento
    st.subheader("📈 Tendencias de Matrícula Departamental")
    
    df_dept_trend = df_dept.groupby('Year').agg({
        'Engineering Enrolled': 'sum',
        'Business Enrolled': 'sum',
        'Arts Enrolled': 'sum',
        'Science Enrolled': 'sum'
    }).reset_index()
    
    fig9 = go.Figure()
    
    departments = [
        ('Engineering Enrolled', 'Ingeniería ⚙️', '#0077B6'),
        ('Business Enrolled', 'Negocios 💼', '#E63946'),
        ('Arts Enrolled', 'Artes 🎨', '#2A9D8F'),
        ('Science Enrolled', 'Ciencias 🔬', '#F4A261')
    ]
    
    for col, name, color in departments:
        fig9.add_trace(go.Scatter(
            x=df_dept_trend['Year'],
            y=df_dept_trend[col],
            name=name,
            mode='lines+markers',
            line=dict(width=3, color=color),
            marker=dict(size=8)
        ))
    
    fig9.update_layout(
        height=450,
        xaxis_title="<b>Año</b>",
        yaxis_title="<b>Estudiantes Matriculados</b>",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig9, use_container_width=True)
    
    # Análisis de crecimiento departamental
    st.subheader("📊 Análisis de Crecimiento Departamental")
    
    growth_data = []
    for col, name, _ in departments:
        initial = df_dept_trend[col].iloc[0]
        final = df_dept_trend[col].iloc[-1]
        growth = ((final / initial) - 1) * 100 if initial > 0 else 0
        growth_data.append({
            'Departamento': name.split()[0],
            'Crecimiento (%)': round(growth, 1),
            'Valor Inicial': initial,
            'Valor Final': final,
            'Incremento': final - initial
        })
    
    growth_df = pd.DataFrame(growth_data).sort_values('Crecimiento (%)', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig10 = px.bar(
            growth_df,
            x='Departamento',
            y='Crecimiento (%)',
            title='<b>Porcentaje de Crecimiento por Departamento</b>',
            color='Crecimiento (%)',
            color_continuous_scale='RdYlGn',
            text='Crecimiento (%)'
        )
        
        fig10.update_traces(texttemplate='%{text}%', textposition='outside')
        fig10.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)')
        
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Rankings")
        st.markdown("**Mayor Matrícula:**")
        st.markdown(f"🥇 {dept_data.iloc[0]['Departamento']}: {dept_data.iloc[0]['Total Matriculados']:,}")
        
        st.markdown("**Mayor Crecimiento:**")
        st.markdown(f"📈 {growth_df.iloc[0]['Departamento']}: +{growth_df.iloc[0]['Crecimiento (%)']}%")
        
        st.markdown("**Más Estable:**")
        stability = growth_df.loc[growth_df['Crecimiento (%)'].abs().idxmin()]
        st.markdown(f"⚖️ {stability['Departamento']}: {stability['Crecimiento (%)']}%")

# ==================== TAB 4: ANÁLISIS PROFUNDO ====================
with tab4:
    st.header("🎯 Análisis Profundo e Insights Estratégicos")
    
    # Selector de tipo de análisis
    analysis_type = st.radio(
        "Selecciona el tipo de análisis:",
        options=["📊 Resumen Ejecutivo", "🔍 Análisis Predictivo", "💡 Recomendaciones"],
        horizontal=True
    )
    
    if analysis_type == "📊 Resumen Ejecutivo":
        st.subheader("📋 Resumen Ejecutivo Institucional")
        
        # Métricas clave
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📝 Proceso de Admisión")
            total_apps = df['Applications'].sum()
            total_admitted = df['Admitted'].sum()
            total_enrolled = df['Enrolled'].sum()
            
            st.metric("Aplicaciones Totales", f"{total_apps:,}")
            st.metric("Estudiantes Admitidos", f"{total_admitted:,}")
            st.metric("Estudiantes Matriculados", f"{total_enrolled:,}")
        
        with col2:
            st.markdown("### 📊 Indicadores de Calidad")
            avg_retention = df['Retention Rate (%)'].mean()
            avg_satisfaction = df['Student Satisfaction (%)'].mean()
            
            st.metric("Retención Promedio", f"{avg_retention:.1f}%")
            st.metric("Satisfacción Promedio", f"{avg_satisfaction:.1f}%")
            
            # Calcular tendencia
            df_trend_quality = df.groupby('Year').agg({
                'Retention Rate (%)': 'mean',
                'Student Satisfaction (%)': 'mean'
            })
            trend = "Positiva ✅" if df_trend_quality['Retention Rate (%)'].is_monotonic_increasing else "Estable 📊"
            st.metric("Tendencia General", trend)
        
        with col3:
            st.markdown("### 🏢 Distribución Académica")
            total_eng = df['Engineering Enrolled'].sum()
            total_bus = df['Business Enrolled'].sum()
            total_arts = df['Arts Enrolled'].sum()
            total_sci = df['Science Enrolled'].sum()
            
            max_dept = max([(total_eng, "Ingeniería"), (total_bus, "Negocios"), 
                           (total_arts, "Artes"), (total_sci, "Ciencias")])
            
            st.metric("Departamento Líder", max_dept[1])
            st.metric("Estudiantes", f"{max_dept[0]:,}")
            st.metric("Total Departamentos", "4")
        
        st.markdown("---")
        
        # Embudo completo
        st.subheader("🎯 Embudo Completo de Conversión")
        
        funnel_data = pd.DataFrame({
            'Etapa': ['Aplicaciones Recibidas', 'Estudiantes Admitidos', 'Estudiantes Matriculados'],
            'Cantidad': [total_apps, total_admitted, total_enrolled],
            'Porcentaje': [100, (total_admitted/total_apps*100), (total_enrolled/total_apps*100)]
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_funnel = go.Figure()
            
            fig_funnel.add_trace(go.Funnel(
                name='Conversión',
                y=funnel_data['Etapa'],
                x=funnel_data['Cantidad'],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=['#0077B6', '#2A9D8F', '#F4A261'],
                    line=dict(width=2, color='white')
                ),
                connector=dict(line=dict(color='gray', dash='dot', width=2))
            ))
            
            fig_funnel.update_layout(
                title="<b>Proceso de Admisión y Matrícula</b>",
                height=400
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Métricas del Embudo")
            st.metric("Tasa de Admisión", f"{(total_admitted/total_apps*100):.1f}%")
            st.metric("Tasa de Matrícula", f"{(total_enrolled/total_admitted*100):.1f}%")
            st.metric("Conversión Total", f"{(total_enrolled/total_apps*100):.1f}%")
            
            st.markdown(f"""
            **Interpretación:**
            
            Por cada 100 aplicantes:
            - **{int(total_admitted/total_apps*100)}** son admitidos
            - **{int(total_enrolled/total_apps*100)}** se matriculan
            
            La tasa de conversión final es **excelente** 
            y muestra alta eficiencia del proceso.
            """)
        
        st.markdown("---")
        
        # Tabla de evolución histórica
        st.subheader("📅 Evolución Histórica Año por Año")
        
        historical_data = df.groupby('Year').agg({
            'Applications': 'sum',
            'Admitted': 'sum',
            'Enrolled': 'sum',
            'Retention Rate (%)': 'mean',
            'Student Satisfaction (%)': 'mean'
        }).reset_index()
        
        historical_data.columns = ['Año', 'Aplicaciones', 'Admitidos', 'Matriculados', 
                                   'Retención (%)', 'Satisfacción (%)']
        
        # Formatear números
        historical_data['Retención (%)'] = historical_data['Retención (%)'].round(1)
        historical_data['Satisfacción (%)'] = historical_data['Satisfacción (%)'].round(1)
        
        st.dataframe(
            historical_data.style.background_gradient(subset=['Retención (%)', 'Satisfacción (%)'], cmap='RdYlGn'),
            use_container_width=True,
            height=400
        )
        
        # Descarga de datos
        csv = historical_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Resumen Histórico (CSV)",
            data=csv,
            file_name='resumen_historico_universidad.csv',
            mime='text/csv',
        )
    
    elif analysis_type == "🔍 Análisis Predictivo":
        st.subheader("🔮 Proyecciones y Análisis de Tendencias")
        
        st.info("📊 Este análisis muestra las tendencias actuales y proyecciones basadas en datos históricos")
        
        # Análisis de tendencias
        df_yearly_pred = df.groupby('Year').agg({
            'Retention Rate (%)': 'mean',
            'Student Satisfaction (%)': 'mean',
            'Enrolled': 'sum'
        }).reset_index()
        
        # Calcular tasas de crecimiento
        retention_growth_rate = (df_yearly_pred['Retention Rate (%)'].iloc[-1] - 
                                df_yearly_pred['Retention Rate (%)'].iloc[0]) / len(df_yearly_pred)
        satisfaction_growth_rate = (df_yearly_pred['Student Satisfaction (%)'].iloc[-1] - 
                                   df_yearly_pred['Student Satisfaction (%)'].iloc[0]) / len(df_yearly_pred)
        enrollment_growth_rate = (df_yearly_pred['Enrolled'].iloc[-1] - 
                                 df_yearly_pred['Enrolled'].iloc[0]) / df_yearly_pred['Enrolled'].iloc[0] / len(df_yearly_pred)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📈 Crecimiento Anual - Retención",
                f"+{retention_growth_rate:.2f}%",
                delta="por año"
            )
        
        with col2:
            st.metric(
                "😊 Crecimiento Anual - Satisfacción",
                f"+{satisfaction_growth_rate:.2f}%",
                delta="por año"
            )
        
        with col3:
            st.metric(
                "👥 Crecimiento Anual - Matrícula",
                f"+{enrollment_growth_rate*100:.1f}%",
                delta="por año"
            )
        
        st.markdown("---")
        
        # Proyección simple para próximos 3 años
        st.subheader("🎯 Proyección para los Próximos 3 Años")
        
        last_year = df_yearly_pred['Year'].iloc[-1]
        future_years = [last_year + 1, last_year + 2, last_year + 3]
        
        projected_retention = [
            df_yearly_pred['Retention Rate (%)'].iloc[-1] + retention_growth_rate * i 
            for i in range(1, 4)
        ]
        projected_satisfaction = [
            df_yearly_pred['Student Satisfaction (%)'].iloc[-1] + satisfaction_growth_rate * i 
            for i in range(1, 4)
        ]
        projected_enrollment = [
            int(df_yearly_pred['Enrolled'].iloc[-1] * (1 + enrollment_growth_rate) ** i)
            for i in range(1, 4)
        ]
        
        projection_df = pd.DataFrame({
            'Año': future_years,
            'Retención Proyectada (%)': [round(x, 1) for x in projected_retention],
            'Satisfacción Proyectada (%)': [round(x, 1) for x in projected_satisfaction],
            'Matrícula Proyectada': projected_enrollment
        })
        
        # Gráfico de proyección
        fig_proj = go.Figure()
        
        # Datos históricos
        fig_proj.add_trace(go.Scatter(
            x=df_yearly_pred['Year'],
            y=df_yearly_pred['Retention Rate (%)'],
            name='Retención (Histórico)',
            mode='lines+markers',
            line=dict(color='#0077B6', width=3)
        ))
        
        # Proyección
        fig_proj.add_trace(go.Scatter(
            x=[last_year] + future_years,
            y=[df_yearly_pred['Retention Rate (%)'].iloc[-1]] + projected_retention,
            name='Retención (Proyección)',
            mode='lines+markers',
            line=dict(color='#0077B6', width=3, dash='dash')
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=df_yearly_pred['Year'],
            y=df_yearly_pred['Student Satisfaction (%)'],
            name='Satisfacción (Histórico)',
            mode='lines+markers',
            line=dict(color='#E63946', width=3)
        ))
        
        fig_proj.add_trace(go.Scatter(
            x=[last_year] + future_years,
            y=[df_yearly_pred['Student Satisfaction (%)'].iloc[-1]] + projected_satisfaction,
            name='Satisfacción (Proyección)',
            mode='lines+markers',
            line=dict(color='#E63946', width=3, dash='dash')
        ))
        
        fig_proj.update_layout(
            title="<b>Proyección de Indicadores de Calidad</b>",
            height=450,
            xaxis_title="<b>Año</b>",
            yaxis_title="<b>Porcentaje (%)</b>",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_proj, use_container_width=True)
        
        st.dataframe(projection_df, use_container_width=True)
        
        st.warning("""
        ⚠️ **Nota importante:** Estas proyecciones son estimaciones basadas en tendencias históricas lineales 
        y asumen que las condiciones actuales se mantendrán. Factores externos pueden alterar estas predicciones.
        """)
    
    else:  # Recomendaciones
        st.subheader("💡 Recomendaciones Estratégicas Basadas en Datos")
        
        # Análisis para recomendaciones
        df_analysis = df.groupby('Year').agg({
            'Retention Rate (%)': 'mean',
            'Student Satisfaction (%)': 'mean',
            'Enrolled': 'sum',
            'Engineering Enrolled': 'sum',
            'Business Enrolled': 'sum',
            'Arts Enrolled': 'sum',
            'Science Enrolled': 'sum'
        })
        
        # Identificar áreas de oportunidad
        st.markdown("### 🎯 Áreas de Fortaleza")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **✅ Retención Estudiantil**
            - Tendencia positiva sostenida
            - Actualmente en niveles excelentes (>88%)
            - Mejora continua año tras año
            
            **Recomendación:** Mantener y documentar las prácticas actuales que generan 
            estos resultados para replicarlas en áreas de mejora.
            """)
        
        with col2:
            st.success("""
            **✅ Satisfacción Estudiantil**
            - Crecimiento constante
            - Niveles superiores al 85%
            - Alta correlación con retención
            
            **Recomendación:** Realizar estudios cualitativos para identificar los factores 
            específicos que más contribuyen a la satisfacción.
            """)
        
        st.markdown("---")
        st.markdown("### 🔍 Oportunidades de Mejora")
        
        # Identificar departamento con menor crecimiento
        dept_growth = {
            'Ingeniería': ((df_analysis['Engineering Enrolled'].iloc[-1] / 
                          df_analysis['Engineering Enrolled'].iloc[0]) - 1) * 100,
            'Negocios': ((df_analysis['Business Enrolled'].iloc[-1] / 
                        df_analysis['Business Enrolled'].iloc[0]) - 1) * 100,
            'Artes': ((df_analysis['Arts Enrolled'].iloc[-1] / 
                      df_analysis['Arts Enrolled'].iloc[0]) - 1) * 100,
            'Ciencias': ((df_analysis['Science Enrolled'].iloc[-1] / 
                        df_analysis['Science Enrolled'].iloc[0]) - 1) * 100
        }
        
        min_growth_dept = min(dept_growth.items(), key=lambda x: x[1])
        max_growth_dept = max(dept_growth.items(), key=lambda x: x[1])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning(f"""
            **⚠️ Departamento de {min_growth_dept[0]}**
            - Crecimiento del {min_growth_dept[1]:.1f}%
            - Menor crecimiento relativo
            
            **Recomendaciones:**
            1. Revisar oferta de programas académicos
            2. Actualizar curriculum según demanda del mercado
            3. Mejorar estrategias de marketing del departamento
            4. Establecer alianzas con sector productivo
            5. Evaluar infraestructura y recursos disponibles
            """)
        
        with col2:
            st.info(f"""
            **📚 Benchmarking Interno**
            
            El departamento de **{max_growth_dept[0]}** ha crecido **{max_growth_dept[1]:.1f}%**, 
            siendo el más exitoso.
            
            **Recomendación:** Analizar y replicar las mejores prácticas de este departamento 
            en las áreas con menor desempeño. Considerar:
            - Estrategias de reclutamiento
            - Calidad de profesores
            - Recursos tecnológicos
            - Vinculación con la industria
            """)
        
        st.markdown("---")
        st.markdown("### 🚀 Plan de Acción Sugerido")
        
        action_plan = pd.DataFrame({
            'Prioridad': ['🔴 Alta', '🟡 Media', '🟢 Baja'],
            'Área': ['Crecimiento Departamental', 'Proceso de Admisión', 'Infraestructura'],
            'Acción Recomendada': [
                f'Fortalecer departamento de {min_growth_dept[0]} con nuevos programas',
                'Optimizar conversión de admitidos a matriculados',
                'Expandir capacidad para sostener crecimiento'
            ],
            'Impacto Esperado': ['Alto - +15% matrícula', 'Medio - +5% conversión', 'Alto - Sostenibilidad'],
            'Plazo': ['12-18 meses', '6-12 meses', '18-24 meses']
        })
        
        st.dataframe(action_plan, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 📊 Indicadores de Seguimiento Recomendados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **KPIs Trimestrales:**
            - Tasa de retención por cohorte
            - NPS (Net Promoter Score)
            - Tasa de graduación
            - Empleabilidad egresados
            """)
        
        with col2:
            st.markdown("""
            **KPIs Semestrales:**
            - Satisfacción por departamento
            - Ratio estudiante-profesor
            - Inversión en infraestructura
            - Publicaciones académicas
            """)
        
        with col3:
            st.markdown("""
            **KPIs Anuales:**
            - Crecimiento de matrícula
            - Ranking institucional
            - Acreditaciones obtenidas
            - ROI de programas
            """)

# Datos completos (al final)
st.markdown("---")
st.header("🗂️ Explorador de Datos Completo")

with st.expander("📋 Ver todos los datos del dataset", expanded=False):
    st.dataframe(df, use_container_width=True, height=400)
    
    # Estadísticas descriptivas
    st.subheader("📊 Estadísticas Descriptivas")
    st.dataframe(df.describe(), use_container_width=True)
    
    # Descarga completa
    csv_full = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Dataset Completo (CSV)",
        data=csv_full,
        file_name='university_student_data_complete.csv',
        mime='text/csv',
    )

# Footer mejorado
st.markdown("---")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown("**Universidad de la Costa**")
    st.markdown("Departamento de Ciencias de la Computación y Electrónica")

with col2:
    st.markdown("**Curso:** Minería de Datos")
    st.markdown("**Docente:** José Escorcia-Gutierrez, Ph.D.")

with col3:
    st.markdown("**Año:** 2025")
    st.markdown("**Actividad 1**")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><b>Desarrollado por:</b> Alejandro Escorcia & Ashley Urueta</p>
    <p>Dashboard Interactivo de Análisis Universitario | Visualización de Datos y Despliegue</p>
</div>
""", unsafe_allow_html=True)