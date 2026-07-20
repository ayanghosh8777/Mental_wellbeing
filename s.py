
import pickle

import sklearn
import numpy
import pandas

model = ...  # Your trained model
pickle.dump(model, open("model.pkl", "wb"))

print("scikit-learn:", sklearn.__version__)
print("numpy:", numpy.__version__)
print("pandas:", pandas.__version__)