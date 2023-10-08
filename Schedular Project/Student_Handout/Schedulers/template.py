import sys
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Define the process data clas
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency


#FCFS Scheduler first one
#WORKING FCFS
def fcfs_scheduler(process_list):
    # sort the processes based on their arrival time
    process_list.sort(key=lambda x: x.arrival_time)

    # variable to store the scheduled tasks in order
    schedule_order = ""

    for process in process_list:
        # counter to keep track of time units since the last I/O for this process
        time_since_last_io = 0

        # schedule the process and handle I/O
        while process.duration > 0:
            # check if we need to schedule I/O
            if process.io_frequency and time_since_last_io == process.io_frequency:
                schedule_order += f"!{process.name} "
                time_since_last_io = 0  # reset the counter
            else:
                schedule_order += f"{process.name} "
                process.duration -= 1
                time_since_last_io += 1

    return schedule_order.strip()

# #FCFS scheduler second one optomized
# def fcfs_scheduler(process_list):
#     # Sort the processes based on their I/O frequency (ascending order)
#     process_list.sort(key=lambda x: x.io_frequency)

#     # Use a list comprehension to generate the schedule order
#     schedule_order = []

#     for process in process_list:
#         for i in range(process.duration):
#             io_event = ''
#             if process.io_frequency > 0 and i % process.io_frequency == 0:
#                 io_event = f" !{process.name}"
#             schedule_order.append(f"{process.name}{io_event}")

#     return ' '.join(schedule_order).strip()





#STCF Scheduler
#WORKING STCF

def stcf_scheduler(process_list):
    # sort the processes based on their arrival time for initial processing
    process_list.sort(key=lambda x: x.arrival_time)

    current_time = 0
    schedule_order = ""

    # this will hold processes that have arrived but haven't finished executing
    ready_queue = []
    # Initialize a dictionary to track the time since the last I/O for each process
    time_since_last_io = {}

    while process_list or ready_queue:
        # add processes to the ready queue that have arrived
        while process_list and process_list[0].arrival_time <= current_time:
            ready_queue.append(process_list.pop(0))

        if not ready_queue:  # if there's no process in the ready queue, just move time forward
            current_time += 1
            continue

        # select the process with the shortest duration left
        process = min(ready_queue, key=lambda x: x.duration)
        ready_queue.remove(process)

        # Check if it's time for I/O for the current process
        if process.io_frequency:
            if process.name not in time_since_last_io:
                time_since_last_io[process.name] = 0

            if time_since_last_io[process.name] == process.io_frequency:
                schedule_order += f"!{process.name} "
                time_since_last_io[process.name] = 0  # Reset the counter
            else:
                schedule_order += f"{process.name} "
                process.duration -= 1
                time_since_last_io[process.name] += 1
        else:
            schedule_order += f"{process.name} "
            process.duration -= 1

        current_time += 1

        # Check if the process has completed
        if process.duration > 0:
            ready_queue.append(process)
        


    return schedule_order.strip()



#MLFQ Scheduler
#NOT WORKING MLFQ

# def mlfq_scheduler(process_list):
#     process_list.sort(key=lambda x: x.arrival_time)

#     current_time = 0
#     schedule_order = ""

#     ready_queue_1 = []  # for I/O-bound processes (shorter quantum)
#     ready_queue_2 = []  # for CPU-bound processes (longer quantum)

#     quantum_1 = 2
#     quantum_2 = 8

#     while process_list or ready_queue_1 or ready_queue_2:
#         while process_list and process_list[0].arrival_time <= current_time:
#             ready_queue_1.append(process_list.pop(0))

#         if not ready_queue_1 and not ready_queue_2:
#             current_time = process_list[0].arrival_time
#             continue

#         # First serve processes in ready_queue_1
#         if ready_queue_1:
#             process = ready_queue_1.pop(0)
#             time_spent = 0
#             while time_spent < quantum_1 and process.duration > 0:
#                 if process.io_frequency and time_spent > 0 and time_spent % process.io_frequency == 0:
#                     schedule_order += f"!{process.name} "
#                     process.duration -= 1  # Process an I/O operation
#                 else:
#                     schedule_order += f"{process.name} "
#                     process.duration -= 1
#                 time_spent += 1
#                 current_time += 1

#             # if the process still has duration, move to queue 2
#             if process.duration > 0:
#                 ready_queue_2.append(process)

#         # Then serve processes in ready_queue_2 if ready_queue_1 is empty
#         elif ready_queue_2:
#             process = ready_queue_2.pop(0)
#             time_spent = 0
#             while time_spent < quantum_2 and process.duration > 0:
#                 if process.io_frequency and time_spent > 0 and time_spent % process.io_frequency == 0:
#                     schedule_order += f"!{process.name} "
#                     process.duration -= 1  # Process an I/O operation
#                 else:
#                     schedule_order += f"{process.name} "
#                     process.duration -= 1
#                 time_spent += 1
#                 current_time += 1

#             # place back in queue 2 if the quantum is exhausted
#             if process.duration > 0:
#                 ready_queue_2.append(process)

#     return schedule_order.strip()

def mlfq_scheduler(process_list):
    process_list.sort(key=lambda x: x.arrival_time)

    current_time = 0
    schedule_order = ""

    ready_queue_1 = []  # High priority (shortest quantum)
    ready_queue_2 = []  # Medium priority
    ready_queue_3 = []  # Low priority (longest quantum)

    quantum_1 = 2
    quantum_2 = 4
    quantum_3 = 8

    while process_list or ready_queue_1 or ready_queue_2 or ready_queue_3:
        while process_list and process_list[0].arrival_time <= current_time:
            ready_queue_1.append(process_list.pop(0))

        if not ready_queue_1 and not ready_queue_2 and not ready_queue_3:
            current_time = process_list[0].arrival_time
            continue

        # First serve processes in ready_queue_1
        if ready_queue_1:
            process = ready_queue_1.pop(0)
            execute_process(process, quantum_1, schedule_order, current_time, ready_queue_2)

        # Then serve processes in ready_queue_2 if ready_queue_1 is empty
        elif ready_queue_2:
            process = ready_queue_2.pop(0)
            execute_process(process, quantum_2, schedule_order, current_time, ready_queue_3)

        # Lastly, serve processes in ready_queue_3 if ready_queue_1 and ready_queue_2 are empty
        elif ready_queue_3:
            process = ready_queue_3.pop(0)
            execute_process(process, quantum_3, schedule_order, current_time, ready_queue_3)  # Put it back to ready_queue_3 if not finished

    return schedule_order.strip()

def execute_process(process, quantum, schedule_order, current_time, next_queue):
    time_spent = 0
    while time_spent < quantum and process.duration > 0:
        if process.io_frequency and time_spent > 0 and time_spent % process.io_frequency == 0:
            schedule_order += f"!{process.name} "
            process.duration -= 1  # Process an I/O operation
        else:
            schedule_order += f"{process.name} "
            process.duration -= 1
        time_spent += 1
        current_time += 1

    # if the process still has duration, move to next queue
    if process.duration > 0:
        next_queue.append(process)




def main():
    # Check if the correct number of arguments is provided
    import sys
    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1


    """
    TODO Your Algorithm - assign your output to the output variable
    """


    #output = "AB AC AB !AD BA CB !BL BX AB" #Example output
    #output = fcfs_scheduler(data_set)
    #output = stcf_scheduler(data_set)
    output = mlfq_scheduler(data_set)

    """
    End of your algorithm
    """

    

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
