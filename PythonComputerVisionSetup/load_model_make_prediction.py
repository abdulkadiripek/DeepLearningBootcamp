import torch
from model_creation import DesertClassifier
import torchvision
from torchvision import transforms
import setup_data

MODEL_SAVE_PATH = 'models/desert_classifier.pth'

NUM_EPOCHS = 10
BATCH_SIZE = 32
HIDDEN_UNIT = 32
LEARNING_RATE = 0.0003

train_dir = "data/desert101/train"
test_dir = "data/desert101/test"

data_transform = transforms.Compose([
    transforms.Resize(size=(64,64)), 
    transforms.RandomRotation(degrees=20),   
    transforms.ToTensor(),
    transforms.Normalize([0.5483, 0.4638, 0.3865],[0.2542, 0.2576, 0.2630]),
    ])

train_dataloader, test_dataloader, class_names= setup_data.create_dataloader(
    train_dir=train_dir,
    test_dir=test_dir,
    batch_size=BATCH_SIZE,
    transforms=data_transform
)

load_model = DesertClassifier(
    input_shape=3,
    hidden_unit=HIDDEN_UNIT,
    output_shape=len(class_names))

load_model.load_state_dict(torch.load(f=MODEL_SAVE_PATH))

from pathlib import Path
data_path = Path("data/")
image_path = data_path / "baklava.jpg"
single_image = torchvision.io.read_image(path=str(image_path)).type(torch.float32)
single_image /= 255
single_image_transforms = transforms.Compose([
    transforms.Resize(size=(64,64))
])
single_image = single_image_transforms(single_image)
single_image = single_image.unsqueeze(dim=0)

load_model.eval()
with torch.inference_mode():
    logits = load_model(single_image)
    probs = torch.softmax(logits,dim=1)
    pred_idx = torch.argmax(probs,dim=1)

print("Predicted class: ", class_names[pred_idx])