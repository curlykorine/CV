from xmlrpc.server import SimpleXMLRPCServer
import sys
import os.path

# Read command line arguments
ip = sys.argv[1]
port = int(sys.argv[2])
# Create server
with SimpleXMLRPCServer((ip, port), logRequests=False) as my_server:
    my_server.register_introspection_functions()

    # send
    def send_file(filename, data):
        if not os.path.exists('./s_files/' + filename):
            my_file = open('./s_files/' + filename, 'wb')
            my_file.write(data.data)
            my_file.close()
            print(f'{filename} saved')
            return True
        else:
            print(f'{filename} not saved')
            return False
    my_server.register_function(send_file, 'send')

    # list
    def list_files():
        return os.listdir('./s_files')
    my_server.register_function(list_files, 'list')

    # delete
    def delete_file(filename):
        if os.path.exists('./s_files/' + filename):
            os.remove('./s_files/' + filename)
            print(f'{filename} deleted')
            return True
        else:
            print(f'{filename} not deleted')
            return False
    my_server.register_function(delete_file, 'delete')

    # get
    def get_file(filename):
        if os.path.exists('./s_files/' + filename):
            my_file = open('./s_files/' + filename, 'rb')
            my_file_size = os.path.getsize('./s_files/' + filename)
            print(f'File send: {filename}')
            return my_file.read(my_file_size)
        else:
            print(f'No such file: {filename}')
            return False
    my_server.register_function(get_file, 'get')

    # calc
    def calculate(expression):
        try:
            operator, left, right = expression.split()
            if check(left) != 'Invalid input' and check(right) != 'Invalid input':
                # Left operand = int/float
                left = check(left)
                # Right operand = int/float
                right = check(right)

                if operator == '+':
                    result = left + right
                elif operator == '-':
                    result = left - right
                elif operator == '*':
                    result = left * right
                elif operator == '/':
                    try:
                        result = left / right
                    except ZeroDivisionError:
                        result = 'Division by 0'
                elif operator == '>':
                    result = left > right
                elif operator == '<':
                    result = left < right
                elif operator == '>=':
                    result = left >= right
                elif operator == '<=':
                    result = left <= right
                else:
                    result = False

                # If the result = n.0 then this code makes it = n
                if str(result).endswith('.0'):
                    result = int(result)
            else:
                result = False
        except Exception:
            result = False

        if result == False or result == 'Division by 0':
            print(f'{expression} -- not done')
        else:
            print(f'{expression} -- done')

        return result
    my_server.register_function(calculate, 'calc')

    # Check whether the operand is valid:
    # if it consists only of digits then int, if digits and one '.' then float
    def check(num):
        if num.isdigit():
            return int(num)
        elif num.find('.') == num.rfind('.') != -1:
            left1, left2 = num.split('.')
            if (left1 + left2).isdigit():
                return float(num)
            else:
                return 'Invalid input'
        else:
            return'Invalid input'

    # main
    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        print('Server is stopping')