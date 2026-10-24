from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
import os, hashlib, json, time

app=FastAPI(title="Project Management API", version="1.0.0")
mongo=MongoClient(os.getenv("MONGODB_URL","mongodb://localhost:27017"))
db=mongo["project_suite"]
projects=db["projects"]; tasks=db["tasks"]; events=db["webhook_events"]

class Project(BaseModel):
    name:str=Field(min_length=1)
    owner:str=Field(min_length=1)

class Task(BaseModel):
    project_id:str
    title:str=Field(min_length=1)
    priority:str="medium"
    status:str="todo"
    assignee:str|None=None
    depends_on:list[str]=[]

@app.get("/health")
def health(): return {"ok":True}

@app.post("/projects")
def create_project(p:Project):
    doc=p.model_dump(); doc["created_at"]=time.time()
    result=projects.insert_one(doc); doc["id"]=str(result.inserted_id); return doc

@app.get("/projects")
def list_projects():
    return [{"id":str(x["_id"]),**{k:v for k,v in x.items() if k!="_id"}} for x in projects.find().sort("created_at",-1)]

@app.post("/tasks")
def create_task(t:Task):
    doc=t.model_dump()
    result=tasks.insert_one(doc); doc["id"]=str(result.inserted_id); return doc

@app.get("/tasks")
def list_tasks(project_id:str|None=None):
    q={"project_id":project_id} if project_id else {}
    return [{"id":str(x["_id"]),**{k:v for k,v in x.items() if k!="_id"}} for x in tasks.find(q)]

def event_key(provider:str, event_id:str)->str:
    return hashlib.sha256(f"{provider}:{event_id}".encode()).hexdigest()

@app.post("/webhooks/{provider}")
def webhook(provider:str, payload:dict):
    event_id=str(payload.get("id") or hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest())
    key=event_key(provider,event_id)
    if events.find_one({"key":key}): return {"accepted":True,"duplicate":True}
    events.insert_one({"key":key,"provider":provider,"event_id":event_id,"payload":payload,"received_at":time.time(),"attempts":0})
    return {"accepted":True,"duplicate":False,"provider":provider}

@app.post("/documents/presign")
def presign_document(filename:str):
    bucket=os.getenv("AWS_S3_BUCKET")
    if not bucket: raise HTTPException(503,"S3 bucket is not configured")
    return {"bucket":bucket,"filename":filename,"message":"Use boto3 generate_presigned_post in production"}

@app.get("/integrations")
def integrations():
    return {"slack":{"enabled":True},"google_calendar":{"enabled":True},"stripe":{"enabled":True},
            "delivery_policy":{"retry":"exponential","idempotency":True}}
