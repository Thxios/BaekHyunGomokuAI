import tensorflow as tf
import numpy as np
import pickle as pkl
from typing import *

from Network.networks import create_rollout_policy_network, create_tree_policy_network, create_value_network



batch_size = 64
n_validation = 5000
policy_data_path = 'train_data/gomoku+soosyrv_swap_shuffled.bin'
value_data_path = 'train_data/value_6000_6000_swap_shuffled.bin'


def load_data(data_path):
    with open(data_path, 'rb') as f:
        (train_x, train_y), (test_x, test_y) = pkl.load(f)

    return (train_x, train_y), (test_x, test_y)


def train(model, data_path, epoch, cp_path):
    (train_x, train_y), (test_x, test_y) = load_data(data_path)

    # validation_x, validation_y = train_x[-n_validation:], train_y[-n_validation:]
    # train_x, train_y = train_x[:-n_validation], train_y[:-n_validation]

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=cp_path,
        save_weights_only=True,
        period=2,
        verbose=1,
    )

    model.fit(
        train_x,
        train_y,
        batch_size=batch_size,
        epochs=epoch,
        callbacks=[checkpoint_callback],
        # validation_data=(validation_x, validation_y)
        validation_data=(test_x, test_y)
    )

    test_loss, test_acc = model.evaluate(test_x, test_y, verbose=2)
    print(test_loss, test_acc)


def train_v2(model, data_path, epoch, cp_dir, save_step=False):
    (train_x, train_y), (test_x, test_y) = load_data(data_path)

    # validation_x, validation_y = test_x[:n_validation], test_y[:n_validation]
    # test_x, test_y = test_x[n_validation:], test_y[n_validation:]
    # validation_x, validation_y = train_x[-n_validation:], train_y[-n_validation:]
    # train_x, train_y = train_x[:-n_validation], train_y[:-n_validation]

    if save_step:
        cp_path = cp_dir + 'cp-{epoch:03d}.ckpt'
        model.save_weights(cp_path.format(epoch=0))
    else:
        cp_path = cp_dir + 'cp.ckpt'

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=cp_path,
        save_weights_only=True,
        verbose=1,
    )

    model.fit(
        train_x,
        train_y,
        batch_size=batch_size,
        epochs=epoch,
        callbacks=[checkpoint_callback],
        # validation_data=(validation_x, validation_y)
        validation_data=(test_x, test_y)
    )

    test_loss, test_acc = model.evaluate(test_x, test_y, verbose=2)
    print(test_loss, test_acc)



def train_rollout_network():
    model = create_rollout_policy_network()
    cp_dir = 'save/rollout/test2/'

    train_v2(model, policy_data_path, 10, cp_dir)


def train_tree_network():
    model = create_tree_policy_network()
    cp_dir = 'save/tree/test2_64kernel/'

    # train(model, 10, cp_path)
    train_v2(model, policy_data_path, 10, cp_dir, save_step=True)


def train_value_network():
    model = create_value_network()
    cp_dir = 'save/value/swap1/'

    train_v2(model, value_data_path, 5, cp_dir, save_step=True)


if __name__ == '__main__':
    # train_tree_network()
    # train_rollout_network()
    train_value_network()

    pass

