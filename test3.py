from time import sleep
import threading

# a = {1:1, 2:2, 3:3}
# def func1(dictt):
#     for key, value in dictt.items():

#         print(key, value)
#         sleep(1)

# def func2(dictt):
#     sleep(1)
#     del dictt[2]

# th1 = threading.Thread(target=func1, args=(a,))
# th2 = threading.Thread(target=func2, args=(a,))

# th1.start()
# th2.start()
# th1.join()
# th2.join()
def val(value):
    match value:
        case int(value) if value>0:
            return 'positive', value
        case int(value):
            return 'negative', value
        case str(value) if len(value)<5:
            return 'short string', value
        case str(value):
            return 'string', value
print(val(10))
print(val(-3))
print(val('hi'))
print(val('wtfwtfwtf'))
        



