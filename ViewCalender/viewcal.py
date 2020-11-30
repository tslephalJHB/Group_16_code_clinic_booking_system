import quickstart

def command():
    command = input("Enter your command")
    if command == "view":
        quickstart.main()
    else:
        print("wrong entry")

def start():
    command()
    
    

if __name__ == '__main__':
    start()