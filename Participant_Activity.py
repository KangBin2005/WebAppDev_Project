class ParticipantActivity:
    count_id = 0

    def __init__(self, name, description, venue, date, start_time, end_time):
        ParticipantActivity.count_id += 1
        self.__activity_id = ParticipantActivity.count_id
        self.__name = name
        self.__description = description
        self.__venue = venue
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time

    def get_activity_id(self):
        return self.__activity_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_venue(self):
        return self.__venue

    def get_date(self):
        return self.__date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def set_activity_id(self, activity_id):
        self.__activity_id = activity_id

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_venue(self, venue):
        self.__venue = venue

    def set_date(self, date):
        self.__date = date

    def set_start_time(self, start_time):
        self.__start_time = start_time

    def set_end_time(self, end_time):
        self.__end_time = end_time