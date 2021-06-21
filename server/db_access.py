from pymongo import MongoClient


class Connect(object):
    @staticmethod
    def get_connection():
        port = 27017
        url = "mongodb://localhost:27017"
        return MongoClient(url)


class DBAccess:
    database = None
    DB_name = 'programsDB'
    collection_name = 'programs'
    __instance = None  # to ensure its a singleton
    mongo_client = None
    isPopulated = False

    def __init__(self):
        if DBAccess.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.mongo_client = Connect().get_connection()
            # Create the programs database under the name 'programsDB'
            self.database = self.mongo_client.programsDB
            self.db_name = "programsDB"
            DBAccess.__instance = self
            if self.database.Programs.count() > 0:
                self.isPopulated = True

    @staticmethod
    def getInstance():
        if DBAccess.__instance is None:
            return DBAccess()
        return DBAccess.__instance

    def insert_programs(self, data):
        print(data)
        self.database.Programs.insert(data)
        if self.database.Programs.count() > 0:
            self.isPopulated = True

    def fetch_programs(self):
        programs_cursor = self.database.Programs.find()
        programs = []
        for program in programs_cursor:
            program.pop('_id', None)
            programs.append(program)
        return programs

    def update_programs(self):
        pass

    def update_program(self, program: dict, new_data: dict):
        self.database.Programs.update(program, {'$set': new_data})

    def drop_db(self):
        self.mongo_client.drop_database(self.db_name)
        if self.database.Programs.count() < 1:
            self.isPopulated = False
