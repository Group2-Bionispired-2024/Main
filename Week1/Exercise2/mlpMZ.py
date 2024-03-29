import numpy as np

from perceptronMZ import Perceptron, SignActivation
from activationMZ import ActivationFunction

class Sigmoid(ActivationFunction):
   """ 
      Sigmoid activation: `f(x) = 1/(1+e^(-x))`
   """
   def forward(self, x):
      """
         Activation function output.
         TODO: Change the function to return the correct value, given input `x`.
      """
      sigmoid_act = 1/(1+np.exp(-x))

      return sigmoid_act

   def gradient(self, x):
      """
         Activation function derivative.
         TODO: Change the function to return the correct value, given input `x`.
      """
      sigmoid_grad = self.forward(x)*(1-self.forward(x))

      return sigmoid_grad

class LinearActivation(ActivationFunction):
   """ 
      Linear activation: `f(x) = x`
   """
   def forward(self, x):
      """
         Activation function output.
         TODO: Change the function to return the correct value, given input `x`.
      """
      lin_act = x
      return lin_act

   def gradient(self, x):
      """
         Activation function derivative.
         TODO: Change the function to return the correct value, given input `x`.
      """
      lin_grad = 1
      return lin_grad

class Layer:
   def __init__(self, num_inputs, num_units, act_f):
      """ 
         Initialize the layer, creating `num_units` perceptrons with `num_inputs` each. 
      """
      # TODO Create the perceptrons required for the layer
      self.num_units = num_units
      self.ps = []
      for i in range(num_units):
         self.ps.append(Perceptron(num_inputs, act_f))

   def activation(self, x):
      """ Returns the activation `a` of all perceptrons in the layer, given the input vector`x`. """
      return np.array([p.activation(x) for p in self.ps])

   def output(self, a):
      """ Returns the output `o` of all perceptrons in the layer, given the activation vector `a`. """
      return np.array([p.output(ai) for p, ai in zip(self.ps, a)])

   def predict(self, x):
      """ Returns the output `o` of all perceptrons in the layer, given the input vector `x`. """
      return np.array([p.predict(x) for p in self.ps])

   def gradient(self, a):
      """ Returns the gradient of the activation function for all perceptrons in the layer, given the activation vector `a`. """
      return np.array([p.gradient(ai) for p, ai in zip(self.ps, a)])

   def update_weights(self, dw):
      """ 
      Update the weights of all of the perceptrons in the layer, given the weight change of each.
      Input size: (n_inputs+1, n_units)
      """
      for i in range(self.num_units):
         self.ps[i].w += dw[:,i]
      
   @property
   def w(self):
      """
         Returns the weights of the neurons in the layer.
         Size: (n_inputs+1, n_units)
      """
      return np.array([p.w for p in self.ps]).T

   def import_weights(self, w):
      """ 
         Import the weights of all of the perceptrons in the layer.
         Input size: (n_inputs+1, n_units)
      """
      for i in range(self.num_units):
         self.ps[i].w = w[:,i]

class MLP:
   """ 
      Multi-layer perceptron class

   Parameters
   ----------
   n_inputs : int
      Number of inputs
   n_hidden_units : int
      Number of units in the hidden layer
   n_outputs : int
      Number of outputs
   alpha : float
      Learning rate used for gradient descent
   """
   def __init__(self, num_inputs, n_hidden_units, n_outputs, alpha=1e-3):
      self.num_inputs = num_inputs
      self.n_hidden_units = n_hidden_units
      self.n_outputs = n_outputs

      self.alpha = alpha

      # TODO: Define a hidden layer and the output layer
      self.l1 = Layer(self.num_inputs, self.n_hidden_units, Sigmoid) # hidden layer 1
      self.l_out = Layer(self.n_hidden_units, self.n_outputs, LinearActivation) # output layer

   def predict(self, x):
      """ 
      Forward pass prediction given the input x
      TODO: Write the function
      """
      forward_pass_pred = self.l_out.predict(self.l1.predict(x))

      return forward_pass_pred

   def train(self, inputs, outputs):
      """
         Train the network

      Parameters
      ----------
      `x` : numpy array
         Inputs (size: n_examples, n_inputs)
      `t` : numpy array
         Targets (size: n_examples, n_outputs)

      TODO: Write the function to iterate through training examples and apply gradient descent to update the neuron weights
      """
      weight_deltas = []
      # Loop over training examples
      for i in range(inputs.shape[0]):
         # Forward pass
         act_first_lay = self.l1.activation(inputs[i])
         out_first_lay = self.l1.output(act_first_lay)
         act_second_lay = self.l_out.activation(out_first_lay)
         out_second_lay = self.l_out.output(act_second_lay)

         # Backpropagation
         predictions = out_second_lay
         print("predictions", predictions)
         delta_out = (outputs[i]-predictions)*self.l_out.gradient(act_second_lay)
         delta1 = self.l1.gradient(act_first_lay)*self.l_out.w*delta_out
         weight_change = -self.alpha*delta1*out_first_lay
         weight_deltas.append(weight_change)
         # Add weight change contributions to temporary array
      print(weight_deltas)
      weight_deltas_sum = np.sum(weight_deltas, axis=0)
      print("weights sum" ,weight_deltas_sum)
      #dw1 += delta1.reshape(-1,1).dot(o0.reshape(1,-1))
      #dw3 += delta_out.reshape(-1,1).dot(o1.reshape(1,-1))
         
         # Update weights
      self.l1.update_weights(weight_deltas_sum)
      #self.l1.w += np.array(weight_deltas)

   def export_weights(self):
      return [self.l1.w, self.l2.w]
   
   def import_weights(self, ws):
      if ws[0].shape == (self.l1.n_units, self.n_inputs+1) and ws[1].shape == (self.l2.n_units, self.l1.n_units+1):
         print("Importing weights..")
         self.l1.import_weights(ws[0])
         self.l2.import_weights(ws[1])
      else:
         print("Sizes do not match")

def calc_prediction_error(model, x, t):
   """ Calculate the average prediction error """
   # TODO Write the function
   error = t - model.predict(x.T)
   mse = np.mean(error**2)
   return mse

if __name__ == "__main__":
   # TODO: Test new activation functions
   sigmoid_test = Sigmoid()
   print(sigmoid_test.forward(2))
   print(sigmoid_test.forward(0))

   linear_test = LinearActivation()
   print(linear_test.forward(2))
   print(linear_test.forward(0))

   # TODO: Test Layer class init
   num_of_inputs = 3
   num_of_units = 5
   activation_used = Sigmoid
   layer_test = Layer(num_of_inputs, num_of_units, activation_used)


   test_inputs = np.array([[np.pi, 1.0]])
   test_dims = test_inputs.shape
   test_inputs = np.append(np.ones((test_dims[0],1)), test_inputs, axis=1)
   test_dims = test_inputs.shape
   test_activation = layer_test.activation(test_inputs.T)
   test_output = layer_test.output(test_activation)
   test_predict = layer_test.predict(test_inputs.T)
   test_gradient = layer_test.gradient(test_activation)
   test_weights = layer_test.w

   print("Test inputs: ", test_inputs)
   print("Test dimensions: ", test_dims)
   print("Test activation: ", test_activation)
   print("Test output: ", test_output)
   print("Test predict: ", test_predict)
   print("Test gradient: ", test_gradient)
   print("Test weights: ", test_weights)


   # TODO: Test MLP class init
   num_of_inputs = 2+1
   num_of_hidden_units = 3
   num_of_outputs = 1
   print(test_inputs)

   mlp_test = MLP(num_of_inputs, num_of_hidden_units, num_of_outputs)
   mlp_test.predict(test_inputs.T)
   print("Test MLP predict: ", mlp_test.predict(test_inputs.T))
   print(mlp_test.l1.w)
   print(mlp_test.l_out.w)

   # Testing the calc error function
   test_data = np.array([[1, 1, 3], [2, 2, 4], [3, 3, 5], [4, 4, 6], [5, 5, 7]])
   test_data_x = test_data[:,0:2]
   test_data_y = test_data[:,2]
   test_data_x_dims = test_data_x.shape
   test_data_x = np.append(np.ones((test_data_x_dims[0],1)), test_data_x, axis=1)
   test_data_x_dims = test_data_x.shape

   num_of_inputs = test_data_x_dims[1]
   num_of_hidden_units = 3
   num_of_outputs = 1

   mlp_data_test = MLP(num_of_inputs, num_of_hidden_units, num_of_outputs)
   print("Test data: ", test_data)
   print("Test data x: ", test_data_x)
   print("Test data y: ", test_data_y)

   data_test_predictions = mlp_data_test.predict(test_data_x.T)
   print("Test data predictions: ", data_test_predictions)
   mse_result = calc_prediction_error(mlp_data_test, test_data_x, test_data_y)
   print(f'MSE: {mse_result}')

   # TODO: Training data
   xor_data = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]])
   xor_data_x = xor_data[:,0:2]
   xor_data_y = xor_data[:,2]
   xor_data_x_dims = xor_data_x.shape
   xor_data_x = np.append(np.ones((xor_data_x_dims[0],1)), xor_data_x, axis=1)
   xor_data_x_dims = xor_data_x.shape

   num_of_inputs = xor_data_x_dims[1]
   num_of_hidden_units = 2
   num_of_outputs = 1



   # TODO: Initialization
   
   mlp_xor = MLP(num_of_inputs, num_of_hidden_units, num_of_outputs)
   print("Test data: ", xor_data)
   print("Test data x: ", xor_data_x)
   print("Test data y: ", xor_data_y)

   mlp_xor.train(xor_data_x, xor_data_y)

   # TODO: Write a for loop to train the network for a number of iterations. Make plots.
   pass
