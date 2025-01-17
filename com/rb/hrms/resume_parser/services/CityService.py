import requests
import json
from com.rb.hrms.resume_parser.constants.AiApiConstant import *
from com.rb.hrms.resume_parser.constants.HRMSApiConstants import *
import logging
from com.rb.hrms.resume_parser.services.HRMSAIService import AIService
from com.rb.hrms.resume_parser.logging.Logging_file import custom_logger

logger = custom_logger


class CityService:
    def __init__(self):
        self.ai_service = AIService('gemini')

    @custom_logger.log_around
    def cleanData(self, hrms_api_service, city_name):
        try:
            response = self.search_city_in_master(hrms_api_service, city_name)  # search
            print(f"Response :: {response}")
            if response is None:
                self.ai_service.login()
                # TODO - Call AI Service
                AI_response = self.ai_service.ai_api_call(
                    f"{CITY_DETAILS_PROMPT_PART1} {city_name} {CITY_DETAILS_PROMPT_PART2} {CITY_DETAILS_RESPONSE_FORMAT}")
                print(f"AI RESPONSE :: {response}")
                if AI_response:
                    city_name = self.get_clean_city_name(AI_response)
                    response = self.insert_city_in_master(hrms_api_service, city_name)
                else:
                    return None
            """if response is None:
                pass
                # TODO - Insert data into city Master
            else:
                city_name = self.get_clean_city_name(response)
                response = self.search_city_in_master(hrms_api_service, city_name)  # search
                print(f"Response :: {response}")
                if response is None:
                    response = self.insert_city_in_master(hrms_api_service, city_name)"""
            return response
        except Exception as e:
            logging.error(str(e))

    @custom_logger.log_around
    def search_city_in_master(self, hrms_api_service, city_name):
        try:
            url = f"{hrms_api_service.base_url}/{SEARCH_CITY_BY_NAME_API_END_POINT}"
            print(f"URL :: {url}")

            json_body_of_city = {"cityName": city_name}

            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='GET',
                                                      url=url, data=json_body_of_city)
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @custom_logger.log_around
    def insert_city_in_master(self, hrms_api_service, city_name):
        try:

            url = f"{hrms_api_service.base_url}/{INSERT_CITY_API_END_POINT.format(city_name=city_name)}"
            print(f"URL :: {url}")
            payload = {"cityName": city_name,
                       "isActive": True}
            response = hrms_api_service.hrms_api_call(headers=hrms_api_service.headers, method='POST',
                                                      url=url, data=payload)
            if response:
                return response
        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None

    @custom_logger.log_around
    def get_clean_city_name(self, response):
        try:
            self.city_response = response
            logging.info(self.city_response)
            clean_city_response = self.city_response.replace('```', "").replace('json', "").replace('JSON',
                                                                                                    "").replace(
                '\n', '')
            city_data = json.loads(clean_city_response)
            if 'city_name' in city_data and city_data['city_name'] is not None:
                city_data['city_name'] = city_data['city_name'].upper()

            logging.info(f"city information {city_data}")
            city_name = city_data.get('city_name')

            return city_name

        except Exception as e:
            print("Exception occurrence while processing ai response...")
            print(e)
            return None
