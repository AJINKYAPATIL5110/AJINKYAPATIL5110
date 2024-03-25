from flask import Flask,render_template,request,redirect,session,send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import os

app = Flask(__name__)
app.secret_key = "login"
# db_folder = os.path.abspath('D:/Auditorium_management_system/instances')
# db_file_path = os.path.join(db_folder, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.bd"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Register(db.Model):
    SNO=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    p_number=db.Column(db.String(10))
    d_id=db.Column(db.String(15))
    year=db.Column(db.String(15))
    branch=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(10))
    c_password=db.Column(db.String(10))
    role=db.Column(db.String(10))
    
    
class Auditorium(db.Model):
    SNO = db.Column(db.Integer, primary_key=True)
    p_name=db.Column(db.String(15),nullable=False)
    year = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(500), nullable=False)
    d_id=db.Column(db.Integer)
    date1=db.Column(db.String(15))
    # time=db.Column(db.String(50))
    # from1=db.Column(db.Interger)
    # to=db.Column(db.Interger)
    p_number=db.Column(db.String(10))
    slot=db.Column(db.String(10))


class temp_data(db.Model):
    SNO = db.Column(db.Integer, primary_key=True,autoincrement=True)
    p_name=db.Column(db.String(15),nullable=False)
    year = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(500), nullable=False)
    d_id=db.Column(db.Integer)
    date1=db.Column(db.String(200), nullable=False)
    slot=db.Column(db.String(15))

class slot_available(db.Model):
    SNO = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date1 = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    duration=db.Column(db.String(500), nullable=False)
    availability = db.Column(db.Integer)

    
# with app.app_context():
#    db.create_all()
    

global slot
slot=['9am-10am','10am-11am','11am-12pm','12pm-1pm','1pm-2pm','2pm-3pm','3pm-4pm','4pm-5pm']

slot1={'9am-10am':10,'10am-11am':11,'11am-12pm':12,'12pm-1pm':13,'1pm-2pm':14,'2pm-3pm':15,'3pm-4pm':16,'4pm-5pm':17}

@app.route('/')
def hello_world():
 
    session['logged-in']=False
    session['admin-logged-in']=False
    return render_template("index.html")

@app.route('/close')
def close():
    return render_template("index.html",msg=1)



@app.route('/admin_page')
def admin_page():
    if not session.get('logged-in'):
        session['admin-logged-in']=True
        msg=1
        return render_template("login.html",msg2=msg)
    msg=1
    all_data=Register.query.all()
    return render_template("register.html",msg7=msg,all_data=all_data)

@app.route("/go_to")
def go_to():
    return render_template("index.html",msg=1)

@app.route('/register_page')
def register_page():
    msg=1
    return render_template("register.html",msg6=msg)

@app.route("/register",methods=['GET','POST'])
def register():
    
    print("Hello")
    if request.method=='POST':
        name=request.form['name']
        number=request.form['number']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['c_password']
        department_id=request.form['department_id']
        year=request.form['year']
        branch=request.form['branch']
        role=request.form['role']
        
        found=Register.query.all()
        
        for i in found:
            if i.d_id==department_id:
                msg="Username Already Exist!"
                msg1=1
                return render_template("register.html",msg5=msg,msg6=msg1)
            
            
        add_data=Register(name=name,email=email,p_number=number,year=year,branch=branch,d_id=department_id,password=password,c_password=confirm_password,role=role)
        db.session.add(add_data)
        db.session.commit()
        return redirect("/login")
    msg=1
    return render_template("register.html",msg6=msg)


@app.route("/dashboard")
def dashboard():
    if not session.get('logged-in'):
        return render_template("login.html")
    msg=1
    all_data=Register.query.all()
    return render_template("register.html",msg7=msg,all_data=all_data)


@app.route("/delete1/<int:SNO>")
def delete1(SNO):
    if not session.get('logged-in'):
        return render_template("login.html")
    database=Register.query.filter_by(SNO=SNO).first()
    if database:
        db.session.delete(database)
        db.session.commit()
        return redirect("/dashboard")
    return redirect("/dashboard")

@app.route("/edit/<int:SNO>")
def edit(SNO):
    if not session.get('logged-in'):
        return render_template("login.html")
    msg=1
    global sno1
    sno1=SNO
    return render_template("register.html",msg8=msg)

@app.route("/update",methods=['GET','POST'])
def update():
    if not session.get('logged-in'):
        return render_template("login.html")
    global sno1
    if request.method=="POST":
        name=request.form['name']
        number=request.form['number']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['c_password']
        department_id=request.form['department_id']
        year=request.form['year']
        branch=request.form['branch']
        
        database=Register.query.filter_by(SNO=sno1).first()
        database.name=name
        database.email=email
        database.p_number=number
        database.password=password
        database.year=year
        database.branch=branch
        database.d_id=department_id
        database.c_password=confirm_password
        db.session.commit()
        return redirect("/dashboard")
    

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/login_credential', methods=['POST', 'GET'])
def login_credential():
    if request.method == 'POST':
        if session.get('admin-logged-in'):
            if 'username' in request.form and 'password' in request.form:
                username = request.form["username"]
                password=request.form['password']
                all_data=Register.query.filter_by(d_id=username,password=password,role="Admin").first()
                if all_data:
                    session['username']= all_data.d_id
                    session['password']=all_data.password
                    msg=1
                    all_data=Register.query.all()
                    return render_template("register.html",msg7=msg,all_data=all_data)
                msg=1
                return render_template("login.html",msg3=msg)
        



        if 'department_id' in request.form and 'password' in request.form:
            
            department_id = request.form["department_id"]
            password=request.form['password']
            
            all_data=Register.query.filter_by(d_id=department_id,password=password).first()
            if all_data:
                session['id']= all_data.d_id
                session['password']=all_data.password
                session['logged-in']=True
                msg=1
                return render_template("index.html",msg=msg)
                
    msg=1
    return render_template("login.html",msg=msg)

@app.route("/book_seat")
def book_seat():
    if not session.get('logged-in'):
        session['admin-logged-in']=False
        return render_template("login.html")
    msg=0
    return render_template("book.html",msg=msg)


@app.route("/book",methods=['POST','GET'])
def book():
    global slot
    print("Hello")
    if request.method=='POST':
        # temp_slots=[]
        p_name=request.form['name']
        number=request.form['number']
        department_id=request.form['department_id']
        year=request.form['year']
        branch=request.form['branch']
        date1=request.form['date']

        found4=Register.query.filter_by(d_id=session.get('id')).first()
        if found4.branch!=branch:
            msg="You are not authorized to book slot of other departments"
            return render_template("book.html",msg=msg)
        
        if not Register.query.filter_by(branch=branch,d_id=department_id).first():
            msg="Invalid credential"
            return render_template("book.html",msg=msg)
        
        found=Register.query.filter_by(d_id=department_id).first()
        found1=Auditorium.query.filter_by(year=year,branch=branch).first()
        found2=slot_available.query.filter_by(date1=date1).all()
        

        if found1:
            msg="Your Department already book the auditorium"
            return render_template("book.html",msg=msg)
        
        if not found:
            msg="Department ID is incorrect"
            return render_template("book.html",msg=msg)
        else:
            current_date = date.today()
            input_date = datetime.strptime(date1, "%Y-%m-%d")
            current_time = datetime.now()
            input_time=int(current_time.strftime("%H"))

            if input_date.date() < current_date:
                msg="Not Available"
                return render_template("book.html",msg2=msg)
            
            if not found2:
                for i in range(1,9):
                    add_slot=slot_available(name=slot1[slot[i-1]],date1=date1,availability=0,duration=slot[i-1])
                    db.session.add(add_slot)
                    db.session.commit()

            found3=slot_available.query.filter((slot_available.name)>=input_time,slot_available.date1==date1,slot_available.availability==0).all()

            if found3:
                temp_data2=temp_data.query.filter_by(d_id=department_id).first()
                if temp_data2:
                    db.session.delete(temp_data2)
                    db.session.commit()

                temp_data1=temp_data(p_name=p_name,year=year,branch=branch,d_id=department_id,date1=date1)
                db.session.add(temp_data1)
                db.session.commit()
                msg=1
                return render_template('book.html',msg1=msg,slots=found3)
            else:
                msg="Slots are full"
                return render_template('book.html',msg=msg)
    return render_template("book.html")

@app.route("/slot_booking/<int:SNO>")
def slot_booking(SNO):
    slot=slot_available.query.filter_by(SNO=SNO).first()
    if slot and slot.availability==0:
        slot.availability=1
        db.session.commit()

        temp_data1=temp_data.query.filter_by(d_id=session.get('id')).first()
        temp_data1.slot=slot.name
        db.session.commit()
        auditorium=Auditorium(p_name=temp_data1.p_name,year=temp_data1.year,branch=temp_data1.branch,d_id=temp_data1.d_id,date1=temp_data1.date1,slot=temp_data1.slot)
        db.session.add(auditorium)
        db.session.commit()

    slot_ava=slot_available.query.filter_by(date1=slot.date1,availability=0).all()
    return render_template("book.html",msg1=1,slots=slot_ava)

@app.route("/program_details")
def program_details():
    if not session.get('logged-in'):
        return render_template("login.html")
    slot_details=Auditorium.query.filter_by(d_id=session.get('id')).all()
    return render_template("index.html",slot_details=slot_details,msg=1)
        

@app.route("/log_out")
def log_out():
    session['logged-in']=False
    session['admin-logged-in']=False
    msg=0
    return render_template("index.html",msg=msg)
            
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)