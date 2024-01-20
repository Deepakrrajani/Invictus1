import joblib
import pandas as pd
model=joblib.load('Classify1.joblib')

data=[[1,4,0,0]]
columns = ['Medu', 'Fedu', 'schoolsup', 'famsup']

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

pred=model.predict(data)
print('prediction is:')