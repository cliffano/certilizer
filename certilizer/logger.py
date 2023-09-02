"""Logger for Certilizer."""
from conflog import Conflog

def init():
    """Initialize logger.
    """
    cfl = Conflog(
        conf_dict={
            'level': 'info',
            'format': '[certilizer] %(levelname)s %(message)s'
        }
    )
    return cfl.get_logger(__name__)
