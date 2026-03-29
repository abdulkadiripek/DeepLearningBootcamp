import torch 
from torchvision import transforms

import setup_data, training_testing_motor, model_creation, utils

def main():

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

    model = model_creation.DesertClassifier(
        input_shape=3,
        hidden_unit=HIDDEN_UNIT,
        output_shape=len(class_names)
    )

    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(params=model.parameters(), lr=LEARNING_RATE)

    results = training_testing_motor.train(
        model=model,
        train_dataloader=train_dataloader,
        test_dataloader=test_dataloader,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=NUM_EPOCHS
        )
    
    print(f"Final results {results}")

    utils.save_model(model=model,target_dir="models",model_name="desert_classifier.pth")


if __name__ == "__main__":
    #torch.multiprocessing.set_start_method('spawn',force=True)
    main()