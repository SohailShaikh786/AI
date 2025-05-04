def generate_magic_square(n):
    if n % 2 == 0:
        print("This method works only for odd-order magic squares.")
        return

    magic_square = [[0] * n for _ in range(n)]

    i = 0
    j = n // 2

    for num in range(1, n * n + 1):
        magic_square[i][j] = num

        new_i = (i - 1) % n
        new_j = (j + 1) % n

        if magic_square[new_i][new_j]:
            i = (i + 1) % n
        else:
            i, j = new_i, new_j


    print(f"\nMagic Square of order {n}:")
    for row in magic_square:
        print(row)


try:
    n = int(input("Enter the size of the magic square (odd number): "))
    if n % 2 == 0:
        print("Please enter an odd number.")
    else:
        generate_magic_square(n)
except ValueError:
    print("Invalid input. Please enter a valid integer.")