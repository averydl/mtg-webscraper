import urllib.request
import re
import ssl
import smtplib
import datetime
from email.message import EmailMessage

# path to url.txt file and output file(s)
filepath = 'ENTER FULL PATH TO URL/OUTPUT PRICE FILES'

# prevent connections from being refused due to user agent
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

# header for url request
headers = {'User-Agent':user_agent}

### regexes for price/name on different MTG websites ###

# CARDKINGDOM.COM #
ck_cost = '<span class="stylePrice">(.*)</span>' # regex for price (cardkingdom.com)
ck_name = '<meta itemprop="name" content=(.*)>' # regex for name (cardkingdom.com)
ck_cost_split = r'\n'
ck_name_split = r'>'
ck = []
ck.append(ck_cost)
ck.append(ck_name)
ck.append(ck_cost_split)
ck.append(ck_name_split)

output = ''

# download web content from each url and store prices in output file
with open(filepath + 'urls.txt') as urls:
    with open(filepath + 'prices.txt', 'w') as prices:
        for url in urls:
            curlist = [] # regex list to find price/name at the current url

            # select the proper list of regexes/split string literals for the current url
            if 'cardkingdom' in url:
                cur_list = ck
            elif 'tcg' in url:
                cur_list = tcg

            # download the target webpage
            req = urllib.request.Request(url, None, headers)
            scontext = ssl.SSLContext() # bypass SSL certificate verification
            webpage = urllib.request.urlopen(req, context=scontext).read()

            # find target name/price using regexes and split function
            price = re.findall(cur_list[0], str(webpage))
            price = price[0].split(cur_list[2])[0]

            name = re.findall(cur_list[1], str(webpage))
            name = name[0].split(cur_list[3])[0]

            # write results to output file
            prices.write(name + ': ' + price + '\n')

            output = output + name + ': ' + price + '\n'

# send the results to email
from_email = 'username@example.com'
to_email = 'username@example.com'
subject = 'MTG Prices: ' + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

message = EmailMessage()
message['Subject'] = subject
message['From'] = from_email
message['To'] = to_email
message.set_content(output)

server = smtplib.SMTP('smtp.example.com')
server.connect('smtp.example.com')
server.ehlo()
server.starttls()
server.ehlo()
server.login(from_email, input("Enter Password: "))
server.send_message(message)
server.quit()
