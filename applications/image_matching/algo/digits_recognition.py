import torch
from matplotlib import pyplot as plt
from torch import nn, optim
from torch.utils.data import random_split, DataLoader
from torchvision import datasets, transforms

dataset = datasets.MNIST(
	'data/mnist', train=True, download=True, transform=transforms.ToTensor())

img_batch, label = dataset[0]

img_batch.shape

plt.imshow(img_batch[0], cmap='gray')
plt.show()

train, val = random_split(dataset, [55000, 5000])
train_loader = DataLoader(train, batch_size=32)
val_loader = DataLoader(val, batch_size=32)

# Step 1: Define the model
model = nn.Sequential(
	nn.Linear(784, 128),
	nn.ReLU(),
	nn.Linear(128, 64),
	nn.ReLU(),
	nn.Linear(64, 64),
	nn.ReLU(),
	nn.Linear(64, 128),
	nn.ReLU(),
	nn.Linear(128, 10)
)

# Step 2: Define an optimizer
optimizer = optim.Adam(model.parameters(), lr=1e-2)

# Step 3: Define a loss function
loss = nn.CrossEntropyLoss()

# Step 4: Train the model
epochs = 100
for epoch in range(epochs):
	train_losses = list()
	train_accuracy = list()
	for batch in train_loader:
		x, y = batch

		# Convert this to (batch, dimensions) without the color channel
		b = x.size(0)
		x = x.view(b, -1)

		# Forward pass
		logits = model(x)

		# Calculate loss
		J = loss(logits, y)

		# Reset the accumulated gradient map
		model.zero_grad()

		# Backpropagate the error
		J.backward()

		# Update the parameters
		optimizer.step()

		train_losses.append(J.item())
		train_accuracy.append(
			y.eq(logits.argmax(dim=1).float().mean()))

	# Validation
	val_losses = list()
	val_accuracy = list()
	for batch in val_loader:
		x, y = batch

		# Convert this to (batch, dimensions) without the color channel
		b = x.size(0)
		x = x.view(b, -1)

		# Forward pass
		with torch.no_grad(x):
			logits = model(x)

		# Calculate loss
		J = loss(logits, y)

		val_losses.append(J.item())
		val_accuracy.append(
			y.eq(logits.argmax(dim=1).float().mean()))

	print(
		f'Epoch {epoch + 1}, train loss: {torch.tensor(train_losses).mean():.2f},'
		f'val loss: {torch.tensor(val_losses).mean():.2f}\n'
		f'train accuracy: {torch.tensor(train_accuracy).mean():.2f}, '
		f'val accuracy: {torch.tensor(val_accuracy).mean():.2f}\n')
