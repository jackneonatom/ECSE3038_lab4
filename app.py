from fastapi.middleware.cors import CORSMiddleware
from typing import Optional,Annotated,List
from fastapi import FastAPI,HTTPException,Response
from pydantic import BaseModel, BeforeValidator,Field,TypeAdapter
import uuid
import motor.motor_asyncio
from dotenv import dotenv_values
import datetime
from bson.objectid import ObjectId
import tracemalloc

app = FastAPI()

origins = [ "https://ecse3038-lab3-tester.netlify.app" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = dotenv_values(".env")

client=motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_URL"])
db=client.tank_profile


PyObjectId= Annotated[str,BeforeValidator(str)]


class Tank(BaseModel):
    id: Optional[PyObjectId]=Field(alias="_id",default=None)
    location: Optional[str]=None
    lat: Optional[float]=None
    long: Optional[float]=None

class Profile(BaseModel):
    last_updated:Optional[str]=None
    username: Optional[str]=None
    role: Optional[str]=None
    color: Optional[str]=None


@app.get("/profile")
async def get_profile():
    profiles= await db["profiles"].find().to_list(999)

    return TypeAdapter(List[Profile]).validate_python(profiles)

@app.post("/profile", status_code=201)
async def create_profile(profile: Profile):
    areprofiles= await db["profiles"].find().to_list(999)
    if len(areprofiles)==0:
        the_time=datetime.datetime.now().strftime("%d/%m/%y, %I:%M:%S %p")
        profile_data=profile.model_dump()
        profile_data["last_updated"]=the_time
        new_profile=await db["profiles"].insert_one(profile_data)
        created_profile=await db["profiles"].find_one({"_id":new_profile.inserted_id})
        return Profile(**created_profile)

@app.get("/tank")
async def get_tanks():
    tanks= await db["tanks"].find().to_list(999)
    await update_profile()

    return TypeAdapter(List[Tank]).validate_python(tanks)


@app.get("/tank/{id}")
async def get_tanks_id(id: str):
    a_tank=await db ["tanks"].find_one({"_id":ObjectId(id)})
    await update_profile()
    if a_tank is None:
        raise HTTPException(status_code=404, detail="Tank of id "+ id +" not found")
    return Tank(**a_tank)
    # tanks= await db["tanks"].find().to_list(999)
    return TypeAdapter(List[Tank]).validate_python(tanks)


@app.post("/tank", status_code=201)
async def create_tank(tank: Tank):
   new_tank =await db["tanks"].insert_one(tank.model_dump())

   created_tank=await db["tanks"].find_one({"_id":new_tank.inserted_id})
   await update_profile()

   return Tank(**created_tank)

@app.patch("/tank/{id}",status_code=200)
async def update_tank(id: str, tank_update: Tank):
    tracemalloc.start()
    updated_tank= await db["tanks"].update_one({"_id":ObjectId(id)},{"$set": tank_update.model_dump(exclude_unset=True)})
    await update_profile()

    if updated_tank.modified_count>0:
        patched_tank = await db ["tanks"].find_one({"_id":ObjectId(id)})
        return Tank(**patched_tank)
    raise HTTPException(status_code = 404, detail = "Tank of id: " + id + " not found.")
    

@app.delete("/tank/{id}",status_code=204)
async def delete_tank(id:str):
    deleted_tank = await db["tanks"].delete_one({"_id":ObjectId(id)})
    await update_profile()

    if deleted_tank.deleted_count<1:
        raise HTTPException(status_code=404,detail="Tank of id: "+id+" not found.")


async def update_profile():
    the_time = datetime.datetime.now().strftime("%d/%m/%y, %I:%M:%S %p")
    
    profile_data = await db["profiles"].find().to_list(1)
    
    db["profiles"].update_one(
        {"_id": profile_data[0]["_id"]},
        {"$set": {"last_updated": the_time}},
    )