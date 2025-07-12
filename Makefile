VENV_PATH=./workout_api/bin

run:
	@$(VENV_PATH)/uvicorn api.main:app --reload

create-migrations:
	@PYTHONPATH=$(PYTHONPATH):$(pwd) $(VENV_PATH)/alembic revision --autogenerate -m "$(d)"

run-migrations:
	@PYTHONPATH=$(PYTHONPATH):$(pwd) $(VENV_PATH)/alembic upgrade head
