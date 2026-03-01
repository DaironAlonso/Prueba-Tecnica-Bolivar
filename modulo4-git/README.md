# Módulo 4 — Versionamiento de Código
## Git y GitHub — Seguros Bolívar

---

## Escenario

Estoy trabajando en la rama `feature/new-login`. Mientras tanto, un compañero
fusionó un cambio crítico de seguridad en `main`. Necesito incorporar
**únicamente ese commit específico** en mi rama sin traer el resto de
actualizaciones de `main`.

---

## Solución — `git cherry-pick`

### Paso a paso

```bash
# 1. Identificar el hash del commit crítico en main
git log main --oneline

# Ejemplo de salida:
# a1b2c3d fix: corregir vulnerabilidad XSS en formulario de login  ← este necesito
# e4f5g6h feat: agregar nuevo módulo de reportes
# i7j8k9l refactor: reorganizar estructura de carpetas

# 2. Asegurarse de estar en la rama correcta
git checkout feature/new-login

# 3. Aplicar únicamente ese commit
git cherry-pick a1b2c3d

# 4. Verificar que el commit fue aplicado correctamente
git log --oneline

# 5. Subir los cambios
git push origin feature/new-login
```

---

## ¿Por qué cherry-pick y no otras alternativas?

| Estrategia | ¿Qué hace? | ¿Por qué NO usarla aquí? |
|------------|------------|--------------------------|
| `git merge main` | Trae TODOS los cambios de main | Contamina la rama con cambios no relacionados |
| `git rebase main` | Reescribe el historial completo | Trae todos los commits de main, no solo el que necesito |
| `git cherry-pick` | Aplica SOLO el commit específico | Es exactamente lo que necesitamos |

---

## Manejo de conflictos durante cherry-pick

Si el cherry-pick genera conflictos:

```bash
# 1. Git pausa y muestra los archivos en conflicto
git status

# 2. Resolver los conflictos manualmente en los archivos marcados
# Buscar y editar las secciones con <<<<<<< HEAD

# 3. Marcar como resuelto
git add archivo-con-conflicto.js

# 4. Continuar el cherry-pick
git cherry-pick --continue

# O si decides abortar
git cherry-pick --abort
```

---

## Buenas Prácticas de Versionamiento

### Convención de ramas
```
main          → código en producción
develop       → integración de features
feature/xxx   → nuevas funcionalidades
bugfix/xxx    → corrección de bugs
hotfix/xxx    → correcciones urgentes en producción
release/xxx   → preparación de versión
```

### Conventional Commits
```bash
feat: agregar endpoint de renovación de pólizas
fix: corregir validación de póliza individual
refactor: reorganizar capa de servicios
docs: actualizar README con ejemplos de uso
test: agregar pruebas unitarias al servicio de pólizas
chore: actualizar dependencias
```

### Flujo de trabajo recomendado
```bash
# 1. Siempre crear rama desde develop actualizado
git checkout develop
git pull origin develop
git checkout -b feature/nueva-funcionalidad

# 2. Commits frecuentes y descriptivos
git add .
git commit -m "feat: descripción clara del cambio"

# 3. Antes de hacer PR, sincronizar con develop
git fetch origin
git rebase origin/develop

# 4. Crear Pull Request con descripción clara
# 5. Code review obligatorio antes de mergear
```
