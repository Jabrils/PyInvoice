# v1.0.3

from fpdf import FPDF
import argparse
import os

parser = argparse.ArgumentParser(description="\tEasy invoicer from the commandline.\n\n\tHow to use:\n\npython --number 109 --logo 'C://Location_To_Logo.png' --company 'COMPANY' 'STREET' 'CITY / STATE / ZIP' 'NUMBER' --idate 09.09.019 --work 'Item' 'Description' 2000 1",formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--number','-n', type=str, default=0, required=True,
                    help="the number of the invoice")
parser.add_argument('--info','-i', nargs="+", type=str, default=[],
                    help="All the info if you don't want to use the default: 'Name' 'Address' 'City / State / Zipcode' 'Routing #' 'Account #' 'Email'")
parser.add_argument('--company','-c', nargs="+", type=str, default=[], required=True,
                    help="the name of the company you're invoicing")
parser.add_argument('--idate','-id', type=str, default='04.09.019',
                    help="the date that you're invoicing")
parser.add_argument('--ddate','-dd', type=str,
                    help="the date that your invoice is due")
parser.add_argument('--work','-w', nargs='+', type=str, default=[], action='append',
                    help="use -w to add some work: Item Description Price Quantity")
parser.add_argument('--dest','-d', type=str,
                    help="the destination you want this file to be generated")
parser.add_argument('--logo','-l', type=str,
                    help="the destination to the logo you want to appear on the invoice (converted to a 1:1 ratio)")
parser.add_argument('-s', "--save", action='store_true',
                    help='add -s if you want to save your info')

args = parser.parse_args()

cwd = os.getcwd()

'''
IMPORT DATA
'''

data = [
    ['Item','Description','Unit Price','Qty', 'Subtotal'],
]
for row in args.work:
    row[2] = float(row[2])
    row[3] = int(row[3])
    data.append(row)
data.append(['','','Total:','',''])

# 
if args.idate is None:
    args.idate = "Today"

# If the due date is empty, set it to match the invoice date
if args.ddate is None:
    args.ddate = args.idate


createFile = not os.path.exists('info.txt')

if args.info == []:

    allData = []

    if createFile:
        cont = input("Wait, it appears that you aren't inputting any data & don't have a data file\nWould you like to create one? (type 'y' if yes): ")
        
        if cont.lower() == 'y':
            allData.append(input("What is the name on the invoice: "))
            allData.append(input("What is the address for the invoice: "))
            allData.append(input("What is the City, State Zip for that address: "))
            allData.append(input("What is the routing number to your bank: "))
            allData.append(input("What is the account number you want funds transferred to: "))
            allData.append(input("What is your email?: "))

            with open(f'{cwd}/info.txt', 'w') as f:
                print(f"Saving info to @ {cwd}\\info.txt")
                f.write('\n'.join(allData))

        else:
            print("okay goodbye then")
            quit()

    with open(f'{cwd}/info.txt', 'r') as f:
        print(f"Reading info from @ {cwd}\\info.txt")
        allData = f.read().split('\n')
else:
    allData = args.info

    if createFile:

        if args.save:
            with open(f'{cwd}/info.txt', 'w') as f:
                print(f"Saving info to @ {cwd}\\info.txt")
                f.write('\n'.join(allData))
        elif input("It appears that you don't have a data file\nWould you like to create one? (type 'y' if yes): ").lower() == 'y':
            with open(f'{cwd}/info.txt', 'w') as f:
                print(f"Saving info to @ {cwd}\\info.txt")
                f.write('\n'.join(allData))

'''
DOCUMENT HEADER
'''

# Create instance of FPDF class
# Letter size paper, use inches as unit of measure
pdf=FPDF(format='letter', unit='in')
 
# Add new page. Without this you cannot create the document.
pdf.add_page()
 
# Remember to always put one of these at least once.
pdf.set_font('Times','',10) 
 
# Long meaningless piece of text
header = f"""
Invoice ID: {args.number}
Invoice Date: {args.idate}
Due Date: {args.ddate}
"""
 
effective_page_width = pdf.w - 2 * pdf.l_margin

me = f"""
{allData[0]}
{allData[1]}
{allData[2]}
"""

ybefore = pdf.get_y()
pdf.set_font('Times', '', 12.0)
pdf.multi_cell(effective_page_width/2,0.15, me)

bank = f"""
Routing #: {allData[3]}
Account #: {allData[4]}

Please contact {allData[5]}
for other means of payment
"""

pdf.set_font('Times','B') 
pdf.multi_cell(effective_page_width/2,0.15, bank)
pdf.ln(0.25)

# First save the y coordinate just before rendering the first multi_cell
pdf.set_font('Times','B',36)
pdf.cell(5)
pdf.set_xy(effective_page_width/2 + pdf.l_margin, ybefore)
pdf.cell(effective_page_width/2, 0, 'INVOICE', align='R')
pdf.ln(0.25)
 
pdf.set_font('Times','',16)
pdf.cell(5)
pdf.set_xy(effective_page_width/2 + pdf.l_margin, ybefore)
pdf.multi_cell(effective_page_width/2, 0.20, header, align='R')
pdf.ln(0.5)

'''
CLIENT INFO 
'''
if args.logo != None:
    pdf.image(args.logo, x=3.5,y=.1,w=1.45,h=1.5)
pdf.set_font('Times','B',16)
pdf.cell(4)
pdf.multi_cell(0, 0.20,
f"Bill To:", align='L')

pdf.set_font('Times','',16)
pdf.cell(4)
pdf.multi_cell(0, 0.20,
f"""
{args.company[0]}
{args.company[1]}
{args.company[2]}
{args.company[3]}
""", align='L')
pdf.ln(0.5)

'''
INVOICING DATA
'''

# Effective page width, or just epw
epw = pdf.w - 2*pdf.l_margin
 
# Set column width to 1/4 of effective page width to distribute content 
# evenly across table and page 7.7 = total
col_width = [2,3.2,1,.5,1]

# Text height is the same as current font size
th = pdf.font_size

subTotal = 0
place = 0

pdf.set_font('Times','B', 14)

for row in data:
    index = 0
    
    # Check to see if our 3 colum is a number or not
    if isinstance(row[2], float):
        subTotal+= row[2] * row[3]
        data[len(data)-1][4] = '${:,.2f}'.format(subTotal)
        row.append(row[2] * row[3])

    # Loop through 
    for datum in row:
        pdf.set_fill_color(255,255,255)

        if place == 0:
            pdf.set_fill_color(200,200,200)
        elif place == 1:
            pdf.set_font('Times')
        elif place == len(data)-1:
            pdf.set_fill_color(200,255,200)
            pdf.set_font('Times','B')

        if isinstance(datum, float):
            datum = '${:,.2f}'.format(datum)

        pdf.cell(col_width[index], th, str(datum), border=1, align='C', fill=True)
        index+=1

    pdf.ln(th)
    place +=1

if args.dest == None:
    pdf.output(f"{args.idate.replace('.','-')}_{args.number}_Invoice_{args.company[0]}.pdf",'F')
    print(f"Invoice saved @ {cwd}\\{args.idate.replace('.','-')}_{args.number}_Invoice_{args.company[0]}.pdf")
else:
    pdf.output(f"{args.dest}/{args.idate.replace('.','-')}_{args.number}_Invoice_{args.company[0]}.pdf",'F')
    print(f"Invoice saved @ {args.idate.replace('.','-')}_{args.dest}\\{args.number}_Invoice_{args.company[0]}.pdf")