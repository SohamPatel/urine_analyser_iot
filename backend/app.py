from flask import Flask

app = Flask(__name__)

@app.route("/sensor_data", methods = ['POST'])
def sensor_data():
    if request.method == 'POST':
        # sensor_data = request.get_json()
        sensor_data = """
        {
            "deviceID": "34124412",
            "patientID": "92152244",
            "sensorData": {
                "colour": {
                "R": 12,
                "G": 245,
                "B": 189
                },
                "pH": 6.2,
                "glucose": "100 mg/dl",
                "protein": "0.7 g/l"
            }
        }
        """
        return sensor_data
    else:
        return 'Error 405 - Method Not Allowed'


if __name__ == '__main__':
    app.run(debug=True)
