import sqlite3
import json
import random
import names
import webcolors
import datetime


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)


def gen_patient_record_table(db_file):
    conn = create_connection(db_file)
    cur = conn.cursor()

    sql = "CREATE TABLE IF NOT EXISTS patient_urine_records (" \
          "patient_id INTEGER, " \
          "gravity REAL," \
          "ph REAL," \
          "bilirubin REAL," \
          "urobilinogen REAL," \
          "protein REAL," \
          "glucose REAL," \
          "ketones REAL," \
          "hemoglobin REAL," \
          "myoglobin INTEGER," \
          "leukocyte_esterase INTEGER," \
          "nitrite INTEGER," \
          "ascorbic_acid INTEGER," \
          "colour TEXT," \
          "sample_time DATETIME," \
          "FOREIGN KEY(patient_id) REFERENCES patient(id))"
    cur.execute(sql)
    conn.commit()
    conn.close()


def gen_normal_data(num, db_file):
    start_date = datetime.datetime.strptime('1/4/2019 0:01 AM', '%d/%m/%Y %H:%M %p')
    end_date = datetime.datetime.strptime('1/5/2019 23:59 PM', '%d/%m/%Y %H:%M %p')

    db_conn = create_connection(db_file)
    cur = db_conn.cursor()
    cur.execute("SELECT id FROM patient")
    rows = cur.fetchall()

    for row in rows:
        id = row[0]
        # ##################################################################
        # gravity range: 1.002 to 1.035  ,gravity>1.035 = dehydration
        # Decreased: <1.005
        # Inability to concentrate urine or excessive hydration (volume resuscitation with IV fluids)
        # Nephrogenic diabetes insipidus, acute golmerulonephritis, pyelonephritis, acute tubular necrosis
        # Falsely low specific gravity can be associated with alkaline urine
        #
        # Fixed: 1.010
        # In end stage renal disease, specific gravity tends towards 1.010. Chronic Renal Failure (CRF), Chronic glomerulonephritis (GN)
        #
        # Increased: >1.0035
        # Dehydration (fever, vomiting, diarrohea), SIADH, adrenal insufficiency, pre-renal renal failure, hyponatraemia with oedema, liver failure, CCF, nephrotic syndrome
        # Elevation in specific gravity also occurs with glycosuria (e.g. diabetes mellitus or IV glucose administration), proteinuria, IV contrast, urine contamination, LMW dextran solutions (colloid)

        grav_low = 1.002
        grav_up = 1.035
        gravity = [round(random.uniform(grav_low, grav_up), 3) for _ in range(num)]

        # ##################################################################
        # ph range: 4.8 to 8, usually around 6

        ph_low = 4.8
        ph_up = 8.0
        ph = [round(random.uniform(ph_low, ph_up), 1) for _ in range(num)]

        # ##################################################################
        # bilirubin: Boolean Value, if True, implicates liver diseases. Associated with Dark urine

        bilirubin = [0] * num

        # ##################################################################
        # urobilinogen: 0.2-1.0 mg/dL

        urobilinogen_low = 0.2
        urobilinogen_up = 1.0
        urobilinogen = [round(random.uniform(urobilinogen_low, urobilinogen_up), 2) for _ in range(num)]

        # ##################################################################
        # protein: <10mg/100mL

        protein_low = 0
        protein_up = 10
        protein = [round(random.uniform(protein_low, protein_up), 1) for _ in range(num)]

        # ##################################################################
        # glucose: 0 to 0.8 mmol/L

        glucose_low = 0
        glucose_up = 0.8
        glucose = [round(random.uniform(glucose_low, glucose_up), 1) for _ in range(num)]

        # ##################################################################
        # ketones:
        # Small: <20 mg/dL
        # Moderate: 30 to 40 mg/dL
        # Large: >80 mg/dL

        ketones_low = 0
        ketones_up = 100
        ketones = [round(random.uniform(ketones_low, ketones_up), 1) for _ in range(num)]

        # ##################################################################
        # hemoglobin:
        # male: 13.5 to 17.5 grams/dL
        # female: 12.0 to 15.5 grams/dL

        hemoglobin_low = 12
        hemoglobin_up = 17.5
        hemoglobin = [round(random.uniform(hemoglobin_low, hemoglobin_up), 1) for _ in range(num)]

        # ##################################################################
        # myoglobin:
        # Normal: False
        # Abnormal: True

        myoglobin = [0] * num

        # ##################################################################
        # Leucocytes: Integer, 0 to 5

        leucocytes = [random.randrange(0, 6) for _ in range(num)]

        # ##################################################################
        # nitrite:
        # If present -> Have infection
        # If not present -> Still may have infection

        nitrite = [0] * num

        # ##################################################################
        # ascorbic_acid: Boolean value. If True, test sample is useless

        ascorbic_acid = [0] * num

        # ##################################################################
        # colour: randomly pick colours from [yello, white, green]
        colour = ['yellow', 'white', 'green']
        colour = [random.choice(colour) for _ in range(num)]


        ####################################################################
        # generates sample time
        sample_time = [random_date(start_date, end_date) for _ in range(num)]

        sql = 'INSERT INTO patient_urine_records (patient_id, gravity, ph, bilirubin, urobilinogen, protein, glucose, ketones, hemoglobin, myoglobin, leukocyte_esterase, nitrite, ' \
            'ascorbic_acid, colour, sample_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        for entry in range(num):
            cur.execute(sql, (id, gravity[entry], ph[entry], bilirubin[entry], urobilinogen[entry], protein[entry], glucose[entry], ketones[entry], hemoglobin[entry], myoglobin[entry],
                        leucocytes[entry], nitrite[entry], ascorbic_acid[entry], colour[entry], sample_time[entry]))
    db_conn.commit()
    cur.close()


def gen_staff(num, db_file):
    db_conn = create_connection(db_file)
    cur = db_conn.cursor()

    for i in range(num):
        occupation = 'doctor'
        if i >= num//2:
            occupation = 'nurse'
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        mobile = '0404'+''.join([str(random.randint(0, 9)) for _ in range(6)])
        print(f'occ: {occupation}, name: {first_name} {last_name}, mob: {mobile}')
        cur.execute('INSERT INTO staff (occupation,first_name, last_name, mobile) VALUES (?,?,?,?)', (occupation, first_name, last_name, mobile))
    db_conn.commit()
    cur.close()


# def gen_ward(staff_num, ward_num, db_file):
#     db_conn = create_connection(db_file)
#     cur = db_conn.cursor()
#
#     nurse_per_ward = (staff_num//2) // ward_num
#     for i in range(ward_num):
#         for j in range(nurse_per_ward):
#             cur_ward = j
#         pass
#
#     db_conn.commit()
#     cur.close()


def gen_patient(num, db_file):
    db_conn = create_connection(db_file)
    cur = db_conn.cursor()

    for i in range(num):
        ward = 1
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        doctor = random.randint(0, 50)
        print(f'ward: {ward}, name: {first_name} {last_name}, doc: {doctor}')
        cur.execute('INSERT INTO patient (ward,first_name, last_name, doctor) VALUES (?,?,?,?)', (1, first_name, last_name, doctor))
    db_conn.commit()
    cur.close()


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        colour = webcolors.rgb_to_name(requested_colour, spec='css2')
        return colour
    except ValueError:
        colour = closest_colour(requested_colour)
        return colour


def random_date(start, end):
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())),)


if __name__ == '__main__':
    # Value definitions
    db_file = 'hospital.db'
    staff_num = 100
    patient_num = 100
    sample_per_patient = 5


    # Generates table for patient records
    gen_patient_record_table(db_file)

    # Randomly generates staff and inserts into database. First half of the staff will be doctors, second half will be nurses
    # gen_staff(staff_num, db_file)
    # Generates patients
    # gen_patient(patient_num, db_file)

    gen_normal_data(sample_per_patient, db_file)

