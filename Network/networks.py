import tensorflow as tf
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Softmax, Dense


def create_rollout_policy_network():
    model = Sequential(name='RolloutPolicyNet')

    n_kernel = 64
    n_hidden = 32

    model.add(Conv2D(n_kernel, (5, 5), activation='relu', padding='same', input_shape=(15, 15, 2), name='Conv_5x5'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_kernel), name='Conv1'))
    model.add(Conv2D(1, (1, 1), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv_1x1'))
    model.add(Flatten())
    model.add(Softmax())

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    # model.summary()

    return model


def create_tree_policy_network():
    model = Sequential(name='TreePolicyNet')

    n_kernel = 128
    n_hidden = 128

    model.add(Conv2D(n_kernel, (5, 5), activation='relu', padding='same', input_shape=(15, 15, 2), name='Conv_5x5'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_kernel), name='Conv1'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv2'))
    model.add(Conv2D(1, (1, 1), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv_1x1'))
    model.add(Flatten())
    model.add(Softmax())

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    # model.summary()

    return model


def create_value_network():
    model = Sequential(name='ValueNetwork')

    model.add(Conv2D(128, (5, 5), activation='relu', input_shape=(15, 15, 2), name='Conv_5x5'))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same', input_shape=(11, 11, 128), name='Conv1'))
    model.add(MaxPool2D((2, 2), padding='same', name='MaxPool1'))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same', input_shape=(6, 6, 128), name='Conv2'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu', name='FC_1'))
    model.add(Dense(1, activation='sigmoid', name='FC_2'))

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # model.summary()

    return model


def create_rollout_policy_network_v2():
    model = Sequential(name='RolloutPolicyNet')

    n_kernels = 64
    n_hidden = 32

    model.add(Conv2D(n_kernels, (5, 5), activation='relu', padding='same', input_shape=(15, 15, 2), name='Conv_5x5'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_kernels), name='Conv1'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_kernels), name='Conv2'))
    model.add(Conv2D(1, (1, 1), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv_1x1'))
    model.add(Flatten())
    model.add(Softmax())

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    # model.summary()

    return model


def create_tree_policy_network_v2():
    model = Sequential(name='TreePolicyNet')

    n_kernels = 128
    n_hidden_first = 128
    n_hidden = 64

    model.add(Conv2D(n_kernels, (5, 5), activation='relu', padding='same', input_shape=(15, 15, 2), name='Conv_5x5'))
    model.add(Conv2D(n_hidden_first, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_kernels), name='Conv1'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_hidden_first), name='Conv2'))
    model.add(Conv2D(n_hidden, (3, 3), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv3'))
    model.add(Conv2D(1, (1, 1), activation='relu', padding='same', input_shape=(15, 15, n_hidden), name='Conv_1x1'))
    model.add(Flatten())
    model.add(Softmax())

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    # model.summary()

    return model


if __name__ == '__main__':
    test = create_tree_policy_network()
    print(test)
    print(type(test))
