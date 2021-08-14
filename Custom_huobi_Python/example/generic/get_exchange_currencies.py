from huobi.client.generic import GenericClient
from huobi.utils import *
import datetime

date_object = datetime.date.today()
print(date_object)


generic_client = GenericClient()
list_obj = generic_client.get_exchange_currencies()

print('')

if len(list_obj) != 360:
    print('New Currency Launched')
    print(f'New Coin is {list_obj[-1]}')
# for currency in list_obj:
#     LogInfo.output(currency)