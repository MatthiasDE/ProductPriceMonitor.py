### IMPORTANT VARIABLES
urls_dict =  dict()
urls_dict['GeForce RTX 3060'] = 'https://www.heise.de/preisvergleich/?cat=gra16_512&v=e&hloc=at&hloc=de&sort=r&bl1_id=30&xf=545_ASRock%7E545_ASUS%7E545_ATI%7E545_EVGA%7E545_GIGABYTE%7E545_MSI%7E545_NVIDIA%7E545_Sapphire%7E9810_06+16+-+RTX+3060'
urls_dict['GeForce RTX 3060 Ti'] = 'https://www.heise.de/preisvergleich/?cat=gra16_512&v=e&hloc=at&hloc=de&sort=r&bl1_id=30&xf=545_ASRock%7E545_ASUS%7E545_ATI%7E545_EVGA%7E545_GIGABYTE%7E545_MSI%7E545_NVIDIA%7E545_Sapphire%7E9816_03+05+16+-+RTX+3060+Ti'
#urls_dict['Radeon RX 6600 XT'] = 'https://www.heise.de/preisvergleich/?cat=gra16_512&v=e&hloc=at&hloc=de&sort=r&bl1_id=30&xf=545_ASRock%7E545_ASUS%7E545_ATI%7E545_EVGA%7E545_GIGABYTE%7E545_MSI%7E545_NVIDIA%7E545_Sapphire%7E9816_02+04+11+-+RX+6600+XT'
#urls_dict['Radeon RX 6700 XT'] = 'https://www.heise.de/preisvergleich/?cat=gra16_512&v=e&hloc=at&hloc=de&sort=r&bl1_id=30&xf=545_ASRock%7E545_ASUS%7E545_ATI%7E545_EVGA%7E545_GIGABYTE%7E545_MSI%7E545_NVIDIA%7E545_Sapphire%7E9816_02+04+11+-+RX+6700+XT'


requests_header_dict = dict()
requests_header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'


###CONNECTOR HELPER FUNCTIONS
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    con = None
    try:
        con = sqlite3.connect(db_file, timeout=5)
        return con
    except Error as e:
        print(e)

    return con

        
def close_connection(con):
    """ close database connection to the SQLit database after your doings
    :param con: Connection object
    :return:
    """
    try:
        con.close()
    except Error as e:
        print(e)


def get_model_price_data(url):
    """ get model price data from heise preisvergleich based on url
    :param url: url to extract
    :return: Dictionary with price information or None
    """
    import requests
    from lxml import html

    r = requests.get(url, headers=requests_header_dict)
    #r = requests.get(url, headers={'User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'})
    
    print(r.content)
    
    product_dict = dict()
    
    tree = html.document_fromstring(r.content)
    for e in tree.find_class("row productlist__product"):
        product_name = str.strip(e.find_class("productlist__link")[0].text_content())
        prefix_chars_count = str.strip(e.find_class("cell productlist__price")[0].text_content()).find("€ ")
        if prefix_chars_count > 0:
            product_price = str.strip(e.find_class("cell productlist__price")[0].text_content())[prefix_chars_count+2:]
        else:
            product_price = str.strip(e.find_class("cell productlist__price")[0].text_content())[2:]
        
        product_dict[product_name] = [model, float(product_price.replace(",", "."))]

    #print(product_dict)

    return product_dict


def create_dataset(con, dataset):
    """
    Create a new task
    :param conn:
    :param task:
    :return: last rowid
    """
    
    sql = ''' INSERT INTO tbl(timestamp,name,model,price)
              VALUES(?,?,?,?) '''
    cur = con.cursor()
    cur.execute(sql, dataset)
    con.commit()

    return cur.lastrowid


def save_model_price_data(dict):
    """ stores model price data from dict to sqlite3
    :param dict: dictionary to write to disk
    :return: None
    """

    import time
    save_time = time.time()

    # create a database connection
    con = create_connection(args.dbfile)

    # insert dataset
    if con is not None:
        # insert dataset
        for e in product_dict:
            dataset = (save_time, e, product_dict[e][0], product_dict[e][1])
            if args.mode == 'test':
                print('INFO - TESTMODE: New dataset received "', str(dataset) + '"')
            if args.mode == 'normal':
                print('INFO - NORMALMODE: New dataset', str(create_dataset(con, dataset)), "stored in database")
        close_connection(con)
    else:
        print("Error! cannot create the database connection.")



### CREATE DATA SINK FILE
import sqlite3
from sqlite3 import Error

sql_create_tbl = """CREATE TABLE IF NOT EXISTS tbl (
                                        id integer PRIMARY KEY,
                                        timestamp REAL NOT NULL,
                                        name text NOT NULL,
                                        model text NOT NULL,
                                        price integer NOT NULL
                                    ); """


def create_table(con, create_table_sql):
    """ create a table from the create_table_sql statement
    :param con: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = con.cursor()
        c.execute(create_table_sql)
        print('INFO: Database Structure was was created within database with filepath/-name', args.dbfile)
    except Error as e:
        print(e)
   

# create a database connection & table structure
def create_database(db_file):
    con = create_connection(db_file)

    # create tables
    if con is not None:
        # create table
        create_table(con, sql_create_tbl)
        close_connection(con)
    else:
        print("Error! cannot create the database connection.")

    print('INFO: Database File was created with filepath/-name', args.dbfile)



### ENTRY POINT
import argparse

def testmode():
    print('Test')

def normalmode():
    print(args)

parser = argparse.ArgumentParser(
    description="""    ____                 __           __  ____       _           __  ___            _ __            
   / __ \_________  ____/ /_  _______/ /_/ __ \_____(_)_______  /  |/  /___  ____  (_) /_____  _____
  / /_/ / ___/ __ \/ __  / / / / ___/ __/ /_/ / ___/ / ___/ _ \/ /|_/ / __ \/ __ \/ / __/ __ \/ ___/
 / ____/ /  / /_/ / /_/ / /_/ / /__/ /_/ ____/ /  / / /__/  __/ /  / / /_/ / / / / / /_/ /_/ / /    
/_/   /_/   \____/\__,_/\__,_/\___/\__/_/   /_/  /_/\___/\___/_/  /_/\____/_/ /_/_/\__/\____/_/     

Data Source Connector Module: Heise Preisvergleich (Graphic Card Model Abstract)

Gets the aggregated entry class Graphic Card model prices for Nvidia RTX 3060 (TI), AMD Radeon 6600 XT and 6700 XT and stores in sqlite3 database""",
    epilog='For further information visit https://github.com/MatthiasDE',
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-m', '--mode',
                    default='normal',
                    choices=['test', 'normal'],
                    help='(-m test) for testmode without storing data to db (default: normal for nomal mode incl. storage)')
parser.add_argument('-f', '--dbfile',
                    default='product_price_monitor.db',
                    help='sqlite3 database file (default: .\product_price_monitor.db)')
parser.add_argument('-r', '--runhour',
                    type=int,
                    help='keep alive and run every <int> hour')
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='verbose mode to debug (to be implemented)')

args = parser.parse_args()

#Info to user what URLs must be whitelisted in firewalls
print('Please make sure that the following links can be reached from the server where this module runs:')
for e in sorted(urls_dict):
    print(e + ": " + urls_dict[e])

#Check if database is existant; else create the data sink file & structure
import os
if os.path.isfile(args.dbfile) == False:
    print ('CRITICAL:', args.dbfile, "not found. Generation of file and necessary structure in progress..")
    create_database(args.dbfile)

#Getting the data
import time
from datetime import datetime
from random import randint

while True:
    for listitem in sorted(urls_dict):
        model = listitem
        url = urls_dict[listitem]
        product_dict = get_model_price_data(url)
        save_model_price_data(product_dict)
        time.sleep(randint(5,15)) # Sleep for 5-15 seconds to avoid banning
    
    print('INFO: Collection of data was finished at', datetime.now())

    if args.runhour:
        print ('INFO: Next data collection will run in', args.runhour, 'hours..')
        time.sleep(randint(int(args.runhour*60*60*0.9),int(args.runhour*60*60*1.1)))  # Sleep for seconds multiplied by user time (if any) +/- 10% to avoid banning
    else:
        exit()
