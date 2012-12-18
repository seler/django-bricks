# -*- coding: utf-8 -*-
import hashlib
import os
import sys
import re
import subprocess
import logging
import urllib2

import time

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from urllib import urlopen

USE_CELERY = settings.BRICKS_USE_CELERY

if USE_CELERY:
    from celery.decorators import task
    from celery import current_task


safe_storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)
safe_storage = safe_storage_class()

logger = logging.getLogger(__name__)

TEMP_DIR = settings.FILE_UPLOAD_TEMP_DIR
if TEMP_DIR is None:
    import tempfile
    TEMP_DIR = tempfile.gettempdir()


def fetch_file(obj):
    filename = obj.file.name
    logger.info(filename)
    tmpdir = os.path.join(TEMP_DIR, hashlib.md5(filename + str(time.time())).hexdigest())
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    src = safe_storage.open(filename).read()

    tmp_src_path = os.path.join(tmpdir, os.path.basename(filename))
    tmp_src = open(tmp_src_path, 'wb')
    tmp_src.write(src)
    tmp_src.close()
    return tmp_src_path


def clean_files(*filenames):
    for filename in filenames:
        try:
            os.unlink(filename)
            os.removedirs(os.path.dirname(filename))
        except IOError:
            pass
        except OSError:
            pass


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def retrieve_info(filename):
    u"""
    Returns tuple of codec, width and height of given video file
    """
    logger.info('pobieram dane o pliku %s' % filename)

    params = {
        'ffmpeg': getattr(settings, 'FFMPEG', '/usr/bin/ffmpeg'),
        'filename': filename,
        'grep': getattr(settings, 'GREP', '/bin/grep')
    }

    if sys.platform.startswith('win'):
        command1 = "{ffmpeg:s} -i {filename:s} 2>&1".format(**params)
        process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
        command = "{grep:s} 'Duration\|Video:'".format(grep=getattr(settings, 'GREP', '/bin/grep'))
        process = subprocess.Popen(command, stdin=process1.stdout, stdout=subprocess.PIPE)
        process1.stdout.close()
    else:
        command = "{ffmpeg:s} -i {filename:s} 2>&1 | {grep:s} 'Duration\|Video:'".format(**params)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    logger.info(command)
    result = process.communicate()[0]
    logger.info(result)

    duration, video = result.splitlines()
    regexp = '\s*Duration[:]{1}\s*(\d{2,5})[:]{1}' \
             '(\d{2})[:]{1}' \
             '(\d{2}[.]{1}\d{2}).*'
    h, m, s = re.match(regexp, duration).groups()

    duration = int(round(float(s) + int(m) * 60 + int(h) * 3600))

    codec, width, height = re.match('^\s*Stream.*Video:\s*([a-zA-Z0-9]*).*,\s*'
                      '([0-9]{3,4})x([0-9]{3,4}).*$', video).groups()
    width = int(width)
    height = int(height)
    if width % 2:
        width += 1
    if height % 2:
        height += 1
    return codec, width, height, duration


def capture_screenshot(filename, time, width, height):
    logger.info('robie screena z filmu %s' % filename)
    screenshot_filename = os.path.splitext(filename)[0] + '.jpg'
    params = {
        'ffmpeg': getattr(settings, 'FFMPEG', '/usr/bin/ffmpeg'),
        'filename': filename,
        'time': time,
        'width': width,
        'height': height,
        'screenshot_filename': screenshot_filename
    }
    command = "/usr/bin/ffmpeg -i {filename:s} -ss {time} -an -vframes 1 -y -f " \
            "image2 -s {width}x{height} {screenshot_filename} 2>&1".format(**params)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = process.communicate()[0]
    logger.info(result)
    return screenshot_filename


def save_screenshot(filename, obj, time=None, delete=False):
    # generowanie screena
    screenshot_filename = capture_screenshot(filename, obj.screenshot_time,
                                   obj.width, obj.height)
    screenshot_file = open(screenshot_filename, 'rb')
    screenshot_file_content = ContentFile(screenshot_file.read())
    if delete:
        # kasuje stary screenshot
        obj.screenshot.delete()

    obj.screenshot.save(os.path.basename(screenshot_filename), screenshot_file_content)
    screenshot_file.close()
    return screenshot_filename


@task()
def capture_screenshot_task(object_id, time=None):
    # powinno tutaj zostać, bo się nie zaimportuje przy budowaniu
    from .models import Video
    obj = Video.objects.get(id=object_id)

    # pobieram plik do tempa
    filename = fetch_file(obj)

    # generowanie screena
    screenshot_filename = save_screenshot(filename, obj, time=time, delete=True)

    # zapisanie całości zmian
    obj.save()

    # sprzątnięcie zbędnych plików w tempie
    clean_files(screenshot_filename)


def convert_format(filename, format_id, width, height, ext, command):
    logger.info('konwertuje do formatu %d' % format_id)
    filename_base = os.path.splitext(filename)[0] + '_' + str(format_id)
    no_faststart_filename = filename_base + '_nofaststart' + ext
    format_filename = filename_base + ext

    params = {
        'ffmpeg': getattr(settings, 'FFMPEG', '/usr/bin/ffmpeg'),
        'filename': filename,
        'format_filename': no_faststart_filename,
        'format_width': width,
        'format_height': height,
    }
    command = command.format(**params)
    logger.info(command)
    process = subprocess.Popen(command + ' 2>&1', shell=True, stdout=subprocess.PIPE)
    while process.poll() is None:
        output = process.stdout.read(1024)
        regexp = ".*time=\s*(\d+[.]\d+).*"
        try:
            current_time = float(re.findall(regexp, output)[-1])
        except IndexError:
            # nie pasuje regexp
            pass
        else:
            meta = {'current': int(current_time), 'total': 100}
            logger.info('time: %s' % current_time)
            current_task.update_state(state='PROGRESS', meta=meta)

    result = process.communicate()[0]
    logger.info(result)
    logger.info("srutu tutu 2")

    command2 = "{qtfaststart:s} {infile:s} {outfile:s}".format(qtfaststart=getattr(settings, 'QT_FASTSTART', '/usr/bin/qt-faststart'),
                                                              infile=no_faststart_filename,
                                                              outfile=format_filename)
    process2 = subprocess.Popen(command2 + ' 2>&1', shell=True, stdout=subprocess.PIPE)
    result2 = process2.communicate()[0]
    logger.info(result2)

    return format_filename


def save_format(format, filename, obj, width, height, ext, command):
    logger.info("save format")
    from .models import ConvertedVideo
    format_filename = convert_format(filename, format,
                                     width,
                                     height,
                                     ext, command)
    converted_video = ConvertedVideo(video=obj, format=format)
    format_file = open(format_filename, 'rb')
    format_file_content = ContentFile(format_file.read())
    converted_video.file.save(os.path.basename(format_filename), format_file_content)
    converted_video.save()
    format_file.close()
    return format_filename


def save_formats(formats, filename, obj):
    # generowanie formatów video
    logger.info("generowanie formatów video")

    formats_dict = settings.BRICKS_VIDEO_FORMATS
    format_filenames = []
    for i, d in formats_dict.items():
        logger.info("generowanie formatu")
        obj_formats_qs = obj.converted_videos.all()
        obj_formats = list(obj_formats_qs.values_list('format', flat=True))
        logger.info("i:{0}, formats:{1}, obj_formats:{2}".format(i, formats, obj_formats))
        if i in formats and i not in obj_formats:
            logger.info("srutu tutu")
            format_width = d[obj.aspect_ratio]['width']
            format_height = d[obj.aspect_ratio]['height']
            if format_width <= obj.width and format_height <= obj.height:
                format_filename = save_format(i, filename, obj,
                                              format_width,
                                              format_height,
                                              d['extension'],
                                              d['command'])
                format_filenames.append(format_filename)
            else:
                if obj.converted_videos.count() > 0:
                    converted_formats = obj.converted_videos.all() \
                                               .values_list('format', flat=True)
                else:
                    converted_formats = []
                if d['fallback'] not in list(converted_formats) + [None, ]:
                    format_filenames += save_formats((d['fallback'],),
                                                      filename, obj)
    return format_filenames


def process_video(object_id, formats=None):
    """
    TODO: zdecydowac czy ma isc asynchronicznie czy synchronicznie
    """
    return process_video_task.delay(object_id, formats=formats)


@task()
def process_video_task(object_id, formats=None):
    print 'asd'
    """
    for i in range(10):
        meta = {'current': i, 'total': 10}
        logger.info(repr(meta))
        current_task.update_state(state='PROGRESS', meta=meta)
        process_video_task.update_state(state='PROGRESS', meta=meta)
        time.sleep(20)
    """
    ffmpeg = which(getattr(settings, 'FFMPEG', 'fmpeg'))
    #if not ffmpeg:
    #    raise Exception("ffmpeg not installed")

    if formats is None:
        formats = settings.BRICKS_DEFAULT_CONVERTEDVIDEO_FORMATS

    # powinno tutaj zostac, zeby sie nie importowalo przy budowaniu
    from .models import Video
    try:
        obj = Video.objects.get(id=object_id)
    except Video.DoesNotExist, exc:
        process_video_task.retry(exc=exc, countdown=30)

    # pobieram plik do tempa
    filename = fetch_file(obj)

    # pobieram info o pliku
    logger.info("pobieram info o pliku")
    codec, width, height, duration = retrieve_info(filename)
    obj.codec = codec
    obj.width = width
    obj.height = height
    obj.duration = duration
    obj.aspect_ratio = obj._calculate_ratio()

    # generowanie screena
    logger.info("generowanie screena")
    screenshot_filename = save_screenshot(filename, obj)

    # zapisanie całości zmian
    logger.info("zapisanie całości zmian")
    obj.save()

    # generowanie formatów video
    logger.info("generowanie formatów video")
    format_filenames = save_formats(formats, filename, obj)
    # sprzątnięcie zbędnych plików w tempie
    logger.info("sprzątnięcie zbędnych plików w tempie")
    no_faststart_filenames = [u'%s_nofaststart%s' % os.path.splitext(name) for name in format_filenames]
    format_filenames.extend(no_faststart_filenames)
    clean_files(filename, screenshot_filename, *format_filenames)

    # oznaczenie jako skonwertowany
    logger.info("oznaczenie jako skonwertowany")
    obj.ready = True
    obj.save()


def get_file_to_tmp(file_url, video):
    """ pobieranie plik do tempa """
    tmpdir = os.path.join(settings.VIDEO_TMP,
                          hashlib.md5(file_url).hexdigest())
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    response = urlopen(file_url)
    video_file_content = response.read()
    tmp_src_path = os.path.join(tmpdir, os.path.basename(file_url))
    tmp_src = open(tmp_src_path, 'wb')
    tmp_src.write(video_file_content)
    tmp_src.close()
    video.file.save(os.path.basename(tmp_src_path),
                    ContentFile(video_file_content))
    video.save()
    return tmp_src_path


def create_formats(video, video_filename):
    u""" generowanie formatów video """
    formats = (settings.BRICKS_DEFAULT_CONVERTEDVIDEO_FORMAT,)
    format_filenames = save_formats(formats, video_filename, video)
    # oznaczenie video jako skonwertowany
    video.ready = True
    video.save()

    return format_filenames
