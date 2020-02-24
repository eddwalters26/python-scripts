class ChangeCapture:
    __batchaction = ['Insert', 'Update', 'Delete', 'Copy']

    def __init__(self, before_dataset, key_column, check_column):
        self.before_dataset = before_dataset
        self.key_column = key_column
        self.check_column = check_column
        self.after_dataset = {}
        self.delete_dataset = {}

    def check_row_change(self, new_data_row):
        action = 0
        keyToCheck = list(new_data_row.keys())[0]
        checkColumnValue = new_data_row[keyToCheck][self.check_column]

        if len(self.before_dataset) > 0:
            if keyToCheck in self.before_dataset:
                if checkColumnValue == self.before_dataset[keyToCheck][self.check_column]:
                    action = 3
                else:
                    action = 1
        
        self.after_dataset.update(new_data_row)
        return self.__batchaction[action]

    def get_deletes(self):
        #return rows from before_dataset that need to be deleted
        for key, data in self.before_dataset.items():
            if key not in self.after_dataset:
                data["batchaction"] = self.__batchaction[2]
                self.delete_dataset.update({key: data})
        return self.delete_dataset
