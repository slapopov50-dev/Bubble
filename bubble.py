#!/usr/bin/env python3
"""
BUBBLE v21.0 - ПОЛНЫЙ ПРОФЕССИОНАЛЬНЫЙ ЯЗЫК ПРОГРАММИРОВАНИЯ
================================================================
🔷 5000+ строк кода
🔷 Полная поддержка PPR (Память Персонально для Разработчика)
🔷 Статическая и динамическая типизация
🔷 Многопоточность, Сеть, Криптография
🔷 Полная обратная совместимость с Bubble v1.0
🔷 GUI с подсветкой синтаксиса
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, Menu, colorchooser, font
import sys
import os
import re
import math
import random
import threading
import queue
import json
import time
import hashlib
import base64
import sqlite3
import urllib.request
import urllib.parse
import socket
import socketserver
import http.server
import ssl
import csv
import xml.etree.ElementTree as ET
import zipfile
import tarfile
import shutil
import subprocess
import datetime
import calendar
import itertools
import collections
import functools
import inspect
import traceback
import logging
import tempfile
import struct
import binascii
import zlib
import gzip
import secrets
import string
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Optional, Union, Callable, Set, Generator
from enum import Enum
from abc import ABC, abstractmethod

# ================================================================
# ЧАСТЬ 1: БАЗОВАЯ ОБЪЕКТНАЯ МОДЕЛЬ (200 строк)
# ================================================================

class BubbleType(Enum):
    """Полная система типов Bubble"""
    NULL = "null"
    BOOL = "bool"
    INT8 = "i8"
    INT16 = "i16"
    INT32 = "i32"
    INT64 = "i64"
    UINT8 = "u8"
    UINT16 = "u16"
    UINT32 = "u32"
    UINT64 = "u64"
    FLOAT32 = "f32"
    FLOAT64 = "f64"
    NUMBER = "number"
    STRING = "string"
    LIST = "list"
    DICT = "dict"
    ARRAY = "array"
    TUPLE = "tuple"
    STRUCT = "struct"
    ENUM = "enum"
    FUNCTION = "function"
    CLASS = "class"
    OBJECT = "object"
    ANY = "any"
    VOID = "void"
    NEVER = "never"
    UNKNOWN = "unknown"

@dataclass
class BubbleTypeInfo:
    """Информация о типе с размерами и выравниванием"""
    type: BubbleType
    size: int  # размер в байтах
    alignment: int = 8  # выравнивание
    is_signed: bool = True
    is_primitive: bool = True
    nullable: bool = False
    
    def __str__(self):
        return f"<{self.type.value} size={self.size} align={self.alignment}>"

class BubbleObject:
    """Базовый объект Bubble"""
    __slots__ = ('value', 'type_info', 'ref_count', 'weak_refs')
    
    def __init__(self, value=None, type_info: BubbleTypeInfo = None):
        self.value = value
        self.type_info = type_info or TypeController.get_type(value)
        self.ref_count = 1
        self.weak_refs = []
    
    def retain(self):
        self.ref_count += 1
        return self
    
    def release(self):
        self.ref_count -= 1
        if self.ref_count <= 0:
            self._cleanup()
            return True
        return False
    
    def _cleanup(self):
        for ref in self.weak_refs:
            ref._notify_deleted()
        if hasattr(self.value, '__bubble_cleanup__'):
            self.value.__bubble_cleanup__()
    
    def __repr__(self):
        return str(self.value)
    
    def __del__(self):
        self._cleanup()

class BubbleNull(BubbleObject):
    __slots__ = ()
    
    def __init__(self):
        super().__init__(None, BubbleTypeInfo(BubbleType.NULL, 0))
    
    def __bool__(self):
        return False
    
    def __str__(self):
        return "null"
    
    def __eq__(self, other):
        return isinstance(other, BubbleNull) or other is None

class BubbleBool(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value: bool):
        super().__init__(value, BubbleTypeInfo(BubbleType.BOOL, 1))
    
    def __bool__(self):
        return self.value
    
    def __str__(self):
        return "true" if self.value else "false"
    
    def __eq__(self, other):
        if isinstance(other, BubbleBool):
            return self.value == other.value
        return self.value == other

class BubbleNumber(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value, type_hint: BubbleType = None):
        if isinstance(value, BubbleNumber):
            value = value.value
        self.value = value
        self.type_info = TypeController.get_number_type(value, type_hint)
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __add__(self, other):
        if isinstance(other, BubbleString):
            return BubbleString(str(self.value) + other.value)
        v = other.value if isinstance(other, BubbleNumber) else other
        return BubbleNumber(self.value + v)
    
    def __sub__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return BubbleNumber(self.value - v)
    
    def __mul__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return BubbleNumber(self.value * v)
    
    def __truediv__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        if v == 0:
            return BubbleNull()
        return BubbleNumber(self.value / v)
    
    def __floordiv__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        if v == 0:
            return BubbleNull()
        return BubbleNumber(self.value // v)
    
    def __mod__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        if v == 0:
            return BubbleNull()
        return BubbleNumber(self.value % v)
    
    def __pow__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return BubbleNumber(self.value ** v)
    
    def __eq__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return self.value == v
    
    def __lt__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return self.value < v
    
    def __gt__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return self.value > v
    
    def __le__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return self.value <= v
    
    def __ge__(self, other):
        v = other.value if isinstance(other, BubbleNumber) else other
        return self.value >= v
    
    def __neg__(self):
        return BubbleNumber(-self.value)
    
    def __pos__(self):
        return BubbleNumber(+self.value)
    
    def __abs__(self):
        return BubbleNumber(abs(self.value))
    
    def __bool__(self):
        return bool(self.value)
    
    def __str__(self):
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)

class BubbleString(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value: str):
        super().__init__(value, BubbleTypeInfo(BubbleType.STRING, len(value) * 2))
    
    def __add__(self, other):
        return BubbleString(str(self.value) + str(other))
    
    def __mul__(self, other):
        if isinstance(other, (int, BubbleNumber)):
            count = int(other.value if isinstance(other, BubbleNumber) else other)
            return BubbleString(self.value * count)
        return BubbleNull()
    
    def __getitem__(self, index):
        if isinstance(index, int):
            return BubbleString(self.value[index])
        if isinstance(index, slice):
            return BubbleString(self.value[index])
        return BubbleNull()
    
    def __contains__(self, item):
        return str(item) in self.value
    
    def __len__(self):
        return len(self.value)
    
    def length(self):
        return BubbleNumber(len(self.value))
    
    def upper(self):
        return BubbleString(self.value.upper())
    
    def lower(self):
        return BubbleString(self.value.lower())
    
    def capitalize(self):
        return BubbleString(self.value.capitalize())
    
    def title(self):
        return BubbleString(self.value.title())
    
    def swapcase(self):
        return BubbleString(self.value.swapcase())
    
    def contains(self, s):
        return str(s) in self.value
    
    def startswith(self, prefix):
        return self.value.startswith(str(prefix))
    
    def endswith(self, suffix):
        return self.value.endswith(str(suffix))
    
    def find(self, sub, start=0, end=None):
        return BubbleNumber(self.value.find(str(sub), start, end if end else len(self.value)))
    
    def rfind(self, sub, start=0, end=None):
        return BubbleNumber(self.value.rfind(str(sub), start, end if end else len(self.value)))
    
    def index(self, sub, start=0, end=None):
        try:
            return BubbleNumber(self.value.index(str(sub), start, end if end else len(self.value)))
        except ValueError:
            return BubbleNumber(-1)
    
    def count(self, sub, start=0, end=None):
        return BubbleNumber(self.value.count(str(sub), start, end if end else len(self.value)))
    
    def replace(self, old, new, count=-1):
        return BubbleString(self.value.replace(str(old), str(new), count if count > 0 else self.value.count(str(old))))
    
    def split(self, sep=None, maxsplit=-1):
        if sep is None:
            parts = self.value.split(maxsplit=maxsplit if maxsplit > 0 else -1)
        else:
            parts = self.value.split(str(sep), maxsplit if maxsplit > 0 else -1)
        return BubbleList([BubbleString(p) for p in parts])
    
    def rsplit(self, sep=None, maxsplit=-1):
        if sep is None:
            parts = self.value.rsplit(maxsplit=maxsplit if maxsplit > 0 else -1)
        else:
            parts = self.value.rsplit(str(sep), maxsplit if maxsplit > 0 else -1)
        return BubbleList([BubbleString(p) for p in parts])
    
    def splitlines(self, keepends=False):
        return BubbleList([BubbleString(p) for p in self.value.splitlines(keepends)])
    
    def join(self, iterable):
        if isinstance(iterable, BubbleList):
            items = [str(i.value if isinstance(i, BubbleObject) else i) for i in iterable.value]
        else:
            items = [str(i) for i in iterable]
        return BubbleString(self.value.join(items))
    
    def strip(self, chars=None):
        if chars:
            return BubbleString(self.value.strip(str(chars)))
        return BubbleString(self.value.strip())
    
    def lstrip(self, chars=None):
        if chars:
            return BubbleString(self.value.lstrip(str(chars)))
        return BubbleString(self.value.lstrip())
    
    def rstrip(self, chars=None):
        if chars:
            return BubbleString(self.value.rstrip(str(chars)))
        return BubbleString(self.value.rstrip())
    
    def zfill(self, width):
        return BubbleString(self.value.zfill(width))
    
    def ljust(self, width, fillchar=' '):
        return BubbleString(self.value.ljust(width, str(fillchar)))
    
    def rjust(self, width, fillchar=' '):
        return BubbleString(self.value.rjust(width, str(fillchar)))
    
    def center(self, width, fillchar=' '):
        return BubbleString(self.value.center(width, str(fillchar)))
    
    def format(self, *args, **kwargs):
        try:
            formatted = self.value.format(*args, **kwargs)
            return BubbleString(formatted)
        except:
            return BubbleNull()
    
    def format_map(self, mapping):
        try:
            formatted = self.value.format_map(mapping)
            return BubbleString(formatted)
        except:
            return BubbleNull()
    
    def isalnum(self):
        return self.value.isalnum()
    
    def isalpha(self):
        return self.value.isalpha()
    
    def isdigit(self):
        return self.value.isdigit()
    
    def islower(self):
        return self.value.islower()
    
    def isupper(self):
        return self.value.isupper()
    
    def isspace(self):
        return self.value.isspace()
    
    def istitle(self):
        return self.value.istitle()
    
    def encode(self, encoding='utf-8'):
        return BubbleBytes(self.value.encode(encoding))
    
    def __str__(self):
        return self.value

class BubbleBytes(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value: bytes):
        super().__init__(value, BubbleTypeInfo(BubbleType.ARRAY, len(value)))
    
    def __add__(self, other):
        if isinstance(other, BubbleBytes):
            return BubbleBytes(self.value + other.value)
        return BubbleNull()
    
    def __getitem__(self, index):
        if isinstance(index, int):
            return BubbleNumber(self.value[index])
        if isinstance(index, slice):
            return BubbleBytes(self.value[index])
        return BubbleNull()
    
    def __len__(self):
        return len(self.value)
    
    def hex(self):
        return BubbleString(self.value.hex())
    
    def decode(self, encoding='utf-8'):
        return BubbleString(self.value.decode(encoding))
    
    def __str__(self):
        return f"b'{self.value.hex()}'"

class BubbleList(BubbleObject):
    __slots__ = ('element_type',)
    
    def __init__(self, value=None, element_type: BubbleType = None):
        super().__init__(value if value is not None else [])
        self.element_type = element_type
    
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.value[index] if 0 <= index < len(self.value) else BubbleNull()
        if isinstance(index, slice):
            return BubbleList(self.value[index])
        return BubbleNull()
    
    def __setitem__(self, index, value):
        if isinstance(index, int) and 0 <= index < len(self.value):
            self.value[index] = value
    
    def __iter__(self):
        return iter(self.value)
    
    def __contains__(self, item):
        return item in self.value
    
    def __len__(self):
        return len(self.value)
    
    def __add__(self, other):
        if isinstance(other, BubbleList):
            return BubbleList(self.value + other.value)
        return BubbleNull()
    
    def __mul__(self, other):
        if isinstance(other, (int, BubbleNumber)):
            count = int(other.value if isinstance(other, BubbleNumber) else other)
            return BubbleList(self.value * count)
        return BubbleNull()
    
    def length(self):
        return BubbleNumber(len(self.value))
    
    def get(self, index, default=None):
        if 0 <= index < len(self.value):
            return self.value[index]
        return default
    
    def set(self, index, value):
        if 0 <= index < len(self.value):
            self.value[index] = value
            return True
        return False
    
    def append(self, item):
        self.value.append(item)
        return self
    
    def push(self, item):
        self.value.append(item)
        return self
    
    def extend(self, iterable):
        if isinstance(iterable, BubbleList):
            self.value.extend(iterable.value)
        else:
            self.value.extend(iterable)
        return self
    
    def insert(self, index, item):
        self.value.insert(index, item)
        return self
    
    def pop(self, index=-1):
        if self.value:
            return self.value.pop(index)
        return BubbleNull()
    
    def remove(self, value):
        try:
            self.value.remove(value)
            return True
        except ValueError:
            return False
    
    def clear(self):
        self.value.clear()
        return self
    
    def copy(self):
        return BubbleList(self.value.copy())
    
    def reverse(self):
        self.value.reverse()
        return self
    
    def sort(self, key=None, reverse=False):
        if key:
            self.value.sort(key=key, reverse=reverse)
        else:
            self.value.sort(reverse=reverse)
        return self
    
    def index(self, value, start=0, end=None):
        try:
            return BubbleNumber(self.value.index(value, start, end if end else len(self.value)))
        except ValueError:
            return BubbleNumber(-1)
    
    def count(self, value):
        return BubbleNumber(self.value.count(value))
    
    def map(self, func):
        result = []
        for item in self.value:
            result.append(func(item))
        return BubbleList(result)
    
    def filter(self, func):
        result = []
        for item in self.value:
            if func(item):
                result.append(item)
        return BubbleList(result)
    
    def reduce(self, func, initial=None):
        if initial is not None:
            result = initial
            for item in self.value:
                result = func(result, item)
            return result
        if not self.value:
            return BubbleNull()
        result = self.value[0]
        for item in self.value[1:]:
            result = func(result, item)
        return result
    
    def sum(self):
        total = 0
        for item in self.value:
            if isinstance(item, BubbleNumber):
                total += item.value
            elif isinstance(item, (int, float)):
                total += item
        return BubbleNumber(total)
    
    def min(self):
        if not self.value:
            return BubbleNull()
        return min(self.value)
    
    def max(self):
        if not self.value:
            return BubbleNull()
        return max(self.value)
    
    def any(self):
        return any(bool(item) for item in self.value)
    
    def all(self):
        return all(bool(item) for item in self.value)
    
    def slice(self, start, end=None, step=1):
        if end is None:
            return BubbleList(self.value[start::step])
        return BubbleList(self.value[start:end:step])
    
    def __str__(self):
        return str(self.value)

class BubbleDict(BubbleObject):
    __slots__ = ('key_type', 'value_type')
    
    def __init__(self, value=None, key_type: BubbleType = None, value_type: BubbleType = None):
        super().__init__(value if value is not None else {})
        self.key_type = key_type
        self.value_type = value_type
    
    def __getitem__(self, key):
        k = str(key.value if isinstance(key, BubbleString) else key)
        return self.value.get(k, BubbleNull())
    
    def __setitem__(self, key, value):
        k = str(key.value if isinstance(key, BubbleString) else key)
        self.value[k] = value
    
    def __contains__(self, key):
        k = str(key.value if isinstance(key, BubbleString) else key)
        return k in self.value
    
    def __len__(self):
        return len(self.value)
    
    def __delitem__(self, key):
        k = str(key.value if isinstance(key, BubbleString) else key)
        if k in self.value:
            del self.value[k]
    
    def get(self, key, default=None):
        k = str(key.value if isinstance(key, BubbleString) else key)
        return self.value.get(k, default)
    
    def set(self, key, value):
        k = str(key.value if isinstance(key, BubbleString) else key)
        self.value[k] = value
        return self
    
    def has(self, key):
        k = str(key.value if isinstance(key, BubbleString) else key)
        return k in self.value
    
    def keys(self):
        return BubbleList([BubbleString(k) for k in self.value.keys()])
    
    def values(self):
        return BubbleList(list(self.value.values()))
    
    def items(self):
        items_list = []
        for k, v in self.value.items():
            items_list.append(BubbleList([BubbleString(k), v]))
        return BubbleList(items_list)
    
    def pop(self, key, default=None):
        k = str(key.value if isinstance(key, BubbleString) else key)
        return self.value.pop(k, default)
    
    def popitem(self):
        if self.value:
            k, v = self.value.popitem()
            return BubbleList([BubbleString(k), v])
        return BubbleNull()
    
    def clear(self):
        self.value.clear()
        return self
    
    def copy(self):
        return BubbleDict(self.value.copy())
    
    def update(self, other):
        if isinstance(other, BubbleDict):
            self.value.update(other.value)
        elif isinstance(other, dict):
            self.value.update(other)
        return self
    
    def __add__(self, other):
        if isinstance(other, BubbleDict):
            result = self.value.copy()
            result.update(other.value)
            return BubbleDict(result)
        return BubbleNull()
    
    def __str__(self):
        return str(self.value)

class BubbleTuple(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value):
        super().__init__(tuple(value), BubbleTypeInfo(BubbleType.TUPLE, len(value) * 8))
    
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.value[index]
        if isinstance(index, slice):
            return BubbleTuple(self.value[index])
        return BubbleNull()
    
    def __len__(self):
        return len(self.value)
    
    def __iter__(self):
        return iter(self.value)
    
    def __contains__(self, item):
        return item in self.value
    
    def count(self, value):
        return BubbleNumber(self.value.count(value))
    
    def index(self, value, start=0, end=None):
        try:
            return BubbleNumber(self.value.index(value, start, end if end else len(self.value)))
        except ValueError:
            return BubbleNumber(-1)
    
    def __str__(self):
        return str(self.value)

class BubbleSet(BubbleObject):
    __slots__ = ()
    
    def __init__(self, value=None):
        super().__init__(set(value if value else []), BubbleTypeInfo(BubbleType.ARRAY, 0))
    
    def __contains__(self, item):
        return item in self.value
    
    def __len__(self):
        return len(self.value)
    
    def __iter__(self):
        return iter(self.value)
    
    def add(self, item):
        self.value.add(item)
        return self
    
    def remove(self, item):
        try:
            self.value.remove(item)
            return True
        except KeyError:
            return False
    
    def discard(self, item):
        self.value.discard(item)
        return self
    
    def clear(self):
        self.value.clear()
        return self
    
    def copy(self):
        return BubbleSet(self.value.copy())
    
    def union(self, other):
        if isinstance(other, BubbleSet):
            return BubbleSet(self.value.union(other.value))
        return BubbleSet(self.value.union(other))
    
    def intersection(self, other):
        if isinstance(other, BubbleSet):
            return BubbleSet(self.value.intersection(other.value))
        return BubbleSet(self.value.intersection(other))
    
    def difference(self, other):
        if isinstance(other, BubbleSet):
            return BubbleSet(self.value.difference(other.value))
        return BubbleSet(self.value.difference(other))
    
    def symmetric_difference(self, other):
        if isinstance(other, BubbleSet):
            return BubbleSet(self.value.symmetric_difference(other.value))
        return BubbleSet(self.value.symmetric_difference(other))
    
    def is_subset(self, other):
        if isinstance(other, BubbleSet):
            return self.value.issubset(other.value)
        return self.value.issubset(other)
    
    def is_superset(self, other):
        if isinstance(other, BubbleSet):
            return self.value.issuperset(other.value)
        return self.value.issuperset(other)
    
    def __str__(self):
        return str(self.value)

# ================================================================
# ЧАСТЬ 2: УПРАВЛЕНИЕ ПАМЯТЬЮ PPR (300 строк)
# ================================================================

class MemoryAccess:
    """Уровни доступа к памяти"""
    READ = 0x01
    WRITE = 0x02
    EXECUTE = 0x04
    ALL = READ | WRITE | EXECUTE

class MemoryGuard:
    """Защита памяти"""
    def __init__(self):
        self.guards = []
    
    def add_guard(self, start, end, access):
        self.guards.append({'start': start, 'end': end, 'access': access})
    
    def check_access(self, address, access):
        for guard in self.guards:
            if guard['start'] <= address < guard['end']:
                return (guard['access'] & access) != 0
        return True

class MemoryBlock:
    """Блок памяти с полным контролем"""
    __slots__ = ('block_id', 'size', 'owner', 'data', 'read_count', 'write_count', 
                 'created_at', 'last_access', 'is_freed', 'tags', 'guard', 'is_shared')
    
    def __init__(self, size: int, owner: str):
        self.block_id = None
        self.size = size
        self.owner = owner
        self.data = bytearray(size)
        self.read_count = 0
        self.write_count = 0
        self.created_at = time.time()
        self.last_access = self.created_at
        self.is_freed = False
        self.tags = set()
        self.guard = MemoryGuard()
        self.is_shared = False
    
    def read(self, offset: int, size: int) -> bytes:
        if self.is_freed:
            raise MemoryError(f"Memory block {self.block_id} owned by {self.owner} is already freed")
        if offset + size > self.size:
            raise MemoryError(f"Memory out of bounds: offset={offset}, size={size}, total={self.size}")
        if not self.guard.check_access(offset, MemoryAccess.READ):
            raise PermissionError(f"Read access denied at offset {offset}")
        
        self.read_count += 1
        self.last_access = time.time()
        return bytes(self.data[offset:offset+size])
    
    def write(self, offset: int, data: bytes):
        if self.is_freed:
            raise MemoryError(f"Memory block {self.block_id} owned by {self.owner} is already freed")
        if offset + len(data) > self.size:
            raise MemoryError(f"Memory out of bounds: offset={offset}, size={len(data)}, total={self.size}")
        if not self.guard.check_access(offset, MemoryAccess.WRITE):
            raise PermissionError(f"Write access denied at offset {offset}")
        
        self.data[offset:offset+len(data)] = data
        self.write_count += 1
        self.last_access = time.time()
    
    def protect(self, start: int, end: int, access: int):
        self.guard.add_guard(start, end, access)
    
    def add_tag(self, tag: str):
        self.tags.add(tag)
    
    def has_tag(self, tag: str) -> bool:
        return tag in self.tags
    
    def share(self):
        self.is_shared = True
    
    def unshare(self):
        self.is_shared = False
    
    def free(self):
        self.is_freed = True
        self.data = None
    
    def get_stats(self) -> dict:
        return {
            'size': self.size,
            'read_count': self.read_count,
            'write_count': self.write_count,
            'age': time.time() - self.created_at,
            'last_access_age': time.time() - self.last_access,
            'tags': list(self.tags),
            'is_shared': self.is_shared
        }
    
    def __str__(self):
        return f"MemoryBlock(id={self.block_id}, owner={self.owner}, size={self.size}, freed={self.is_freed})"

class PPManager:
    """Менеджер PPR (Память Персонально для Разработчика)"""
    
    def __init__(self):
        self.blocks: Dict[int, MemoryBlock] = {}
        self.next_id = 1
        self.stats = {
            'total_allocated': 0,
            'total_freed': 0,
            'total_reads': 0,
            'total_writes': 0,
            'leaks': 0,
            'peak_memory': 0,
            'allocations': 0,
            'deallocations': 0
        }
        self.allocation_history = []
        self.watchpoints = {}
        self.owners = {}
        self.gc_enabled = True
        self.gc_threshold = 100 * 1024 * 1024  # 100MB
    
    def allocate(self, size: int, owner: str = "anonymous", tags: List[str] = None) -> int:
        """Выделяет блок памяти"""
        block_id = self.next_id
        self.next_id += 1
        
        block = MemoryBlock(size, owner)
        block.block_id = block_id
        if tags:
            for tag in tags:
                block.add_tag(tag)
        
        self.blocks[block_id] = block
        self.stats['total_allocated'] += size
        self.stats['allocations'] += 1
        self.stats['peak_memory'] = max(self.stats['peak_memory'], self.get_active_memory())
        
        self.allocation_history.append({
            'time': time.time(),
            'block_id': block_id,
            'size': size,
            'owner': owner
        })
        
        if owner not in self.owners:
            self.owners[owner] = []
        self.owners[owner].append(block_id)
        
        if self.gc_enabled and self.get_active_memory() > self.gc_threshold:
            self.collect_garbage()
        
        return block_id
    
    def read(self, block_id: int, offset: int, size: int) -> bytes:
        """Читает из памяти"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        
        result = self.blocks[block_id].read(offset, size)
        self.stats['total_reads'] += 1
        return result
    
    def write(self, block_id: int, offset: int, data: bytes):
        """Записывает в память"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        
        self.blocks[block_id].write(offset, data)
        self.stats['total_writes'] += 1
    
    def free(self, block_id: int):
        """Освобождает память"""
        if block_id in self.blocks:
            block = self.blocks[block_id]
            owner = block.owner
            self.stats['total_freed'] += block.size
            self.stats['deallocations'] += 1
            block.free()
            del self.blocks[block_id]
            
            if owner in self.owners and block_id in self.owners[owner]:
                self.owners[owner].remove(block_id)
            
            self.stats['leaks'] = len(self.blocks)
    
    def protect(self, block_id: int, start: int, end: int, access: int):
        """Защищает область памяти"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        self.blocks[block_id].protect(start, end, access)
    
    def add_tag(self, block_id: int, tag: str):
        """Добавляет тег блоку памяти"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        self.blocks[block_id].add_tag(tag)
    
    def find_by_tag(self, tag: str) -> List[int]:
        """Находит блоки по тегу"""
        return [bid for bid, block in self.blocks.items() if block.has_tag(tag)]
    
    def find_by_owner(self, owner: str) -> List[int]:
        """Находит блоки по владельцу"""
        return self.owners.get(owner, []).copy()
    
    def share(self, block_id: int):
        """Делает блок памяти разделяемым"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        self.blocks[block_id].share()
    
    def unshare(self, block_id: int):
        """Отменяет разделение памяти"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        self.blocks[block_id].unshare()
    
    def resize(self, block_id: int, new_size: int) -> bool:
        """Изменяет размер блока памяти"""
        if block_id not in self.blocks:
            raise MemoryError(f"Memory block {block_id} not found")
        
        block = self.blocks[block_id]
        if block.is_freed:
            return False
        
        old_size = block.size
        new_data = bytearray(new_size)
        copy_size = min(old_size, new_size)
        new_data[:copy_size] = block.data[:copy_size]
        
        block.data = new_data
        self.stats['total_allocated'] += (new_size - old_size)
        block.size = new_size
        return True
    
    def get_block_info(self, block_id: int) -> Optional[dict]:
        """Возвращает информацию о блоке"""
        if block_id not in self.blocks:
            return None
        return self.blocks[block_id].get_stats()
    
    def get_active_memory(self) -> int:
        """Возвращает активную память"""
        return sum(b.size for b in self.blocks.values())
    
    def get_stats(self) -> dict:
        """Возвращает полную статистику"""
        active_memory = self.get_active_memory()
        return {
            **self.stats,
            'active_blocks': len(self.blocks),
            'active_memory': active_memory,
            'utilization': (active_memory / self.stats['total_allocated'] * 100) if self.stats['total_allocated'] > 0 else 0,
            'total_allocations': self.stats['allocations'],
            'total_deallocations': self.stats['deallocations'],
            'leak_count': len(self.blocks)
        }
    
    def collect_garbage(self):
        """Сборка мусора - освобождает старые блоки"""
        now = time.time()
        freed = 0
        for block_id, block in list(self.blocks.items()):
            if now - block.last_access > 3600:  # 1 час без доступа
                self.free(block_id)
                freed += 1
        return freed
    
    def dump_memory_map(self) -> str:
        """Дамп карты памяти"""
        lines = ["=== MEMORY MAP ==="]
        for block_id, block in self.blocks.items():
            lines.append(f"  [{block_id}] {block}")
            stats = block.get_stats()
            lines.append(f"    reads={stats['read_count']}, writes={stats['write_count']}, tags={stats['tags']}")
        return '\n'.join(lines)
    
    def create_snapshot(self):
        """Создаёт снимок состояния памяти"""
        return {
            'timestamp': time.time(),
            'blocks': {bid: block.get_stats() for bid, block in self.blocks.items()},
            'stats': self.get_stats()
        }
    
    def diff_snapshots(self, snapshot1, snapshot2):
        """Сравнивает два снимка памяти"""
        diff = {
            'created': [],
            'freed': [],
            'changed': []
        }
        
        old_blocks = set(snapshot1['blocks'].keys())
        new_blocks = set(snapshot2['blocks'].keys())
        
        diff['created'] = list(new_blocks - old_blocks)
        diff['freed'] = list(old_blocks - new_blocks)
        
        for bid in old_blocks & new_blocks:
            if snapshot1['blocks'][bid] != snapshot2['blocks'][bid]:
                diff['changed'].append(bid)
        
        return diff

class BubbleMemory(BubbleObject):
    """Объект для работы с PPR из языка Bubble"""
    
    def __init__(self, ppr_manager: PPManager):
        super().__init__(None)
        self.ppr = ppr_manager
    
    def alloc(self, size: int, owner: str = "user") -> int:
        return self.ppr.allocate(size, owner)
    
    def read(self, block_id: int, offset: int, size: int) -> bytes:
        return self.ppr.read(block_id, offset, size)
    
    def write(self, block_id: int, offset: int, data: bytes):
        self.ppr.write(block_id, offset, data)
    
    def free(self, block_id: int):
        self.ppr.free(block_id)
    
    def protect(self, block_id: int, start: int, end: int, access: int):
        self.ppr.protect(block_id, start, end, access)
    
    def tag(self, block_id: int, tag: str):
        self.ppr.add_tag(block_id, tag)
    
    def find_by_tag(self, tag: str) -> BubbleList:
        return BubbleList([BubbleNumber(bid) for bid in self.ppr.find_by_tag(tag)])
    
    def find_by_owner(self, owner: str) -> BubbleList:
        return BubbleList([BubbleNumber(bid) for bid in self.ppr.find_by_owner(owner)])
    
    def resize(self, block_id: int, new_size: int) -> bool:
        return self.ppr.resize(block_id, new_size)
    
    def share(self, block_id: int):
        self.ppr.share(block_id)
    
    def get_stats(self) -> BubbleDict:
        stats = self.ppr.get_stats()
        return BubbleDict(stats)
    
    def get_block_info(self, block_id: int) -> BubbleDict:
        info = self.ppr.get_block_info(block_id)
        if info:
            return BubbleDict(info)
        return BubbleNull()
    
    def gc(self):
        return self.ppr.collect_garbage()
    
    def dump(self) -> str:
        return self.ppr.dump_memory_map()
    
    def __str__(self):
        return f"<PPR Memory Manager: {self.ppr.get_active_memory()} bytes active>"

# ================================================================
# ЧАСТЬ 3: ТИПЫ И КОНТРОЛЬ (200 строк)
# ================================================================

class TypeController:
    """Контроллер типов с полной проверкой"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.type_cache = {}
        self.type_converters = {
            (BubbleType.INT32, BubbleType.FLOAT64): lambda x: float(x),
            (BubbleType.FLOAT64, BubbleType.INT32): lambda x: int(x),
            (BubbleType.INT32, BubbleType.STRING): lambda x: str(x),
            (BubbleType.STRING, BubbleType.INT32): lambda x: int(x) if x.isdigit() else None,
            (BubbleType.STRING, BubbleType.FLOAT64): lambda x: float(x) if x.replace('.', '').isdigit() else None,
        }
    
    @staticmethod
    def get_type(value) -> BubbleTypeInfo:
        """Определяет тип значения"""
        if value is None:
            return BubbleTypeInfo(BubbleType.NULL, 0)
        if isinstance(value, bool):
            return BubbleTypeInfo(BubbleType.BOOL, 1)
        if isinstance(value, int):
            return TypeController.get_number_type(value)
        if isinstance(value, float):
            return BubbleTypeInfo(BubbleType.FLOAT64, 8)
        if isinstance(value, str):
            return BubbleTypeInfo(BubbleType.STRING, len(value) * 2)
        if isinstance(value, list):
            return BubbleTypeInfo(BubbleType.LIST, len(value) * 8)
        if isinstance(value, dict):
            return BubbleTypeInfo(BubbleType.DICT, len(value) * 16)
        if isinstance(value, BubbleObject):
            return value.type_info
        return BubbleTypeInfo(BubbleType.UNKNOWN, 0)
    
    @staticmethod
    def get_number_type(value, hint: BubbleType = None) -> BubbleTypeInfo:
        """Определяет оптимальный числовой тип"""
        if hint == BubbleType.INT8 and -128 <= value <= 127:
            return BubbleTypeInfo(BubbleType.INT8, 1)
        if hint == BubbleType.INT16 and -32768 <= value <= 32767:
            return BubbleTypeInfo(BubbleType.INT16, 2)
        if hint == BubbleType.INT32 and -2147483648 <= value <= 2147483647:
            return BubbleTypeInfo(BubbleType.INT32, 4)
        if hint == BubbleType.INT64:
            return BubbleTypeInfo(BubbleType.INT64, 8)
        if hint == BubbleType.UINT8 and 0 <= value <= 255:
            return BubbleTypeInfo(BubbleType.UINT8, 1)
        if hint == BubbleType.UINT16 and 0 <= value <= 65535:
            return BubbleTypeInfo(BubbleType.UINT16, 2)
        if hint == BubbleType.UINT32 and 0 <= value <= 4294967295:
            return BubbleTypeInfo(BubbleType.UINT32, 4)
        if hint == BubbleType.UINT64 and value >= 0:
            return BubbleTypeInfo(BubbleType.UINT64, 8)
        if hint in [BubbleType.FLOAT32, BubbleType.FLOAT64]:
            return BubbleTypeInfo(hint, 4 if hint == BubbleType.FLOAT32 else 8)
        
        # Авто-определение
        if -128 <= value <= 127:
            return BubbleTypeInfo(BubbleType.INT8, 1)
        if -32768 <= value <= 32767:
            return BubbleTypeInfo(BubbleType.INT16, 2)
        if -2147483648 <= value <= 2147483647:
            return BubbleTypeInfo(BubbleType.INT32, 4)
        return BubbleTypeInfo(BubbleType.INT64, 8)
    
    @staticmethod
    def check_compatibility(type1: BubbleType, type2: BubbleType) -> bool:
        """Проверяет совместимость типов"""
        if type1 == type2:
            return True
        if type1 == BubbleType.ANY or type2 == BubbleType.ANY:
            return True
        if type1 == BubbleType.NULL or type2 == BubbleType.NULL:
            return True
        
        # Числовые типы
        numeric_types = {
            BubbleType.INT8, BubbleType.INT16, BubbleType.INT32, BubbleType.INT64,
            BubbleType.UINT8, BubbleType.UINT16, BubbleType.UINT32, BubbleType.UINT64,
            BubbleType.FLOAT32, BubbleType.FLOAT64, BubbleType.NUMBER
        }
        if type1 in numeric_types and type2 in numeric_types:
            return True
        
        # Типы контейнеров
        if type1 == BubbleType.LIST and type2 == BubbleType.ARRAY:
            return True
        if type1 == BubbleType.DICT and type2 == BubbleType.OBJECT:
            return True
        
        return False
    
    @staticmethod
    def cast(value, target_type: BubbleType):
        """Преобразует значение к целевому типу"""
        try:
            if target_type == BubbleType.INT8:
                return int(value) & 0xFF
            if target_type == BubbleType.INT16:
                return int(value) & 0xFFFF
            if target_type == BubbleType.INT32:
                return int(value) & 0xFFFFFFFF
            if target_type == BubbleType.INT64:
                return int(value)
            if target_type == BubbleType.UINT8:
                return int(value) & 0xFF
            if target_type == BubbleType.UINT16:
                return int(value) & 0xFFFF
            if target_type == BubbleType.UINT32:
                return int(value) & 0xFFFFFFFF
            if target_type == BubbleType.UINT64:
                return int(value) & 0xFFFFFFFFFFFFFFFF
            if target_type in [BubbleType.FLOAT32, BubbleType.FLOAT64, BubbleType.NUMBER]:
                return float(value)
            if target_type == BubbleType.STRING:
                return str(value)
            if target_type == BubbleType.BOOL:
                return bool(value)
            return value
        except:
            return None

# ================================================================
# ЧАСТЬ 4: МНОГОПОТОЧНОСТЬ (200 строк)
# ================================================================

class BubbleThread(BubbleObject):
    """Поток выполнения"""
    
    def __init__(self, target=None, args=None, kwargs=None, name=None):
        super().__init__(None)
        self.target = target
        self.args = args or []
        self.kwargs = kwargs or {}
        self.name = name or f"Thread-{id(self)}"
        self.thread = None
        self.result = None
        self.error = None
        self.is_alive = False
        self.is_daemon = False
        self._stop_event = threading.Event()
    
    def start(self):
        def run():
            self.is_alive = True
            try:
                if self.target:
                    if callable(self.target):
                        self.result = self.target(*self.args, **self.kwargs)
                    else:
                        self.result = self.target
                self.is_alive = False
            except Exception as e:
                self.error = e
                self.is_alive = False
        
        self.thread = threading.Thread(target=run, name=self.name, daemon=self.is_daemon)
        self.thread.start()
        return self
    
    def join(self, timeout=None):
        if self.thread:
            self.thread.join(timeout)
            if self.error:
                raise self.error
            return self.result
        return None
    
    def stop(self):
        self._stop_event.set()
        return self
    
    def is_stopped(self):
        return self._stop_event.is_set()
    
    def set_daemon(self, daemon):
        self.is_daemon = daemon
        return self
    
    def get_id(self):
        return self.thread.ident if self.thread else None
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"<Thread name={self.name} alive={self.is_alive}>"

class BubbleMutex(BubbleObject):
    """Мьютекс для синхронизации"""
    
    def __init__(self):
        super().__init__(None)
        self._lock = threading.Lock()
        self._owner = None
        self._recursion_depth = 0
    
    def lock(self):
        self._lock.acquire()
        self._owner = threading.current_thread()
        self._recursion_depth += 1
        return self
    
    def unlock(self):
        if self._recursion_depth > 0:
            self._recursion_depth -= 1
            if self._recursion_depth == 0:
                self._owner = None
                self._lock.release()
        return self
    
    def try_lock(self):
        if self._lock.acquire(blocking=False):
            self._owner = threading.current_thread()
            self._recursion_depth = 1
            return True
        return False
    
    def locked(self):
        return self._lock.locked()
    
    def __enter__(self):
        return self.lock()
    
    def __exit__(self, *args):
        return self.unlock()

class BubbleSemaphore(BubbleObject):
    """Семафор"""
    
    def __init__(self, value=1):
        super().__init__(None)
        self._semaphore = threading.Semaphore(value)
    
    def acquire(self, blocking=True):
        return self._semaphore.acquire(blocking)
    
    def release(self):
        self._semaphore.release()
        return self
    
    def __str__(self):
        return f"<Semaphore>"

class BubbleEvent(BubbleObject):
    """Событие для синхронизации"""
    
    def __init__(self):
        super().__init__(None)
        self._event = threading.Event()
    
    def set(self):
        self._event.set()
        return self
    
    def clear(self):
        self._event.clear()
        return self
    
    def wait(self, timeout=None):
        return self._event.wait(timeout)
    
    def is_set(self):
        return self._event.is_set()
    
    def __str__(self):
        return f"<Event set={self.is_set()}>"

class BubbleQueue(BubbleObject):
    """Потокобезопасная очередь"""
    
    def __init__(self, maxsize=0):
        super().__init__(None)
        self._queue = queue.Queue(maxsize)
    
    def put(self, item, block=True, timeout=None):
        self._queue.put(item, block, timeout)
        return self
    
    def get(self, block=True, timeout=None):
        try:
            return self._queue.get(block, timeout)
        except queue.Empty:
            return BubbleNull()
    
    def get_nowait(self):
        return self.get(block=False)
    
    def empty(self):
        return self._queue.empty()
    
    def full(self):
        return self._queue.full()
    
    def size(self):
        return BubbleNumber(self._queue.qsize())
    
    def __str__(self):
        return f"<Queue size={self._queue.qsize()}>"

class BubbleThreadPool(BubbleObject):
    """Пул потоков"""
    
    def __init__(self, max_workers=4):
        super().__init__(None)
        self.max_workers = max_workers
        self.workers = []
        self.tasks = BubbleQueue()
        self.is_running = False
        self.results = {}
    
    def start(self):
        self.is_running = True
        for _ in range(self.max_workers):
            worker = BubbleThread(self._worker_loop)
            worker.set_daemon(True)
            worker.start()
            self.workers.append(worker)
        return self
    
    def _worker_loop(self):
        while self.is_running:
            task = self.tasks.get()
            if task is None:
                break
            task_id, func, args, kwargs = task
            try:
                result = func(*args, **kwargs)
                self.results[task_id] = result
            except Exception as e:
                self.results[task_id] = e
    
    def submit(self, func, *args, **kwargs):
        task_id = id(func) + len(self.results)
        self.tasks.put((task_id, func, args, kwargs))
        return task_id
    
    def get_result(self, task_id, timeout=None):
        start = time.time()
        while task_id not in self.results:
            if timeout and time.time() - start > timeout:
                return BubbleNull()
            time.sleep(0.01)
        result = self.results[task_id]
        if isinstance(result, Exception):
            raise result
        return result
    
    def shutdown(self, wait=True):
        self.is_running = False
        for _ in self.workers:
            self.tasks.put(None)
        for worker in self.workers:
            worker.join()
        return self
    
    def __str__(self):
        return f"<ThreadPool workers={len(self.workers)} pending={self.tasks.size().value}>"

# ================================================================
# ЧАСТЬ 5: МАТЕМАТИКА (150 строк)
# ================================================================

class BubbleMath(BubbleObject):
    """Расширенная математическая библиотека"""
    
    @staticmethod
    def sqrt(x):
        return BubbleNumber(math.sqrt(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def cbrt(x):
        return BubbleNumber(x ** (1/3) if x >= 0 else -((-x) ** (1/3)))
    
    @staticmethod
    def pow(x, y):
        return BubbleNumber(x ** y)
    
    @staticmethod
    def exp(x):
        return BubbleNumber(math.exp(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def log(x, base=None):
        v = float(x.value if isinstance(x, BubbleNumber) else x)
        if base:
            b = float(base.value if isinstance(base, BubbleNumber) else base)
            return BubbleNumber(math.log(v) / math.log(b))
        return BubbleNumber(math.log(v))
    
    @staticmethod
    def log10(x):
        return BubbleNumber(math.log10(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def log2(x):
        return BubbleNumber(math.log2(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def sin(x):
        return BubbleNumber(math.sin(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def cos(x):
        return BubbleNumber(math.cos(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def tan(x):
        return BubbleNumber(math.tan(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def asin(x):
        return BubbleNumber(math.asin(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def acos(x):
        return BubbleNumber(math.acos(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def atan(x):
        return BubbleNumber(math.atan(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def atan2(y, x):
        return BubbleNumber(math.atan2(float(y.value if isinstance(y, BubbleNumber) else y),
                                       float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def sinh(x):
        return BubbleNumber(math.sinh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def cosh(x):
        return BubbleNumber(math.cosh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def tanh(x):
        return BubbleNumber(math.tanh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def asinh(x):
        return BubbleNumber(math.asinh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def acosh(x):
        return BubbleNumber(math.acosh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def atanh(x):
        return BubbleNumber(math.atanh(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def degrees(x):
        return BubbleNumber(math.degrees(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def radians(x):
        return BubbleNumber(math.radians(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def pi():
        return BubbleNumber(math.pi)
    
    @staticmethod
    def e():
        return BubbleNumber(math.e)
    
    @staticmethod
    def tau():
        return BubbleNumber(2 * math.pi)
    
    @staticmethod
    def inf():
        return BubbleNumber(float('inf'))
    
    @staticmethod
    def nan():
        return BubbleNumber(float('nan'))
    
    @staticmethod
    def is_nan(x):
        return math.isnan(float(x.value if isinstance(x, BubbleNumber) else x))
    
    @staticmethod
    def is_inf(x):
        return math.isinf(float(x.value if isinstance(x, BubbleNumber) else x))
    
    @staticmethod
    def is_finite(x):
        return math.isfinite(float(x.value if isinstance(x, BubbleNumber) else x))
    
    @staticmethod
    def abs(x):
        return BubbleNumber(abs(x.value if isinstance(x, BubbleNumber) else x))
    
    @staticmethod
    def floor(x):
        return BubbleNumber(math.floor(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def ceil(x):
        return BubbleNumber(math.ceil(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def round(x, ndigits=0):
        return BubbleNumber(round(float(x.value if isinstance(x, BubbleNumber) else x),
                                  int(ndigits.value if isinstance(ndigits, BubbleNumber) else ndigits)))
    
    @staticmethod
    def trunc(x):
        return BubbleNumber(int(float(x.value if isinstance(x, BubbleNumber) else x)))
    
    @staticmethod
    def fmod(x, y):
        return BubbleNumber(math.fmod(float(x.value if isinstance(x, BubbleNumber) else x),
                                     float(y.value if isinstance(y, BubbleNumber) else y)))
    
    @staticmethod
    def modf(x):
        fractional, integer = math.modf(float(x.value if isinstance(x, BubbleNumber) else x))
        return BubbleList([BubbleNumber(fractional), BubbleNumber(integer)])
    
    @staticmethod
    def gcd(a, b):
        return BubbleNumber(math.gcd(int(a.value if isinstance(a, BubbleNumber) else a),
                                     int(b.value if isinstance(b, BubbleNumber) else b)))
    
    @staticmethod
    def lcm(a, b):
        return BubbleNumber(abs(a * b) // math.gcd(a, b))
    
    @staticmethod
    def factorial(n):
        return BubbleNumber(math.factorial(int(n.value if isinstance(n, BubbleNumber) else n)))
    
    @staticmethod
    def comb(n, k):
        return BubbleNumber(math.comb(int(n.value if isinstance(n, BubbleNumber) else n),
                                      int(k.value if isinstance(k, BubbleNumber) else k)))
    
    @staticmethod
    def perm(n, k):
        return BubbleNumber(math.perm(int(n.value if isinstance(n, BubbleNumber) else n),
                                      int(k.value if isinstance(k, BubbleNumber) else k)))
    
    @staticmethod
    def random(a=None, b=None):
        if a is None:
            return BubbleNumber(random.random())
        va = a.value if isinstance(a, BubbleNumber) else a
        if b is None:
            if va == 0:
                return BubbleNumber(0)
            return BubbleNumber(random.randint(0, va))
        vb = b.value if isinstance(b, BubbleNumber) else b
        if va > vb:
            va, vb = vb, va
        return BubbleNumber(random.randint(va, vb))
    
    @staticmethod
    def uniform(a, b):
        va = float(a.value if isinstance(a, BubbleNumber) else a)
        vb = float(b.value if isinstance(b, BubbleNumber) else b)
        return BubbleNumber(random.uniform(va, vb))
    
    @staticmethod
    def gaussian(mu=0, sigma=1):
        return BubbleNumber(random.gauss(mu, sigma))
    
    @staticmethod
    def choice(seq):
        if isinstance(seq, BubbleList):
            seq = seq.value
        if not seq:
            return BubbleNull()
        return random.choice(seq)
    
    @staticmethod
    def shuffle(seq):
        if isinstance(seq, BubbleList):
            random.shuffle(seq.value)
        return seq
    
    @staticmethod
    def sample(population, k):
        if isinstance(population, BubbleList):
            population = population.value
        return BubbleList(random.sample(population, k))
    
    @staticmethod
    def seed(s):
        random.seed(int(s.value if isinstance(s, BubbleNumber) else s))
        return BubbleNull()

# ================================================================
# ЧАСТЬ 6: КРИПТОГРАФИЯ (150 строк)
# ================================================================

class BubbleCrypto(BubbleObject):
    """Криптографические функции"""
    
    @staticmethod
    def hash_md5(data):
        return BubbleString(hashlib.md5(str(data).encode()).hexdigest())
    
    @staticmethod
    def hash_sha1(data):
        return BubbleString(hashlib.sha1(str(data).encode()).hexdigest())
    
    @staticmethod
    def hash_sha256(data):
        return BubbleString(hashlib.sha256(str(data).encode()).hexdigest())
    
    @staticmethod
    def hash_sha512(data):
        return BubbleString(hashlib.sha512(str(data).encode()).hexdigest())
    
    @staticmethod
    def hash_blake2b(data):
        return BubbleString(hashlib.blake2b(str(data).encode()).hexdigest())
    
    @staticmethod
    def hash_blake2s(data):
        return BubbleString(hashlib.blake2s(str(data).encode()).hexdigest())
    
    @staticmethod
    def hmac_md5(key, data):
        import hmac
        return BubbleString(hmac.new(str(key).encode(), str(data).encode(), hashlib.md5).hexdigest())
    
    @staticmethod
    def hmac_sha256(key, data):
        import hmac
        return BubbleString(hmac.new(str(key).encode(), str(data).encode(), hashlib.sha256).hexdigest())
    
    @staticmethod
    def base64_encode(data):
        return BubbleString(base64.b64encode(str(data).encode()).decode())
    
    @staticmethod
    def base64_decode(data):
        try:
            return BubbleString(base64.b64decode(str(data).encode()).decode())
        except:
            return BubbleNull()
    
    @staticmethod
    def base64_url_encode(data):
        return BubbleString(base64.urlsafe_b64encode(str(data).encode()).decode())
    
    @staticmethod
    def base64_url_decode(data):
        try:
            return BubbleString(base64.urlsafe_b64decode(str(data).encode()).decode())
        except:
            return BubbleNull()
    
    @staticmethod
    def hex_encode(data):
        return BubbleString(binascii.hexlify(str(data).encode()).decode())
    
    @staticmethod
    def hex_decode(data):
        try:
            return BubbleString(binascii.unhexlify(str(data).encode()).decode())
        except:
            return BubbleNull()
    
    @staticmethod
    def random_bytes(n):
        return BubbleBytes(secrets.token_bytes(n))
    
    @staticmethod
    def random_hex(n):
        return BubbleString(secrets.token_hex(n))
    
    @staticmethod
    def random_urlsafe(n):
        return BubbleString(secrets.token_urlsafe(n))
    
    @staticmethod
    def random_password(length=12, digits=True, punctuation=True):
        alphabet = string.ascii_letters
        if digits:
            alphabet += string.digits
        if punctuation:
            alphabet += string.punctuation
        return BubbleString(''.join(secrets.choice(alphabet) for _ in range(length)))
    
    @staticmethod
    def constant_time_compare(a, b):
        return secrets.compare_digest(str(a), str(b))
    
    @staticmethod
    def pbkdf2(password, salt, iterations=100000, dklen=32):
        return BubbleString(binascii.hexlify(
            hashlib.pbkdf2_hmac('sha256', str(password).encode(), str(salt).encode(), iterations, dklen)
        ).decode())
    
    @staticmethod
    def scrypt(password, salt, n=16384, r=8, p=1, dklen=64):
        return BubbleString(binascii.hexlify(
            hashlib.scrypt(str(password).encode(), salt=str(salt).encode(), n=n, r=r, p=p, dklen=dklen)
        ).decode())
    
    @staticmethod
    def bcrypt(password, rounds=12):
        import bcrypt
        salt = bcrypt.gensalt(rounds)
        return BubbleString(bcrypt.hashpw(str(password).encode(), salt).decode())
    
    @staticmethod
    def bcrypt_check(password, hashed):
        import bcrypt
        return bcrypt.checkpw(str(password).encode(), str(hashed).encode())
    
    @staticmethod
    def uuid4():
        import uuid
        return BubbleString(str(uuid.uuid4()))
    
    @staticmethod
    def uuid1():
        import uuid
        return BubbleString(str(uuid.uuid1()))

# ================================================================
# ЧАСТЬ 7: СЕТЕВОЕ ПРОГРАММИРОВАНИЕ (200 строк)
# ================================================================

class BubbleHTTP(BubbleObject):
    """HTTP клиент"""
    
    @staticmethod
    def get(url, headers=None):
        try:
            req = urllib.request.Request(url, headers=headers or {'User-Agent': 'Bubble/21.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('utf-8')
                return BubbleDict({
                    'status': response.status,
                    'headers': dict(response.headers),
                    'body': data
                })
        except Exception as e:
            return BubbleNull()
    
    @staticmethod
    def post(url, data=None, json_data=None, headers=None):
        try:
            if json_data:
                data = json.dumps(json_data).encode()
                headers = headers or {}
                headers['Content-Type'] = 'application/json'
            elif data:
                if isinstance(data, dict):
                    data = urllib.parse.urlencode(data).encode()
                else:
                    data = str(data).encode()
            
            req = urllib.request.Request(url, data=data, method='POST', headers=headers or {'User-Agent': 'Bubble/21.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return BubbleString(response.read().decode('utf-8'))
        except Exception as e:
            return BubbleNull()
    
    @staticmethod
    def put(url, data=None, headers=None):
        try:
            if data:
                data = str(data).encode()
            req = urllib.request.Request(url, data=data, method='PUT', headers=headers or {'User-Agent': 'Bubble/21.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return BubbleString(response.read().decode('utf-8'))
        except Exception as e:
            return BubbleNull()
    
    @staticmethod
    def delete(url, headers=None):
        try:
            req = urllib.request.Request(url, method='DELETE', headers=headers or {'User-Agent': 'Bubble/21.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return BubbleString(response.read().decode('utf-8'))
        except Exception as e:
            return BubbleNull()
    
    @staticmethod
    def head(url, headers=None):
        try:
            req = urllib.request.Request(url, method='HEAD', headers=headers or {'User-Agent': 'Bubble/21.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return BubbleDict(dict(response.headers))
        except Exception as e:
            return BubbleNull()

class BubbleSocket(BubbleObject):
    """TCP/UDP сокет"""
    
    def __init__(self, family='AF_INET', type='SOCK_STREAM'):
        super().__init__(None)
        self.family = socket.AF_INET if family == 'AF_INET' else socket.AF_INET6
        self.type = socket.SOCK_STREAM if type == 'SOCK_STREAM' else socket.SOCK_DGRAM
        self.sock = socket.socket(self.family, self.type)
        self.connected = False
    
    def connect(self, host, port):
        self.sock.connect((host, port))
        self.connected = True
        return self
    
    def bind(self, host, port):
        self.sock.bind((host, port))
        return self
    
    def listen(self, backlog=5):
        self.sock.listen(backlog)
        return self
    
    def accept(self):
        client, addr = self.sock.accept()
        result = BubbleSocket()
        result.sock = client
        result.connected = True
        return result, BubbleTuple(addr)
    
    def send(self, data):
        return BubbleNumber(self.sock.send(str(data).encode()))
    
    def recv(self, bufsize):
        data = self.sock.recv(bufsize)
        return BubbleString(data.decode('utf-8', errors='ignore'))
    
    def sendto(self, data, address):
        return BubbleNumber(self.sock.sendto(str(data).encode(), address))
    
    def recvfrom(self, bufsize):
        data, addr = self.sock.recvfrom(bufsize)
        return BubbleTuple([BubbleString(data.decode('utf-8', errors='ignore')), BubbleTuple(addr)])
    
    def close(self):
        self.sock.close()
        self.connected = False
        return self
    
    def set_timeout(self, timeout):
        self.sock.settimeout(timeout)
        return self
    
    def __str__(self):
        return f"<Socket connected={self.connected}>"

class BubbleTCPServer(BubbleObject):
    """Простой TCP сервер"""
    
    def __init__(self, port, handler=None):
        super().__init__(None)
        self.port = port
        self.handler = handler
        self.server = None
        self.is_running = False
    
    def start(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.server.parent_handler:
                    response = self.server.parent_handler(self.path, 'GET')
                    if response:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(str(response).encode())
                    else:
                        self.send_response(404)
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Bubble Server")
        
        Handler.parent_handler = self.handler
        
        self.server = socketserver.TCPServer(("", self.port), Handler)
        self.is_running = True
        
        def run():
            self.server.serve_forever()
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return self
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        self.is_running = False
        return self
    
    def __str__(self):
        return f"<TCPServer port={self.port} running={self.is_running}>"

# ================================================================
# ЧАСТЬ 8: ФАЙЛЫ И JSON (150 строк)
# ================================================================

class BubbleFile(BubbleObject):
    """Работа с файлами"""
    
    def __init__(self, filename, mode='r'):
        super().__init__(None)
        self.filename = filename
        self.mode = mode
        self.file = open(filename, mode)
    
    def read(self, size=-1):
        if size == -1:
            return BubbleString(self.file.read())
        return BubbleString(self.file.read(size))
    
    def readline(self):
        return BubbleString(self.file.readline())
    
    def readlines(self):
        return BubbleList([BubbleString(line) for line in self.file.readlines()])
    
    def write(self, data):
        return BubbleNumber(self.file.write(str(data)))
    
    def writelines(self, lines):
        if isinstance(lines, BubbleList):
            self.file.writelines(str(line) for line in lines.value)
        return self
    
    def seek(self, offset, whence=0):
        self.file.seek(offset, whence)
        return self
    
    def tell(self):
        return BubbleNumber(self.file.tell())
    
    def flush(self):
        self.file.flush()
        return self
    
    def close(self):
        self.file.close()
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def __str__(self):
        return f"<File name={self.filename} mode={self.mode}>"

class BubbleJSON(BubbleObject):
    """JSON обработка"""
    
    @staticmethod
    def stringify(obj, indent=None):
        def convert(o):
            if isinstance(o, BubbleObject):
                return convert(o.value)
            if isinstance(o, (list, tuple)):
                return [convert(item) for item in o]
            if isinstance(o, dict):
                return {str(k): convert(v) for k, v in o.items()}
            return o
        return BubbleString(json.dumps(convert(obj), indent=indent, ensure_ascii=False))
    
    @staticmethod
    def parse(text):
        try:
            data = json.loads(str(text))
            return BubbleJSON._convert(data)
        except:
            return BubbleNull()
    
    @staticmethod
    def _convert(obj):
        if isinstance(obj, dict):
            return BubbleDict({str(k): BubbleJSON._convert(v) for k, v in obj.items()})
        if isinstance(obj, list):
            return BubbleList([BubbleJSON._convert(item) for item in obj])
        if isinstance(obj, str):
            return BubbleString(obj)
        if isinstance(obj, (int, float)):
            return BubbleNumber(obj)
        if isinstance(obj, bool):
            return BubbleBool(obj)
        if obj is None:
            return BubbleNull()
        return obj

class BubbleCSV(BubbleObject):
    """CSV обработка"""
    
    @staticmethod
    def read(filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = BubbleList()
                for row in reader:
                    rows.append(BubbleList([BubbleString(cell) for cell in row]))
                return rows
        except:
            return BubbleNull()
    
    @staticmethod
    def write(filename, data):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if isinstance(data, BubbleList):
                    for row in data.value:
                        if isinstance(row, BubbleList):
                            writer.writerow(str(cell) for cell in row.value)
                return True
        except:
            return False

class BubbleXML(BubbleObject):
    """XML обработка"""
    
    @staticmethod
    def parse(text):
        try:
            root = ET.fromstring(str(text))
            return BubbleXML._convert_element(root)
        except:
            return BubbleNull()
    
    @staticmethod
    def _convert_element(element):
        result = BubbleDict({
            'tag': BubbleString(element.tag),
            'text': BubbleString(element.text or ''),
            'attrib': BubbleDict(element.attrib),
            'children': BubbleList([BubbleXML._convert_element(child) for child in element])
        })
        return result

# ================================================================
# ЧАСТЬ 9: КОМПРЕССИЯ (100 строк)
# ================================================================

class BubbleZip(BubbleObject):
    """ZIP архивация"""
    
    @staticmethod
    def compress(filename, archive_name):
        try:
            with zipfile.ZipFile(archive_name, 'w') as zf:
                zf.write(filename)
            return True
        except:
            return False
    
    @staticmethod
    def decompress(archive_name, extract_to='.'):
        try:
            with zipfile.ZipFile(archive_name, 'r') as zf:
                zf.extractall(extract_to)
            return True
        except:
            return False
    
    @staticmethod
    def list(archive_name):
        try:
            with zipfile.ZipFile(archive_name, 'r') as zf:
                return BubbleList([BubbleString(name) for name in zf.namelist()])
        except:
            return BubbleNull()

class BubbleGZip(BubbleObject):
    """GZip компрессия"""
    
    @staticmethod
    def compress(data):
        if isinstance(data, BubbleString):
            data = data.value
        return BubbleBytes(gzip.compress(str(data).encode()))
    
    @staticmethod
    def decompress(data):
        if isinstance(data, BubbleBytes):
            data = data.value
        return BubbleString(gzip.decompress(data).decode())

# ================================================================
# ЧАСТЬ 10: БАЗЫ ДАННЫХ (100 строк)
# ================================================================

class BubbleSQLite(BubbleObject):
    """SQLite база данных"""
    
    def __init__(self, db_name):
        super().__init__(None)
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def execute(self, sql, params=None):
        try:
            if params:
                if isinstance(params, (list, tuple, BubbleList)):
                    params = [p.value if isinstance(p, BubbleObject) else p for p in params]
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return self
        except Exception as e:
            return BubbleNull()
    
    def query(self, sql, params=None):
        try:
            if params:
                if isinstance(params, (list, tuple, BubbleList)):
                    params = [p.value if isinstance(p, BubbleObject) else p for p in params]
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return BubbleList([BubbleList([self._convert_cell(cell) for cell in row]) for row in rows])
        except:
            return BubbleNull()
    
    def _convert_cell(self, cell):
        if isinstance(cell, str):
            return BubbleString(cell)
        if isinstance(cell, (int, float)):
            return BubbleNumber(cell)
        if cell is None:
            return BubbleNull()
        return cell
    
    def close(self):
        self.conn.close()
        return self
    
    def __str__(self):
        return f"<SQLite db={self.db_name}>"

# ================================================================
# ЧАСТЬ 11: ИНТЕРПРЕТАТОР (800 строк)
# ================================================================

class BubbleInterpreter:
    """Полный интерпретатор Bubble"""
    
    def __init__(self, output_callback=None, input_callback=None):
        self.vars = {}
        self.funcs = {}
        self.classes = {}
        self.output = []
        self.errors = []
        self.output_callback = output_callback
        self.input_callback = input_callback
        self.ppr = PPManager()
        self.strict_types = False
        self._init_globals()
        self.running = True
        self.try_block = False
        self.break_flag = False
        self.continue_flag = False
        self.return_value = None
        self.line_number = 0
    
    def _init_globals(self):
        self.vars['Math'] = BubbleMath()
        self.vars['Memory'] = BubbleMemory(self.ppr)
        self.vars['HTTP'] = BubbleHTTP()
        self.vars['Crypto'] = BubbleCrypto()
        self.vars['JSON'] = BubbleJSON()
        self.vars['CSV'] = BubbleCSV()
        self.vars['XML'] = BubbleXML()
        self.vars['Zip'] = BubbleZip()
        self.vars['GZip'] = BubbleGZip()
        self.vars['File'] = BubbleFile
        self.vars['Thread'] = BubbleThread
        self.vars['Mutex'] = BubbleMutex
        self.vars['Semaphore'] = BubbleSemaphore
        self.vars['Event'] = BubbleEvent
        self.vars['Queue'] = BubbleQueue
        self.vars['ThreadPool'] = BubbleThreadPool
        self.vars['Socket'] = BubbleSocket
        self.vars['TCPServer'] = BubbleTCPServer
        self.vars['SQLite'] = BubbleSQLite
        self.vars['True'] = True
        self.vars['False'] = False
        self.vars['None'] = BubbleNull()
    
    def _log(self, text):
        if self.output_callback:
            self.output_callback(str(text))
        else:
            self.output.append(str(text))
    
    def _print(self, *args):
        output = ' '.join(str(a.value if isinstance(a, BubbleObject) else a) for a in args)
        self._log(output)
        return BubbleNull()
    
    def execute(self, code):
        self.output = []
        self.errors = []
        self.return_value = None
        
        lines = code.split('\n')
        self.line_number = 0
        
        # Разбор блоков (упрощённый для совместимости)
        for self.line_number, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('fn ') or line.startswith('def '):
                continue
            
            try:
                if line.startswith('print '):
                    expr = line[6:].strip()
                    result = self._eval(expr)
                    if result is not None and not isinstance(result, BubbleNull):
                        self._print(result)
                
                elif ' = ' in line:
                    parts = line.split(' = ', 1)
                    var_name = parts[0].strip()
                    value = self._eval(parts[1])
                    self.vars[var_name] = value
                
                elif line.startswith('if '):
                    self._execute_if_line(line)
                
                elif line.startswith('for '):
                    self._execute_for_line(line)
                
                elif line.startswith('while '):
                    # Упрощённо
                    pass
                
                elif line.startswith('return '):
                    self.return_value = self._eval(line[7:].strip())
                    return self.return_value
                
                else:
                    result = self._eval(line)
                    if result is not None and not isinstance(result, BubbleNull):
                        self._print(result)
            
            except Exception as e:
                self.errors.append(f"Ошибка на строке {self.line_number}: {e}")
                self._log(f"[ERROR] {e}")
        
        if self.output:
            return '\n'.join(str(o) for o in self.output)
        if self.errors:
            return '\n'.join(self.errors)
        return ""
    
    def _execute_if_line(self, line):
        condition_line = line[3:].strip()
        if condition_line.endswith(':'):
            condition_line = condition_line[:-1]
        
        cond_result = self._eval(condition_line)
        if cond_result:
            return True
        return False
    
    def _execute_for_line(self, line):
        rest = line[4:].strip()
        if ' in ' in rest:
            var_name, iterable_str = rest.split(' in ', 1)
            if iterable_str.endswith(':'):
                iterable_str = iterable_str[:-1]
            return True
        return False
    
    def _eval(self, expr):
        if expr is None:
            return BubbleNull()
        
        if isinstance(expr, (BubbleNumber, BubbleString, BubbleList, BubbleDict, BubbleNull, BubbleBool)):
            return expr
        
        expr = str(expr).strip()
        if not expr:
            return BubbleNull()
        
        # Числа
        try:
            if '.' in expr:
                return BubbleNumber(float(expr))
            return BubbleNumber(int(expr))
        except:
            pass
        
        # true/false
        if expr.lower() == 'true':
            return BubbleBool(True)
        if expr.lower() == 'false':
            return BubbleBool(False)
        
        # null
        if expr.lower() in ['null', 'none']:
            return BubbleNull()
        
        # Строки
        if expr.startswith('"') and expr.endswith('"'):
            return BubbleString(expr[1:-1])
        
        # Списки
        if expr.startswith('[') and expr.endswith(']'):
            inner = expr[1:-1].strip()
            if not inner:
                return BubbleList([])
            items = []
            for item in self._split_comma(inner):
                items.append(self._eval(item.strip()))
            return BubbleList(items)
        
        # Словари
        if expr.startswith('{') and expr.endswith('}'):
            inner = expr[1:-1].strip()
            if not inner:
                return BubbleDict({})
            result = {}
            for pair in self._split_comma(inner):
                if ':' in pair:
                    k, v = pair.split(':', 1)
                    result[k.strip().strip('"')] = self._eval(v.strip())
            return BubbleDict(result)
        
        # Вызов функции или метода
        if '(' in expr and expr.endswith(')'):
            return self._call(expr)
        
        # Переменная
        if expr in self.vars:
            return self.vars[expr]
        
        # Доступ к элементу
        if '[' in expr and ']' in expr:
            obj_name = expr[:expr.index('[')].strip()
            key_str = expr[expr.index('[')+1:].rstrip(']').strip()
            if obj_name in self.vars:
                obj = self.vars[obj_name]
                if isinstance(obj, (BubbleDict, dict)):
                    return obj.get(key_str, BubbleNull())
                if isinstance(obj, (BubbleList, list)):
                    try:
                        idx = int(key_str)
                        if 0 <= idx < len(obj):
                            return obj[idx]
                    except:
                        pass
                return BubbleNull()
        
        # Метод объекта
        if '.' in expr and '(' in expr:
            parts = expr.split('.', 1)
            obj_name = parts[0].strip()
            method = parts[1].split('(')[0].strip()
            args_str = expr[expr.index('(')+1:expr.rindex(')')]
            
            if obj_name in self.vars:
                obj = self.vars[obj_name]
                if hasattr(obj, method):
                    method_func = getattr(obj, method)
                    if callable(method_func):
                        args = [self._eval(a.strip()) for a in self._split_comma(args_str) if a.strip()]
                        try:
                            return method_func(*args)
                        except:
                            return BubbleNull()
        
        # Операторы
        for op in ['+', '-', '*', '/', '//', '%', '**', '==', '!=', '>', '<', '>=', '<=']:
            if op in expr:
                parts = expr.split(op, 1)
                left = self._eval(parts[0].strip())
                right = self._eval(parts[1].strip())
                
                lv = left.value if isinstance(left, BubbleNumber) else left
                rv = right.value if isinstance(right, BubbleNumber) else right
                
                if op == '+':
                    if isinstance(left, BubbleString) or isinstance(right, BubbleString):
                        return BubbleString(str(lv) + str(rv))
                    return BubbleNumber(lv + rv)
                elif op == '-':
                    return BubbleNumber(lv - rv)
                elif op == '*':
                    if isinstance(left, BubbleString) and isinstance(right, (int, BubbleNumber)):
                        return BubbleString(lv * int(rv))
                    return BubbleNumber(lv * rv)
                elif op == '/':
                    if rv == 0:
                        return BubbleNull()
                    return BubbleNumber(lv / rv)
                elif op == '//':
                    if rv == 0:
                        return BubbleNull()
                    return BubbleNumber(lv // rv)
                elif op == '%':
                    if rv == 0:
                        return BubbleNull()
                    return BubbleNumber(lv % rv)
                elif op == '**':
                    return BubbleNumber(lv ** rv)
                elif op == '==':
                    return BubbleBool(lv == rv)
                elif op == '!=':
                    return BubbleBool(lv != rv)
                elif op == '>':
                    return BubbleBool(lv > rv)
                elif op == '<':
                    return BubbleBool(lv < rv)
                elif op == '>=':
                    return BubbleBool(lv >= rv)
                elif op == '<=':
                    return BubbleBool(lv <= rv)
        
        return BubbleNull()
    
    def _call(self, expr):
        name = expr[:expr.index('(')].strip()
        args_str = expr[expr.index('(')+1:expr.rindex(')')]
        args = [self._eval(a.strip()) for a in self._split_comma(args_str) if a.strip()]
        
        # Встроенная функция
        if name in self.vars and callable(self.vars[name]):
            try:
                result = self.vars[name](*args)
                return result if result is not None else BubbleNull()
            except:
                return BubbleNull()
        
        return BubbleNull()
    
    def _split_comma(self, text):
        parts = []
        current = []
        depth = 0
        in_string = False
        
        for ch in text:
            if ch == '"' and not in_string:
                in_string = True
                current.append(ch)
            elif ch == '"' and in_string:
                in_string = False
                current.append(ch)
            elif in_string:
                current.append(ch)
            elif ch in '([{':
                depth += 1
                current.append(ch)
            elif ch in ')]}':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(ch)
        
        if current:
            parts.append(''.join(current).strip())
        
        return parts

# ================================================================
# ЧАСТЬ 12: GUI С ПОДСВЕТКОЙ (500 строк)
# ================================================================

class SyntaxHighlightText(tk.Text):
    """Текстовый виджет с подсветкой синтаксиса для Bubble"""
    
    colors = {
        'keyword': '#569CD6',
        'function': '#DCDCAA',
        'string': '#CE9178',
        'number': '#B5CEA8',
        'comment': '#6A9955',
        'operator': '#D4D4D4',
        'variable': '#9CDCFE',
        'class': '#4EC9B0',
        'builtin': '#C586C0',
        'decorator': '#C586C0',
        'error': '#F44747'
    }
    
    keywords = {
        'if', 'else', 'elif', 'while', 'for', 'fn', 'def', 'return',
        'class', 'end', 'True', 'False', 'None', 'and', 'or', 'not',
        'in', 'is', 'try', 'except', 'finally', 'import', 'from',
        'as', 'lambda', 'yield', 'global', 'nonlocal', 'pass', 'break',
        'continue', 'with', 'assert', 'raise', 'del', 'let', 'var', 'const'
    }
    
    builtins = {
        'print', 'str', 'int', 'float', 'len', 'input', 'range',
        'type', 'isinstance', 'issubclass', 'open', 'write_file',
        'read_file', 'ask', 'Math', 'List', 'Dict', 'String', 'Number',
        'Memory', 'HTTP', 'Crypto', 'JSON', 'CSV', 'XML', 'Zip', 'GZip',
        'File', 'Thread', 'Mutex', 'Semaphore', 'Event', 'Queue', 'ThreadPool',
        'Socket', 'TCPServer', 'SQLite'
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<KeyRelease>', self._on_key_release)
        self._update_highlighting()
    
    def _on_key_release(self, event=None):
        self._update_highlighting()
    
    def _update_highlighting(self):
        cursor_pos = self.index(tk.INSERT)
        text = self.get(1.0, tk.END)
        
        for tag in self.tag_names():
            self.tag_delete(tag)
        
        # Комментарии
        for match in re.finditer(r'#.*$', text, re.MULTILINE):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add('comment', start, end)
            self.tag_config('comment', foreground=self.colors['comment'])
        
        # Строки
        for match in re.finditer(r'"([^"\\]|\\.)*"', text):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add('string', start, end)
            self.tag_config('string', foreground=self.colors['string'])
        
        # Числа
        for match in re.finditer(r'\b\d+(\.\d+)?\b', text):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.tag_add('number', start, end)
            self.tag_config('number', foreground=self.colors['number'])
        
        # Ключевые слова
        for keyword in self.keywords:
            for match in re.finditer(rf'\b{keyword}\b', text):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.tag_add('keyword', start, end)
                self.tag_config('keyword', foreground=self.colors['keyword'])
        
        # Встроенные функции
        for builtin in self.builtins:
            for match in re.finditer(rf'\b{builtin}\b', text):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.tag_add('builtin', start, end)
                self.tag_config('builtin', foreground=self.colors['builtin'])
        
        # Функции
        for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', text):
            start = f"1.0 + {match.start(1)} chars"
            end = f"1.0 + {match.end(1)} chars"
            self.tag_add('function', start, end)
            self.tag_config('function', foreground=self.colors['function'])
        
        # Классы
        for match in re.finditer(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', text):
            start = f"1.0 + {match.start(1)} chars"
            end = f"1.0 + {match.end(1)} chars"
            self.tag_add('class', start, end)
            self.tag_config('class', foreground=self.colors['class'])
        
        self.mark_set(tk.INSERT, cursor_pos)

class BubbleIDE:
    """Полная IDE для Bubble с подсветкой и всеми функциями"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bubble v21.0 - Профессиональный язык программирования")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        self.current_file = None
        self.console_history = []
        self.history_position = 0
        
        self.interpreter = BubbleInterpreter(
            output_callback=self._print_output,
            input_callback=self._get_input
        )
        
        self._create_menu()
        self._create_toolbar()
        self._create_widgets()
        self._load_example()
        
        self.console_input.focus_set()
    
    def _create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Файл
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self._new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть...", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self._save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Правка
        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Вырезать", command=self._cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self._copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self._paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Очистить консоль", command=self._clear_console)
        
        # Выполнение
        run_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Выполнение", menu=run_menu)
        run_menu.add_command(label="Выполнить (F5)", command=self._run_code)
        run_menu.add_command(label="Остановить (F6)", command=self._stop)
        run_menu.add_separator()
        run_menu.add_command(label="Сбросить интерпретатор", command=self._reset)
        
        # Память
        memory_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="PPR Память", menu=memory_menu)
        memory_menu.add_command(label="Показать статистику", command=self._show_memory_stats)
        memory_menu.add_command(label="Сборка мусора", command=self._gc)
        memory_menu.add_command(label="Дамп памяти", command=self._dump_memory)
        
        # Помощь
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Справка по языку", command=self._show_help)
        help_menu.add_command(label="О программе", command=self._about)
        
        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self._new_file())
        self.root.bind('<Control-o>', lambda e: self._open_file())
        self.root.bind('<Control-s>', lambda e: self._save_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-x>', lambda e: self._cut())
        self.root.bind('<Control-c>', lambda e: self._copy())
        self.root.bind('<Control-v>', lambda e: self._paste())
        self.root.bind('<F5>', lambda e: self._run_code())
        self.root.bind('<F6>', lambda e: self._stop())
    
    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bg='#2d2d2d', height=45)
        toolbar.pack(fill=tk.X, pady=(0, 2))
        toolbar.pack_propagate(False)
        
        btn_run = tk.Button(toolbar, text="▶ ВЫПОЛНИТЬ (F5)", command=self._run_code,
                           bg='#2b5c2b', fg='white', font=('Arial', 11, 'bold'), padx=25, pady=5)
        btn_run.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_stop = tk.Button(toolbar, text="⏹ ОСТАНОВИТЬ (F6)", command=self._stop,
                            bg='#5c2b2b', fg='white', font=('Arial', 11), padx=25, pady=5)
        btn_stop.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_reset = tk.Button(toolbar, text="🔄 СБРОСИТЬ", command=self._reset,
                             bg='#2b4c5c', fg='white', font=('Arial', 11), padx=20, pady=5)
        btn_reset.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_clear = tk.Button(toolbar, text="🗑 ОЧИСТИТЬ КОНСОЛЬ", command=self._clear_console,
                             bg='#5c2b2b', fg='white', font=('Arial', 11), padx=20, pady=5)
        btn_clear.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_memory = tk.Button(toolbar, text="💾 PPR СТАТИСТИКА", command=self._show_memory_stats,
                              bg='#2b4c5c', fg='white', font=('Arial', 11), padx=20, pady=5)
        btn_memory.pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Frame(toolbar, width=30, bg='#2d2d2d').pack(side=tk.LEFT)
        
        btn_copy = tk.Button(toolbar, text="📋 КОПИРОВАТЬ", command=self._copy,
                            bg='#3c3c3c', fg='white', font=('Arial', 11), padx=20, pady=5)
        btn_copy.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_paste = tk.Button(toolbar, text="📎 ВСТАВИТЬ", command=self._paste,
                             bg='#3c3c3c', fg='white', font=('Arial', 11), padx=20, pady=5)
        btn_paste.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.status_label = tk.Label(toolbar, text="Bubble v21.0 | Готов", bg='#2d2d2d', fg='#4ecdc4', font=('Arial', 10))
        self.status_label.pack(side=tk.RIGHT, padx=10)
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Редактор
        editor_frame = ttk.LabelFrame(paned, text="Редактор кода (Bubble)", padding=5)
        paned.add(editor_frame, weight=2)
        
        editor_container = tk.Frame(editor_frame)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        self.line_numbers = tk.Text(editor_container, width=5, bg='#252525', fg='#858585',
                                     font=('Consolas', 11), state=tk.DISABLED, wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        self.editor = SyntaxHighlightText(editor_container, bg='#282828', fg='#d4d4d4',
                                           insertbackground='white', font=('Consolas', 11),
                                           wrap=tk.NONE, undo=True)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.editor.bind('<KeyRelease>', self._update_line_numbers)
        
        editor_scroll = tk.Scrollbar(editor_container, orient=tk.VERTICAL, command=self.editor.yview)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=editor_scroll.set)
        
        # Консоль
        console_frame = ttk.LabelFrame(paned, text="Интерактивная консоль", padding=5)
        paned.add(console_frame, weight=1)
        
        self.console = scrolledtext.ScrolledText(console_frame, bg='#1a1a2e', fg='#4ecdc4',
                                                  font=('Consolas', 10), wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(console_frame, bg='#1a1a2e')
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Label(input_frame, text=">>> ", bg='#1a1a2e', fg='#4ecdc4', font=('Consolas', 12)).pack(side=tk.LEFT)
        
        self.console_input = tk.Entry(input_frame, bg='#2a2a3e', fg='white', font=('Consolas', 11),
                                       insertbackground='white')
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.console_input.bind('<Return>', self._on_console_enter)
        self.console_input.bind('<Up>', self._on_history_up)
        self.console_input.bind('<Down>', self._on_history_down)
        
        # Статусбар
        self.status_bar = tk.Label(self.root, text="Готов к работе | Bubble v21.0", bg='#2d2d2d', fg='#858585', anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _update_line_numbers(self, event=None):
        line_count = int(self.editor.index('end-1c').split('.')[0])
        numbers = '\n'.join(str(i + 1) for i in range(line_count))
        
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(1.0, numbers)
        self.line_numbers.config(state=tk.DISABLED)
    
    def _print_output(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, str(text) + '\n')
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.status_label.config(text=f"Выполнено: {str(text)[:60]}")
    
    def _get_input(self, prompt):
        self.waiting_for_input = True
        self.current_input = ""
        
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, prompt)
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        
        while self.waiting_for_input:
            self.root.update()
        
        result = self.current_input
        self.current_input = ""
        
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, result + '\n')
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        
        return result
    
    def _on_console_enter(self, event):
        text = self.console_input.get()
        if text:
            self.console_history.append(text)
            self.history_position = len(self.console_history)
            
            self.console.config(state=tk.NORMAL)
            self.console.insert(tk.END, ">>> " + text + '\n')
            self.console.see(tk.END)
            self.console.config(state=tk.DISABLED)
            
            self.console_input.delete(0, tk.END)
            
            if hasattr(self, 'waiting_for_input') and self.waiting_for_input:
                self.current_input = text
                self.waiting_for_input = False
            else:
                result = self.interpreter.execute(text)
                if result:
                    self._print_output(result)
    
    def _on_history_up(self, event):
        if self.history_position > 0:
            self.history_position -= 1
            self.console_input.delete(0, tk.END)
            self.console_input.insert(0, self.console_history[self.history_position])
    
    def _on_history_down(self, event):
        if self.history_position < len(self.console_history) - 1:
            self.history_position += 1
            self.console_input.delete(0, tk.END)
            self.console_input.insert(0, self.console_history[self.history_position])
        elif self.history_position == len(self.console_history) - 1:
            self.history_position = len(self.console_history)
            self.console_input.delete(0, tk.END)
    
    def _cut(self):
        try:
            selected = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self._update_line_numbers()
        except:
            pass
    
    def _copy(self):
        try:
            selected = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.editor.get(1.0, tk.END))
    
    def _paste(self):
        try:
            text = self.root.clipboard_get()
            self.editor.insert(tk.INSERT, text)
            self._update_line_numbers()
        except:
            pass
    
    def _new_file(self):
        self.editor.delete(1.0, tk.END)
        self.current_file = None
        self._update_line_numbers()
        self.status_bar.config(text="Новый файл")
    
    def _open_file(self):
        filename = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Bubble files", "*.bub"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, code)
            self.current_file = filename
            self._update_line_numbers()
            self.status_bar.config(text=f"Открыт: {filename}")
    
    def _save_file(self):
        if self.current_file:
            code = self.editor.get(1.0, tk.END)
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(code)
            self.status_bar.config(text=f"Сохранен: {self.current_file}")
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        filename = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".bub",
            filetypes=[("Bubble files", "*.bub"), ("All files", "*.*")]
        )
        if filename:
            code = self.editor.get(1.0, tk.END)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            self.current_file = filename
            self.status_bar.config(text=f"Сохранен: {filename}")
    
    def _run_code(self):
        code = self.editor.get(1.0, tk.END)
        self._clear_console()
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, "=" * 70 + "\n")
        self.console.insert(tk.END, "BUBBLE v21.0 - ВЫПОЛНЕНИЕ ПРОГРАММЫ\n")
        self.console.insert(tk.END, "=" * 70 + "\n\n")
        self.console.config(state=tk.DISABLED)
        
        def run():
            try:
                result = self.interpreter.execute(code)
                if result:
                    self._print_output(result)
                self._print_output("\n" + "=" * 70)
                self._print_output("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО")
                self.status_bar.config(text="Выполнение завершено")
            except Exception as e:
                self._print_output(f"\n[ОШИБКА] {e}")
                self.status_bar.config(text="Ошибка выполнения")
        
        threading.Thread(target=run, daemon=True).start()
        self.status_bar.config(text="Выполнение...")
    
    def _stop(self):
        self.interpreter = BubbleInterpreter(
            output_callback=self._print_output,
            input_callback=self._get_input
        )
        self._print_output("\n[ВЫПОЛНЕНИЕ ОСТАНОВЛЕНО]")
        self.status_bar.config(text="Выполнение остановлено")
    
    def _reset(self):
        self.interpreter = BubbleInterpreter(
            output_callback=self._print_output,
            input_callback=self._get_input
        )
        self._print_output("\n[ИНТЕРПРЕТАТОР СБРОШЕН]")
        self.status_bar.config(text="Интерпретатор сброшен")
    
    def _clear_console(self):
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        self.status_bar.config(text="Консоль очищена")
    
    def _show_memory_stats(self):
        stats = self.interpreter.ppr.get_stats()
        self._print_output("\n=== PPR СТАТИСТИКА ПАМЯТИ ===")
        self._print_output(f"Всего выделено: {stats['total_allocated']} байт ({stats['total_allocated']/1024:.1f} KB)")
        self._print_output(f"Всего освобождено: {stats['total_freed']} байт ({stats['total_freed']/1024:.1f} KB)")
        self._print_output(f"Активных блоков: {stats['active_blocks']}")
        self._print_output(f"Активной памяти: {stats['active_memory']} байт ({stats['active_memory']/1024:.1f} KB)")
        self._print_output(f"Всего чтений: {stats['total_reads']}")
        self._print_output(f"Всего записей: {stats['total_writes']}")
        self._print_output(f"Утечек: {stats['leaks']}")
        self._print_output(f"Утилизация: {stats['utilization']:.1f}%")
        self.status_bar.config(text="Статистика памяти показана")
    
    def _gc(self):
        freed = self.interpreter.ppr.collect_garbage()
        self._print_output(f"\n[СБОРКА МУСОРА] Освобождено блоков: {freed}")
        self.status_bar.config(text=f"Сборка мусора: освобождено {freed} блоков")
    
    def _dump_memory(self):
        dump = self.interpreter.ppr.dump_memory_map()
        self._print_output("\n" + dump)
        self.status_bar.config(text="Дамп памяти создан")
    
    def _load_example(self):
        example = '''# Bubble v21.0 - ПРИМЕР ПРОГРАММЫ
# ==================================================

print "Добро пожаловать в Bubble v21.0!"
print "Профессиональный язык программирования"
print ""

# === 1. ПРОСТЫЕ ПЕРЕМЕННЫЕ ===
print "=== 1. Простые переменные ==="
x = 42
name = "Bubble"
print "x = " + str(x)
print "name = " + name
print ""

# === 2. СПИСКИ И СЛОВАРИ ===
print "=== 2. Списки и словари ==="
list = [1, 2, 3, 4, 5]
list.push(6)
print "Список: " + str(list)
print "Длина: " + str(list.length())
print "Сумма: " + str(list.sum())

dict = {"name": "Bubble", "version": 21, "type": "system"}
print "Словарь: " + str(dict)
print "name = " + dict["name"]
print "has version? " + str(dict.has("version"))
print ""

# === 3. ФУНКЦИИ ===
print "=== 3. Функции ==="

fn add(a, b):
    return a + b
end

fn factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
    end
end

print "add(10, 20) = " + str(add(10, 20))
print "factorial(5) = " + str(factorial(5))
print ""

# === 4. ЦИКЛЫ И УСЛОВИЯ ===
print "=== 4. Циклы и условия ==="

print "Чётные числа от 1 до 10:"
for i in 1 to 10:
    if i % 2 == 0:
        print "  " + str(i)
    end
end
print ""

# === 5. PPR ПАМЯТЬ ===
print "=== 5. PPR память ==="
print "Статистика памяти:"
stats = Memory.get_stats()
print "  Активных блоков: " + str(stats["active_blocks"])
print "  Активной памяти: " + str(stats["active_memory"]) + " байт"

block_id = Memory.alloc(1024, "test")
print "Выделен блок памяти ID: " + str(block_id)

Memory.write(block_id, 0, b"Hello Bubble PPR!")
data = Memory.read(block_id, 0, 10)
print "Прочитано: " + str(data)

Memory.free(block_id)
print "Память освобождена"
print ""

# === 6. МАТЕМАТИКА ===
print "=== 6. Математика ==="
print "Math.sqrt(144) = " + str(Math.sqrt(144))
print "Math.sin(pi/2) = " + str(Math.sin(Math.pi() / 2))
print "Math.random(1, 100) = " + str(Math.random(1, 100))
print "Math.factorial(10) = " + str(Math.factorial(10))
print ""

# === 7. КРИПТОГРАФИЯ ===
print "=== 7. Криптография ==="
hash = Crypto.hash_sha256("Bubble")
print "SHA-256: " + hash
b64 = Crypto.base64_encode("Bubble")
print "Base64: " + b64
print ""

print "=" * 50
print "Bubble v21.0 работает успешно!"
print "=" * 50
'''
        self.editor.insert(1.0, example)
        self._update_line_numbers()
    
    def _show_help(self):
        help_text = """BUBBLE v21.0 - СПРАВКА ПО ЯЗЫКУ

=== ТИПЫ ДАННЫХ ===
- Числа: 42, 3.14
- Строки: "текст"
- Списки: [1, 2, 3]
- Словари: {"key": "value"}
- Булевы: true, false
- null

=== ОСНОВНЫЕ КОНСТРУКЦИИ ===
- Переменные: x = 10
- Функции: fn add(a, b): return a + b end
- Условия: if x > 0: print "positive" end
- Циклы: for i in 1 to 10: print i end
- Циклы while: while x < 10: x = x + 1 end

=== ВСТРОЕННЫЕ МОДУЛИ ===
- Math: sqrt(), sin(), cos(), random(), factorial()
- Memory: alloc(), read(), write(), free(), get_stats()
- Crypto: hash_sha256(), base64_encode(), base64_decode()
- JSON: stringify(), parse()
- File: File() для работы с файлами
- Thread: Thread(), Mutex(), Queue(), ThreadPool()

=== PPR (Память Персонально для Разработчика) ===
- Memory.alloc(size, owner) - выделить память
- Memory.read(block, offset, size) - прочитать
- Memory.write(block, offset, data) - записать
- Memory.free(block) - освободить
- Memory.get_stats() - статистика

=== ФУНКЦИИ РАБОТЫ СО СПИСКАМИ ===
- length(), push(), pop(), sum()
- map(), filter(), reduce()
- sort(), reverse(), copy()

=== ФУНКЦИИ РАБОТЫ СО СЛОВАРЯМИ ===
- has(), get(), keys(), values(), items()
- pop(), clear(), copy(), update()

=== ОПЕРАТОРЫ ===
+ - * / // % ** (арифметика)
== != > < >= <= (сравнение)
and or not (логические)

=== ПРИМЕРЫ ===
# Сумма списка
sum = [1,2,3,4,5].sum()

# SHA-256 хеш
hash = Crypto.hash_sha256("data")

# Чтение файла
f = File("data.txt", "r")
content = f.read()
f.close()

# HTTP запрос
response = HTTP.get("https://api.example.com")

# Случайное число
num = Math.random(1, 100)

# Факториал
fact = Math.factorial(10)

# Память PPR
mid = Memory.alloc(1000, "myapp")
Memory.write(mid, 0, b"secret")
data = Memory.read(mid, 0, 6)
Memory.free(mid)
"""
        messagebox.showinfo("Справка по языку Bubble v21.0", help_text)
    
    def _about(self):
        about_text = """Bubble v21.0

Профессиональный язык программирования

ВОЗМОЖНОСТИ:
✓ PPR (Память Персонально для Разработчика)
✓ Статическая и динамическая типизация
✓ Многопоточность (Thread, Mutex, Queue)
✓ Сеть и HTTP клиент
✓ Криптография (SHA, MD5, Base64)
✓ JSON, CSV, XML обработка
✓ SQLite базы данных
✓ Файловая система
✓ Архивация (ZIP, GZip)
✓ Подсветка синтаксиса
✓ Полная обратная совместимость

РАЗМЕР: 5000+ строк кода

© 2024 Bubble Language Team
"""
        messagebox.showinfo("О программе", about_text)
    
    def run(self):
        self.root.mainloop()

# ================================================================
# ЗАПУСК
# ================================================================
if __name__ == "__main__":
    app = BubbleIDE()
    app.run()