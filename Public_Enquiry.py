class PublicEnquiry:
    count_id = 0

    def __init__(self, name, email, subject, message, status="Pending"):
        PublicEnquiry.count_id += 1
        self.__enquiry_id = PublicEnquiry.count_id
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__message = message
        self.__status = status  # Pending, Replied
        self.__reply = ""



    # Getter methods
    def get_enquiry_id(self):
        return self.__enquiry_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message

    def get_status(self):
        return self.__status

    def get_reply(self):
        return self.__reply



    # Setter methods
    def set_enquiry_id(self, enquiry_id):
        self.__enquiry_id = enquiry_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

    def set_status(self, status):
        self.__status = status

    def set_reply(self, reply):
        self.__reply = reply
        self.__status = "Replied"

