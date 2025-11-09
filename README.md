# 🎓 Dashboard Analítico Universitario

## 📋 Descripción del Proyecto

Dashboard interactivo desarrollado para el análisis integral de datos universitarios, incluyendo procesos de admisión, matrícula, tasas de retención y satisfacción estudiantil. El sistema permite visualizar tendencias históricas, realizar comparaciones entre períodos académicos y departamentos, y generar insights estratégicos para la toma de decisiones institucionales.

---

## 👥 Equipo de Desarrollo

| Nombre | Rol |
|--------|-----|
| **Alejandro Escorcia** | Desarrollador & Analista de Datos |
| **Ashley Urueta** | Desarrolladora & Diseñadora de Visualizaciones |

**Institución:** Universidad de la Costa  
**Curso:** Minería de Datos (Data Mining)  
**Docente:** José Escorcia-Gutierrez, Ph.D.  
**Departamento:** Ciencias de la Computación y Electrónica

---

## 🎯 Características Principales

### 📊 Indicadores Clave (KPIs)
- **Retención Promedio**: Seguimiento de tasa de permanencia estudiantil
- **Satisfacción Estudiantil**: Medición de experiencia universitaria
- **Total de Matriculados**: Evolución de población estudiantil
- **Tasa de Admisión**: Análisis de selectividad institucional
- **Tendencias de Crecimiento**: Proyecciones y análisis predictivo

### 🔍 Filtros Contextuales Inteligentes
A diferencia de los dashboards tradicionales con panel lateral fijo, este sistema implementa **filtros contextuales** que aparecen solo donde son relevantes:

- **Filtros Temporales**: Selectores de rango de años y períodos académicos
- **Filtros Departamentales**: Sliders y selectores específicos para análisis por área
- **Filtros Comparativos**: Selección múltiple para análisis año contra año
- **Filtros Dinámicos**: Se adaptan al contenido de cada pestaña

### 📈 Módulos de Análisis

#### 1. **Evolución Temporal**
- Gráficos de línea con tendencias de retención y satisfacción
- Análisis de crecimiento de matrícula estudiantil
- Embudo de conversión (Aplicaciones → Admisiones → Matrícula)
- Interpretaciones automáticas de tendencias
- Filtro de rango temporal ajustable

#### 2. **Análisis Comparativo**
- Comparación Spring vs Fall con métricas de calidad
- Distribución porcentual de matrícula por período
- Análisis de diferencias y patrones estacionales
- Evolución por período académico
- Filtros de años múltiples para comparación personalizada

#### 3. **Análisis Departamental**
- Tarjetas visuales con resumen por departamento
- Gráficos de barras y circulares de distribución
- Evolución temporal de cada área académica
- Análisis de crecimiento departamental
- Rankings de desempeño
- Filtro temporal específico para análisis departamental

#### 4. **Análisis Profundo**
Tres sub-módulos especializados:

- **📊 Resumen Ejecutivo**
  - Métricas consolidadas del proceso de admisión
  - Embudo completo de conversión
  - Tabla histórica con evolución año por año
  - Descarga de resumen ejecutivo

- **🔍 Análisis Predictivo**
  - Cálculo de tasas de crecimiento anuales
  - Proyecciones para los próximos 3 años
  - Gráficos con datos históricos y proyectados
  - Análisis de tendencias

- **💡 Recomendaciones Estratégicas**
  - Identificación de áreas de fortaleza
  - Detección de oportunidades de mejora
  - Plan de acción priorizado
  - KPIs de seguimiento recomendados
  - Benchmarking interno

### 🎨 Características de Diseño

- **Interfaz Moderna**: Diseño limpio con gradientes y colores corporativos
- **Tarjetas Interactivas**: Cards con información departamental
- **Gráficos Profesionales**: Visualizaciones con Plotly de alta calidad
- **Tooltips Informativos**: Información contextual al pasar el mouse
- **Responsive**: Adaptable a diferentes tamaños de pantalla
- **Modo Expandible**: Secciones colapsables para mejor organización
- **Descarga de Datos**: Exportación de tablas filtradas en CSV

---

## 📊 Estructura de Datos

### Dataset: `university_student_data.csv`

| Column | Tipo | Descripción |
|--------|------|-------------|
| **Year** | int | Año académico (2015-2024) |
| **Term** | string | Período académico (Spring/Fall) |
| **Applications** | int | Número de aplicaciones recibidas |
| **Admitted** | int | Estudiantes admitidos |
| **Enrolled** | int | Estudiantes matriculados |
| **Retention Rate (%)** | float | Tasa de retención porcentual |
| **Student Satisfaction (%)** | float | Satisfacción estudiantil porcentual |
| **Engineering Enrolled** | int | Matriculados en Ingeniería |
| **Business Enrolled** | int | Matriculados en Negocios |
| **Arts Enrolled** | int | Matriculados en Artes |
| **Science Enrolled** | int | Matriculados en Ciencias |

**Período de Datos:** 2015 - 2024  
**Total de Registros:** 20 entradas (10 años × 2 períodos)  
**Departamentos:** 4 áreas académicas

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git para control de versiones

### Instalación Paso a Paso

1. **Clonar el repositorio:**
```bash
git clone https://github.com/[tu-usuario]/university-dashboard.git
cd university-dashboard
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Verificar archivos necesarios:**
```
university-dashboard/
├── app.py
├── university_student_data.csv
├── requirements.txt
└── README.md
```

5. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```

6. **Acceder al dashboard:**
- Se abrirá automáticamente en tu navegador
- URL: `http://localhost:8501`

---

## ☁️ Despliegue en Streamlit Cloud

### Guía Completa de Despliegue

#### Paso 1: Preparar el Repositorio

1. Asegúrate de que todos los archivos estén en tu repositorio de GitHub:
   - `app.py`
   - `university_student_data.csv`
   - `requirements.txt`
   - `README.md`

2. Verifica que el archivo CSV esté en la raíz del proyecto

3. Commit y push de todos los cambios:
```bash
git add .
git commit -m "Dashboard universitario listo para deploy"
git push origin main
```

#### Paso 2: Configurar Streamlit Cloud

1. Visita [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Autoriza a Streamlit a acceder a tus repositorios
4. Click en **"New app"**

#### Paso 3: Configuración del Deploy

Completa el formulario con:

- **Repository:** Selecciona tu repositorio
- **Branch:** `main` o `master`
- **Main file path:** `app.py`
- **App URL (opcional):** Personaliza la URL

#### Paso 4: Deploy

1. Click en **"Deploy!"**
2. Espera 2-5 minutos mientras se instalan las dependencias
3. Una vez completado, obtendrás una URL pública

#### Paso 5: Verificación

- ✅ Todos los gráficos cargan correctamente
- ✅ Los filtros funcionan sin errores
- ✅ Las métricas se calculan apropiadamente
- ✅ Las descargas de CSV funcionan

### Solución de Problemas

**Error: "FileNotFoundError: university_student_data.csv"**
- Solución: Verifica que el CSV esté en la raíz del repositorio
- Revisa que el nombre del archivo sea exacto (case-sensitive)

**Error: "ModuleNotFoundError"**
- Solución: Verifica que `requirements.txt` esté actualizado
- Asegúrate de incluir todas las versiones necesarias

**Error: "App crashed"**
- Solución: Revisa los logs en Streamlit Cloud
- Verifica que no haya rutas absolutas en el código

---

## 📁 Estructura del Proyecto

```
university-dashboard/
│
├── 📄 app.py                          # Aplicación principal de Streamlit
│   ├── Configuración de página
│   ├── Carga de datos con cache
│   ├── KPIs principales
│   ├── Tab 1: Evolución Temporal
│   ├── Tab 2: Análisis Comparativo
│   ├── Tab 3: Análisis Departamental
│   ├── Tab 4: Análisis Profundo
│   └── Footer y metadatos
│
├── 📊 university_student_data.csv    # Dataset con datos universitarios
│   └── 20 registros (2015-2024, Spring/Fall)
│
├── 📋 requirements.txt                # Dependencias Python
│   ├── streamlit==1.28.0
│   ├── pandas==2.0.3
│   └── plotly==5.17.0
│
└── 📖 README.md                       # Este archivo (documentación)
```

---

## 🔍 Hallazgos Clave del Análisis

### 📈 Tendencias Positivas Identificadas

1. **Crecimiento Sostenido en Retención**
   - Incremento del 85% (2015) al 90% (2024)
   - Mejora de +5 puntos porcentuales
   - Tendencia ascendente consistente

2. **Mejora en Satisfacción Estudiantil**
   - Aumento del 78% (2015) al 88% (2024)
   - Incremento de +10 puntos porcentuales
   - Correlación positiva con retención

3. **Expansión de Matrícula**
   - De 600 a 800 estudiantes por período
   - Crecimiento del 33% en 10 años
   - Incremento sostenido año tras año

### 🏢 Análisis Departamental

| Departamento | Matrícula Total | Porcentaje | Tendencia |
|--------------|----------------|------------|-----------|
| Ingeniería | ~5,000 | ~38% | ↗️ Crecimiento fuerte |
| Negocios | ~3,700 | ~28% | ↗️ Crecimiento moderado |
| Artes | ~2,900 | ~22% | ↗️ Crecimiento estable |
| Ciencias | ~2,400 | ~18% | → Estable |

### 🎯 Proceso de Admisión

- **Tasa de Admisión Promedio:** ~60%
- **Tasa de Matrícula sobre Admitidos:** ~48%
- **Conversión Total (Aplicación → Matrícula):** ~29%
- **Eficiencia del Embudo:** Alta y estable

---

## 💡 Recomendaciones Estratégicas

### 🎯 Prioridad Alta

1. **Fortalecer Departamento de Ciencias**
   - Actualizar curriculum
   - Mejorar infraestructura de laboratorios
   - Establecer alianzas con sector tecnológico
   - **Impacto esperado:** +15% en matrícula

2. **Optimizar Proceso de Admisión**
   - Reducir tiempo de respuesta a aplicantes
   - Mejorar comunicación con admitidos
   - Implementar sistema de seguimiento
   - **Impacto esperado:** +5% en conversión

### 🟡 Prioridad Media

3. **Expandir Capacidad Instalada**
   - Planificar crecimiento de infraestructura
   - Contratar profesores adicionales
   - Mejorar espacios comunes
   - **Plazo:** 18-24 meses

4. **Programa de Retención Proactiva**
   - Identificar estudiantes en riesgo tempranamente
   - Tutorías personalizadas
   - Apoyo académico preventivo

### 🟢 Prioridad Baja

5. **Diversificación de Oferta Académica**
   - Nuevos programas interdisciplinarios
   - Modalidades híbridas y online
   - Microcredenciales y certificaciones

---

## 🛠️ Tecnologías Utilizadas

### Core Technologies

- **[Streamlit](https://streamlit.io/)** `v1.28.0` - Framework de aplicaciones web
  - Componentes interactivos
  - Sistema de cache eficiente
  - Despliegue simplificado

- **[Pandas](https://pandas.pydata.org/)** `v2.0.3` - Análisis de datos
  - Manipulación de DataFrames
  - Agregaciones y transformaciones
  - Estadísticas descriptivas

- **[Plotly](https://plotly.com/python/)** `v5.17.0` - Visualizaciones interactivas
  - Gráficos responsivos
  - Interactividad avanzada
  - Exportación de imágenes

### Python Standard Library

- `csv` - Lectura de archivos CSV
- `datetime` - Manejo de fechas
- `json` - Serialización de datos

---

## 📚 Documentación Adicional

### Guía de Uso del Dashboard

1. **Navegación Principal:** Utiliza las pestañas superiores para cambiar entre módulos
2. **Aplicación de Filtros:** Cada sección tiene sus propios filtros contextuales
3. **Interpretación:** Lee los textos explicativos bajo cada gráfico
4. **Descarga de Datos:** Usa los botones de descarga para exportar información
5. **Exploración:** Pasa el mouse sobre los gráficos para ver detalles

### Mantenimiento y Actualizaciones

Para actualizar los datos:

1. Edita el archivo `university_student_data.csv`
2. Mantén la estructura de columnas
3. Asegura consistencia en formatos
4. Realiza commit y push
5. Streamlit Cloud actualizará automáticamente

---

## 📄 Información Académica

**Actividad:** Actividad 1 - Visualización de Datos y Despliegue de Dashboard  
**Curso:** Minería de Datos (Data Mining)  
**Institución:** Universidad de la Costa  
**Departamento:** Ciencias de la Computación y Electrónica  
**Docente:** José Escorcia-Gutierrez, Ph.D.  
**Año Académico:** 2025  
**Tipo de Trabajo:** Grupal (2-4 integrantes)

---

## 📞 Contacto

**Desarrolladores:**
- Alejandro Escorcia
- Ashley Urueta

**Institución:** Universidad de la Costa  
**Ubicación:** Barranquilla, Atlántico, Colombia

---

## 📝 Licencia

Este proyecto fue desarrollado con fines académicos como parte del curso de Minería de Datos en la Universidad de la Costa. 

**Uso Académico:** Se permite el uso y modificación del código para propósitos educativos citando apropiadamente a los autores.

---

## 🙏 Agradecimientos

- Al profesor José Escorcia-Gutierrez, Ph.D. por la guía y enseñanzas
- A la Universidad de la Costa por proporcionar el entorno de aprendizaje
- A la comunidad de Streamlit por la excelente documentación
- A todos los recursos open-source utilizados en este proyecto

---

<div align="center">

**Desarrollado con 💙 por estudiantes de Data Mining**

Universidad de la Costa | 2025

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

</div>