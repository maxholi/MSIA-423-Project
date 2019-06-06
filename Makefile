.PHONY: venv clean_env db_local db_remote get_data load_data fit_model test_model similarity app

data/Seasons_Stats.csv: src/get_data.py config/config.yml
	python src/get_data.py --config=config/config.yml

data/Hist.csv: data/Seasons_Stats.csv src/load_data.py config/config.yml
	python src/load_data.py --config=config/config.yml --input=data/Seasons_Stats.csv -oh=data/Hist.csv -oc=data/Current.csv

data/model.pkl: data/Hist.csv src/fit_model.py config/config.yml
	python src/fit_model.py --config=config/config.yml --input=data/Hist.csv -om=data/model.pkl -or=data/model_report.csv

data/CurrentPred.csv: data/Current.csv src/test_model.py config/config.yml
	python src/test_model.py --config=config/config.yml --input=data/Current.csv -od=data/CurrentPred.csv -op=data/Player_HOF.csv

data/Similar.csv: data/CurrentPred.csv src/similarity.py config/config.yml
	python src/similarity.py --config=config/config.yml -ih=data/Hist.csv -ic=data/CurrentPred.csv --output=data/Similar.csv


get_data: data/Seasons_Stats.csv

load_data: data/Hist.csv

fit_model: data/model.pkl

test_model: data/CurrentPred.csv

similarity: data/Similar.csv

all: fit_model test_model similarity

hof-env/bin/activate: requirements.txt
	test -d hof-env || virtualenv hof-env
	. hof-env/bin/activate; pip install -r requirements.txt
	touch hof-env/bin/activate

venv: hof-env/bin/activate

clean_env:
	rm -r hof-env

db_local:
	python app/models.py

db_remote:
	python app/models.py --rds=True

app:
	python app/hof_app.py



