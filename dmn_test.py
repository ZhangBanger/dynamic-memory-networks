import argparse

import tensorflow as tf

from dmn_plus import Config
from dmn_plus import DMN_PLUS

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--babi_task_id", help="specify babi task 1-20 (default=1)")
parser.add_argument("-t", "--dmn_type", help="specify type of dmn (default=original)")
args = parser.parse_args()

dmn_type = args.dmn_type if args.dmn_type is not None else "plus"

config = Config()

if args.babi_task_id is not None:
    config.babi_id = args.babi_task_id

config.strong_supervision = False

config.train_mode = False

print('Testing DMN ' + dmn_type + ' on babi task', config.babi_id)

# create model
model = DMN_PLUS(config)

print('==> initializing variables')
init = tf.initialize_all_variables()
saver = tf.train.Saver()

with tf.Session() as session:
    session.run(init)

    print('==> restoring weights')
    saver.restore(session, 'weights/task' + str(model.config.babi_id) + '.weights')

    print('==> running DMN')
    test_loss, test_accuracy = model.run_epoch(session, model.test)

    print('')
    print('Test accuracy:', test_accuracy)
