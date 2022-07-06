from time import sleep
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rq.job import Job
from users.models import CustomUser, Task
from .models import Student
import random
import string
import rq
from faker import Faker


def crud(pk_user):
    # delete all
    Student.objects.all().delete()  # type: ignore
    l = []
    fake = Faker()

    # save
    for _ in range(10000):
        # name = "".join(random.choice(letters) for _ in range(random.randint(10, 30)))
        # last_name = "".join(
        #     random.choice(letters) for _ in range(random.randint(10, 30))
        # )
        name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        age = random.randint(15, 70)
        student = Student(first_name=name, last_name=last_name, age=age, email=email)
        student.save()
        l.append(student.pk)
        print(f"{student} saved")
        sleep(0.001)

    # for pk in l:
    #     s = Student.objects.get(pk=pk)  # type: ignore
    #     s.delete()
    #     print(f"{s} deleted")
    #     sleep(0.001)

    # channel_layer = get_channel_layer()
    # user = CustomUser.objects.filter(pk=pk_user)

    # if user.count() > 0:
    #     user = user[0]
    #     channel_name = user.channel_name
    #     async_to_sync(channel_layer.send)(
    #         channel_name, {"type": "success_message", "message": "task is done"}
    #     )
    # job: Job = rq.get_current_job()
    # task: Task = Task.objects.get(pk=job.id)
    # task.status = task.StatusChoices.FINISHED
    # task.save()
    #
    # print(f"fetched task => {task}")
    # print(f"current job => {job}")
    # print(f"user => {user}")
    #
    # return f"{user} - {job} - {task}"


def get_students():
    return Student.objects.all()  # type: ignore
