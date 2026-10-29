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


class HashTable:

    def __init__(self, initial_size=11):
        self.size = next_prime(initial_size)
        self.slots = [None] * self.size 
        self.data = [None] * self.size 
        self.count = 0 

    def hashfunction(self, key, size):
        return key % size

    def rehash(self, oldhash, attempt, size):
        return (oldhash + attempt * attempt) % size

    def load_factor(self):
        return self.count / self.size

    def _resize(self, new_size):
        new_size = next_prime(new_size)
        old_slots, old_data = self.slots, self.data

        self.size = new_size
        self.slots = [None] * new_size
        self.data = [None] * new_size
        self.count = 0

        for key, value in zip(old_slots, old_data):
            if key is not None:
                self._put_no_resize(key, value)

    def _maybe_grow(self):
        if self.load_factor() > 0.7:
            self._resize(self.size * 2)

    def _maybe_shrink(self):
        if self.size > 11 and self.load_factor() < 0.2:
            self._resize(self.size // 2)

    def _put_no_resize(self, key, value):
        hashvalue = self.hashfunction(key, self.size)

        if self.slots[hashvalue] is None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = value
            self.count += 1
            return

        if self.slots[hashvalue] == key:
            self.data[hashvalue] = value
            return

        attempt = 1
        nextslot = self.rehash(hashvalue, attempt, self.size)
        while self.slots[nextslot] is not None and self.slots[nextslot] != key:
            attempt += 1
            nextslot = self.rehash(hashvalue, attempt, self.size)
            if attempt > self.size: 
                raise RuntimeError("Hash table is full")

        if self.slots[nextslot] is None:
            self.slots[nextslot] = key
            self.data[nextslot] = value
            self.count += 1
        else:
            self.data[nextslot] = value 

    def put(self, key, value):
        self._maybe_grow()
        self._put_no_resize(key, value)

    def get(self, key):
        start = self.hashfunction(key, self.size)
        if self.slots[start] == key:
            return self.data[start]

        attempt = 1
        pos = self.rehash(start, attempt, self.size)
        while self.slots[pos] is not None and self.slots[pos] != key:
            attempt += 1
            pos = self.rehash(start, attempt, self.size)
            if attempt > self.size:
                return None

        if self.slots[pos] == key:
            return self.data[pos]
        return None

    def __len__(self):
        return self.count

    def __contains__(self, key):
        return self.get(key) is not None

    def __delitem__(self, key):
        start = self.hashfunction(key, self.size)
        pos = start
        attempt = 0

        while self.slots[pos] is not None:
            if self.slots[pos] == key:
                break
            attempt += 1
            pos = self.rehash(start, attempt, self.size)
            if attempt > self.size:
                raise KeyError(key)

        if self.slots[pos] != key:
            raise KeyError(key)

        self.slots[pos] = None
        self.data[pos] = None
        self.count -= 1

        self._rehash_after_delete()

        self._maybe_shrink()

    def _rehash_after_delete(self):
        old_slots, old_data = self.slots, self.data
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.count = 0
        for key, value in zip(old_slots, old_data):
            if key is not None:
                self._put_no_resize(key, value)

    def __str__(self):
        pairs = []
        for i in range(self.size):
            if self.slots[i] is not None:
                pairs.append(f"{self.slots[i]}:{self.data[i]}")
        return "{" + ", ".join(pairs) + "}"


if __name__ == "__main__":
    print("HASH TABLE TESTS (quadratic probing)")

    ht = HashTable()
    print("Initial size:", ht.size)      
    print("Initial len:", len(ht))     

    for i in [54, 26, 93, 17, 77, 31]:
        ht.put(i, i * i)
    print("\nAfter put 54,26,93,17,77,31:")
    print("  table:", ht)
    print("  len:", len(ht))     
    print("  size:", ht.size)         
    print("  LF:", round(ht.load_factor(), 3))

    print("\nget(93):", ht.get(93))      
    print("get(99):", ht.get(99))      

    print("\n93 in ht:", 93 in ht)       
    print("99 in ht:", 99 in ht)      

    del ht[93]
    print("\nAfter del ht[93]:")
    print("  len:", len(ht))      
    print("  93 in ht:", 93 in ht)   

    print("\nAUTO GROW (LF > 0.7)")
    ht = HashTable()
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
    ht = HashTable()
    for i in range(1, 50):
        ht.put(i, i * i)
    ok = all(ht.get(i) == i * i for i in range(1, 50))
    print("All 49 keys correct after resizes:", ok)

    print("\nKeyError test")
    try:
        del ht[999]
    except KeyError as e:
        print("Raised KeyError as expected:", e)