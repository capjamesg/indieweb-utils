from typing import Any, Dict, List


class Paginator:
    def __init__(self, series: list, per_page: int):
        self.series = series
        self.per_page = per_page
        self.pages = self.paginate_list(series, per_page)
        self.total_pages = len(self.pages)
        self.total_objects = len(series)
        self.current_page = 0

    def paginate_list(self, series: list, per_page: int) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create a paginator for a series of objects.

        :param series: A list of objects to paginate.
        :return: A dictionary containing the paginated objects.
        """

        pages = [series[i : i + per_page] for i in range(0, len(series), per_page)]

        return pages

    def next_page(self) -> List[Dict[str, Any]]:
        """
        Get the next page of objects.

        :param current_page: The current page.
        :return: A list of objects.
        """

        all_pages = self.total_pages

        for p in self.pages:
            if self.current_page == all_pages:
                raise StopIteration

            self.current_page += 1

            yield p

    def previous_page(self) -> List[Dict[str, Any]]:
        """
        Get the previous page of objects.

        :param current_page: The current page.
        :return: A list of objects.
        """

        for p in self.pages:
            if self.current_page == 0:
                raise StopIteration

            self.current_page -= 1

            yield p

    def get_page(self, page: int) -> List[Dict[str, Any]]:
        """
        Get a specific page of objects.

        :param page: The page to get.
        :return: A list of objects.
        """

        return self.pages[page]
