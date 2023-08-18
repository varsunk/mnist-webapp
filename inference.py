import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F

MODEL_PATH = 'model/mnist_model.pt'

# define model here (so importing nn.ipynb is not necessary)
class CNN(nn.Module):
    def __init__(self, in_channels = 1, num_classes = 10):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=(3,3), stride=(1,1), padding=(1,1))
        self.pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2,2))
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3,3), stride=(1,1), padding=(1,1))
        self.fc1 = nn.Linear(16*7*7, num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.reshape(x.shape[0], -1)
        x = self.fc1(x)

        return x

def make_prediction(image_path):
    model = CNN()
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # pre-processing
    img = cv2.bitwise_not(img)
    img = img/255.
    img = torch.Tensor(img).unsqueeze(axis=0).unsqueeze(axis=0)

    # performing inference
    scores = model(img)
    _, pred = scores.max(1)

    return pred[0].item()


# if __name__ == '__main__':
#     # testing
#     model = CNN()
#     model.load_state_dict(torch.load(MODEL_PATH))
#     model.eval()

#     img = cv2.imread('static/uploads/8.png')
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # invert colors
#     img = cv2.bitwise_not(img)
#     img = img/255.
#     img = torch.Tensor(img).unsqueeze(axis=0).unsqueeze(axis=0)
#     # print(img)
#     # print(img.shape)
#     scores = model(img)
#     _, pred = scores.max(1)
#     print(pred[0].item())
    # print(make_prediction('static/uploads/8.png'))