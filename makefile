DEFAULT_GOAL := dev

.PHONY: dev

dev:
	docker compose -f docker-compose-dev.yml down
	docker compose -f docker-compose-dev.yml up
