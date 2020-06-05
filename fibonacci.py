class Fibonacci:
    def __init__(self,max_n):
        self.MaxN = max_n
        self.N = 0
        self.A = 0
        self.B = 1
    def __iter__(self):
        self.N = 0
        self.A = 0
        self.B = 1
        return self
    def __next__(self):
        if self.MaxN > self.N:
            self.N += 1
            self.A, self.B = self.B, self.A + self.B
            return self.A
        else:
            raise StopIteration


l = Fibonacci(6)
for i in l:
    print(i)
