import argparse
import logging
import random
import faker
import re
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFormatRandomizer:
    """
    Randomly changes the format of data fields to one of several predefined formats,
    providing data variety while masking the original format.
    """

    def __init__(self, locale='en_US'):
        """
        Initializes the DataFormatRandomizer with a specified locale.
        """
        try:
            self.fake = faker.Faker(locale)
            self.locale = locale
        except faker.exceptions.FakerError as e:
            logging.error(f"Error initializing Faker with locale '{locale}': {e}")
            raise  # Re-raise the exception so the program halts if Faker init fails

        self.date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d %B, %Y", "%B %d, %Y", "%m-%d-%y"]
        self.phone_formats = ["+1-XXX-XXX-XXXX", "(XXX) XXX-XXXX", "XXX-XXX-XXXX", "XXX.XXX.XXXX"]
        self.address_formats = [
            "{street_address}\n{city}, {state} {postcode}",
            "{building_number} {street_name}\n{city}, {state} {postcode}",
            "{street_address}, {city}, {state} {postcode}, {country}",
            "{building_number} {street_name}, {city}, {state} {postcode}, {country}"
        ]

    def randomize_date(self):
        """
        Generates a random date with a randomly selected date format.
        """
        try:
            date_format = random.choice(self.date_formats)
            return self.fake.date(pattern=date_format)
        except Exception as e:
            logging.error(f"Error generating random date: {e}")
            return None

    def randomize_phone(self):
        """
        Generates a random phone number with a randomly selected phone format.
        """
        try:
            phone_format = random.choice(self.phone_formats)
            # Replace X's with random digits
            phone_number = ''.join([self.fake.random_digit() if char == 'X' else char for char in phone_format])
            return phone_number
        except Exception as e:
            logging.error(f"Error generating random phone number: {e}")
            return None

    def randomize_address(self):
        """
        Generates a random address with a randomly selected address format.
        """
        try:
            address_format = random.choice(self.address_formats)
            return address_format.format(
                street_address=self.fake.street_address(),
                building_number=self.fake.building_number(),
                street_name=self.fake.street_name(),
                city=self.fake.city(),
                state=self.fake.state(),
                postcode=self.fake.postcode(),
                country=self.fake.country()
            )
        except Exception as e:
            logging.error(f"Error generating random address: {e}")
            return None

    def randomize_data_type(self, data_type):
        """
        Randomizes data based on specified data type.
        """
        try:
            if data_type == "date":
                return self.randomize_date()
            elif data_type == "phone":
                return self.randomize_phone()
            elif data_type == "address":
                return self.randomize_address()
            elif data_type == "name":
                return self.fake.name()
            elif data_type == "email":
                return self.fake.email()
            elif data_type == "text":
                return self.fake.text()
            else:
                logging.warning(f"Unknown data type: {data_type}")
                return None
        except Exception as e:
            logging.error(f"Error randomizing data type '{data_type}': {e}")
            return None


def setup_argparse():
    """
    Sets up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(description="Randomly changes the format of data fields to one of several predefined formats.")
    parser.add_argument("-t", "--type", dest="data_type", required=True,
                        help="The type of data to randomize (date, phone, address, name, email, text).")
    parser.add_argument("-n", "--number", dest="number_of_samples", type=int, default=1,
                        help="The number of samples to generate. Defaults to 1.")
    parser.add_argument("-l", "--locale", dest="locale", type=str, default="en_US",
                        help="The Faker locale to use. Defaults to en_US.")

    return parser

def main():
    """
    Main function to parse arguments and execute the data format randomization.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Input validation
    if args.number_of_samples <= 0:
        logging.error("Number of samples must be greater than zero.")
        sys.exit(1)

    try:
        randomizer = DataFormatRandomizer(args.locale)

        for _ in range(args.number_of_samples):
            randomized_data = randomizer.randomize_data_type(args.data_type)
            if randomized_data is not None:
                print(randomized_data)

    except faker.exceptions.FakerError as e:
        logging.error(f"Faker Error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Usage Examples:
    # 1. Generate a random date: python main.py -t date
    # 2. Generate 5 random phone numbers: python main.py -t phone -n 5
    # 3. Generate a random address with French locale: python main.py -t address -l fr_FR
    # 4. Generate a random name: python main.py -t name
    # 5. Generate a random email: python main.py -t email
    # 6. Generate a random text: python main.py -t text
    main()