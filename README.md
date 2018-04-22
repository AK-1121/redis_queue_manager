<h1>Redis Queue manager</h1>
Queue manager help to set up background tasks to Redis (used as queue)
and with the help of workers execute them.

<b>Requirements:</b> Python 3.5+, Redis

<h3>Getting started</h3>
* Clone project from Github: git clone <br>
* Install Python3 and Redis v.4 if you don't have it on your PC or laptop. Redis can work on a remote machine <br>
* install required Python3 libraries from requirements.txt <br>
* in config.json set credentials to Redis (host, port, database number)<br>
* write needed code for tasks in tasks.py <br>
* run in cli worker manager process. Example: <br>
python worker_manager.py --task_types 'task_download_file_by_url,task_send_push_msg' -n 3 <br>
* in your code instantiate RedisQueue and call enqueue method to set a task (example in example.py)


<h3>Modules</h3>
<h4>Tasks storage (tasks.py)</h4>
Code of every job stores in separate function. Job parameters is passed
to job as valid JSON-string. When you add your own task it is good practise to describe all job params in doc-string
at the begin of job function.
Each job name must starts with "task_".

<h4>Worker manager</h4>
Module in witch done code for running manager for Redis workers. You can run it in cli. <br>
Each manager run workers with the same tasks. If you want to run workers for serving different set of tasks
you can run several worker_manager processes. Example of command: <br>
python worker_manager.py --task_types 'task_download_file_by_url,task_send_push_msg' -n 3 <br>
Possible optional arguments: <br>
* --host - host address of Redis (default: localhost) <br>
* --port - port number of Redis (default: 6379) <br>
* --db - used database number in Redis (default: 0)<br>
* --worker_number - number of workers that will started to serve tasks (default: 1) <br>
* --task_types - list of tasks to serve by workers (comma separated string) <br>
* --sleep_time - sleep time before each worker send new request to Redis about new task for it (in seconds).
It should not be too small cause it may provokes too many request to Redis when worker will have no tasks. (default: 0.5) <br>
* --is_verbose - flag that switches on extra logging (default: False) <br>
* --config - all parameters to workers can be passed through this argument in json format. If this argument is present, other params
other cli params for worker will be ignored <br>


<Author>
Alexey Kuznetsov. Here will be my contacts:...

<h2>License</h2>
This project is licensed under the MIT License - see the LICENSE.md file for details
