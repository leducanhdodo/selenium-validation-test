from hypothesis import strategies


class AutoTest:
    @staticmethod
    def generate_data_for_require(record_data, input_type=None):
        if record_data['Is Email']:
            data = strategies.emails().example()
        elif record_data['Is Url']:
            regex = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
            data = strategies.from_regex(regex=regex).example()
        elif record_data['Max Length'] or record_data['Min Length']:
            min_size = record_data['Min Length'] if record_data['Min Length'] else None
            max_size = record_data['Max Length'] if record_data['Max Length'] else None
            data = strategies.text(
                min_size=min_size,
                max_size=max_size,
                alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
            ).example()
        elif record_data['Min'] or record_data['Max']:
            min_value = record_data['Min'] if record_data['Min'] else None
            max_value = record_data['Max'] if record_data['Max'] else None
            data = strategies.integers(min_value=min_value, max_value=max_value).example()
        else:
            if input_type == 'number':
                data = strategies.integers().example()
            else:
                data = strategies.text(
                    min_size=1,
                    alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
                ).example()

        return [
            {
                'data': data,
                'is_valid': True
            },
            {
                'data': '',
                'is_valid': False
            }
        ]

    @staticmethod
    def generate_data_for_email():
        return [
            {
                'data': strategies.emails().example(),
                'is_valid': True
            },
            {
                'data': strategies.text(min_size=1,
                                        max_size=100,
                                        alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
                                        ).example(),
                'is_valid': False
            },
            {
                'data': '@@gmail.com',
                'is_valid': False
            },
        ]

    @staticmethod
    def generate_data_for_url():
        regex = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
        list_urls = strategies.lists(elements=strategies.from_regex(regex=regex), min_size=4).example()
        test_cases = [
            {
                'data': strategies.text(
                    min_size=1,
                    max_size=100,
                    alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)).example(),
                'is_valid': False
            },
            {
                'data': 'http://',
                'is_valid': False
            },
            {
                'data': '://www.google.com',
                'is_valid': False
            },
            {
                'data': 'htt://www.google.com',
                'is_valid': False
            },
        ]
        for url in list_urls:
            test_cases.append({
                'data': url,
                'is_valid': True
            })
        return test_cases

    def generate_data_for_min(self, min_value, max_value=None):
        # Valid
        list_integers = strategies.lists(
            elements=strategies.integers(min_value=min_value, max_value=max_value),
            min_size=4
        ).example()

        # Invalid
        invalid_list_integers = strategies.lists(
            elements=strategies.integers(min_value=min_value-2, max_value=min_value-1),
            min_size=1
        ).example()

        test_cases = []
        for number in list_integers:
            test_cases.append({
                'data': number,
                'is_valid': True
            })

        for number in invalid_list_integers:
            test_cases.append({
                'data': number,
                'is_valid': False
            })
        return test_cases

    def generate_data_for_max(self, max_value, min_value=None):
        # Valid
        list_integers = strategies.lists(
            elements=strategies.integers(min_value=min_value, max_value=max_value),
            min_size=4
        ).example()

        # Invalid
        invalid_list_integers = strategies.lists(
            elements=strategies.integers(min_value=max_value + 1, max_value=max_value + 2),
            min_size=1
        ).example()

        test_cases = []
        for number in list_integers:
            test_cases.append({
                'data': number,
                'is_valid': True
            })

        for number in invalid_list_integers:
            test_cases.append({
                'data': number,
                'is_valid': False
            })

    def generate_data_for_text(self, min_length=None, max_length=None):
        list_texts = strategies.lists(
            elements=strategies.text(
                min_size=min_length,
                max_size=max_length,
                alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
            ),
            min_size=3
        ).example()

        test_cases = []
        for text in list_texts:
            test_cases.append({
                'data': text,
                'is_valid': True
            })
        if min_length and min_length > 1:
            invalid_list_texts = strategies.lists(
                elements=strategies.text(
                    min_size=0,
                    max_size=min_length - 1,
                    alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
                ),
                min_size=4
            ).example()

            for text in invalid_list_texts:
                test_cases.append({
                    'data': text,
                    'is_valid': False
                })

        if max_length and max_length > 0:
            invalid_list_texts = strategies.lists(
                elements=strategies.text(
                    min_size=max_length + 1,
                    alphabet=strategies.characters(min_codepoint=33, max_codepoint=126)
                ),
                min_size=4
            ).example()

            for text in invalid_list_texts:
                test_cases.append({
                    'data': text,
                    'is_valid': False
                })
        return test_cases
