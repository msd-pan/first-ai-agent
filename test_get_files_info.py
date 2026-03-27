from functions.get_files_info import get_files_info


def main():
    # Test 1: List current directory in calculator
    print("get_files_info(\"calculator\", \".\"):")
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    for line in result.split("\n"):
        print(f"  {line}")
    print()

    # Test 2: List pkg subdirectory
    print("get_files_info(\"calculator\", \"pkg\"):")
    print("Result for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    for line in result.split("\n"):
        print(f"  {line}")
    print()

    # Test 3: Try to access /bin (should fail)
    print("get_files_info(\"calculator\", \"/bin\"):")
    print("Result for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(f"    {result}")
    print()

    # Test 4: Try to access parent directory (should fail)
    print("get_files_info(\"calculator\", \"../\"):")
    print("Result for '../' directory:")
    result = get_files_info("calculator", "../")
    print(f"    {result}")
    print()


if __name__ == "__main__":
    main()
