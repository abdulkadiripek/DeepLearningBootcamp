import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

NUM_WORKERS = os.cpu_count()

def create_dataloader(train_dir: str,
                      test_dir: str,
                      transforms: transforms.Compose,
                      batch_size: int,
                      num_worksers: int):
    
    train_data  = datasets.ImageFolder(root=train_dir,
                                       transform=transforms)

    test_data = datasets.ImageFolder(root=test_dir,
                                     transform=transforms)

    class_names = train_data.classes

    train_dataloader = DataLoader(dataset=train_data,
                                  shuffle=True,
                                  batch_size=batch_size,
                                  num_workers=num_worksers)
    
    test_dataloader =  DataLoader(dataset=test_data,
                                  batch_size=batch_size,
                                  shuffle=False,
                                  num_workers=num_worksers)

    return train_dataloader, test_dataloader, class_names
    