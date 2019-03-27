'''
The regexes module contains regexes and tokens for string splitting
which can be used to extract scrape price/name information from
various MTG card price websites
'''

# CARDKINGDOM.COM #
CK_COST = '<span class="stylePrice">(.*)</span>' # regex for price (cardkingdom.com)
CK_NAME = '<meta itemprop="name" content=(.*)>' # regex for name (cardkingdom.com)
CK_COST_SPLIT = r'\n' # string split token for price (cardkingdom.com)
CK_NAME_SPLIT = r'>' # string split token for name (cardkingdom.com)

# TCGPLAYER.COM
TCG_COST = '<span class="stylePrice">(.*)</span>' # regex for price (tcgplayer.com)
TCG_NAME = '<meta itemprop="name" content=(.*)>' # regex for name (tcgplayer.com)
TCG_COST_SPLIT = r'\n' # string split token for price (tcgplayer.com)
TCG_NAME_SPLIT = r'>' # string split token for name (tcgplayer.com)
