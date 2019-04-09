from flask import Flask, request

app = Flask(__name__)

@app.route("/sensor_data", methods = ['POST'])
def sensor_data():
    if request.method == 'POST':
        sensor_data = request.get_json()        
        # Example Data
        # {
        #     "deviceID": "34124412",
        #     "patientID": "92152244",
        #     "sensorData": {
        #         "colour": {
        #             "R": 12,
        #             "G": 245,
        #             "B": 189
        #         },
        #         "pH": 6.2,
        #         "glucose": "5 mmol/L",
        #         "protein": "0.7 g/l"
        #     }
        # }
        patientID = sensor_data['patientID']
        colour = sensor_data['sensorData']['colour']
        ph = sensor_data['sensorData']['pH']
        glucose = float(sensor_data['sensorData']['glucose'].split()[0])
        protein = float(sensor_data['sensorData']['protein'].split()[0])

        # TODO: Update EMR

        outcome = ""

        # https://www.aci.health.nsw.gov.au/__data/assets/pdf_file/0007/285811/Lets_Get_Started_-_Urinalysis.pdf

        # Normal values for urine - http://intranet.tdmu.edu.ua/data/kafedra/internal/i_nurse/classes_stud/BSN%20(4year)%20Program/Full%20time%20study/Third%20year/Integrate%20Nursing%20Practicum/17.%20Diagnostic%20Testing.files/image082.jpg

        # TODO: Analyse Colour - https://www.semanticscholar.org/paper/An-IoT-based-pervasive-body-hydration-tracker-(PHT)-Chin-Tisan/1cc21f9479b012e02bb433fd0d3d39b11be37561/figure/5
    #                            https://www.korwater.com/pages/hydration-urine-test
        if (colour['B'] < 40):
            # Extremely Dehydrated, may indicate blood in urine or kidney disease, alert doctor
            outcome += "Colour indicates extreme dehydration, possible blood in urine or kidney disease."
        elif (colour['B'] >= 40 and colour['B'] < 100):
            # Dehydration, alert staff to monitor and hydrate patient
            outcome += "Colour indicates dehyrdation."
        elif (colour['B'] >= 100 and colour['B'] < 170):
            # Minimal Dehydration
            outcome += "Colour indicates minimal dehyrdation."
        elif (colour['B'] >= 170):
            # Hydrated
            outcome += "Colour indicates optimal hyrdration."


        # TODO: Analyse pH - https://betterhealthclinic.com.au/urine-tests/
        if (ph < 5.5):
            # Very acidic, alert doctor
            outcome += "\npH level indicates very acidic urine."
        elif (ph >= 5.5 and ph < 6.5):
            # Acidic, alert staff to change diet to more alkaline and/or alkaline mineral supplements
            outcome += "\npH level indicates acidic urine."
        elif (ph >= 6.5 and ph < 7.5):
            # Optimal, don't alert
            outcome += "\npH level is optimal."
        elif (ph >= 7.5):
            # Alkaline, alert staff to monitor and acidify via diet if needed
            outcome += "\npH level indicates alkaline urine."


        # TODO: Analyse Glucose - https://www.healthline.com/health/glucose-test-urine#results
        if (glucose >= 0 and glucose <= 0.8):
            # Normal glucose level
            outcome += "\nNormal glucose level."
        else:
            # Possible diabetes
            outcome += "\nGlucose level inicates possible diabetes."
        

        # TODO: Analyse Protein
        outcome += "\nUnable to analyse Protein level."


        # print(colour, ph, glucose, protein)
        
        return 'SUCCESS.\n\n' + outcome
    else:
        return 'Error 405 - Method Not Allowed'


if __name__ == '__main__':
    app.run(debug=True)
