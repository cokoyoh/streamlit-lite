run: 
	cd src && streamlit run app.py
	@echo "Running Streamlit app..."

run-watch:
	cd src && streamlit run app.py --server.runOnSave true
	@echo "Running Streamlit app with watch mode..."

format:
	black .

requirements:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt
