# Script to start Gunicorn

#!/bin/bash
source /home/mike/ifsc/pj3/software/venv/bin/activate
exec gunicorn -c /home/mike/ifsc/pj3/software/config/gunicorn_config.py app:create_app
