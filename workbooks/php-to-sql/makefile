include .env

compose_up: 
	docker compose up -d --build

compose_down:
	docker compose down

compose_down_clean: backup-db
	docker compose down -v
	sudo rm -rf ./database/mysql-server/src/*

save_db_snapshot:
	if [ -f database/backup/main.sql ]; then \
		mv database/backup/main.sql database/backup/main.$$(date +%Y%m%d%H%M%S).sql; \
	else \
		echo 'NO database to snapshot'; \
	fi

backup_db: save_db_snapshot
	docker exec ${COMPOSE_PROJECT_NAME}_mysql /usr/bin/mysqldump -u root \
	--password=${DATABASE_ROOT_PASSWORD} \
	--single-transaction \
	--set-gtid-purged=OFF \
	${COMPOSE_PROJECT_NAME} > database/backup/main.sql

restore_db:
	@if [ -f database/backup/main.sql ]; then \
		echo 'RESTORING database'; \
		docker exec -i ${COMPOSE_PROJECT_NAME}_mysql \
			mysql -u root --password=${DATABASE_ROOT_PASSWORD} ${COMPOSE_PROJECT_NAME} \
			< database/backup/main.sql; \
		echo 'RESTORED database'; \
	else \
		echo 'NO database to restore'; \
	fi

	