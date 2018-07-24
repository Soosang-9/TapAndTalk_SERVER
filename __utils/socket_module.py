# 통신부분에 대한 것을 여기다 모아야 한다.
# 현재는 그냥 동작 돌 수 있도록 가져다 놓았다.
# 추후 수정 필요 꼭
# 커넥팅 후에 꼭!
# 꼬옥!
# 꼭!
import socket

from __configure.mubby_value import BUF_SIZE


# 메시지 형태를 구분하는 구분자 역활 함수를 집어 넣어야 한다.
# app-text, app-voice, mubby-voice 등등..
class Socket(object):
    "" "server socket" ""
    def __init__(self, address_port=None):
        if address_port:
            self.__server = socket.socket()
            self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server.bind(address_port)
            self.__server.listen(5)
        else:
            print("에러에러 소켓 정의가 잘못 되었음")
            exit(1)

    def getting_server(self):
        "" "return server socket value" ""
        return self.__server


class SocketAction(object):
    "" "action for socket" ""
    def __init__(self, client_info):
        self.__client = client_info['request_socket_from_client']
        self.__audio_path = client_info['folder_path']
        self.__client.settimeout(2)

    def receiving(self):
        data = self.__client.recv(BUF_SIZE)
        return data

    def sending(self, data):
        self.__client.send(data)
        answer = self.__client.recv(BUF_SIZE)

        if answer == b'end':
            print("client send me >> end")
            return True
        else:
            print('client send me >> {}'.format(answer.decode()))
            return False

    def closing(self):
        try:
            self.__client.close()
            return True
        except:
            return False

    def sending_wav(self, file_name):
        audio_path = self.__audio_path + file_name
        answer = self.receiving()
        if answer == b'tel':

            with open(audio_path, "rb") as wave_file:
                data = wave_file.read()
                is_success = self.sending(str(len(data)).encode())

            if is_success:
                with open(audio_path, "rb") as wave_file:
                    count = 0
                    data = wave_file.read(FILE_HEADER_SIZE)
                    if self.sending(data):
                        while True:
                            data = wave_file.read(FILE_READ_SIZE)
                            if len(data) == 0:
                                self.sending(b'end')
                                break
                            else:
                                count += 1
                                if not self.sending(data):
                                    break

    def get_data(self):
        try:
            data = self.receiving()
        except socket.timeout as e:
            print("can't start '{}'".format(e))
            return b''

        else:
            print("rec check >> {}".format(data[:3]))
            if data[:3] == b'rec':
                if len(data) > 3:
                    yield data[3:]
                print("go to while")
                while True:
                    try:
                        data = self.receiving()
                    except socket.timeout as e:
                        print("can't second '{}'".format(e))
                        yield b''
                        break

                    else:
                        if data[-3:] == b'end':
                            if len(data) > 3:
                                yield data[:-3]
                            break
                        yield data
