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
        # page_number is the current page
        if int(self.page_number) == 1:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, 'page_number', 1)

    def get_last_link(self):
        if int(self.page_number) == self.paginator.num_pages:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, 'page_number', self.paginator.num_pages)

    def get_previous_link(self):
        url = self.request.build_absolute_uri()
        page = self.paginator.page(self.page_number)
        if page.has_previous():
            url = replace_query_param(url, 'page_number', page.previous_page_number())
        else:
            url = None
        return url

    def get_next_link(self):
        url = self.request.build_absolute_uri()
        page = self.paginator.page(self.page_number)
        if page.has_next():
            url = replace_query_param(url, 'page_number', page.next_page_number())
        else:
            url = None
        return url
