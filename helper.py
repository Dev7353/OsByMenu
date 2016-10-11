import platform
from collections import OrderedDict
import subprocess
import shlex


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
                            ("Kernel Redflease", platform.release()),
                            ("System", os),
                            ("Linux Release", platform.linux_distribution[1]),  # deprecated functions
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
    model = str("0x{:02x}".format(model))
    family = str("0x{:02x}".format(family))

    file = open("proc_code.txt", 'r')

    for line in file.readlines():
        if model and family in line:
            return line.split(':')[0].replace(" ", "")  # slices the codename from line


def cpu_info():
    '''
    :return: Dictionary mit Dictionary, Key des ersten Dictionaries ist die CPU Nummer (z.B. 1), das zweite Dictionary enthaelt somit das Dictionary mit folgenden CPU Informationen
    '''

    os = platform.system()

    if os == 'Linux':
        model = int(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.model")))
        family = int(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.family")))
        frequency = str(int(subprocess.check_output(shlex.split("sysctl -n hw.cpufrequency"))) * (10**-6)) + " Mhz"
        modelname = str(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.brand_string")))
        modelname = modelname[2:len(modelname)-3]  # remove string modifiers
        cm = codename(model, family)

        if cm is "":
            cm = "Newer microarchitecture"

        return OrderedDict([('Modelname', modelname),
                          ('Architecture', platform.architecture()[0]),
                          ('Model', str(model)),
                          ('Family', str(family)),
                          ('Frequency', frequency),
                          ('Codename', cm)])
    elif os == 'Darwin':
        file = open("/proc/cpuinfo", 'r')
        cpus = int(subprocess.check_output(shlex.split("grep -c ^processor /proc/cpuinfo ")))  # number of cpu
        i = 0
        d = OrderedDict()

        for line in file.readlines():
            if i == cpus-1:
                break;

            d[str(i)] = OrderedDict()
            d[str(i)]['Processor'] = str(i)

            if 'Modelname' in line:
                d[str(i)]['Modelname'] = line.split(':')[0].replace(" ", "")

            elif 'Architecture' in line:
                d[str(i)]['Architecture'] = 'Architecture', line.split(':')[0].replace(" ", "")

            elif 'Model' in line:
                d[str(i)]['Model'] = 'Model', line.split(':')[0].replace(" ", "")

            elif 'Family' in line:
                d[str(i)]['Family'] = 'Model', line.split(':')[0].replace(" ", "")

            elif 'Frequency' in line:
                d[str(i)]['Model'] = 'Model', line.split(':')[0].replace(" ", "")

            elif 'Codename' in line:
                d[str(i)]['Codename'] = 'Codename', line.split(':')[0].replace(" ", "")
        return d

    elif os == 'Windows':
        pass

