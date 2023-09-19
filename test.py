import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask
from sklearn.model_selection import train_test_split
import serial
import time
from sklearn.ensemble import RandomForestClassifier
from flask import Response
app = Flask(__name__)

df = pd.read_csv(r"C:\Users\Zribi Ahmed\Desktop\pcd\Data_for_UCI_named.csv")

df['stabf'] = df['stabf'].replace(['unstable', 'stable'], ['0', '1'])

X = df.drop(['stabf', 'stab'], axis=1)
Y = df['stabf']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

rfc = RandomForestClassifier(
    n_estimators=50,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    max_depth=None
)

rfc.fit(X_train, y_train)

ser = serial.Serial('COM4', 115200, timeout=1)
ser.flush()
@app.route('/')
def loop_and_print():
    def generate_values():
        j=0
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                powers = data.split(',')
                if len(powers) >= 3 and powers[0] != '' and powers[1] != '' and powers[2] != '':
                    power1 = float(powers[0])
                    power2 = float(powers[1])
                    power3 = float(powers[2]) 
                    time.sleep(3)
                    print("Power 1:", power1, "mW")
                    print("Power 2:", power2, "mW")
                    print("Power 3:", power3)
                    new_data = [[
                        0.82, 5.42, 9.43, 2.48, 3.04,
                        -power1/200, -power2/200, -power3/40,
                        0.702, 0.1160, 0.57, 0.578
                    ]]

                    prediction = rfc.predict(new_data)
                    j=j+1
            yield f"Prediction {power1}={prediction}<br>"
    return Response(generate_values(),mimetype='text/html')

if __name__ == '__main__':
    app.run()

