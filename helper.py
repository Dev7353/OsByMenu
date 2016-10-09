import platform
from collections import OrderedDict


def python_info():
    '''
    :return: Python-Versions-String (ohne Leerzeichen)
    '''
    return platform.python_version()


def system_info():
    '''
    :return: Dictionary mit entspr. Systeminformationen
    '''

    os = platform.system()

    if os == 'Darwin':
        return OrderedDict([("LABEL", "CONTENT"),
                            ("Architecture", platform.architecture()[0]),
                            ("Kernel Release", platform.release()),
                            ("Real Processor", platform.processor()),
                            ("System", os),
                            ("Mac Release", platform.mac_ver()[0])])
    elif os == 'Linux':
        return OrderedDict([("LABEL", "CONTENT"),
                            ("Architecture", platform.architecture()[0])
                            ("Kernel Release", platform.release()),
                            ("System", os),
                            ("Linux Release", platform.linux_distribution[1]),
                            ("Linux Distribution", platform.linux_distribution()[0])])
    elif os == 'Windows':
        pass
    else:
        pass


def codename(model, family):
    '''
    :param model:
    :param family:
    :return: Den Codenamen als String
    '''
    pass


def cpu_info():
    '''
    :return: Dictionary mit Dictionary, Key des ersten Dictionaries ist die CPU Nummer (z.B. 1), das zweite Dictionary enthaelt somit das Dictionary mit folgenden CPU Informationen
    '''
