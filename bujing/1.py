import multiprocessing as mp
import time

# Read msg from the queue and print it out
def reader(queue):
    while True:
        msg = queue.get()
        # if (msg == 'DONE'):
        #     break
        print("[Reader]Get msg from writer: %s" % msg)

# Write msg with number into the queue
def writer(queue):
    print("[Writer] Sending msg to reader...")
    i = 0
    while True:
        queue.put("Hello <%d>!" % i)
        time.sleep(1)
        i+=1
    #queue.put('DONE')

if __name__=="__main__":
    queue = mp.Queue()
    print("Create new process as reader!")
    reader_p = mp.Process(target=reader, args=((queue),))
    reader_p.daemon = True
    reader_p.start()
    writer(queue)
    #reader_p.join()