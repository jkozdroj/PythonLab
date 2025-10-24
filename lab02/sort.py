import random


def insertion_sort(arr):
    a = arr[:]  # kopia listy
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def bubble_sort(arr):
    a = arr[:]  # kopia listy
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:  # jesli nic nie zamieniono, lista juz posortowana
            break
    return a


if __name__ == "__main__":
    print("=== SORTOWANIE LICZB DWOMA NAJPROSTSZYMI METODAMI ===")
    try:
        N = int(input("Podaj ilosc liczb do wylosowania: "))
    except ValueError:
        N = 10
        print("Niepoprawna wartosc - przyjeto N = 10")

    # Losowanie liczb calkowitych z zakresu -100 do 100
    numbers = [random.randint(-100, 100) for _ in range(N)]

    print("\nWylosowane liczby:")
    print(numbers)

    # Sortowanie dwiema metodami
    sorted_insertion = insertion_sort(numbers)
    sorted_bubble = bubble_sort(numbers)

    # Weryfikacja z wbudowanym sorted()
    reference = sorted(numbers)
    ok1 = sorted_insertion == reference
    ok2 = sorted_bubble == reference

    print("\n=== WYNIKI SORTOWANIA ===")
    print("Insertion Sort:", sorted_insertion)
    print("Poprawnosc:", "OK" if ok1 else "BLAD")

    print("\nBubble Sort:", sorted_bubble)
    print("Poprawnosc:", "OK" if ok2 else "BLAD")

    print("\nWynik wbudowanego sorted():", reference)
