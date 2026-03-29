import torch
from torch import nn

def train_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer,
              ):
    model.train() # Modelimizi train moduna alıyoruz.
    
    train_loss = 0 # Train Loss değerlerini tutmak için bir değişken oluşturuyoruz.
    train_acc = 0 # Train Accuracy değerlerini tutmak için bir değişken oluşturuyoruz.

    for batch, (X,y) in enumerate(dataloader): # Batch size gerekli değil burada.
        y_pred = model(X) # Modelimize bir tahminde bulunduruyoruz.
        
        loss = loss_fn(y_pred,y) # Loss değerlerimizi loss_fn ile hesaplıyoruz.
        train_loss += loss.item() # Çıkan loss değerlerini train_loss değişlenine toplayarak atıyoruz.

        # Modelimizi backpropagation yapıyoruz.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Softmax kullanarak modelimize label tahmininde bulunduruyoruz.
        y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1) 
        
        train_acc += (y_pred_class == y).sum().item() / len(y_pred) # Accuracy değerlerimizi bir değişkende tutuyoruz.

    train_loss /= len(dataloader) # Train Loss değerlerimizi dataloader boyuna bölüyoruz ve ort. elde ediyoruz.
    train_acc /= len(dataloader) # Train Acc değerlerimizi dataloader boyuna bölüyoruz ve ort. elde ediyoruz
    return train_loss, train_acc # Geriye train_loss ve train_acc döndürüyoruz.

def test_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
              ):
    model.eval() # Modelimizi test moduna alıyoruz.
    
    test_loss = 0 # test loss'ları tutmak için bir değişken oluşturuyoruz.
    test_acc = 0 # test accuracy'ları tutmak için bir değişken oluşturuyoruz.
    
    with torch.inference_mode(): # inference mode'a aldık.
        for batch, (X,y) in enumerate(dataloader): # batch gerekli değil fakat yine de aldık.
            test_pred = model(X) # modelimize tahmin ettiriyoruz.
            
            loss = loss_fn(test_pred,y) # loss'umuzu loss_fn ile hesaplıyoruz.
            test_loss += loss.item() # loss değerlerimizi test_loss değişkeninde topluyoruz.

            # Softmax activation function ile label tahmin ettiriyoruz.
            test_pred_label = torch.softmax(test_pred,dim=1).argmax(dim=1) 
            
            acc = (test_pred_label == y).sum().item() / len(test_pred) # Calculate accuracy
            test_acc += acc # Accuracy değerlerimizi toplayıp test_acc değişkenine atıyoruz.
            
    test_loss /= len(dataloader) # Test loss değerlerimizi dataloader boyuna bölüyoruz.
    test_acc /= len(dataloader) # Test acc değerlerimizi dataloader boyuna bölüyoruz.
    
    return test_loss, test_acc # Geriye test_loss ve test_acc döndürüyoruz.

def train(model: torch.nn.Module,
               train_dataloader: torch.utils.data.DataLoader,
               test_dataloader: torch.utils.data.DataLoader,
               optimizer: torch.optim.Optimizer,
               loss_fn: torch.nn.Module = nn.CrossEntropyLoss(),
               epochs:int = 10,
              ):
    results = {
        "train_loss": [],
        "train_acc": [],
        "test_loss": [],
        "test_acc": []
    }
    for epoch in range(epochs):
        train_loss, train_acc = train_step(model = model,
                                           dataloader = train_dataloader,
                                           loss_fn = loss_fn,
                                           optimizer = optimizer,
                                          )
        test_loss, test_acc = test_step(model = model,
                                           dataloader = test_dataloader,
                                           loss_fn = loss_fn,
                                          )
        print(f""" 
        Epoch:{epoch}
        Train Loss : {train_loss:.2f} -  Train Accuracy : {train_acc*100:.2f}
        Test Loss  : { test_loss:.2f} -  Test Accuracy  : {test_acc*100:.2f}
        """)
        results["train_loss"].append(train_loss.item() if isinstance(train_loss, torch.Tensor) else train_loss)
        results["train_acc"].append(train_acc.item() if isinstance(train_acc, torch.Tensor) else train_acc)
        results["test_loss"].append(test_loss.item() if isinstance(test_loss, torch.Tensor) else test_loss)
        results["test_acc"].append(test_acc.item() if isinstance(test_acc, torch.Tensor) else test_acc)
    return results