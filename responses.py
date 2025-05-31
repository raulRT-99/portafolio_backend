ERROR_501 = 'Could not obtain data form server'

def generate(type=200,error='',response=''):
    if 400 <= int(type) <= 404 or int(type) == 501:
        msg = 'ERROR'
    else:
        msg = 'OK'

    response_msg = {
        str(type):msg,
        'type':msg,
        'msg': error if error else 'Correcto',
        'response': response
    }

    return response_msg
