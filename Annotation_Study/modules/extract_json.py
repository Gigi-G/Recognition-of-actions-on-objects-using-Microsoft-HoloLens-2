class ExtractJSON:
    
    @staticmethod
    def get_json(path:str) -> str:
        """
        Return an extract JSON from a file
        """
        try:
            return open(path, "r").readlines()[0]
        except ValueError:
            print("ERROR: file not found.")
            exit(-1) 
        return None