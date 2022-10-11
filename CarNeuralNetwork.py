import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


"""
---------------------
//NEURONSKA MREŽA\\
---------------------
"""

INPUT_SIZE = 5
HIDDEN1_LAYER_SIZE = 8
HIDDEN2_LAYER_SIZE = 6
OUTPUT_SIZE = 2

MIN_WEIGHT_VALUE = -10
MAX_WEIGHT_VALUE = 10

def fc_layer(x, size_out, weight ,name='fc', activation=None):
    if(weight.shape[0] != x.shape[0] or weight.shape[1] != size_out):
        w = weight
        wx = tf.matmul(x, w)
        if activation: return activation(wx)
        return wx
    return 0


class NeuralNetwork:   #nije genericna
     def __init__(self, num_of_hidden_layers=2, nodes_per_layer=[INPUT_SIZE, HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE, OUTPUT_SIZE]):
         self.number_of_layers = 2 + num_of_hidden_layers
         self.input_size = nodes_per_layer[0]
         self.hidden1_size = nodes_per_layer[1]
         self.hidden2_size = nodes_per_layer[2]
         self.output_size = nodes_per_layer[3]
         
         self.x = tf.placeholder(tf.float32, shape=[1, self.input_size], name='input')
         self.w1 = tf.placeholder(tf.float32, shape=[self.input_size, self.hidden1_size], name='in-hidden')
         self.w2 = tf.placeholder(tf.float32, shape=[self.hidden1_size, self.hidden2_size], name='hidden-hidden')
         self.w3 = tf.placeholder(tf.float32, shape=[self.hidden2_size, self.output_size], name='hidden-out')
         
         self.fc1 = fc_layer(self.x, self.hidden1_size, self.w1, name='fc1', activation=tf.nn.relu)
         self.fc2 = fc_layer(self.fc1, self.hidden2_size, self.w2, name='fc2', activation=tf.nn.relu)
         self.y = fc_layer(self.fc2, self.output_size, self.w3, name='output', activation=tf.nn.sigmoid)
         
         self.sess = tf.Session()
         self.sess.run(tf.global_variables_initializer())
         
         
     def calc_output(self, x, w1, w2, w3):
         if(x.shape[0] == self.x.shape[0] and w1.shape[0] == self.w1.shape[0] and w2.shape[0] == self.w2.shape[0] and w3.shape[0] == self.w3.shape[0] and
            x.shape[1] == self.x.shape[1] and w1.shape[1] == self.w1.shape[1] and w2.shape[1] == self.w2.shape[1] and w3.shape[1] == self.w3.shape[1]):
             out = self.sess.run(self.y, feed_dict={self.x: x, self.w1: w1, self.w2: w2, self.w3: w3})
             return out
         else:
             return None
         

if __name__ == "__main__":
    nn = NeuralNetwork()
    ulaz = np.random.rand(1, INPUT_SIZE)
    promjena_tezine1 = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE, size=(INPUT_SIZE, HIDDEN1_LAYER_SIZE))
    promjena_tezine2 = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE, size=(HIDDEN1_LAYER_SIZE, HIDDEN2_LAYER_SIZE))
    promjena_tezine3 = np.random.randint(MIN_WEIGHT_VALUE, MAX_WEIGHT_VALUE, size=(HIDDEN2_LAYER_SIZE, OUTPUT_SIZE))
    
    izlaz = nn.calc_output(ulaz, promjena_tezine1, promjena_tezine2, promjena_tezine3)
    print(izlaz)
    
         