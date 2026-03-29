from typing import Any

import torch
import torch.nn as nn

class DesertClassifier(nn.Module):

    def __init__(self, input_shape:int, hidden_unit:int, output_shape:int):
        super().__init__()
        self.conv_block_1 = nn.Sequential(
            nn.Conv2d(in_channels=input_shape,
                      out_channels=hidden_unit,
                      kernel_size=3,
                      stride=1,
                      padding=1
                      ),
            nn.GELU(),
            nn.Conv2d(in_channels=hidden_unit,
                      out_channels=hidden_unit,
                      kernel_size=3,
                      stride=1,
                      padding=1
                      ),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2,stride=2)
        )

        self.conv_block_2 = nn.Sequential(
            nn.Conv2d(in_channels=hidden_unit,
                      out_channels=hidden_unit,
                      kernel_size=3,
                      stride=1,
                      padding=1
                      ),
            nn.GELU(),
            nn.Conv2d(in_channels=hidden_unit,
                      out_channels=hidden_unit,
                      kernel_size=3,
                      stride=1,
                      padding=1
                      ),
            nn.GELU(),
            nn.MaxPool2d(kernel_size=2,stride=2)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hidden_unit*16*16, 
                      out_features=output_shape)
        )
    
    def forward(self,x):
        x= self.conv_block_1(x)
        x= self.conv_block_2(x)
        x= self.classifier(x)
        return x