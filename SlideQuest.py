from SQ_modules.Window import Window
import os
import sys
print(os.getcwd())
# print(os.path.isdir('levels'))

# root = os.path.dirname(__file__)
# print(root)
# sys.path.append(root)


if __name__=="__main__":
    window = Window()
    window.run()