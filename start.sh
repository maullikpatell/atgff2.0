if [ -z $SOURCE_CODE ]
then
  echo "Cloning main Repository"
  
  git clone https://github.com/maullikpatell/atgff2.0.git /atgff2.0
else
  echo "Cloning Custom Repo from $SOURCE_CODE "
  git clone $SOURCE_CODE /atgff2.0
fi
cd /atgff2.0
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 -m main
