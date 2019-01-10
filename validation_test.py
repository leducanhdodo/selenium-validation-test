import unittest
import gspread
import time
from selenium.common.exceptions import NoSuchElementException

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
            if record_data['Required']:
                test_data = AutoTest.generate_data_for_require(record_data=record_data,
                                                               input_type=element.get_attribute('type'))
                validation = common.parse_validation_type(record_data['Required'])

                for data in test_data:
                    element = WebDriverWait(self.driver, 20).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, record_data['Selector'])
                        )
                    )
                    element.send_keys(data['data'])
                    time.sleep(0.7)
                    element.submit()

                    if data['is_valid']:
                        self.assertFalse(self.check_presence_by_type(validation[1], validation[2]))
                    else:
                        self.assertTrue(self.check_presence_by_type(validation[1], validation[2]))

                    self.driver.refresh()

        elif record_data['Is Email']:
            pass
        elif record_data['Is Url']:
            pass
        elif record_data['Max Length'] or record_data['Min Length']:
            pass
        elif record_data['Min'] or record_data['Max']:
            pass

    def check_exists_by_css_selector(self, selector):
        try:
            self.driver.find_element_by_css_selector(selector)
        except NoSuchElementException:
            return False
        return True

    def check_presence_by_type(self, check_type, check_data=None):
        if check_type == 'Text':
            return check_data in self.driver.page_source
        return False

    def tearDown(self):
        # Close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
