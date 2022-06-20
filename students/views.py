from django.shortcuts import render, redirect
import django_rq
from rq.job import Job
from users.models import Task
from .services import get_students, crud
import django_rq

# Create your views here.


def index(req):
    context = {"students": get_students()}
    return render(req, "students.html", context)


def test(req):
    if not req.method == "POST":
        return render(req, "test.html")

    q = django_rq.get_queue()
    job: Job = q.enqueue(crud, req.user.pk)
    Task(task_id=job.id).save()

    return redirect("main")


def result(req):

    tasks: list[Task] = Task.objects.filter(status=Task.StatusChoices.FINISHED)  # type: ignore
    queue = django_rq.get_queue()
    l = []
    for task in tasks:
        job = queue.fetch_job(task.task_id)
        if job and job.result:
            l.append(job)
        else:
            task.delete()

    return render(req, "other.html", {"tasks": l})
