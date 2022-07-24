import xml.etree.ElementTree as et
import sys
from statistics import mean, median
import numpy as np


class PersonalInfo:
    """
    This class contains personal information
    """

    def __init__(self, name: str, id: str, phone_num: str, email: str):
        """
        Initializing PersonalInfo

        :param name: str, person name
        :param id: str, person id, should be unique number
        :param phone_num: str, phone number
        :param email: str, personal email
        """
        self._name = name
        self._id = id
        self._phone_num = phone_num
        self._email = email

    def __str__(self) -> str:
        """
        Returns string representation for PersonalInfo object
        :return: str
        """
        return f"Personal Info:\n name = {self._name}, \n id = {self._id}, \n phone_num = {self._phone_num}, \n email = {self._email}"


class BusinessInfo:
    """
    Contains business details for business account
    """

    def __init__(self, business_name: str, business_id: str, business_phone_num: str, business_email: str):
        """
        Initializing BusinessInfo
        :param business_name: str, business account name
        :param business_id: str , business account id
        :param business_phone_num: str, business phone number
        :param business_email: str, business email
        """
        self._business_name = business_name
        self._business_id = business_id
        self._business_phone_num = business_phone_num
        self._business_email = business_email

    def __str__(self) -> str:
        """
        Returns string representation for BusinessInfo object
        :return: str
        """
        return f"Business Info:\n business name = {self._business_name},\n business id = {self._business_id},\n " \
               f"business phone number = {self._business_phone_num},\n " \
               f"business email = {self._business_email}"


class BankAccount:
    """
    Represents Bank account
    """

    def __init__(self, person_info: PersonalInfo, balance: float = 0.0):
        """
        BankAccount initialization

        :param person_info: PersonalInfo
        :param balance: float, default value is 0.0
        """
        self._personal_info = person_info
        self._balance = balance
        self._commission = 1.1

    def set_commission(self, commission: float):
        """
        Updates commision
        :param commission: float, commission value
        :return:
        """
        self._commission = commission

    def get_balance(self) -> float:
        """
        Returns balance
        :return: float, balance value
        """
        return self._balance

    def __str__(self):
        """
        Returns string representation for BankAccount object
        :return: str
        """
        return f"BankAccount:\n {self._personal_info},\n balance = {self._balance},\n commission = {self._commission}"

    def withdraw(self, amount: float):
        """
        Withdraws provided amount from the balance
        :param amount: float, amount to withdraw
        :return:
        """
        self._balance -= amount * self._commission

    def deposit(self, amount: float):
        """
        Update existing balance with the provided amount
        :param amount: float, amount to deposit
        :return:
        """
        self._balance += (amount - amount * (self._commission - 1))


class StudentBankAccount(BankAccount):
    """
    Represents Student Bank Account
    """

    def __init__(self, person_info: PersonalInfo, college_name: str, balance: float = 0.0):
        """
        Student Bank Account initialization
        :param person_info: PersonalInfo
        :param college_name: str
        :param balance: float, default 0.0
        """
        super().__init__(person_info, balance)
        # self._commission = 1.1
        self._college_name = college_name

    def __str__(self):
        """
        Returns string representation for StudentBankAccount object
        :return: str
        """
        return f"StudentBankAccount:\n {self._personal_info},\n balance = {self._balance},\n" \
               f" commission = {self._commission},\n college name = {self._college_name}"

    def withdraw(self, amount: float):
        """
        Withdraws provided amount from the balance
        :param amount: float, amount to withdraw
        :return:
        """
        if amount < self._balance:
            self._balance -= amount * self._commission
        else:
            print(f"Impossible to withdraw {amount}, because of the required amount is greater than balance")


class BusinessBankAccount(BankAccount):
    """
    Represents Business Bank Account
    """

    def __init__(self, person_info: PersonalInfo, business_info: BusinessInfo, balance: float = 0.0):
        """
        initializing Business Bank Account
        :param person_info: PersonalInfo
        :param business_info: BusinessInfo
        :param balance: float, default 0.0
        """
        super().__init__(person_info, balance)
        self._business_info = business_info
        super().set_commission(1.5)

    def __str__(self):
        """
        Returns string representation for StudentBankAccount object
        :return: str
        """
        return f"BusinessBankAccount:\n {self._personal_info},\n balance = {self._balance},\n" \
               f" commission = {self._commission},\n business info = {self._business_info}"


class Bank:
    """
    Represents Bank object that is container that manage bank's clients and actions
    """
    student_type = "StudentBankAccount"
    bank_type = "BankAccount"
    business_type = "BusinessBankAccount"

    accounts = {}

    def __init__(self, file_name: str):
        """
        Bank initialization
        :param file_name: str, filename to initialize bank clients data
        """
        self.load_and_parse_init_data(file_name)
        self.wait_flag = True
        self.start()

    def start(self):
        """
        This method is managing available actions
        :return:
        """

        while self.wait_flag:

            action = input(f"""Please enter required action:\n
                    1 - Add new account\n
                    2 - delete account\n
                    3 - withdraw\n
                    4 - deposit\n
                    5 - calculate balance statistics\n
                    6 - present all accounts information\n
                    0 - end bank application\n
                    """).strip()

            if action == "1":
                file_name = input("Please provide xml file with account details")
                self.add_new_account(file_name.strip())

            elif action == '2':
                user_id = input("Please enter user id to delete the user or -1 to cancel the action").strip()

                if user_id != "-1":
                    self.delete_by_user_id(user_id)

            elif action == "3":
                user_id = input("Please enter user id to withdraw").strip()
                amount = input("Please enter amount to withdraw").strip()
                if amount.isnumeric():
                    self.withdraw_by_user_id(user_id, float(amount))
                else:
                    print("Amount is not valid")

            elif action == "4":
                user_id = input("Please enter user id to deposit").strip()
                amount = input("Please enter amount to deposit").strip()
                if amount.isnumeric():
                    self.deposit_by_user_id(user_id, float(amount))
                else:
                    print("Amount is not valid")

            elif action == "5":
                self.calc_balance_statistics()
            elif action == "6":
                print(self.__str__())

            elif action == "0":
                self.end()
            else:
                print(f"Selected action {action} is not valid")

    def end(self):
        """
        Finish programm
        :return:
        """
        self.wait_flag = False

    def load_and_parse_init_data(self, file_name: str):
        """
        loading initial data from provided xml file
        :param file_name: str, file name to load data
        :return:
        """
        try:
            tree = et.parse(file_name)
            root = tree.getroot()

            for account in root.findall('account'):

                person = self.parse_person_info(account)
                if person:
                    is_valid, msgs = self.validate_person_info(person)

                    if is_valid:
                        if not self.accounts.get(person._id, None):
                            acc_type = account.attrib["type"]

                            if acc_type == self.bank_type:
                                self.accounts[person._id] = BankAccount(person)

                            elif acc_type == self.student_type:
                                self.accounts[person._id] = StudentBankAccount(person, account.find('college').text)

                            elif acc_type == self.business_type:
                                business_info = self.parse_business_info(account)
                                if business_info:
                                    self.accounts[person._id] = BusinessBankAccount(person, business_info)
                        else:
                            print(f"Key for account\n {person}\n is not valid, as such key is already existing.")

                    else:
                        print(f"Data for account\n {person}\n is not valid.\n"
                              f"{msgs}")

        except Exception as ex:
            print(f'Please provide valid init xml file')
            print(f'Exception: {ex.with_traceback()}')

    def validate_person_info(self, person: PersonalInfo) -> (bool, list[str]):
        """
        Validates PersonalInfo object
        :param person: PersonalInfo
        :return: is_valid - bool flag if object contains valid data
                msgs - list of error messages
        """
        msgs = []
        is_valid = True
        if person:
            if not person._id or len(person._id) < 7 or not person._id.isnumeric():
                msgs.append("Person id length should be not less than 7 and should include digits")
                is_valid = False
            if not person._name or len(person._name) == 0:
                msgs.append("Person name is mandatory")
                is_valid = False
            if not person._email or len(person._email) == 0:
                msgs.append("Person email is mandatory")
                is_valid = False
            if not person._phone_num or len(person._phone_num) < 10:
                msgs.append("Person phone is not valid")
                is_valid = False
        else:
            is_valid = False
            msgs.append("PersonalInfo can't be empty")

        return is_valid, msgs

    def parse_person_info(self, account: et.Element) -> PersonalInfo | None:
        """
        Initializing PersonalInfo
        :param account: et.Element, parsed object
        :return: PersonalInfo in case of provided valid data
                 None in case of provided invalid data
        """
        try:
            person = account.find('personalInfo')

            name = person.find('name').text
            pers_id = person.find('id').text
            phone = person.find('phone').text
            email = person.find('email').text

            return PersonalInfo(name, pers_id, phone, email)
        except Exception:
            print(f'Some of the accounts is not valid.\n')
            return None

    def parse_business_info(self, account: et.Element) -> BusinessInfo | None:
        """"
        Initializing BusinessInfo
        :param account: et.Element, parsed object
        :return: BusinessInfo in case of provided valid data
                 None in case of provided invalid data
        """
        try:
            business = account.find('businessInfo')
            name = business.find('name').text
            id = business.find('id').text
            phone = business.find('phone').text
            email = business.find('email').text

            return BusinessInfo(name, id, phone, email)
        except Exception:
            print(f'Some of the business accounts is not valid.\n')
            return None

    def add_new_account(self, file_name):
        """
        Add new account from xml file
        :param file_name: str, file name to load
        :return:
        """
        self.load_and_parse_init_data(file_name)

    def delete_by_user_id(self, user_id: str):
        """
        Deletes user by user id
        :param user_id: str
        :return:
        """
        try:
            self.accounts.pop(user_id)

        except Exception:
            print(f"Can't delete account by id {user_id}, because such id is not found")

    def withdraw_by_user_id(self, user_id: str, amount: float):
        """
        Withdraw account by user id
        :param user_id: str
        :param amount: float, amount to withdraw
        :return:
        """

        acc = self.accounts.get(user_id)

        if acc:
            acc.withdraw(amount)
        else:
            print(f"Account with id {user_id} is not found")

    def deposit_by_user_id(self, user_id: str, amount: float):
        """
        Deposit provided amount by user id
        :param user_id: str
        :param amount: float, amount to deposit
        :return:
        """

        acc = self.accounts.get(user_id)

        if acc:
            acc.deposit(amount)
        else:
            print(f"Account with id {user_id} is not found")

    def __str__(self):
        items_str = []
        for i in self.accounts.values():
            items_str.append(i.__str__())

        data_str = '\n'.join(items_str)
        return f"Existing Accounts:\n {data_str}"

    def calc_balance_statistics(self):
        """
        Calculates balance statistics: Average, Median, 90th percentile, 10th percentile
        :return:
        """
        items = self.accounts.values()
        average = mean([item.get_balance() for item in items])
        current_median = median([item.get_balance() for item in items])

        percentile_90 = np.percentile([item.get_balance() for item in items], 90)
        percentile_10 = np.percentile([item.get_balance() for item in items], 10)

        print(f'Average = {average}\n'
              f'Median = {current_median}\n'
              f'90th percentile = {percentile_90}\n'
              f'10th percentile = {percentile_10}\n')


def main():
    """
    This method runs Bank manager class

    """
    if len(sys.argv) < 2:
        print("PLease provide initialization xml file")
        sys.exit(1)

    file_name = sys.argv[1]

    bank = Bank(file_name)


if __name__ == '__main__':
    main()
