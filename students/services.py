from time import sleep
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rq.job import Job
from users.models import CustomUser, Task
from .models import Student
import random
import string
import rq


def crud(pk_user):
    # delete all
    Student.objects.all().delete()  # type: ignore
    l = []

    # save
    letters = string.ascii_lowercase
    for _ in range(1000):
        name = "".join(random.choice(letters) for _ in range(random.randint(4, 10)))
        last_name = "".join(
            random.choice(letters) for _ in range(random.randint(4, 10))
        )
        age = random.randint(15, 70)
        student = Student(first_name=name, last_name=last_name, age=age)
        student.save()
        l.append(student.pk)
        print(f"{student} saved")
        sleep(0.001)

    for pk in l:
        s = Student.objects.get(pk=pk)  # type: ignore
        s.delete()
        print(f"{s} deleted")
        sleep(0.001)

    channel_layer = get_channel_layer()
    user = CustomUser.objects.get(pk=pk_user)
    channel_name = user.channel_name
    async_to_sync(channel_layer.send)(
        channel_name, {"type": "success_message", "message": "task is done"}
    )
    job: Job = rq.get_current_job()
    task: Task = Task.objects.get(pk=job.id)
    task.status = task.StatusChoices.FINISHED
    task.save()

    print(f"fetched task => {task}")
    print(f"current job => {job}")
    print(f"user => {user}")

    return f"{user} - {job} - {task}"


def get_students():
    return Student.objects.all()  # type: ignore
