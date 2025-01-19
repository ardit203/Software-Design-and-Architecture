from Services.Fundamental_Service import FundamentalService


class FundamentalController:
    def __init__(self, issuer):
        self._service = FundamentalService(issuer)

    def get_fundamental_analysis(self):
        return self._service.get_fundamental_data()

