from socket import timeout
import time

from __function.default import understand_func
from __function.english import english_word

from __configure.mubby_value import RESPONSE_FILE_NAME
from __utils.socket_module import SocketAction


# < If select find old client_info >
# 각 try 별로 isSuccess 를 달아서 실패하면 더 이상 동작하지 않게 해야할 것 같다.
# 이하 내용을 client_info = 1 class 형식으로 담아서 주고 받아야 하지 않을까 싶다.
def action_thread(client_info=None):
    socket_action = SocketAction(client_info)
    ack = ''

    # while client_info['request_socket_from_client']:
    if client_info:
        # 01. STT Streaming
        understand_func(client_info, socket_action)

        # 02. English word
        english_word(client_info)

        try:
            ack = socket_action.receiving()
        except timeout as e:
            print('ack error')

        if ack == b'ack':
            count = 3
            while count:
                try:
                    if socket_action.sending(client_info['response'].encode()):
                        break
                except timeout as e:
                    print('\t★ __send time out error >> {}, {}'.format(e, count))
                    count -= 1

        if socket_action.closing():
            client_info['request_socket_from_client'] = ''

    else:
        print('info가 선언이 안될 수 있나 지금 상황에.. 몰라.. 일단.. 뭐.. 안되면.. 생각해보자..')

    print("Thread end")
