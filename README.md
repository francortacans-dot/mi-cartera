# Mi Cartera Pro - Setup Completo

## 📦 Arquitectura

```
Netlify (Frontend)        Render.com (Backend)
  index.html     ----→    Flask API (yfinance)
  Firebase       ←---     Precios NYSE → CEDEAR
```

---

## 🚀 PASO 1: Deploy API en Render.com

### Crear repositorio Git (si no tienes)
```bash
mkdir mi-cartera-api
cd mi-cartera-api
git init
git add app.py requirements.txt build.sh
git commit -m "Initial commit"
git remote add origin https://github.com/TU_USUARIO/mi-cartera-api.git
git push -u origin main
```

### En Render.com
1. Ve a **render.com** y loguéate
2. **New → Web Service**
3. Conecta tu repo GitHub
4. **Settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3.11
5. Deploy
6. **Copia la URL:** `https://tu-servicio.onrender.com`

**Render te dará un dominio gratis similar a:**
```
https://mi-cartera-api-xyz.onrender.com
```

---

## 🌐 PASO 2: Actualizar HTML con tu URL de Render

En `index.html`, busca esta línea (~250):

```javascript
const API_URL = "https://mi-cartera-api.onrender.com";
```

**Reemplázala con TU URL de Render:**

```javascript
const API_URL = "https://tu-servicio-xyz.onrender.com";
```

---

## 📤 PASO 3: Deploy Frontend en Netlify

1. Ve a **netlify.com**
2. **New site → Import existing project**
3. Sube tu `index.html` (y cualquier archivo extra)
4. Deploy

Tu app estará en:
```
https://tu-app.netlify.app
```

---

## 🔧 PASO 4: Probar

1. Abre tu app en Netlify
2. Loguéate con Firebase
3. Añade un CEDEAR (ej: NVDA, ratio 10)
4. Apretá el botón **↻** (refresh)
5. **Debería traer el precio en tiempo real** sin límites

---

## 🐛 Troubleshooting

### "No se pudieron traer los precios"
- ✅ Verifica que copiaste bien la URL de Render
- ✅ Espera 1 min (Render demora en desplegarse)
- ✅ Abre consola (F12) y busca errores CORS

### "Sin datos para TICKER"
- ✅ El ticker no existe en yfinance
- ✅ Busca el ticker correcto en Yahoo Finance

### Render se durmió (free tier)
- ✅ Solo ocurre si no usas la API en 15 min
- ✅ El primer refresh será lento (~5s)
- ✅ Luego es instantáneo

---

## 📝 Agregar más CEDEARs

En `app.py`, línea 11, el diccionario `RATIOS`:

```python
RATIOS = {
    'NVDA': 10,
    'MSFT': 30,
    'TU_NUEVO': 1,  # ← Agregar aquí
    ...
}
```

Luego:
```bash
git add app.py
git commit -m "Add new CEDEAR"
git push
```

Render redeploy automático.

---

## 💡 Mejoras futuras

- Agregar gráficos históricos (Plotly)
- Alertas automáticas por email
- Historial de trades (CSV export)
- Dashboard móvil optimizado

---

**¿Dudas? Chequea logs en Render (Dashboard → Service → Logs)**
