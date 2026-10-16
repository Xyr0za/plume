# Plume
A command-line Python tool that generates organic, coral-like visualizations of the Collatz conjecture by mapping sequences to branching angles.

## Requirements

```pip
matplotlib
numpy
pycairo
```

## Installation

Clone this repo and initialise the virtual environment - then install the requirements using pip. 

```bash
pip install -r requirements.txt
```

## Usage
You can run the script with default settings, which generates a high-resolution, magma-colored visualization for the first 10,000 integers:

```bash
python3 plume.py
```