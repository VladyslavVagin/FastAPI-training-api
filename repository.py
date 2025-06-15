from sqlalchemy import select
from database import new_session, TaskOrm
from schemas import STaskAdd, STask

class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()  # Ensure the task is added to the session
            await session.commit()
            return task.id
            
        
        
    @classmethod
    async def get_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            tasks = result.scalars().all()
            tasks_schemas = [STask.model_validate(task, from_attributes=True) for task in tasks]
            return tasks_schemas