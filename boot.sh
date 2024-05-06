#!/bin/bash
FLASK_ENV=$1

if [ "$FLASK_ENV" = "production" ]
then
    FLASK_ENV=production
elif [ "$FLASK_ENV" = "testing" ]
then
    FLASK_ENV=testing
else
    FLASK_ENV=development
fi
echo "environment set to: $FLASK_ENV"
export FLASK_ENV=$FLASK_ENV
python3 app.py