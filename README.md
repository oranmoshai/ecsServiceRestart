[![Build Status](https://travis-ci.org/fdfk/ecsServiceRestart.svg?branch=master)](https://travis-ci.org/fdfk/ecsServiceRestart)

# Description:  
Trigger AWS ECS service restart using force new deployment.

# Install:  
pip install boto3  
pip install fire  


# Usage:  
python ecsServiceRestart.py restart --services="app app2" --cluster=test

Or docker  
```bash
docker build -t ecs-service-restart .  
docker run \
-e AWS_DEFAULT_REGION='us-east-1' \
-e AWS_ACCESS_KEY_ID='xxxx' \
-e AWS_SECRET_ACCESS_KEY='xxxx' \
-it ecs-service-restart python ecsServiceRestart.py restart --services="app app2" --cluster=test
```
