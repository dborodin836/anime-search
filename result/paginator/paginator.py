from typing import Union
from math import ceil


class Paginator:

    def __init__(self, page_no: int, no_of_results: Union[str, int], limit: int = 10):
        """Constructor"""
        if isinstance(no_of_results, str):
            self.__results = int(no_of_results)
        else:
            self.__results = no_of_results

        self.__current_page = page_no - 1  # Compensate that user starts counting from 1
        self.__DATA_LIMIT = limit
        self.__last_page = self.__results / self.__DATA_LIMIT

    @property
    def data_limit(self):
        """Returns info about curren data limit"""
        return self.__DATA_LIMIT

    @data_limit.setter
    def data_limit(self, value: int):
        """Sets data limit"""
        self.__DATA_LIMIT = value

    @property
    def page_offset(self):
        """Returns info about page offset"""
        return self.__current_page * self.__DATA_LIMIT

    @property
    def current_page(self):
        """Return current page"""
        return self.__current_page + 1

    @current_page.setter
    def current_page(self, value: int):
        """Sets current page"""
        self.__current_page = value

    @property
    def has_other_pages(self):
        """Return True if paginator has more than 1 page"""
        return True if self.__results > self.__DATA_LIMIT else False

    @property
    def last_page(self):
        """Returns last available page"""
        return ceil(self.__results / self.__DATA_LIMIT) - 1

    @property
    def pages_list(self):
        """Returns list of pages from the first available page to the last available page"""
        # Looks kinda awful
        pages_list = [x for x in range(self.current_first_page + 2 if self.current_first_page > 3
                                       else self.current_first_page, self.__current_page + 2)]
        pages_list.extend([x + 1 for x in range(self.current_page, self.current_last_page)])
        return pages_list

    @property
    def current_last_page(self):
        """Returns the lasts page, that gonna be displayed in the list of available pages"""
        if self.current_page + 5 > self.last_page:
            return self.last_page
        return self.current_page + 5
    
    @property
    def current_first_page(self):
        """Returns the first page, that gonna be displayed in the list of available pages"""
        if self.__current_page > 5:
            return self.__current_page - 5
        else:
            return 1
