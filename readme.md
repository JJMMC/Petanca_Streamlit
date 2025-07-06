# 🎯 Petanca Tournament Manager

Una aplicación web desarrollada en **Streamlit** para gestionar torneos de petanca de manera sencilla y eficiente. Permite registrar jugadores, partidas y visualizar estadísticas detalladas con gráficos interactivos.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.1-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características Principales

- **👤 Gestión de Jugadores**: Registro y administración de participantes
- **⚔️ Registro de Partidas**: Sistema completo para registrar resultados entre equipos
- **📊 Estadísticas Avanzadas**: Visualizaciones interactivas con Altair
- **🏆 Rankings**: Seguimiento de parejas y jugadores más exitosos
- **📱 Interfaz Intuitiva**: Diseño responsive con navegación por menú lateral
- **💾 Exportación**: Funcionalidad para exportar datos a Excel

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Streamlit 1.44.1** - Framework para aplicaciones web
- **Pandas 2.2.3** - Manipulación y análisis de datos
- **Altair 5.5.0** - Visualizaciones interactivas
- **SQLite** - Base de datos relacional local
- **OpenPyXL** - Exportación a Excel

## 📦 Instalación y Uso

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/JJMMC/Petanca_Streamlit.git
cd Petanca_Streamlit
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
Petanca_Streamlit/
├── app.py              # Aplicación principal y navegación
├── scripts.py          # Funciones de las páginas de la aplicación
├── db_utils.py         # Utilidades y operaciones de base de datos
├── requirements.txt    # Dependencias del proyecto
├── readme.md          # Documentación del proyecto
├── database.db        # Base de datos SQLite (se crea automáticamente)
└── resources/         # Recursos del proyecto
    ├── boule.png      # Icono de la aplicación
    └── users_photo/   # Directorio para fotos de usuarios
```

## 🎮 Funcionalidades Detalladas

### 🏠 Página de Inicio
- Descripción general de la aplicación
- Información sobre las reglas de la petanca

### 👤 Gestión de Jugadores
- ✅ Formulario para agregar jugadores con validación
- ✅ Campos: nombre, apellido, fecha de creación
- ✅ Almacenamiento automático en base de datos
- ✅ Funciones CRUD completas (Create, Read, Update, Delete)

### ⚔️ Registro de Partidas
- ✅ Selección inteligente de 4 jugadores únicos
- ✅ Formación automática de 2 equipos
- ✅ Sistema de puntuación de 0-13 puntos por equipo
- ✅ Determinación automática del ganador
- ✅ Prevención de selección duplicada de jugadores
- ✅ Registro automático con timestamp

### 📊 Estadísticas y Análisis
- **📋 Partidas Detalladas**: Vista completa con equipos y resultados
- **🥇 Pareja Ganadora**: Identificación de la dupla más exitosa
- **🏅 Jugador Estrella**: Ranking individual de victorias
- **📈 Visualizaciones Interactivas**:
  - Distribución de puntos por equipo
  - Historial de victorias por equipo
  - Evolución temporal de duración de partidas
  - Comparación lado a lado de puntuaciones
- **📊 Dashboard**: Resumen con métricas clave del torneo
- **📤 Exportación**: Datos exportables a Excel

## 🗄️ Arquitectura de Base de Datos

Utiliza **SQLite** con esquema relacional optimizado:

```sql
players           # Información de jugadores
├── id (PK)
├── name
├── surname
├── photo_path
└── creation_date

matches           # Registro de partidas
├── id (PK)
├── fecha
├── duracion
├── puntos_equipo1
├── puntos_equipo2
└── ganador

teams             # Equipos por partida
├── id (PK)
├── partida_id (FK)
└── equipo_numero

teams_players     # Relación equipos-jugadores
├── id (PK)
├── equipo_id (FK)
└── jugador_id (FK)
```

### Funciones de Base de Datos Disponibles
- **CRUD Jugadores**: `add_player()`, `get_players()`, `update_player()`, `delete_player()`
- **CRUD Partidas**: `add_match()`, `get_matches()`, `delete_match()`
- **Gestión Equipos**: `add_team()`, `add_team_player()`, `get_teams()`
- **Estadísticas**: `get_matches_with_players()`, `get_pareja_mas_ganadora()`, `get_jugador_mas_ganador()`
- **Utilidades**: `clear_tables_except_players()`, `clear_all_tables()`, `export_db_to_excel()`

## 🎯 Reglas del Juego

- 🔢 **Equipos**: 2 equipos de 2 jugadores cada uno
- 🎯 **Puntuación**: 0-13 puntos por equipo
- 🏆 **Ganador**: No se permiten empates
- 👥 **Jugadores**: Sin repetición en la misma partida
- 📅 **Registro**: Timestamp automático de cada partida

## 🔧 Funciones Principales del Código

### `app.py` - Aplicación Principal
- Configuración de Streamlit y navegación
- Menú lateral con 5 secciones principales
- Inicialización de base de datos

### `scripts.py` - Lógica de Páginas
- `incio()`: Página de bienvenida
- `pag_add_players()`: Gestión de jugadores
- `save_match()`: Registro de partidas con validaciones
- `estadisticas()`: Dashboard completo de análisis

### `db_utils.py` - Gestión de Datos
- 15+ funciones para operaciones de base de datos
- Consultas SQL optimizadas para estadísticas
- Funciones de exportación e importación

## 📊 Capturas de Pantalla

*[Aquí podrías agregar screenshots de tu aplicación]*

## 🚀 Próximas Mejoras

- [ ] 🔐 Sistema de autenticación de usuarios
- [ ] 📤 Importación de datos desde CSV/Excel
- [ ] 🏆 Sistema de torneos por eliminación
- [ ] 📸 Subida y gestión de fotos de jugadores
- [ ] 📧 Sistema de notificaciones por email
- [ ] ⚡ Actualizaciones en tiempo real
- [ ] 🎨 Temas personalizables
- [ ] 📱 PWA para dispositivos móviles
- [ ] 🔍 Búsqueda avanzada de jugadores
- [ ] 📈 Más métricas y estadísticas

## 🛠️ Desarrollo

### Requisitos para Contribuir
```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar tests (cuando estén disponibles)
python -m pytest

# Formatear código
black scripts.py db_utils.py app.py
```

### Estructura de Commits
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Documentación
- `style:` Formato de código
- `refactor:` Refactorización
- `test:` Tests

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. **Fork** el proyecto
2. **Crea** tu rama feature (`git checkout -b feature/NuevaFuncionalidad`)
3. **Commit** tus cambios (`git commit -m 'feat: Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/NuevaFuncionalidad`)
5. **Abre** un Pull Request

## 📋 Changelog

### v1.0.0 (Actual)
- ✅ Gestión completa de jugadores
- ✅ Registro de partidas con validaciones
- ✅ Estadísticas avanzadas con Altair
- ✅ Base de datos SQLite relacional
- ✅ Exportación a Excel
- ✅ Interfaz responsive

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 👨‍💻 Desarrollador

**JJMMC** - Desarrollador Junior Backend

- 🐙 **GitHub**: [@JJMMC](https://github.com/JJMMC)
- 🌐 **Proyecto**: [Petanca Streamlit](https://github.com/JJMMC/Petanca_Streamlit)
- 📧 **Email**: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

## 🌟 Demostración

Puedes ver la aplicación en funcionamiento:
- [Demo en vivo](tu-enlace-demo) *(cuando esté disponible)*
- [Video demostración](tu-enlace-video) *(cuando esté disponible)*

## 📞 Soporte

¿Encontraste un bug o tienes una sugerencia? 

- 🐛 [Reportar Bug](https://github.com/JJMMC/Petanca_Streamlit/issues)
- 💡 [Solicitar Feature](https://github.com/JJMMC/Petanca_Streamlit/issues)
- ❓ [Hacer Pregunta](https://github.com/JJMMC/Petanca_Streamlit/discussions)

## 🏗️ Stack Tecnológico Completo

| Categoría | Tecnología | Versión |
|-----------|------------|---------|
| **Backend** | Python | 3.8+ |
| **Framework Web** | Streamlit | 1.44.1 |
| **Base de Datos** | SQLite | Built-in |
| **Análisis de Datos** | Pandas | 2.2.3 |
| **Visualización** | Altair | 5.5.0 |
| **Exportación** | OpenPyXL | 3.1.5 |
| **UI/UX** | Streamlit Components | Latest |

---

⭐ **¡Si este proyecto te resultó útil, considera darle una estrella!** ⭐

**Hecho con ❤️ para la comunidad de petanca**

![Petanca](https://img.shields.io/badge/Deporte-Petanca-orange.svg)
![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-red.svg)

