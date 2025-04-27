import copy
import os
import random
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data
import torchvision.datasets as datasets
import torchvision.transforms as transforms


def main():
    # training_dir = os.environ["TRAINING_DATA_DIR"]
    SEED = 1234

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True

    ROOT = ".data"

    train_data = datasets.MNIST(root=ROOT, train=True, download=True)

    mean = train_data.data.float().mean() / 255
    std = train_data.data.float().std() / 255

    print(f"Calculated mean: {mean}")
    print(f"Calculated std: {std}")


if __name__ == "__main__":
    main()
