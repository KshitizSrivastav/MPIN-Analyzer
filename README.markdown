# MPINChecker

## Overview
MPINChecker is a Python program designed to validate the strength of Mobile Personal Identification Numbers (MPINs) used for mobile banking apps. It checks if an MPIN is commonly used or derived from user demographics (e.g., date of birth, spouse's date of birth, or wedding anniversary). The program supports both 4-digit and 6-digit MPINs and provides detailed outputs for strength and reasons for weakness, as specified by OneBanc Technologies Pvt. Ltd.

## Features
The program is divided into four parts, as outlined in the requirements:
1. **Part A**: Checks if a 4-digit MPIN is commonly used (e.g., repetitive, sequential, or paired digits).
2. **Part B**: Evaluates the strength of a 4-digit MPIN (WEAK or STRONG) based on common patterns and demographic data.
3. **Part C**: Extends Part B to include reasons for weakness (e.g., COMMONLY_USED, DEMOGRAPHIC_DOB_SELF, DEMOGRAPHIC_DOB_SPOUSE, DEMOGRAPHIC_ANNIVERSARY) for 4-digit MPINs.
4. **Part D**: Applies the same checks as Part C for 6-digit MPINs.
5. **Test Suite**: Includes 24 test cases to validate the functionality of all parts.

## Requirements
- **Python**: Version 3.8 or higher.
- **Dependencies**: None (uses only the Python standard library's `datetime` module).

See `requirements.txt` for details.

## Installation
1. Clone or download the project files.
2. Ensure Python 3.8+ is installed on your system.
3. No additional dependencies are required, as the program uses only the standard library.

## Usage
1. **Run the Program**:
   - Execute the script using:
     ```bash
     python app.py
     ```
   - The program runs in an interactive mode, prompting the user to select a task (1–5).

2. **Available Tasks**:
   - **Task 1 (Part A)**: Check if a 4-digit MPIN is commonly used.
   - **Task 2 (Part B)**: Check the strength of a 4-digit MPIN with optional demographic inputs (DOB, spouse's DOB, anniversary).
   - **Task 3 (Part C)**: Check the strength and reasons for a 4-digit MPIN.
   - **Task 4 (Part D)**: Check the strength and reasons for a 6-digit MPIN.
   - **Task 5**: Run all 24 test cases to validate the program.

3. **Input Format**:
   - MPIN: Enter a 4-digit or 6-digit number (depending on the task).
   - Demographics: Enter dates in `DD-MM-YYYY` format (e.g., `02-01-1998`) or press Enter to skip.

4. **Example**:
   ```plaintext
   Welcome to MPIN Checker!
   Select a task:
   1. Part A: Check if 4-digit MPIN is commonly used
   2. Part B: Check strength of 4-digit MPIN with demographics
   3. Part C: Check strength and reasons for 4-digit MPIN
   4. Part D: Check strength and reasons for 6-digit MPIN
   5. Run all test cases
   Enter task number (1-5): 3
   Enter 4-digit MPIN: 1122
   Enter DOB (DD-MM-YYYY, press Enter to skip): 22-11-1999
   Enter spouse's DOB (DD-MM-YYYY, press Enter to skip): 
   Enter anniversary (DD-MM-YYYY, press Enter to skip): 
   MPIT strength: WEAK
   Reasons: ['COMMONLY_USED', 'DEMOGRAPHIC_DOB_SELF']
   Do you want to run another task? (yes/no): no
   Thank You for using MPIN Checker!
    ```

## Test Cases
The program includes a test suite with 24 test cases covering all parts (A, B, C, and D). The test cases validate:
- **Part A**: Common patterns for 4-digit MPINs (e.g., `1111`, `1234`, `1122`) and invalid inputs.
- **Part B**: Strength of 4-digit MPINs with demographic checks (e.g., `0201` with DOB `02-01-1998`).
- **Part C**: Strength and reasons for 4-digit MPINs, including multiple reasons (e.g., `1122` being both common and demographic).
- **Part D**: Strength and reasons for 6-digit MPINs (e.g., `123456`, `020198`).

To run the test suite, select Task 5. All test cases pass, as verified by assertions in the `run_tests` function.

## File Structure
- `app.py`: Main Python script containing the `MPINChecker` class and interactive/test functions.
- `requirements.txt`: Lists dependencies (none, as only standard library is used).
- `README.md`: This file, providing project documentation.
- `Test Case Report.md` : This file, providing the detailed test cases report.

## Notes
- The program avoids hardcoded values, generating common MPINs dynamically based on digit length.
- Invalid inputs (e.g., non-numeric MPINs or incorrect date formats) are handled gracefully, returning `INVALID` or empty results as appropriate.
- The code is designed to be extensible for additional MPIN lengths or demographic checks.

## Contact
For questions or feedback, contact Kshitiz Srivastav:
- Email: kshitizsr02@gmail.com
