import sqlite3
from flask import Flask, request, jsonify
import requests
import re
import json
from flask_cors import CORS
from os import environ

db_path = 'hospital_edit.db'
emr_path = 'emr.db'

app = Flask(__name__)
CORS(app)

# Telstra API Credentials
TAPI_CLIENT_ID = 'WTM8cZvo1xzWKTnDgIGwIdiblmVDhxaB'
TAPI_CLIENT_SECRET = 'QMjsw8iQ1mDV4Utq'

@app.route("/", methods = ['GET'])
def home(): 
    return "website live"

@app.route("/sensor_data", methods = ['POST'])
def sensor_data():
    global tapi_client_id, tapi_client_secret

    if request.method == 'POST':
        sensor_data = request.get_json()        
        # Example Data
        # {
        #     "deviceID": "34124412",
        #     "patientID": "DCE5AEB8-6DB9-4106-8AE4-02CCC5C23741",
        #     "sensorData": {
        #         "colour": {
        #             "R": 12,
        #             "G": 245,
        #             "B": 189
        #         },
        #         "pH": 6.2,
        #         "glucose": "1.0 mmol/L",
        #         "protein": "0.7 g/l"
        #     }
        # }
        patientID = sensor_data['patientID']
        colour = sensor_data['sensorData']['colour']
        ph = float(sensor_data['sensorData']['pH'])/100
        glucose = float(sensor_data['sensorData']['glucose'].split()[0])/100
        protein = float(sensor_data['sensorData']['protein'].split()[0])

        print(patientID)
        # Retrieve nurse contact
        result = query_db('''SELECT s.mobile, p.first_name, p.last_name, w.room FROM patient p
                                JOIN ward w ON w.patient=p.id
                                JOIN staff s ON w.nurse=s.id
                                WHERE p.id = ?''', (patientID,))[0]
        
        nurse_contact = result['mobile']
        patientFirstName = result['first_name']
        patientLastName = result['last_name']
        patientWard = result['room']

        print('Nurse contact number:', nurse_contact)

        result = query_db('''SELECT s.mobile FROM patient p
                                JOIN staff s ON p.doctor=s.id
                                WHERE p.id = ?''', (patientID,))[0]
        doctor_contact = result['mobile']
        print('Doctor contact number:', doctor_contact)


        # TODO: Update EMR

        alertFor = 'none'
        outcome = "PATIENT: " + patientFirstName + " " + patientLastName + " (Ward " + patientWard + ")\r"

        # https://www.aci.health.nsw.gov.au/__data/assets/pdf_file/0007/285811/Lets_Get_Started_-_Urinalysis.pdf

        # Normal values for urine - http://intranet.tdmu.edu.ua/data/kafedra/internal/i_nurse/classes_stud/BSN%20(4year)%20Program/Full%20time%20study/Third%20year/Integrate%20Nursing%20Practicum/17.%20Diagnostic%20Testing.files/image082.jpg

        # TODO: Analyse Colour - https://www.semanticscholar.org/paper/An-IoT-based-pervasive-body-hydration-tracker-(PHT)-Chin-Tisan/1cc21f9479b012e02bb433fd0d3d39b11be37561/figure/5
    #                            https://www.korwater.com/pages/hydration-urine-test
        if (colour['B'] < 40):
            # Extremely Dehydrated, may indicate blood in urine or kidney disease, alert doctor
            outcome += "\rColour indicates extreme dehydration."
            alertFor = 'doctor'
        elif (colour['B'] >= 40 and colour['B'] < 100):
            # Dehydration, alert staff to monitor and hydrate patient
            outcome += "\rColour indicates dehyrdation."
            alertFor = 'nurse'
        elif (colour['B'] >= 100 and colour['B'] < 170):
            # Minimal Dehydration
            # outcome += "Colour indicates minimal dehyrdation."
            pass

        elif (colour['B'] >= 170):
            # Hydrated
            # outcome += "Colour indicates optimal hyrdration."
            pass


        # TODO: Analyse pH - https://betterhealthclinic.com.au/urine-tests/
        if (ph < 5.5):
            # Very acidic, alert doctor
            outcome += "\rpH level indicates very acidic urine (" + str(ph) + ")."
            alertFor = 'doctor'
            
        elif (ph >= 5.5 and ph < 6.5):
            # Acidic, alert staff to change diet to more alkaline and/or alkaline mineral supplements
            outcome += "\rpH level indicates acidic urine (" + str(ph) + ")."
            if (alertFor == 'none'):
                alertFor = 'nurse'

        elif (ph >= 6.5 and ph < 7.5):
            # Optimal, don't alert
            # outcome += "\rpH level is optimal."
            pass

        elif (ph >= 7.5):
            # Alkaline, alert staff to monitor and acidify via diet if needed
            outcome += "\rpH level indicates alkaline urine (" + str(ph) + " mmol/L)."
            if (alertFor == 'none'):
                alertFor = 'nurse'


        # TODO: Analyse Glucose - https://www.healthline.com/health/glucose-test-urine#results
        if (glucose >= 0 and glucose <= 0.8):
            # Normal glucose level
            # outcome += "\rNormal glucose level."
            pass
        else:
            # Possible diabetes
            outcome += "\rGlucose level is not normal (" + str(glucose) + " mmol/L)."
            alertFor = 'doctor'
        

        # # TODO: Analyse Protein
        # outcome += "\rUnable to analyse Protein level."


        # Send Notification to either Doctor or staff based on analysis (UNCOMMENT BELOW TO MAKE IT WORK)
        # ========== SMS MESSAGING START ============
        if alertFor != 'none':
            # Get authorisation token
            auth_payload = {
                'client_id' : TAPI_CLIENT_ID,
                'client_secret': TAPI_CLIENT_SECRET,
                'grant_type' : 'client_credentials',
                'scope' : 'NSMS'
            }
            access_token = json.loads(requests.post("https://tapi.telstra.com/v2/oauth/token", data=auth_payload).text)['access_token']
            
            # Provision application
            provisioning_headers = {
                'Content-Type': "application/json",
                'Authorization': f"Bearer {access_token}"
            }
            provisioning_number = json.loads(requests.post("https://tapi.telstra.com/v2/messages/provisioning/subscriptions", data=json.dumps({}), headers=provisioning_headers).text)['destinationAddress']

            # Send SMS
            sms_message = outcome
            sms_payload = {
                'to': doctor_contact if alertFor == 'doctor' else nurse_contact,
                'from': provisioning_number,
                'body': sms_message
            }
            sms_headers = {
                'Content-Type': "application/json",
                'Authorization': f"Bearer {access_token}"
            }
            sms_response = requests.post("https://tapi.telstra.com/v2/messages/sms", data=json.dumps(sms_payload), headers=sms_headers)
            print(sms_response.text)
            print(sms_response.status_code)
            
        # ========== SMS MESSAGING END ============
        
        return jsonify({'data': outcome})
    else:
        return 'Error 405 - Method Not Allowed'

def query_db(query, args):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.close()
    if result == None:
        return result[0]
    else:
        return result

def execute_db(query, args):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()
    return

def query_emr(query, args):
    conn = sqlite3.connect(emr_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.close()
    if result == None:
        return result[0]
    else:
        return result

def execute_emr(query, args):
    conn = sqlite3.connect(emr_path)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()
    return

def dict_factory(cursor, row):
    dictionary = {}
    for index, column in enumerate(cursor.description):
        dictionary[column[0]] = row[index]
    return dictionary

if __name__ == '__main__':
    app.run(host='0.0.0.0')
