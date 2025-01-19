from Services.Technical_Service import TechnicalService



class TechnicalController:
    _service = None


    def __init__(self, issuer, indicator, from_date=None):
        self._service = TechnicalService(issuer, indicator, from_date)

    def get_technical_data(self):
        return self._service.get_technical_data()


