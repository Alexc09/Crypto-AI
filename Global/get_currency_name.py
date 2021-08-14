import requests

url = 'https://api.huobi.pro/v1/common/symbols'

x = requests.get(url).json()


def get_symbols(currency='usdt'):
    '''
    :param currency:  Currency the crypto is bought (Defaults to USDT)
    :return: A dictionary containing 3 lists: One for all products, one for ETP products and one for Non-ETP products
    '''
    coin_names_dict = {'ALL': [], 'ETP': [], 'NORMAL': []}
    for data in x['data']:
        if data['quote-currency'] == currency:
            # If this is an ETP
            if 'underlying' in data:
                coin_names_dict['ETP'].append(data['symbol'])
            else:
                coin_names_dict['NORMAL'].append(data['symbol'])
            coin_names_dict['ALL'].append(data['symbol'])

    return coin_names_dict


if __name__ == "__main__":
    print(get_symbols()['NORMAL'])


