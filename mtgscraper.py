import urllib.request
import re
import ssl
import smtplib
import datetime
from email.message import EmailMessage

# path to url.txt file and output file(s)
filepath = 'ENTER_FULL_FILE_PATH'

# prevent connections from being refused due to user agent
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

# header for url request
headers = {'User-Agent':user_agent}

output = ''

# download web content from each url and store prices in output file
with open(filepath + 'urls.txt') as urls:
    with open(filepath + 'prices.txt', 'w') as prices:
        for url in urls:
            # download the target webpage
            req = urllib.request.Request(url, None, headers)
            scontext = ssl.SSLContext() # bypass SSL certificate verification
            webpage = urllib.request.urlopen(req, context=scontext).read()

            # find target values (name/price) using regex module and string split function
            price = re.findall('<span class="stylePrice">(.*)</span>', str(webpage))
            price = price[0].split(r'\n')[0]

            name = re.findall('<meta itemprop="name" content="(.*)"', str(webpage))
            name = name[0].split(r'\n')[0]

            # write results to output file
            prices.write(name + ': ' + price + '\n')

            output = output + name + ': ' + price + '\n'

# send the results to email
from_email = 'EXAMPLE@gmail.com'
to_email = 'EXAMPLE@gmail.com'
subject = 'MTG Prices: ' + datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")

message = EmailMessage()
message['Subject'] = subject
message['From'] = from_email
message['To'] = to_email
message.set_content(output)

server = smtplib.SMTP('smtp.gmail.com')
server.connect('smtp.gmail.com')
server.ehlo()
server.starttls()
server.ehlo()
server.login(from_email, input("Enter Password: "))
server.send_message(message)
server.quit()
