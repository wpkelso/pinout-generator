import shutil, argparse, os
from datetime import datetime
import xml.etree.ElementTree as ET
    
FISCHER_LIST = ['fischer11', 'fischer8', 'fischer4', 'fischer3', 'fischer2']
TEMPLATE_LIST = [FISCHER_LIST]    
# ~---------------------------
# Takes: none
# Returns: none
#
# Prints list of available templates
# ~---------------------------
def print_template_list() :
    print('TEMPLATES---------------------')
    for name in TEMPLATE_LIST:
        print(name)
    print('------------------------------')
# ~---------------------------

# ~---------------------------
# Takes: str
# Returns: list of color codes in RGB format
#
# Returns a list of associated RGB color codes to a
# given format code
# ~---------------------------
def get_color_code(code) :
    translated_colors = 2
    return_codes = []
    if code.startswith('S'):
        code = code.strip('S')
        return_codes.append('F7F7F7')
        translated_colors -= 1
        print('This is a striped format')
    while translated_colors > 0:
        match code:
            case 'UNC':
                return_codes.append('000000')
            case 'RED':
                return_codes.append('EA3030')
            case 'ORG':
                return_codes.append('DE5D3A')
            case 'YLW':
                return_codes.append('F2A833')
            case 'GRN':
                return_codes.append('5AB552')
            case 'BLU':
                return_codes.append('3388DE')
            case 'PPL':
                return_codes.append('CC99FF')
            case 'WHT':
                return_codes.append('F7F7F7')
            case 'BRN':
                return_codes.append('8D3B25')
            case 'BLK':
                return_codes.append('111111')
            case other:
                print('#!Invalid color code')
                exit()
        translated_colors -= 1 
    return return_codes
# ~---------------------------
    
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
    # arg DRAFT LINES
    argParser.add_argument('-d',
                           '--draft',
                           default=False,
                           help='Enables drafting lines; This does nothing except make it look fancier (DEFAULT="OFF")')
    # arg TEMPLATE SELECTION
    argParser.add_argument('-t', 
                           '--template', 
                           type=str, 
                           metavar='TEMPLATE',
                           help='Select the desired template for modification')
    # arg COLOR SPACE
    argParser.add_argument('-u',
                           '--usecolor',
                           '--usecolour',
                           dest='use_color',
                           default=False,
                           action='store_true',
                           help='Tells the script to use the color templates rather than the greyscale templates'
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
    
    if args.print_list:
        print_template_list()
        quit()
    
    ##~- ------------------------------
    ##   FILE GENERATION & MODIFICATION
    ##~- ------------------------------
    
    # generating a timestamp and appending it to the output file name
    time = datetime.now()
    timestamp = time.strftime('%Y%m%d')
    filename_postfix = f'{args.name.lower()}-{timestamp}'
    
    # creating an output directory if one does not exist already within the parent directory
    if not os.path.isdir('./output') :
        print('Creating output directory')
        os.mkdir('./output')
        print('Created output directory at ./pinout-generator/output...')
    
    # determination of which template file to copy to a working document
    match args.template:
        case 'fischer11':
            template_name = '11-Pin Fischer'
            num_pins = 11
            src_file = './templates/fischer/t_diagram_g-fischer-11.svg'
            if args.use_color:
                dest_file = './output/fischer-11-color-'
            else:
                dest_file = './output/fischer-11-'
        case 'fischer8':
            template_name = '8-Pin Fischer'
            num_pins = 8
            src_file = './templates/fischer/t_diagram_g-fischer-8.svg'
            if args.use_color:
                dest_file = './output/fischer-8-color-'
            else:
                dest_file = './output/fischer-8-'
        case 'fischer4':
            template_name = '4-Pin Fischer'
            num_pins = 4
            src_file = './templates/fischer/t_diagram_g-fischer-4.svg'
            if args.use_color:
                dest_file = './output/fischer-4-color-'
            else:
                dest_file = './output/fischer-4-'
        case 'fischer3':
            template_name = '3-Pin Fischer'
            num_pins = 3
            src_file = './templates/fischer/t_diagram_g-fischer-3.svg'
            if args.use_color:
                dest_file = './output/fischer-3-color-'
            else:
                dest_file = './output/fischer-3-'
        case 'fischer2':
            template_name = '2-Pin Fischer'
            num_pins = 2
            src_file = './templates/fischer/t_diagram_g-fischer-2.svg'
            if args.use_color:
                dest_file = './output/fischer-2-color-'
            else:
                dest_file = './output/fischer-2-'
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
            print(f'#! Failed label renaming at iteration {num+1}')
            
        element.text = args.color[num]
        print(f'  New:{element.text}')
    print('Finished relabelling pins with colors')
    
    # Pin Symbol Colors
    if args.use_color:
        print('Adding colors to pin symbols...')
        for num in range(num_pins):
            assigned_color = get_color_code(args.color[num])
            if args.color[num] == 'UNC':
                opacity = 0
            else:
                opacity = 1
            
            # Coloring top of circle
            pattern = f'pin_{num+1}_color_top'
            try:
                element = root.find(f'.//*[@id="{pattern}"]')
                print(element)
            except:
                print(f'#! Failed symbol coloring at iteration {num+1} top')
            style_string = f'display:inline;fill:#{assigned_color[0]};fill-opacity:{opacity};'
            element.set('style', style_string)
            print({f'    New:{args.color[num]}'})
            
            # Coloring bottom of circle
            pattern = f'pin_{num+1}_color_bot'
            try:
                element = root.find(f'.//*[@id="{pattern}"]')
                print(element)
            except:
                print(f'#! Failed symbol coloring at iteration {num+1} bot')
                
            style_string = f'display:inline;fill:#{assigned_color[1]};fill-opacity:{opacity};'
            element.set('style', style_string)
            print({f'    New:{args.color[num]}'})
        print('Finished coloring symbols')
        
        
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

    