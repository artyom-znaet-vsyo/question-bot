SRC_DIR = question_bot
SERVICE_TAG = question_bot:latest

poetry-shell:
	set -a && source ./.env && \
	    poetry shell

local-run:
	set -a && source ./.env && \
	    PYTHONPATH=. poetry run python question_bot/bot_logic.py


@build:
	docker build --tag ${SERVICE_TAG} .

docker-run:
	docker run -it --rm --env-file .env ${SERVICE_TAG}

docker-run-daemon:
	docker run -d --env-file .env --name artyom_bot ${SERVICE_TAG}

#
# Linting
#

lint-isort:
	find ${SRC_DIR} -iname '*.py' -exec isort --check-only {} +

lint-black:
	black --check ${SRC_DIR}

lint-black-fix:
	black ${SRC_DIR}

lint-flake:
	flake8 ${SRC_DIR}

@lint: lint-black lint-flake lint-isort
