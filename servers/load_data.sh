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
echo "\n\n\n\n\SERVER SCRIPT STOPS\n\n\n\n\n"
cd ../dev-tools
python3 sync-users.py
echo "\n\n\n\n\nSYNC USERS SCRIPT STOPS\n\n\n\n\n"
cd ../servers/tenant/test
python3 test.py
fi
