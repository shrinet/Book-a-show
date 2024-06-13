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
export SECRET_KEY= 
# Strong, unique, random key or salt
export SECURITY_PASSWORD_SALT=
export JWT_SECRET_KEY=
python main.py
deactivate