from threading import Thread, Event
import time


def countdown(n, started_event):
    print('countdown starting')
    started_event.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


# Create the event object that will be used to signal startup
started_event = Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(5, started_event))
t.start()

started_event.wait()
print('countdown is running')
