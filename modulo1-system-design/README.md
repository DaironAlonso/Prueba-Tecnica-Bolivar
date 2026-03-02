# Módulo 1 — Diseño de Sistema
## Plataforma de Gestión de Pólizas — Seguros Bolívar

---

## 1. Arquitectura de Alto Nivel

El sistema se diseña como una arquitectura de **microservicios** con los siguientes
componentes principales:

```
[Frontend / Consumidores externos]
             │
        [API Gateway]
     (autenticación, rate-limiting, versionamiento)
             │
    ┌────────┼────────────────┐
    │        │                │
[Svc Pólizas] [Svc Riesgos] [Svc Notificaciones]
    │        │                │
    └────────┴───────┬────────┘
                     │
            [Core Adapter]
            (Adaptador WebLogic)
                     │
          [CORE Transaccional Legado]

[Base de Datos: Postgres]
[Message Broker: RabbitMQ]
[Caché: Redis]
```

---

## 2. Patrones de Arquitectura Seleccionados

### Patrón 1 — Arquitectura Hexagonal (Ports & Adapters)
**¿Por qué?**
Desacopla completamente la lógica de negocio (pólizas, riesgos, renovaciones)
de los adaptadores externos como el CORE legado, la base de datos y las
notificaciones. Esto permite:
- Testear la lógica de negocio sin depender de infraestructura externa
- Cambiar el CORE o la BD sin afectar las reglas de negocio
- Incorporar nuevos canales de notificación sin modificar el dominio

### Patrón 2 — Event-Driven Architecture (Arquitectura Orientada a Eventos)
**¿Por qué?**
Las notificaciones (correo/SMS) en creación y renovación de pólizas se
publican como eventos asíncronos en un Message Broker (RabbitMQ).
Esto garantiza:
- Disponibilidad 24/7 — si el servicio de notificaciones falla, los eventos
  se procesan cuando vuelva
- Desacoplamiento entre servicios
- Tolerancia a fallos sin afectar el flujo principal de pólizas

### Patrón 3 — API Gateway + CQRS
**¿Por qué?**
- El **API Gateway** centraliza autenticación, versionamiento (`/v1/`, `/v2/`),
  rate-limiting y logging de todas las peticiones entrantes
- **CQRS** (Command Query Responsibility Segregation) separa las operaciones
  de lectura (consultar pólizas) de las de escritura (crear, renovar, cancelar),
  permitiendo escalar cada lado de forma independiente según la carga

---

## 3. Modelo de Datos Principal

### Entidad: Poliza
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Long | Identificador único |
| tipo | Enum | INDIVIDUAL / COLECTIVA |
| estado | Enum | ACTIVA / CANCELADA / RENOVADA |
| fecha_inicio | Date | Inicio de vigencia |
| fecha_fin | Date | Fin de vigencia |
| valor_canon | Decimal | Valor mensual del canon |
| valor_prima | Decimal | Canon x meses de vigencia |
| tomador_id | Long | FK a persona |
| asegurado_id | Long | FK a persona |
| beneficiario_id | Long | FK a persona |

### Entidad: Riesgo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Long | Identificador único |
| poliza_id | Long | FK a Póliza |
| estado | Enum | ACTIVO / CANCELADO |
| descripcion | String | Descripción del riesgo |
| fecha_cancelacion | Date | Fecha de cancelación (nullable) |

### Entidad: Renovacion
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Long | Identificador único |
| poliza_id | Long | FK a Póliza |
| ipc_aplicado | Decimal | Porcentaje IPC usado |
| fecha_renovacion | Date | Fecha de la renovación |

### Relaciones
- Una **Póliza COLECTIVA** puede tener **muchos Riesgos**
- Una **Póliza INDIVIDUAL** solo puede tener **1 Riesgo**
- Una **Póliza** puede tener **muchas Renovaciones** (historial)

---

## 4. Decisiones de Diseño Clave

### Escalabilidad
- Cada microservicio escala de forma independiente según carga
- El servicio de consultas (CQRS read) puede replicarse sin afectar escrituras
- Se usa **Redis** como caché para consultas frecuentes de pólizas activas
- Base de datos con **particionamiento** por fecha para tablas de alto volumen

### Logs y Observabilidad
- Cada servicio emite logs estructurados en formato JSON
- Stack de observabilidad: **ELK** (Elasticsearch + Logstash + Kibana)
- Trazabilidad distribuida con **correlation ID** en cada request
- Métricas de negocio: pólizas creadas/renovadas/canceladas por día

### Tolerancia a Fallos
- **Circuit Breaker** (patrón Resilience4j) en el Core Adapter para evitar
  cascada de fallos si el CORE legado no responde
- Las notificaciones son asíncronas — un fallo en el servicio de notificaciones
  no afecta la creación o renovación de pólizas
- **Retry automático** con backoff exponencial para llamadas al CORE

### Versionamiento de APIs
- URLs versionadas: `/api/v1/polizas/`, `/api/v2/polizas/`
- La versión anterior se mantiene activa durante un período de transición
- Los cambios breaking se publican en nueva versión, nunca en la existente

---

## 5. Diagrama de Componentes

```
┌─────────────────────────────────────────────────────┐
│                    API GATEWAY                       │
│         (Auth, Rate Limit, Versioning /v1/)          │
└──────────────┬──────────────┬───────────────────────┘
               │              │
    ┌──────────▼──┐    ┌──────▼──────────┐
    │ Svc Pólizas │    │   Svc Riesgos   │
    │  (CRUD +    │    │  (Agregar /     │
    │  Renovar /  │    │   Cancelar)     │
    │  Cancelar)  │    └──────┬──────────┘
    └──────┬──────┘           │
           │                  │
           └────────┬─────────┘
                    │ Publica eventos
            ┌───────▼────────┐
            │ Message Broker │
            │    (Rabbit)    │
            └───────┬────────┘
                    │ Consume eventos
            ┌───────▼──────────────┐
            │  Svc Notificaciones  │
            │  (Correo / SMS)      │
            └──────────────────────┘

           Todas las escrituras
                    │
            ┌───────▼──────────────┐
            │    Core Adapter      │
            │ (Circuit Breaker +   │
            │  Retry + WebLogic)   │
            └───────┬──────────────┘
                    │
            ┌───────▼──────────────┐
            │  CORE Legado         │
            │  (WebLogic / SOAP)   │
            └──────────────────────┘

            ┌──────────────────────┐
            │   Base de Datos      │
            │     Postgres         │
            └──────────────────────┘
```
