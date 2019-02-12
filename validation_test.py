import unittest
import gspread
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import settings
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import common
from helpers.auto_test import AutoTest


class ValidationTest(unittest.TestCase):
    def setUp(self):
        # Create a new Google Chrome session with headless mode
        driver_options = Options()
        driver_options.headless = settings.BROWSER_HEADLESS

        self.driver = webdriver.Chrome(options=driver_options)
        self.driver.set_window_size(1366, 768)

        # Visit website to test
        self.driver.get(settings.WEBSITE_URL)

    def test_payment_options(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLE_DRIVE_API_KEY_FILE, scope)

        gc = gspread.authorize(credentials)

        source_file_urls = settings.SOURCE_FILES

        for source_file_url in source_file_urls:
            wks = gc.open_by_url(source_file_url)

            worksheet_list = wks.worksheets()
            for sheet in worksheet_list:
                # Get all sheet records
                records = sheet.get_all_records()

                for record in records:
                    if 'Step Name' not in record:
                        continue
                    # Start subTest by Step name
                    with self.subTest('{} - {}'.format(sheet.title, record['Step Name'])):
                        if record['Action'] == 'set_value':
                            element = WebDriverWait(self.driver, 20).until(
                                expected_conditions.presence_of_element_located(
                                    (By.CSS_SELECTOR, record['Selector'])
                                )
                            )
                            element.send_keys(record['Value'])
                        elif record['Action'] == 'visit':
                            self.driver.get(record['Value'])
                        elif record['Action'] == 'wait':
                            time.sleep(record['Value'])
                        elif record['Action'] == 'click':
                            element = WebDriverWait(self.driver, 10).until(
                                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, record['Selector']))
                            )
                            element.click()
                        elif record['Action'] == 'check_presence':
                            self.assertTrue(self.check_exists_by_css_selector(record['Selector']))
                        elif record['Action'] == 'autotest':
                            self.handle_auto_test_field(record)

    def handle_auto_test_field(self, record_data):
        element = WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, record_data['Selector'])
            )
        )

        if record_data['Required']:
            test_data = AutoTest.generate_data_for_require(record_data=record_data,
                                                           input_type=element.get_attribute('type'))
            self.handle_test_input(record_data['Required'], record_data, test_data)

        if record_data['Is Email']:
            test_data = AutoTest.generate_data_for_email()
            self.handle_test_input(record_data['Is Email'], record_data, test_data)
        if record_data['Is Url']:
            test_data = AutoTest.generate_data_for_url()
            self.handle_test_input(record_data['Is Url'], record_data, test_data)
        if record_data['Max Length']:
            max_validation = common.parse_validation_type(record_data['Max Length'])
            if record_data['Min Length']:
                min_validation = common.parse_validation_type(record_data['Min Length'])
                min_value = int(min_validation[0])
            else:
                min_value = None
            test_data = AutoTest.generate_data_for_max_length(int(max_validation[0]), min_value)
            self.handle_test_input(record_data['Max Length'], record_data, test_data)
        if record_data['Min Length']:
            min_validation = common.parse_validation_type(record_data['Min Length'])
            if record_data['Max Length']:
                max_validation = common.parse_validation_type(record_data['Max Length'])
                max_value = int(max_validation[0])
            else:
                max_value = None
            test_data = AutoTest.generate_data_for_min_length(int(min_validation[0]), max_value)
            self.handle_test_input(record_data['Min Length'], record_data, test_data)
        if record_data['Min']:
            min_validation = common.parse_validation_type(record_data['Min'])
            if record_data['Max']:
                max_validation = common.parse_validation_type(record_data['Max'])
                max_value = int(max_validation[0])
            else:
                max_value = None
            test_min_data = AutoTest.generate_data_for_min(int(min_validation[0]), max_value)
            self.handle_test_input(record_data['Min'], record_data, test_min_data)
        if record_data['Max']:
            if record_data['Min']:
                min_validation = common.parse_validation_type(record_data['Min'])
                min_value = int(min_validation[0])
            else:
                min_value = None
            max_validation = common.parse_validation_type(record_data['Max'])
            test_max_data = AutoTest.generate_data_for_max(int(max_validation[0]), min_value)
            self.handle_test_input(record_data['Max'], record_data, test_max_data)

    def handle_test_input(self, validation_data, record_data, generated_data):
        validation = common.parse_validation_type(validation_data)

        for data in generated_data:
            element = WebDriverWait(self.driver, 20).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, record_data['Selector'])
                )
            )
            if not data['data']:
                element.clear()
                element.send_keys(' ')
                element.send_keys(Keys.BACK_SPACE)
            else:
                element.send_keys(data['data'])
            time.sleep(0.7)
            element.submit()
            time.sleep(1)

            if data['is_valid']:
                self.assertFalse(self.check_presence_by_type(
                    validation[1],
                    validation[2]),
                    'See presence by type: {}, value: {}'.format(validation[1], validation[2])
                )
            else:
                self.assertTrue(self.check_presence_by_type(
                    validation[1],
                    validation[2]),
                    'Cannot see presence by type: {}, value: {}'.format(validation[1], validation[2])
                )

            # self.driver.refresh()
            element.clear()
            element.send_keys(' ')
            element.send_keys(Keys.BACK_SPACE)

    def check_exists_by_css_selector(self, selector):
        try:
            self.driver.find_element_by_css_selector(selector)
        except NoSuchElementException:
            return False
        return True

    def check_presence_by_type(self, check_type, check_data=None):
        if check_type == 'Text':
            print(check_data)
            return check_data in self.driver.page_source
        return False

    def tearDown(self):
        # Close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
