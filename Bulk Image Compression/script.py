from PIL import Image
import sys
import os

# python script.py <format to compress> <format to output> <input folder> <output folder>
class BulkImageCompress:
    quality:int = 85
    kwargs:dict = {"progressive": True, 
                   "optimize": True}

    def __init__(self, in_type, out_type, in_folder, out_folder):
        self.in_type = in_type
        self.out_type = out_type
        self.in_folder = in_folder
        self.out_folder = out_folder

        if out_type == "webp":
            self.kwargs = {"method": 6, "lossless": False}

    def get_files(self):
        self.file_list = []
        for (directory, directory_names, filenames) in os.walk(self.in_folder):
            for filename in filenames:
                if filename.endswith(f".{self.in_type}"): 
                    # Append to list as full path
                    self.file_list.append(os.sep.join([directory, filename]))

    def compress_all(self):
        for file in self.file_list:
            self.compress_image(file)

    def compress_image(self, file_path):
        img = Image.open(file_path)
        # Get just file name
        file_name = os.path.basename(file_path)

        if self.out_type in ("jpg", "jpeg"):
            img = img.convert('RGB') # Remove transparency
            self.out_type = "jpeg" 

        # Create path with output folder, type and file name
        output_name = file_name.replace(f".{self.in_type}", f"_compressed.{self.out_type}")

        img.save(os.sep.join([self.out_folder, output_name]), # Create full path
                self.out_type,
                quality=self.quality, # Lossless quality setting
                **self.kwargs)   # Dynamic arguments based on output type

if __name__ == "__main__":
    bic = BulkImageCompress(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    bic.get_files()
    bic.compress_all()
