# Install VMware/Virtualbox
# Install Lubuntu 16.04.6 iso
# Install Linux tools
```bash
sudo apt install curl git autoconf build-essential pkg-config automake libtool
```
# Setup EON SSH KEY
```bash
mkdir ~/.ssh/
touch ~/.ssh/openpilot_rsa
(https://community.comma.ai/wiki/index.php/Configuring_OpenPilot copy SSH key and paste into ~/.ssh/openpilot_rsa)
chmod 600 ~/.ssh/openpilot_rsa
```
# Install android SDK
```bash
sudo apt install openjdk-8-jdk openjdk-8-jre android-sdk
sudo chown -R $(whoami): /usr/lib/android-sdk
echo 'export ANDROID_HOME=/usr/lib/android-sdk' >> ~/.bashrc
echo 'export PATH="$PATH:/usr/lib/android-sdk/tools/bin"' >> ~/.bashrc
source ~/.bashrc
```
# Install Android SDK Tools:
```bash
curl -o sdk-tools.zip "https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip"
unzip -o sdk-tools.zip -d "/usr/lib/android-sdk/"
sudo chmod +x /usr/lib/android-sdk/tools/bin/*
sdkmanager "platform-tools" "platforms;android-23" "platforms;android-27"
sdkmanager "extras;android;m2repository"
sdkmanager "extras;google;m2repository"
sdkmanager --licenses
```
# Install NodeJS
```bash
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
```
# Install Yarn
```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
```
# Insatll capnproto (https://capnproto.org/install.html)
```bash
# capnproto
git clone https://github.com/capnproto/capnproto.git
cd capnproto/c++
autoreconf -i
./configure
make -j6 check
sudo make install
cd ..

# c-capnproto
git clone https://github.com/opensourcerouting/c-capnproto
cd c-capnproto
git submodule update --init --recursive
autoreconf -f -i -s
./configure
make
make check
sudo make install
cd ..

# capnproto-java
git clone https://github.com/capnproto/capnproto-java
sed -i "s/c++11/c++14/" Makefile
make
sudo cp capnpc-java /usr/local/bin/
cd ..
```
# Edit /etc/ld.so.conf
```bash
sudo -s
echo 'include /usr/local/lib' >> /etc/ld.so.conf
sudo ldconfig
```
# Setup Repo
```bash
git clone https://github.com/commaai/openpilot.git
cd openpilot/
cd cereal/
make
cd ..
```
# Build frame apk
```bash
git clone https://github.com/commaai/openpilot-apks.git
cd openpilot-apks/frame
# fix your symbolic link
rm -fr app/src/main/java/ai/comma/openpilot/cereal
ln -sf <your_openpilot_director>/cereal/gen/java app/src/main/java/ai/comma/openpilot/cereal
./build.sh
scp -P 8022 -i ~/.ssh/openpilot_rsa out.apk root@<EON_IP>:/data/openpilot/apk/ai.comma.plus.frame.apk
cd ..
```
# Build offroad apk
```bash
cd offroad
yarn
node_modules/.bin/react-native link
# (Select "React Native")
./build.sh
scp -P 8022 -i ~/.ssh/openpilot_rsa ai.comma.plus.offroad.apk root@<EON_IP>:/data/openpilot/apk/ai.comma.plus.offroad.apk
cd ..
```
# Build black apk
```bash
cd black
./build.sh
scp -P 8022 -i ~/.ssh/openpilot_rsa out.apk root@<EON_IP>:/data/openpilot/apk/ai.comma.plus.black.apk
cd ..
```
