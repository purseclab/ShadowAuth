# ECU Firmware Static Analysis Tool

Goal: To distinguish not CAN Transmission functions from the given ECU firmware

## Env

Python 3.8.10

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ~~ToPcode.py
python CANTxFilter.py
```

## Example

Modify contents of CANTxFilter.py as follows:
```python
...
path = ms3_pcode
ans = 0xc301
...

```

```bash
python Ms3ToPcode.py # don't have to rerun once it is done
... # takes long time
python CANTxFilter.py
132/239
True
```
-> means 132 functions *might be* CAN Tx function out of 239.

-> guarantees other (239-132) functions are *not* CAN Tx functions.

-> True means it cross checked by the given address of CAN Tx function from user input (0xc301).

Also you will get `ms3_pcode_basicblock_str_distribution.txt` and `ms3_pcode_fucntion_str_distribution.txt`

e.g.,
```
3
4
5
```
meaning MS3's have three or more store insturctions, accessing to the three different addresses.

Their store sizes are 3, 4, and 5 responsively.

`_basicblock_str_distribution.txt` describes the store insturctions per basic block.

`_function_str_distribution.txt` describes the store insturctions per functions.

## ~~ToPcode.py

### Input: Two files

* ELF, ECU firmware
* map of functions of the firmware


map file example

```
can_sendburn .text3 00004000 00000052
can_crc32 .text3 00004052 00000050
can_reqdata .text3 000040A2 0000000E
```
Each field is separated by space  
1. Function name (optional)
2. Section name
3. Function's offset of the ELF (where is the function in the ELF?)
4. Function length


### Output: One or more P-code lifted files

Each file contains Pcode-lifted strings of each function of the ELF.

File's name is identical to the function's ***virtual address***.

## CANTxFilter.py

### Input: Output of ~~ToPcode.py

### Output: Ratio, a out of b

a means the nubmer of the CAN transmission functions with false positives.

b means the number of all functions.