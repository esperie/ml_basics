import os
import uvicorn
from importlib.util import find_spec
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

from config import setup_logger  # initialize_django

# django_app = initialize_django()  # Get Django WSGI app

from applications.autovaluation import views

logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI()

# Load FastAPI routers from the various modules
app.include_router(views.app)
origins = ['*']

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get('/')
async def root():
	return {'message': 'Welcome to My Autovaluation App Server.'}


app.mount('/autovaluation', views)
# app.mount('/admin', WSGIMiddleware(django_app))
# app.mount('/django-test', WSGIMiddleware(django_app))
app.mount('/static', StaticFiles(
	directory=os.path.normpath(
		os.path.join(
			find_spec("django.contrib.admin").origin, "..", "static"))),
          name="static", )

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8080)
