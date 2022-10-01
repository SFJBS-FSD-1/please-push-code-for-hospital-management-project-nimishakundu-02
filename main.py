from flask import Flask,request,jsonify,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/hospitaldb'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/hospitaldb'

class Production_Config(Config):
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith('postgres://'):
        uri=uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri

env=os.environ.get("ENV","Development")
if env == "Production":
    config_str=Production_Config
else:
    config_str=Development_Config

app=Flask(__name__)
app.config.from_object(config_str)

db=SQLAlchemy(app)
migrate=Migrate(app,db)

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:1234@localhost/hospitaldb'



class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    age=db.Column(db.Integer, nullable=False)
    bed_type=db.Column(db.String(100), nullable=False)
    address=db.Column(db.String(100), nullable=False)
    state=db.Column(db.String(100), nullable=False)
    city=db.Column(db.String(100), nullable=False)
    patient_status=db.Column(db.String(100), nullable=False)


    @staticmethod
    def add_patient(name,phone_number,age,bed_type,address,state,city,patient_status):
        new_patient = Hospital(name=name, phone_number=phone_number, age=age, bed_type=bed_type,
                           address=address, state=state, city=city, patient_status=patient_status)
        db.session.add(new_patient)
        db.session.commit()


    @staticmethod
    def get_patient():
        data = Hospital.query.all()
        return data

    @staticmethod
    def get_patient_id(id):
        return Hospital.query.filter_by(id=id).first()


    @staticmethod
    def del_Hospital(id):
        new_patient = Hospital.query.filter_by(id=id).delete()
        db.session.commit()
        return new_patient


    @staticmethod
    def update_Hospital(id,age,bed_type,address,state,city,patient_status):
        updatepatient = Hospital.query.filter_by(id=id).first()
        if updatepatient:
            updatepatient.age = age
            updatepatient.bed_type = bed_type
            updatepatient.address = address
            updatepatient.state = state
            updatepatient.city = city
            updatepatient.patient_status = patient_status
            db.session.commit()
        return updatepatient


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.String(100), nullable=False)

    @staticmethod
    def add_medicine(name, quantity, rate):
        new_medicine = Medicine(name=name, quantity=quantity, rate=rate)
        db.session.add(new_medicine)
        db.session.commit()


    @staticmethod
    def get_medicine():
        data = Medicine.query.all()
        return data


    @staticmethod
    def get_medicine_id(id):
        return Medicine.query.filter_by(id=id).first()


    @staticmethod
    def del_medicine(id):
        new_medicine = Medicine.query.filter_by(id=id).delete()
        db.session.commit()
        return new_medicine


    @staticmethod
    def update_Medicine(id, quantity, rate):
        updatemedicine = Hospital.query.filter_by(id=id).first()
        if updatemedicine:
            updatemedicine.quantity = quantity
            updatemedicine.rate = rate
            db.session.commit()
        return updatemedicine

@app.route("/home",methods=['GET','POST'])
def home():
    if request.method == "GET":
        return render_template("home.html")


@app.route('/getpatient',methods=['GET'])
def get_AllPatients():
        data = Hospital.get_patient()
        return render_template("AllPatients.html", data=data)


@app.route('/getmed',methods=['GET'])
def get_AllMedicine():
    data=Medicine.get_medicine()
    return render_template("AllMedicine.html", data=data)

@app.route('/getpatient/<int:id>',methods=['GET','POST'])
def get_Patient_by_id(id):
    data = Hospital.get_patient_id(id)
    if data:
        print(data.name)
        print(data.phone_number)
        print(data.age)
        print(data.bed_type)
        print(data.address)
        print(data.state)
        print(data.city)
        print(data.patient_status)
        return jsonify({'name': data.name, 'phone_number': data.phone_number, 'age': data.age,
                        'bed_type': data.bed_type, 'address':data.address, 'state':data.state,
                        'city':data.city,'patient_status':data.patient_status})
    else:
        return jsonify({'message': 'Patient ID not found'})


@app.route('/getmed/<int:id>',methods=['GET','POST'])
def get_Medicine_by_id(id):
    data=Medicine.get_medicine_id(id)
    if data:
        print(data.name)
        print(data.quantity)
        print(data.rate)
        return jsonify({'name':data.name,'quantity':data.quantity,'rate':data.rate})
    else:
        return jsonify({'message': 'Medicine ID not found'})


@app.route('/delpatient/<int:id>',methods=['DELETE'])
def del_Patient_by_id(id):
        data=Hospital.del_Hospital(id)
        if data:
            return jsonify({'message':'Patient deleted'})
        else:
            return jsonify({'message': 'Patient id not found'})


@app.route('/delmed/<int:id>',methods=['DELETE'])
def del_Medicine_by_id(id):
        data=Medicine.del_medicine(id)
        if data:
            return jsonify({'message':'Medicine deleted'})
        else:
            return jsonify({'message': 'Medicine id not found'})


@app.route('/updatepatient/<int:id>',methods=['PUT'])
def update_Patient_by_id(id):
    print("Updating Patient")
    data = request.get_json()
    print(data)
    response = Hospital.update_Hospital(id,data["age"],data["bed_type"],
                                        data["address"],data["state"],data["city"],
                                        data["patient_status"])
    print(response)
    if response:
        return jsonify({"message": 'Patient info updated'})
    else:
        return jsonify({'message': 'Patient id not found'})


@app.route('/updatemed/<int:id>',methods=['PUT'])
def update_Medicine_by_id(id):
    print("Updating Medcine")
    data = request.get_json()
    print(data)
    response = Medicine.update_Medicine(id,data["quantity"],data["rate"])
    print(response)
    if response:
        return jsonify({"message": 'Medicine info updated'})
    else:
        return jsonify({'message': 'Medicine id not found'})

@app.route("/registerpatient",methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html",flag=False)
    else:
        if request.method == 'POST':
            name=request.form["name"]
            phone_number=request.form["phone_number"]
            age=request.form["age"]
            bed_type=request.form["bed_type"]
            address=request.form["address"]
            state=request.form["state"]
            city=request.form["city"]
            patient_status=request.form["patient_status"]
            add_entry = Hospital.add_patient(name=name,phone_number=phone_number, age=age,
                                             bed_type=bed_type,
                           address=address, state=state, city=city, patient_status=patient_status)
            return render_template("register.html",flag=True)


@app.route("/registermed",methods=["GET","POST"])
def register_med():
    if request.method == 'GET':
        return render_template("registermed.html",flag=False)
    else:
        if request.method == 'POST':
            name=request.form["name"]
            quantity=request.form["quantity"]
            rate=request.form["rate"]
            new_medicine=Medicine.add_medicine(name=name, quantity=quantity, rate=rate)
            return render_template("registermed.html",flag=True)





port = int(os.environ.get("PORT",5000))

if __name__ == "__main__":
    app.run(port=port)