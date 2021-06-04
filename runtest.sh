set -e
echo "clean *.pyc files"
find $(pwd) -name '*.pyc' -print -delete

echo "flake8 test start"
flake8 app

if [ "$?" != 0 ]
then
    echo "flake8 test failed!"
    exit 1;
else
    echo "flake8 test success!"
fi
