# Activate virtual environment
source ./flask/bin/activate

# Install new requirements if necessary
pip install -r requirements.txt

# Set Development environment
export FLASK_ENV=development

# Run App
flask run
