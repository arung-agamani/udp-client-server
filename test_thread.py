from threading import Thread, Event, Timer
import time

def thread_func(name):
    print("Thread %s: starting", name)
    time.sleep(2)
    print("Thread %s: stopping", name)


def set_timeout(callback, timeout):
    timeout_lock_object = True
    callback_thread = threading.Thread(target=callback)
    pass

def clear_timeout(timeout_object):
    pass

def call_func(func_to_call, event: Event):
    

if __name__ == "__main__":
    print("Main function starts")
    x = threading.Thread(target=thread_func, args=(1,))
    x.start()
    print("Main function ends")
