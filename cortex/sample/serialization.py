class Serialization:
    @staticmethod
    def remove_endianity(data):
        if (0 == len(data)):
            return data
        e = data[0]
        if e not in ['<', '>', '!', '@', '=']:
            return data
        return data[1:] 
    