from datetime import datetime

class MPINChecker:
    def __init__(self, digit_length=4):
        self.digit_length = digit_length
        self.common_pins = self.generate_common_pins()

    def generate_common_pins(self):
        common_pins = set()
        for digit in range(10):
            common_pins.add(str(digit) * self.digit_length)
        
        for start in range(1, 11 - self.digit_length):
            sequence = ""
            for index in range(start, start + self.digit_length):
                sequence += str(index)
            common_pins.add(sequence)
        for start in range(9, self.digit_length - 1, -1):
            sequence = ""
            for index in range(start, start - self.digit_length, -1):
                sequence += str(index)
            common_pins.add(sequence)
        if self.digit_length == 4:
            for digit in range(1, 9):
                common_pins.add(str(digit) * 2 + str(digit + 1) * 2)
        elif self.digit_length == 6:
            for digit in range(1, 8):
                common_pins.add(str(digit) * 2 + str(digit + 1) * 2 + str(digit + 2) * 2)
        return common_pins

    def get_date_parts(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            day = date_obj.strftime("%d")
            month = date_obj.strftime("%m")
            year = date_obj.strftime("%y")
            return day, month, year
        except ValueError:
            return None, None, None

    def generate_demographic_combinations(self, date_str):
        day, month, year = self.get_date_parts(date_str)
        if day is None:
            return set()
        parts = [day, month, year]
        combinations = set()
        digits_needed = self.digit_length // 2
        if digits_needed == 2:
            pairs = [(0, 1), (0, 2), (1, 2)]
            for i, j in pairs:
                combinations.add(parts[i] + parts[j])
                combinations.add(parts[j] + parts[i])
        elif digits_needed == 3:
            orders = [
                (0, 1, 2), (0, 2, 1), (1, 0, 2),
                (1, 2, 0), (2, 0, 1), (2, 1, 0)
            ]
            for order in orders:
                combination = parts[order[0]] + parts[order[1]] + parts[order[2]]
                combinations.add(combination)
        return combinations

    def is_common(self, pin):
        if not (pin.isdigit() and len(pin) == self.digit_length):
            return False
        return pin in self.common_pins

    def check_strength(self, pin, birth_date=None, spouse_birth_date=None, wedding_date=None):
        if not (pin.isdigit() and len(pin) == self.digit_length):
            return "INVALID", []
        reasons = []
        if pin in self.common_pins:
            reasons.append("COMMONLY_USED")
        if birth_date:
            birth_date_combinations = self.generate_demographic_combinations(birth_date)
            if pin in birth_date_combinations:
                reasons.append("DEMOGRAPHIC_DOB_SELF")
        if spouse_birth_date:
            spouse_birth_date_combinations = self.generate_demographic_combinations(spouse_birth_date)
            if pin in spouse_birth_date_combinations:
                reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
        if wedding_date:
            wedding_date_combinations = self.generate_demographic_combinations(wedding_date)
            if pin in wedding_date_combinations:
                reasons.append("DEMOGRAPHIC_ANNIVERSARY")
        strength = "WEAK" if reasons else "STRONG"
        return strength, reasons

def run_interactive():
    print("Welcome to MPIN Checker!")
    print("Select a task:")
    print("1. Part A: Check if 4-digit PIN is commonly used")
    print("2. Part B: Check strength of 4-digit PIN with demographics")
    print("3. Part C: Check strength and reasons for 4-digit PIN")
    print("4. Part D: Check strength and reasons for 6-digit PIN")
    print("5. Run all test cases")
    task = input("Enter task number (1-5): ").strip()

    if task == "1":
        pin = input("Enter 4-digit PIN: ").strip()
        checker = MPINChecker(digit_length=4)
        result = checker.is_common(pin)
        print(f"Is PIN commonly used? {result}")
    
    elif task == "2":
        pin = input("Enter 4-digit PIN: ").strip()
        birth_date = input("Enter DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        spouse_birth_date = input("Enter spouse's DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        wedding_date = input("Enter anniversary (DD-MM-YYYY, press Enter to skip): ").strip()
        birth_date = birth_date if birth_date else None
        spouse_birth_date = spouse_birth_date if spouse_birth_date else None
        wedding_date = wedding_date if wedding_date else None
        checker = MPINChecker(digit_length=4)
        strength, _ = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
        print(f"PIN strength: {strength}")
    
    elif task == "3":
        pin = input("Enter 4-digit PIN: ").strip()
        birth_date = input("Enter DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        spouse_birth_date = input("Enter spouse's DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        wedding_date = input("Enter anniversary (DD-MM-YYYY, press Enter to skip): ").strip()
        birth_date = birth_date if birth_date else None
        spouse_birth_date = spouse_birth_date if spouse_birth_date else None
        wedding_date = wedding_date if wedding_date else None
        checker = MPINChecker(digit_length=4)
        strength, reasons = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
        print(f"PIN strength: {strength}")
        print(f"Reasons: {reasons}")
    
    elif task == "4":
        pin = input("Enter 6-digit PIN: ").strip()
        birth_date = input("Enter DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        spouse_birth_date = input("Enter spouse's DOB (DD-MM-YYYY, press Enter to skip): ").strip()
        wedding_date = input("Enter anniversary (DD-MM-YYYY, press Enter to skip): ").strip()
        birth_date = birth_date if birth_date else None
        spouse_birth_date = spouse_birth_date if spouse_birth_date else None
        wedding_date = wedding_date if wedding_date else None
        checker = MPINChecker(digit_length=6)
        strength, reasons = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
        print(f"PIN strength: {strength}")
        print(f"Reasons: {reasons}")
    
    elif task == "5":
        print("Running all test cases...")
        run_tests()
    
    else:
        print("Invalid task number. Please enter 1, 2, 3, 4, or 5.")

def run_tests():
    test_cases = [
        {"part": "A", "digit_length": 4, "pin": "1111", "expected": True},
        {"part": "A", "digit_length": 4, "pin": "1234", "expected": True},
        {"part": "A", "digit_length": 4, "pin": "9876", "expected": True},
        {"part": "A", "digit_length": 4, "pin": "1122", "expected": True},
        {"part": "A", "digit_length": 4, "pin": "4839", "expected": False},
        {"part": "A", "digit_length": 4, "pin": "abc", "expected": False},
        {"part": "A", "digit_length": 4, "pin": "123", "expected": False},
        {"part": "B", "digit_length": 4, "pin": "1111", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": "WEAK"},
        {"part": "B", "digit_length": 4, "pin": "0201", "birth_date": "02-01-1998", "spouse_birth_date": None, "wedding_date": None, "expected": "WEAK"},
        {"part": "B", "digit_length": 4, "pin": "4839", "birth_date": "02-01-1998", "spouse_birth_date": "15-06-1995", "wedding_date": "10-07-2020", "expected": "STRONG"},
        {"part": "B", "digit_length": 4, "pin": "abc", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": "INVALID"},
        {"part": "C", "digit_length": 4, "pin": "1111", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 4, "pin": "0201", "birth_date": "02-01-1998", "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["DEMOGRAPHIC_DOB_SELF"])},
        {"part": "C", "digit_length": 4, "pin": "1506", "birth_date": None, "spouse_birth_date": "15-06-1995", "wedding_date": None, "expected": ("WEAK", ["DEMOGRAPHIC_DOB_SPOUSE"])},
        {"part": "C", "digit_length": 4, "pin": "1122", "birth_date": "22-11-1999", "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED", "DEMOGRAPHIC_DOB_SELF"])},
        {"part": "C", "digit_length": 4, "pin": "1007", "birth_date": None, "spouse_birth_date": None, "wedding_date": "10-07-2020", "expected": ("WEAK", ["DEMOGRAPHIC_ANNIVERSARY"])},
        {"part": "C", "digit_length": 4, "pin": "4839", "birth_date": "02-01-1998", "spouse_birth_date": "15-06-1995", "wedding_date": "10-07-2020", "expected": ("STRONG", [])},
        {"part": "C", "digit_length": 4, "pin": "0101", "birth_date": "01-01-2000", "spouse_birth_date": None, "wedding_date": "01-01-2010", "expected": ("WEAK", ["DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_ANNIVERSARY"])},
        {"part": "C", "digit_length": 4, "pin": "0000", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 4, "pin": "9999", "birth_date": "02-01-1998", "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 6, "pin": "111111", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 6, "pin": "123456", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 6, "pin": "987654", "birth_date": None, "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["COMMONLY_USED"])},
        {"part": "C", "digit_length": 6, "pin": "020198", "birth_date": "02-01-1998", "spouse_birth_date": None, "wedding_date": None, "expected": ("WEAK", ["DEMOGRAPHIC_DOB_SELF"])},
        {"part": "C", "digit_length": 6, "pin": "750293", "birth_date": "02-01-1998", "spouse_birth_date": "15-06-1995", "wedding_date": "10-07-2020", "expected": ("STRONG", [])},
    ]

    for test_index, test in enumerate(test_cases, 1):
        checker = MPINChecker(digit_length=test["digit_length"])
        pin = test["pin"]
        if test["part"] == "A":
            result = checker.is_common(pin)
            assert result == test["expected"], f"Test {test_index} failed: Expected {test['expected']}, got {result}"
        elif test["part"] == "B":
            birth_date = test.get("birth_date")
            spouse_birth_date = test.get("spouse_birth_date")
            wedding_date = test.get("wedding_date")
            strength = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)[0]
            assert strength == test["expected"], f"Test {test_index} failed: Expected {test['expected']}, got {strength}"
        elif test["part"] == "C":
            birth_date = test.get("birth_date")
            spouse_birth_date = test.get("spouse_birth_date")
            wedding_date = test.get("wedding_date")
            strength, reasons = checker.check_strength(pin, birth_date, spouse_birth_date, wedding_date)
            expected_strength, expected_reasons = test["expected"]
            assert strength == expected_strength and reasons == expected_reasons, f"Test {test_index} failed: Expected {test['expected']}, got {(strength, reasons)}"
        print(f"Test {test_index} passed")

if __name__ == "__main__":
    ch= "yes"
    while ch=="yes":
        run_interactive()
        ch= input("Do you want to run another task? (yes/no): ").strip().lower()
        if ch!= "yes":
            print("Thank you for using MPIN Checker!")
            break

