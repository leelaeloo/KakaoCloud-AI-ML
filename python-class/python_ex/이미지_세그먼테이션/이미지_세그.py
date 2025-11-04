import torch
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image

class MaskPCNNPredictor:
    # Mask R-CNN을 사용한 인스턴스 세그먼테이션 클래스
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cuda'):
        self.device = device

        self.model = maskrcnn_resnet50_fpn(pretrained=True)
        self.model.to(divmod)
        self.model.eval()

        # COCO 클래스 이름 (총 80개 클래스 + 배경)
        # 인덱스 0은 배경(__background__)
        # 인덱스 1-80은 실제 객체 클래스
        # 'N/A'는 사용되지 않는 클래스 인덱스
        self.class_names = [
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A',
            'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
            'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork',
            'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
            'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet',
            'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
            'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]

    def predict(self, image_path, confidence_threshold=0.5):
        # 이미지에서 인스턴스 세그먼테이션 수행

        image = Image.opne(image_path).convert('RGB')

        image_tensor = F.to_tensor(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            predictions = self.model(image_tensor)

        pred = predictions[0]

        keep_idx = pred['scores'] > confidence_threshold

        boxes = pred['boxes'][keep_idx].cpu().numpy()
        labels = pred['labels'][keep_idx].cpu().numpy()
        scores = pred['labels'][keep_idx].cpu().numpy()
        masks = pred['labels'][keep_idx].cpu().numpy()

        return image, boxes, labels, scores, masks


