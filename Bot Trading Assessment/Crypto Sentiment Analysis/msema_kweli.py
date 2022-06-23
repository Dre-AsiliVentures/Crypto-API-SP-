if __name__ == '__main__':
    n = int(input().strip())
    if(n>=1 and n<=100):
        remainder=n%2
        if (remainder>=2 and remainder<=5):
            print("Not Weird")
        elif(remainder>=6 and remainder <=20):
            print("Weird")
        elif(remainder>20):
            print("Not weird")
        else:
            pass
    else:
        print("Please enter a valid input")