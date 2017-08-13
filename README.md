# Description:  
Trigger AWS ECS service restart by clone current task definition and update service 

# Install:  
pip install boto3  
pip install fire  


# Usage:  
python ecsServiceRestart.py restart --services="app app2" --cluster=test


# Testing:  
pip install moto
pip install pytest
pytest test_ecsServiceRestart.py
