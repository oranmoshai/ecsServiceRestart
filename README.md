#Install:  
pip install boto3  
pip install fire  


#Run:  
python ecsServiceRestart.py restart --services="app app2" --cluster=test


#Testing:  
pip install moto
pip install pytest
pytest test_ecsServiceRestart.py
