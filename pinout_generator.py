# ~---------------------------
# SCRIPT HEADER HERE
# ~---------------------------

import shutil, argparse, os
from datetime import datetime
import xml.etree.ElementTree as ET

import helperfns, svgfns    

# ~---------------------------
if __name__ == '__main__' :
    argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    
    ##~- -------------
    ##   CLI ARGUMENTS
    ##~- -------------
    
    # arg TEMPLATE LIST
    argParser.add_argument('-l', 
                           '--list',
                           dest='print_list',
                           default=False,
                           action='store_true',
                           help='List the available template options for pinouts')
    # arg TEMPLATE SELECTION
    argParser.add_argument('-t', 
                           '--template', 
                           type=str, 
                           metavar='TEMPLATE',
                           help='Select the desired template for modification')
    # arg COLOR SPACE
    argParser.add_argument('-d',
                           '--nocolor',
                           '--nocolour',
                           dest='no_color',
                           default=False,
                           action='store_true',
                           help='Tells the script not to fill the pin symbols with color (DEFAULT="FALSE")'
                           )
    #arg FIGURE NAME
    argParser.add_argument('-n',
                           '--name',
                           default='Unnamed',
                           type=str,
                           help='Write help message here')
    # arg REVISION NUMBER
    argParser.add_argument('-r',
                           '--revision',
                           type=str,
                           default='1.00',
                           metavar='REVISION NUMBER',
                           help='Specifiy the revision number of the diagram (DEFAULT="1.00")')
    # arg COLOR SELECTION
    argParser.add_argument('-c',
                           '--color',
                           '--colour',
                           dest='color',
                           nargs='+',
                           type=str,
                           choices=['UNC', 'RED', 'ORG', 'YLW', 'GRN', 'BLU', 'PPL', 'WHT', 'BRN', 'BLK', 'SRED', 'SORG', 'SYLW', 'SGRN', 'SBLU', 'SPPL', 'SWHT', 'SBRN', 'SBLK'],
                           metavar='COLOR',
                           help='Specifies the colors of the pins using a 3 letter color code;\nAvailable List:\n    [UNC] Unconnected\n    [RED] Red\n    [ORG] Orange\n    [YLW] Yellow\n    [GRN] Green\n    [BLU] Blue\n    [PPL] Purple\n    [WHT] White\n    [BRN] Brown\n    [BLK] Black\n(Prepending an "S" to any code will convert it to a striped format)')
    
    args = argParser.parse_args() 

    ##~- ------------------------------
    ##   TEMPLATE LIST DISPLAY HANDLING
    ##~- ------------------------------
    FISCHER_LIST = ['fischer:11', 'fischer:8', 'fischer:4', 'fischer:3', 'fischer:2']
    TEMPLATE_LIST = [FISCHER_LIST]
    
    if args.print_list:
        print('TEMPLATES---------------------')
        for name in TEMPLATE_LIST:
            print(name)
        print('------------------------------')
        quit()
    
    ##~- ------------------------------
    ##   FILE GENERATION & MODIFICATION
    ##~- ------------------------------
    
    # creating an output directory if one does not exist already within the parent directory
    if not os.path.isdir('./output') :
        print('Creating output directory')
        os.mkdir('./output')
        print('Created output directory at ./pinout-generator/output...')
    
    # generating a timestamp and appending it to the output file name
    time = datetime.now()
    timestamp = time.strftime('%Y%m%d')
    filename_postfix = f'{args.name.lower()}-{timestamp}'
    
    # determination of which template file to generate a working document from
    template = args.template.split(':')
    family = template[0]
    num_pins = template[1]
    match family:
        case 'fischer':
            if num_pins in {2, 3, 4, 8, 11}:
                template_name = f'{num_pins}-Pin Fischer'
                src_file = f'./templates/fischer/t_fischer-{num_pins}.svg'
                dest_file = f'./output/fischer-{num_pins}-'
                if args.no_color:
                    dest_file = dest_file.append('nocolor-')
        case other:
            print('No match found for the specified template, use the "-l" flag to see the list of available templates')
            exit()
    
    print('Generating working file...')
    dest_file = f'{dest_file}{filename_postfix}.svg'
    shutil.copy(src_file, dest_file)
    
    target_file = dest_file
    
    # generating a working xml tree
    tree = ET.parse(target_file) 
    root = tree.getroot()
    
    # Pin Color Labels
    print('Relabelling pins with colors...')
    labels = {}
    for num in range(num_pins):
        pattern = f'pin_{num+1}_label_text'
        try:
            element = root.find(f'.//*[@id="{pattern}"]')
            print(element)
            print(f'{num+1} Old: {element.text}')
        except:
            print(f'!! FAILED label renaming at iteration {num+1}')
            
        element.text = args.color[num]
        print(f'  New:{element.text}')
    print('Finished relabelling pins with colors')
    
    if args.no_color:
        # Pin Symbol Colors
        print('Adding colors to pin symbols...')
        for num in range(num_pins):
            assigned_color = helperfns.get_color_code(args.color[num])
            if args.color[num] == 'UNC':
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
            assigned_color = helperfns.get_color_code(args.color[num])
            if args.color[num] == 'UNC':
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
        
    # Document Information
    print('Adding document info...')
    
    pattern = 'gen_timestamp_tspan'
    gen_time = time.strftime('%Y.%m.%d')
    print(f'Generation Date: {gen_time}')
    try:
        element = root.find(f'.//*[@id="{pattern}"]')
        element.text = f'Gen {gen_time}'
    except:
        print(f'#! Failed at adding timestamp to document')
        
    pattern = 'rev_num_tspan'
    try:
        element = root.find(f'.//*[@id="{pattern}"]')
        element.text = f'Rev {args.revision}'
    except:
        print('#! Failed at adding revision number to document')
        
    pattern = 'fig_name_tspan'
    try:
        element = root.find(f'.//*[@id="{pattern}"]')
        element.text = f'Fig. {args.name}'
    except:
        print('#! Failed at adding the figure name to the document')
        
    print('Finished adding document info')
        
        
        
    # writing the tree out to the final file
    print('Generating final file...')
    tree.write(target_file)
    print(f'File generated at {dest_file}')

    