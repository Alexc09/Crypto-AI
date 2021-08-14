from Analyze.RFI_Indicator import get_rsi_report, get_symbols
from Global.mailer import send_mail
import json

CONFIG = json.load(open("../Configs/secret.json"))


coins_to_consider = get_symbols(currency='usdt')
report = get_rsi_report(coins_to_consider=coins_to_consider, sorted_rsi_dict='AUTO', top_k=8)
print(report)

emails = CONFIG["DAILY_REPORT_EMAILS"]

send_mail(emails, content=report)