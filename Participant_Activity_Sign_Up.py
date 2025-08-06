class ParticipantActivitySignUp:
    count_id = 0  # Class variable to auto-generate IDs

    def __init__(self, name, phone, email, accessibility_needs, emergency_contact_name, emergency_phone, activity_id):
        ParticipantActivitySignUp.count_id += 1
        self.__signup_id = ParticipantActivitySignUp.count_id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__accessibility_needs = accessibility_needs
        self.__emergency_contact_name = emergency_contact_name
        self.__emergency_phone = emergency_phone
        self.__activity_id = activity_id  # Links to ParticipantActivity

    # Getters
    def get_signup_id(self):
        return self.__signup_id

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_accessibility_needs(self):
        return self.__accessibility_needs

    def get_emergency_contact_name(self):
        return self.__emergency_contact_name

    def get_emergency_phone(self):
        return self.__emergency_phone

    def get_activity_id(self):
        return self.__activity_id

    # Setters
    def set_signup_id(self, signup_id):
        self.__signup_id = signup_id

    def set_name(self, name):
        self.__name = name

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_accessibility_needs(self, accessibility_needs):
        self.__accessibility_needs = accessibility_needs

    def set_emergency_contact_name(self, emergency_contact_name):
        self.__emergency_contact_name = emergency_contact_name

    def set_emergency_phone(self, emergency_phone):
        self.__emergency_phone = emergency_phone

    def set_activity_id(self, activity_id):
        self.__activity_id = activity_id