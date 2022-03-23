import multiprocessing as mp
import time

# print(__name__)


def f(q):
    time.sleep(5)
    q.put(3)
    print('get input')


if __name__ == '__main__':
    queue = mp.Queue()

    p = mp.Process(target=f, args=(queue,))
    p.start()

    try:
        t = queue.get(timeout=1)
    except Exception:
        print('empty')
    else:
        print(t)

