# Configuración de la organización de GitHub del AiLab (GitHub Free)

Configuración única de https://github.com/AI-Lab-Universidad-de-La-Sabana (regla [ORG-05](../README.md#org-05) de la guía).
La ejecuta un propietario.

```bash
gh auth login
bash aplicar.sh
```

El script es idempotente y hace lo siguiente:

| Qué | Detalle |
|---|---|
| Ajustes de la organización | Permiso base «sin acceso»; los miembros no crean repositorios ni hacen fork de los privados |
| Actions | `GITHUB_TOKEN` de solo lectura por defecto (cada workflow pide solo los permisos que necesita) |
| Equipo `ailab-core` | Lo crea si no existe; luego agregas a sus integrantes |

Al terminar, imprime los ajustes que la API no permite cambiar (2FA obligatoria, borrado de repositorios,
presupuesto de Actions en 0 USD, etc.).

## Qué no incluye GitHub Free y cómo se compensa

| Limitación en repositorios privados | Compensación en [`plantilla-proyecto`](https://github.com/AI-Lab-Universidad-de-La-Sabana/plantilla-proyecto) |
|---|---|
| No hay ramas protegidas ni rulesets | Hooks locales bloquean commits y push a `main`; la auditoría de CI abre un issue si algo llega a `main` sin PR aprobado |
| No se exigen revisiones ni se aplica CODEOWNERS | La plantilla del PR menciona a `ailab-core`; la auditoría verifica que otra persona aprobó |
| No hay *environments* ni aprobación de despliegues | Secretos del repositorio con prefijo por entorno; producción solo se despliega desde etiquetas que crea el equipo base |
| No hay *push protection* de secretos | gitleaks en el hook de commit y en CI, sobre todo el historial |
| 2.000 minutos de Actions al mes para toda la organización | CI en un solo job, cancelación de ejecuciones viejas y presupuesto en 0 USD |

Los repositorios **públicos** sí tienen protección de ramas en GitHub Free: `scripts/configurar-github.sh`
de la plantilla ([ver script](https://github.com/AI-Lab-Universidad-de-La-Sabana/plantilla-proyecto/blob/main/scripts/configurar-github.sh)) aplica el ruleset automáticamente cuando el repositorio es público.

Si en algún momento la organización obtiene GitHub Team (los docentes verificados pueden solicitarlo para
investigación a través de GitHub Education), la protección pasa al servidor con un ruleset de
organización y los hooks quedan como ayuda local.
