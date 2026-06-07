# Vehicle Maintenance Scheduler

## Problem Statement

Given a list of vehicle maintenance tasks, each with:

* Duration (mechanic hours required)
* Impact score (operational importance)

and a depot mechanic-hour budget, determine the subset of tasks that maximizes total impact without exceeding available mechanic hours.

## Approach

This solution uses the 0/1 Knapsack Dynamic Programming algorithm.

For each depot:

1. Fetch depot data from API.
2. Fetch vehicle maintenance tasks from API.
3. Apply Dynamic Programming.
4. Select tasks that maximize impact score.
5. Display:

   * Maximum impact score
   * Total hours used
   * Selected tasks

## Technologies

* Python
* Requests Library
* REST APIs

## Execution

```bash
python app.py
```

## Output

Results are displayed for every depot along with selected maintenance tasks.
