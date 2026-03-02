# Módulo 5 — Liderazgo Técnico y Gestión
## Seguros Bolívar

---

## Contexto del Equipo

- 8 desarrolladores en total
- 40% de deuda técnica en servicios clave
- 10 incidentes críticos en el último mes
- Presión del negocio para entregar funcionalidad en 3 semanas
- Falta de estándares y code review irregular
- 2 desarrolladores junior con brechas técnicas importantes

---

## 1. Las 5 Prioridades en las Primeras 2 Semanas

### Prioridad 1 — Estabilizar los incidentes críticos
Antes de construir cualquier cosa nueva, hay que apagar el fuego.
Organizaría un **war room** de triage en el primer día para clasificar
los 10 incidentes por impacto en producción y asignar responsables.
Sin estabilidad operacional, cualquier avance nuevo es construir sobre
arena.

### Prioridad 2 — Establecer estándares mínimos de code review
Definiría un **checklist básico obligatorio** de 5-7 puntos que todo
PR debe cumplir antes de mergearse. Sin esto, los problemas seguirán
multiplicándose sin importar cuánto código nuevo se escriba.

### Prioridad 3 — Mapear y priorizar la deuda técnica
Con el equipo, identificaría cuál del 40% de deuda técnica está
directamente relacionado con los incidentes críticos. No toda la deuda
es igual — hay que atacar primero la que genera inestabilidad real en
producción.

### Prioridad 4 — Plan de mentoría para los desarrolladores junior
Asignaría un desarrollador senior como **buddy** a cada junior para
pair programming en tickets reales. Esto reduce errores, acelera su
curva de aprendizaje y mejora la calidad del código entregado.

### Prioridad 5 — Negociar el alcance de la funcionalidad con el negocio
Presentaría al negocio un **MVP reducido** entregable en 3 semanas,
dejando funcionalidades secundarias para el siguiente sprint. Es mejor
entregar menos y bien, que todo y con deuda nueva.

---

## 2. Organización del Equipo

### Estructura propuesta

```
Equipo (8 desarrolladores)
│
├── Célula Estabilización (3 devs)
│   └── Foco: resolver incidentes + deuda técnica crítica
│
├── Célula Feature (3 devs)
│   └── Foco: entregar el MVP acordado con el negocio
│
└── Célula Calidad (2 devs senior)
    └── Foco: code reviews, estándares, mentoría a juniors
```

### Dinámicas del equipo
- **Daily standup de 15 minutos** — enfocado en bloqueos, no en status
- **Code review obligatorio** — mínimo 1 aprobación de un senior antes de mergear
- **Pair programming semanal** — senior con junior en tickets de mediana complejidad
- **Retrospectiva quincenal** — identificar qué mejorar en proceso y comunicación
- **Rotación de células** — cada 2 sprints para distribuir conocimiento

---

## 3. Métricas para Evaluar el Desempeño

### Métricas de estabilidad
| Métrica | Objetivo |
|---------|----------|
| Número de incidentes por sprint | Reducir 50% en 4 semanas |
| Tiempo promedio de resolución (MTTR) | Menos de 2 horas |
| Tasa de incidentes recurrentes | 0% — cada incidente resuelto de raíz |

### Métricas de velocidad y calidad
| Métrica | Objetivo |
|---------|----------|
| Lead time (idea → producción) | Menos de 5 días |
| Deployment frequency | Al menos 1 deploy por semana |
| Change failure rate | Menos del 10% |
| Cobertura de tests | Mínimo 70% en servicios críticos |

### Métricas de deuda técnica
| Métrica | Objetivo |
|---------|----------|
| Issues críticos en SonarQube | Reducir 30% por sprint |
| % deuda técnica en servicios clave | Bajar de 40% a 20% en 2 meses |

### Métricas de equipo
| Métrica | Objetivo |
|---------|----------|
| PRs rechazados en code review | Tendencia a la baja |
| Tiempo de onboarding de juniors | Reducir con sesiones de mentoría |

---

## 4. Prácticas Técnicas Obligatorias

### Control de calidad
- **SonarQube en el pipeline CI/CD** — ningún PR puede mergearse con
  issues de severidad crítica o bloqueante
- **Code review obligatorio** — mínimo 1 aprobación de un desarrollador
  senior antes de fusionar cualquier rama
- **Cobertura mínima de tests** — 70% en servicios críticos, medido
  automáticamente en cada PR

### Estándares de código
- **Conventional Commits** — mensajes de commit estandarizados:
  `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- **Linting automático** — herramienta configurada en pre-commit hook
  para garantizar estilo consistente
- **Documentación de APIs** — Swagger/OpenAPI obligatorio en todos
  los endpoints nuevos o modificados

### Flujo de trabajo
- **GitFlow estricto** — ramas `feature/`, `bugfix/`, `hotfix/`
  siempre desde `develop`, nunca directamente desde `main`
- **PRs pequeños** — máximo 400 líneas de código por PR para facilitar
  el code review efectivo
- **Definition of Done** — un ticket solo es "terminado" cuando tiene
  tests, documentación y pasó code review

### Seguridad
- **OWASP Top 10** como checklist obligatorio en el code review
- **Secrets management** — prohibido hardcodear credenciales,
  usar variables de entorno o vault
- **Dependency scanning** — revisión automática de vulnerabilidades
  en dependencias en cada PR

---

## 5. Gestión de la Presión del Negocio sin Comprometer la Calidad

### Principio base
La velocidad sostenible supera la velocidad explosiva. Entregar rápido
hoy generando más deuda técnica solo garantiza más incidentes mañana,
lo cual termina siendo más lento para el negocio.

### Estrategia concreta

**Paso 1 — Transparencia total con el negocio**
Presentar un dashboard sencillo que muestre el estado real:
incidentes activos, deuda técnica y capacidad real del equipo.
El negocio toma mejores decisiones cuando tiene información real.

**Paso 2 — Negociar alcance, no calidad**
Proponer al negocio tres opciones:
- **Opción A:** MVP en 3 semanas con funcionalidades esenciales
- **Opción B:** Funcionalidad completa en 5 semanas
- **Opción C:** Todo en 3 semanas (implica deuda técnica y riesgo
  de nuevos incidentes)

**Paso 3 — Hacer visible el costo de la deuda técnica**
Mostrar con datos cómo los 10 incidentes del último mes costaron X
horas de desarrollo que no se invirtieron en features. La deuda
técnica no es un problema técnico — es un problema de negocio.

**Paso 4 — Compromisos claros y cumplibles**
Mejor prometer menos y cumplir, que prometer todo y fallar.
Un equipo que cumple consistentemente genera más confianza que uno
que entrega todo una vez y luego falla repetidamente.
