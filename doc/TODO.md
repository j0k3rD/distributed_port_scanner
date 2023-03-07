## SOME IMPROVEMENTS

- 1 - **SERVER**
    - AUTOSCALE = Fix the 'autoscale' so that when the number of tasks is greater than 2, they go from 2 workers to 16 workers, and when the number drops, they go back to 2. In this way, we can better optimize the use of station resources.

    - REAL TIME = Make the tasks update in real time so we don't have to f5 to see the pending tasks and the completed ones.
    - FIX TASK WITH TWO MACHINES = fix database error when tasks are consumed on remote celery.

- 2 - **UTILITY**
    - ADD MORE UTILITIES = look to not only do port scans but other types of scans and generate more extensive reports.
