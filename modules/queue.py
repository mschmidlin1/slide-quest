

from collections import deque



class MyStack():
    def __init__(self):
        self.stack=[]
    def __print__(self):
        print(self.stack)
    def empty(self):
        return not bool(len(self.stack))
    def push(self, element):
        self.stack.append(element)
    def pop(self):
        return self.stack.pop()
    def top(self):
        return self.stack[-1]




class MyQueue():
    def __init__(self):
        self.queue = deque()
    def __print__(self):
        print(self.queue)
    def front(self):
        return self.queue[0]
    def enqueue(self, e):
        self.queue.append(e)
    def dequeue(self):
        return self.queue.popleft()
    def empty(self):
        return not bool(len(self.queue))
    def contains(self, item):
        return item in self.queue