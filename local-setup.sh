#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "bookashow" ];
then
    echo "bookashow folder exists. Installing using pip"
else
    echo "creating bookashow and install using pip"
    python3.9 -m venv bookashow
fi

# Activate virtual env
. bookashow/bin/activate

# Upgrade the PIP
pip install --upgrade pip
pip install -r requirements.txt
# Work done. so deactivate the virtual env
deactivate