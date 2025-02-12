# AntiArgfuscator
### A xgboost model to detect obfuscated CLI commands


## How it works ?
AntiArgfuscator is a very lightweight XGBoost modelled trained to detect obfuscated CLI commands. <br>
To run it follow the following steps:

```
git clone https://github.com/0x-Apollyon/AntiArgfuscator.git
cd AntiArgfuscator
python -m venv venv (optional)
source venv/bin/activate (optional)
pip install -r requirements.txt
python prediction.py
```

and voila....

## Model metrics

```
Training Metrics:
accuracy: 0.8857
precision: 1.0000
recall: 0.8605
f1: 0.9250
average_precision: 0.9992

Testing Metrics:
accuracy: 0.7736
precision: 1.0000
recall: 0.7209
f1: 0.8378
average_precision: 0.9865
```

![training_metrics](https://github.com/user-attachments/assets/ce1ff337-4f5b-479d-87c1-d549fa85a6c0)


## Drawbacks

This approach is in no way the best one but rather the fastest one. <br>
I believe creating vector embeddings of each command in the training set and then training a transformer would result in the best accuracy. <br>
However a transformer is very very computationally expensive and slow. <br>
<br>
Another issue I noticed is that the model is somewhat biased towards labelling samples as "unobfuscated". 
