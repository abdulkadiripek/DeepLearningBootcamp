import torch 
from torchvision import transforms

import setup_data, training_testing_motor, models, utils

def main():

    NUM_EPOCHS = 10
    BATCH_SIZE = 32
    HIDDEN_UNIT = 32
    LEARNING_RATE = 0.0001

    train_dir = "data/desert101/train"
    test_dir = "data/desert101/test"

    data_transform = transforms.Compose([
    transforms.Resize(size=(64,64)),    
    transforms.RandomHorizontalFlip(p=0.4),  
    transforms.RandomRotation(degrees=15),
    transforms.ToTensor(),
    transforms.Normalize([0.5483, 0.4638, 0.3865],[0.2542, 0.2576, 0.2630])])

    train_dataloader, test_dataloader, class_names= setup_data.create_dataloader(
        train_dir=train_dir,
        test_dir=test_dir,
        batch_size=BATCH_SIZE,
        transforms=data_transform
    )