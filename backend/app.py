from flask import Flask

app = Flask(__name__)

@app.route("/sensor_data", methods = ['POST'])
def sensor_data():
    if request.method == 'POST':
        sensor_data = request.get_json()
        return sensor_data
    else
        return 'Error 405 - Method Not Allowed'


if __name__ == '__main__':
    app.run(debug=True)
