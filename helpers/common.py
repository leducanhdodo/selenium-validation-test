from selenium.webdriver.common.keys import Keys


def parse_validation_type(text):
    return text.split('|')


def clear_element(element):
    input_value = element.get_attribute('value')
    # element.clear()
    if len(input_value) > 0:
        i = 0
        while i < len(input_value):
            element.send_keys(Keys.BACK_SPACE)
            i = i + 1
    element.send_keys(' ')
    element.send_keys(Keys.BACK_SPACE)
