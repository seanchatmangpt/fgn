import torch
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split

class CodeData(Dataset):
    """
    Dataset for storing code and corresponding distances.
    """
    def __init__(self, codes, distances):
        """
        Initialize CodeData instance.

        :param codes: List of source code sequences
        :param distances: List of estimated distances
        """
        self.codes = codes
        self.distances = distances

    def __len__(self):
        return len(self.codes)

    def __getitem__(self, idx):
        return self.codes[idx], self.distances[idx]

class CodeDistanceModel(nn.Module):
    """
    Neural network model for estimating code distances.
    """
    def __init__(self):
        super(CodeDistanceModel, self).__init__()
        self.fc1 = nn.Linear(512, 512)   # Choose the dimension according to your feature set
        self.fc2 = nn.Linear(512, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_model(model, data_loader, criterion, optimizer):
    """
    Function to train the model.

    :param model: Model to be trained
    :param data_loader: DataLoader for the training data
    :param criterion: Loss function
    :param optimizer: optimizer
    """
    model.train()
    running_loss = 0
    for i, data in enumerate(data_loader):
        # get the inputs
        codes, distances = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(codes)
        loss = criterion(outputs, distances)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(data_loader)
    return avg_loss

def evaluate_model(model, data_loader, criterion):
    """
    Function to evaluate the model.

    :param model: Model to be evaluated
    :param data_loader: DataLoader for the evaluation data
    :param criterion: Loss function
    """
    model.eval()
    running_loss = 0
    with torch.no_grad():
        for i, data in enumerate(data_loader):
            # get the inputs
            codes, distances = data

            # forward
            outputs = model(codes)
            loss = criterion(outputs, distances)

            running_loss += loss.item()

    avg_loss = running_loss / len(data_loader)
    return avg_loss

def run_training_and_evaluation(codes, distances, epochs=5):
    """
    Function to train and evaluate the model.

    :param codes: List of source code sequences
    :param distances: List of estimated distances
    :param epochs: Number of training epochs
    """
    # Split data into train and test sets
    codes_train, codes_test, distances_train, distances_test = train_test_split(codes, distances, test_size=0.2)

    # Create datasets
    train_data = CodeData(codes_train, distances_train)
    test_data = CodeData(codes_test, distances_test)

    # Create data loaders
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

    # Create model, criterion and optimizer
    model = CodeDistanceModel()
    criterion = nn.MSELoss() # Mean Squared Error Loss for regression task
    optimizer = optim.Adam(model.parameters())

    for epoch in range(epochs):
        # Train and evaluate model
        train_loss = train_model(model, train_loader, criterion, optimizer)
        eval_loss = evaluate_model(model, test_loader, criterion)

        print(f"Epoch {epoch+1}/{epochs}.. "
              f"Train loss: {train_loss:.3f}.. "
              f"Validation loss: {eval_loss:.3f}")
