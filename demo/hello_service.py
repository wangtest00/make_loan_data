from nameko.rpc import rpc

class hello_service:
    name = "hello_service"

    @rpc
    def hello(self):
        print("hello world")
