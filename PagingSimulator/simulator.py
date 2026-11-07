
from algorithms import fifo, lru, optimal


def test_algorithm(name, function, reference_string, frame_count, expected_faults):

    result = function(reference_string, frame_count)

    hits = sum(step["hit"] for step in result)
    faults = sum(step["fault"] for step in result)

    print(f"\nTesting {name}")
    print("-" * 35)
    print(f"Total References : {len(reference_string)}")
    print(f"Page Hits        : {hits}")
    print(f"Page Faults      : {faults}")
    print(f"Expected Faults  : {expected_faults}")

    assert faults == expected_faults, (
        f"{name} failed! Expected {expected_faults}, got {faults}"
    )

    assert hits + faults == len(reference_string)

    print(f"Result           : PASSED ✅")


reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
frame_count = 3

print("=" * 40)
print("PAGING SIMULATOR - ALGORITHM TESTS")
print("=" * 40)

test_algorithm("FIFO", fifo, reference_string, frame_count, 10)
test_algorithm("LRU", lru, reference_string, frame_count, 9)
test_algorithm("Optimal", optimal, reference_string, frame_count, 7)

print("\nAll algorithm tests completed successfully! 🎉")
