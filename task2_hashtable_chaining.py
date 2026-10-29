from task1_unordered_list import UnorderedList

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def next_prime(n):
    if n <= 2:
        return 2
    candidate = n if n % 2 == 1 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate

class HashTableChaining:

    def __init__(self, initial_size=11):
        self.size = next_prime(initial_size)
        # each slot is a list of (key, value) tuples
        self.slots = [UnorderedList() for _ in range(self.size)]
        self.count = 0

    def hashfunction(self, key, size):
        return key % size

    def load_factor(self):
        return self.count / self.size

    def _resize(self, new_size):
        new_size = next_prime(new_size)
        old_slots = self.slots

        self.size = new_size
        self.slots = [UnorderedList() for _ in range(new_size)]
        self.count = 0

        for chain in old_slots:
            current = chain.head
            while current is not None:
                key, value = current.getData()
                self._put_no_resize(key, value)
                current = current.getNext()

    def _maybe_grow(self):
        if self.load_factor() > 0.7:
            self._resize(self.size * 2)

    def _maybe_shrink(self):
        if self.size > 11 and self.load_factor() < 0.2:
            self._resize(self.size // 2)

    def _put_no_resize(self, key, value):
        index = self.hashfunction(key, self.size)
        chain = self.slots[index]

        current = chain.head
        while current is not None:
            k, _ = current.getData()
            if k == key:
                current.setData((key, value))
                return
            current = current.getNext()

        chain.add((key, value))
        self.count += 1

    def put(self, key, value):
        self._put_no_resize(key, value)
        self._maybe_grow()

    def get(self, key):
        index = self.hashfunction(key, self.size)
        chain = self.slots[index]

        current = chain.head
        while current is not None:
            k, v = current.getData()
            if k == key:
                return v
            current = current.getNext()
        return None

    def __len__(self):
        return self.count

    def __contains__(self, key):
        index = self.hashfunction(key, self.size)
        chain = self.slots[index]

        current = chain.head
        while current is not None:
            k, _ = current.getData()
            if k == key:
                return True
            current = current.getNext()
        return False

    def __delitem__(self, key):
        index = self.hashfunction(key, self.size)
        chain = self.slots[index]

        if not chain.search((key, self.get(key))):
            found = False
            current = chain.head
            while current is not None:
                k, _ = current.getData()
                if k == key:
                    found = True
                    break
                current = current.getNext()
            if not found:
                raise KeyError(key)

        current = chain.head
        while current is not None:
            k, _ = current.getData()
            if k == key:
                chain.remove(current.getData())
                self.count -= 1
                self._maybe_shrink()
                return
            current = current.getNext()

        raise KeyError(key)

    def __str__(self):
        parts = []
        for i in range(self.size):
            chain = self.slots[i]
            if not chain.isEmpty():
                items = []
                current = chain.head
                while current is not None:
                    k, v = current.getData()
                    items.append(f"{k}:{v}")
                    current = current.getNext()
                parts.append(f"[{i}] " + ", ".join(items))
        return "\n".join(parts)


if __name__ == "__main__":
    print("HASH TABLE TESTS (chaining)")

    ht = HashTableChaining()
    print("Initial size:", ht.size) 
    print("Initial len:", len(ht))  

    for i in [54, 26, 93, 17, 77, 31]:
        ht.put(i, i * i)
    print("\nAfter put 54,26,93,17,77,31:")
    print("  len:", len(ht))             
    print("  size:", ht.size)             
    print("  LF:", round(ht.load_factor(), 3))
    print("  chains:")
    print(ht)

    print("\nget(93):", ht.get(93))  
    print("get(99):", ht.get(99))    

    print("\n93 in ht:", 93 in ht)  
    print("99 in ht:", 99 in ht)  

    del ht[93]
    print("\nAfter del ht[93]:")
    print("  len:", len(ht))       
    print("  93 in ht:", 93 in ht) 

    print("\nAUTO GROW (LF > 0.7)")
    ht = HashTableChaining()
    for i in range(1, 15):
        ht.put(i, i * 10)
        if i in (7, 8, 9, 10, 11, 12, 13, 14):
            print(f"  after {i} items: size={ht.size:>3}, len={len(ht):>2}, "
                  f"LF={ht.load_factor():.2f}")

    print("\nAUTO SHRINK (LF < 0.2)")
    for i in range(1, 13):
        if i in ht:
            del ht[i]
        if i % 2 == 0:
            print(f"  after deleting {i}: size={ht.size:>3}, len={len(ht):>2}, "
                  f"LF={ht.load_factor():.2f}")

    print("\nData integrity after resizes")
    ht = HashTableChaining()
    for i in range(1, 50):
        ht.put(i, i * i)
    ok = all(ht.get(i) == i * i for i in range(1, 50))
    print("All 49 keys correct after resizes:", ok)

    print("\nKeyError test")
    try:
        del ht[999]
    except KeyError as e:
        print("Raised KeyError as expected:", e)