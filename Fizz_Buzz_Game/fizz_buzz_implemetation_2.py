def fizz_buzz(number: int) -> str:
    """
    Play Fizz buzz.
    (Checking if the numbers provided are
    divisible by 3 or 5 or both or neither).

    :param number: The numbers to test.
    :return: Returns fizz if number is divisible by 3, buzz if by 5, fizz
    buzz if by both or the number as a string if by neither.
    """
    if number % 3 == 0 and number % 5 == 0:
        return "fizz buzz"
    elif number % 3 == 0:
        return "fizz"
    elif number % 5 == 0:
        return "buzz"
    else:
        return str(number)


input("Play Fizz Buzz. Press ENTER to start")
print()

for value in range(1, 101):
    if value % 2 != 0:
        print(fizz_buzz(value))
    elif input("Your go: ") == fizz_buzz(value):
        pass
    else:
        print("You lost. The correct answer was {}".format(fizz_buzz(value)))
        break
