from faker import Faker
from jinja2 import Environment, nodes
from jinja2.ext import Extension


class FakerExtension(Extension):
    tags = set(["faker"])

    def __init__(self, environment):
        super().__init__(environment)
        self.faker = Faker()

        # Register a macro for each method in the Faker instance
        # print("# List of faker methods:")
        for method in dir(self.faker):
            try:
                if callable(getattr(self.faker, method)) and not method.startswith("_"):
                    self.environment.globals["faker_" + method] = getattr(
                        self.faker, method
                    )
                    # print("# faker_" + method)
            except TypeError as e:
                continue

    def parse(self, parser):
        pass  # We don't need to implement this method as we won't be using the {% faker %} tag anymore


def main():
    env = Environment(extensions=[FakerExtension])

    # Define some templates to test
    templates = [
        "{{ faker_name() }}",
        "{{ faker_email() }}",
        "{{ faker_country() }}",
        "{{ faker_city() }}",
        "{{ faker_address() }}",
        "{{ faker_text() }}",
        "{{ faker_job() }}",
        "{{ faker_company() }}",
        "{{ faker_phone_number() }}",
        "{{ faker_bs() }}",
        "{{ faker_pydict() }}",
    ]

    # Render and print each template
    for template in templates:
        result = env.from_string(template).render()
        print(result)


if __name__ == "__main__":
    main()

# faker_aba
# faker_add_provider
# faker_address
# faker_administrative_unit
# faker_am_pm
# faker_android_platform_token
# faker_ascii_company_email
# faker_ascii_email
# faker_ascii_free_email
# faker_ascii_safe_email
# faker_bank_country
# faker_basic_phone_number
# faker_bban
# faker_binary
# faker_boolean
# faker_bothify
# faker_bs
# faker_building_number
# faker_catch_phrase
# faker_century
# faker_chrome
# faker_city
# faker_city_prefix
# faker_city_suffix
# faker_color
# faker_color_name
# faker_company
# faker_company_email
# faker_company_suffix
# faker_coordinate
# faker_country
# faker_country_calling_code
# faker_country_code
# faker_credit_card_expire
# faker_credit_card_full
# faker_credit_card_number
# faker_credit_card_provider
# faker_credit_card_security_code
# faker_cryptocurrency
# faker_cryptocurrency_code
# faker_cryptocurrency_name
# faker_csv
# faker_currency
# faker_currency_code
# faker_currency_name
# faker_currency_symbol
# faker_current_country
# faker_current_country_code
# faker_date
# faker_date_between
# faker_date_between_dates
# faker_date_object
# faker_date_of_birth
# faker_date_this_century
# faker_date_this_decade
# faker_date_this_month
# faker_date_this_year
# faker_date_time
# faker_date_time_ad
# faker_date_time_between
# faker_date_time_between_dates
# faker_date_time_this_century
# faker_date_time_this_decade
# faker_date_time_this_month
# faker_date_time_this_year
# faker_day_of_month
# faker_day_of_week
# faker_del_arguments
# faker_dga
# faker_domain_name
# faker_domain_word
# faker_dsv
# faker_ean
# faker_ean13
# faker_ean8
# faker_ein
# faker_email
# faker_emoji
# faker_enum
# faker_file_extension
# faker_file_name
# faker_file_path
# faker_firefox
# faker_first_name
# faker_first_name_female
# faker_first_name_male
# faker_first_name_nonbinary
# faker_fixed_width
# faker_format
# faker_free_email
# faker_free_email_domain
# faker_future_date
# faker_future_datetime
# faker_get_arguments
# faker_get_formatter
# faker_get_providers
# faker_hex_color
# faker_hexify
# faker_hostname
# faker_http_method
# faker_iana_id
# faker_iban
# faker_image
# faker_image_url
# faker_internet_explorer
# faker_invalid_ssn
# faker_ios_platform_token
# faker_ipv4
# faker_ipv4_network_class
# faker_ipv4_private
# faker_ipv4_public
# faker_ipv6
# faker_isbn10
# faker_isbn13
# faker_iso8601
# faker_items
# faker_itin
# faker_job
# faker_json
# faker_json_bytes
# faker_language_code
# faker_language_name
# faker_last_name
# faker_last_name_female
# faker_last_name_male
# faker_last_name_nonbinary
# faker_latitude
# faker_latlng
# faker_lexify
# faker_license_plate
# faker_linux_platform_token
# faker_linux_processor
# faker_local_latlng
# faker_locale
# faker_localized_ean
# faker_localized_ean13
# faker_localized_ean8
# faker_location_on_land
# faker_longitude
# faker_mac_address
# faker_mac_platform_token
# faker_mac_processor
# faker_md5
# faker_military_apo
# faker_military_dpo
# faker_military_ship
# faker_military_state
# faker_mime_type
# faker_month
# faker_month_name
# faker_msisdn
# faker_name
# faker_name_female
# faker_name_male
# faker_name_nonbinary
# faker_nic_handle
# faker_nic_handles
# faker_null_boolean
# faker_numerify
# faker_opera
# faker_paragraph
# faker_paragraphs
# faker_parse
# faker_passport_dates
# faker_passport_dob
# faker_passport_full
# faker_passport_gender
# faker_passport_number
# faker_passport_owner
# faker_password
# faker_past_date
# faker_past_datetime
# faker_phone_number
# faker_port_number
# faker_postalcode
# faker_postalcode_in_state
# faker_postalcode_plus4
# faker_postcode
# faker_postcode_in_state
# faker_prefix
# faker_prefix_female
# faker_prefix_male
# faker_prefix_nonbinary
# faker_pricetag
# faker_profile
# faker_provider
# faker_psv
# faker_pybool
# faker_pydecimal
# faker_pydict
# faker_pyfloat
# faker_pyint
# faker_pyiterable
# faker_pylist
# faker_pyobject
# faker_pyset
# faker_pystr
# faker_pystr_format
# faker_pystruct
# faker_pytimezone
# faker_pytuple
# faker_random_choices
# faker_random_digit
# faker_random_digit_above_two
# faker_random_digit_not_null
# faker_random_digit_not_null_or_empty
# faker_random_digit_or_empty
# faker_random_element
# faker_random_elements
# faker_random_int
# faker_random_letter
# faker_random_letters
# faker_random_lowercase_letter
# faker_random_number
# faker_random_sample
# faker_random_uppercase_letter
# faker_randomize_nb_elements
# faker_rgb_color
# faker_rgb_css_color
# faker_ripe_id
# faker_safari
# faker_safe_color_name
# faker_safe_domain_name
# faker_safe_email
# faker_safe_hex_color
# faker_sbn9
# faker_secondary_address
# faker_seed_instance
# faker_seed_locale
# faker_sentence
# faker_sentences
# faker_set_arguments
# faker_set_formatter
# faker_sha1
# faker_sha256
# faker_simple_profile
# faker_slug
# faker_ssn
# faker_state
# faker_state_abbr
# faker_street_address
# faker_street_name
# faker_street_suffix
# faker_suffix
# faker_suffix_female
# faker_suffix_male
# faker_suffix_nonbinary
# faker_swift
# faker_swift11
# faker_swift8
# faker_tar
# faker_text
# faker_texts
# faker_time
# faker_time_delta
# faker_time_object
# faker_time_series
# faker_timezone
# faker_tld
# faker_tsv
# faker_unix_device
# faker_unix_partition
# faker_unix_time
# faker_upc_a
# faker_upc_e
# faker_uri
# faker_uri_extension
# faker_uri_page
# faker_uri_path
# faker_url
# faker_user_agent
# faker_user_name
# faker_uuid4
# faker_vin
# faker_windows_platform_token
# faker_word
# faker_words
# faker_xml
# faker_year
# faker_zip
# faker_zipcode
# faker_zipcode_in_state
# faker_zipcode_plus4
# List of faker methods:
# faker_aba
# faker_add_provider
# faker_address
# faker_administrative_unit
# faker_am_pm
# faker_android_platform_token
# faker_ascii_company_email
# faker_ascii_email
# faker_ascii_free_email
# faker_ascii_safe_email
# faker_bank_country
# faker_basic_phone_number
# faker_bban
# faker_binary
# faker_boolean
# faker_bothify
# faker_bs
# faker_building_number
# faker_catch_phrase
# faker_century
# faker_chrome
# faker_city
# faker_city_prefix
# faker_city_suffix
# faker_color
# faker_color_name
# faker_company
# faker_company_email
# faker_company_suffix
# faker_coordinate
# faker_country
# faker_country_calling_code
# faker_country_code
# faker_credit_card_expire
# faker_credit_card_full
# faker_credit_card_number
# faker_credit_card_provider
# faker_credit_card_security_code
# faker_cryptocurrency
# faker_cryptocurrency_code
# faker_cryptocurrency_name
# faker_csv
# faker_currency
# faker_currency_code
# faker_currency_name
# faker_currency_symbol
# faker_current_country
# faker_current_country_code
# faker_date
# faker_date_between
# faker_date_between_dates
# faker_date_object
# faker_date_of_birth
# faker_date_this_century
# faker_date_this_decade
# faker_date_this_month
# faker_date_this_year
# faker_date_time
# faker_date_time_ad
# faker_date_time_between
# faker_date_time_between_dates
# faker_date_time_this_century
# faker_date_time_this_decade
# faker_date_time_this_month
# faker_date_time_this_year
# faker_day_of_month
# faker_day_of_week
# faker_del_arguments
# faker_dga
# faker_domain_name
# faker_domain_word
# faker_dsv
# faker_ean
# faker_ean13
# faker_ean8
# faker_ein
# faker_email
# faker_emoji
# faker_enum
# faker_file_extension
# faker_file_name
# faker_file_path
# faker_firefox
# faker_first_name
# faker_first_name_female
# faker_first_name_male
# faker_first_name_nonbinary
# faker_fixed_width
# faker_format
# faker_free_email
# faker_free_email_domain
# faker_future_date
# faker_future_datetime
# faker_get_arguments
# faker_get_formatter
# faker_get_providers
# faker_hex_color
# faker_hexify
# faker_hostname
# faker_http_method
# faker_iana_id
# faker_iban
# faker_image
# faker_image_url
# faker_internet_explorer
# faker_invalid_ssn
# faker_ios_platform_token
# faker_ipv4
# faker_ipv4_network_class
# faker_ipv4_private
# faker_ipv4_public
# faker_ipv6
# faker_isbn10
# faker_isbn13
# faker_iso8601
# faker_items
# faker_itin
# faker_job
# faker_json
# faker_json_bytes
# faker_language_code
# faker_language_name
# faker_last_name
# faker_last_name_female
# faker_last_name_male
# faker_last_name_nonbinary
# faker_latitude
# faker_latlng
# faker_lexify
# faker_license_plate
# faker_linux_platform_token
# faker_linux_processor
# faker_local_latlng
# faker_locale
# faker_localized_ean
# faker_localized_ean13
# faker_localized_ean8
# faker_location_on_land
# faker_longitude
# faker_mac_address
# faker_mac_platform_token
# faker_mac_processor
# faker_md5
# faker_military_apo
# faker_military_dpo
# faker_military_ship
# faker_military_state
# faker_mime_type
# faker_month
# faker_month_name
# faker_msisdn
# faker_name
# faker_name_female
# faker_name_male
# faker_name_nonbinary
# faker_nic_handle
# faker_nic_handles
# faker_null_boolean
# faker_numerify
# faker_opera
# faker_paragraph
# faker_paragraphs
# faker_parse
# faker_passport_dates
# faker_passport_dob
# faker_passport_full
# faker_passport_gender
# faker_passport_number
# faker_passport_owner
# faker_password
# faker_past_date
# faker_past_datetime
# faker_phone_number
# faker_port_number
# faker_postalcode
# faker_postalcode_in_state
# faker_postalcode_plus4
# faker_postcode
# faker_postcode_in_state
# faker_prefix
# faker_prefix_female
# faker_prefix_male
# faker_prefix_nonbinary
# faker_pricetag
# faker_profile
# faker_provider
# faker_psv
# faker_pybool
# faker_pydecimal
# faker_pydict
# faker_pyfloat
# faker_pyint
# faker_pyiterable
# faker_pylist
# faker_pyobject
# faker_pyset
# faker_pystr
# faker_pystr_format
# faker_pystruct
# faker_pytimezone
# faker_pytuple
# faker_random_choices
# faker_random_digit
# faker_random_digit_above_two
# faker_random_digit_not_null
# faker_random_digit_not_null_or_empty
# faker_random_digit_or_empty
# faker_random_element
# faker_random_elements
# faker_random_int
# faker_random_letter
# faker_random_letters
# faker_random_lowercase_letter
# faker_random_number
# faker_random_sample
# faker_random_uppercase_letter
# faker_randomize_nb_elements
# faker_rgb_color
# faker_rgb_css_color
# faker_ripe_id
# faker_safari
# faker_safe_color_name
# faker_safe_domain_name
# faker_safe_email
# faker_safe_hex_color
# faker_sbn9
# faker_secondary_address
# faker_seed_instance
# faker_seed_locale
# faker_sentence
# faker_sentences
# faker_set_arguments
# faker_set_formatter
# faker_sha1
# faker_sha256
# faker_simple_profile
# faker_slug
# faker_ssn
# faker_state
# faker_state_abbr
# faker_street_address
# faker_street_name
# faker_street_suffix
# faker_suffix
# faker_suffix_female
# faker_suffix_male
# faker_suffix_nonbinary
# faker_swift
# faker_swift11
# faker_swift8
# faker_tar
# faker_text
# faker_texts
# faker_time
# faker_time_delta
# faker_time_object
# faker_time_series
# faker_timezone
# faker_tld
# faker_tsv
# faker_unix_device
# faker_unix_partition
# faker_unix_time
# faker_upc_a
# faker_upc_e
# faker_uri
# faker_uri_extension
# faker_uri_page
# faker_uri_path
# faker_url
# faker_user_agent
# faker_user_name
# faker_uuid4
# faker_vin
# faker_windows_platform_token
# faker_word
# faker_words
# faker_xml
# faker_year
# faker_zip
# faker_zipcode
# faker_zipcode_in_state
# faker_zipcode_plus4
# List of faker methods:
# faker_aba
# faker_add_provider
# faker_address
# faker_administrative_unit
# faker_am_pm
# faker_android_platform_token
# faker_ascii_company_email
# faker_ascii_email
# faker_ascii_free_email
# faker_ascii_safe_email
# faker_bank_country
# faker_basic_phone_number
# faker_bban
# faker_binary
# faker_boolean
# faker_bothify
# faker_bs
# faker_building_number
# faker_catch_phrase
# faker_century
# faker_chrome
# faker_city
# faker_city_prefix
# faker_city_suffix
# faker_color
# faker_color_name
# faker_company
# faker_company_email
# faker_company_suffix
# faker_coordinate
# faker_country
# faker_country_calling_code
# faker_country_code
# faker_credit_card_expire
# faker_credit_card_full
# faker_credit_card_number
# faker_credit_card_provider
# faker_credit_card_security_code
# faker_cryptocurrency
# faker_cryptocurrency_code
# faker_cryptocurrency_name
# faker_csv
# faker_currency
# faker_currency_code
# faker_currency_name
# faker_currency_symbol
# faker_current_country
# faker_current_country_code
# faker_date
# faker_date_between
# faker_date_between_dates
# faker_date_object
# faker_date_of_birth
# faker_date_this_century
# faker_date_this_decade
# faker_date_this_month
# faker_date_this_year
# faker_date_time
# faker_date_time_ad
# faker_date_time_between
# faker_date_time_between_dates
# faker_date_time_this_century
# faker_date_time_this_decade
# faker_date_time_this_month
# faker_date_time_this_year
# faker_day_of_month
# faker_day_of_week
# faker_del_arguments
# faker_dga
# faker_domain_name
# faker_domain_word
# faker_dsv
# faker_ean
# faker_ean13
# faker_ean8
# faker_ein
# faker_email
# faker_emoji
# faker_enum
# faker_file_extension
# faker_file_name
# faker_file_path
# faker_firefox
# faker_first_name
# faker_first_name_female
# faker_first_name_male
# faker_first_name_nonbinary
# faker_fixed_width
# faker_format
# faker_free_email
# faker_free_email_domain
# faker_future_date
# faker_future_datetime
# faker_get_arguments
# faker_get_formatter
# faker_get_providers
# faker_hex_color
# faker_hexify
# faker_hostname
# faker_http_method
# faker_iana_id
# faker_iban
# faker_image
# faker_image_url
# faker_internet_explorer
# faker_invalid_ssn
# faker_ios_platform_token
# faker_ipv4
# faker_ipv4_network_class
# faker_ipv4_private
# faker_ipv4_public
# faker_ipv6
# faker_isbn10
# faker_isbn13
# faker_iso8601
# faker_items
# faker_itin
# faker_job
# faker_json
# faker_json_bytes
# faker_language_code
# faker_language_name
# faker_last_name
# faker_last_name_female
# faker_last_name_male
# faker_last_name_nonbinary
# faker_latitude
# faker_latlng
# faker_lexify
# faker_license_plate
# faker_linux_platform_token
# faker_linux_processor
# faker_local_latlng
# faker_locale
# faker_localized_ean
# faker_localized_ean13
# faker_localized_ean8
# faker_location_on_land
# faker_longitude
# faker_mac_address
# faker_mac_platform_token
# faker_mac_processor
# faker_md5
# faker_military_apo
# faker_military_dpo
# faker_military_ship
# faker_military_state
# faker_mime_type
# faker_month
# faker_month_name
# faker_msisdn
# faker_name
# faker_name_female
# faker_name_male
# faker_name_nonbinary
# faker_nic_handle
# faker_nic_handles
# faker_null_boolean
# faker_numerify
# faker_opera
# faker_paragraph
# faker_paragraphs
# faker_parse
# faker_passport_dates
# faker_passport_dob
# faker_passport_full
# faker_passport_gender
# faker_passport_number
# faker_passport_owner
# faker_password
# faker_past_date
# faker_past_datetime
# faker_phone_number
# faker_port_number
# faker_postalcode
# faker_postalcode_in_state
# faker_postalcode_plus4
# faker_postcode
# faker_postcode_in_state
# faker_prefix
# faker_prefix_female
# faker_prefix_male
# faker_prefix_nonbinary
# faker_pricetag
# faker_profile
# faker_provider
# faker_psv
# faker_pybool
# faker_pydecimal
# faker_pydict
# faker_pyfloat
# faker_pyint
# faker_pyiterable
# faker_pylist
# faker_pyobject
# faker_pyset
# faker_pystr
# faker_pystr_format
# faker_pystruct
# faker_pytimezone
# faker_pytuple
# faker_random_choices
# faker_random_digit
# faker_random_digit_above_two
# faker_random_digit_not_null
# faker_random_digit_not_null_or_empty
# faker_random_digit_or_empty
# faker_random_element
# faker_random_elements
# faker_random_int
# faker_random_letter
# faker_random_letters
# faker_random_lowercase_letter
# faker_random_number
# faker_random_sample
# faker_random_uppercase_letter
# faker_randomize_nb_elements
# faker_rgb_color
# faker_rgb_css_color
# faker_ripe_id
# faker_safari
# faker_safe_color_name
# faker_safe_domain_name
# faker_safe_email
# faker_safe_hex_color
# faker_sbn9
# faker_secondary_address
# faker_seed_instance
# faker_seed_locale
# faker_sentence
# faker_sentences
# faker_set_arguments
# faker_set_formatter
# faker_sha1
# faker_sha256
# faker_simple_profile
# faker_slug
# faker_ssn
# faker_state
# faker_state_abbr
# faker_street_address
# faker_street_name
# faker_street_suffix
# faker_suffix
# faker_suffix_female
# faker_suffix_male
# faker_suffix_nonbinary
# faker_swift
# faker_swift11
# faker_swift8
# faker_tar
# faker_text
# faker_texts
# faker_time
# faker_time_delta
# faker_time_object
# faker_time_series
# faker_timezone
# faker_tld
# faker_tsv
# faker_unix_device
# faker_unix_partition
# faker_unix_time
# faker_upc_a
# faker_upc_e
# faker_uri
# faker_uri_extension
# faker_uri_page
# faker_uri_path
# faker_url
# faker_user_agent
# faker_user_name
# faker_uuid4
# faker_vin
# faker_windows_platform_token
# faker_word
# faker_words
# faker_xml
# faker_year
# faker_zip
# faker_zipcode
# faker_zipcode_in_state
# faker_zipcode_plus4
# List of faker methods:
# faker_aba
# faker_add_provider
# faker_address
# faker_administrative_unit
# faker_am_pm
# faker_android_platform_token
# faker_ascii_company_email
# faker_ascii_email
# faker_ascii_free_email
# faker_ascii_safe_email
# faker_bank_country
# faker_basic_phone_number
# faker_bban
# faker_binary
# faker_boolean
# faker_bothify
# faker_bs
# faker_building_number
# faker_catch_phrase
# faker_century
# faker_chrome
# faker_city
# faker_city_prefix
# faker_city_suffix
# faker_color
# faker_color_name
# faker_company
# faker_company_email
# faker_company_suffix
# faker_coordinate
# faker_country
# faker_country_calling_code
# faker_country_code
# faker_credit_card_expire
# faker_credit_card_full
# faker_credit_card_number
# faker_credit_card_provider
# faker_credit_card_security_code
# faker_cryptocurrency
# faker_cryptocurrency_code
# faker_cryptocurrency_name
# faker_csv
# faker_currency
# faker_currency_code
# faker_currency_name
# faker_currency_symbol
# faker_current_country
# faker_current_country_code
# faker_date
# faker_date_between
# faker_date_between_dates
# faker_date_object
# faker_date_of_birth
# faker_date_this_century
# faker_date_this_decade
# faker_date_this_month
# faker_date_this_year
# faker_date_time
# faker_date_time_ad
# faker_date_time_between
# faker_date_time_between_dates
# faker_date_time_this_century
# faker_date_time_this_decade
# faker_date_time_this_month
# faker_date_time_this_year
# faker_day_of_month
# faker_day_of_week
# faker_del_arguments
# faker_dga
# faker_domain_name
# faker_domain_word
# faker_dsv
# faker_ean
# faker_ean13
# faker_ean8
# faker_ein
# faker_email
# faker_emoji
# faker_enum
# faker_file_extension
# faker_file_name
# faker_file_path
# faker_firefox
# faker_first_name
# faker_first_name_female
# faker_first_name_male
# faker_first_name_nonbinary
# faker_fixed_width
# faker_format
# faker_free_email
# faker_free_email_domain
# faker_future_date
# faker_future_datetime
# faker_get_arguments
# faker_get_formatter
# faker_get_providers
# faker_hex_color
# faker_hexify
# faker_hostname
# faker_http_method
# faker_iana_id
# faker_iban
# faker_image
# faker_image_url
# faker_internet_explorer
# faker_invalid_ssn
# faker_ios_platform_token
# faker_ipv4
# faker_ipv4_network_class
# faker_ipv4_private
# faker_ipv4_public
# faker_ipv6
# faker_isbn10
# faker_isbn13
# faker_iso8601
# faker_items
# faker_itin
# faker_job
# faker_json
# faker_json_bytes
# faker_language_code
# faker_language_name
# faker_last_name
# faker_last_name_female
# faker_last_name_male
# faker_last_name_nonbinary
# faker_latitude
# faker_latlng
# faker_lexify
# faker_license_plate
# faker_linux_platform_token
# faker_linux_processor
# faker_local_latlng
# faker_locale
# faker_localized_ean
# faker_localized_ean13
# faker_localized_ean8
# faker_location_on_land
# faker_longitude
# faker_mac_address
# faker_mac_platform_token
# faker_mac_processor
# faker_md5
# faker_military_apo
# faker_military_dpo
# faker_military_ship
# faker_military_state
# faker_mime_type
# faker_month
# faker_month_name
# faker_msisdn
# faker_name
# faker_name_female
# faker_name_male
# faker_name_nonbinary
# faker_nic_handle
# faker_nic_handles
# faker_null_boolean
# faker_numerify
# faker_opera
# faker_paragraph
# faker_paragraphs
# faker_parse
# faker_passport_dates
# faker_passport_dob
# faker_passport_full
# faker_passport_gender
# faker_passport_number
# faker_passport_owner
# faker_password
# faker_past_date
# faker_past_datetime
# faker_phone_number
# faker_port_number
# faker_postalcode
# faker_postalcode_in_state
# faker_postalcode_plus4
# faker_postcode
# faker_postcode_in_state
# faker_prefix
# faker_prefix_female
# faker_prefix_male
# faker_prefix_nonbinary
# faker_pricetag
# faker_profile
# faker_provider
# faker_psv
# faker_pybool
# faker_pydecimal
# faker_pydict
# faker_pyfloat
# faker_pyint
# faker_pyiterable
# faker_pylist
# faker_pyobject
# faker_pyset
# faker_pystr
# faker_pystr_format
# faker_pystruct
# faker_pytimezone
# faker_pytuple
# faker_random_choices
# faker_random_digit
# faker_random_digit_above_two
# faker_random_digit_not_null
# faker_random_digit_not_null_or_empty
# faker_random_digit_or_empty
# faker_random_element
# faker_random_elements
# faker_random_int
# faker_random_letter
# faker_random_letters
# faker_random_lowercase_letter
# faker_random_number
# faker_random_sample
# faker_random_uppercase_letter
# faker_randomize_nb_elements
# faker_rgb_color
# faker_rgb_css_color
# faker_ripe_id
# faker_safari
# faker_safe_color_name
# faker_safe_domain_name
# faker_safe_email
# faker_safe_hex_color
# faker_sbn9
# faker_secondary_address
# faker_seed_instance
# faker_seed_locale
# faker_sentence
# faker_sentences
# faker_set_arguments
# faker_set_formatter
# faker_sha1
# faker_sha256
# faker_simple_profile
# faker_slug
# faker_ssn
# faker_state
# faker_state_abbr
# faker_street_address
# faker_street_name
# faker_street_suffix
# faker_suffix
# faker_suffix_female
# faker_suffix_male
# faker_suffix_nonbinary
# faker_swift
# faker_swift11
# faker_swift8
# faker_tar
# faker_text
# faker_texts
# faker_time
# faker_time_delta
# faker_time_object
# faker_time_series
# faker_timezone
# faker_tld
# faker_tsv
# faker_unix_device
# faker_unix_partition
# faker_unix_time
# faker_upc_a
# faker_upc_e
# faker_uri
# faker_uri_extension
# faker_uri_page
# faker_uri_path
# faker_url
# faker_user_agent
# faker_user_name
# faker_uuid4
# faker_vin
# faker_windows_platform_token
# faker_word
# faker_words
# faker_xml
# faker_year
# faker_zip
# faker_zipcode
# faker_zipcode_in_state
# faker_zipcode_plus4
