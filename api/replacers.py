def body_decoder(body: str):
    return_body: str = ''

    for char in body:
        if char == 'Ä':
            return_body += '*A'
        elif char == 'Ö':
            return_body += '*O'
        elif char == 'Ü':
            return_body += '*U'
        elif char == 'ä':
            return_body += '*a'
        elif char == 'ö':
            return_body += '*o'
        elif char == 'ü':
            return_body += '*u'
        elif char == 'ß':
            return_body += '*s'
        elif char == '–':
            return_body += '-'
        elif char == '„':
            return_body += '"'
        elif char == '“':
            return_body += '"'
        elif char == '…':
            return_body += '...'
        elif char == '´':
            return_body += "*'"
        else: return_body += char

    return return_body
