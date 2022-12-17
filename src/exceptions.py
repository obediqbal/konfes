class EmptyOptionValueException(Exception):
    '''Exception raised when the input value of a slash command is empty'''

    def __init__(self, options: list[str]):
        self.options = options
        super().__init__(f'Options {self.options} can not be empty')


class AllOptionsUnselectedException(Exception):
    '''Exception raised when all of the options of a slash command are not selected'''

    def __init__(self):
        super().__init__('At least one of the available options must be selected')