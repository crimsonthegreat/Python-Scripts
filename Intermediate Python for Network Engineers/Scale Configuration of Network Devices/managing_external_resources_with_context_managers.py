import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        print("Timer started...")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        end = time.time()
        print(f"Timer stopped.  Elapsed: {end - self.start:.2f} seconds")

with Timer():
    time.sleep(2)
with Timer():
    time.sleep(30)