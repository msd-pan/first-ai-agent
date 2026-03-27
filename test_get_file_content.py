from functions.get_file_content import get_file_content


def main():
    print("=" * 70)
    print("Test 1: get_file_content(\"calculator\", \"lorem.txt\")")
    print("=" * 70)
    result = get_file_content("calculator", "lorem.txt")
    print(f"Content length: {len(result)} characters")
    print(f"Content starts with: {result[:100]}...")
    print(f"Content ends with: ...{result[-100:]}")
    print()

    print("=" * 70)
    print("Test 2: get_file_content(\"calculator\", \"main.py\")")
    print("=" * 70)
    result = get_file_content("calculator", "main.py")
    print(result)
    print()

    print("=" * 70)
    print("Test 3: get_file_content(\"calculator\", \"pkg/calculator.py\")")
    print("=" * 70)
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    print()

    print("=" * 70)
    print("Test 4: get_file_content(\"calculator\", \"/bin/cat\") - Should fail")
    print("=" * 70)
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    print()

    print("=" * 70)
    print("Test 5: get_file_content(\"calculator\", \"pkg/does_not_exist.py\") - Should fail")
    print("=" * 70)
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)
    print()


if __name__ == "__main__":
    main()
