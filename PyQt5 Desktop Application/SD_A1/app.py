from PyQt5 import QtWidgets
from presentation.main_page import MainPage
import sys

# main function where the MainPage is displayed
if __name__ == '__main__':
    
    # main application
    app = QtWidgets.QApplication(sys.argv)

    # show the main page view
    main_page = MainPage()
    main_page.show()

    # exit application
    sys.exit(app.exec_())
