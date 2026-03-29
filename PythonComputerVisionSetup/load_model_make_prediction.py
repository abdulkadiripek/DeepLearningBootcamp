import torch
from model_creation import DesertClassifier

MODEL_SAVE_PATH = 'models/desert_classifier.pth'

load_model = DesertClassifier(
    input_shape=3,
    hidden_unit=32,
    output_shape=4)

load_model.load_state_dict(torch.load(MODEL_SAVE_PATH))