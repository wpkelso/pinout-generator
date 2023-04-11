import argparse
from datetime import datetime

if __name__ == '__main__' :
    argParser = argparse.ArgumentParser()
    
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
                           help='Enables the draft lines on the diagram; This does nothing except make it look fancier (DEFAULT="OFF")')
    # arg TEMPLATE SELECTION
    argParser.add_argument('-t', 
                           '--template', 
                           type=str, 
                           help='Select the desired template for modification')
    # arg REVISION NUMBER
    argParser.add_argument('-r',
                           '--revision',
                           help='Specifiy the revision number of the diagram (DEFAULT="1")')
    # arg COLOR SELECTION
    argParser.add_argument('-c',
                           '--color',
                           '--colour',
                           nargs='+',
                           type=str,
                           help='Specifies the colors of the pins using the 3 letter color code; Available List: UNC Unconnected || RED Red || ORG Orange || YLW Yellow || GRN Green || BLU Blue || PPL Purple || WHT White || BRN Brown || BLK Black (Prepending an "S" to any code will convert it to a striped format)')
    
    args = argParser.parse_args()