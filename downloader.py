import sys, os, cfscrape
from clint.textui import progress

class Downloader(object):
    def __init__(self, url=None, file_path=None):
        self.url = url
        self.file_path = file_path
        self.scraper = cfscrape.create_scraper()

    def start(self):
        file_name = self.file_path.split('\\')[-1]
        if not self._check_duplicate():
            print 'Skipping download %s.' % file_name
            return
        resp = self.scraper.get(self.url, allow_redirects=True, stream=True)
        length = int(resp.headers.get('content-length', default=0))
        resp_it = resp.iter_content(chunk_size=1024)
        label = 'Downloading %s - ' % file_name
        size = (length/1024) + 1
        self._show_progress(resp_it, label, size)

    def _check_duplicate(self):
        if os.path.exists(self.file_path):
            message = 'File %s already exists. Overwite file? (Y/N): '
            overwrite = raw_input(message % self.file_path)
            if overwrite.lower() == 'y':
                return True
            elif overwrite.lower() == 'n':
                return False
            else:
                print('Invalid input. Please try again.')
                return self._check_duplicate()
            #endelse
        else:
            return True
        #endelse    
        
    def _show_progress(self, resp_it, label, size):
        with open(self.file_path, 'wb') as f:
            for chunk in progress.bar(resp_it, label=label, expected_size=size):
                f.write(chunk)
                f.flush()
            #endfor
        #endwith
    #enddef

 
