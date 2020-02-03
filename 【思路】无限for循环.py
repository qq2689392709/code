class fo:
    def __init__(self,x=0):
        self.x = x
        self.y = -1
    def __iter__(self):
        return self
    def __next__(self):
        if not isinstance(self.x,int):
            self.y += 1
            return self.x[self.y % len(self.x)]
        else:
            self.x += 1
            return self.x

for i in fo():
    print(i)
