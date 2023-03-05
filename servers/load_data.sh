export PYTHONPATH=.
echo "edit /servers/tenant/test/test.py and set MANAGER_USER variable to your userId before running script."
echo "if MANAGER_USER is set correctly, you may continue"
read -p "Continue? [Y/N] >  " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
source ../venv/bin/activate
export PYTHONPATH=.
python3 tenant/server.py & PID=$!
sleep 4
kill $PID
cd ../dev-tools
python3 sync-users.py
cd ../servers/tenant/test
python3 test.py
fi
