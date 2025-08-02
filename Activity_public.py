class ActivityPublic:
    count_id = 0

    def __init__(self, activity_name, activity_details, activity_start_datetime, activity_end_datetime):
        ActivityPublic.count_id += 1
        self.__activity_id = ActivityPublic.count_id
        self.__activity_name = activity_name
        self.__activity_details = activity_details
        self.__activity_start_datetime = activity_start_datetime
        self.__activity_end_datetime = activity_end_datetime

    def get_activity_id(self):
        return self.__activity_id

    def get_activity_name(self):
        return self.__activity_name

    def get_activity_details(self):
        return self.__activity_details

    def get_activity_start_datetime(self):
        return self.__activity_start_datetime

    def get_activity_end_datetime(self):
        return self.__activity_end_datetime



    def set_activity_id(self, activity_id):
        self.__activity_id = activity_id

    def set_activity_name(self, activity_name):
        self.__activity_name = activity_name

    def set_activity_details(self, activity_details):
        self.__activity_details = activity_details

    def set_activity_start_datetime(self, activity_start_datetime):
        self.__activity_start_datetime = activity_start_datetime

    def set_activity_end_datetime(self, activity_end_datetime):
        self.__activity_end_datetime = activity_end_datetime
