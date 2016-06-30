from __future__ import unicode_literals

from django.db import models


class Cloud:

    def __init__(self, user_username, cloud_name, cloud_gallery, images_list):
        self.user_username = user_username
        self.cloud_name = cloud_name
        self.cloud_gallery = cloud_gallery
        self.number_of_images = len(images_list)
        self.number_of_pages = (self.number_of_images / 15) + 1
        self.images_list = images_list

    def get_images_by_page(self, page_number):
        if (page_number > self.number_of_pages or page_number < 1):
            return []
        else:
            start_index = (page_number - 1) * 15
            end_index_temp = page_number * 15 - 1
            end_index = (self.number_of_images - 1) if (self.number_of_pages == page_number) else end_index_temp
            return self.images_list[start_index:end_index]
