# coding:utf-8
import os


class Upload(object):
    upload_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/contracts'
    
    def __init__(self):
        self.allowed_extensions = set(['sol'])

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.allowed_extensions

