import sys
import warnings

import winerror
import win32api
import win32job

g_hjob = None


def create_job(job_name='', breakaway='silent'):
    hjob = win32job.CreateJobObject(None, job_name)
    if breakaway:
        info = win32job.QueryInformationJobObject(
            hjob,
            win32job.JobObjectExtendedLimitInformation
        )
        if breakaway == 'silent':
            info['BasicLimitInformation']['LimitFlags'] |= (
                win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK
            )
        else:
            info['BasicLimitInformation']['LimitFlags'] |= (
                win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK
            )
        win32job.SetInformationJobObject(
            hjob,
            win32job.JobObjectExtendedLimitInformation,
            info
        )
    return hjob


def assign_job(hjob):
    global g_hjob
    hprocess = win32api.GetCurrentProcess()
    try:
        win32job.AssignProcessToJobObject(hjob, hprocess)
        g_hjob = hjob
    except win32job.error as e:
        if (e.winerror != winerror.ERROR_ACCESS_DENIED or
            sys.getwindowsversion() >= (6, 2) or
                not win32job.IsProcessInJob(hprocess, None)):
            raise
        warnings.warn('The process is already in a job. Nested jobs are not '
                      'supported prior to Windows 8.')


def limit_memory(memory_limit):
    assign_job(create_job())

    if g_hjob is None:
        return
    info = win32job.QueryInformationJobObject(
        g_hjob,
        win32job.JobObjectExtendedLimitInformation
    )
    info['ProcessMemoryLimit'] = memory_limit
    info['BasicLimitInformation']['LimitFlags'] |= (
        win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY
    )
    win32job.SetInformationJobObject(
        g_hjob,
        win32job.JobObjectExtendedLimitInformation,
        info
    )


class resource:
    # To imitate standard resource library.
    # Which is unix exclusive.

    RLIMIT_AS = None

    @classmethod
    def getrlimit(cls, *args, **kwargs):
        return (0, 0)

    @classmethod
    def setrlimit(cls, temp, value, *args, **kwargs):
        limit_value = value[0]
        limit_memory(limit_value)
