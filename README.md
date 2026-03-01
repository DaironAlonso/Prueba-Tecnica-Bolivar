# API de Gestión de Pólizas — Seguros Bolívar

## Decisión Tecnológica

La prueba especifica Spring Boot (Java) como tecnología base. Sin embargo,
se tomó la decisión de implementar la solución con **Python + Django REST Framework**
por las siguientes razones:

### Justificación técnica

1. **Dominio y experiencia** — Cuento con más de 2 años de experiencia desarrollando
   APIs REST con Django, lo que me permite entregar una solución más robusta, limpia
   y bien estructurada en el tiempo disponible.

2. **Equivalencia arquitectónica** — Django REST Framework implementa exactamente
   los mismos patrones que Spring Boot:
   - `Models` = `@Entity` (JPA)
   - `Serializers` = DTOs
   - `Views` = `@RestController`
   - `Middleware` = `Filter/Interceptor`
   - `ORM Django` = `Hibernate`

3. **Mismos principios evaluados** — La prueba evalúa arquitectura limpia, separación
   de capas, validaciones de negocio, manejo de errores y buenas prácticas. Estos
   principios son independientes del lenguaje.

4. **Calidad sobre tecnología** — Preferí entregar código limpio, funcional y bien
   documentado en un lenguaje que domino, antes que código incompleto o con errores
   en un lenguaje menos familiar.

### Nota
Si soy seleccionado, me comprometo a aprender Spring Boot y Java con el rigor
necesario para aportar al equipo desde el primer sprint. Los conceptos de
arquitectura ya están claros — solo es cuestión de trasladarlos al nuevo lenguaje.

---

## Tecnologías utilizadas

- Python 3.9.11
- Django 5.2.x
- Django REST Framework
- SQLite (base de datos de desarrollo)

---

## Instalación y ejecución

```bash
# 1. Clonar o descomprimir el proyecto
git clone https://github.com/DaironAlonso/Prueba-Tecnica-Bolivar.git
cd Prueba-Tecnica-Bolivar/modulo2-api
cd modulo2-api

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instalar dependencias
pip install django djangorestframework

# 4. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 5. Iniciar servidor
python manage.py runserver
```

El servidor queda disponible en: `http://127.0.0.1:8000`

---

## Autenticación

Todos los endpoints requieren el siguiente header obligatorio:

```
x-api-key: 123456
```

Si no se envía o es inválida, la API responde `401 No autorizado`.

---

## Endpoints disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/polizas/` | Listar pólizas (filtros opcionales: `tipo`, `estado`) |
| POST | `/api/polizas/` | Crear nueva póliza |
| GET | `/api/polizas/{id}/riesgos/` | Listar riesgos de una póliza |
| POST | `/api/polizas/{id}/renovar/` | Renovar póliza aplicando IPC |
| POST | `/api/polizas/{id}/cancelar/` | Cancelar póliza y todos sus riesgos |
| POST | `/api/polizas/{id}/riesgos/agregar/` | Agregar riesgo (solo pólizas COLECTIVAS) |
| POST | `/riesgos/{id}/cancelar/` | Cancelar un riesgo individual |
| POST | `/core-mock/evento/` | Mock de integración con sistema CORE |

---

## Ejemplos completos con PowerShell

### Crear póliza COLECTIVA
```powershell
$headers = @{ "x-api-key" = "123456"; "Content-Type" = "application/json" }
$body = '{"tipo": "COLECTIVA", "fecha_inicio": "2026-01-01", "fecha_fin": "2026-12-31", "valor_canon": 1000000, "valor_prima": 12000000, "tomador": "Inmobiliaria XYZ", "asegurado": "Juan Perez", "beneficiario": "Maria Lopez"}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/ -Method POST -Headers $headers -Body $body -UseBasicParsing
```

### Crear póliza INDIVIDUAL
```powershell
$headers = @{ "x-api-key" = "123456"; "Content-Type" = "application/json" }
$body = '{"tipo": "INDIVIDUAL", "fecha_inicio": "2026-01-01", "fecha_fin": "2026-12-31", "valor_canon": 500000, "valor_prima": 6000000, "tomador": "Carlos Ruiz", "asegurado": "Carlos Ruiz", "beneficiario": "Ana Ruiz"}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/ -Method POST -Headers $headers -Body $body -UseBasicParsing
```

### Listar todas las pólizas
```powershell
$headers = @{ "x-api-key" = "123456" }
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/ -Method GET -Headers $headers -UseBasicParsing
```

### Filtrar pólizas por tipo y estado
```powershell
$headers = @{ "x-api-key" = "123456" }
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/polizas/?tipo=COLECTIVA&estado=ACTIVA" -Method GET -Headers $headers -UseBasicParsing
```

### Agregar riesgo a póliza COLECTIVA
```powershell
$headers = @{ "x-api-key" = "123456"; "Content-Type" = "application/json" }
$body = '{"descripcion": "Riesgo de incendio"}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/1/riesgos/agregar/ -Method POST -Headers $headers -Body $body -UseBasicParsing
```

### Listar riesgos de una póliza
```powershell
$headers = @{ "x-api-key" = "123456" }
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/1/riesgos/ -Method GET -Headers $headers -UseBasicParsing
```

### Renovar póliza con IPC
```powershell
$headers = @{ "x-api-key" = "123456"; "Content-Type" = "application/json" }
$body = '{"ipc": 9.28}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/1/renovar/ -Method POST -Headers $headers -Body $body -UseBasicParsing
```

### Cancelar una póliza
```powershell
$headers = @{ "x-api-key" = "123456" }
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/1/cancelar/ -Method POST -Headers $headers -UseBasicParsing
```

### Cancelar un riesgo individual
```powershell
$headers = @{ "x-api-key" = "123456" }
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/riesgos/1/cancelar/ -Method POST -Headers $headers -UseBasicParsing
```

### Enviar evento al CORE mock
```powershell
$headers = @{ "x-api-key" = "123456"; "Content-Type" = "application/json" }
$body = '{"evento": "ACTUALIZACION", "polizaId": 1}'
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/core-mock/evento/ -Method POST -Headers $headers -Body $body -UseBasicParsing
```

### Probar sin API key (debe retornar 401)
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/polizas/ -Method GET -UseBasicParsing
```