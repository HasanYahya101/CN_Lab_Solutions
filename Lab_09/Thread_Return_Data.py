import threading

def print_thread_id(message):
    print(message)

def main():
    message1 = "Thread 1"
    message2 = "Thread 2"

    # Create threads
    thread1 = threading.Thread(target=print_thread_id, args=(message1,))
    thread2 = threading.Thread(target=print_thread_id, args=(message2,))

    # Start and join first thread
    thread1.start()
    thread1.join()  # Wait for thread1 to finish

    # Start and join second thread
    thread2.start()
    thread2.join()  # Wait for thread2 to finish

if __name__ == "__main__":
    main()
