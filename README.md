# ARMconv 
#### *Azure Sentinel Playbook and Workbook Converter*
#### Author: Tom Porter

## Overview

The Azure Sentinel Playbook and Workbook Converter is a tool designed to replace static variables in ARM templates with dynamic values. This enables the deployment of these templates in different Azure Sentinel resources and subscriptions.

## Features

- Converts Playbooks and Workbooks ARM templates.
- Replaces static variables with dynamic values.
- Facilitates deployment in various Azure Sentinel environments.

## Prerequisites

- Python 3.x installed on your machine.
- Ensure that the required Python packages are installed. You can install them using:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Clone this repository:

    ```bash
    https://github.com/tvp227/ARMconv.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ARMConv
    ```

3. Run the converter script:

    ```bash
    python ConverterGUI.py
    ```

4. The converted templates can overwrite the original or be saved wherever the user sees fit.

## Example
![image](https://github.com/tvp227/ARMconv/assets/46229276/d26eccc5-0fca-4373-9645-76057e0d3833)
![image](https://github.com/tvp227/ARMconv/assets/46229276/d8a796ec-02aa-4f27-bbbd-0f340900e77a)
*Lists the variables and highlights the convertions*
![image](https://github.com/tvp227/ARMconv/assets/46229276/50fda650-b493-4b49-bfac-081cc77c1258)
![image](https://github.com/tvp227/ARMconv/assets/46229276/6d9675d7-107f-4935-b581-111bf2ab761f)
<div>

  *Changes to parameters made*

![image](https://github.com/tvp227/ARMconv/assets/46229276/b373388d-37d3-4bd0-8a76-ce8ccb3414d2) ![image](https://github.com/tvp227/ARMconv/assets/46229276/01a11a0b-d6d7-4262-8d59-aa76b2eb5893)