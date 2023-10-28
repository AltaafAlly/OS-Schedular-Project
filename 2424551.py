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


#STCF Scheduler
#WORKING STCF

def stcf_scheduler(process_list):
    process_list.sort(key=lambda x: x.arrival_time)

    current_time = 0
    schedule_order = ""

    ready_queue = []
    time_since_last_io = {}

    while process_list or ready_queue:
        while process_list and process_list[0].arrival_time <= current_time:
            ready_queue.append(process_list.pop(0))

        if not ready_queue:
            current_time += 1
            continue

        process = min(ready_queue, key=lambda x: x.duration)
        ready_queue.remove(process)

        if process.io_frequency:
            if process.name not in time_since_last_io:
                time_since_last_io[process.name] = 0

            if time_since_last_io[process.name] == process.io_frequency:
                schedule_order += f"!{process.name} "
                time_since_last_io[process.name] = 0  
            else:
                schedule_order += f"{process.name} "
                process.duration -= 1
                time_since_last_io[process.name] += 1
        else:
            schedule_order += f"{process.name} "
            process.duration -= 1

        current_time += 1

        if process.duration > 0:
            ready_queue.append(process)
        


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
    output = stcf_scheduler(data_set)
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
