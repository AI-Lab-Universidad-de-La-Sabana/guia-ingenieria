#!/usr/bin/env bash
# Configuración única de la organización de GitHub del AiLab [ORG-05], para el plan GitHub Free.
# En GitHub Free no hay rulesets de organización ni protección de ramas en repositorios privados:
# esa protección la aportan los hooks y la auditoría de CI de plantilla-proyecto.
# Lo ejecuta un propietario con la CLI de GitHub autenticada (gh auth login).
# Es idempotente: se puede volver a ejecutar sin problema.
#
# Uso: bash aplicar.sh [organizacion]
set -euo pipefail

org="${1:-AI-Lab-Universidad-de-La-Sabana}"

command -v gh >/dev/null || { echo "Falta la CLI de GitHub: https://cli.github.com"; exit 1; }
gh api "orgs/${org}" --silent || { echo "No hay acceso a la organización ${org}."; exit 1; }

echo "== Ajustes de la organización ${org}"
gh api --method PATCH "orgs/${org}" --silent \
  -f default_repository_permission=none \
  -F members_can_create_repositories=false \
  -F members_can_create_public_repositories=false \
  -F members_can_create_private_repositories=false \
  -F members_can_fork_private_repositories=false

echo "== GITHUB_TOKEN de solo lectura por defecto en Actions"
gh api --method PUT "orgs/${org}/actions/permissions/workflow" --silent \
  -f default_workflow_permissions=read \
  -F can_approve_pull_request_reviews=false

echo "== Equipo ailab-core"
if ! gh api "orgs/${org}/teams/ailab-core" --silent 2>/dev/null; then
  gh api --method POST "orgs/${org}/teams" --silent \
    -f name=ailab-core -f privacy=closed \
    -f description="Equipo base del AiLab: revisa y aprueba todos los PR"
  echo "Creado. Agrega a sus integrantes en GitHub → Teams → ailab-core."
fi

cat <<'EOF'

Listo. Ajustes que la API no permite cambiar y se hacen a mano, una sola vez,
en GitHub → Settings de la organización:
  [ ] Authentication security → Require two-factor authentication
  [ ] Member privileges → desmarcar "Allow members to delete or transfer repositories"
  [ ] Member privileges → desmarcar "Allow members to change repository visibilities"
  [ ] Member privileges → "Repository invitations": solo propietarios
  [ ] Third-party access / GitHub Apps: exigir aprobación de un propietario
  [ ] Code security → activar Dependabot alerts y security updates para repositorios nuevos
  [ ] Billing → presupuesto de Actions en 0 USD: si se agotan los 2.000 minutos del mes,
      CI se detiene en los repositorios privados en lugar de generar cobros
EOF
