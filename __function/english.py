from __configure.word_E import ENGLISH_DICTIONARY

def english_word(client_info):
    try:
        value = ENGLISH_DICTIONARY[client_info['stt_text']]
    except KeyError:
        value = 'Z'

    finally:
        client_info['response'] = value
        print("client_info['response']={}".format(client_info['response']))
