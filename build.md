
http://127.0.0.1:5000

python app.py

# create python virtual environment、都度
python3 -m venv venv

# activate the virtual environment、都度
source venv/bin/activate

# install dependencies、都度
# 最新を選ばないのが成功のコツ
pip install -r requirements.txt

# 都度
python3 -m app


git init
git remote add origin https://github.com/tztechno/tz_flask_camera.git
git pull origin master 
git add .
git commit -m "2024-08-29"
git push -u origin master
