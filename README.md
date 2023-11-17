# ARMconv 
### *Azure Sentinel Playbook and Workbook Converter*
### Author: Tom Porter

## Overview
This suite of tools is designed to assist security engineers in Azure Sentinel deployments. The toolset can convert Sentinel playbooks and workbooks into dynamic templates, facilitating deployments across various domains. It also offers additional capabilities for converting KQL queries into ARM template formats.

## Features

- Converts Playbooks and Workbooks to ARM templates.
- Replaces static variables with dynamic values.
- Converts KQL queries into ARM template formats.
- Facilitates deployment in various Azure Sentinel environments.

## Prerequisites

- Python 3.x installed on your machine.
- Ensure that the required Python packages are installed. You can install them using:

    ```bash
    pip install -r requirements.txt
    ```
- Access to a Sentinel instance.
  
## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/tvp227/ARMconv.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ARMConv
    ```

3. Run the converter script:

    ```bash
    python ConverterGUI.py
    ```

4. The converted templates can overwrite the original or be saved wherever the user sees fit. The additional tools available help adjust and manage the code used for Sentinel deployments.

## Example
#### *GUI- All the tools available*

![Screenshot 2023-11-16 221501](https://github.com/tvp227/ARMconv/assets/46229276/ff8297ac-340a-40cd-b588-166440b3c8ae)

#### *When converting templates it will lists the variables and highlights the conversions being implemented*

![Example Image 3](https://github.com/tvp227/ARMconv/assets/46229276/50fda650-b493-4b49-bfac-081cc77c1258)
![Example Image 4](https://github.com/tvp227/ARMconv/assets/46229276/6d9675d7-107f-4935-b581-111bf2ab761f)

#### *Changes to parameters made*

![Example Image 5](https://github.com/tvp227/ARMconv/assets/46229276/b373388d-37d3-4bd0-8a76-ce8ccb3414d2) ![Example Image 6](https://github.com/tvp227/ARMconv/assets/46229276/01a11a0b-d6d7-4262-8d59-aa76b2eb5893)

### *Additional tools*
#### *KQL converter - Input the KQL query and will output text appropriate for template consumption*
![Screenshot 2023-11-16 221742](https://github.com/tvp227/ARMconv/assets/46229276/f741c975-e50a-4ce1-8762-fcbfb101e845)