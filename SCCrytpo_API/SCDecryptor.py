# -*- coding: utf-8 -*-

import os
import shutil
import uuid

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from SCCrytpo_API.SCCryptoUtil import SCCrypto

from cloud_API.google_drive_API import GoogleDriveAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.dropbox_API import DropboxAPI

from api.models import Encryption

class SCDecryptor:

    def __init__(self):
        self.temp_dir = "sc_temp_down"
        self.temp_meta1D = "meta1-de.txt"
        self.temp_meta1E = "meta1-en.txt"

        self.storage_folder = "sc_storage"
        self.storage_GD_folder = "google_drive"
        self.storage_OD_folder = "one_drive"
        self.storage_DB_folder = "drop_box"
        self.storage_file_pri = "private.txt"

        self.meta1E = 'meta1-en.txt'
        self.meta1D = 'meta1-de.txt'
        self.meta1EEnum = 1
        self.meta1DEnum = 2

        self.meta2E = 'meta2-en.txt'
        self.meta2D = 'meta2-de.txt'
        self.meta2EEnum = 3
        self.meta2DEnum = 4
    # bice izmena posle, zbog nacina downloada.
    def decryptLocal(self, location_folder_value, location_folder_name, download_path, drive):
        user_id, bl = drive.get_user_data()

        meta_pri = self.temp_dir + "/" + self.temp_meta1D
        meta_pub = self.temp_dir + "/" + self.temp_meta1E

        stored_file_pri = None

        if isinstance(drive,  GoogleDriveAPI):
            stored_file_pri = self.storage_folder + "/" + self.storage_GD_folder + "/" + user_id + "/" + self.storage_file_pri

        if isinstance(drive,  OneDriveAPI):
            stored_file_pri = self.storage_folder + "/" + self.storage_OD_folder + "/" + user_id + "/" + self.storage_file_pri

        if isinstance(drive,  DropboxAPI):
            stored_file_pri = self.storage_folder + "/" + self.storage_DB_folder + "/" + user_id + "/" + self.storage_file_pri

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        drive.get_meta_file(location_folder_name, self.temp_dir, self.meta1DEnum)
        drive.get_meta_file(location_folder_name, self.temp_dir, self.meta1EEnum)

        private1_exists = False
        if os.path.exists(stored_file_pri) and os.stat(stored_file_pri).st_size != 0:
            private1_exists = True

        private2_exists = False
        if os.path.exists(meta_pri) and os.stat(meta_pri).st_size != 0:
            private2_exists = True

        list_file_exists = False
        if os.path.exists(meta_pub):
            list_file_exists = True

        if not(private1_exists and private2_exists and list_file_exists):
            # ovde neka forma
            return

        if os.stat(meta_pub).st_size == 0:
            # ovde neka forma
            return

        with open(meta_pri, 'r') as fhI:
            key_part_1 = fhI.read()

        with open(stored_file_pri, 'r') as fhI:
            key_part_2 = fhI.read()

        sc = SCCrypto()
        key = sc.mergeSK_RSA(key_part_1, key_part_2)

        dsk = None
        with open(meta_pub, 'r') as fhI:

            for line in fhI:
                line_content = str.split(line)
                if len(line_content) == 1:
                    dsk = key.decrypt(sc.b642bin(line_content[0]))
                else:

                    drive.download_file(location_folder_value, line_content[0], self.temp_dir)

                    with open(self.temp_dir + "/" + line_content[0], 'r') as fhI2:
                        enc_pic_data_hex = fhI2.read()
                        enc_pic_data_bin = sc.b642bin(enc_pic_data_hex)

                        aes = AES.new(dsk, AES.MODE_CFB, sc.b642bin(line_content[1]))
                        dec_pic_data_bin = aes.decrypt(enc_pic_data_bin)

                        location = download_path + "/" + line_content[0]
                        with open(location, 'wb') as fhO:
                            fhO.write(dec_pic_data_bin)

        shutil.rmtree(self.temp_dir)

        return True

    def decryptShared(self, dir_path,  gallery_name, drive):

        user_id = drive.get_user_id_by_folder_id(gallery_name)
        hid = SHA256.new(user_id).hexdigest()
        ret = Encryption.objects.filter(id=hid)
        if len(ret) == 0:
            return None

        user_temp_dir = dir_path + str(uuid.uuid1())
        if not os.path.exists(user_temp_dir):
            os.makedirs(user_temp_dir)

        meta_pri = user_temp_dir + "/" + self.meta2D
        meta_pub = user_temp_dir + "/" + self.meta2E

        cloud_user_id, bl = drive.get_user_data()

        same_user = False
        if cloud_user_id == user_id:
            same_user = True

        # drive.download_file(gallery_name, 'slika.jpg', 'viewer/static/viewer/img')
        # drive.download_shared_file(gallery_name, 'meta1-de.txt', 'tu')

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
            return None

        with open(meta_pri, 'r') as fhI:
            key_part_1 = fhI.read()

        key_part_2 = ret[0].private_key_part

        sc = SCCrypto()
        key = sc.mergeSK_RSA(key_part_1, key_part_2)

        with open(meta_pub, 'r') as fhI:

            i = 0
            for line in fhI:
                line_content = str.split(line)
                if len(line_content) == 1:
                    dsk = key.decrypt(sc.b642bin(line_content[0]))
                else:

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
                        with open(location, 'wb') as fhO:
                            fhO.write(dec_pic_data_bin)

                    i += 1

                    if i == 9:
                        break

        return user_temp_dir







