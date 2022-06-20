from django.shortcuts import render
import django_rq
from .models import Task

# Create your views here.


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

    return render(req, "result.html", {"tasks": l})
