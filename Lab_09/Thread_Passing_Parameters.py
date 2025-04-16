import threading

def print_thread_id(message):
    print(message)

def main():
    message1 = "Thread 1"
    message2 = "Thread 2"

    # Create and start first thread
    thread1 = threading.Thread(target=print_thread_id, args=(message1,))
    ret1 = thread1.start()
    thread1.join()  # Wait for thread1 to finish

    # Create and start second thread
    thread2 = threading.Thread(target=print_thread_id, args=(message2,))
    ret2 = thread2.start()
    thread2.join()  # Wait for thread2 to finish

if __name__ == "__main__":
    main()
