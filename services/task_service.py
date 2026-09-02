from models import db, Todo


class TaskService:

    @staticmethod
    def create_task(user_id, content, priority='media'):

        task = Todo(
            content=content,
            user_id=user_id,
            priority=priority
        )

        db.session.add(task)
        db.session.commit()

        return task

    @staticmethod
    def update_task(task, content, priority=None):

        task.content = content

        if priority is not None:
            task.priority = priority

        db.session.commit()

        return task

    @staticmethod
    def delete_task(task):

        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def move_task(task, status):

        task.status = status

        db.session.commit()

        return task