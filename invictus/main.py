
import json
#from sqlalchemy.engine import URL
import io
from io import StringIO
from fastapi import FastAPI ,Form,Request,Depends,File,UploadFile
from fastapi.responses import JSONResponse ,HTMLResponse,PlainTextResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List
import uvicorn
import joblib
import pandas as pd
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.staticfiles import StaticFiles
templates = Jinja2Templates(directory="templates")


# Define a model
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    username = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    password = Column(String(50),nullable=False)















model=joblib.load('Classify1.joblib')
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"),name='static')




# Create an SQLite database in memory for demonstration purposes
# engine = create_engine(url)



   

                
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    password = Column(String(50), nullable=False)

class Institute(Base):
    __tablename__ = 'institute1'
    name = Column(String,  primary_key=True)
    city = Column(String(50))
    state = Column(String(20))
    course1 = Column(String(50))
    course2 = Column(String(50))

class Recruiter(Base):
    __tablename__ = 'job1'
    id=Column(Integer,primary_key=True)
    name = Column(String(100))
    city = Column(String(50))
    role= Column(String(50))
    

# Create an SQLite in-memory database for testing purposes
DATABASE_URL = "sqlite:///./in.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Dependency function to get a database session
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return db()

@app.get('/',response_class=HTMLResponse)
def user(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/contact',response_class=HTMLResponse)
def user(request:Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get('/user',response_class=HTMLResponse)
def user(request:Request):
    return templates.TemplateResponse("userData.html", {"request": request})

@app.post('/classify',response_class=HTMLResponse)
def classify(request:Request,med:int=Form(...),fed:int=Form(...),ss:int=Form(...),fs:int=Form(...),city:str=Form(...),db: Session = Depends(get_db)):


    data=[[med,fed,ss,fs]]
    print(data)
    columns = ['Medu', 'Fedu', 'schoolsup', 'famsup']

# Create a DataFrame
    df = pd.DataFrame(data, columns=columns)

    pred=model.predict(data)
    if pred==[0]:
        p='Student is not at much risk'
    else :
        p='Student is at high risk'
    ot=p
    query_result = db.query(Institute).filter(Institute.city == city).all()
    job=db.query(Recruiter).filter(Recruiter.city==city).all()
    if job ==[]:
        job='no jobs available'

    return templates.TemplateResponse("res.html", {"request": request,"pred":ot,"data":query_result,"job":job})


@app.get('/insti2',response_class=HTMLResponse)
def user(request:Request):
    return templates.TemplateResponse("insti.html", {"request": request})

@app.post('/ngo')
async def classify1(request:Request,sheet: UploadFile = File(...)):
    
        content = sheet.file.read()
        csv_data = content.decode('utf-8')

# Use StringIO to create a file-like object
        csv_file = StringIO(csv_data)
        # Now you can process the content as needed, for example, using pandas to read the CSV.
        df = pd.read_csv(csv_file)
        for  row in df.iterrows():
            l=[]
            n=[]
            for index, row in df.iterrows():
                list =[[row['Medu'],row['Fedu'],row['schoolsup'],row['fasup']]]
                name=row['name']
                
                pred=model.predict(list)
                if pred==[0]:
                    x='No'
                else:
                    x='Yes'
                l.append(x)
                n.append(name)
                
                
        
        data3={'At_risk':l,'Student name': n}
        df2=pd.DataFrame(data3)   
        print(df2)   
         
        
        return templates.TemplateResponse("instdisp.html", {"request": request,'data4':df2})



#     # pred=model.predict(data)
#     # if pred==[0]:
#     #     p='Student is not at much risk'
#     # else :
#     #     p='Student is at high risk'
   

#     return JSONResponse('done')


@app.post("/resources")
async def read_item(request:Request,db: Session = Depends(get_db)):
   ins=Institute(name='Ulhasnagar college',city='Mumbai',state='Maharashtra',course1='sales expert',course2='Call center expert')
   db.add(ins)
   db.commit()
    
    
    
   return 'done'

# db=get_db()
# ins=Institute(name='Chembur Technical institute',city='Munbai',state='Maharashtra',course1='Electrician',course2='Mechanic')
# db.add(ins)
# db.commit()
# data=db.query(Institute).all()
# data=jsonable_encoder(data)






if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8221, reload=True)
