from generate import generate_code, save_code

TASKS = [
    # Math operations
    ("Check if a number is prime and return a boolean", "is_prime.py"),
    ("Compute the factorial of an integer n using recursion", "factorial.py"),
    ("Find the greatest common divisor (GCD) of two integers using Euclid's algorithm", "gcd.py"),
    
    # String operations
    ("Check if a given string is a palindrome, ignoring casing and non-alphanumeric characters", "is_palindrome.py"),
    ("Count the frequency of each vowel in a string and return as a dictionary", "vowel_count.py"),
    
    # List & Dictionary operations
    ("Flatten a nested list of arbitrary depth into a single flat list", "flatten_list.py"),
    ("Merge two dictionaries, summing the values for any matching keys", "merge_dicts.py"),
    ("Find the second largest number in a list of integers without using sorted()", "second_largest.py"),
]

def run_tests():
    print(f"Running batch generation for {len(TASKS)} distinct tasks...\n")
    for idx, (prompt, filename) in enumerate(TASKS, 1):
        print(f"[{idx}/{len(TASKS)}] Generating for: {prompt}")
        code = generate_code(prompt)
        saved_path = save_code(code, filename)
        print(f"       -> Saved to {saved_path}")
    print("\nAll 8 tasks generated successfully!")

if __name__ == "__main__":
    run_tests()