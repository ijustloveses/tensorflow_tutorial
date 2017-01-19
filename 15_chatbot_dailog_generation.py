# encoding: utf-8
import sys
import tensorflow as tf
from tensorflow.models.rnn.translate import seq2seq_model
import os
import numpy as np
import codecs

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3
VOCAB_SIZE = 5000

buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]
layer_size = 256
num_layers = 3
batch_size = 1

def read_vocabulary(vocabfile):
    vocabs = []
    with codecs.open(vocabfile, 'r', 'utf-8') as f:
        for line in f:
            vocabs.append(line.strip())

    vocab_dict = dict([(x, y) for (y, x) in enumerate(vocabs)])
    return vocab_dict, vocabs


vocab_enc, _ = read_vocabulary("data/shooter/vocab.enc")
_, vocab_dec = read_vocabulary("data/shooter/vocab.dec")
batch_size = 1

model = seq2seq_model.Seq2SeqModel(VOCAB_SIZE, VOCAB_SIZE, buckets=buckets, size=layer_size, num_layers=num_layers, max_gradient_norm= 5.0,
                                   batch_size=batch_size, learning_rate=0.5, learning_rate_decay_factor=0.99, forward_only=True)

sess = tf.Session()
ckpt = tf.train.get_checkpoint_state('data/shooter')
if ckpt != None:
    print(ckpt.model_checkpoint_path)
    model.saver.restore(sess, ckpt.model_checkpoint_path)
else:
    print("Failed to find model file")
    sys.exit(1)

while True:
    input_string = raw_input('Me > ').decode('utf-8')
    if input_string == 'quit':
        sys.exit(0)

    input_string_vec = []
    for w in input_string.strip():
        input_string_vec.append(vocab_enc.get(w, UNK_ID))
    bucket_id = min([i for i in range(len(buckets)) if buckets[i][0] > len(input_string_vec)])
    encoder_inputs, decoder_inputs, target_weights = model.get_batch({bucket_id: [(input_string_vec, [])]}, bucket_id)
    _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)
    outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
    if EOS_ID in outputs:
        outputs = outputs[: outputs.index(EOS_ID)]

    response = "".join([tf.compat.as_str(vocab_dec[output]) for output in outputs])
    print('AI > ' + response)
