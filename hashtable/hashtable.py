class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f'HashTableEntry({repr(self.key)},{repr(self.value)})'


class LinkedList:
    def __init__(self):
        self.head = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = [LinkedList()] * capacity
        self.item_count = 0

    def __repr__(self):
        return f"{self.storage}"

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.item_count / len(self.storage)

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # 64 bit fnv offset = 14695981039346656037 = 0xCBF29CE484222325
        hashed = 0xCBF29CE484222325
        #  64 bit fnv prime = 2^40 + 2^8 + 0xb3 = 1099511628211 = 0x100000001b3
        fnv_prime = 0x100000001b3

        for byte in key.encode():
            hashed *= fnv_prime
            hashed ^= byte
            hashed &= 0xffffffffffffffff

        return hashed

    def fnv1a(self, key):
        """
        FNV-1a Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # 64 bit fnv offset = 14695981039346656037 = 0xCBF29CE484222325
        hashed = 0xCBF29CE484222325
        #  64 bit fnv prime = 2^40 + 2^8 + 0xb3 = 1099511628211 = 0x100000001b3
        fnv_prime = 0x100000001b3

        for byte in key.encode():
            hashed ^= byte
            hashed *= fnv_prime
            hashed &= 0xffffffffffffffff

        return hashed

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.

        Some insight into the magic numbers 5381 and 33: 
        https://stackoverflow.com/questions/1579721/why-are-5381-and-33-so-important-in-the-djb2-algorithm
        """

        hashed = 5381

        for byte in key.encode():
            hashed = ((hashed << 5) + hashed) + byte
            # this ^^^ is an optimized version of: hashed = hashed * 33 + byte
            hashed &= 0xffffffff

        return hashed

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """

        # return self.djb2(key) % self.capacity
        # return self.fnv1(key) % self.capacity
        return self.fnv1a(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # find the hash index
        index = self.hash_index(key)

        # if LL is empty
        if self.storage[index].head == None:
            self.storage[index].head = HashTableEntry(key, value)
            self.item_count += 1
            return

        else:
            cur = self.storage[index].head
            # search the list for the key
            while cur.next:
                # if it's there, replace it's value
                if cur.key == key:
                    cur.value = value
                cur = cur.next

            # otherwise add a new node to the list
            cur.next = HashTableEntry(key, value)
            self.item_count += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

        index = self.hash_index(key)
        cur = self.storage[index].head

        if cur.key == key:
            self.storage[index].head = self.storage[index].head.next
            self.item_count -= 1
            return

        while cur.next:
            prev = cur
            cur = cur.next
            if cur.key == key:
                prev.next = cur.next
                self.item_count -= 1
                return None

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """

        index = self.hash_index(key)
        cur = self.storage[index].head

        if cur == None:
            return None

        if cur.key == key:
            return cur.value

        while cur.next:
            cur = cur.next
            if cur.key == key:
                return cur.value
        return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        self.capacity = new_capacity
        new_array = [LinkedList()] * new_capacity

        # iterate through existing array
        for slot in self.storage:
            # grab reference to head from each linked list
            cur = slot.head
            # iterate through linked list
            while cur:
                # generate a new index (capacity has changed - so will index)
                index = self.hash_index(cur.key)
                # check if the current list doesn't have a head, if not add one
                if new_array[index].head == None:
                    new_array[index].head = HashTableEntry(cur.key, cur.value)
                # otherwise add a new node to the list
                else:
                    node = HashTableEntry(cur.key, cur.value)
                    node.next = new_array[index].head
                    new_array[index].head = node 
                cur = cur.next
        self.storage = new_array


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))
    print("item count is: ", ht.item_count)

    # Test deletion
    # for i in range(13, 0, -1):
    #     ht.delete(f"line_{i}")

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, len(ht.storage)+1):
        print(ht.get(f"line_{i}"))

    print("item count is: ", ht.item_count)

    print("")
