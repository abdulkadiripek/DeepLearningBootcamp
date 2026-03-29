import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Use all available CPU cores for data loading by default.
NUM_WORKERS = os.cpu_count()

def create_dataloader(train_dir: str,
                      test_dir: str,
                      transforms: transforms.Compose,
                      batch_size: int,
                      num_worksers: int):
    # Load training images from folder structure.
    train_data  = datasets.ImageFolder(root=train_dir,
                                       transform=transforms)

    # Load test images from folder structure.
    test_data = datasets.ImageFolder(root=test_dir,
                                     transform=transforms)

    # Get class names from training dataset folders.
    class_names = train_data.classes

    # Create DataLoader for training data (shuffled each epoch).
    train_dataloader = DataLoader(dataset=train_data,
                                  shuffle=True,
                                  batch_size=batch_size,
                                  num_workers=num_worksers)

    # Create DataLoader for test data (no shuffle for evaluation).
    test_dataloader =  DataLoader(dataset=test_data,
                                  batch_size=batch_size,
                                  shuffle=False,
                                  num_workers=num_worksers)

    # Return both dataloaders and class labels.
    return train_dataloader, test_dataloader, class_names
