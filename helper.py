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
                            ("Architecture", platform.architecture()[0]),
                            ("Kernel Release", platform.release()),
                            ("System", os),
                            ("Linux Release", platform.linux_distribution()[1]),  # deprecated functions
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

    if os == 'Darwin':
        model = int(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.model")))
        family = int(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.family")))
        frequency = str(int(subprocess.check_output(shlex.split("sysctl -n hw.cpufrequency"))) * (10**-6)) + " Mhz"
        modelname = str(subprocess.check_output(shlex.split("sysctl -n machdep.cpu.brand_string")))
        modelname = modelname[2:len(modelname)-3]  # remove string modifiers
        cm = codename(model, family)

        return OrderedDict([('Modelname', modelname),
                          ('Architecture', platform.architecture()[0]),
                          ('Model', str(model)),
                          ('Family', str(family)),
                          ('Frequency', frequency),
                          ('Codename', cm)])
    elif os == "Linux":
        cpuinfo = get_proc_cpuinfo_as_list()
        cpus = int(subprocess.check_output(shlex.split("grep -c ^processor /proc/cpuinfo ")))  # number of cpu
        file = open("/proc/cpuinfo", "r")
        d = OrderedDict()
        while(len(cpuinfo) > 0):
            for i in range(cpus):
                d[str(i)] = OrderedDict()
                for j in range(5):
                    d[str(i)][cpuinfo[0][0]] = cpuinfo[0][1]
                    del cpuinfo[0]


        # add additional attributes which are not in the cpuinfo file
        for key in d.keys():
            d[key]["architecture"] = platform.architecture()[0]
            d[key]["codename"] = codename(model=int(d[key]["model"]), family=int(d[key]["cpu family"]))
        return d

    elif os == 'Windows':
        pass


def get_proc_cpuinfo_as_list():
    '''
    :return: double list with processor number, model/name, cpu family and cpu frequency
    '''
    infos = subprocess.check_output(shlex.split("grep 'processor\|model name\|cpu family\|model\|cpu MHz' /proc/cpuinfo ")).decode(encoding="UTF-8")
    infos = infos.replace("\\", "").replace("\t", "").split("\n")

    for item in range(len(infos)):
        infos[item]= infos[item].split(":")

    del infos[len(infos)-1]  # remove empty entry
    return infos

