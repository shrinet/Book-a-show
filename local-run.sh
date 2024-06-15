#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
if [ -d "bookashow" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run-setup.sh first"
    exit N
fi

# Activate virtual env
. bookashow/bin/activate
export ENV=development
#Strong, random, difficult key
export SECRET_KEY=5e198607494ce54f8121ef260e0b02ecaa0ff240fc04964a7f6d252d0fc1ee68 
# Strong, unique, random key or salt
export SECURITY_PASSWORD_SALT=hjuyt67bhgrtyujhgf
export JWT_SECRET_KEY=longkeynottobeguess
python main.py
deactivate