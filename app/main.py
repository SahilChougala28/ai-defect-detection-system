from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import torch
import torch.nn as nn

from torchvision import transforms
from PIL import Image

import io

# FastAPI App
app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Image Transform
transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor()
])

# CNN Model
class DefectCNN(nn.Module):

    def __init__(self):

        super(DefectCNN, self).__init__()

        self.conv_layers = nn.Sequential(

            nn.Conv2d(3, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2)

        )

        self.fc_layers = nn.Sequential(

            nn.Flatten(),

            nn.Linear(64 * 30 * 30, 128),
            nn.ReLU(),

            nn.Linear(128, 2)

        )

    def forward(self, x):

        x = self.conv_layers(x)
        x = self.fc_layers(x)

        return x

# Load Model
model = DefectCNN()

model.load_state_dict(
    torch.load("model/defect_model.pth")
)

model.eval()

# Classes
classes = [
    "Defective",
    "Non_Defective"
]

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# Prediction Route
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    with torch.no_grad():

        outputs = model(image)

        _, predicted = torch.max(outputs, 1)

        prediction = classes[predicted.item()]

    return f"""

    <html>

    <head>

        <link rel="stylesheet" href="/static/style.css">

    </head>

    <body>

        <div class="container">

            <h1>Prediction Result</h1>

            <h2>{prediction}</h2>

            <a href="/">
                <button>Try Another Image</button>
            </a>

        </div>

    </body>

    </html>

    """