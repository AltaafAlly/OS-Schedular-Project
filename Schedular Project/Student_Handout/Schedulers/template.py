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

#FCFS Scheduler
def fcfs_scheduler(process_list):
    # sort the processes based on their arrival time
    process_list.sort(key=lambda x: x.arrival_time)

    # variable to track the current time
    current_time = 0

    # variable to store the scheduled tasks in order
    schedule_order = ""

    for process in process_list:
        # if a process arrives after the current time, just move the time forward
        if process.arrival_time > current_time:
            current_time = process.arrival_time

        # schedule the process and handle I/O
        while process.duration > 0:
            # check if we need to schedule I/O
            if process.io_frequency and process.duration % process.io_frequency == 0:
                schedule_order += f"!{process.name} "
                process.duration -= 1
            else:
                schedule_order += f"{process.name} "
                process.duration -= 1

            current_time += 1

    return schedule_order.strip()

#STCF Scheduler

def stcf_scheduler(process_list):
    # sort the processes based on their arrival time for initial processing
    process_list.sort(key=lambda x: x.arrival_time)

    current_time = 0
    schedule_order = ""

    # this will hold processes that have arrived but haven't finished executing
    ready_queue = []

    while process_list or ready_queue:
        # add processes to the ready queue that have arrived
        while process_list and process_list[0].arrival_time <= current_time:
            ready_queue.append(process_list.pop(0))

        if not ready_queue:  # if there's no process in the ready queue, just move time forward
            current_time = process_list[0].arrival_time
            continue

        # select the process with the shortest duration left
        process = min(ready_queue, key=lambda x: x.duration)
        ready_queue.remove(process)

        # check if we need to schedule I/O
        if process.io_frequency and process.duration % process.io_frequency == 0:
            schedule_order += f"!{process.name} "
            current_time += 1
        else:
            schedule_order += f"{process.name} "
            process.duration -= 1
            current_time += 1

        # if the process has not finished executing, return it to the ready queue
        if process.duration > 0:
            ready_queue.append(process)

    return schedule_order.strip()

#MLFQ Scheduler

def mlfq_scheduler(process_list):
    process_list.sort(key=lambda x: x.arrival_time)

    current_time = 0
    schedule_order = ""

    ready_queue_1 = []  # for I/O bound processes (shorter quantum)
    ready_queue_2 = []  # for CPU bound processes (longer quantum)

    quantum_1 = 2
    quantum_2 = 4

    while process_list or ready_queue_1 or ready_queue_2:
        while process_list and process_list[0].arrival_time <= current_time:
            ready_queue_1.append(process_list.pop(0))

        if not ready_queue_1 and not ready_queue_2:
            current_time = process_list[0].arrival_time
            continue

        # First serve processes in ready_queue_1
        if ready_queue_1:
            process = ready_queue_1.pop(0)
            time_spent = 0
            while time_spent < quantum_1 and process.duration > 0:
                if process.io_frequency and process.duration % process.io_frequency == 0:
                    schedule_order += f"!{process.name} "
                    break
                else:
                    schedule_order += f"{process.name} "
                    process.duration -= 1
                    time_spent += 1
                    current_time += 1

            if process.duration > 0:
                if time_spent == quantum_1:
                    ready_queue_2.append(process)
                else:
                    ready_queue_1.append(process)

        # Then serve processes in ready_queue_2 if ready_queue_1 is empty
        elif ready_queue_2:
            process = ready_queue_2.pop(0)
            time_spent = 0
            while time_spent < quantum_2 and process.duration > 0:
                if process.io_frequency and process.duration % process.io_frequency == 0:
                    schedule_order += f"!{process.name} "
                    break
                else:
                    schedule_order += f"{process.name} "
                    process.duration -= 1
                    time_spent += 1
                    current_time += 1

            if process.duration > 0:
                ready_queue_2.append(process)

    return schedule_order.strip()


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
            print(f"Number of processes: {num_processes}")
            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency))
                data_set.append(process)

            # Check if the expected number of processes matches the filename
            # expected_num_processes = int(sys.argv[1].split('_')[1].split('.')[0]) # Extracting '9' from 'data_9.txt'
            # if expected_num_processes != num_processes:
            #     print(f"Expected {expected_num_processes} processes but got {num_processes} processes")
            #     return 1

    except FileNotFoundError:
        print("Error opening the file.")
        return 1

    # Call the FCFS scheduler function to generate the output
    # decide which scheduler to use
    scheduler_type = sys.argv[1].split('_')[0]

    if scheduler_type == "fcfs":
                output = fcfs_scheduler(data_set)
    elif scheduler_type == "stcf":
        output = stcf_scheduler(data_set)
    elif scheduler_type == "mlfq":
        output = mlfq_scheduler(data_set)
    else:
        print("Invalid scheduler name")

    

    # Open a file for writing
    try:
        #output = fcfs_scheduler(data_set)
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)
    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

    """
    TODO Your Algorithm - assign your output to the output variable
    """


    #output = "AB AC AB !AD BA CB !BL BX AB" #Example output


    """
    End of your algorithm
    """
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
