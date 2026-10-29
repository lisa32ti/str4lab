class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class UnorderedList:

    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    # Доработки

    def append(self, item):
        temp = Node(item)
        if self.head == None:
            self.head = temp
        else:
            current = self.head
            while current.getNext() != None:
                current = current.getNext()
            current.setNext(temp)

    def index(self, item):
        current = self.head
        pos = 0
        while current != None:
            if current.getData() == item:
                return pos
            current = current.getNext()
            pos = pos + 1
        return -1

    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
            return
        if pos >= self.size():
            self.append(item)
            return
        temp = Node(item)
        current = self.head
        previous = None
        count = 0
        while count < pos:
            previous = current
            current = current.getNext()
            count = count + 1
        previous.setNext(temp)
        temp.setNext(current)

    def pop(self, pos=None):
        if self.isEmpty():
            raise IndexError("pop from empty list")
        if pos is None:
            pos = self.size() - 1
        if pos == 0:
            data = self.head.getData()
            self.head = self.head.getNext()
            return data
        current = self.head
        previous = None
        count = 0
        while count < pos:
            previous = current
            current = current.getNext()
            count = count + 1
        data = current.getData()
        previous.setNext(current.getNext())
        return data

    def __str__(self):
        items = []
        current = self.head
        while current != None:
            items.append(str(current.getData()))
            current = current.getNext()
        return "[" + ", ".join(items) + "]"

    def slice(self, start, stop):
        result = UnorderedList()
        temp_items = []
        current = self.head
        pos = 0
        while current != None:
            if start <= pos < stop:
                temp_items.append(current.getData())
            current = current.getNext()
            pos = pos + 1
        for item in reversed(temp_items):
            result.add(item)
        return result


if __name__ == "__main__":
    mylist = UnorderedList()
    mylist.add(31); mylist.add(77); mylist.add(17)
    mylist.add(93); mylist.add(26); mylist.add(54)
    print("List:", mylist)
    print("size:", mylist.size())
    print("index(93):", mylist.index(93))
    mylist.append(100)
    print("append(100):", mylist)
    mylist.insert(2, 999)
    print("insert(2, 999):", mylist)
    print("pop():", mylist.pop())
    print("pop(0):", mylist.pop(0))
    print("slice(1,4):", mylist.slice(1, 4))