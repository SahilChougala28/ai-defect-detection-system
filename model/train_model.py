import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Image Transform
transform = transforms.Compose([

    transforms.Resize((128,128)),
    transforms.ToTensor()

])

# Load Training Dataset
train_dataset = datasets.ImageFolder(

    root="../dataset/train",
    transform=transform

)

# Load Testing Dataset
test_dataset = datasets.ImageFolder(

    root="../dataset/test",
    transform=transform

)

# Data Loaders
train_loader = DataLoader(

    train_dataset,
    batch_size=32,
    shuffle=True

)

test_loader = DataLoader(

    test_dataset,
    batch_size=32,
    shuffle=False

)

# CNN Model
class DefectCNN(nn.Module):

    def __init__(self):

        super(DefectCNN, self).__init__()

        self.conv_layers = nn.Sequential(

            nn.Conv2d(3, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)

        )

        self.fc_layers = nn.Sequential(

            nn.Flatten(),

            nn.Linear(64 * 30 * 30, 128),
            nn.ReLU(),

            nn.Linear(128, 2)

        )

    def forward(self, x):

        x = self.conv_layers(x)
        x = self.fc_layers(x)

        return x

# Initialize Model
model = DefectCNN()

# Loss Function
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.Adam(

    model.parameters(),
    lr=0.001

)

# Training
epochs = 30

for epoch in range(epochs):

    running_loss = 0.0

    for images, labels in train_loader:

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss:.4f}")

# Save Model
torch.save(

    model.state_dict(),
    "defect_model.pth"

)

print("✅ Model Saved Successfully")