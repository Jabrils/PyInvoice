# PyInvoice v1.0.2

## Installing Dependencies:
    pip install -r requirements.txt

## How to use:
```
usage: pyinvoice.py [-h] --number NUMBER [--info INFO [INFO ...]] --company
                    COMPANY [COMPANY ...] [--idate IDATE] [--ddate DDATE]
                    [--work WORK [WORK ...]] [--dest DEST] [--logo LOGO] [-s]

        Easy invoicer from the commandline.

        How to use:

python pyinvoice.py --number 109 --logo 'C://Location_To_Logo.png' --company 'COMPANY' 'STREET' 'CITY / STATE / ZIP' 'NUMBER' --idate 09.09.019 --work 'Item' 'Description' 2000 1

optional arguments:
  -h, --help            show this help message and exit
  --number NUMBER, -n NUMBER
                        the number of the invoice
  --info INFO [INFO ...], -i INFO [INFO ...]
                        All the info if you don't want to use the default: 'Name' 'Address' 'City / State / Zipcode' 'Routing #' 'Account #' 'Email'
  --company COMPANY [COMPANY ...], -c COMPANY [COMPANY ...]
                        the name of the company you're invoicing
  --idate IDATE, -id IDATE
                        the date that you're invoicing
  --ddate DDATE, -dd DDATE
                        the date that your invoice is due
  --work WORK [WORK ...], -w WORK [WORK ...]
                        use -w to add some work: Item Description Price Quantity
  --dest DEST, -d DEST  the destination you want this file to be generated
  --logo LOGO, -l LOGO  the destination to the logo you want to appear on the invoice (converted to a 1:1 ratio)
  -s, --save            add -s if you want to save your info
```

## Example:
  python pyinvoice.py --number 109 --logo 'C://Location_To_Logo.png' --company 'COMPANY' 'STREET' 'CITY / STATE / ZIP' 'NUMBER' --idate 09.09.019 --work 'Item' 'Description' 2000 1

## Roadmap:

### To-Do
- [ ] Add the feature where pyvoice can keep track of what has been paid & not paid
- [ ] Make a short video on this?
- [ ] Clean script
- [ ] Make pyinvoice save the terminal command as well so if you want to easily modify or continue an invoice later

### Done
- [x] Get destination saving to work
- [x] Add a config file that saves user's bank info & address so they don't have to type it every time & can change it at will
- [x] Do something about the option for a logo & where saving that goes
- [x] Add an example with the -h tag!
