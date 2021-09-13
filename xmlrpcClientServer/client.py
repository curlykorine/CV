import xmlrpc.client
import sys
import os

# Read command line arguments
ip = sys.argv[1]
port = int(sys.argv[2])
# Create client
my_client = xmlrpc.client.ServerProxy('http://' + ip + ':' + str(port))

try:
    while True:
        print('\nEnter the command:')
        operation = input()
        first = operation[0]

        # quit
        if first == 'q':
            if operation == 'quit':
                print('Client is stopping')
                break
            else:
                print('Not completed')
                print('Wrong command')

        # send
        elif first == 's':
            try:
                command, tail = operation.split()
                if command == 'send':
                    filename = tail
                    if os.path.exists('./c_files/' + filename):
                        my_file = open('./c_files/' + filename, 'rb')
                        my_file_size = os.path.getsize('./c_files/' + filename)
                        data = my_file.read(my_file_size)
                        if my_client.send(filename, data):
                            print('Completed')
                        else:
                            print('Not completed')
                            print('File already exists')
                    else:
                        print('Not completed')
                        print('No such file')
                else:
                    raise Exception()
            except Exception:
                print('Not completed')
                print('Wrong command')

        # list
        elif first == 'l':
            if operation == 'list':
                my_list = my_client.list()
                for i in range(0, len(my_list)):
                    print(my_list[i])
                print('Completed')
            else:
                print('Not completed')
                print('Wrong command')

        # delete
        elif first == 'd':
            try:
                command, tail = operation.split()
                if command == 'delete':
                    filename = tail
                    if my_client.delete(filename):
                        print('Completed')
                    else:
                        print('Not completed')
                        print('No such file')
                else:
                    raise Exception()
            except Exception:
                print('Not completed')
                print('Wrong command')

        # get
        elif first == 'g':
            try:
                command, tail = operation.split(maxsplit=1)
                if command == 'get':
                    if tail.find(' ') == -1:
                        filename = tail
                        answer = my_client.get(filename)
                        if answer == False:
                            print('Not completed')
                            print('No such file')
                        elif os.path.exists('./c_files/' + filename):
                            print('Not completed')
                            print('File already exists')
                        else:
                            my_file = open('./c_files/' + filename, 'wb')
                            my_file.write(answer.data)
                            my_file.close()
                            print('Completed')
                    else:
                        filename, new_filename = tail.split()
                        answer = my_client.get(filename)
                        if answer == False:
                            print('Not completed')
                            print('No such file')
                        elif os.path.exists('./c_files/' + new_filename):
                            print('Not completed')
                            print('File already exists')
                        else:
                            my_file = open('./c_files/' + new_filename, 'wb')
                            my_file.write(answer.data)
                            my_file.close()
                            print('Completed')
                else:
                    raise Exception()
            except Exception:
                print('Not completed')
                print('Wrong command')

        # calc
        elif first == 'c':
            try:
                command, tail = operation.split(maxsplit=1)
                if command == 'calc':
                    answer = my_client.calc(tail)
                    if answer == False:
                        print('Not completed')
                        print('Wrong expression')
                    elif answer == 'Division by 0':
                        print('Not completed')
                        print(answer)
                    else:
                        print(answer)
                        print('Completed')
                else:
                    raise Exception()
            except Exception:
                print('Not completed')
                print('Wrong command')

        # impossible commands
        else:
            print('Wrong command')

except KeyboardInterrupt:
    print('Client is stopping')