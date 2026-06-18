# Cortex DHS — developer convenience commands.
# Usage: `make <target>` (run from the repo root). `make help` lists targets.

COMPOSE       := docker compose
COMPOSE_SIM   := docker compose --profile simulator
BACKEND       := backend

.DEFAULT_GOAL := help
.PHONY: help up down reseed seed logs ps restart-backend sim-stop sim-start

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

up: ## Start the full stack including the vital simulator
	$(COMPOSE_SIM) up -d

down: ## Stop and remove the stack (and orphan containers like the simulator)
	$(COMPOSE_SIM) down --remove-orphans

reseed: ## Race-proof DB reseed: pause simulator, seed (stable IDs), resume
	@echo "⏸  Stopping vital simulator (if running)..."
	-$(COMPOSE) stop vital_simulator
	@echo "🌱  Reseeding database..."
	$(COMPOSE) exec -T $(BACKEND) python scripts/seed_dev_data.py
	@echo "▶  Restarting vital simulator..."
	$(COMPOSE_SIM) up -d vital_simulator
	@echo "✅  Reseed complete."

seed: ## Reseed the DB (alias for reseed — keeps IDs stable and simulator safe)
	@$(MAKE) --no-print-directory reseed

sim-stop: ## Stop just the vital simulator
	-$(COMPOSE) stop vital_simulator

sim-start: ## Start just the vital simulator
	$(COMPOSE_SIM) up -d vital_simulator

restart-backend: ## Restart the backend container
	$(COMPOSE) restart backend

logs: ## Tail backend logs
	$(COMPOSE) logs -f backend

ps: ## Show container status
	$(COMPOSE) ps
