def outer(obj):  # 类方法装饰器
    def inner(self):
        print('hello inner')
        obj(self)
    return inner

class Zoo(object):
    def __init__(self):
        pass
    @outer  # => zoo = outer(zoo)
    def zoo(self):
        print('hello zoo')


zoo = Zoo()
print(zoo.zoo.__name__)
#zoo.zoo()