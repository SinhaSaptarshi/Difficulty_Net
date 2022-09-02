"""
Copyright (c) Hitachi, Ltd. and its affiliates.
All rights reserved.

This source code is licensed under the license found in the
LICENSE file in the CDB-loss/CIFAR-LT directory.
=======
"""

import numpy as np
import torch




def sigmoid(x):
   return (1/(1+np.exp(-x)))

def compute_weights(class_wise_accuracy, tau='dynamic', normalize=True, epsilon=0.01):
    if tau == 'dynamic':
        bias = np.max(class_wise_accuracy)/(np.min(class_wise_accuracy) + epsilon)
        tau = 2 * sigmoid(bias-1)
    else:
        tau = float(tau)
    class_wise_difficulty = 1 - (class_wise_accuracy/class_wise_accuracy.sum())
    cdb_weights = (class_wise_difficulty)**tau
    assert (cdb_weights < 0).sum() == 0
    if normalize:
         cdb_weights = cdb_weights/ cdb_weights.sum() * len(cdb_weights)   #normalizing weights to make sum of weights = number of classes
    
    #return torch.FloatTensor(cdb_weights)
    return cdb_weights