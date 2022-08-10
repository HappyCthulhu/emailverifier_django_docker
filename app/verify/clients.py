import requests


class MillionVerifierClient:

    def __init__(self):
        self.url = f'https/api.millionverifier.com/api/v3/?api=N7JIvmPXtNIEruQ3ILd8yAudp'

    def check_email(self, email) -> int:
        """
        Посылает запрос на проверку email в api.millionverifier.com

        :param email: проверяемый email
        :return: код ответа
        """
        response = requests.get(url=self.url, params={'email': email})
        j = response.json()
        result_code = j['resultcode']
        return result_code
