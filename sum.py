import sys
import threading

mutex = threading.Semaphore(1)
hash_mutex = threading.Semaphore(1)
multiplex = None
total_sum = 0
list_sums = []
hash_sums = dict()

def do_sum(path, i):
    _sum = 0
    global multiplex
    multiplex.acquire()
    with open(path, 'rb') as f:
        byte = f.read(1)
        while byte:
            _sum += int.from_bytes(byte, byteorder='big', signed=False)
            byte = f.read(1)
    mutex.acquire()
    global total_sum
    total_sum += _sum
    mutex.release()
    print(path + " : " + str(_sum))
    global list_sums
    list_sums[i] = _sum
    multiplex.release()
    global hash_mutex
    hash_mutex.acquire()
    global hash_sums
    if not (_sum in hash_sums):
        hash_sums[_sum] = []
    hash_sums[_sum].append(path)
    hash_mutex.release()

#many error could be raised error. we don't care
if __name__ == "__main__":
    paths = sys.argv[1:]
    n = len(paths)//2
    multiplex = threading.Semaphore(n)
    threads = [None]*(len(paths))
    list_sums = [0]*(len(paths))
    i = 0
    for path in paths:
        try:
            thread = threading.Thread(target=do_sum, args=(path,i, ))
            threads[i] = thread
            i += 1
            print(i)
            thread.start()
        except Exception as e:
            print(f"Erro ao processar {path}: {e}")
    for t in threads:
        t.join()
    print(total_sum)
    for k, v in hash_sums.items():
        if len(v) > 1:
            print(str(k) + " " + str(v))
