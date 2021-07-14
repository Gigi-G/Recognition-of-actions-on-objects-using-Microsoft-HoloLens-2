import torch
from torch import nn
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_size, output_size, hidden_layer_size, num_layers):
        super(LSTM, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_layer_size
        self.output_size = output_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers)
        self.regressor = nn.Linear(hidden_layer_size, output_size)
        
    def forward(self, x, hidden=None):
        if hidden is not None:
            h0 = hidden[0]
            c0 = hidden [1]
        else:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            h0 = torch.zeros(self.num_layers, x.size()[0], self.hidden_size).to(device)
            c0 = torch.zeros(self.num_layers, x.size()[0], self.hidden_size).to(device)
        e = x.view(x.size(1), x.size(0), x.size(2))
        h, hn = self.lstm(e, (h0, c0))
        h = h.view(h.size(1), h.size(0), h.size(2))
        h = h[:,-1,:]
        h = self.regressor(h)
        return h, hn