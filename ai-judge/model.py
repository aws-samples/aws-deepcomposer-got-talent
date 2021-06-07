# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import torch
from torch.autograd import Variable
from torch.nn import Linear, ReLU, CrossEntropyLoss, Sequential, Conv2d, AdaptiveMaxPool2d, MaxPool2d, Module, Softmax, BatchNorm2d, Dropout
from torch.optim import Adam, SGD
from tqdm import tqdm
torch.manual_seed(0)

class CNN(Module):
    def __init__(self):
        super(CNN, self).__init__()
        
        self.conv2D_1 = Sequential(
            Conv2d(1, 16, kernel_size=5, stride=2, padding=2),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2))
        self.conv2D_2 = Sequential(
            Conv2d(16, 32, kernel_size=5, stride=2, padding=2),
            ReLU(),
            AdaptiveMaxPool2d((5, 5)))
        self.dropout = Dropout(0.5)
        self.linear_1 = Linear(5 * 5 * 32, 100)
        self.linear_2 = Linear(100, 2)

    def forward(self, x):
        x = self.conv2D_1(x)
        x = self.dropout(x)
        x = self.conv2D_2(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.linear_1(x)
        x = self.linear_2(x)
        return x
