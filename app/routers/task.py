from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from app.database import SessionLocal

from app.models import Task

from app.schemas import TaskCreate


from app.routers.auth import (
    get_current_user
)



router=APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



def get_db():

    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()




# create task

@router.post("/")
def create_task(
    task:TaskCreate,
    db:Session=Depends(get_db),
    user=Depends(get_current_user)
):

    new_task=Task(

        title=task.title,

        user_id=user["id"]

    )


    db.add(new_task)

    db.commit()


    return {

        "message":"Task created"

    }


# get all tasks

@router.get("/")
def get_tasks(

    db:Session=Depends(
        get_db
    ),

    user=Depends(
        get_current_user
    )
):


    tasks=db.query(Task).filter(

        Task.user_id==user["id"]

    ).all()


    return tasks