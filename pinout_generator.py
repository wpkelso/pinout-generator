import shutil, argparse, os
from datetime import datetime
import xml.etree.ElementTree as ET
    
if __name__ == '__main__' :
    argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    
    
    
    ##~- -------------
    ##   CLI ARGUMENTS
    ##~- -------------
    
    # arg TEMPLATE LIST
    argParser.add_argument('-l', 
                           '--list', 
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
                           type=bool,
                           default=False,
                           metavar='USE COLOR TEMPLATE',
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
                           choices=['UNC', 'RED', 'ORG', 'YLW', 'GRN', 'BLU', 'PPL', 'WHT', 'BRN', 'BLK'],
                           metavar='COLOR',
                           help='Specifies the colors of the pins using a 3 letter color code;\nAvailable List:\n    [UNC] Unconnected\n    [RED] Red\n    [ORG] Orange\n    [YLW] Yellow\n    [GRN] Green\n    [BLU] Blue\n    [PPL] Purple\n    [WHT] White\n    [BRN] Brown\n    [BLK] Black\n(Prepending an "S" to any code will convert it to a striped format)')
    
    args = argParser.parse_args() 
    
    
    
    ##~- ------------------------------
    ##   FILE GENERATION & MODIFICATION
    ##~- ------------------------------
    
    # generating a timestamp and appending it to the output file name
    time = datetime.now()
    timestamp = time.strftime('%Y%m%d')
    filename_postfix = f'{args.name.lower()}-{timestamp}'
    
    # creating an output directory if one does not exist already within the parent directory
    if not os.path.isdir('./output') :
        os.mkdir('./output')
    
    # determination of which template file to copy to a working document
    match args.template:
        case 'fischer11':
            template_name = '11-Pin Fischer'
            num_pins = 11
            if args.use_color:
                src_file = './templates/fischer/t_diagram_c-fischer-11.svg'
                dest_file = './output/fischer-11-color-'
            else:
                src_file = './templates/fischer/t_diagram_g-fischer-11.svg'
                dest_file = './output/fischer-11-'
        case 'fischer8':
            template_name = '8-Pin Fischer'
            num_pins = 8
            if args.use_color:
                src_file = './templates/fischer/t_diagram_c-fischer-8.svg'
                dest_file = './output/fischer-8-color-'
            else:
                src_file = './templates/fischer/t_diagram_g-fischer-8.svg'
                dest_file = './output/fischer-8-'
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
            print(f'{num+1} Old: {element.text}')
        except:
            print(f'#! Failed label renaming at iteration {num}')
            
        element.text = args.color[num]
        print(f'  New:{element.text}\n')
    print('Finished relabelling pins with colors')
        
        
        
    # Administrative Information
    print('Adding administrative info...')
    
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
        
    print('Finished adding administrative info')
        
        
        
    # writing the tree out to the final file
    print('Generating final file...')
    tree.write(target_file)

    