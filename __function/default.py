import os

from __utils.socket_module import SocketAction

from __configure.mubby_value import *
from __utils.stt_module import SpeechToText

__stt = SpeechToText()

def understand_func(client_info, socket_action=None):
    try:
        if socket_action:
            stt_text = __stt.speech_to_text(client_info, 'google_streaming', socket_action)
        else:
            stt_text = __stt.speech_to_text(client_info, 'google')
    
    except Exception as e:
        print('\t★ stt streaming error >> {}'.format(e))
        stt_text = ''

    finally:
        client_info['stt_text'] = stt_text
