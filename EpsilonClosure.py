# epsilon_closure.py
from collections import deque


def epsilon_closure(fa, initial_state):
    result_state_set = {initial_state, }
    task_state_queue = deque([initial_state])
    while task_state_queue:
        key = (task_state_queue.pop(), 'ε')
        states = fa.delta_functions.get(key)

        if states is None:
            continue

        for state in states:
            if state in result_state_set:
                continue
            task_state_queue.append(state)
            result_state_set.add(state)

    return result_state_set
