import xml.etree.ElementTree
import re

# ~---------------------------
def color_element(root, pattern, color, opacity):
    print(f'Replacing with {color}')
    print(f'Using opacity {opacity}')
    
    try:
        element = root.find(f'.//*[@id="{pattern}"]')
        print(element)
    except:
        print(f'!! FAILED coloring at element "{pattern}"')
        
    try:
        current_style = element.get('style')
        print(current_style)
        new_style = re.sub('#[0-9A-Fa-f]{6}', color, current_style, 1)
    except:
        print(f'!! Failed regex substitution while coloring "{pattern}"')
        
    try:
        new_style = re.sub(r'fill-opacity:[0-1][.0-9]+', 'fill-opacity:'+str(opacity), new_style, 1)
    except:
        print(f'!! FAILED regex substitution while changing opacity on "{pattern}"')
    
    element.set('style', new_style)
    print(f'SUCCESS coloring {pattern}')
    
    return root
        
# ~---------------------------