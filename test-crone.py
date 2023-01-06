from datetime import datetime

try:
    with open('test_output.txt', 'w+') as f:
        f.write(str(datetime.now()))
except Exception as e:
    print(e)

