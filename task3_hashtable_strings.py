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
        self.slots = [UnorderedList() for _ in range(self.size)]
        self.count = 0

    def hashfunction(self, key, size):
        if isinstance(key, str):
            total = 0
            for ch in key:
                total = (total * 31 + ord(ch)) % size
            return total
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

        current = chain.head
        while current is not None:
            k, v = current.getData()
            if k == key:
                chain.remove((k, v))
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
                    items.append(f"{k!r}:{v!r}")
                    current = current.getNext()
                parts.append(f"[{i}] " + ", ".join(items))
        return "\n".join(parts)


if __name__ == "__main__":
    print("HASH TABLE TESTS (string keys)")

    ht = HashTableChaining()
    print("Initial size:", ht.size)
    print("Initial len:", len(ht))

    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    for w in words:
        ht.put(w, len(w))
    print("\nAfter put string keys:")
    print(ht)
    print("  len:", len(ht))                 
    print("  size:", ht.size)                 
    print("  LF:", round(ht.load_factor(), 3))

    print("\nget('apple'):", ht.get("apple"))    
    print("get('cherry'):", ht.get("cherry"))  
    print("get('xyz'):", ht.get("xyz"))         

    print("\n'banana' in ht:", "banana" in ht)   
    print("'xyz' in ht:", "xyz" in ht)         

    #  update 
    ht.put("apple", 999)
    print("\nAfter put('apple', 999):")
    print("  get('apple'):", ht.get("apple"))  
    print("  len:", len(ht))       

    del ht["banana"]
    print("\nAfter del ht['banana']:")
    print("  'banana' in ht:", "banana" in ht)  
    print("  len:", len(ht))     

    print("\nKeyError test")
    try:
        del ht["xyz"]
    except KeyError as e:
        print("Raised KeyError as expected:", e)

    print("\nMixed keys (int + str)")
    ht2 = HashTableChaining()
    ht2.put("one", 1)
    ht2.put(2, "two")
    ht2.put("three", 3)
    ht2.put(4, "four")
    print("  get('one'):", ht2.get("one")) 
    print("  get(2):", ht2.get(2))            
    print("  get('three'):", ht2.get("three"))
    print("  get(4):", ht2.get(4))          
    print("  len:", len(ht2))    

    print("\nAUTO GROW (many string keys)")
    ht3 = HashTableChaining()
    for i in range(20):
        ht3.put(f"key{i}", i)
    print(f"  after 20 inserts: size={ht3.size}, len={len(ht3)}, "
          f"LF={ht3.load_factor():.2f}")

    ok = all(ht3.get(f"key{i}") == i for i in range(20))
    print("  All 20 string keys correct:", ok)