import torch
from pathlib import Path
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
import setup_data

def save_model(
        model:torch.nn.Module,
        target_dir:str,
        model_name: str):
    
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True, exist_ok=True)

    model_save_path = target_dir_path / model_name
    torch.save(obj=model.state_dict(), f=model_save_path)


def calculate_mean_std(dataset_path, batch_size=64):
    # Görselleri [0, 1] arasına çeken transform (ToTensor bunu otomatik yapar)
    # Not: Görseller farklı boyutlardaysa Resize eklemek gerekebilir.
    transform = transforms.Compose([
        transforms.Resize((224, 224)), # Opsiyonel: Boyutlar farklıysa sabitleyin
        transforms.ToTensor()
    ])

    # Eğer alt klasörler (class folders) varsa ImageFolder kullanın
    # Eğer yoksa, görseller doğrudan klasördeyse özel bir Dataset sınıfı gerekebilir.
    dataset = datasets.ImageFolder(dataset_path, transform=transform)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    cnt = 0
    fst_moment = torch.empty(3)
    snd_moment = torch.empty(3)

    print("Hesaplanıyor, lütfen bekleyin...")
    for images, _ in loader:
        b, c, h, w = images.shape
        nb_pixels = b * h * w
        sum_ = torch.sum(images, dim=[0, 2, 3])
        sum_of_square = torch.sum(images ** 2, dim=[0, 2, 3])
        
        fst_moment = (cnt * fst_moment + sum_) / (cnt + nb_pixels)
        snd_moment = (cnt * snd_moment + sum_of_square) / (cnt + nb_pixels)
        cnt += nb_pixels

    mean = fst_moment
    std = torch.sqrt(snd_moment - fst_moment ** 2)

    return mean, std

if __name__ == "__main__":

    train_dir = "data/desert101/train"
    test_dir = "data/desert101/test"

    mean,std = calculate_mean_std(train_dir)
    print("Mean: ",mean)
    print("Std: ",std)