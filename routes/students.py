from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
from database import db, to_response_id
from models import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_student(student: StudentCreate):
    student_dict = student.dict()
    result = await db.students.insert_one(student_dict)
    return {"id": str(result.inserted_id)}

@router.get("/", response_model=dict)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    filters = {}
    if country:
        filters["address.country"] = country
    if age is not None:
        filters["age"] = {"$gte": age}

    students = await db.students.find(filters, {"name": 1, "age": 1}).to_list(100)

    response_data = [{"name": student["name"], "age": student["age"]} for student in students]

    return {"data": response_data}

@router.get("/{id}", response_model=StudentResponse)
async def fetch_student(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    student = await db.students.find_one({"_id": ObjectId(id)})
    

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student.pop("_id"))
    
    return student

@router.patch("/{id}", status_code=204)
async def update_student(id: str, student_update: StudentUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = {k: v for k, v in student_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    result = await db.students.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

@router.delete("/{id}", status_code=200)
async def delete_student(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = await db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {}
