"""
Copyright (c) Hitachi, Ltd. and its affiliates.
All rights reserved.

This source code is licensed under the license found in the
LICENSE file in the CDB-loss/CIFAR-LT directory.
=======
"""

import numpy as np
import pickle
import json

def load_data(args):
     
     train_images = np.zeros([0, 3072])
     train_labels = np.zeros(0)
     
     if args.class_num == 100:
         train_path = './data/cifar-100-python/train'
         with open(train_path, 'rb') as f:
             dict = pickle.load(f, encoding='bytes')
         train_images = np.concatenate((train_images, dict[b'data']),0)
         train_labels = np.concatenate((train_labels, dict[b'fine_labels']),0)
     
     elif args.class_num == 10:
         train_data_1 = './data/cifar-10-batches-py/data_batch_1'
         for i in range(5):
             with open(train_data_1.replace('_1', '_'+ str(i+1)), 'rb') as f:
                 dict = pickle.load(f, encoding='bytes')
             train_images = np.concatenate((train_images, dict[b'data']),0)
             train_labels = np.concatenate((train_labels, dict[b'labels']),0)

        
     else:
       raise NotImplementedError
     
     return train_images, train_labels


     



def load_test_data(args):

     test_images = np.zeros([0,3072])
     test_labels = np.zeros(0)
     coarse_labels = np.zeros(0)
     if args.class_num == 100:
        test_path = './data/cifar-100-python/test'
        label = b'fine_labels'
     elif args.class_num == 10:
        test_path = './data/cifar-10-batches-py/test_batch'
        label = b'labels'     
     else:
         raise NotImplementedError


     with open(test_path, 'rb') as f:
        dict = pickle.load(f, encoding='bytes')
        test_images = np.concatenate((test_images, dict[b'data']))
        test_labels = np.concatenate((test_labels, dict[label]))
        coarse_labels = np.concatenate((coarse_labels, dict[b'coarse_labels']))
     with open(test_path.replace('test', 'meta'), 'rb') as f:
        dict = pickle.load(f, encoding='bytes')
        print(dict.keys())
        class_names = dict[b'fine_label_names']
     
     
     return test_images, test_labels, class_names

def sep_train_val(images, labels, args):
     
     
     train_indices = np.zeros(0)
     val_indices = np.zeros(0)
     
     for cls in range(args.class_num):
         loc = np.where(labels == cls)[0]
         train_indices = np.concatenate((train_indices, loc[ : - args.val_samples_per_class]), 0)
         val_indices = np.concatenate((val_indices, loc[ - args.val_samples_per_class : ]), 0)
     train_indices, val_indices = train_indices.astype(int), val_indices.astype(int)

     return images[train_indices], labels[train_indices], images[val_indices], labels[val_indices]


def create_imbalance(images, labels, args):
      if args.imbalance == 1:
           return images, labels
      
      imb = 1/args.imbalance
      train_images_per_class = int(labels.size/args.class_num)
      selected_indices = np.zeros(0)
      
      for cls in range(args.class_num):
          loc = np.where(labels == cls)[0]
          slct_amt = int(train_images_per_class * (imb ** (cls/(args.class_num-1))))
          selected_indices = np.concatenate((selected_indices, loc[ : slct_amt]), 0)
      
      return images[selected_indices.astype(int)], labels[selected_indices.astype(int)]
     
     