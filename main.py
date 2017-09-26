import Task1
import Task2And3

ITEM_COUNT = {
    'albums': 100,
    'photos': 5000,
    'todos': 200,
    'users': 10,
    'posts':100,
    'comments': 500}

task1 = Task1.MakingHttpRequestsTask(ITEM_COUNT)
task1.make_and_save_requests()

Task2And3.task2()
Task2And3.task3()

