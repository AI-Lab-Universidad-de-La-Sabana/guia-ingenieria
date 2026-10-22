# Makefile del repositorio de la guía (mismos nombres que en todos los proyectos del AiLab).
.DEFAULT_GOAL := help
SHELL := bash

.PHONY: help setup check

help: ## Muestra los comandos disponibles
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

setup: ## Activa los hooks de git (requiere uv: https://docs.astral.sh/uv/)
	@command -v uv >/dev/null || { echo "Falta uv: https://docs.astral.sh/uv/getting-started/installation/"; exit 1; }
	uvx pre-commit install

check: ## Valida reglas, anclas y enlaces de la guía (lo mismo que CI)
	python3 scripts/validar_guia.py
