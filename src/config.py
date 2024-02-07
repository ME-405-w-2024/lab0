import cqueue

def init():
    global square_toggle
    global int_queue

    #Define queue maximum size
    QUEUE_SIZE = 10

    square_toggle = 0
    int_queue = cqueue.IntQueue(QUEUE_SIZE)