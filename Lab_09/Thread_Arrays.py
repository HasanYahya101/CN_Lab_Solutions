import threading

class ThreadStruct:
    def __init__(self, t_msg, tid):
        self.t_msg = t_msg
        self.tid = tid

def print_thread_info(thread_struct):
    print(thread_struct.t_msg, end='')
    print(thread_struct.tid)

def main():
    threads = []
    thread_structs = []

    # Populate thread_structs with data
    for i in range(10):
        thread_structs.append(ThreadStruct("Hi I am thread ", i + 1))

    # Create and start threads
    for i in range(10):
        t = threading.Thread(target=print_thread_info, args=(thread_structs[i],))
        threads.append(t)
        t.start()
        t.join()  # Wait for the current thread to finish before creating the next

if __name__ == "__main__":
    main()
