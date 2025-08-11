import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# Pick device: AMD GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

## define Sequential model with 3 layers
class SequentialNetwork(nn.Module):
    def __init__(self, input_dim, output_dim, num_epochs):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.num_epochs = num_epochs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Define model architecture
        self.net = nn.Sequential(
            nn.Linear(self.input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, self.output_dim)
        ).to(self.device)

        # Loss (MAPE equivalent) — PyTorch doesn't have built-in MAPE, so we implement it
        self.loss_fn = lambda pred, target: torch.mean(torch.abs((target - pred) / target)) * 100

        # Optimizer
        self.optimizer = optim.Adam(self.net.parameters(), lr=0.001)

    def train(self, training_set_in, training_set_out):
        # Convert numpy arrays or lists to torch tensors
        X = torch.tensor(training_set_in, dtype=torch.float32)
        y = torch.tensor(training_set_out, dtype=torch.float32)

        dataset = TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=2, shuffle=True)

        for epoch in range(self.num_epochs):
            self.net.train()
            epoch_loss = 0
            correct = 0
            total = 0
            for batch_X, batch_y in loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.net(batch_X)

                # custom MAPE
                #loss = self.loss_fn(outputs, batch_y)
                # MSE loss
                loss = F.mse_loss(outputs, batch_y)
                # MAE loss (absolute error)
                # loss = F.l1_loss(outputs, batch_y)
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item() * batch_X.size(0)

                # calculating metrics
                preds = outputs.detach()
                correct += torch.sum(torch.isclose(preds, batch_y, atol=1e-1)).item()
                total += batch_y.numel()

            print(f"Epoch [{epoch+1}/{self.num_epochs}] - Loss: {epoch_loss/len(dataset):.4f} - Accuracy: {correct/total:.4f}")
        
        return self

    def predict(self, inputs):
        # switch to eval mode
        self.net.eval()
        with torch.no_grad():
            inputs = torch.tensor(inputs, dtype=torch.float32)
            data = inputs.to(self.device)    
            output = self.net(data)
            return output
    
    def sample_from_output(self, params, num_samples=1):
        # dummy function
        return params