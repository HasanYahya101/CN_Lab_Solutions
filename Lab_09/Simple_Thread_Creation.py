import threading

# Global thread ID counter and a lock for thread-safe updates
tid = 1
tid_lock = threading.Lock()

def print_thread_id():
    global tid
    with tid_lock:
        current_id = tid
        tid += 1
    print(f"This is Thread {current_id}")

def main():
    # Create two threads
    thread1 = threading.Thread(target=print_thread_id)
    thread2 = threading.Thread(target=print_thread_id)

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
