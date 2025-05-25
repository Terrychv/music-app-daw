# 🎵 Music App DAW - Proyecto Final

Esta aplicación permite explorar catálogos de álbumes, canciones y artistas, así como gestionar contenido según el rol del usuario.

---

## 🚀 Tecnologías utilizadas

- Python 3.12
- Django 4.x
- Bootstrap 5
- HTML / CSS / JS / jQuery
- MariaDB / SQLite (dependiendo del entorno)

---

## 📁 Estructura del proyecto

```
project_music_app/
├── core/              # Home y
├── catalog/           # Álbumes, canciones, artistas, géneros
├── users/             # Autenticación y perfiles de usuario
├── media/             # Archivos subidos (portadas, avatares...)
├── db.sqlite3         # (Ignorado en Git)
├── manage.py
```

---

## 🧑‍💻 Instalación (para colaboradores)

### 1. Clona el repositorio
```bash
git clone git@github.com:Terrychv/music-app-daw.git
cd music-app-daw
```

### 2. Crea el entorno virtual y actívalo
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
# o
source venv/bin/activate  # En Linux/Mac
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt  
```

### 4. Configura la base de datos
```bash
python manage.py migrate
```

### 5. (Opcional) Carga datos de prueba
```bash
python manage.py loaddata nombre_fixture.json
```
### 6. Crea el superusuario para entrar al admin
```bash
python manage.py createsuperuser

```

### 7. Ejecuta el servidor
```bash
python manage.py runserver
```

Abre [http://localhost:8000](http://localhost:8000) para ver la app en tu navegador.

---



## ✅ Funcionalidades principales

- Registro e inicio de sesión
- Visualización de catálogos musicales
- Comentarios y valoraciones
- Gestiones según el rol (cliente / admin)
- Carga de portadas, audios y avatares

---

## ⚠️ Importante

- No subir `media/`, `.env`, ni `db.sqlite3` al repositorio

---
