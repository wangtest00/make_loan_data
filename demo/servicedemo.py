from nameko.standalone.rpc import ClusterRpcProxy


CONFIG = {'AMQP_URI': "amqp://guest:guest@192.168.20.222"}


def compute():
    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.hello_service.hello()


if __name__ == '__main__':
    compute()
