# P McKie March 2021

# delete and re-create the env
rm -r ./env
python3.9 -m venv env

#activate
source ./env/bin/activate

#pip install
./env/bin/pip install --upgrade pip
./env/bin/pip install -r requirements.txt
./env/bin/pip list > requirementsSuccess.txt

#deactivate
deactivate

# ./runme1.py