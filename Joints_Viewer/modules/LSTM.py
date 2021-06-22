import torch
from torch import nn
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_size, output_size=4, hidden_layer_size=78, num_layers=1):
        super(LSTM, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_layer_size 
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers)
        self.regressor = nn.Linear(hidden_layer_size, output_size)
        
    def forward(self, x, hidden=None):
        if hidden is not None:
            h0 = hidden[0]
            c0 = hidden [1]
        else:
            h0 = torch.zeros(self.num_layers, 1, self.hidden_size).to(
                torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            )
            c0 = torch.zeros(self.num_layers, 1, self.hidden_size).to(
                torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            )
        h, hn = self.lstm(x.view(len(x), 1, -1), (h0, c0))
        h = self.regressor(h.view(len(x), -1))        
        return h, hn