from rest_framework.utils.urls import remove_query_param, replace_query_param


class NavigationLinks:
    paginator = None
    page_number = None
    request = None

    def __init__(self, request, paginator, page_number):

        self.request = request
        self.paginator = paginator
        self.page_number = page_number

    def get_first_link(self):
        return 1

    def get_last_link(self):
        return int(self.paginator.num_pages)

    def get_previous_link(self):
        page = self.paginator.page(self.page_number)
        if page.has_previous():
            url = int(page.previous_page_number())
        else:
            url = None
        return url

    def get_next_link(self):
        page = self.paginator.page(self.page_number)
        if page.has_next():
            url = int(page.next_page_number())
        else:
            url = None
        return url
