import os.path


class WxFile:
    wxfile_name_length = 0
    wxfile_name = ""
    offset_in_data_section = 0
    wxfile_size = 0
class WxApkg:
    miniprogram_id = ""
    be = ''
    blank = ""
    index_section_length = 0
    data_section_length = 0
    ed = ''
    sum_of_the_files = 0
    full_wxapkg_file_path = ""

    def __init__(self, full_wxapkg_file_path, miniprogram_id):
        self.full_wxapkg_file_path = full_wxapkg_file_path
        self.miniprogram_id = miniprogram_id

    def resolve_wxapkg(self):
        with open(self.full_wxapkg_file_path, 'rb') as wxapkg:
            self.be = wxapkg.read(1)
            self.blank = wxapkg.read(4)
            self.index_section_length = wxapkg.read(4)
            self.data_section_length = wxapkg.read(4)
            self.ed = wxapkg.read(1)
            self.sum_of_the_files = int.from_bytes(wxapkg.read(4), 'big')
            wxfiles = []
            for i in range(self.sum_of_the_files):
                wxfile = WxFile()
                wxfile.wxfile_name_length = wxapkg.read(4)
                print(wxfile.wxfile_name_length)
                wxfile.wxfile_name_length = int.from_bytes(wxfile.wxfile_name_length, 'big')

                wxfile.wxfile_name = wxapkg.read(wxfile.wxfile_name_length)
                print(wxfile.wxfile_name)
                wxfile.wxfile_name = wxfile.wxfile_name.decode('ascii')

                wxfile.offset_in_data_section = int.from_bytes(wxapkg.read(4), 'big')
                wxfile.wxfile_size = int.from_bytes(wxapkg.read(4), 'big')
                wxfiles.append(wxfile)
            for result in wxfiles:
                temp_path = self.miniprogram_id + "_resolve" + result.wxfile_name
                directory_path = os.path.split(temp_path)[0]
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                with open(temp_path, 'wb') as temp:
                    temp.write(wxapkg.read(result.wxfile_size))

wxapkg_sample = WxApkg("wx0bad87c71b11ea8c", "wx0bad87c71b11ea8c")
wxapkg_sample.resolve_wxapkg()



