#CRYPTO-AI #

## Features
Data pulling from live feed to generate datasets <br>
Alert for new coin listings <br>
Analyzing Trends using collected Data <br>
Explosive Market Advantage Trader <br>
Custom Trader Class with additional features <br>



## Instructions
###Installation of TA-lib
Refer to this for installation of TA-lib on python: <br>
https://blog.quantinsti.com/install-ta-lib-python/


### Config File
Refer to `secret.example.json` <br>
Make a new copy and rename to `secret.json`. This is the .json file accessed by programme <br>
Refer to `config.md` for information on configuration parameters

### Startup Instructions
Run `setup.sh` file for startup

To set cronjob to execute file every 9am <br>
`/etc/crontab` <br>
`0 9 * * * root python3 /Huobi-bot/daily_report.py`
