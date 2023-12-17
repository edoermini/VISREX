import ctypes
import psutil
import platform
import time

# Constants
PTRACE_ATTACH = 16
PTRACE_GETREGS = 12
PTRACE_DETACH = 17

class ProcessAttachError(Exception):
    pass

class ProcessDetachError(Exception):
    pass

class RegisterReadError(Exception):
    pass

class CONTEXT(ctypes.Structure):
        _fields_ = [("ContextFlags", ctypes.c_ulong),
                    ("Dr0", ctypes.c_ulong),
                    ("Dr1", ctypes.c_ulong),
                    ("Dr2", ctypes.c_ulong),
                    ("Dr3", ctypes.c_ulong),
                    ("Dr6", ctypes.c_ulong),
                    ("Dr7", ctypes.c_ulong),
                    ("FloatSave", ctypes.c_byte * 112),
                    ("SegGs", ctypes.c_ulong),
                    ("SegFs", ctypes.c_ulong),
                    ("SegEs", ctypes.c_ulong),
                    ("SegDs", ctypes.c_ulong),
                    ("Edi", ctypes.c_ulong),
                    ("Esi", ctypes.c_ulong),
                    ("Ebx", ctypes.c_ulong),
                    ("Edx", ctypes.c_ulong),
                    ("Ecx", ctypes.c_ulong),
                    ("Eax", ctypes.c_ulong),
                    ("Ebp", ctypes.c_ulong),
                    ("Eip", ctypes.c_ulong),
                    ("SegCs", ctypes.c_ulong),
                    ("EFlags", ctypes.c_ulong),
                    ("Esp", ctypes.c_ulong),
                    ("SegSs", ctypes.c_ulong),
                    ("ExtendedRegisters", ctypes.c_byte * 512)]

def get_pid_by_name(process_name:str):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return None

def get_libc_path():
    system = platform.system()
    if system == 'Linux':
        return "/lib/x86_64-linux-gnu/libc.so.6"  # Modify this path as needed for Linux
    elif system == 'Windows':
        return "kernel32.dll"  # Windows uses kernel32.dll for process manipulation
    else:
        raise NotImplementedError("Unsupported operating system")

def attach_to_process(pid):
    libc_path = get_libc_path()

    if platform.system() == 'Linux':
        # Attach to the process
        if ctypes.CDLL(libc_path).ptrace(PTRACE_ATTACH, pid, 0, 0) != 0:
            raise ProcessAttachError("Failed to attach to the process")
        
        # Wait for the process to stop
        ctypes.CDLL(libc_path).waitpid(pid, 0, 0)
    elif platform.system() == 'Windows':
        # Attach to the process on Windows (using Windows API)
        process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)  # PROCESS_ALL_ACCESS
        if process_handle == 0:
            raise ProcessAttachError("Failed to open process")

        # Suspend the process
        ctypes.windll.kernel32.SuspendThread(ctypes.windll.kernel32.OpenThread(0x2, False, pid))

    return libc_path

def detach_from_process(pid, libc_path):
    if platform.system() == 'Linux':
        # Detach from the process
        if ctypes.CDLL(libc_path).ptrace(PTRACE_DETACH, pid, 0, 0) != 0:
            raise ProcessDetachError("Failed to detach from the process")
    elif platform.system() == 'Windows':
        # Resume the process on Windows
        ctypes.windll.kernel32.ResumeThread(ctypes.windll.kernel32.OpenThread(0x2, False, pid))

def get_eip(process_name:str):

    pid = get_pid_by_name(process_name)

    if pid is None:
        raise ValueError("Process {} not found".format(process_name))

    libc_path = attach_to_process(pid)

    context = CONTEXT()
    context.ContextFlags = 0x10007
    
    if platform.system() == 'Linux':
        if ctypes.CDLL(libc_path).ptrace(PTRACE_GETREGS, pid, 0, ctypes.byref(context)) != 0:
            raise RegisterReadError("Failed to get register values")
    elif platform.system() == 'Windows':
        # Read the thread context on Windows
        is_wow64 = ctypes.c_int()
        ctypes.windll.kernel32.IsWow64Process(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(is_wow64))

        thread_handle = None
        try:
            if is_wow64.value:
                # 32-bit process on 64-bit Windows
                thread_handle = ctypes.windll.kernel32.OpenThread(0x1F03FF, False, pid)
                ctypes.windll.kernel32.Wow64SuspendThread(thread_handle)
                if not ctypes.windll.kernel32.Wow64GetThreadContext(thread_handle, ctypes.byref(context)):
                    error_code = ctypes.windll.kernel32.GetLastError()
                    raise RegisterReadError("Failed to get thread context (Error code: {})".format(error_code))
            else:
                # 32-bit or 64-bit process on 32-bit Windows
                thread_handle = ctypes.windll.kernel32.OpenThread(0x1F03FF, False, pid)
                ctypes.windll.kernel32.SuspendThread(thread_handle)
                if not ctypes.windll.kernel32.GetThreadContext(thread_handle, ctypes.byref(context)):
                    error_code = ctypes.windll.kernel32.GetLastError()
                    raise RegisterReadError("Failed to get thread context (Error code: {})".format(error_code))
        finally:
            if thread_handle:
                if is_wow64.value:
                    ctypes.windll.kernel32.Wow64ResumeThread(thread_handle)
                else:
                    ctypes.windll.kernel32.ResumeThread(thread_handle)
                ctypes.windll.kernel32.CloseHandle(thread_handle)

    detach_from_process(pid, libc_path)
    
    return context.Eip