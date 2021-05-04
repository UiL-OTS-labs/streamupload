from django.utils.deconstruct import deconstructible
from datetime import datetime

@deconstructible
class UploadFilenameFactory:
    '''A callable class which can be passed to upload_to() in FileFields
    and can be deconstructed for migrations'''
    
    def __init__(self, prefix):
        self.prefix = prefix
    
    def __call__(self, upload, original_fn):
        '''Returns a custom filename preserving the original extension'''
                
        extension = '.' + original_fn.split('.')[-1][-7:] # At most 7 chars seems reasonable
        
        weekdays = ['Mon',
                    'Tue',
                    'Wed',
                    'Thu',
                    'Fri',
                    'Sat',
                    'Sun',
                    ]
        
        prefix = self.prefix
        token = str(upload.token)
        
        dt = upload.start_time
        if not dt:
            dt = datetime.now()
        
        weekday = weekdays[dt.weekday()]
        date = str(dt.date())
        
        time = '{}-{}-{}.{}'.format(
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            )        
        
        fn_parts = [prefix,
                    token,
                    weekday,
                    date,
                    time,
                    ]
        
        def not_empty(item):
            if item == None:
                return False
            if str(item) == '':
                return False
            return True
        
        fn_parts = filter(not_empty, fn_parts)
        
        return '_'.join(fn_parts) + extension 
