1: python -m venv fastapi-env
    Win: fastapi-env\Scripts\activate
    Mac/Linux : source fastapi-env/bin/activate
2: pip install -r requirements.txt
3: To test app.py : uvicorn api:app --reload
4: docker build -t sentiment-app .
5: docker run -it -p 8000:8000 --name sentiment-hf sentiment-app