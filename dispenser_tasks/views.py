from django.shortcuts import render
from main.api.dispenser_task import dispenser_task_init, dispenser_task_status

def dispenser_tasks(request):

    # dispenser = dispenser_task_init()
    # print(dispenser)
    taskid='8fc39d82-5d32-49fa-9bcd-fa1bfe3e78f9'
    task_status = dispenser_task_status(taskid)


    return render(request, 'dispenser-tasks.html')
