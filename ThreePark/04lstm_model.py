from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

def train_model(X_train, y_train, output_units):
    input_shape = (X_train.shape[1], X_train.shape[2])
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),  # Ensure the LSTM does not return sequences
        Dropout(0.2),
        Dense(units=output_units)  # Dynamically set the number of output units
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, callbacks=[early_stopping], verbose=1)

    return model

X, y = scaled_data['Materials']

# y's shape is (num_samples, len(y_columns)) – len(y_columns) is number of features to predict
output_units = y.shape[1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = train_model(X_train, y_train, output_units=output_units)


