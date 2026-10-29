import hashlib
import os

def file_hash(path, chunk_size=8192):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError) as e:
        print(f"  [skip] {path}: {e}")
        return None

def find_duplicates(directory):
    by_size = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                continue
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            by_size.setdefault(size, []).append(path)

    by_hash = {}
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue 
        for path in paths:
            h = file_hash(path)
            if h is None:
                continue
            by_hash.setdefault(h, []).append(path)

    duplicates = {h: paths for h, paths in by_hash.items() if len(paths) > 1}
    return duplicates


def print_duplicates(duplicates):
    if not duplicates:
        print("No duplicates found.")
        return

    print(f"Found {len(duplicates)} group(s) of duplicates:")
    for i, (h, paths) in enumerate(duplicates.items(), start=1):
        print(f"\n  Group {i}  (hash: {h[:16]}...)")
        for p in paths:
            size = os.path.getsize(p)
            print(f"    {p}  ({size} bytes)")

if __name__ == "__main__":
    import tempfile

    print("DUPLICATE FILE FINDER")

    with tempfile.TemporaryDirectory() as tmp:
        print(f"\nCreating test files in: {tmp}")

        with open(os.path.join(tmp, "unique1.txt"), "w") as f:
            f.write("unique content 1")
        with open(os.path.join(tmp, "unique2.txt"), "w") as f:
            f.write("completely different content 2")

        with open(os.path.join(tmp, "a.txt"), "w") as f:
            f.write("hello duplicate")
        with open(os.path.join(tmp, "b.txt"), "w") as f:
            f.write("hello duplicate")

        subdir = os.path.join(tmp, "sub")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "copy1.dat"), "wb") as f:
            f.write(b"\x00\x01\x02\x03" * 100)
        with open(os.path.join(subdir, "copy2.dat"), "wb") as f:
            f.write(b"\x00\x01\x02\x03" * 100)
        with open(os.path.join(tmp, "copy3.dat"), "wb") as f:
            f.write(b"\x00\x01\x02\x03" * 100)

        with open(os.path.join(tmp, "same_size_A.txt"), "w") as f:
            f.write("AAAA")
        with open(os.path.join(tmp, "same_size_B.txt"), "w") as f:
            f.write("BBBB")

        print("\nFiles created:")
        for root, _, files in os.walk(tmp):
            for name in files:
                print(f"  {os.path.join(root, name)}")

        print("SEARCHING FOR DUPLICATES")
        duplicates = find_duplicates(tmp)
        print_duplicates(duplicates)

        total_files = sum(len(files) for _, _, files in os.walk(tmp))
        dup_files = sum(len(p) for p in duplicates.values())
        print(f"\nSummary:")
        print(f"  Total files:      {total_files}")
        print(f"  Duplicate groups: {len(duplicates)}")
        print(f"  Duplicate files:  {dup_files}")