from os import system
import platform


class Utility():
    lineBreak = "--------------------Input Nothing to Exit--------------------"

    @staticmethod
    def clear():
        # Clear console command base on OS type
        osName = platform.system().lower()
        if 'windows'.lower() in osName:
            system('cls')
        else:
            system('clear')

    @staticmethod
    def validateInput(i, arr, setLen=0):
        # If no input end script
        if not i:
            exit()

        # Set length to the array or to a specific length
        length = len(arr)
        if setLen:
            length = setLen

        # Try to convert into int and return if valid
        try:
            result = int(i)
            if result in range(length):
                return result
        except ValueError:
            result = None

        # Keep trying to get a valid input with the same process as before and
        # return the input value
        while result not in range(length) and result != -1:
            try:
                result = input("Invalid input, please try again. Input -1 "
                               "to exit: ")
                if not result:
                    exit()
                result = int(result)
            except ValueError:
                print("Input must be an integer")

        if result == -1:
            exit()
        return result
