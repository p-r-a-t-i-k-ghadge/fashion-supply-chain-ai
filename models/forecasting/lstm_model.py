import sys
import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader, TensorDataset

class DemandLSTM(nn.Module):
    def __init__(self, input_size=5, hidden_layer_size=50, output_size=1):
        super(DemandLSTM, self).__init__()
        self.hidden_layer_size = hidden_layer_size
        
        # Multi-layer LSTM mapping with dropout for deep regularization
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers=2, batch_first=True, dropout=0.2)
        
        # Dense linear node evaluating terminal predictions
        self.linear = nn.Linear(hidden_layer_size, output_size)

    def forward(self, input_seq):
        # input_seq geometrical shape mapping: (batch_size, sequence_length, input_size)
        lstm_out, _ = self.lstm(input_seq)
        
        # Evaluate singular scalar representation from the final trajectory vector
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions

def create_sequences(data, seq_length=14):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length)]
        y = data[i + seq_length, 0] # Assuming target dimension 'quantity' is index 0
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

def train_model():
    print("Loading PyTorch LSTM Demand Forecasting Engine...")
    
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed", "time_series_ready.csv")
    if not os.path.exists(data_path):
        print(f"Error: Math tensors not found at {data_path}. Please execute PyTorch preprocessing first.")
        return

    df = pd.read_csv(data_path)
    
    # Mathematical variables map: normalized sales, stock constraints, pricing, temporal
    features = ['quantity', 'stock_level', 'base_price', 'day_of_week', 'month']
    data = df[features].values
    
    seq_length = 14 # Look backwards precisely 14 days continuously
    X, y = create_sequences(data, seq_length)
    
    # 80% train ratio partitioning
    train_size = int(len(X) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    
    # Instantiating backend ML tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)
    
    dataset = TensorDataset(X_train_tensor, y_train_tensor)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Injecting AI graph
    model = DemandLSTM(input_size=len(features))
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    epochs = 10
    print(f"Gradient tuning deployed on {len(X_train)} mapped node sequences. Running {epochs} epochs...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for seq, labels in dataloader:
            optimizer.zero_grad() # Re-initialize backprop
            y_pred = model(seq) # Neural forward pass
            
            loss = loss_function(y_pred, labels) # Calculate MSE 
            loss.backward() # Backpropagation
            optimizer.step() # Apply dynamic gradients
            total_loss += loss.item()
            
        print(f'Epoch {epoch+1:3} | Avg Loss Trajectory: {total_loss/len(dataloader):.5f}')
        
    print("AI training successfully completed!")
    
    save_path = os.path.join(os.path.dirname(__file__), "lstm_demand_v1.pth")
    torch.save(model.state_dict(), save_path)
    print(f"Checkpoint safely frozen to disk -> {save_path}")

if __name__ == "__main__":
    train_model()
