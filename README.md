# MIBI scanning GUI

## Aim
The aim of this project is to make configuring MIBI scans easier for a biologist.

## Software Requirements
The user is expected to have Anaconda3 installed. If you have not installed Anaconda3, you can find it here
> https://www.anaconda.com/products/distribution

## Installation
Copy this repository onto your local device and navigate to the `HE_GUI` folder.

Run Anaconda from the Start Menu and create a new environment for heGUI:
```
conda env create -n heGUI -f environment.yml
```
Now run heGUI using the newly created Anaconda environment:
```
conda run -n heGUI .\heGUI\main.pyw
```
