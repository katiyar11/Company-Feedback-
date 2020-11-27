from controller import app,db,es
from flask_login import login_required
from flask import render_template, redirect, url_for, request, flash
from functools import wraps
from models import *
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message,Mail
import datetime


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'Your_email@gmail.com',
    MAIL_PASSWORD = 'password',
))
mail=Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("home.html") 

@app.route('/addNewQuestions', methods=["POST", "GET"])
@login_required
def addNewQuestions():
    if request.method=="POST":  

        option_for_column={}
            
        for questions_name in request.form.get('qsn').split(","):
            option_array=[]
            
            if (("name_add" in questions_name) and (request.form.get(questions_name)!="")):
                for option_name in request.form.get('opt').split(","):
                    if questions_name in option_name:
                        option_array.append(request.form.get(option_name))

                option_for_column[request.form.get(questions_name)]=option_array
                qsnInsert = questions_tbl(questions=request.form.get(questions_name), question_type="multiple", options=option_array)  
                db.session.add(qsnInsert) 
                db.session.flush()
                db.session.commit()
               


            elif (("qsn_add" in questions_name) and (request.form.get(questions_name)!="")):
                insert_value  = questions_tbl(questions=request.form.get(questions_name), question_type="short", options=None)  
                db.session.add(insert_value)
                db.session.flush()          
                db.session.commit()
                
    return render_template("AfrontPage.html", allQuestions=db.session.query(questions_tbl).all()) 


@app.route('/update', methods=["POST", "GET"])
@login_required
def update():
    if request.method == "POST":

        update_data = db.session.query(questions_tbl).filter(questions_tbl.questionID==request.form.get('id')).all()
        var =0 
        
        if request.form.get('question_type')== 'multiple':  
            optArr=[]                  
            for i in update_data:          
                for data in range(len(i.options)):
                    var+=1
                    optStr=str(var)
                    optArr.append(request.form.get(optStr))
          
            db.session.query(questions_tbl).filter(questions_tbl.questionID==request.form.get('id')).update({questions_tbl.questions:request.form.get('question'), questions_tbl.options:optArr},synchronize_session = False)
            db.session.commit()  
        else:
            db.session.query(questions_tbl).filter(questions_tbl.questionID==request.form.get('id')).update({questions_tbl.questions:request.form.get('question'),questions_tbl.options:None},synchronize_session = False)
            db.session.commit()   
        
        return redirect(url_for('addNewQuestions'))  




@app.route('/deleteQsn/<id>', methods=["GET", "POST"])
@login_required
def deleteQsn(id): 
    record = db.session.query(questions_tbl).filter(questions_tbl.questionID==id).all()
    for i in record:
        print(i)
        db.session.delete(i)
        db.session.commit()
    flash("Question Deleted Successfully")
 
    return redirect (url_for('addNewQuestions'))




@app.route('/NewFeedbackForm', methods=["POST", "GET"])
@login_required
def NewFeedbackForm():
    if request.method=="POST":  

        option_for_column={}
        for questions_name in request.form.get('qsn').split(","):
            option_array=[]
            getQuestion = db.session.query(questions_tbl.questions).filter_by(questions=request.form.get(questions_name)).first()
            
            if (("name_add" in questions_name) and (request.form.get(questions_name)!="")):
                for option_name in request.form.get('opt').split(","):
                    if questions_name in option_name:
                        option_array.append(request.form.get(option_name))
          
                option_for_column[request.form.get(questions_name)]=option_array

                if getQuestion == None:    
                    qsnInsert = questions_tbl(questions=request.form.get(questions_name), question_type="multiple", options=option_array) 
                    db.session.add(qsnInsert) 
                    # db.session.flush()
                    db.session.commit()
               


            elif getQuestion == None: 
               if(("qsn_add" in questions_name) and (request.form.get(questions_name)!="")):
                    insert_value  = questions_tbl(questions=request.form.get(questions_name), question_type="short", options=None)  
                    db.session.add(insert_value)
                    # db.session.flush()          
                    db.session.commit()
                    option_for_column[request.form.get(questions_name)]=None

        if request.form != "" :          
            insert_form =feedback_formCreation(formName= request.form.get('form_name'), questions= option_for_column, options=None)
            db.session.add(insert_form)          
            db.session.commit()
            flash(request.form.get('form_name')+' Form created added')
        return redirect (url_for('NewFeedbackForm'))
 
    return render_template("NewForm.html", questions_list= db.session.query(questions_tbl).all()) 

@app.route('/form_send', methods=["GET", "POST"])
@login_required
def form_send():
    if request.method=='POST':
        email = request.form.get('email')
        form_id= request.form.get('id')
        
        sel_id= int(form_id)
        

        token = s.dumps(form_id, salt='Taking_Feedback')
        print(token)
        link = url_for('taking_form', token=token, _external=True) 

        # with mail.connect() as conn:
        #     for email in request.form.get('email').split(","):
        #         subject = "Please Fill The Form"
        #         msg = Message(subject,recipients=[email] ,sender='kshobhana11@gmail.com' ) 
        #         msg.body = 'Your link is {}'.format(link)

        #         conn.send(msg)


        subject = "Please Fill The Form"

        msg = Message(subject,recipients=[email] ,sender='kshobhana11@gmail.com' ) 
        msg.body = 'Your link is {}'.format(link)
        
        mail.send(msg)    
        # return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token) 
        return '<h2>Form sent..<a class="nav-item nav-link " href="/form_send">Back</a></h2>'
        

    return render_template("formSend.html", forms= db.session.query(feedback_formCreation).all(), sub_users= db.session.query(Add_SubUsers).all())

@app.route('/taking_form/<token>', methods=['GET'])
def taking_form(token):
    try:
        id = s.loads(token, salt='Taking_Feedback', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    # return '<h1>Hello mona my code has worked ! </h1>'
      
    return render_template('form_toBe_fill.html', form= db.session.query(feedback_formCreation).filter(feedback_formCreation.formID==int(id)).all())   

@app.route('/get_response', methods=['GET', 'POST'])
def get_response():
    if request.method=='POST':
        responses=request.form
        form_name= request.form.get('formName')
        email= request.form.get('email')
        users_responses={}
        print("the responses are",responses)
        res_keys= list(responses.keys())

        a=2
        for row in responses:
            if row== res_keys[a]:
               users_responses[row]= responses[row]
               a+=1           

        print(users_responses)    

        # res = es.search(index="test-index", body={"query": {"match_all": {}}})

        # sq=email
        # doc=[sq.split('@')[0]]
        # doc= "".join(doc)

        
        # print(doc)
        # new_index = es.index(index=form_name,  doc = users_responses)

            
        # return render_template('show_responses.html', form=responses)
        return '<h2>Form submitted</h2>'


@app.route('/deleteFrm/<id>', methods=["GET"])
@login_required
def deleteFrm(id): 
    db.session.query(feedback_formCreation).filter(feedback_formCreation.formID==id).delete()
    # db.session.delete(record)
    db.session.commit()
    flash("Form Deleted Successfully")
    return redirect (url_for('form_send'))