from models import db, Todo


class TaskService:

    @staticmethod
    def create_task(user_id, content):

        task = Todo(
            content=content,
            user_id=user_id
        )

        db.session.add(task)
        db.session.commit()

        return task

@staticmethod
def delete_task(task):

    db.session.delete(task)
    db.session.commit()

@staticmethod
def update_task(task, content):

    task.content = content

    db.session.commit()

    return task

new_task = Todo(
    content=content,
    user_id=user_id
)

db.session.add(new_task)
db.session.commit()

TaskService.create_task(
    user_id,
    content
)