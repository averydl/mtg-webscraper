import configparser
import urllib.request
import re
import ssl
import smtplib
import datetime
import regexes
from email.message import EmailMessage

#read from config file
config = configparser.ConfigParser()
config.read('settings.cnf')

# path to url.txt file and output file(s)
filepath = config['DEFAULT']['home_dir']

# prevent connections from being refused due to user agent
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

# header for url request
headers = {'User-Agent':user_agent}

### create lists of regexes and line split() tokens for different MTG websites ###

# CARDKINGDOM.COM #
ck = []
ck.append(regexes.CK_COST)
ck.append(regexes.CK_NAME)
ck.append(regexes.CK_COST_SPLIT)
ck.append(regexes.CK_NAME_SPLIT)

# TCGPLAYER.COM #
tcg = []
tcg.append(regexes.TCG_COST)
tcg.append(regexes.TCG_NAME)
tcg.append(regexes.TCG_COST_SPLIT)
tcg.append(regexes.TCG_NAME_SPLIT)

results = ''

# download web content from each url and store prices to results string
with open(filepath + 'urls.txt') as urls:
    results = []
    for url in urls:
        curlist = [] # regex list to find price/name at the current url

        # select the proper list of regexes/split string literals for the current url
        if 'cardkingdom' in url:
            cur_list = ck
        elif 'tcg' in url:
            cur_list = tcg

        # download the target webpage
        req = urllib.request.Request(url, None, headers)
        webpage = urllib.request.urlopen(req).read()

        # find target name/price using regexes and split tokens
        price = re.findall(cur_list[0], str(webpage))
        price = price[0].split(cur_list[2])[0]
        name = re.findall(cur_list[1], str(webpage))
        name = name[0].split(cur_list[3])[0]

        # append current card name/price to results string
        currentPrice = name + ': ' + price
        print(currentPrice)
        results.append(currentPrice)

# store current date/time
cur_date = datetime.datetime.now().strftime('%m_%d_%Y_%H:%M:%S')

# write results to text file
with open(filepath + 'prices_' + cur_date + '.txt', 'w') as prices:
    prices.write("\n".join(results))


# send the results to email
from_email = config['DEFAULT']['from_email']
to_email = config['DEFAULT']['to_email']
subject = 'MTG Prices: ' + cur_date

message = EmailMessage()
message['Subject'] = subject
message['From'] = from_email
message['To'] = to_email
message.set_content("\n".join(results))

server = smtplib.SMTP(config['DEFAULT']['from_email_domain'])
server.connect(config['DEFAULT']['from_email_domain'])
server.ehlo()
server.starttls()
server.ehlo()
server.login(from_email, config['DEFAULT']['from_email_password'])
server.send_message(message)
server.quit()
