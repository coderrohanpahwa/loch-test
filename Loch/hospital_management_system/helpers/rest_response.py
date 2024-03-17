
class RestResponse:
    def __init__(self,data={},status=0,message="",err="") :

        self.__entity = {}
        self.__entity['data'] = data
        self.__entity['status'] = status
        self.__entity['message'] = message
        self.__entity['err'] = err
    def to_json(self):
        if 'created_at' in self.__entity['data']:
            if self.__entity['data']['created_at'] and type(self.__entity['data']['created_at']) != str:
                self.__entity['data']['created_at'] = self.__entity['data']['created_at'].strftime(
                    "%Y-%m-%dT%H:%M:%S.000Z")
            else:
                self.__entity['data']['created_at'] = self.__entity['data']['created_at']
        if 'updated_at' in self.__entity['data']:
            if self.__entity['data']['updated_at'] and type(self.__entity['data']['updated_at']) != str:
                self.__entity['data']['updated_at'] = self.__entity['data']['updated_at'].strftime(
                    "%Y-%m-%dT%H:%M:%S.000Z")
            else:
                self.__entity['data']['updated_at'] = self.__entity['data']['updated_at']
        return self.__entity