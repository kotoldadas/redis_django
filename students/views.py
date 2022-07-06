from django.http import JsonResponse
from django.shortcuts import render, redirect
import django_rq
from elasticsearch_dsl import Q
from rq.job import Job
from users.models import Task
from .services import get_students, crud
import django_rq
from .documents import StudentDocument

# Create your views here.


def index(req):
    context = {"students": get_students()}
    return render(req, "students.html", context)


def search(req, name):
    q = Q(
        "multi_match",
        query=str(name),
        fields=["first_name", "last_name", "email"],
        fuzziness="auto",
    )
    response = StudentDocument.search().query(q).execute()

    data = {
        "success": response.success(),
        "students": [(s.first_name, s.last_name, s.email) for s in response],
    }
    return JsonResponse(data)


def test(req):
    if not req.method == "POST":
        return render(req, "test.html")

    q = django_rq.get_queue()
    job: Job = q.enqueue(crud, args=(req.user.pk,))
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
