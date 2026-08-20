#healthcheck.py - API class for Healthcheck API calls

from .apihelper import APIHelper
import warnings

class Healthcheck():

     def healthcheck(self):
        warnings.warn(
            "Healthcheck().healthcheck() is deprecated, use Users().get_self() instead.", 
            category=DeprecationWarning, 
            stacklevel=2
        )
        return 

     def status(self):
        warnings.warn(
            "Healthcheck().status() is deprecated, use Users().get_self() instead.", 
            category=DeprecationWarning, 
            stacklevel=2
        )
        return 