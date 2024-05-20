sudo apt-get install unzip
wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip -P ~/Downloads
unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads
chmod +x ~/Downloads/chromedriver
sudo mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver
Change the directory to /usr/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver