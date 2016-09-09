# -*- coding: utf-8 -*-

import os
import shutil
import uuid

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from SCCrytpo.SCCryptoUtil import SCCrypto

from cloud_API.google_drive_API import GoogleDriveAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.dropbox_API import DropboxAPI

from api.models import Encryption

class SCDecryptor:

    def __init__(self):
        self.temp_dir = "sc_temp_down"

        self.storage_GD_folder = "google_drive"
        self.storage_OD_folder = "one_drive"
        self.storage_DB_folder = "drop_box"

        self.meta2E = 'meta2-en.txt'
        self.meta2D = 'meta2-de.txt'
        self.meta2EEnum = 3
        self.meta2DEnum = 4

    def decryptShared(self, dir_path, dir_path_view, gallery_name, drive, folder_name, images_per_page, active_page):

        user_id = drive.get_user_id_by_folder_id(gallery_name)
        hid = SHA256.new(user_id).hexdigest()
        ret = Encryption.objects.filter(id=hid)
        if len(ret) == 0:
            return "", [], 0, 0

        if folder_name == "":
            folder_name = uuid.uuid1()

        user_temp_dir = dir_path + str(folder_name)
        user_temp_dir_view = dir_path_view + str(folder_name)
        if not os.path.exists(user_temp_dir):
            os.makedirs(user_temp_dir)

        meta_pri = user_temp_dir + "/" + self.meta2D
        meta_pub = user_temp_dir + "/" + self.meta2E

        cloud_user_id, bl = drive.get_user_data()

        same_user = False
        if cloud_user_id == user_id:
            same_user = True

        if same_user:
            drive.download_file(gallery_name, self.meta2D, user_temp_dir)
            drive.download_file(gallery_name, self.meta2E, user_temp_dir)
        else:
            drive.download_shared_file(gallery_name, self.meta2D, user_temp_dir)
            drive.download_shared_file(gallery_name, self.meta2E, user_temp_dir)

        private_exists = False
        if os.path.exists(meta_pri) and os.stat(meta_pri).st_size != 0:
            private_exists = True

        list_file_exists = False
        if os.path.exists(meta_pub) and os.stat(meta_pub).st_size != 0:
            list_file_exists = True

        if not (private_exists and list_file_exists):
            return "", [], 0, 0

        with open(meta_pri, 'r') as fhI:
            key_part_1 = fhI.read()

        key_part_2 = ret[0].private_key_part

        sc = SCCrypto()
        key = sc.mergeSK_RSA(key_part_1, key_part_2)

        ret_img_location = []
        with open(meta_pub, 'r') as fhI:

            i = 0
            for line in fhI:
                line_content = line.split(",")
                if len(line_content) == 1:
                    dsk = key.decrypt(sc.b642bin(line_content[0]))
                else:

                    if (i >= images_per_page * (active_page - 1)) and\
                            (i < images_per_page*active_page):
                        if same_user:
                            drive.download_file(gallery_name, line_content[0], user_temp_dir)
                        else:
                            drive.download_shared_file(gallery_name, line_content[0], user_temp_dir)

                        with open(user_temp_dir + "/" + line_content[0], 'r') as fhI2:
                            enc_pic_data_hex = fhI2.read()
                            enc_pic_data_bin = sc.b642bin(enc_pic_data_hex)

                            aes = AES.new(dsk, AES.MODE_CFB, sc.b642bin(line_content[1]))
                            dec_pic_data_bin = aes.decrypt(enc_pic_data_bin)

                            location = user_temp_dir + "/" + line_content[0]
                            location_view = user_temp_dir_view + "/" + line_content[0]
                            ret_img_location.append(location_view)
                            with open(location, 'wb') as fhO:
                                fhO.write(dec_pic_data_bin)

                    i += 1

            page_no = (i // images_per_page) + 1

        return folder_name, ret_img_location, page_no, i







