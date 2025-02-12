import pickle
import numpy as np
import sys
import os
import json

class PredictionModel:    
    def __init__(self, model_path='obfuscation_model.pkl', encoder_path='label_encoder.pkl'):
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
        except:
            print("[X] Model files not found. Please ensure the model has been installed")
            sys.exit(1)
    
    def predict(self, param1, param2, param3, param4 , param5):
        try:
            features = np.array([[float(param1), float(param2), float(param3), float(param4), float(param5)]])
            
            prediction = self.model.predict(features)
            result = self.label_encoder.inverse_transform(prediction)[0]
            confidence = self.model.predict_proba(features)[0]
            
            return result, max(confidence)
        except:
            raise print("[X] Invalid input, all parameters must be numeric")

def generate_parameters(line):
    alnum_count = 0
    quote_count = 0
    slash_count = 0
    word_count = 0
    lower_case_letters = 0
    upper_case_letters = 0
    currently_word_active = False

    for char in line:

        if char.isalnum():
            alnum_count = alnum_count + 1
            if currently_word_active == False:
                currently_word_active = True
                word_count = word_count + 1
            if char.islower():
                lower_case_letters = lower_case_letters + 1
            if char.isupper():
                upper_case_letters = upper_case_letters + 1
        else:
            currently_word_active = False
                    
        if char == "'" or char == '"':
            quote_count = quote_count + 1
        if char == r"\\" or char == r"/":
            slash_count = slash_count + 1

    quote_alnum = quote_count/alnum_count
    slash_alnum = slash_count/alnum_count
    word_alnum = word_count/alnum_count
    special_ratio = len(line)/alnum_count
    lower_upper_ratio = ((lower_case_letters - upper_case_letters)**2)

    return (quote_alnum,slash_alnum,word_alnum,special_ratio,lower_upper_ratio)
            
try:
    predictor = PredictionModel()
    result, confidence = predictor.predict(*sys.argv[1:5])
    print(f"\nPrediction: {result}")
    print(f"Confidence: {confidence:.2%}")
except Exception as e:
    print(f"Error: {str(e)}")

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
print("Argfuscation Detector")
print("-------------------------------")
    
try:
    predictor = PredictionModel()
except Exception as e:
    print(f"Error initializing model: {str(e)}")

def menu():
    print("\nOptions:")
    print("1. Make prediction")
    print("2. Batch prediction from file")
    print("3. Clear screen")
    print("4. Exit")

menu()
while True:

    choice = input("\nEnter your choice (1-4): ").strip()
     
    if choice == '4':
        print("[*] Quitting")
        quit()

    elif choice == '1':
        try:
            command = input("[*] Input the command: ")
            params = generate_parameters(command)
                
            result, confidence = predictor.predict(params[0], params[1], params[2], params[3], params[4])
                
            print("\n[!] Prediction Results:")
            print(f"[!] Classification: {result}")
            print(f"[!] Confidence: {confidence:.2%}")
                
        except Exception as e:
            print(f"\n[X] An error occurred: {str(e)}")
        
    elif choice == '2':
        try:
            filename = input("[*] Enter the path to your input file: ").strip()
            output_file = input("[*] Enter the path for results file: ").strip()
            if os.path.isfile(filename):
                with open(filename , "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line:
                            params = generate_parameters(line)
                            result, confidence = predictor.predict(params[0], params[1], params[2], params[3], params[4])
                            result_json = {
                                "command":str(line),
                                "verdict":str(result),
                                "confidence":str(confidence)}
                            with open(output_file , "a") as ff:
                                ff.write(json.dumps(result_json))
                                ff.write("\n")
                    else:
                        print(f"[!] All results written to {output_file}")
            else:
                print("[X] Input file path specified does not exist")

        except Exception as e:
            print(f"[X] Error processing file: {str(e)}")

    elif choice == '3':
        menu()
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        
    else:
        print("\nInvalid choice. Please enter 1, 2, 3 or 4.")
