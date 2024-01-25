### Initialize Poetry

Navigate to the project's root directory in the terminal and run:

```poetry init ```

### Poetry configuration
Specify the URL where the  CPU-only wheels for PyTorch are located, reducing size considerably (no GPU needed):

```poetry source add -p explicit pytorch https://download.pytorch.org/whl/cpu```

### Adding Dependencies
Use poetry to add the dependencies of the project:

```poetry add --source pytorch torch torchvision```

```poetry add fastapi uvicorn pydantic transformers ```

> Note: sqlite3 is already included in Python standard library




