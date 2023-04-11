import shutil, argparse
from datetime import datetime
from svgutils import transform

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
                           metavar='REVISION NUMBER',
                           help='Specifiy the revision number of the diagram (DEFAULT="1.0")')
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
    
    time = datetime.now()
    timestamp = time.strftime('%Y%m%d')
    filename_postfix = args.name.lower() + '-' + timestamp
    
    match args.template:
        case 'fischer11':
            if args.color:
                src_file = './templates/fischer/t_diagram_c-fischer-11.svg'
                dest_file = './output/fischer-11-color-'
            else:
                src_file = './templates/fischer/t_diagram_g-fischer-11.svg'
                dest_file = './output/fischer-11-'
        case 'fischer8':
            if args.color:
                src_file = './templates/fischer/t_diagram_c-fischer-8.svg'
                dest_file = './output/fischer-8-color-'
            else:
                src_file = './templates/fischer/t_diagram_g-fischer-8.svg'
                dest_file = './output/fischer-8-'
        case other:
            print('No match found for the specified template, use the "-l" flag to see the list of available templates')
    
    dest_file = dest_file + filename_postfix + '.svg'
    shutil.copy(src_file, dest_file)
    
    target_file = transform.fromfile(dest_file)