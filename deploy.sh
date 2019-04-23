export FLASK_RUN_PORT=$1
os.environ["PORT"]=$1
cd backend && flask run