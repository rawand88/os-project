from typing import List, Tuple

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.execution_intervals = []

def read_processes_from_file(filename: str) -> List[Process]:
    processes = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            pid, arrival_time, burst_time = map(int, line.strip().split())
            process = Process(pid, arrival_time, burst_time)
            processes.append(process)
    return processes
def run_fcfs(processes: List[Process], context_switch_time: int):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        process.execution_intervals.append((current_time, current_time + process.burst_time))
        current_time += process.burst_time + context_switch_time

def run_rr(processes: List[Process], quantum: int, context_switch_time: int):
    if not processes:
        print("Error: No processes to schedule.")
        return
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = []
    current_time = 0
    idx = 0
    completed = 0
    while completed < len(processes):
        while idx < len(processes) and processes[idx].arrival_time <= current_time:
            ready_queue.append(idx)
            idx += 1
        if not ready_queue:
            current_time = processes[idx].arrival_time
            continue
        current_process_idx = ready_queue.pop(0)
        current_process = processes[current_process_idx]
        start_time = current_time
        execute_time = min(quantum, current_process.remaining_burst_time)
        current_time += execute_time
        current_process.remaining_burst_time -= execute_time
        if current_process.remaining_burst_time > 0:
            ready_queue.append(current_process_idx)
        else:
            completed += 1
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        current_process.execution_intervals.append((start_time, current_time))
        if ready_queue or current_process.remaining_burst_time > 0:
            current_time += context_switch_time

def run_srt(processes: List[Process], context_switch_time: int):
    if not processes:
        print("Error: No processes to schedule.")
        return
    processes.sort(key=lambda x: x.arrival_time)
    pq = []
    current_time = 0
    idx = 0
    completed = 0
    while completed < len(processes):
        while idx < len(processes) and processes[idx].arrival_time <= current_time:
            pq.append((processes[idx].remaining_burst_time, idx))
            idx += 1
        if not pq:
            current_time = processes[idx].arrival_time
            continue
        process_idx = min(range(len(pq)), key=lambda i: pq[i][0])
        process_idx = pq.pop(process_idx)[1]
        current_process = processes[process_idx]
        start_time = current_time
        current_time += 1
        current_process.remaining_burst_time -= 1
        if current_process.remaining_burst_time > 0:
            pq.append((current_process.remaining_burst_time, process_idx))
        else:
            completed += 1
            current_process.turnaround_time = current_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        current_process.execution_intervals.append((start_time, current_time))
        if pq:
            current_time += context_switch_time

def generate_gantt_chart(processes: List[Process], context_switch_time: int):
    # Collect all intervals
    intervals = []
    for process in processes:
        intervals.extend((process.pid, start, end) for start, end in process.execution_intervals)

    # Sort intervals by start time
    intervals.sort(key=lambda x: x[1])

    # Print the top border of the Gantt chart
    print("Gantt Chart:")
    for _ in intervals:
        print("+-----", end="")
    print("+")

    # Print the process IDs in the Gantt chart
    for pid, _, _ in intervals:
        print(f"| P{pid:2} ", end="")
    print("|")

    # Print the bottom border of the Gantt chart
    for _ in intervals:
        print("+-----", end="")
    print("+")

    # Print the time intervals in the Gantt chart
    current_time = 0
    for _, start, end in intervals:
        if start > current_time:
            print(f"{current_time:2}    {start:2}", end="")
        print(f"   {end:2}", end="")
        current_time = end
    print()

def display_results(processes: List[Process]):
    print("Process\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print("P{:>2}\t{:>12}\t{:>10}\t{:>12}\t{:>16}".format(process.pid, process.arrival_time, process.burst_time,
                                                              process.waiting_time, process.turnaround_time))

if __name__ == "__main__":
    filename = "input.txt"
    context_switch_time = 0
    quantum = 4

    processes = read_processes_from_file(filename)

    # FCFS
    run_fcfs(processes, context_switch_time)
    print("First-Come First-Served (FCFS) Results:")
    display_results(processes)
    generate_gantt_chart(processes, context_switch_time)

    # Reset process states
    for process in processes:
        process.remaining_burst_time = process.burst_time
        process.waiting_time = 0
        process.turnaround_time = 0
        process.execution_intervals = []

    # SRT
    run_srt(processes, context_switch_time)
    print("Shortest Remaining Time (SRT) Results:")
    display_results(processes)
    generate_gantt_chart(processes, context_switch_time)

    # Reset process states
    for process in processes:
        process.remaining_burst_time = process.burst_time
        process.waiting_time = 0
        process.turnaround_time = 0
        process.execution_intervals = []

    # RR
    run_rr(processes, quantum, context_switch_time)
    print("Round-Robin (RR) Results:")
    display_results(processes)
    generate_gantt_chart(processes, context_switch_time)
