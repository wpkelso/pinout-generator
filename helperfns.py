# ~---------------------------
# SCRIPT HEADER HERE
# ~---------------------------

# ~---------------------------
# Takes: str
# Returns: list of color codes in RGB format
#
# Returns a list of associated RGB color codes to a
# given format code
# ~---------------------------
def get_color_code(code):
    translated_colors = 2
    return_codes = []
    if code.startswith('S'):
        code = code.strip('S')
        return_codes.append('#F7F7F7')
        translated_colors -= 1
        print('This is a striped format')
    while translated_colors > 0:
        match code:
            case 'UNC':
                return_codes.append('#000000')
            case 'RED':
                return_codes.append('#EA3030')
            case 'ORG':
                return_codes.append('#DE5D3A')
            case 'YLW':
                return_codes.append('#F2A833')
            case 'GRN':
                return_codes.append('#5AB552')
            case 'BLU':
                return_codes.append('#3388DE')
            case 'PPL':
                return_codes.append('#CC99FF')
            case 'WHT':
                return_codes.append('#F7F7F7')
            case 'BRN':
                return_codes.append('#8D3B25')
            case 'BLK':
                return_codes.append('#111111')
            case other:
                print('#!Invalid color code')
                exit()
        translated_colors -= 1 
    return return_codes
# ~---------------------------