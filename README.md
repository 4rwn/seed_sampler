# GUI Application to Calculate a Seed Sampling Strategy
## Usage
The application works on four floating-point inputs:
* Original sample weight in grams (e.g. 250)
* Desired weight in grams (e.g. 100)
* Tolerance as a percentage (e.g. 5%)
* Margin inside the tolerance interval as a percentage (e.g. 20%)

A strategy will be calculated that respects the tolerance (100-105g) and keeps a certain margin to the tolerance boundaries (101-104g) to account for the fact that the divider does not exactly split its input sample in half.
In this case, the output weight is 101.563g and the strategy is:
1. L
2. R
3. R
4. L

To employ the strategy with the divider follow these steps:
1. Start at a 50-50 distribution of the sample in the trays, i.e. the state after the initial mixing.
2. Divide the trays as indicated by the strategy in order.
3. The new sample of the desired weight is in the left tray in the end.

## Building and Running
The application uses Python and the `keyboard` library.

To bundle a stand-alone Windows .exe, use PyInstaller on a Windows machine as `$ python -m PyInstaller --onefile --noconsole seed_sample_calculator.py`