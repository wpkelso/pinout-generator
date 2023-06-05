# ~---------------------------
# SCRIPT HEADER HERE
# ~---------------------------

import helperfns, svgfns

# ~---------------------------
def label_diagram(root, num_pins, color):
    # Pin Color Labels
    print('Relabelling pins with colors...')
    for num in range(num_pins):
        pattern = f'pin_{num+1}_label_text'
        try:
            element = root.find(f'.//*[@id="{pattern}"]')
            #print(element)
            print(f'{num+1} Old: {element.text}')
        except:
            print(f'!! FAILED label renaming at iteration {num+1}')
            
        element.text = color[num]
        print(f'  New:{element.text}')
    print('Finished relabelling pins with colors')
    return root
# ~---------------------------

# ~---------------------------
def color_diagram(root, num_pins, color):
    # Pin Symbol Colors
    print('Adding colors to pin symbols...')
    for num in range(num_pins):
        assigned_color = helperfns.get_color_code(color[num])
        if color[num] == 'UNC':
            opacity = 0
        else:
            opacity = 1
        
        # Coloring top of circle
        pattern = f'pin_{num+1}_color_top'
        root = svgfns.color_element(root, pattern, assigned_color[0], opacity)
        
        # Coloring bottom of circle
        pattern = f'pin_{num+1}_color_bot'
        root = svgfns.color_element(root, pattern, assigned_color[1], opacity)
    print('Finished coloring symbols')
       
    # Pin Label Colors
    print('Adding colors to pin labels...')
    for num in range(num_pins):
        assigned_color = helperfns.get_color_code(color[num])
        if color[num] == 'UNC':
            opacity = 0
        else:
            opacity = 1
        
        # Coloring top of square
        pattern = f'pin_{num+1}_label_c_top'
        root = svgfns.color_element(root, pattern, assigned_color[1], opacity)
        
        # Coloring bottom of square
        pattern = f'pin_{num+1}_label_c_bot'
        root = svgfns.color_element(root, pattern, assigned_color[1], opacity)
    print('Finished coloring labels')
    
    # Modifying red dot on Fischer
    try:
        element = root.find('.//*[@id="fig_dot"]')
        style_string = 'fill:#EA3030;fill-opacity:1;stroke:#111111;stroke-width:3;stroke-linecap:round;stroke-dasharray:none;stroke-opacity:1'
        element.set('style', style_string)
    except:
        print('#! Failed to find red dot element') 

    return root
# ~---------------------------