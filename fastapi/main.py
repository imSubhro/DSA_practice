from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "Alice", "age": 20, "class": "Math"},
    2: {"name": "Bob", "age": 22, "class": "Science"},
}


class Student(BaseModel):
    name: str
    age: int
    class_name: str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_name: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student to retrieve")):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name :Optional[str] =None, test:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"message": "Student not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"message": "Student ID already exists"}
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students:
        return {"message": "Student ID does not exist"}
    
    if student.name is not None:
        students[student_id]["name"] = student.name
    
    if student.age is not None:
        students[student_id]["age"] = student.age
    
    if student.year is not None:
        students[student_id]["year"] = student.year
    
    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"message": "Student ID does not exist"}
    del students[student_id]
    return {"message": "Student deleted"}