<h1>Redis Queue manager</h1>
Queue manager help to set up background tasks to Redis (used as queue)
and with the help of workers execute them.

Requirements: Python 3.5+, Redis

<h3>Modules</h3>
<h4>Tasks storage (tasks.py)</h4>
Code of every job stores in separate function. Job parameters is passed
to job as valid JSON-string

Each job name must starts with "task_".



<Author>
Alexey Kuznetsov. Here will be my contacts:...

<h2>License</h2>
This project is licensed under the MIT License - see the LICENSE.md file for details
