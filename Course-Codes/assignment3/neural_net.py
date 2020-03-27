from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from past.builtins import xrange

class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network. The net has an input dimension of
    N, a hidden layer dimension of H, and performs classification over C classes 
    of output_size. We train the network with a softmax loss function and L2 
    regularization on the weight matrices. The network uses a ReLU nonlinearity 
    after the first fully connected layer.

    In other words, the network has the following architecture:

    input - fully connected layer - ReLU - fully connected layer - softmax

    The outputs of the second fully-connected layer are the scores for each class.
    """

    def __init__(self, input_size, hidden_size, output_size, std=1e-4):
        """
        Initialize the model. Weights are initialized to small random values and
        biases are initialized to zero. Weights and biases are stored in the
        variable self.params, which is a dictionary with the following keys:

        W1: First layer weights; has shape (D, H)
        b1: First layer biases; has shape (H,)
        W2: Second layer weights; has shape (H, C)
        b2: Second layer biases; has shape (C,)

        Inputs:
        - input_size: The dimension D of the input data.
        - hidden_size: The number of neurons H in the hidden layer.
        - output_size: The number of classes C.
        """
        self.params = {}
        self.params['W1'] = std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)

    def loss(self, X, y=None, wd_decay=0.0):
        """
        Compute the loss and gradients for a two layer fully connected neural
        network.

        Inputs:
        - X: Input data of shape (N, D). Each X[i] is a training sample.
        - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
          an integer in the range 0 <= y[i] < C. This parameter is optional; if it
          is not passed then we only return scores, and if it is passed then we
          instead return the loss and gradients.
        - wd_decay: Weight decay.

        Returns:
        If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
        the score for class c on input X[i].

        If y is not None, instead return a tuple of:
        - loss: Loss (classification loss and weigth decay loss) for this batch of training
          samples.
        - grads: Dictionary mapping parameter names to gradients of those parameters
          with respect to the loss function; has the same keys as self.params.
        """
        # Unpack variables from the params dictionary
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        N, D = X.shape

        # Compute the forward pass
        scores = None

        # Forward pass
        hidden_layer = np.maximum(0, np.dot(X,W1)+b1)
        scores = np.dot(hidden_layer, W2)+b2

        # If the targets are not given then jump out, we're done
        if y is None:
            return scores

        # Compute the loss
        loss = None
        # If the learning rate is too big you can get numerical problems
        # with the exponential. We solve this problem is to normalize
        # the unnormalized log probabilities with the maximum set at 0
        
        exp_scores = np.exp(scores - np.max(scores, axis=1, keepdims=True))
        probs = exp_scores/np.sum(exp_scores,axis=1,keepdims=True)
        correct_logprobs = -np.log(probs[np.arange(N),y])
        class_loss = np.sum(correct_logprobs)/N
        
        wd_loss = wd_decay*(np.sum(W1*W1)+np.sum(W2*W2))
        loss = class_loss+wd_loss

        # Backward pass: compute gradients
        grads = {}
        #grads['W1'] = np.zeros_like(self.params['W1'])
        #grads['W2'] = np.zeros_like(self.params['W2'])
        #grads['b1'] = np.zeros_like(self.params['b1'])
        #grads['b2'] = np.zeros_like(self.params['b2'])
        #############################################################################
        # TODO: Compute the backward pass, computing the derivatives of the weights #
        # and biases. Store the results in the grads dictionary.              #
        #############################################################################
        scores = probs
        scores[np.arange(N),y]  -= 1
        dW2 = np.dot(hidden_layer.T,scores)/N + 2*wd_decay*W2 
        db2 = np.sum(scores,axis =0)/N 
        buf_hide = np.dot(W2,scores.T)
        hidden_layer[hidden_layer>0] = 1
        buf_relu = buf_hide.T * hidden_layer 
        dW1 =   np.dot(X.T,buf_relu) /N + 2*wd_decay*W1
        db1 = np.sum(buf_relu,axis =0) /N
        grads['W1'] = dW1
        grads['W2'] = dW2
        grads['b1'] = db1
        grads['b2'] = db2
        #############################################################################
        #                          END OF YOUR CODE               #
        #############################################################################

        return loss, grads

    def train(self, X, y, X_val, y_val,
                learning_rate=0, 
                momentum=0, do_early_stopping=False,
                wd_decay=0, num_iters=10,
                batch_size=4, verbose=False, print_every=10):
        """
        Train this neural network using stochastic gradient descent with momentum (optional).

        Inputs:
        - X: A numpy array of shape (N, D) giving training data.
        - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
          X[i] has label c, where 0 <= c < C.
        - X_val: A numpy array of shape (N_val, D) giving validation data.
        - y_val: A numpy array of shape (N_val,) giving validation labels.
        - learning_rate: Scalar giving learning rate for optimization.
        - momentum: Scalar giving momentum in learning process.
        - do_early_stopping: boolean; if true use the model with minimum validation 
                    loss during iteration.
        - wd_decay: Scalar giving weight decay (regularization strength).
        - num_iters: Number of steps to take when optimizing.
        - batch_size: Number of training examples to use per step.
        - verbose: boolean; if true print progress during optimization.
        - print_every: Scalar giving how many iterations print a result.
        """
        num_train = X.shape[0]
        iterations_per_epoch = max(num_train / batch_size, 1)

        loss_history = []
        train_acc_history = []
        val_acc_history = []
        val_loss_history = []
        best_val_loss = 1e8
        best_params = self.params
        best_iter = 0
 
        for it in range(num_iters):
            X_batch = None
            y_batch = None
            
            # Create a random minibatch of training data and labels, storing  
            # them in X_batch and y_batch respectively.                             

            idx_batch = np.random.choice(np.arange(num_train),size=batch_size)
            X_batch = X[idx_batch]
            y_batch = y[idx_batch]

            # Compute loss and gradients using the current minibatch
            loss, grads = self.loss(X_batch, y=y_batch, wd_decay=wd_decay)
            val_loss, val_grads = self.loss(X_val, y_val)
            loss_history.append(loss)
            val_loss_history.append(val_loss)

            # Use the gradients in the grads dictionary to update the         
            # parameters of the network.      
            # using stochastic gradient descent with momentum.                          
            
            v1 = np.zeros_like(self.params['W1'])
            v2 = np.zeros_like(self.params['W2'])
            vb1 = np.zeros_like(self.params['b1'])
            vb2 = np.zeros_like(self.params['b2'])

            v1 = momentum*v1 - learning_rate*grads['W1']
            v2 = momentum*v2 - learning_rate*grads['W2']
            vb1 = momentum*vb1 - learning_rate*grads['b1']
            vb2 = momentum*vb2 - learning_rate*grads['b2']
            
            self.params['W1'] += v1
            self.params['W2'] += v2
            self.params['b1'] += vb1.ravel()
            self.params['b2'] += vb2.ravel()
            
            if do_early_stopping and val_loss < best_val_loss:
                best_val_loss = val_loss
                best_params = self.params
                best_iter = it
                        
            if verbose and it % print_every == 0:
                print('iteration %d / %d: training loss %f val loss: %f' % (it, num_iters, loss, val_loss))
 
            # Every epoch, check train and val accuracy and decay learning rate.
            if it % iterations_per_epoch == 0:
                # Check accuracy
                train_acc = np.mean(self.predict(X_batch) == y_batch)
                val_acc = np.mean(self.predict(X_val) == y_val)
                train_acc_history.append(train_acc)
                val_acc_history.append(val_acc)

        if do_early_stopping:
            self.params = best_params
            print('Early stopping: validation loss was lowest after %d iterations. We chose the model that we had then.\n' % best_iter)
        
        train_loss, = plt.plot(loss_history,label='Train')
        val_loss, = plt.plot(val_loss_history,label='Validation')
        plt.title('Loss history')
        plt.xlabel('Iteration')
        plt.ylabel('Loss')
        plt.legend(handles=[train_loss, val_loss])
        plt.show()
        
        train_acc = (self.predict(X) == y).mean()
        train_loss, train_grads = self.loss(X, y, wd_decay=wd_decay)
        val_acc = (self.predict(X_val) == y_val).mean()
        val_loss, val_grads = self.loss(X_val, y_val, wd_decay=0) # Weight decay is set to be 0
        
        print('Train accuracy: ',train_acc)
        print('Train loss: ',train_loss)
        print('Validation accuracy: ', val_acc)
        print('Validation loss: ', val_loss, '\n')
        
        return {
          'loss_history': loss_history,
          'val_loss_history': val_loss_history,
          'train_acc_history': train_acc_history,
          'val_acc_history': val_acc_history,
        }

    def predict(self, X):
        """
        Use the trained weights of this two-layer network to predict labels for
        data points. For each data point we predict scores for each of the C
        classes, and assign each data point to the class with the highest score.

        Inputs:
        - X: A numpy array of shape (N, D) giving N D-dimensional data points to
          classify.

        Returns:
        - y_pred: A numpy array of shape (N,) giving predicted labels for each of
          the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
          to have class c, where 0 <= c < C.
        """
        y_pred = None

        y_pred = np.maximum(0,X.dot(self.params['W1'])+self.params['b1']).dot(
            self.params['W2'])+self.params['b2']
        y_pred = np.argmax(y_pred,axis=1)

        return y_pred
