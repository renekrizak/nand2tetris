import sys, os

class JackCompiler:
    def __init__(self):
        pass

    def get_args(self):
        if len(sys.argv) != 1:
            print('Program takes one argument')
            print('Usage: JackCompiler.py <folder name>')
            return 
        return sys.argv[1]
    
    def get_filenames(self, folder_name:  str):
        root_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))

        folder_path = os.path.join(root_dir, folder_name)

        #checks if user specified folder exists
        if not os.path.isdir(folder_path):
            print(f'Folder you specified: {folder_name} doesnt exist.')
            return []


        folderpaths = [os.path.join(folder_path, file)
                        for file in os.listdir(folder_path) if file.endswith('.jack')]
        return folderpaths 


    def main(self):
        folder_name = self.get_args()
        filepaths = self.get_filenames(folder_name)

        print(filepaths)

test = JackCompiler()
test.main()




