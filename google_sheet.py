import gspread
import os
from pprint import pprint

from google.auth.exceptions import RefreshError


class Icont_sheet():
    def __init__(self):
        # self.google_account = gspread.service_account(filename="google_credentials.json") # - egy meghatározott email cimmel lehet módosítani a táblázatokat.
        #self.google_account = gspread.oauth(credentials_filename="OAUTH_client_secret_google_credentials.json") # - nem kell külön e-mail címet megadni, hogy a python program hozzáférjen a táblázathoz-
        self.google_account = gspread.service_account(filename="pandalejelentes-new.json") # - egy meghatározott email cimmel lehet módosítani a táblázatokat.

    """FONTOS A LENTI SZÖVEG!!!"""
    # He megjelenik az alábbi hibaüzenet:
    #
    # Toke expired, client is unable to continue:
    # RefreshError: ('invalid_grant: Token has been expired or revoked.',
    #               {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})
    #
    # Akkor törölni kell az alábbi filet:
    # 'c:\Users\kelet\AppData\Roaming\gspread\authorized_user.json'
    #
    # a lenti függvény ezt meg tudja csinálni, csak meg kell hívni valahol!!!
    #
    # def authorized_user_json_file_delete(self)


    def authorized_user_json_file_delete(self):
        try:
            os.remove(r"c:\Users\kelet\AppData\Roaming\gspread\authorized_user.json")
        except:
            os.remove(r"c:\Users\Szabina\AppData\Roaming\gspread\authorized_user.json")

    def opensheet(self, sheetname, worksheet):
        """opensheet has 2 variabele: sheet (string) = name of the google sheet, worksheet (string) = the workhseet where you want to work in the sheet"""
        try:
            self.sheet = self.google_account.open_by_url(sheetname)
        except RefreshError:
            self.authorized_user_json_file_delete()
            print("Lejárt a Google hoozáférésed!! INDÍTSD újra a programot és már működni fog.")
            exit()
            return False



        #kiszallitasok = google_account.open("KISZALLITASOK")
        #kiszallitasok = google_account.open_by_key('1mQN5woJVHJrqf49D4TlEwQGtDx8PsnqKiLa6B_3Fd4g')
        #kiszallitasok = sgoogle_account.open_by_url('https://docs.google.com/spreadsheets/d/1mQN5woJVHJrqf49D4TlEwQGtDx8PsnqKiLa6B_3Fd4g/edit#gid=0')

        self.worksheet = self.sheet.worksheet(worksheet)


    def get_row_number_of_the_any_container(self, container):
        """get the row number for a, ex: container"""
        cont = container
        container_row = self.worksheet.find(cont)
        print(container_row)
        cell_coord = str(container_row).strip("<Cell R 'NEW BL'>").split("C")
        row = cell_coord[0]
        print(row)
        return row

    def get_rows_and_row_numbers(self, item):
        """item = find any item from the google sheet and return the row or rows of this item/these items"""
        self.item = item
        container_rows_info = {
            "rows":"",
            "row_numbers":""
        }
        rows = []
        row_numbers = []
        item_cell_list = self.worksheet.findall(self.item)
        for cell in item_cell_list:
            cell_str = str(cell)
            cell_coord = cell_str.strip(f"<Cell R '{self.item}'>").split("C")
            row = cell_coord[0]

            rows.append(self.worksheet.row_values(row))
            row_numbers.append(row)

            container_rows_info["rows"] = rows
            container_rows_info["row_numbers"] = row_numbers

            #print(container_rows_info)

        return container_rows_info

    def get_container_rows(self, item):
        """item = find any item from the google sheet and return the row or rows of this item/these items"""
        self.item = item
        container_rows = []
        item_cell_list = self.worksheet.findall(self.item)
        for cell in item_cell_list:
            cell_str = str(cell)

            cell_coord = cell_str.split(item)[0].split("<Cell ")[1].split("C")[0].strip("<Cell R")
            row = cell_coord
            #print(self.worksheet.row_values(row))
            container_rows.append(self.worksheet.row_values(row))

        return container_rows

    def get_container_row_numbers(self, item):
        """item = find any item from the google sheet and return the row numbers of this item/these items"""
        self.item = item
        container_rows_numbers = []
        item_cell_list = self.worksheet.findall(self.item)
        for cell in item_cell_list:
            cell_str = str(cell)
            #cell_coord = cell_str.strip(f"<Cell R'{self.item}'>").split("C")
            cell_coord = cell_str.split("R")[1]
            cell_coord = cell_coord.split("C")
            row = cell_coord[0]
            #print(self.worksheet.row_values(row))
            container_rows_numbers.append(row)

        return container_rows_numbers

    def get_all_values_from_worksheet(self):
        return self.worksheet.get_all_values()

    def get_all_records_from_worksheet_in_dict(self):
        return self.worksheet.get_all_records()

    def get_cell_value(self, row):
        cell_list = self.worksheet.findall("Rug store")

    def updating_cell(self, row, col, value):
        """Update a cell from in the google sheet"""
        print(f"   Google cella adatainak beírása: sor:{row}, oszlop:{col}, érték:{value}")
        #self.worksheet.update_cell(row, col, value)
        self.worksheet.update_cell(row, col, value)

    def bild_dictionary(self, row_key, row_value):
        """Bild a dictionary for two list:   list1: sheet-1.line, list2: sheet-any row form the list"""
        row_dict = {}
        row_dict = dict(zip(row_key, row_value))
        return row_dict




"""
googletabla = Icont()
googletabla.opensheet(sheetname="POLAND, HU - RAIL Transport", worksheet="PL, HU - Rail Transport")
# print(googletabla.get_container_row("CICU3126473"))
print(googletabla.get_container_rows("Container NO.."))
print(googletabla.get_container_rows("CICU3344618"))

print(len(googletabla.get_container_rows("Container NO..")))
print(len(googletabla.get_container_rows("CICU3344618")))

googletabla.updating_cell(1608, 6, "efwdfsdfsd")

#print(googletabla.bild_dictionary(googletabla.get_container_rows("Container NO.."), googletabla.get_container_rows("CICU3344618")))
"""