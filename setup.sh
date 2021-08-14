cd /

apt update
sudo apt-get -y install gcc build-essential

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
  && sudo tar -xzf ta-lib-0.4.0-src.tar.gz \
  && sudo rm ta-lib-0.4.0-src.tar.gz \
  && cd ta-lib/ \
  && sudo ./configure --prefix=/usr \
  && sudo make \
  && sudo make install \
  && cd ~ \
  && sudo rm -rf ta-lib/ \
  && pip3 install ta-lib

echo "Installed ta-lib"

cd /root/Huobi-bot

cd Custom_huobi_Python
pip3 install .
cd ..

pip3 install -r requirements.txt

echo "Finished installation"
