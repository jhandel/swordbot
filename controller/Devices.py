# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.0
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')

# Import the low-level C/C++ module
if __package__ or '.' in __name__:
    from . import _Devices
else:
    import _Devices

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == "thisown":
        return self.this.own(value)
    if name == "this":
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static:
        object.__setattr__(self, name, value)
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == "thisown":
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref

class ClearPathMotorSD(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _Devices.ClearPathMotorSD_swiginit(self, _Devices.new_ClearPathMotorSD())
    __swig_destroy__ = _Devices.delete_ClearPathMotorSD

    def attach(self, *args) -> "void":
        return _Devices.ClearPathMotorSD_attach(self, *args)

    def moveInMM(self, arg2: 'long', arg3: 'int') -> "bool":
        return _Devices.ClearPathMotorSD_moveInMM(self, arg2, arg3)

    def enable(self) -> "void":
        return _Devices.ClearPathMotorSD_enable(self)

    def getCommandedPosition(self) -> "long":
        return _Devices.ClearPathMotorSD_getCommandedPosition(self)

    def readHLFB(self) -> "bool":
        return _Devices.ClearPathMotorSD_readHLFB(self)

    def stopMove(self) -> "void":
        return _Devices.ClearPathMotorSD_stopMove(self)

    def stepsPer100mm(self, arg2: 'double') -> "void":
        return _Devices.ClearPathMotorSD_stepsPer100mm(self, arg2)

    def setMaxVelInMM(self, arg2: 'long') -> "void":
        return _Devices.ClearPathMotorSD_setMaxVelInMM(self, arg2)

    def setAccelInMM(self, arg2: 'long') -> "void":
        return _Devices.ClearPathMotorSD_setAccelInMM(self, arg2)

    def setDeccelInMM(self, arg2: 'long') -> "void":
        return _Devices.ClearPathMotorSD_setDeccelInMM(self, arg2)

    def commandDone(self) -> "bool":
        return _Devices.ClearPathMotorSD_commandDone(self)

    def disable(self) -> "void":
        return _Devices.ClearPathMotorSD_disable(self)
    PinA = property(_Devices.ClearPathMotorSD_PinA_get, _Devices.ClearPathMotorSD_PinA_set)
    PinB = property(_Devices.ClearPathMotorSD_PinB_get, _Devices.ClearPathMotorSD_PinB_set)
    PinE = property(_Devices.ClearPathMotorSD_PinE_get, _Devices.ClearPathMotorSD_PinE_set)
    PinH = property(_Devices.ClearPathMotorSD_PinH_get, _Devices.ClearPathMotorSD_PinH_set)
    Enabled = property(_Devices.ClearPathMotorSD_Enabled_get, _Devices.ClearPathMotorSD_Enabled_set)
    moveStateX = property(_Devices.ClearPathMotorSD_moveStateX_get, _Devices.ClearPathMotorSD_moveStateX_set)
    AbsPosition = property(_Devices.ClearPathMotorSD_AbsPosition_get, _Devices.ClearPathMotorSD_AbsPosition_set)

# Register ClearPathMotorSD in _Devices:
_Devices.ClearPathMotorSD_swigregister(ClearPathMotorSD)

class LoadSensor(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _Devices.LoadSensor_swiginit(self, _Devices.new_LoadSensor())
    __swig_destroy__ = _Devices.delete_LoadSensor

    def startRead(self, *args) -> "void":
        return _Devices.LoadSensor_startRead(self, *args)

    def currentlyReading(self) -> "bool":
        return _Devices.LoadSensor_currentlyReading(self)

    def stopRead(self) -> "void":
        return _Devices.LoadSensor_stopRead(self)

    def clearData(self) -> "void":
        return _Devices.LoadSensor_clearData(self)

    def ReadingAt(self, arg2: 'long') -> "uint32_t":
        return _Devices.LoadSensor_ReadingAt(self, arg2)

    def TimeOfReading(self, arg2: 'long') -> "long":
        return _Devices.LoadSensor_TimeOfReading(self, arg2)
    Channel = property(_Devices.LoadSensor_Channel_get, _Devices.LoadSensor_Channel_set)
    CurrentRead = property(_Devices.LoadSensor_CurrentRead_get, _Devices.LoadSensor_CurrentRead_set)
    RequestedRead = property(_Devices.LoadSensor_RequestedRead_get, _Devices.LoadSensor_RequestedRead_set)
    DateRate = property(_Devices.LoadSensor_DateRate_get, _Devices.LoadSensor_DateRate_set)
    Gain = property(_Devices.LoadSensor_Gain_get, _Devices.LoadSensor_Gain_set)

# Register LoadSensor in _Devices:
_Devices.LoadSensor_swigregister(LoadSensor)

class SwitchCallback(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    __swig_destroy__ = _Devices.delete_SwitchCallback

    def run(self) -> "void":
        return _Devices.SwitchCallback_run(self)

    def __init__(self):
        if self.__class__ == SwitchCallback:
            _self = None
        else:
            _self = self
        _Devices.SwitchCallback_swiginit(self, _Devices.new_SwitchCallback(_self, ))
    def __disown__(self):
        self.this.disown()
        _Devices.disown_SwitchCallback(self)
        return weakref.proxy(self)

# Register SwitchCallback in _Devices:
_Devices.SwitchCallback_swigregister(SwitchCallback)

class Switch(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self):
        _Devices.Switch_swiginit(self, _Devices.new_Switch())
    __swig_destroy__ = _Devices.delete_Switch

    def startMonitor(self, pin: 'uint8_t', edge: 'bool', poll: 'long', cballback: 'SwitchCallback') -> "void":
        return _Devices.Switch_startMonitor(self, pin, edge, poll, cballback)

    def stopMonitor(self) -> "void":
        return _Devices.Switch_stopMonitor(self)
    Pin = property(_Devices.Switch_Pin_get, _Devices.Switch_Pin_set)
    Edge = property(_Devices.Switch_Edge_get, _Devices.Switch_Edge_set)
    Poll = property(_Devices.Switch_Poll_get, _Devices.Switch_Poll_set)

# Register Switch in _Devices:
_Devices.Switch_swigregister(Switch)



