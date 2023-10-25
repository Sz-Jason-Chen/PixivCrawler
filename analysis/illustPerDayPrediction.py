import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Activation, LSTM


def data_preprocessing(previous_days):
    # read data =====================================================================================
    daily_df = pd.read_csv(f"../output/new_and_total_illust_per_day.csv")
    daily_df["date"] = pd.to_datetime(daily_df["date"])

    # data formatting ===============================================================================
    # data scaling or normalizing
    scaler = MinMaxScaler()
    daily_df["scaled_value"] = scaler.fit_transform(daily_df[["new"]])
    # print(daily_df["scaled_value"])
    # print(daily_df[["scaled_value"]])

    # The model aims at predicting new illusts by {previous days} data
    # so the {previous days} data is given sequences
    # the present day data is targets
    # previous_days = 7
    sequences = []
    targets = []
    for i in range(len(daily_df) - previous_days):
        seq = daily_df['scaled_value'].values[i:i + previous_days]
        target = daily_df['scaled_value'].values[i + previous_days]

        sequences.append(seq)
        targets.append(target)
    # print(sequences)

    # divide data into train part and test part
    # 80% data for training, 20% data for testing
    train_size = int(0.8 * len(sequences))

    train_sequences = sequences[:train_size]
    train_targets = targets[:train_size]

    test_sequences = sequences[train_size:]
    test_targets = targets[train_size:]

    # convert ndarray to tensor
    train_sequences = tf.convert_to_tensor(train_sequences, dtype=tf.float32)
    train_targets = tf.convert_to_tensor(train_targets, dtype=tf.float32)
    test_sequences = tf.convert_to_tensor(test_sequences, dtype=tf.float32)
    test_targets = tf.convert_to_tensor(test_targets, dtype=tf.float32)

    # print(train_sequences)
    # print(train_targets)
    # print(test_sequences)
    # print(test_targets)

    return train_sequences, train_targets, test_sequences, test_targets


def visualization(history, true_values, predicted_values):
    # visualization ===============================================================================
    loss = history.history['loss']

    plt.plot(loss, label='Training Loss')
    plt.title('Training Loss')
    plt.legend()
    plt.show()

    plt.figure(figsize=(40, 30))  # set the figure size (inch)
    plt.plot(true_values, label='True Values')
    plt.plot(predicted_values, label='Predicted Values')
    plt.title("Prediction vs real", fontsize=100)  # figure title
    plt.xlabel("Date point", fontsize=70)  # axis label
    plt.ylabel("Count (normalized)", fontsize=70)
    plt.xticks(fontsize=40)  # axis ticks font size
    plt.yticks(fontsize=40)
    plt.xlim(left=0)  # start point of axis
    plt.ylim(bottom=0)
    plt.tick_params(which="both", pad=20)  # label to both axis distance
    plt.grid(linewidth=4)  # show grid and set the grid's width
    plt.legend(fontsize=40, handlelength=4)  # present figure legend

    ax = plt.gca()
    # set the borderlines' width
    for spine in ax.spines.values():
        spine.set_linewidth(8)

    plt.show()


def RNN_model():
    previous_days = 7
    train_sequences, train_targets, test_sequences, test_targets = data_preprocessing(previous_days)

    # modelling ==================================================================================
    # build RNN model
    model = Sequential()
    model.add(SimpleRNN(units=64, activation='relu', input_shape=(previous_days, 1)))
    model.add(Activation("relu"))
    model.add(Dense(1))
    model.summary()

    # compile and train model
    model.compile(optimizer='adam', loss='mean_squared_error')
    history = model.fit(train_sequences, train_targets, epochs=20, batch_size=32)

    # prediction and evaluation
    predicted = model.predict(test_sequences)
    # predicted_values = scaler.inverse_transform(predicted)
    predicted_values = predicted
    # print(predicted_values)
    # print(type(predicted_values))

    true_values = test_targets.numpy()
    true_values = np.array(true_values).reshape(-1, 1)
    # print(true_values)

    mse = mean_squared_error(true_values, predicted_values)
    print("Mean Squared Error:", mse)

    visualization(history, true_values, predicted_values)


def LSTM_model():
    previous_days = 7
    train_sequences, train_targets, test_sequences, test_targets = data_preprocessing(previous_days)
    # modelling ==================================================================================
    # build LSTM model
    model = Sequential()
    model.add(LSTM(units=16, activation='relu', input_shape=(previous_days, 1)))
    model.add(Activation("relu"))
    model.add(Dense(units=1))
    model.summary()

    # compile and train model
    model.compile(optimizer='adam', loss='mean_squared_error')
    history = model.fit(train_sequences, train_targets, epochs=20, batch_size=32)

    # prediction and evaluation
    predicted = model.predict(test_sequences)
    # predicted_values = scaler.inverse_transform(predicted)
    predicted_values = predicted
    # print(predicted_values)
    # print(type(predicted_values))

    true_values = test_targets.numpy()
    true_values = np.array(true_values).reshape(-1, 1)
    # print(true_values)

    mse = mean_squared_error(true_values, predicted_values)
    print("Mean Squared Error:", mse)

    visualization(history, true_values, predicted_values)


if __name__ == "__main__":
    RNN_model()
    # LSTM_model()
