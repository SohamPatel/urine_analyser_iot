import sqlite3
import json
import random
import names
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


def gen_urine_data(num, db_file):
    # Generates num patient & urine records. 65% urine records will be good, 20% low urgency, 10% medium, 5% high

    db_conn = create_connection(db_file)
    cur = db_conn.cursor()
    cur.execute("SELECT id FROM patient")
    rows = cur.fetchall()

    for i in range(num):
        urine_rec = {}
        gen_good_data(int(len(rows)*0.65), urine_rec)
        gen_bad_data(int(len(rows)*0.20), urine_rec, 'low')
        gen_bad_data(int(len(rows) * 0.10), urine_rec, 'medium')
        gen_bad_data(int(len(rows) * 0.05), urine_rec, 'high')
        urine_rec['id'] = [row[0] for row in rows]

        for i in range(len(urine_rec['id'])):
            sql = 'INSERT INTO patient_urine_records (patient_id, gravity, ph, bilirubin, urobilinogen, protein, glucose, ketones, hemoglobin, myoglobin, leukocyte_esterase, nitrite, ' \
                  'ascorbic_acid, colour, sample_time) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(sql, (urine_rec['id'][i], urine_rec['gravity'][i], urine_rec['ph'][i], urine_rec['bilirubin'][i], urine_rec['urobilinogen'][i], urine_rec['protein'][i],
                              urine_rec['glucose'][i], urine_rec['ketones'][i], urine_rec['hemoglobin'][i], urine_rec['myoglobin'][i], urine_rec['leukocyte_esterase'][i], urine_rec['nitrite'][i],
                              urine_rec['ascorbic_acid'][i], urine_rec['colour'][i], urine_rec['sample_time'][i]))
        db_conn.commit()
    cur.close()


def gen_good_data(num, urine_rec):
    good_funcs = {'gravity': good_gravity, 'ph': good_ph, 'bilirubin': good_bilirubin, 'urobilinogen': good_urobilinogen, 'protein': good_protein, 'glucose': good_glucose, 'ketones': good_ketones,
                  'hemoglobin': good_hemoglobin, 'myoglobin': good_myoglobin, 'leukocyte_esterase': good_leucocytes, 'nitrite': good_nitrite, 'colour': good_colour}
    properties = ['gravity', 'ph', 'bilirubin', 'urobilinogen', 'protein', 'glucose', 'ketones', 'hemoglobin', 'myoglobin', 'leukocyte_esterase', 'nitrite', 'colour']
    start_date = datetime.datetime.strptime('1/4/2019 0:01 AM', '%d/%m/%Y %H:%M %p')
    end_date = datetime.datetime.strptime('1/5/2019 23:59 PM', '%d/%m/%Y %H:%M %p')

    for i, property in enumerate(properties):
        try:
            urine_rec[property] += good_funcs[property](num)
        except KeyError:
                urine_rec[property] = good_funcs[property](num)
    try:
        urine_rec['ascorbic_acid'] += [0] * num
        urine_rec['sample_time'] += [random_date(start_date, end_date) for _ in range(num)]
    except KeyError:
        urine_rec['ascorbic_acid'] = [0] * num
        urine_rec['sample_time'] = [random_date(start_date, end_date) for _ in range(num)]


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


def random_date(start, end):
    return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())),)


def gen_bad_data(num, urine_rec, priority):
    bad_funcs = {'gravity': bad_gravity, 'ph': bad_ph, 'bilirubin': bad_bilirubin, 'urobilinogen': bad_urobilinogen, 'protein': bad_protein, 'glucose': bad_glucose, 'ketones': bad_ketones,
                 'hemoglobin': bad_hemoglobin, 'myoglobin': bad_myoglobin, 'leukocyte_esterase': bad_leucocytes, 'nitrite': bad_nitrite, 'colour': bad_colour}
    good_funcs = {'gravity': good_gravity, 'ph': good_ph, 'bilirubin': good_bilirubin, 'urobilinogen': good_urobilinogen, 'protein': good_protein, 'glucose': good_glucose, 'ketones': good_ketones,
                  'hemoglobin': good_hemoglobin, 'myoglobin': good_myoglobin, 'leukocyte_esterase': good_leucocytes, 'nitrite': good_nitrite, 'colour': good_colour}
    start_date = datetime.datetime.strptime('1/4/2019 0:01 AM', '%d/%m/%Y %H:%M %p')
    end_date = datetime.datetime.strptime('1/5/2019 23:59 PM', '%d/%m/%Y %H:%M %p')
    # Low priority: 1~2 properties are off
    # Medium priority: 3~5 properties are off
    # High priority: >6 properties are off
    properties = ['gravity', 'ph', 'bilirubin', 'urobilinogen', 'protein', 'glucose', 'ketones', 'hemoglobin', 'myoglobin', 'leukocyte_esterase', 'nitrite', 'colour']
    random.shuffle(properties)

    if priority == 'low':
        prop_num = random.randint(5, 7)
    elif priority == 'medium':
        prop_num = random.randint(8, 9)
    else:
        prop_num = random.randint(10, 12)
    # prop_num = 10

    for i, property in enumerate(properties):
        if i < prop_num:
            try:
                urine_rec[property] += bad_funcs[property](num, priority)
            except KeyError:
                urine_rec[property] = bad_funcs[property](num, priority)
        else:
            try:
                urine_rec[property] += good_funcs[property](num)
            except KeyError:
                urine_rec[property] = good_funcs[property](num)
    try:
        urine_rec['ascorbic_acid'] += [0] * num
        urine_rec['sample_time'] += [random_date(start_date, end_date) for _ in range(num)]
    except KeyError:
        urine_rec['ascorbic_acid'] = [0] * num
        urine_rec['sample_time'] = [random_date(start_date, end_date) for _ in range(num)]


def bad_gravity(num, priority):
    # gravity range: 1.002 to 1.035, gravity > 1.035 = dehydration
    mean = (1.035+1.002)/2
    div = mean-1.002
    if random.randint(0, 1) % 2 == 0:
        if priority == 'low':
            grav_low = 1.002-div
            grav_up = 1.001
        elif priority == 'medium':
            grav_low = 1.002-div*2
            grav_up = 1.001-div
        else:
            grav_low = 1.002-div*3
            grav_up = 1.001-div*2
    else:
        div = 1.035-mean
        if priority == 'low':
            grav_low = 1.035
            grav_up = 1.035+div
        elif priority == 'medium':
            grav_low = 1.035+div
            grav_up = 1.035+div*2
        else:
            grav_low = 1.035+div*2
            grav_up = 1.035+div*3
    if grav_low < 0:
        grav_low = 0
    gravity = [round(random.uniform(grav_low, grav_up), 3) for _ in range(num)]
    return gravity


def good_gravity(num):
    grav_low = 1.002
    grav_up = 1.035
    gravity = [round(random.uniform(grav_low, grav_up), 3) for _ in range(num)]
    return gravity


def bad_ph(num, priority):
    # ph range: 4.8 to 8, usually around 6
    mean = (4.8+8)/2
    div = mean-4.8
    if random.randint(0, 1) % 2 == 0:
        if priority == 'low':
            ph_low = 4.8-div
            ph_up = 4.8
        elif priority == 'medium':
            ph_low = 4.8-div*2
            ph_up = 4.8-div
        else:
            ph_low = 4.8-div*3
            ph_up = 4.8-div*2
    else:
        if priority == 'low':
            ph_low = 8
            ph_up = 8+div
        elif priority == 'medium':
            ph_low = 8+div
            ph_up = 8+div*2
        else:
            ph_low = 8+div*2
            ph_up = 8+div*3
    if ph_low < 0:
        ph_low = 0
    ph = [round(random.uniform(ph_low, ph_up), 1) for _ in range(num)]
    return ph


def good_ph(num):
    ph_low = 4.8
    ph_up = 8.0
    ph = [round(random.uniform(ph_low, ph_up), 1) for _ in range(num)]
    return ph


def bad_bilirubin(num, priority):
    # bilirubin: Boolean Value, if True, implicates liver diseases. Associated with Dark urine
    return [1]*num


def good_bilirubin(num):
    return [0]*num


def bad_urobilinogen(num, priority):
    # urobilinogen: 0.2-1.0 mg/dL
    mean = (0.2+1)/2
    div = mean-0.2
    if random.randint(0, 1) % 2 == 0:
        if priority == 'low':
            urobilinogen_low = 0.2-div
            urobilinogen_up = 0.19
        elif priority == 'medium':
            urobilinogen_low = 0.2-div*2
            urobilinogen_up = 0.2-div
        else:
            urobilinogen_low = 0.2-div*3
            urobilinogen_up = 0.2-div*2
    else:
        if priority == 'low':
            urobilinogen_low = 1
            urobilinogen_up = 1+div
        elif priority == 'medium':
            urobilinogen_low = 1+div
            urobilinogen_up = 1+div*2
        else:
            urobilinogen_low = 1+div*2
            urobilinogen_up = 1+div*3
    if urobilinogen_low < 0:
        urobilinogen_low = 0
    urobilinogen = [round(random.uniform(urobilinogen_low, urobilinogen_up), 2) for _ in range(num)]
    return urobilinogen


def good_urobilinogen(num):
    urobilinogen_low = 0.2
    urobilinogen_up = 1.0
    urobilinogen = [round(random.uniform(urobilinogen_low, urobilinogen_up), 2) for _ in range(num)]
    return urobilinogen


def bad_protein(num, priority):
    # protein: <10mg/100mL
    div = 10/2
    if priority == 'low':
        protein_low = 10
        protein_up = 10+div
    elif priority == 'medium':
        protein_low = 10+div
        protein_up = 10+div*2
    else:
        protein_low = 10+div*2
        protein_up = 10+div*3
    protein = [round(random.uniform(protein_low, protein_up), 1) for _ in range(num)]
    return protein


def good_protein(num):
    # protein: <10mg/100mL
    protein_low = 0
    protein_up = 10
    protein = [round(random.uniform(protein_low, protein_up), 1) for _ in range(num)]
    return protein


def bad_glucose(num, priority):
    # glucose: 0 to 0.8 mmol/L
    div = 0.8/2
    if priority == 'low':
        glucose_low = 0.8
        glucose_up = 0.8+div
    elif priority == 'medium':
        glucose_low = 0.8+div
        glucose_up = 0.8+div*2
    else:
        glucose_low = 0.8+div*2
        glucose_up = 0.8+div*3
    glucose = [round(random.uniform(glucose_low, glucose_up), 1) for _ in range(num)]
    return glucose


def good_glucose(num):
    # glucose: 0 to 0.8 mmol/L
    glucose_low = 0
    glucose_up = 0.8
    glucose = [round(random.uniform(glucose_low, glucose_up), 1) for _ in range(num)]
    return glucose


def bad_ketones(num, priority):
    # ketones:
    # Small: <20 mg/dL
    # Moderate: 30 to 40 mg/dL
    # Large: >80 mg/dL
    mean = (20+80)/2
    div = mean-20
    if priority == 'low':
        ketones_low = 40
        ketones_up = 40+div
    elif priority == 'medium':
        ketones_low = 40+div
        ketones_up = 40+div*2
    else:
        ketones_low = 40+div*2
        ketones_up = 40+div*3
    ketones = [round(random.uniform(ketones_low, ketones_up), 1) for _ in range(num)]
    return ketones


def good_ketones(num):
    # ketones:
    # Small: <20 mg/dL
    # Moderate: 30 to 40 mg/dL
    # Large: >80 mg/dL

    ketones_low = 0
    ketones_up = 40
    ketones = [round(random.uniform(ketones_low, ketones_up), 1) for _ in range(num)]
    return ketones


def bad_hemoglobin(num, priority):
    # hemoglobin:
    # male: 13.5 to 17.5 grams/dL
    # female: 12.0 to 15.5 grams/dL
    mean = (12 + 17.5) / 2
    div = mean - 12
    if random.randint(0, 1) % 2 == 0:
        if priority == 'low':
            hemoglobin_low = 12-div
            hemoglobin_up = 12
        elif priority == 'medium':
            hemoglobin_low = 12-div*2
            hemoglobin_up = 12-div
        else:
            hemoglobin_low = 12-div*3
            hemoglobin_up = 12-div*2
    else:
        if priority == 'low':
            hemoglobin_low = 17.5
            hemoglobin_up = 17.5+div
        elif priority == 'medium':
            hemoglobin_low = 17.5+div
            hemoglobin_up = 17.5+div*2
        else:
            hemoglobin_low = 17.5+div*2
            hemoglobin_up = 17.5+div*3
    if hemoglobin_low < 0:
        hemoglobin_low = 0
    hemoglobin = [round(random.uniform(hemoglobin_low, hemoglobin_up), 1) for _ in range(num)]
    return hemoglobin


def good_hemoglobin(num):
    # hemoglobin:
    # male: 13.5 to 17.5 grams/dL
    # female: 12.0 to 15.5 grams/dL
    hemoglobin_low = 12.0
    hemoglobin_up = 17.5
    hemoglobin = [round(random.uniform(hemoglobin_low, hemoglobin_up), 1) for _ in range(num)]
    return hemoglobin


def bad_myoglobin(num, priority):
    # myoglobin:
    # Normal: False
    # Abnormal: True
    return [1]*num


def good_myoglobin(num):
    return [0]*num


def bad_leucocytes(num, priority):
    # Leucocytes: Integer, 0 to 5
    div = 5/2
    if priority == 'low':
        leucocytes_low = 5
        leucocytes_up = int(5+div)
    elif priority == 'medium':
        leucocytes_low = int(5+div)
        leucocytes_up = int(5+div*2)
    else:
        leucocytes_low = int(5+div*2)
        leucocytes_up = int(5+div*3)
    leucocytes = [random.randrange(leucocytes_low, leucocytes_up) for _ in range(num)]
    return leucocytes


def good_leucocytes(num):
    leucocytes = [random.randrange(0, 5) for _ in range(num)]
    return leucocytes


def bad_nitrite(num, priority):
    # nitrite:
    # If present -> Have infection
    # If not present -> Still may have infection
    return [1] * num


def good_nitrite(num):
    return [0] * num


def bad_colour(num, priority):
    colours = ['maroon', 'red', 'orange', 'olive', 'purple', 'fuchsia', 'lime', 'navy', 'blue', 'aqua', 'teal', 'black', 'gray', 'silver']
    colours = [random.choice(colours) for _ in range(num)]
    return colours


def good_colour(num):
    colours = ['yellow', 'white', 'green']
    colours = [random.choice(colours) for _ in range(num)]
    return colours

'''
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

    # Generates urine sample data for every patient. Includes good & bad data
    # gen_urine_data(sample_per_patient, db_file)
'''