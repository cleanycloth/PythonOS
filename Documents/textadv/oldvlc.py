import ctypes
from ctypes.util import find_library
import os
import sys
import functools
from inspect import getargspec
__version__ = "N/A"
build_date  = "Fri Oct  7 12:04:48 2016"
DEFAULT_ENCODING = 'utf-8'

if sys.version_info[0] > 2:
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
    PYTHON3 = True
    def str_to_bytes(s):


        if isinstance(s, str):
            return bytes(s, DEFAULT_ENCODING)
        else:
            return s

    def bytes_to_str(b):


        if isinstance(b, bytes):
            return b.decode(DEFAULT_ENCODING)
        else:
            return b
else:
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring
    PYTHON3 = False
    def str_to_bytes(s):


        if isinstance(s, unicode):
            return s.encode(DEFAULT_ENCODING)
        else:
            return s

    def bytes_to_str(b):


        if isinstance(b, str):
            return unicode(b, DEFAULT_ENCODING)
        else:
            return b



_internal_guard = object()

def find_lib():
    dll = None
    plugin_path = None
    if sys.platform.startswith('linux'):
        p = find_library('vlc')
        try:
            dll = ctypes.CDLL(p)
        except OSError:
            dll = ctypes.CDLL('libvlc.so.5')
    elif sys.platform.startswith('win'):
        libname = 'libvlc.dll'
        p = find_library(libname)
        if p is None:
            try:

                if PYTHON3:
                    import winreg as w
                else:
                    import _winreg as w
                for r in w.HKEY_LOCAL_MACHINE, w.HKEY_CURRENT_USER:
                    try:
                        r = w.OpenKey(r, 'Software\\VideoLAN\\VLC')
                        plugin_path, _ = w.QueryValueEx(r, 'InstallDir')
                        w.CloseKey(r)
                        break
                    except w.error:
                        pass
            except ImportError:
                pass
            if plugin_path is None:

                programfiles = os.environ["ProgramFiles"]
                homedir = os.environ["HOMEDRIVE"]
                for p in ('{programfiles}\\VideoLan{libname}', '{homedir}:\\VideoLan{libname}',
                          '{programfiles}{libname}',           '{homedir}:{libname}'):
                    p = p.format(homedir = homedir,
                                 programfiles = programfiles,
                                 libname = '\\VLC\\' + libname)
                    if os.path.exists(p):
                        plugin_path = os.path.dirname(p)
                        break
            if plugin_path is not None:
                p = os.getcwd()
                os.chdir(plugin_path)

                dll = ctypes.CDLL(libname)

                os.chdir(p)
            else:
                dll = ctypes.CDLL(libname)
        else:
            plugin_path = os.path.dirname(p)
            dll = ctypes.CDLL(p)

    elif sys.platform.startswith('darwin'):

        d = '/Applications/VLC.app/Contents/MacOS/'
        p = d + 'lib/libvlc.dylib'
        if os.path.exists(p):
            dll = ctypes.CDLL(p)
            for p in ('modules', 'plugins'):
                p = d + p
                if os.path.isdir(p):
                    plugin_path = p
                    break
        else:
            dll = ctypes.CDLL('libvlc.dylib')

    else:
        raise NotImplementedError('%s: %s not supported' % (sys.argv[0], sys.platform))

    return (dll, plugin_path)


dll, plugin_path  = find_lib()

class VLCException(Exception):


    pass

try:
    _Ints = (int, long)
except NameError:
    _Ints =  int
_Seqs = (list, tuple)


class memoize_parameterless(object):


    def __init__(self, func):
        self.func = func
        self._cache = {}

    def __call__(self, obj):
        try:
            return self._cache[obj]
        except KeyError:
            v = self._cache[obj] = self.func(obj)
            return v

    def __repr__(self):


        return self.func.__doc__

    def __get__(self, obj, objtype):


      return functools.partial(self.__call__, obj)



_default_instance = None

def get_default_instance():


    global _default_instance
    if _default_instance is None:
        _default_instance = Instance()
    return _default_instance

_Cfunctions = {}
_Globals = globals()

def _Cfunction(name, flags, errcheck, *types):


    if hasattr(dll, name) and name in _Globals:
        p = ctypes.CFUNCTYPE(*types)
        f = p((name, dll), flags)
        if errcheck is not None:
            f.errcheck = errcheck



        if __debug__:
            _Cfunctions[name] = f
        else:
            _Globals[name] = f
        return f
    raise NameError('no function %r' % (name,))

def _Cobject(cls, ctype):


    o = object.__new__(cls)
    o._as_parameter_ = ctype
    return o

def _Constructor(cls, ptr=_internal_guard):


    if ptr == _internal_guard:
        raise VLCException("(INTERNAL) ctypes class. You should get references for this class through methods of the LibVLC API.")
    if ptr is None or ptr == 0:
        return None
    return _Cobject(cls, ctypes.c_void_p(ptr))

class _Cstruct(ctypes.Structure):


    _fields_ = []

    def __str__(self):
        l = [' %s:\t%s' % (n, getattr(self, n)) for n, _ in self._fields_]
        return '\n'.join([self.__class__.__name__] + l)

    def __repr__(self):
        return '%s.%s' % (self.__class__.__module__, self)

class _Ctype(object):


    @staticmethod
    def from_param(this):


        if this is None:
            return None
        return this._as_parameter_

class ListPOINTER(object):


    def __init__(self, etype):
        self.etype = etype

    def from_param(self, param):
        if isinstance(param, _Seqs):
            return (self.etype * len(param))(*param)


def string_result(result, func, arguments):
    if result:

        s = bytes_to_str(ctypes.string_at(result))

        libvlc_free(result)
        return s
    return None

def class_result(classname):


    def wrap_errcheck(result, func, arguments):
        if result is None:
            return None
        return classname(result)
    return wrap_errcheck


class Log(ctypes.Structure):
    pass
Log_ptr = ctypes.POINTER(Log)



class FILE(ctypes.Structure):
    pass
FILE_ptr = ctypes.POINTER(FILE)

if PYTHON3:
    PyFile_FromFd = ctypes.pythonapi.PyFile_FromFd
    PyFile_FromFd.restype = ctypes.py_object
    PyFile_FromFd.argtypes = [ctypes.c_int,
                              ctypes.c_char_p,
                              ctypes.c_char_p,
                              ctypes.c_int,
                              ctypes.c_char_p,
                              ctypes.c_char_p,
                              ctypes.c_char_p,
                              ctypes.c_int ]

    PyFile_AsFd = ctypes.pythonapi.PyObject_AsFileDescriptor
    PyFile_AsFd.restype = ctypes.c_int
    PyFile_AsFd.argtypes = [ctypes.py_object]
else:
    PyFile_FromFile = ctypes.pythonapi.PyFile_FromFile
    PyFile_FromFile.restype = ctypes.py_object
    PyFile_FromFile.argtypes = [FILE_ptr,
                                ctypes.c_char_p,
                                ctypes.c_char_p,
                                ctypes.CFUNCTYPE(ctypes.c_int, FILE_ptr)]

    PyFile_AsFile = ctypes.pythonapi.PyFile_AsFile
    PyFile_AsFile.restype = FILE_ptr
    PyFile_AsFile.argtypes = [ctypes.py_object]



class _Enum(ctypes.c_uint):
    '''(INTERNAL) Base class
    '''
    _enum_names_ = {}

    def __str__(self):
        n = self._enum_names_.get(self.value, '') or ('FIXME_(%r)' % (self.value,))
        return '.'.join((self.__class__.__name__, n))

    def __hash__(self):
        return self.value

    def __repr__(self):
        return '.'.join((self.__class__.__module__, self.__str__()))

    def __eq__(self, other):
        return ( (isinstance(other, _Enum) and self.value == other.value)
              or (isinstance(other, _Ints) and self.value == other) )

    def __ne__(self, other):
        return not self.__eq__(other)

class LogLevel(_Enum):
    '''Logging messages level.
\note future libvlc versions may define new levels.
    '''
    _enum_names_ = {
        0: 'DEBUG',
        2: 'NOTICE',
        3: 'WARNING',
        4: 'ERROR',
    }
LogLevel.DEBUG   = LogLevel(0)
LogLevel.ERROR   = LogLevel(4)
LogLevel.NOTICE  = LogLevel(2)
LogLevel.WARNING = LogLevel(3)

class DialogQuestionType(_Enum):
    '''@defgroup libvlc_dialog libvlc dialog
@ingroup libvlc
@{
@file
libvlc dialog external api.
    '''
    _enum_names_ = {
        0: 'NORMAL',
        1: 'WARNING',
        2: 'CRITICAL',
    }
DialogQuestionType.CRITICAL = DialogQuestionType(2)
DialogQuestionType.NORMAL   = DialogQuestionType(0)
DialogQuestionType.WARNING  = DialogQuestionType(1)

class EventType(_Enum):
    '''Event types.
    '''
    _enum_names_ = {
        0: 'MediaMetaChanged',
        1: 'MediaSubItemAdded',
        2: 'MediaDurationChanged',
        3: 'MediaParsedChanged',
        4: 'MediaFreed',
        5: 'MediaStateChanged',
        6: 'MediaSubItemTreeAdded',
        0x100: 'MediaPlayerMediaChanged',
        257: 'MediaPlayerNothingSpecial',
        258: 'MediaPlayerOpening',
        259: 'MediaPlayerBuffering',
        260: 'MediaPlayerPlaying',
        261: 'MediaPlayerPaused',
        262: 'MediaPlayerStopped',
        263: 'MediaPlayerForward',
        264: 'MediaPlayerBackward',
        265: 'MediaPlayerEndReached',
        266: 'MediaPlayerEncounteredError',
        267: 'MediaPlayerTimeChanged',
        268: 'MediaPlayerPositionChanged',
        269: 'MediaPlayerSeekableChanged',
        270: 'MediaPlayerPausableChanged',
        271: 'MediaPlayerTitleChanged',
        272: 'MediaPlayerSnapshotTaken',
        273: 'MediaPlayerLengthChanged',
        274: 'MediaPlayerVout',
        275: 'MediaPlayerScrambledChanged',
        276: 'MediaPlayerESAdded',
        277: 'MediaPlayerESDeleted',
        278: 'MediaPlayerESSelected',
        279: 'MediaPlayerCorked',
        280: 'MediaPlayerUncorked',
        281: 'MediaPlayerMuted',
        282: 'MediaPlayerUnmuted',
        283: 'MediaPlayerAudioVolume',
        284: 'MediaPlayerAudioDevice',
        285: 'MediaPlayerChapterChanged',
        0x200: 'MediaListItemAdded',
        513: 'MediaListWillAddItem',
        514: 'MediaListItemDeleted',
        515: 'MediaListWillDeleteItem',
        516: 'MediaListEndReached',
        0x300: 'MediaListViewItemAdded',
        769: 'MediaListViewWillAddItem',
        770: 'MediaListViewItemDeleted',
        771: 'MediaListViewWillDeleteItem',
        0x400: 'MediaListPlayerPlayed',
        1025: 'MediaListPlayerNextItemSet',
        1026: 'MediaListPlayerStopped',
        0x500: 'MediaDiscovererStarted',
        1281: 'MediaDiscovererEnded',
        1282: 'RendererDiscovererItemAdded',
        1283: 'RendererDiscovererItemDeleted',
        0x600: 'VlmMediaAdded',
        1537: 'VlmMediaRemoved',
        1538: 'VlmMediaChanged',
        1539: 'VlmMediaInstanceStarted',
        1540: 'VlmMediaInstanceStopped',
        1541: 'VlmMediaInstanceStatusInit',
        1542: 'VlmMediaInstanceStatusOpening',
        1543: 'VlmMediaInstanceStatusPlaying',
        1544: 'VlmMediaInstanceStatusPause',
        1545: 'VlmMediaInstanceStatusEnd',
        1546: 'VlmMediaInstanceStatusError',
    }
EventType.MediaDiscovererEnded          = EventType(1281)
EventType.MediaDiscovererStarted        = EventType(0x500)
EventType.MediaDurationChanged          = EventType(2)
EventType.MediaFreed                    = EventType(4)
EventType.MediaListEndReached           = EventType(516)
EventType.MediaListItemAdded            = EventType(0x200)
EventType.MediaListItemDeleted          = EventType(514)
EventType.MediaListPlayerNextItemSet    = EventType(1025)
EventType.MediaListPlayerPlayed         = EventType(0x400)
EventType.MediaListPlayerStopped        = EventType(1026)
EventType.MediaListViewItemAdded        = EventType(0x300)
EventType.MediaListViewItemDeleted      = EventType(770)
EventType.MediaListViewWillAddItem      = EventType(769)
EventType.MediaListViewWillDeleteItem   = EventType(771)
EventType.MediaListWillAddItem          = EventType(513)
EventType.MediaListWillDeleteItem       = EventType(515)
EventType.MediaMetaChanged              = EventType(0)
EventType.MediaParsedChanged            = EventType(3)
EventType.MediaPlayerAudioDevice        = EventType(284)
EventType.MediaPlayerAudioVolume        = EventType(283)
EventType.MediaPlayerBackward           = EventType(264)
EventType.MediaPlayerBuffering          = EventType(259)
EventType.MediaPlayerChapterChanged     = EventType(285)
EventType.MediaPlayerCorked             = EventType(279)
EventType.MediaPlayerESAdded            = EventType(276)
EventType.MediaPlayerESDeleted          = EventType(277)
EventType.MediaPlayerESSelected         = EventType(278)
EventType.MediaPlayerEncounteredError   = EventType(266)
EventType.MediaPlayerEndReached         = EventType(265)
EventType.MediaPlayerForward            = EventType(263)
EventType.MediaPlayerLengthChanged      = EventType(273)
EventType.MediaPlayerMediaChanged       = EventType(0x100)
EventType.MediaPlayerMuted              = EventType(281)
EventType.MediaPlayerNothingSpecial     = EventType(257)
EventType.MediaPlayerOpening            = EventType(258)
EventType.MediaPlayerPausableChanged    = EventType(270)
EventType.MediaPlayerPaused             = EventType(261)
EventType.MediaPlayerPlaying            = EventType(260)
EventType.MediaPlayerPositionChanged    = EventType(268)
EventType.MediaPlayerScrambledChanged   = EventType(275)
EventType.MediaPlayerSeekableChanged    = EventType(269)
EventType.MediaPlayerSnapshotTaken      = EventType(272)
EventType.MediaPlayerStopped            = EventType(262)
EventType.MediaPlayerTimeChanged        = EventType(267)
EventType.MediaPlayerTitleChanged       = EventType(271)
EventType.MediaPlayerUncorked           = EventType(280)
EventType.MediaPlayerUnmuted            = EventType(282)
EventType.MediaPlayerVout               = EventType(274)
EventType.MediaStateChanged             = EventType(5)
EventType.MediaSubItemAdded             = EventType(1)
EventType.MediaSubItemTreeAdded         = EventType(6)
EventType.RendererDiscovererItemAdded   = EventType(1282)
EventType.RendererDiscovererItemDeleted = EventType(1283)
EventType.VlmMediaAdded                 = EventType(0x600)
EventType.VlmMediaChanged               = EventType(1538)
EventType.VlmMediaInstanceStarted       = EventType(1539)
EventType.VlmMediaInstanceStatusEnd     = EventType(1545)
EventType.VlmMediaInstanceStatusError   = EventType(1546)
EventType.VlmMediaInstanceStatusInit    = EventType(1541)
EventType.VlmMediaInstanceStatusOpening = EventType(1542)
EventType.VlmMediaInstanceStatusPause   = EventType(1544)
EventType.VlmMediaInstanceStatusPlaying = EventType(1543)
EventType.VlmMediaInstanceStopped       = EventType(1540)
EventType.VlmMediaRemoved               = EventType(1537)

class Meta(_Enum):
    '''Meta data types.
    '''
    _enum_names_ = {
        0: 'Title',
        1: 'Artist',
        2: 'Genre',
        3: 'Copyright',
        4: 'Album',
        5: 'TrackNumber',
        6: 'Description',
        7: 'Rating',
        8: 'Date',
        9: 'Setting',
        10: 'URL',
        11: 'Language',
        12: 'NowPlaying',
        13: 'Publisher',
        14: 'EncodedBy',
        15: 'ArtworkURL',
        16: 'TrackID',
        17: 'TrackTotal',
        18: 'Director',
        19: 'Season',
        20: 'Episode',
        21: 'ShowName',
        22: 'Actors',
        23: 'AlbumArtist',
        24: 'DiscNumber',
        25: 'DiscTotal',
    }
Meta.Actors      = Meta(22)
Meta.Album       = Meta(4)
Meta.AlbumArtist = Meta(23)
Meta.Artist      = Meta(1)
Meta.ArtworkURL  = Meta(15)
Meta.Copyright   = Meta(3)
Meta.Date        = Meta(8)
Meta.Description = Meta(6)
Meta.Director    = Meta(18)
Meta.DiscNumber  = Meta(24)
Meta.DiscTotal   = Meta(25)
Meta.EncodedBy   = Meta(14)
Meta.Episode     = Meta(20)
Meta.Genre       = Meta(2)
Meta.Language    = Meta(11)
Meta.NowPlaying  = Meta(12)
Meta.Publisher   = Meta(13)
Meta.Rating      = Meta(7)
Meta.Season      = Meta(19)
Meta.Setting     = Meta(9)
Meta.ShowName    = Meta(21)
Meta.Title       = Meta(0)
Meta.TrackID     = Meta(16)
Meta.TrackNumber = Meta(5)
Meta.TrackTotal  = Meta(17)
Meta.URL         = Meta(10)

class State(_Enum):
    '''Note the order of libvlc_state_t enum must match exactly the order of
See mediacontrol_playerstatus, See input_state_e enums,
and videolan.libvlc.state (at bindings/cil/src/media.cs).
expected states by web plugins are:
idle/close=0, opening=1, playing=3, paused=4,
stopping=5, ended=6, error=7.
    '''
    _enum_names_ = {
        0: 'NothingSpecial',
        1: 'Opening',
        2: 'Buffering',
        3: 'Playing',
        4: 'Paused',
        5: 'Stopped',
        6: 'Ended',
        7: 'Error',
    }
State.Buffering      = State(2)
State.Ended          = State(6)
State.Error          = State(7)
State.NothingSpecial = State(0)
State.Opening        = State(1)
State.Paused         = State(4)
State.Playing        = State(3)
State.Stopped        = State(5)

class TrackType(_Enum):
    '''N/A
    '''
    _enum_names_ = {
        -1: 'unknown',
        0: 'audio',
        1: 'video',
        2: 'text',
    }
TrackType.audio   = TrackType(0)
TrackType.text    = TrackType(2)
TrackType.unknown = TrackType(-1)
TrackType.video   = TrackType(1)

class MediaType(_Enum):
    '''Media type
See libvlc_media_get_type.
    '''
    _enum_names_ = {
        0: 'unknown',
        1: 'file',
        2: 'directory',
        3: 'disc',
        4: 'stream',
        5: 'playlist',
    }
MediaType.directory = MediaType(2)
MediaType.disc      = MediaType(3)
MediaType.file      = MediaType(1)
MediaType.playlist  = MediaType(5)
MediaType.stream    = MediaType(4)
MediaType.unknown   = MediaType(0)

class MediaParseFlag(_Enum):
    '''Parse flags used by libvlc_media_parse_with_options()
See libvlc_media_parse_with_options.
    '''
    _enum_names_ = {
        0x0: 'local',
        0x1: 'network',
        0x2: 'local',
        0x4: 'network',
        0x8: 'interact',
    }
MediaParseFlag.interact = MediaParseFlag(0x8)
MediaParseFlag.local    = MediaParseFlag(0x0)
MediaParseFlag.local    = MediaParseFlag(0x2)
MediaParseFlag.network  = MediaParseFlag(0x1)
MediaParseFlag.network  = MediaParseFlag(0x4)

class MediaParsedStatus(_Enum):
    '''Parse status used sent by libvlc_media_parse_with_options() or returned by
libvlc_media_get_parsed_status()
See libvlc_media_parse_with_options
See libvlc_media_get_parsed_status.
    '''
    _enum_names_ = {
        1: 'skipped',
        2: 'failed',
        3: 'timeout',
        4: 'done',
    }
MediaParsedStatus.done    = MediaParsedStatus(4)
MediaParsedStatus.failed  = MediaParsedStatus(2)
MediaParsedStatus.skipped = MediaParsedStatus(1)
MediaParsedStatus.timeout = MediaParsedStatus(3)

class MediaSlaveType(_Enum):
    '''Type of a media slave: subtitle or audio.
    '''
    _enum_names_ = {
        0: 'subtitle',
        1: 'audio',
    }
MediaSlaveType.audio    = MediaSlaveType(1)
MediaSlaveType.subtitle = MediaSlaveType(0)

class MediaDiscovererCategory(_Enum):
    '''Category of a media discoverer
See libvlc_media_discoverer_list_get().
    '''
    _enum_names_ = {
        0: 'devices',
        1: 'lan',
        2: 'podcasts',
        3: 'localdirs',
    }
MediaDiscovererCategory.devices   = MediaDiscovererCategory(0)
MediaDiscovererCategory.lan       = MediaDiscovererCategory(1)
MediaDiscovererCategory.localdirs = MediaDiscovererCategory(3)
MediaDiscovererCategory.podcasts  = MediaDiscovererCategory(2)

class PlaybackMode(_Enum):
    '''Defines playback modes for playlist.
    '''
    _enum_names_ = {
        0: 'default',
        1: 'loop',
        2: 'repeat',
    }
PlaybackMode.default = PlaybackMode(0)
PlaybackMode.loop    = PlaybackMode(1)
PlaybackMode.repeat  = PlaybackMode(2)

class VideoMarqueeOption(_Enum):
    '''Marq options definition.
    '''
    _enum_names_ = {
        0: 'Enable',
        1: 'Text',
        2: 'Color',
        3: 'Opacity',
        4: 'Position',
        5: 'Refresh',
        6: 'Size',
        7: 'Timeout',
        8: 'marquee_X',
        9: 'marquee_Y',
    }
VideoMarqueeOption.Color     = VideoMarqueeOption(2)
VideoMarqueeOption.Enable    = VideoMarqueeOption(0)
VideoMarqueeOption.Opacity   = VideoMarqueeOption(3)
VideoMarqueeOption.Position  = VideoMarqueeOption(4)
VideoMarqueeOption.Refresh   = VideoMarqueeOption(5)
VideoMarqueeOption.Size      = VideoMarqueeOption(6)
VideoMarqueeOption.Text      = VideoMarqueeOption(1)
VideoMarqueeOption.Timeout   = VideoMarqueeOption(7)
VideoMarqueeOption.marquee_X = VideoMarqueeOption(8)
VideoMarqueeOption.marquee_Y = VideoMarqueeOption(9)

class NavigateMode(_Enum):
    '''Navigation mode.
    '''
    _enum_names_ = {
        0: 'activate',
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right',
        5: 'popup',
    }
NavigateMode.activate = NavigateMode(0)
NavigateMode.down     = NavigateMode(2)
NavigateMode.left     = NavigateMode(3)
NavigateMode.popup    = NavigateMode(5)
NavigateMode.right    = NavigateMode(4)
NavigateMode.up       = NavigateMode(1)

class Position(_Enum):
    '''Enumeration of values used to set position (e.g. of video title).
    '''
    _enum_names_ = {
        -1: 'disable',
        0: 'center',
        1: 'left',
        2: 'right',
        3: 'top',
        4: 'left',
        5: 'right',
        6: 'bottom',
        7: 'left',
        8: 'right',
    }
Position.bottom  = Position(6)
Position.center  = Position(0)
Position.disable = Position(-1)
Position.left    = Position(1)
Position.left    = Position(4)
Position.left    = Position(7)
Position.right   = Position(2)
Position.right   = Position(5)
Position.right   = Position(8)
Position.top     = Position(3)

class AudioOutputDeviceTypes(_Enum):
    '''Audio device types.
    '''
    _enum_names_ = {
        -1: 'Error',
        1: 'Mono',
        2: 'Stereo',
        4: '_2F2R',
        5: '_3F2R',
        6: '_5_1',
        7: '_6_1',
        8: '_7_1',
        10: 'SPDIF',
    }
AudioOutputDeviceTypes.Error  = AudioOutputDeviceTypes(-1)
AudioOutputDeviceTypes.Mono   = AudioOutputDeviceTypes(1)
AudioOutputDeviceTypes.SPDIF  = AudioOutputDeviceTypes(10)
AudioOutputDeviceTypes.Stereo = AudioOutputDeviceTypes(2)
AudioOutputDeviceTypes._2F2R  = AudioOutputDeviceTypes(4)
AudioOutputDeviceTypes._3F2R  = AudioOutputDeviceTypes(5)
AudioOutputDeviceTypes._5_1   = AudioOutputDeviceTypes(6)
AudioOutputDeviceTypes._6_1   = AudioOutputDeviceTypes(7)
AudioOutputDeviceTypes._7_1   = AudioOutputDeviceTypes(8)

class AudioOutputChannel(_Enum):
    '''Audio channels.
    '''
    _enum_names_ = {
        -1: 'Error',
        1: 'Stereo',
        2: 'RStereo',
        3: 'Left',
        4: 'Right',
        5: 'Dolbys',
    }
AudioOutputChannel.Dolbys  = AudioOutputChannel(5)
AudioOutputChannel.Error   = AudioOutputChannel(-1)
AudioOutputChannel.Left    = AudioOutputChannel(3)
AudioOutputChannel.RStereo = AudioOutputChannel(2)
AudioOutputChannel.Right   = AudioOutputChannel(4)
AudioOutputChannel.Stereo  = AudioOutputChannel(1)

class MediaPlayerRole(_Enum):
    '''Media player roles.
\version libvlc 3.0.0 and later.
see \ref libvlc_media_player_set_role().
    '''
    _enum_names_ = {
        0: '_None',
        1: 'Music',
        2: 'Video',
        3: 'Communication',
        4: 'Game',
        5: 'Notification',
        6: 'Animation',
        7: 'Production',
        8: 'Accessibility',
        9: 'Test',
    }
MediaPlayerRole.Accessibility = MediaPlayerRole(8)
MediaPlayerRole.Animation     = MediaPlayerRole(6)
MediaPlayerRole.Communication = MediaPlayerRole(3)
MediaPlayerRole.Game          = MediaPlayerRole(4)
MediaPlayerRole.Music         = MediaPlayerRole(1)
MediaPlayerRole.Notification  = MediaPlayerRole(5)
MediaPlayerRole.Production    = MediaPlayerRole(7)
MediaPlayerRole.Test          = MediaPlayerRole(9)
MediaPlayerRole.Video         = MediaPlayerRole(2)
MediaPlayerRole._None         = MediaPlayerRole(0)

class AudioOutput(_Cstruct):

    def __str__(self):
        return '%s(%s:%s)' % (self.__class__.__name__, self.name, self.description)

AudioOutput._fields_ = [
    ('name',        ctypes.c_char_p),
    ('description', ctypes.c_char_p),
    ('next',        ctypes.POINTER(AudioOutput)),
    ]

class LogMessage(_Cstruct):
    _fields_ = [
        ('size',     ctypes.c_uint  ),
        ('severity', ctypes.c_int   ),
        ('type',     ctypes.c_char_p),
        ('name',     ctypes.c_char_p),
        ('header',   ctypes.c_char_p),
        ('message',  ctypes.c_char_p),
    ]

    def __init__(self):
        super(LogMessage, self).__init__()
        self.size = ctypes.sizeof(self)

    def __str__(self):
        return '%s(%d:%s): %s' % (self.__class__.__name__, self.severity, self.type, self.message)

class MediaEvent(_Cstruct):
    _fields_ = [
        ('media_name',    ctypes.c_char_p),
        ('instance_name', ctypes.c_char_p),
    ]

class MediaStats(_Cstruct):
    _fields_ = [
        ('read_bytes',          ctypes.c_int  ),
        ('input_bitrate',       ctypes.c_float),
        ('demux_read_bytes',    ctypes.c_int  ),
        ('demux_bitrate',       ctypes.c_float),
        ('demux_corrupted',     ctypes.c_int  ),
        ('demux_discontinuity', ctypes.c_int  ),
        ('decoded_video',       ctypes.c_int  ),
        ('decoded_audio',       ctypes.c_int  ),
        ('displayed_pictures',  ctypes.c_int  ),
        ('lost_pictures',       ctypes.c_int  ),
        ('played_abuffers',     ctypes.c_int  ),
        ('lost_abuffers',       ctypes.c_int  ),
        ('sent_packets',        ctypes.c_int  ),
        ('sent_bytes',          ctypes.c_int  ),
        ('send_bitrate',        ctypes.c_float),
    ]

class MediaTrackInfo(_Cstruct):
    _fields_ = [
        ('codec',              ctypes.c_uint32),
        ('id',                 ctypes.c_int   ),
        ('type',               TrackType      ),
        ('profile',            ctypes.c_int   ),
        ('level',              ctypes.c_int   ),
        ('channels_or_height', ctypes.c_uint  ),
        ('rate_or_width',      ctypes.c_uint  ),
    ]

class AudioTrack(_Cstruct):
    _fields_ = [
        ('channels', ctypes.c_uint),
        ('rate', ctypes.c_uint),
        ]

class VideoTrack(_Cstruct):
    _fields_ = [
        ('height', ctypes.c_uint),
        ('width', ctypes.c_uint),
        ('sar_num', ctypes.c_uint),
        ('sar_den', ctypes.c_uint),
        ('frame_rate_num', ctypes.c_uint),
        ('frame_rate_den', ctypes.c_uint),
        ]

class SubtitleTrack(_Cstruct):
    _fields_ = [
        ('encoding', ctypes.c_char_p),
        ]

class MediaTrackTracks(ctypes.Union):
    _fields_ = [
        ('audio', ctypes.POINTER(AudioTrack)),
        ('video', ctypes.POINTER(VideoTrack)),
        ('subtitle', ctypes.POINTER(SubtitleTrack)),
        ]

class MediaTrack(_Cstruct):
    _anonymous_ = ("u",)
    _fields_ = [
        ('codec',              ctypes.c_uint32),
        ('original_fourcc',    ctypes.c_uint32),
        ('id',                 ctypes.c_int   ),
        ('type',               TrackType      ),
        ('profile',            ctypes.c_int   ),
        ('level',              ctypes.c_int   ),

        ('u',                  MediaTrackTracks),
        ('bitrate',            ctypes.c_uint),
        ('language',           ctypes.c_char_p),
        ('description',        ctypes.c_char_p),
        ]

class PlaylistItem(_Cstruct):
    _fields_ = [
        ('id',   ctypes.c_int   ),
        ('uri',  ctypes.c_char_p),
        ('name', ctypes.c_char_p),
    ]

    def __str__(self):
        return '%s'

class Position(object):
    Center       = 0
    Left         = 1
    CenterLeft   = 1
    Right        = 2
    CenterRight  = 2
    Top          = 4
    TopCenter    = 4
    TopLeft      = 5
    TopRight     = 6
    Bottom       = 8
    BottomCenter = 8
    BottomLeft   = 9
    BottomRight  = 10
    def __init__(self, *unused):
        raise TypeError('constants only')
    def __setattr__(self, *unused):
        raise TypeError('immutable constants')

class Rectangle(_Cstruct):
    _fields_ = [
        ('top',    ctypes.c_int),
        ('left',   ctypes.c_int),
        ('bottom', ctypes.c_int),
        ('right',  ctypes.c_int),
    ]

class TrackDescription(_Cstruct):

    def __str__(self):
        return '%s(%d:%s)' % (self.__class__.__name__, self.id, self.name)

TrackDescription._fields_ = [
    ('id',   ctypes.c_int   ),
    ('name', ctypes.c_char_p),
    ('next', ctypes.POINTER(TrackDescription)),
    ]

def track_description_list(head):


    r = []
    if head:
        item = head
        while item:
            item = item.contents
            r.append((item.id, item.name))
            item = item.next
        try:
            libvlc_track_description_release(head)
        except NameError:
            libvlc_track_description_list_release(head)

    return r

class EventUnion(ctypes.Union):
    _fields_ = [
        ('meta_type',    ctypes.c_uint    ),
        ('new_child',    ctypes.c_uint    ),
        ('new_duration', ctypes.c_longlong),
        ('new_status',   ctypes.c_int     ),
        ('media',        ctypes.c_void_p  ),
        ('new_state',    ctypes.c_uint    ),

        ('new_cache', ctypes.c_float   ),
        ('new_position', ctypes.c_float   ),
        ('new_time',     ctypes.c_longlong),
        ('new_title',    ctypes.c_int     ),
        ('new_seekable', ctypes.c_longlong),
        ('new_pausable', ctypes.c_longlong),
        ('new_scrambled', ctypes.c_longlong),
        ('new_count', ctypes.c_longlong),

        ('filename',     ctypes.c_char_p  ),
        ('new_length',   ctypes.c_longlong),
        ('media_event',  MediaEvent       ),
    ]

class Event(_Cstruct):
    _fields_ = [
        ('type',   EventType      ),
        ('object', ctypes.c_void_p),
        ('u',      EventUnion     ),
    ]

class ModuleDescription(_Cstruct):

    def __str__(self):
        return '%s %s (%s)' % (self.__class__.__name__, self.shortname, self.name)

ModuleDescription._fields_ = [
    ('name',      ctypes.c_char_p),
    ('shortname', ctypes.c_char_p),
    ('longname',  ctypes.c_char_p),
    ('help',      ctypes.c_char_p),
    ('next',      ctypes.POINTER(ModuleDescription)),
    ]

def module_description_list(head):


    r = []
    if head:
        item = head
        while item:
            item = item.contents
            r.append((item.name, item.shortname, item.longname, item.help))
            item = item.next
        libvlc_module_description_list_release(head)
    return r

class AudioOutputDevice(_Cstruct):

    def __str__(self):
        return '%s(%d:%s)' % (self.__class__.__name__, self.id, self.name)

AudioOutputDevice._fields_ = [
    ('next', ctypes.POINTER(AudioOutputDevice)),
    ('device',   ctypes.c_char_p   ),
    ('description', ctypes.c_char_p),
    ]

class TitleDescription(_Cstruct):
    _fields = [
        ('duration', ctypes.c_longlong),
        ('name', ctypes.c_char_p),
        ('menu', ctypes.c_bool),
    ]

class ChapterDescription(_Cstruct):
    _fields = [
        ('time_offset', ctypes.c_longlong),
        ('duration', ctypes.c_longlong),
        ('name', ctypes.c_char_p),
    ]



if 'MediaSlaveType' in locals():
    class MediaSlave(_Cstruct):
        _fields = [
            ('psz_uri', ctypes.c_char_p),
            ('i_type', MediaSlaveType),
            ('i_priority', ctypes.c_uint)
        ]

class RDDescription(_Cstruct):
    _fields = [
        ('name', ctypes.c_char_p),
        ('longname', ctypes.c_char_p)
    ]


class EventManager(_Ctype):
    '''Create an event manager with callback handler.

    This class interposes the registration and handling of
    event notifications in order to (a) remove the need for
    decorating each callback functions with the decorator
    '@callbackmethod', (b) allow any number of positional
    and/or keyword arguments to the callback (in addition
    to the Event instance) and (c) to preserve the Python
    objects such that the callback and argument objects
    remain alive (i.e. are not garbage collected) until
    B{after} the notification has been unregistered.

    @note: Only a single notification can be registered
    for each event type in an EventManager instance.

    '''

    _callback_handler = None
    _callbacks = {}

    def __new__(cls, ptr=_internal_guard):
        if ptr == _internal_guard:
            raise VLCException("(INTERNAL) ctypes class.\nYou should get a reference to EventManager through the MediaPlayer.event_manager() method.")
        return _Constructor(cls, ptr)

    def event_attach(self, eventtype, callback, *args, **kwds):

        if not isinstance(eventtype, EventType):
            raise VLCException("%s required: %r" % ('EventType', eventtype))
        if not hasattr(callback, '__call__'):
            raise VLCException("%s required: %r" % ('callable', callback))

        if not any(getargspec(callback)[:2]):
            raise VLCException("%s required: %r" % ('argument', callback))

        if self._callback_handler is None:
            _called_from_ctypes = ctypes.CFUNCTYPE(None, ctypes.POINTER(Event), ctypes.c_void_p)
            @_called_from_ctypes
            def _callback_handler(event, k):
                try:
                    call, args, kwds = self._callbacks[k]

                    call(event.contents, *args, **kwds)
                except KeyError:
                    pass
            self._callback_handler = _callback_handler
            self._callbacks = {}

        k = eventtype.value
        r = libvlc_event_attach(self, k, self._callback_handler, k)
        if not r:
            self._callbacks[k] = (callback, args, kwds)
        return r

    def event_detach(self, eventtype):
        if not isinstance(eventtype, EventType):
            raise VLCException("%s required: %r" % ('EventType', eventtype))

        k = eventtype.value
        if k in self._callbacks:
            del self._callbacks[k]
            libvlc_event_detach(self, k, self._callback_handler, k)

class Instance(_Ctype):
    '''Create a new Instance instance.

    It may take as parameter either:
      - a string
      - a list of strings as first parameters
      - the parameters given as the constructor parameters (must be strings)

    '''

    def __new__(cls, *args):
        if len(args) == 1:


            i = args[0]
            if isinstance(i, _Ints):
                return _Constructor(cls, i)
            elif isinstance(i, basestring):
                args = i.strip().split()
            elif isinstance(i, _Seqs):
                args = list(i)
            else:
                raise VLCException('Instance %r' % (args,))
        else:
            args = list(args)

        if not args:
            args = ['vlc']
        elif args[0] != 'vlc':
            args.insert(0, 'vlc')

        if plugin_path is not None:


            os.environ.setdefault('VLC_PLUGIN_PATH', plugin_path)

        if PYTHON3:
            args = [ str_to_bytes(a) for a in args ]
        return libvlc_new(len(args), args)

    def media_player_new(self, uri=None):
        p = libvlc_media_player_new(self)
        if uri:
            p.set_media(self.media_new(uri))
        p._instance = self
        return p

    def media_list_player_new(self):


        p = libvlc_media_list_player_new(self)
        p._instance = self
        return p

    def media_new(self, mrl, *options):
        if ':' in mrl and mrl.index(':') > 1:

            m = libvlc_media_new_location(self, str_to_bytes(mrl))
        else:

            m = libvlc_media_new_path(self, str_to_bytes(os.path.normpath(mrl)))
        for o in options:
            libvlc_media_add_option(m, str_to_bytes(o))
        m._instance = self
        return m

    def media_list_new(self, mrls=None):
        l = libvlc_media_list_new(self)
        if mrls:
            for m in mrls:
                l.add_media(m)
        l._instance = self
        return l

    def audio_output_enumerate_devices(self):
        r = []
        head = libvlc_audio_output_list_get(self)
        if head:
            i = head
            while i:
                i = i.contents
                d = [{'id':       libvlc_audio_output_device_id      (self, i.name, d),
                      'longname': libvlc_audio_output_device_longname(self, i.name, d)}
                   for d in range(libvlc_audio_output_device_count   (self, i.name))]
                r.append({'name': i.name, 'description': i.description, 'devices': d})
                i = i.next
            libvlc_audio_output_list_release(head)
        return r

    def audio_filter_list_get(self):



        return module_description_list(libvlc_audio_filter_list_get(self))

    def video_filter_list_get(self):



        return module_description_list(libvlc_video_filter_list_get(self))



    def release(self):
        '''Decrement the reference count of a libvlc instance, and destroy it
        if it reaches zero.
        '''
        return libvlc_release(self)


    def retain(self):
        '''Increments the reference count of a libvlc instance.
        The initial reference count is 1 after L{new}() returns.
        '''
        return libvlc_retain(self)


    def add_intf(self, name):
        '''Try to start a user interface for the libvlc instance.
        @param name: interface name, or None for default.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_add_intf(self, str_to_bytes(name))


    def set_user_agent(self, name, http):
        '''Sets the application name. LibVLC passes this as the user agent string
        when a protocol requires it.
        @param name: human-readable application name, e.g. "FooBar player 1.2.3".
        @param http: HTTP User Agent, e.g. "FooBar/1.2.3 Python/2.6.0".
        @version: LibVLC 1.1.1 or later.
        '''
        return libvlc_set_user_agent(self, str_to_bytes(name), str_to_bytes(http))


    def set_app_id(self, id, version, icon):
        '''Sets some meta-information about the application.
        See also L{set_user_agent}().
        @param id: Java-style application identifier, e.g. "com.acme.foobar".
        @param version: application version numbers, e.g. "1.2.3".
        @param icon: application icon name, e.g. "foobar".
        @version: LibVLC 2.1.0 or later.
        '''
        return libvlc_set_app_id(self, str_to_bytes(id), str_to_bytes(version), str_to_bytes(icon))


    def log_unset(self):
        '''Unsets the logging callback for a LibVLC instance. This is rarely needed:
        the callback is implicitly unset when the instance is destroyed.
        This function will wait for any pending callbacks invocation to complete
        (causing a deadlock if called from within the callback).
        @version: LibVLC 2.1.0 or later.
        '''
        return libvlc_log_unset(self)


    def log_set(self, data, p_instance):
        '''Sets the logging callback for a LibVLC instance.
        This function is thread-safe: it will wait for any pending callbacks
        invocation to complete.
        @param data: opaque data pointer for the callback function @note Some log messages (especially debug) are emitted by LibVLC while is being initialized. These messages cannot be captured with this interface. @warning A deadlock may occur if this function is called from the callback.
        @param p_instance: libvlc instance.
        @version: LibVLC 2.1.0 or later.
        '''
        return libvlc_log_set(self, data, p_instance)


    def log_set_file(self, stream):
        '''Sets up logging to a file.
        @param stream: FILE pointer opened for writing (the FILE pointer must remain valid until L{log_unset}()).
        @version: LibVLC 2.1.0 or later.
        '''
        return libvlc_log_set_file(self, stream)


    def media_new_location(self, psz_mrl):
        '''Create a media with a certain given media resource location,
        for instance a valid URL.
        @note: To refer to a local file with this function,
        the file://... URI syntax B{must} be used (see IETF RFC3986).
        We recommend using L{media_new_path}() instead when dealing with
        local files.
        See L{media_release}.
        @param psz_mrl: the media location.
        @return: the newly created media or None on error.
        '''
        return libvlc_media_new_location(self, str_to_bytes(psz_mrl))


    def media_new_path(self, path):
        '''Create a media for a certain file path.
        See L{media_release}.
        @param path: local filesystem path.
        @return: the newly created media or None on error.
        '''
        return libvlc_media_new_path(self, str_to_bytes(path))


    def media_new_fd(self, fd):

        return libvlc_media_new_fd(self, fd)


    def media_new_callbacks(self, open_cb, read_cb, seek_cb, close_cb, opaque):

        return libvlc_media_new_callbacks(self, open_cb, read_cb, seek_cb, close_cb, opaque)


    def media_new_as_node(self, psz_name):
        '''Create a media as an empty node with a given name.
        See L{media_release}.
        @param psz_name: the name of the node.
        @return: the new empty media or None on error.
        '''
        return libvlc_media_new_as_node(self, str_to_bytes(psz_name))


    def media_discoverer_new(self, psz_name):

        return libvlc_media_discoverer_new(self, str_to_bytes(psz_name))


    def media_discoverer_list_get(self, i_cat, ppp_services):
        '''Get media discoverer services by category.
        @param i_cat: category of services to fetch.
        @param ppp_services: address to store an allocated array of media discoverer services (must be freed with L{media_discoverer_list_release}() by the caller) [OUT].
        @return: the number of media discoverer services (0 on error).
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_discoverer_list_get(self, i_cat, ppp_services)


    def media_library_new(self):
        '''Create an new Media Library object.
        @return: a new object or None on error.
        '''
        return libvlc_media_library_new(self)


    def audio_output_list_get(self):
        '''Gets the list of available audio output modules.
        @return: list of available audio outputs. It must be freed with In case of error, None is returned.
        '''
        return libvlc_audio_output_list_get(self)


    def audio_output_device_list_get(self, aout):

        return libvlc_audio_output_device_list_get(self, str_to_bytes(aout))


    def renderer_discoverer_new(self, psz_name):

        return libvlc_renderer_discoverer_new(self, str_to_bytes(psz_name))


    def renderer_discoverer_list_get(self, ppp_services):
        '''Get media discoverer services
        See libvlc_renderer_list_release().
        @param ppp_services: address to store an allocated array of renderer discoverer services (must be freed with libvlc_renderer_list_release() by the caller) [OUT].
        @return: the number of media discoverer services (0 on error).
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_renderer_discoverer_list_get(self, ppp_services)


    def vlm_release(self):
        '''Release the vlm instance related to the given L{Instance}.
        '''
        return libvlc_vlm_release(self)


    def vlm_add_broadcast(self, psz_name, psz_input, psz_output, i_options, ppsz_options, b_enabled, b_loop):

        return libvlc_vlm_add_broadcast(self, str_to_bytes(psz_name), str_to_bytes(psz_input), str_to_bytes(psz_output), i_options, ppsz_options, b_enabled, b_loop)


    def vlm_add_vod(self, psz_name, psz_input, i_options, ppsz_options, b_enabled, psz_mux):

        return libvlc_vlm_add_vod(self, str_to_bytes(psz_name), str_to_bytes(psz_input), i_options, ppsz_options, b_enabled, str_to_bytes(psz_mux))


    def vlm_del_media(self, psz_name):
        '''Delete a media (VOD or broadcast).
        @param psz_name: the media to delete.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_del_media(self, str_to_bytes(psz_name))


    def vlm_set_enabled(self, psz_name, b_enabled):
        '''Enable or disable a media (VOD or broadcast).
        @param psz_name: the media to work on.
        @param b_enabled: the new status.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_set_enabled(self, str_to_bytes(psz_name), b_enabled)


    def vlm_set_output(self, psz_name, psz_output):
        '''Set the output for a media.
        @param psz_name: the media to work on.
        @param psz_output: the output MRL (the parameter to the "sout" variable).
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_set_output(self, str_to_bytes(psz_name), str_to_bytes(psz_output))


    def vlm_set_input(self, psz_name, psz_input):
        '''Set a media's input MRL. This will delete all existing inputs and
        add the specified one.
        @param psz_name: the media to work on.
        @param psz_input: the input MRL.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_set_input(self, str_to_bytes(psz_name), str_to_bytes(psz_input))


    def vlm_add_input(self, psz_name, psz_input):
        '''Add a media's input MRL. This will add the specified one.
        @param psz_name: the media to work on.
        @param psz_input: the input MRL.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_add_input(self, str_to_bytes(psz_name), str_to_bytes(psz_input))


    def vlm_set_loop(self, psz_name, b_loop):
        '''Set a media's loop status.
        @param psz_name: the media to work on.
        @param b_loop: the new status.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_set_loop(self, str_to_bytes(psz_name), b_loop)


    def vlm_set_mux(self, psz_name, psz_mux):
        '''Set a media's vod muxer.
        @param psz_name: the media to work on.
        @param psz_mux: the new muxer.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_set_mux(self, str_to_bytes(psz_name), str_to_bytes(psz_mux))


    def vlm_change_media(self, psz_name, psz_input, psz_output, i_options, ppsz_options, b_enabled, b_loop):

        return libvlc_vlm_change_media(self, str_to_bytes(psz_name), str_to_bytes(psz_input), str_to_bytes(psz_output), i_options, ppsz_options, b_enabled, b_loop)


    def vlm_play_media(self, psz_name):
        '''Play the named broadcast.
        @param psz_name: the name of the broadcast.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_play_media(self, str_to_bytes(psz_name))


    def vlm_stop_media(self, psz_name):
        '''Stop the named broadcast.
        @param psz_name: the name of the broadcast.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_stop_media(self, str_to_bytes(psz_name))


    def vlm_pause_media(self, psz_name):
        '''Pause the named broadcast.
        @param psz_name: the name of the broadcast.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_pause_media(self, str_to_bytes(psz_name))


    def vlm_seek_media(self, psz_name, f_percentage):
        '''Seek in the named broadcast.
        @param psz_name: the name of the broadcast.
        @param f_percentage: the percentage to seek to.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_vlm_seek_media(self, str_to_bytes(psz_name), f_percentage)


    def vlm_show_media(self, psz_name):

        return libvlc_vlm_show_media(self, str_to_bytes(psz_name))


    def vlm_get_media_instance_position(self, psz_name, i_instance):
        '''Get vlm_media instance position by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: position as float or -1. on error.
        '''
        return libvlc_vlm_get_media_instance_position(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_time(self, psz_name, i_instance):
        '''Get vlm_media instance time by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: time as integer or -1 on error.
        '''
        return libvlc_vlm_get_media_instance_time(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_length(self, psz_name, i_instance):
        '''Get vlm_media instance length by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: length of media item or -1 on error.
        '''
        return libvlc_vlm_get_media_instance_length(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_rate(self, psz_name, i_instance):
        '''Get vlm_media instance playback rate by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: playback rate or -1 on error.
        '''
        return libvlc_vlm_get_media_instance_rate(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_title(self, psz_name, i_instance):
        '''Get vlm_media instance title number by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: title as number or -1 on error.
        @bug: will always return 0.
        '''
        return libvlc_vlm_get_media_instance_title(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_chapter(self, psz_name, i_instance):
        '''Get vlm_media instance chapter number by name or instance id.
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: chapter as number or -1 on error.
        @bug: will always return 0.
        '''
        return libvlc_vlm_get_media_instance_chapter(self, str_to_bytes(psz_name), i_instance)


    def vlm_get_media_instance_seekable(self, psz_name, i_instance):
        '''Is libvlc instance seekable ?
        @param psz_name: name of vlm media instance.
        @param i_instance: instance id.
        @return: 1 if seekable, 0 if not, -1 if media does not exist.
        @bug: will always return 0.
        '''
        return libvlc_vlm_get_media_instance_seekable(self, str_to_bytes(psz_name), i_instance)

    @memoize_parameterless
    def vlm_get_event_manager(self):
        '''Get libvlc_event_manager from a vlm media.
        The p_event_manager is immutable, so you don't have to hold the lock.
        @return: libvlc_event_manager.
        '''
        return libvlc_vlm_get_event_manager(self)

class Media(_Ctype):
    '''Create a new Media instance.

    Usage: Media(MRL, *options)

    See vlc.Instance.media_new documentation for details.

    '''

    def __new__(cls, *args):
        if args:
            i = args[0]
            if isinstance(i, _Ints):
                return _Constructor(cls, i)
            if isinstance(i, Instance):
                return i.media_new(*args[1:])

        o = get_default_instance().media_new(*args)
        return o

    def get_instance(self):
        return getattr(self, '_instance', None)

    def add_options(self, *options):
        for o in options:
            self.add_option(o)

    def tracks_get(self):
        return info

    def add_option(self, psz_options):
        '''Add an option to the media.
        This option will be used to determine how the media_player will
        read the media. This allows to use VLC's advanced
        reading/streaming options on a per-media basis.
        @note: The options are listed in 'vlc --long-help' from the command line,
        e.g. "-sout-all". Keep in mind that available options and their semantics
        vary across LibVLC versions and builds.
        @warning: Not all options affects L{Media} objects:
        Specifically, due to architectural issues most audio and video options,
        such as text renderer options, have no effects on an individual media.
        These options must be set through L{new}() instead.
        @param psz_options: the options (as a string).
        '''
        return libvlc_media_add_option(self, str_to_bytes(psz_options))


    def add_option_flag(self, psz_options, i_flags):
        '''Add an option to the media with configurable flags.
        This option will be used to determine how the media_player will
        read the media. This allows to use VLC's advanced
        reading/streaming options on a per-media basis.
        The options are detailed in vlc --long-help, for instance
        "--sout-all". Note that all options are not usable on medias:
        specifically, due to architectural issues, video-related options
        such as text renderer options cannot be set on a single media. They
        must be set on the whole libvlc instance instead.
        @param psz_options: the options (as a string).
        @param i_flags: the flags for this option.
        '''
        return libvlc_media_add_option_flag(self, str_to_bytes(psz_options), i_flags)


    def retain(self):
        '''Retain a reference to a media descriptor object (libvlc_media_t). Use
        L{release}() to decrement the reference count of a
        media descriptor object.
        '''
        return libvlc_media_retain(self)


    def release(self):
        '''Decrement the reference count of a media descriptor object. If the
        reference count is 0, then L{release}() will release the
        media descriptor object. It will send out an libvlc_MediaFreed event
        to all listeners. If the media descriptor object has been released it
        should not be used again.
        '''
        return libvlc_media_release(self)


    def get_mrl(self):
        '''Get the media resource locator (mrl) from a media descriptor object.
        @return: string with mrl of media descriptor object.
        '''
        return libvlc_media_get_mrl(self)


    def duplicate(self):
        '''Duplicate a media descriptor object.
        '''
        return libvlc_media_duplicate(self)


    def get_meta(self, e_meta):
        '''Read the meta of the media.
        If the media has not yet been parsed this will return None.
        See L{parse}
        See L{parse_with_options}
        See libvlc_MediaMetaChanged.
        @param e_meta: the meta to read.
        @return: the media's meta.
        '''
        return libvlc_media_get_meta(self, e_meta)


    def set_meta(self, e_meta, psz_value):
        '''Set the meta of the media (this function will not save the meta, call
        L{save_meta} in order to save the meta).
        @param e_meta: the meta to write.
        @param psz_value: the media's meta.
        '''
        return libvlc_media_set_meta(self, e_meta, str_to_bytes(psz_value))


    def save_meta(self):
        '''Save the meta previously set.
        @return: true if the write operation was successful.
        '''
        return libvlc_media_save_meta(self)


    def get_state(self):
        '''Get current state of media descriptor object. Possible media states are
        libvlc_NothingSpecial=0, libvlc_Opening, libvlc_Playing, libvlc_Paused,
        libvlc_Stopped, libvlc_Ended, libvlc_Error.
        See libvlc_state_t.
        @return: state of media descriptor object.
        '''
        return libvlc_media_get_state(self)


    def get_stats(self, p_stats):
        '''Get the current statistics about the media.
        @param p_stats:: structure that contain the statistics about the media (this structure must be allocated by the caller).
        @return: true if the statistics are available, false otherwise \libvlc_return_bool.
        '''
        return libvlc_media_get_stats(self, p_stats)


    def subitems(self):
        '''Get subitems of media descriptor object. This will increment
        the reference count of supplied media descriptor object. Use
        L{list_release}() to decrement the reference counting.
        @return: list of media descriptor subitems or None.
        '''
        return libvlc_media_subitems(self)
    def event_manager(self):
        '''Get event manager from media descriptor object.
        NOTE: this function doesn't increment reference counting.
        @return: event manager object.
        '''
        return libvlc_media_event_manager(self)


    def get_duration(self):
        '''Get duration (in ms) of media descriptor object item.
        @return: duration of media item or -1 on error.
        '''
        return libvlc_media_get_duration(self)


    def parse(self):
        '''Parse a media.
        This fetches (local) art, meta data and tracks information.
        The method is synchronous.
        See L{parse_with_options}
        See L{get_meta}
        See libvlc_media_get_tracks_info.
        '''
        return libvlc_media_parse(self)


    def parse_with_options(self, parse_flag, timeout):
        '''Parse the media asynchronously with options.
        This fetches (local or network) art, meta data and/or tracks information.
        This method is the extended version of L{parse_with_options}().
        To track when this is over you can listen to libvlc_MediaParsedChanged
        event. However if this functions returns an error, you will not receive any
        events.
        It uses a flag to specify parse options (see libvlc_media_parse_flag_t). All
        these flags can be combined. By default, media is parsed if it's a local
        file.
        See libvlc_MediaParsedChanged
        See L{get_meta}
        See L{tracks_get}
        See L{get_parsed_status}
        See libvlc_media_parse_flag_t.
        @param parse_flag: parse options:
        @param timeout: maximum time allowed to preparse the media. If -1, the default "preparse-timeout" option will be used as a timeout. If 0, it will wait indefinitely. If > 0, the timeout will be used (in milliseconds).
        @return: -1 in case of error, 0 otherwise.
        @version: LibVLC 3.0.0 or later.
        '''
        return libvlc_media_parse_with_options(self, parse_flag, timeout)


    def get_parsed_status(self):
        '''Get Parsed status for media descriptor object.
        See libvlc_MediaParsedChanged
        See libvlc_media_parsed_status_t.
        @return: a value of the libvlc_media_parsed_status_t enum.
        @version: LibVLC 3.0.0 or later.
        '''
        return libvlc_media_get_parsed_status(self)


    def set_user_data(self, p_new_user_data):
        '''Sets media descriptor's user_data. user_data is specialized data
        accessed by the host application, VLC.framework uses it as a pointer to
        an native object that references a L{Media} pointer.
        @param p_new_user_data: pointer to user data.
        '''
        return libvlc_media_set_user_data(self, p_new_user_data)


    def get_user_data(self):
        '''Get media descriptor's user_data. user_data is specialized data
        accessed by the host application, VLC.framework uses it as a pointer to
        an native object that references a L{Media} pointer.
        '''
        return libvlc_media_get_user_data(self)


    def get_type(self):
        '''Get the media type of the media descriptor object.
        @return: media type.
        @version: LibVLC 3.0.0 and later. See libvlc_media_type_t.
        '''
        return libvlc_media_get_type(self)


    def slaves_add(self, i_type, i_priority, psz_uri):
        '''Add a slave to the current media.
        A slave is an external input source that may contains an additional subtitle
        track (like a .srt) or an additional audio track (like a .ac3).
        @note: This function must be called before the media is parsed (via
        L{parse_with_options}()) or before the media is played (via
        L{player_play}()).
        @param i_type: subtitle or audio.
        @param i_priority: from 0 (low priority) to 4 (high priority).
        @param psz_uri: Uri of the slave (should contain a valid scheme).
        @return: 0 on success, -1 on error.
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_slaves_add(self, i_type, i_priority, str_to_bytes(psz_uri))


    def slaves_clear(self):
        '''Clear all slaves previously added by L{slaves_add}() or
        internally.
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_slaves_clear(self)


    def slaves_get(self, ppp_slaves):
        '''Get a media descriptor's slave list
        The list will contain slaves parsed by VLC or previously added by
        L{slaves_add}(). The typical use case of this function is to save
        a list of slave in a database for a later use.
        @param ppp_slaves: address to store an allocated array of slaves (must be freed with L{slaves_release}()) [OUT].
        @return: the number of slaves (zero on error).
        @version: LibVLC 3.0.0 and later. See L{slaves_add}.
        '''
        return libvlc_media_slaves_get(self, ppp_slaves)


    def player_new_from_media(self):
        '''Create a Media Player object from a Media.
        @return: a new media player object, or None on error.
        '''
        return libvlc_media_player_new_from_media(self)

class MediaPlayer(_Ctype):
    '''Create a new MediaPlayer instance.

    It may take as parameter either:
      - a string (media URI), options... In this case, a vlc.Instance will be created.
      - a vlc.Instance, a string (media URI), options...

    '''

    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], _Ints):
            return _Constructor(cls, args[0])

        if args and isinstance(args[0], Instance):
            instance = args[0]
            args = args[1:]
        else:
            instance = get_default_instance()

        o = instance.media_player_new()
        if args:
            o.set_media(instance.media_new(*args))
        return o

    def get_instance(self):


        return self._instance

    def set_mrl(self, mrl, *options):
        m = self.get_instance().media_new(mrl, *options)
        self.set_media(m)
        return m

    def video_get_spu_description(self):


        return track_description_list(libvlc_video_get_spu_description(self))

    def video_get_title_description(self):


        return track_description_list(libvlc_video_get_title_description(self))

    def video_get_chapter_description(self, title):

        return track_description_list(libvlc_video_get_chapter_description(self, title))

    def video_get_track_description(self):


        return track_description_list(libvlc_video_get_track_description(self))

    def audio_get_track_description(self):


        return track_description_list(libvlc_audio_get_track_description(self))

    def get_full_title_descriptions(self):
        '''Get the full description of available titles.
        @return: the titles list
        @version: LibVLC 3.0.0 and later.
        '''
        titleDescription_pp = ctypes.POINTER(TitleDescription)()
        n = libvlc_media_player_get_full_title_descriptions(self, ctypes.byref(titleDescription_pp))
        info = ctypes.cast(ctypes.titleDescription_pp, ctypes.POINTER(ctypes.POINTER(TitleDescription) * n))
        return info

    def get_full_chapter_descriptions(self, i_chapters_of_title):
        '''Get the full description of available chapters.
        @param i_chapters_of_title: index of the title to query for chapters (uses current title if set to -1).
        @return: the chapters list
        @version: LibVLC 3.0.0 and later.
        '''
        chapterDescription_pp = ctypes.POINTER(ChapterDescription)()
        n = libvlc_media_player_get_full_chapter_descriptions(self, ctypes.byref(chapterDescription_pp))
        info = ctypes.cast(ctypes.chapterDescription_pp, ctypes.POINTER(ctypes.POINTER(ChapterDescription) * n))
        return info

    def video_get_size(self, num=0):
        r = libvlc_video_get_size(self, num)
        if isinstance(r, tuple) and len(r) == 2:
            return r
        else:
            raise VLCException('invalid video number (%s)' % (num,))

    def set_hwnd(self, drawable):

        if not isinstance(drawable, ctypes.c_void_p):
            drawable = ctypes.c_void_p(int(drawable))
        libvlc_media_player_set_hwnd(self, drawable)

    def video_get_width(self, num=0):
        return self.video_get_size(num)[0]

    def video_get_height(self, num=0):


        return self.video_get_size(num)[1]

    def video_get_cursor(self, num=0):
        r = libvlc_video_get_cursor(self, num)
        if isinstance(r, tuple) and len(r) == 2:
            return r
        raise VLCException('invalid video number (%s)' % (num,))



    def get_fps(self):
        '''Get movie fps rate
        This function is provided for backward compatibility. It cannot deal with
        multiple video tracks. In LibVLC versions prior to 3.0, it would also fail
        if the file format did not convey the frame rate explicitly.
        \deprecated Consider using L{media_tracks_get}() instead.
        @return: frames per second (fps) for this playing movie, or 0 if unspecified.
        '''
        return libvlc_media_player_get_fps(self)


    def set_agl(self, drawable):
        '''\deprecated Use L{set_nsobject}() instead.
        '''
        return libvlc_media_player_set_agl(self, drawable)


    def get_agl(self):
        '''\deprecated Use L{get_nsobject}() instead.
        '''
        return libvlc_media_player_get_agl(self)


    def release(self):
        '''Release a media_player after use
        Decrement the reference count of a media player object. If the
        reference count is 0, then L{release}() will
        release the media player object. If the media player object
        has been released, then it should not be used again.
        '''
        return libvlc_media_player_release(self)


    def retain(self):
        '''Retain a reference to a media player object. Use
        L{release}() to decrement reference count.
        '''
        return libvlc_media_player_retain(self)


    def set_media(self, p_md):
        '''Set the media that will be used by the media_player. If any,
        previous md will be released.
        @param p_md: the Media. Afterwards the p_md can be safely destroyed.
        '''
        return libvlc_media_player_set_media(self, p_md)


    def get_media(self):
        '''Get the media used by the media_player.
        @return: the media associated with p_mi, or None if no media is associated.
        '''
        return libvlc_media_player_get_media(self)

    @memoize_parameterless
    def event_manager(self):
        '''Get the Event Manager from which the media player send event.
        @return: the event manager associated with p_mi.
        '''
        return libvlc_media_player_event_manager(self)


    def is_playing(self):
        '''is_playing.
        @return: 1 if the media player is playing, 0 otherwise \libvlc_return_bool.
        '''
        return libvlc_media_player_is_playing(self)


    def play(self):
        '''Play.
        @return: 0 if playback started (and was already started), or -1 on error.
        '''
        return libvlc_media_player_play(self)


    def set_pause(self, do_pause):
        '''Pause or resume (no effect if there is no media).
        @param do_pause: play/resume if zero, pause if non-zero.
        @version: LibVLC 1.1.1 or later.
        '''
        return libvlc_media_player_set_pause(self, do_pause)


    def pause(self):
        '''Toggle pause (no effect if there is no media).
        '''
        return libvlc_media_player_pause(self)


    def stop(self):
        '''Stop (no effect if there is no media).
        '''
        return libvlc_media_player_stop(self)


    def set_renderer(self, p_item):
        '''Set a renderer to the media player
        @note: must be called before the first call of L{play}() to
        take effect.
        See L{renderer_discoverer_new}.
        @param p_item: an item discovered by L{renderer_discoverer_start}().
        @return: 0 on success, -1 on error.
        @version: LibVLC 3.0.0 or later.
        '''
        return libvlc_media_player_set_renderer(self, p_item)


    def video_set_callbacks(self, lock, unlock, display, opaque):
        '''Set callbacks and private data to render decoded video to a custom area
        in memory.
        Use L{video_set_format}() or L{video_set_format_callbacks}()
        to configure the decoded format.
        @warning: Rendering video into custom memory buffers is considerably less
        efficient than rendering in a custom window as normal.
        For optimal perfomances, VLC media player renders into a custom window, and
        does not use this function and associated callbacks. It is B{highly
        recommended} that other LibVLC-based application do likewise.
        To embed video in a window, use libvlc_media_player_set_xid() or equivalent
        depending on the operating system.
        If window embedding does not fit the application use case, then a custom
        LibVLC video output display plugin is required to maintain optimal video
        rendering performances.
        The following limitations affect performance:
        - Hardware video decoding acceleration will either be disabled completely,
          or require (relatively slow) copy from video/DSP memory to main memory.
        - Sub-pictures (subtitles, on-screen display, etc.) must be blent into the
          main picture by the CPU instead of the GPU.
        - Depending on the video format, pixel format conversion, picture scaling,
          cropping and/or picture re-orientation, must be performed by the CPU
          instead of the GPU.
        - Memory copying is required between LibVLC reference picture buffers and
          application buffers (between lock and unlock callbacks).
        @param lock: callback to lock video memory (must not be None).
        @param unlock: callback to unlock video memory (or None if not needed).
        @param display: callback to display video (or None if not needed).
        @param opaque: private pointer for the three callbacks (as first parameter).
        @version: LibVLC 1.1.1 or later.
        '''
        return libvlc_video_set_callbacks(self, lock, unlock, display, opaque)


    def video_set_format(self, chroma, width, height, pitch):
        '''Set decoded video chroma and dimensions.
        This only works in combination with L{video_set_callbacks}(),
        and is mutually exclusive with L{video_set_format_callbacks}().
        @param chroma: a four-characters string identifying the chroma (e.g. "RV32" or "YUYV").
        @param width: pixel width.
        @param height: pixel height.
        @param pitch: line pitch (in bytes).
        @version: LibVLC 1.1.1 or later.
        @bug: All pixel planes are expected to have the same pitch. To use the YCbCr color space with chrominance subsampling, consider using L{video_set_format_callbacks}() instead.
        '''
        return libvlc_video_set_format(self, str_to_bytes(chroma), width, height, pitch)


    def video_set_format_callbacks(self, setup, cleanup):
        '''Set decoded video chroma and dimensions. This only works in combination with
        L{video_set_callbacks}().
        @param setup: callback to select the video format (cannot be None).
        @param cleanup: callback to release any allocated resources (or None).
        @version: LibVLC 2.0.0 or later.
        '''
        return libvlc_video_set_format_callbacks(self, setup, cleanup)


    def set_nsobject(self, drawable):
        '''Set the NSView handler where the media player should render its video output.
        Use the vout called "macosx".
        The drawable is an NSObject that follow the VLCOpenGLVideoViewEmbedding
        protocol:
        @code.m
        \@protocol VLCOpenGLVideoViewEmbedding <NSObject>
        - (void)addVoutSubview:(NSView *)view;
        - (void)removeVoutSubview:(NSView *)view;
        \@end
        @endcode
        Or it can be an NSView object.
        If you want to use it along with Qt see the QMacCocoaViewContainer. Then
        the following code should work:
        @code.mm

            NSView *video = [[NSView alloc] init];
            QMacCocoaViewContainer *container = new QMacCocoaViewContainer(video, parent);
            L{set_nsobject}(mp, video);
            [video release];

        @endcode
        You can find a live example in VLCVideoView in VLCKit.framework.
        @param drawable: the drawable that is either an NSView or an object following the VLCOpenGLVideoViewEmbedding protocol.
        '''
        return libvlc_media_player_set_nsobject(self, drawable)


    def get_nsobject(self):
        '''Get the NSView handler previously set with L{set_nsobject}().
        @return: the NSView handler or 0 if none where set.
        '''
        return libvlc_media_player_get_nsobject(self)


    def set_xwindow(self, drawable):
        '''Set an X Window System drawable where the media player should render its
        video output. The call takes effect when the playback starts. If it is
        already started, it might need to be stopped before changes apply.
        If LibVLC was built without X11 output support, then this function has no
        effects.
        By default, LibVLC will capture input events on the video rendering area.
        Use L{video_set_mouse_input}() and L{video_set_key_input}() to
        disable that and deliver events to the parent window / to the application
        instead. By design, the X11 protocol delivers input events to only one
        recipient.
        @warning
        The application must call the XInitThreads() function from Xlib before
        L{new}(), and before any call to XOpenDisplay() directly or via any
        other library. Failure to call XInitThreads() will seriously impede LibVLC
        performance. Calling XOpenDisplay() before XInitThreads() will eventually
        crash the process. That is a limitation of Xlib.
        @param drawable: X11 window ID @note The specified identifier must correspond to an existing Input/Output class X11 window. Pixmaps are B{not} currently supported. The default X11 server is assumed, i.e. that specified in the DISPLAY environment variable. @warning LibVLC can deal with invalid X11 handle errors, however some display drivers (EGL, GLX, VA and/or VDPAU) can unfortunately not. Thus the window handle must remain valid until playback is stopped, otherwise the process may abort or crash.
        @bug No more than one window handle per media player instance can be specified. If the media has multiple simultaneously active video tracks, extra tracks will be rendered into external windows beyond the control of the application.
        '''
        return libvlc_media_player_set_xwindow(self, drawable)


    def get_xwindow(self):
        '''Get the X Window System window identifier previously set with
        L{set_xwindow}(). Note that this will return the identifier
        even if VLC is not currently using it (for instance if it is playing an
        audio-only input).
        @return: an X window ID, or 0 if none where set.
        '''
        return libvlc_media_player_get_xwindow(self)


    def get_hwnd(self):
        '''Get the Windows API window handle (HWND) previously set with
        L{set_hwnd}(). The handle will be returned even if LibVLC
        is not currently outputting any video to it.
        @return: a window handle or None if there are none.
        '''
        return libvlc_media_player_get_hwnd(self)


    def set_android_context(self, p_awindow_handler):
        '''Set the android context.
        @param p_awindow_handler: org.videolan.libvlc.IAWindowNativeHandler jobject implemented by the org.videolan.libvlc.MediaPlayer class from the libvlc-android project.
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_player_set_android_context(self, p_awindow_handler)


    def set_evas_object(self, p_evas_object):
        '''Set the EFL Evas Object.
        @param p_evas_object: a valid EFL Evas Object (Evas_Object).
        @return: -1 if an error was detected, 0 otherwise.
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_player_set_evas_object(self, p_evas_object)


    def audio_set_callbacks(self, play, pause, resume, flush, drain, opaque):
        '''Sets callbacks and private data for decoded audio.
        Use L{audio_set_format}() or L{audio_set_format_callbacks}()
        to configure the decoded audio format.
        @note: The audio callbacks override any other audio output mechanism.
        If the callbacks are set, LibVLC will B{not} output audio in any way.
        @param play: callback to play audio samples (must not be None).
        @param pause: callback to pause playback (or None to ignore).
        @param resume: callback to resume playback (or None to ignore).
        @param flush: callback to flush audio buffers (or None to ignore).
        @param drain: callback to drain audio buffers (or None to ignore).
        @param opaque: private pointer for the audio callbacks (as first parameter).
        @version: LibVLC 2.0.0 or later.
        '''
        return libvlc_audio_set_callbacks(self, play, pause, resume, flush, drain, opaque)


    def audio_set_volume_callback(self, set_volume):
        '''Set callbacks and private data for decoded audio. This only works in
        combination with L{audio_set_callbacks}().
        Use L{audio_set_format}() or L{audio_set_format_callbacks}()
        to configure the decoded audio format.
        @param set_volume: callback to apply audio volume, or None to apply volume in software.
        @version: LibVLC 2.0.0 or later.
        '''
        return libvlc_audio_set_volume_callback(self, set_volume)


    def audio_set_format_callbacks(self, setup, cleanup):
        '''Sets decoded audio format via callbacks.
        This only works in combination with L{audio_set_callbacks}().
        @param setup: callback to select the audio format (cannot be None).
        @param cleanup: callback to release any allocated resources (or None).
        @version: LibVLC 2.0.0 or later.
        '''
        return libvlc_audio_set_format_callbacks(self, setup, cleanup)


    def audio_set_format(self, format, rate, channels):
        '''Sets a fixed decoded audio format.
        This only works in combination with L{audio_set_callbacks}(),
        and is mutually exclusive with L{audio_set_format_callbacks}().
        @param format: a four-characters string identifying the sample format (e.g. "S16N" or "FL32").
        @param rate: sample rate (expressed in Hz).
        @param channels: channels count.
        @version: LibVLC 2.0.0 or later.
        '''
        return libvlc_audio_set_format(self, str_to_bytes(format), rate, channels)


    def get_length(self):
        '''Get the current movie length (in ms).
        @return: the movie length (in ms), or -1 if there is no media.
        '''
        return libvlc_media_player_get_length(self)


    def get_time(self):
        '''Get the current movie time (in ms).
        @return: the movie time (in ms), or -1 if there is no media.
        '''
        return libvlc_media_player_get_time(self)


    def set_time(self, i_time):
        '''Set the movie time (in ms). This has no effect if no media is being played.
        Not all formats and protocols support this.
        @param i_time: the movie time (in ms).
        '''
        return libvlc_media_player_set_time(self, i_time)


    def get_position(self):
        '''Get movie position as percentage between 0.0 and 1.0.
        @return: movie position, or -1. in case of error.
        '''
        return libvlc_media_player_get_position(self)


    def set_position(self, f_pos):
        '''Set movie position as percentage between 0.0 and 1.0.
        This has no effect if playback is not enabled.
        This might not work depending on the underlying input format and protocol.
        @param f_pos: the position.
        '''
        return libvlc_media_player_set_position(self, f_pos)


    def set_chapter(self, i_chapter):
        '''Set movie chapter (if applicable).
        @param i_chapter: chapter number to play.
        '''
        return libvlc_media_player_set_chapter(self, i_chapter)


    def get_chapter(self):
        '''Get movie chapter.
        @return: chapter number currently playing, or -1 if there is no media.
        '''
        return libvlc_media_player_get_chapter(self)


    def get_chapter_count(self):
        '''Get movie chapter count.
        @return: number of chapters in movie, or -1.
        '''
        return libvlc_media_player_get_chapter_count(self)


    def will_play(self):
        '''Is the player able to play.
        @return: boolean \libvlc_return_bool.
        '''
        return libvlc_media_player_will_play(self)


    def get_chapter_count_for_title(self, i_title):
        '''Get title chapter count.
        @param i_title: title.
        @return: number of chapters in title, or -1.
        '''
        return libvlc_media_player_get_chapter_count_for_title(self, i_title)


    def set_title(self, i_title):
        '''Set movie title.
        @param i_title: title number to play.
        '''
        return libvlc_media_player_set_title(self, i_title)


    def get_title(self):
        '''Get movie title.
        @return: title number currently playing, or -1.
        '''
        return libvlc_media_player_get_title(self)


    def get_title_count(self):
        '''Get movie title count.
        @return: title number count, or -1.
        '''
        return libvlc_media_player_get_title_count(self)


    def previous_chapter(self):
        '''Set previous chapter (if applicable).
        '''
        return libvlc_media_player_previous_chapter(self)


    def next_chapter(self):
        '''Set next chapter (if applicable).
        '''
        return libvlc_media_player_next_chapter(self)


    def get_rate(self):
        '''Get the requested movie play rate.
        @warning: Depending on the underlying media, the requested rate may be
        different from the real playback rate.
        @return: movie play rate.
        '''
        return libvlc_media_player_get_rate(self)


    def set_rate(self, rate):
        '''Set movie play rate.
        @param rate: movie play rate to set.
        @return: -1 if an error was detected, 0 otherwise (but even then, it might not actually work depending on the underlying media protocol).
        '''
        return libvlc_media_player_set_rate(self, rate)


    def get_state(self):
        '''Get current movie state.
        @return: the current state of the media player (playing, paused, ...) See libvlc_state_t.
        '''
        return libvlc_media_player_get_state(self)


    def has_vout(self):
        '''How many video outputs does this media player have?
        @return: the number of video outputs.
        '''
        return libvlc_media_player_has_vout(self)


    def is_seekable(self):
        '''Is this media player seekable?
        @return: true if the media player can seek \libvlc_return_bool.
        '''
        return libvlc_media_player_is_seekable(self)


    def can_pause(self):
        '''Can this media player be paused?
        @return: true if the media player can pause \libvlc_return_bool.
        '''
        return libvlc_media_player_can_pause(self)


    def program_scrambled(self):
        '''Check if the current program is scrambled.
        @return: true if the current program is scrambled \libvlc_return_bool.
        @version: LibVLC 2.2.0 or later.
        '''
        return libvlc_media_player_program_scrambled(self)


    def next_frame(self):
        '''Display the next frame (if supported).
        '''
        return libvlc_media_player_next_frame(self)


    def navigate(self, navigate):
        '''Navigate through DVD Menu.
        @param navigate: the Navigation mode.
        @version: libVLC 2.0.0 or later.
        '''
        return libvlc_media_player_navigate(self, navigate)


    def set_video_title_display(self, position, timeout):
        '''Set if, and how, the video title will be shown when media is played.
        @param position: position at which to display the title, or libvlc_position_disable to prevent the title from being displayed.
        @param timeout: title display timeout in milliseconds (ignored if libvlc_position_disable).
        @version: libVLC 2.1.0 or later.
        '''
        return libvlc_media_player_set_video_title_display(self, position, timeout)


    def add_slave(self, i_type, psz_uri, b_select):
        return libvlc_media_player_add_slave(self, i_type, str_to_bytes(psz_uri), b_select)


    def toggle_fullscreen(self):
        return libvlc_toggle_fullscreen(self)


    def set_fullscreen(self, b_fullscreen):
        return libvlc_set_fullscreen(self, b_fullscreen)


    def get_fullscreen(self):
        return libvlc_get_fullscreen(self)

    def audio_output_set(self, psz_name):
        return libvlc_audio_output_set(self, str_to_bytes(psz_name))


    def audio_output_device_enum(self):
        return libvlc_audio_output_device_enum(self)


    def audio_output_device_set(self, module, device_id):
        return libvlc_audio_output_device_set(self, str_to_bytes(module), str_to_bytes(device_id))


    def audio_output_device_get(self):
        return libvlc_audio_output_device_get(self)


    def audio_toggle_mute(self):
        '''Toggle mute status.
        '''
        return libvlc_audio_toggle_mute(self)


    def audio_get_mute(self):
        '''Get current mute status.
        @return: the mute status (boolean) if defined, -1 if undefined/unapplicable.
        '''
        return libvlc_audio_get_mute(self)


    def audio_set_mute(self, status):
        '''Set mute status.
        @param status: If status is true then mute, otherwise unmute @warning This function does not always work. If there are no active audio playback stream, the mute status might not be available. If digital pass-through (S/PDIF, HDMI...) is in use, muting may be unapplicable. Also some audio output plugins do not support muting at all. @note To force silent playback, disable all audio tracks. This is more efficient and reliable than mute.
        '''
        return libvlc_audio_set_mute(self, status)


    def audio_get_volume(self):
        '''Get current software audio volume.
        @return: the software volume in percents (0 = mute, 100 = nominal / 0dB).
        '''
        return libvlc_audio_get_volume(self)


    def audio_set_volume(self, i_volume):
        '''Set current software audio volume.
        @param i_volume: the volume in percents (0 = mute, 100 = 0dB).
        @return: 0 if the volume was set, -1 if it was out of range.
        '''
        return libvlc_audio_set_volume(self, i_volume)


    def audio_get_track_count(self):
        '''Get number of available audio tracks.
        @return: the number of available audio tracks (int), or -1 if unavailable.
        '''
        return libvlc_audio_get_track_count(self)


    def audio_get_track(self):
        '''Get current audio track.
        @return: the audio track ID or -1 if no active input.
        '''
        return libvlc_audio_get_track(self)


    def audio_set_track(self, i_track):
        '''Set current audio track.
        @param i_track: the track ID (i_id field from track description).
        @return: 0 on success, -1 on error.
        '''
        return libvlc_audio_set_track(self, i_track)


    def audio_get_channel(self):
        '''Get current audio channel.
        @return: the audio channel See libvlc_audio_output_channel_t.
        '''
        return libvlc_audio_get_channel(self)


    def audio_set_channel(self, channel):
        '''Set current audio channel.
        @param channel: the audio channel, See libvlc_audio_output_channel_t.
        @return: 0 on success, -1 on error.
        '''
        return libvlc_audio_set_channel(self, channel)


    def audio_get_delay(self):
        '''Get current audio delay.
        @return: the audio delay (microseconds).
        @version: LibVLC 1.1.1 or later.
        '''
        return libvlc_audio_get_delay(self)


    def audio_set_delay(self, i_delay):
        '''Set current audio delay. The audio delay will be reset to zero each time the media changes.
        @param i_delay: the audio delay (microseconds).
        @return: 0 on success, -1 on error.
        @version: LibVLC 1.1.1 or later.
        '''
        return libvlc_audio_set_delay(self, i_delay)


    def set_equalizer(self, p_equalizer):
        '''Apply new equalizer settings to a media player.
        The equalizer is first created by invoking L{audio_equalizer_new}() or
        L{audio_equalizer_new_from_preset}().
        It is possible to apply new equalizer settings to a media player whether the media
        player is currently playing media or not.
        Invoking this method will immediately apply the new equalizer settings to the audio
        output of the currently playing media if there is any.
        If there is no currently playing media, the new equalizer settings will be applied
        later if and when new media is played.
        Equalizer settings will automatically be applied to subsequently played media.
        To disable the equalizer for a media player invoke this method passing None for the
        p_equalizer parameter.
        The media player does not keep a reference to the supplied equalizer so it is safe
        for an application to release the equalizer reference any time after this method
        returns.
        @param p_equalizer: opaque equalizer handle, or None to disable the equalizer for this media player.
        @return: zero on success, -1 on error.
        @version: LibVLC 2.2.0 or later.
        '''
        return libvlc_media_player_set_equalizer(self, p_equalizer)


    def get_role(self):
        '''Gets the media role.
        @return: the media player role (\ref libvlc_media_player_role_t).
        @version: LibVLC 3.0.0 and later.
        '''
        return libvlc_media_player_get_role(self)


    def set_role(self, role):
        '''Sets the media role.
        @param role: the media player role (\ref libvlc_media_player_role_t).
        @return: 0 on success, -1 on error.
        '''
        return libvlc_media_player_set_role(self, role)




def libvlc_media_player_get_fps(p_mi):
    '''Get movie fps rate
    This function is provided for backward compatibility. It cannot deal with
    multiple video tracks. In LibVLC versions prior to 3.0, it would also fail
    if the file format did not convey the frame rate explicitly.
    \deprecated Consider using L{libvlc_media_tracks_get}() instead.
    @param p_mi: the Media Player.
    @return: frames per second (fps) for this playing movie, or 0 if unspecified.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_fps', None) or \
        _Cfunction('libvlc_media_player_get_fps', ((1,),), None,
                    ctypes.c_float, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_agl(p_mi, drawable):
    '''\deprecated Use L{libvlc_media_player_set_nsobject}() instead.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_agl', None) or \
        _Cfunction('libvlc_media_player_set_agl', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_uint32)
    return f(p_mi, drawable)

def libvlc_media_player_get_agl(p_mi):
    '''\deprecated Use L{libvlc_media_player_get_nsobject}() instead.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_agl', None) or \
        _Cfunction('libvlc_media_player_get_agl', ((1,),), None,
                    ctypes.c_uint32, MediaPlayer)
    return f(p_mi)

def libvlc_errmsg():
    '''A human-readable error message for the last LibVLC error in the calling
    thread. The resulting string is valid until another error occurs (at least
    until the next LibVLC call).
    @warning
    This will be None if there was no error.
    '''
    f = _Cfunctions.get('libvlc_errmsg', None) or \
        _Cfunction('libvlc_errmsg', (), None,
                    ctypes.c_char_p)
    return f()

def libvlc_clearerr():
    '''Clears the LibVLC error status for the current thread. This is optional.
    By default, the error status is automatically overridden when a new error
    occurs, and destroyed when the thread exits.
    '''
    f = _Cfunctions.get('libvlc_clearerr', None) or \
        _Cfunction('libvlc_clearerr', (), None,
                    None)
    return f()

def libvlc_vprinterr(fmt, ap):
    '''Sets the LibVLC error status and message for the current thread.
    Any previous error is overridden.
    @param fmt: the format string.
    @param ap: the arguments.
    @return: a nul terminated string in any case.
    '''
    f = _Cfunctions.get('libvlc_vprinterr', None) or \
        _Cfunction('libvlc_vprinterr', ((1,), (1,),), None,
                    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p)
    return f(fmt, ap)

def libvlc_new(argc, argv):
    '''Create and initialize a libvlc instance.
    This functions accept a list of "command line" arguments similar to the
    main(). These arguments affect the LibVLC instance default configuration.
    @note
    LibVLC may create threads. Therefore, any thread-unsafe process
    initialization must be performed before calling L{libvlc_new}(). In particular
    and where applicable:
    - setlocale() and textdomain(),
    - setenv(), unsetenv() and putenv(),
    - with the X11 display system, XInitThreads()
      (see also L{libvlc_media_player_set_xwindow}()) and
    - on Microsoft Windows, SetErrorMode().
    - sigprocmask() shall never be invoked; pthread_sigmask() can be used.
    On POSIX systems, the SIGCHLD signal must B{not} be ignored, i.e. the
    signal handler must set to SIG_DFL or a function pointer, not SIG_IGN.
    Also while LibVLC is active, the wait() function shall not be called, and
    any call to waitpid() shall use a strictly positive value for the first
    parameter (i.e. the PID). Failure to follow those rules may lead to a
    deadlock or a busy loop.
    Also on POSIX systems, it is recommended that the SIGPIPE signal be blocked,
    even if it is not, in principles, necessary.
    On Microsoft Windows Vista/2008, the process error mode
    SEM_FAILCRITICALERRORS flag B{must} be set with the SetErrorMode()
    function before using LibVLC. On later versions, it is optional and
    unnecessary.
    @param argc: the number of arguments (should be 0).
    @param argv: list of arguments (should be None).
    @return: the libvlc instance or None in case of error.
    @version Arguments are meant to be passed from the command line to LibVLC, just like VLC media player does. The list of valid arguments depends on the LibVLC version, the operating system and platform, and set of available LibVLC plugins. Invalid or unsupported arguments will cause the function to fail (i.e. return None). Also, some arguments may alter the behaviour or otherwise interfere with other LibVLC functions. @warning There is absolutely no warranty or promise of forward, backward and cross-platform compatibility with regards to L{libvlc_new}() arguments. We recommend that you do not use them, other than when debugging.
    '''
    f = _Cfunctions.get('libvlc_new', None) or \
        _Cfunction('libvlc_new', ((1,), (1,),), class_result(Instance),
                    ctypes.c_void_p, ctypes.c_int, ListPOINTER(ctypes.c_char_p))
    return f(argc, argv)

def libvlc_release(p_instance):
    '''Decrement the reference count of a libvlc instance, and destroy it
    if it reaches zero.
    @param p_instance: the instance to destroy.
    '''
    f = _Cfunctions.get('libvlc_release', None) or \
        _Cfunction('libvlc_release', ((1,),), None,
                    None, Instance)
    return f(p_instance)

def libvlc_retain(p_instance):
    '''Increments the reference count of a libvlc instance.
    The initial reference count is 1 after L{libvlc_new}() returns.
    @param p_instance: the instance to reference.
    '''
    f = _Cfunctions.get('libvlc_retain', None) or \
        _Cfunction('libvlc_retain', ((1,),), None,
                    None, Instance)
    return f(p_instance)

def libvlc_add_intf(p_instance, name):
    '''Try to start a user interface for the libvlc instance.
    @param p_instance: the instance.
    @param name: interface name, or None for default.
    @return: 0 on success, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_add_intf', None) or \
        _Cfunction('libvlc_add_intf', ((1,), (1,),), None,
                    ctypes.c_int, Instance, ctypes.c_char_p)
    return f(p_instance, name)

def libvlc_set_user_agent(p_instance, name, http):
    '''Sets the application name. LibVLC passes this as the user agent string
    when a protocol requires it.
    @param p_instance: LibVLC instance.
    @param name: human-readable application name, e.g. "FooBar player 1.2.3".
    @param http: HTTP User Agent, e.g. "FooBar/1.2.3 Python/2.6.0".
    @version: LibVLC 1.1.1 or later.
    '''
    f = _Cfunctions.get('libvlc_set_user_agent', None) or \
        _Cfunction('libvlc_set_user_agent', ((1,), (1,), (1,),), None,
                    None, Instance, ctypes.c_char_p, ctypes.c_char_p)
    return f(p_instance, name, http)

def libvlc_set_app_id(p_instance, id, version, icon):
    '''Sets some meta-information about the application.
    See also L{libvlc_set_user_agent}().
    @param p_instance: LibVLC instance.
    @param id: Java-style application identifier, e.g. "com.acme.foobar".
    @param version: application version numbers, e.g. "1.2.3".
    @param icon: application icon name, e.g. "foobar".
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_set_app_id', None) or \
        _Cfunction('libvlc_set_app_id', ((1,), (1,), (1,), (1,),), None,
                    None, Instance, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p)
    return f(p_instance, id, version, icon)

def libvlc_get_version():
    '''Retrieve libvlc version.
    Example: "1.1.0-git The Luggage".
    @return: a string containing the libvlc version.
    '''
    f = _Cfunctions.get('libvlc_get_version', None) or \
        _Cfunction('libvlc_get_version', (), None,
                    ctypes.c_char_p)
    return f()

def libvlc_get_compiler():
    '''Retrieve libvlc compiler version.
    Example: "gcc version 4.2.3 (Ubuntu 4.2.3-2ubuntu6)".
    @return: a string containing the libvlc compiler version.
    '''
    f = _Cfunctions.get('libvlc_get_compiler', None) or \
        _Cfunction('libvlc_get_compiler', (), None,
                    ctypes.c_char_p)
    return f()

def libvlc_get_changeset():
    '''Retrieve libvlc changeset.
    Example: "aa9bce0bc4".
    @return: a string containing the libvlc changeset.
    '''
    f = _Cfunctions.get('libvlc_get_changeset', None) or \
        _Cfunction('libvlc_get_changeset', (), None,
                    ctypes.c_char_p)
    return f()

def libvlc_free(ptr):
    '''Frees an heap allocation returned by a LibVLC function.
    If you know you're using the same underlying C run-time as the LibVLC
    implementation, then you can call ANSI C free() directly instead.
    @param ptr: the pointer.
    '''
    f = _Cfunctions.get('libvlc_free', None) or \
        _Cfunction('libvlc_free', ((1,),), None,
                    None, ctypes.c_void_p)
    return f(ptr)

def libvlc_event_attach(p_event_manager, i_event_type, f_callback, user_data):
    '''Register for an event notification.
    @param p_event_manager: the event manager to which you want to attach to. Generally it is obtained by vlc_my_object_event_manager() where my_object is the object you want to listen to.
    @param i_event_type: the desired event to which we want to listen.
    @param f_callback: the function to call when i_event_type occurs.
    @param user_data: user provided data to carry with the event.
    @return: 0 on success, ENOMEM on error.
    '''
    f = _Cfunctions.get('libvlc_event_attach', None) or \
        _Cfunction('libvlc_event_attach', ((1,), (1,), (1,), (1,),), None,
                    ctypes.c_int, EventManager, ctypes.c_uint, Callback, ctypes.c_void_p)
    return f(p_event_manager, i_event_type, f_callback, user_data)

def libvlc_event_detach(p_event_manager, i_event_type, f_callback, p_user_data):
    '''Unregister an event notification.
    @param p_event_manager: the event manager.
    @param i_event_type: the desired event to which we want to unregister.
    @param f_callback: the function to call when i_event_type occurs.
    @param p_user_data: user provided data to carry with the event.
    '''
    f = _Cfunctions.get('libvlc_event_detach', None) or \
        _Cfunction('libvlc_event_detach', ((1,), (1,), (1,), (1,),), None,
                    None, EventManager, ctypes.c_uint, Callback, ctypes.c_void_p)
    return f(p_event_manager, i_event_type, f_callback, p_user_data)

def libvlc_event_type_name(event_type):
    '''Get an event's type name.
    @param event_type: the desired event.
    '''
    f = _Cfunctions.get('libvlc_event_type_name', None) or \
        _Cfunction('libvlc_event_type_name', ((1,),), None,
                    ctypes.c_char_p, ctypes.c_uint)
    return f(event_type)

def libvlc_log_get_context(ctx):
    '''Gets debugging information about a log message: the name of the VLC module
    emitting the message and the message location within the source code.
    The returned module name and file name will be None if unknown.
    The returned line number will similarly be zero if unknown.
    @param ctx: message context (as passed to the @ref libvlc_log_cb callback).
    @return: module module name storage (or None), file source code file name storage (or None), line source code file line number storage (or None).
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_log_get_context', None) or \
        _Cfunction('libvlc_log_get_context', ((1,), (2,), (2,), (2,),), None,
                    None, Log_ptr, ListPOINTER(ctypes.c_char_p), ListPOINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint))
    return f(ctx)

def libvlc_log_get_object(ctx, id):
    '''Gets VLC object information about a log message: the type name of the VLC
    object emitting the message, the object header if any and a temporaly-unique
    object identifier. This information is mainly meant for B{manual}
    troubleshooting.
    The returned type name may be "generic" if unknown, but it cannot be None.
    The returned header will be None if unset; in current versions, the header
    is used to distinguish for VLM inputs.
    The returned object ID will be zero if the message is not associated with
    any VLC object.
    @param ctx: message context (as passed to the @ref libvlc_log_cb callback).
    @return: name object name storage (or None), header object header (or None), line source code file line number storage (or None).
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_log_get_object', None) or \
        _Cfunction('libvlc_log_get_object', ((1,), (2,), (2,), (1,),), None,
                    None, Log_ptr, ListPOINTER(ctypes.c_char_p), ListPOINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint))
    return f(ctx, id)

def libvlc_log_unset(p_instance):
    '''Unsets the logging callback for a LibVLC instance. This is rarely needed:
    the callback is implicitly unset when the instance is destroyed.
    This function will wait for any pending callbacks invocation to complete
    (causing a deadlock if called from within the callback).
    @param p_instance: libvlc instance.
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_log_unset', None) or \
        _Cfunction('libvlc_log_unset', ((1,),), None,
                    None, Instance)
    return f(p_instance)

def libvlc_log_set(cb, data, p_instance):
    '''Sets the logging callback for a LibVLC instance.
    This function is thread-safe: it will wait for any pending callbacks
    invocation to complete.
    @param cb: callback function pointer.
    @param data: opaque data pointer for the callback function @note Some log messages (especially debug) are emitted by LibVLC while is being initialized. These messages cannot be captured with this interface. @warning A deadlock may occur if this function is called from the callback.
    @param p_instance: libvlc instance.
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_log_set', None) or \
        _Cfunction('libvlc_log_set', ((1,), (1,), (1,),), None,
                    None, Instance, LogCb, ctypes.c_void_p)
    return f(cb, data, p_instance)

def libvlc_log_set_file(p_instance, stream):
    '''Sets up logging to a file.
    @param p_instance: libvlc instance.
    @param stream: FILE pointer opened for writing (the FILE pointer must remain valid until L{libvlc_log_unset}()).
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_log_set_file', None) or \
        _Cfunction('libvlc_log_set_file', ((1,), (1,),), None,
                    None, Instance, FILE_ptr)
    return f(p_instance, stream)

def libvlc_module_description_list_release(p_list):
    '''Release a list of module descriptions.
    @param p_list: the list to be released.
    '''
    f = _Cfunctions.get('libvlc_module_description_list_release', None) or \
        _Cfunction('libvlc_module_description_list_release', ((1,),), None,
                    None, ctypes.POINTER(ModuleDescription))
    return f(p_list)

def libvlc_audio_filter_list_get(p_instance):
    '''Returns a list of audio filters that are available.
    @param p_instance: libvlc instance.
    @return: a list of module descriptions. It should be freed with L{libvlc_module_description_list_release}(). In case of an error, None is returned. See L{ModuleDescription} See L{libvlc_module_description_list_release}.
    '''
    f = _Cfunctions.get('libvlc_audio_filter_list_get', None) or \
        _Cfunction('libvlc_audio_filter_list_get', ((1,),), None,
                    ctypes.POINTER(ModuleDescription), Instance)
    return f(p_instance)

def libvlc_video_filter_list_get(p_instance):
    '''Returns a list of video filters that are available.
    @param p_instance: libvlc instance.
    @return: a list of module descriptions. It should be freed with L{libvlc_module_description_list_release}(). In case of an error, None is returned. See L{ModuleDescription} See L{libvlc_module_description_list_release}.
    '''
    f = _Cfunctions.get('libvlc_video_filter_list_get', None) or \
        _Cfunction('libvlc_video_filter_list_get', ((1,),), None,
                    ctypes.POINTER(ModuleDescription), Instance)
    return f(p_instance)

def libvlc_clock():
    '''Return the current time as defined by LibVLC. The unit is the microsecond.
    Time increases monotonically (regardless of time zone changes and RTC
    adjustements).
    The origin is arbitrary but consistent across the whole system
    (e.g. the system uptim, the time since the system was booted).
    @note: On systems that support it, the POSIX monotonic clock is used.
    '''
    f = _Cfunctions.get('libvlc_clock', None) or \
        _Cfunction('libvlc_clock', (), None,
                    ctypes.c_int64)
    return f()

def libvlc_dialog_set_context(p_id, p_context):
    '''Associate an opaque pointer with the dialog id.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_dialog_set_context', None) or \
        _Cfunction('libvlc_dialog_set_context', ((1,), (1,),), None,
                    None, ctypes.c_void_p, ctypes.c_void_p)
    return f(p_id, p_context)

def libvlc_dialog_get_context(p_id):
    '''Return the opaque pointer associated with the dialog id.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_dialog_get_context', None) or \
        _Cfunction('libvlc_dialog_get_context', ((1,),), None,
                    ctypes.c_void_p, ctypes.c_void_p)
    return f(p_id)

def libvlc_dialog_post_login(p_id, psz_username, psz_password, b_store):
    '''Post a login answer
    After this call, p_id won't be valid anymore
    See libvlc_dialog_cbs.pf_display_login.
    @param p_id: id of the dialog.
    @param psz_username: valid and non empty string.
    @param psz_password: valid string (can be empty).
    @param b_store: if true, store the credentials.
    @return: 0 on success, or -1 on error.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_dialog_post_login', None) or \
        _Cfunction('libvlc_dialog_post_login', ((1,), (1,), (1,), (1,),), None,
                    ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool)
    return f(p_id, psz_username, psz_password, b_store)

def libvlc_dialog_post_action(p_id, i_action):
    '''Post a question answer
    After this call, p_id won't be valid anymore
    See libvlc_dialog_cbs.pf_display_question.
    @param p_id: id of the dialog.
    @param i_action: 1 for action1, 2 for action2.
    @return: 0 on success, or -1 on error.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_dialog_post_action', None) or \
        _Cfunction('libvlc_dialog_post_action', ((1,), (1,),), None,
                    ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
    return f(p_id, i_action)

def libvlc_dialog_dismiss(p_id):
    '''Dismiss a dialog
    After this call, p_id won't be valid anymore
    See libvlc_dialog_cbs.pf_cancel.
    @param p_id: id of the dialog.
    @return: 0 on success, or -1 on error.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_dialog_dismiss', None) or \
        _Cfunction('libvlc_dialog_dismiss', ((1,),), None,
                    ctypes.c_int, ctypes.c_void_p)
    return f(p_id)

def libvlc_media_new_location(p_instance, psz_mrl):
    '''Create a media with a certain given media resource location,
    for instance a valid URL.
    @note: To refer to a local file with this function,
    the file://... URI syntax B{must} be used (see IETF RFC3986).
    We recommend using L{libvlc_media_new_path}() instead when dealing with
    local files.
    See L{libvlc_media_release}.
    @param p_instance: the instance.
    @param psz_mrl: the media location.
    @return: the newly created media or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_new_location', None) or \
        _Cfunction('libvlc_media_new_location', ((1,), (1,),), class_result(Media),
                    ctypes.c_void_p, Instance, ctypes.c_char_p)
    return f(p_instance, psz_mrl)

def libvlc_media_new_path(p_instance, path):
    '''Create a media for a certain file path.
    See L{libvlc_media_release}.
    @param p_instance: the instance.
    @param path: local filesystem path.
    @return: the newly created media or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_new_path', None) or \
        _Cfunction('libvlc_media_new_path', ((1,), (1,),), class_result(Media),
                    ctypes.c_void_p, Instance, ctypes.c_char_p)
    return f(p_instance, path)

def libvlc_media_new_fd(p_instance, fd):
    '''Create a media for an already open file descriptor.
    The file descriptor shall be open for reading (or reading and writing).
    Regular file descriptors, pipe read descriptors and character device
    descriptors (including TTYs) are supported on all platforms.
    Block device descriptors are supported where available.
    Directory descriptors are supported on systems that provide fdopendir().
    Sockets are supported on all platforms where they are file descriptors,
    i.e. all except Windows.
    @note: This library will B{not} automatically close the file descriptor
    under any circumstance. Nevertheless, a file descriptor can usually only be
    rendered once in a media player. To render it a second time, the file
    descriptor should probably be rewound to the beginning with lseek().
    See L{libvlc_media_release}.
    @param p_instance: the instance.
    @param fd: open file descriptor.
    @return: the newly created media or None on error.
    @version: LibVLC 1.1.5 and later.
    '''
    f = _Cfunctions.get('libvlc_media_new_fd', None) or \
        _Cfunction('libvlc_media_new_fd', ((1,), (1,),), class_result(Media),
                    ctypes.c_void_p, Instance, ctypes.c_int)
    return f(p_instance, fd)

def libvlc_media_new_callbacks(instance, open_cb, read_cb, seek_cb, close_cb, opaque):
    '''Create a media with custom callbacks to read the data from.
    @param instance: LibVLC instance.
    @param open_cb: callback to open the custom bitstream input media.
    @param read_cb: callback to read data (must not be None).
    @param seek_cb: callback to seek, or None if seeking is not supported.
    @param close_cb: callback to close the media, or None if unnecessary.
    @param opaque: data pointer for the open callback.
    @return: the newly created media or None on error @note If open_cb is None, the opaque pointer will be passed to read_cb, seek_cb and close_cb, and the stream size will be treated as unknown. @note The callbacks may be called asynchronously (from another thread). A single stream instance need not be reentrant. However the open_cb needs to be reentrant if the media is used by multiple player instances. @warning The callbacks may be used until all or any player instances that were supplied the media item are stopped. See L{libvlc_media_release}.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_new_callbacks', None) or \
        _Cfunction('libvlc_media_new_callbacks', ((1,), (1,), (1,), (1,), (1,), (1,),), class_result(Media),
                    ctypes.c_void_p, Instance, MediaOpenCb, MediaReadCb, MediaSeekCb, MediaCloseCb, ctypes.c_void_p)
    return f(instance, open_cb, read_cb, seek_cb, close_cb, opaque)

def libvlc_media_new_as_node(p_instance, psz_name):
    '''Create a media as an empty node with a given name.
    See L{libvlc_media_release}.
    @param p_instance: the instance.
    @param psz_name: the name of the node.
    @return: the new empty media or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_new_as_node', None) or \
        _Cfunction('libvlc_media_new_as_node', ((1,), (1,),), class_result(Media),
                    ctypes.c_void_p, Instance, ctypes.c_char_p)
    return f(p_instance, psz_name)

def libvlc_media_add_option(p_md, psz_options):
    '''Add an option to the media.
    This option will be used to determine how the media_player will
    read the media. This allows to use VLC's advanced
    reading/streaming options on a per-media basis.
    @note: The options are listed in 'vlc --long-help' from the command line,
    e.g. "-sout-all". Keep in mind that available options and their semantics
    vary across LibVLC versions and builds.
    @warning: Not all options affects L{Media} objects:
    Specifically, due to architectural issues most audio and video options,
    such as text renderer options, have no effects on an individual media.
    These options must be set through L{libvlc_new}() instead.
    @param p_md: the media descriptor.
    @param psz_options: the options (as a string).
    '''
    f = _Cfunctions.get('libvlc_media_add_option', None) or \
        _Cfunction('libvlc_media_add_option', ((1,), (1,),), None,
                    None, Media, ctypes.c_char_p)
    return f(p_md, psz_options)

def libvlc_media_add_option_flag(p_md, psz_options, i_flags):
    '''Add an option to the media with configurable flags.
    This option will be used to determine how the media_player will
    read the media. This allows to use VLC's advanced
    reading/streaming options on a per-media basis.
    The options are detailed in vlc --long-help, for instance
    "--sout-all". Note that all options are not usable on medias:
    specifically, due to architectural issues, video-related options
    such as text renderer options cannot be set on a single media. They
    must be set on the whole libvlc instance instead.
    @param p_md: the media descriptor.
    @param psz_options: the options (as a string).
    @param i_flags: the flags for this option.
    '''
    f = _Cfunctions.get('libvlc_media_add_option_flag', None) or \
        _Cfunction('libvlc_media_add_option_flag', ((1,), (1,), (1,),), None,
                    None, Media, ctypes.c_char_p, ctypes.c_uint)
    return f(p_md, psz_options, i_flags)

def libvlc_media_retain(p_md):
    '''Retain a reference to a media descriptor object (libvlc_media_t). Use
    L{libvlc_media_release}() to decrement the reference count of a
    media descriptor object.
    @param p_md: the media descriptor.
    '''
    f = _Cfunctions.get('libvlc_media_retain', None) or \
        _Cfunction('libvlc_media_retain', ((1,),), None,
                    None, Media)
    return f(p_md)

def libvlc_media_release(p_md):
    '''Decrement the reference count of a media descriptor object. If the
    reference count is 0, then L{libvlc_media_release}() will release the
    media descriptor object. It will send out an libvlc_MediaFreed event
    to all listeners. If the media descriptor object has been released it
    should not be used again.
    @param p_md: the media descriptor.
    '''
    f = _Cfunctions.get('libvlc_media_release', None) or \
        _Cfunction('libvlc_media_release', ((1,),), None,
                    None, Media)
    return f(p_md)

def libvlc_media_get_mrl(p_md):
    '''Get the media resource locator (mrl) from a media descriptor object.
    @param p_md: a media descriptor object.
    @return: string with mrl of media descriptor object.
    '''
    f = _Cfunctions.get('libvlc_media_get_mrl', None) or \
        _Cfunction('libvlc_media_get_mrl', ((1,),), string_result,
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_duplicate(p_md):
    '''Duplicate a media descriptor object.
    @param p_md: a media descriptor object.
    '''
    f = _Cfunctions.get('libvlc_media_duplicate', None) or \
        _Cfunction('libvlc_media_duplicate', ((1,),), class_result(Media),
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_get_meta(p_md, e_meta):
    '''Read the meta of the media.
    If the media has not yet been parsed this will return None.
    See L{libvlc_media_parse}
    See L{libvlc_media_parse_with_options}
    See libvlc_MediaMetaChanged.
    @param p_md: the media descriptor.
    @param e_meta: the meta to read.
    @return: the media's meta.
    '''
    f = _Cfunctions.get('libvlc_media_get_meta', None) or \
        _Cfunction('libvlc_media_get_meta', ((1,), (1,),), string_result,
                    ctypes.c_void_p, Media, Meta)
    return f(p_md, e_meta)

def libvlc_media_set_meta(p_md, e_meta, psz_value):
    '''Set the meta of the media (this function will not save the meta, call
    L{libvlc_media_save_meta} in order to save the meta).
    @param p_md: the media descriptor.
    @param e_meta: the meta to write.
    @param psz_value: the media's meta.
    '''
    f = _Cfunctions.get('libvlc_media_set_meta', None) or \
        _Cfunction('libvlc_media_set_meta', ((1,), (1,), (1,),), None,
                    None, Media, Meta, ctypes.c_char_p)
    return f(p_md, e_meta, psz_value)

def libvlc_media_save_meta(p_md):
    '''Save the meta previously set.
    @param p_md: the media desriptor.
    @return: true if the write operation was successful.
    '''
    f = _Cfunctions.get('libvlc_media_save_meta', None) or \
        _Cfunction('libvlc_media_save_meta', ((1,),), None,
                    ctypes.c_int, Media)
    return f(p_md)

def libvlc_media_get_state(p_md):
    '''Get current state of media descriptor object. Possible media states are
    libvlc_NothingSpecial=0, libvlc_Opening, libvlc_Playing, libvlc_Paused,
    libvlc_Stopped, libvlc_Ended, libvlc_Error.
    See libvlc_state_t.
    @param p_md: a media descriptor object.
    @return: state of media descriptor object.
    '''
    f = _Cfunctions.get('libvlc_media_get_state', None) or \
        _Cfunction('libvlc_media_get_state', ((1,),), None,
                    State, Media)
    return f(p_md)

def libvlc_media_get_stats(p_md, p_stats):
    '''Get the current statistics about the media.
    @param p_md:: media descriptor object.
    @param p_stats:: structure that contain the statistics about the media (this structure must be allocated by the caller).
    @return: true if the statistics are available, false otherwise \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_get_stats', None) or \
        _Cfunction('libvlc_media_get_stats', ((1,), (1,),), None,
                    ctypes.c_int, Media, ctypes.POINTER(MediaStats))
    return f(p_md, p_stats)

def libvlc_media_subitems(p_md):
    '''Get subitems of media descriptor object. This will increment
    the reference count of supplied media descriptor object. Use
    L{libvlc_media_list_release}() to decrement the reference counting.
    @param p_md: media descriptor object.
    @return: list of media descriptor subitems or None.
    '''
    f = _Cfunctions.get('libvlc_media_subitems', None) or \
        _Cfunction('libvlc_media_subitems', ((1,),), class_result(MediaList),
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_event_manager(p_md):
    '''Get event manager from media descriptor object.
    NOTE: this function doesn't increment reference counting.
    @param p_md: a media descriptor object.
    @return: event manager object.
    '''
    f = _Cfunctions.get('libvlc_media_event_manager', None) or \
        _Cfunction('libvlc_media_event_manager', ((1,),), class_result(EventManager),
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_get_duration(p_md):
    '''Get duration (in ms) of media descriptor object item.
    @param p_md: media descriptor object.
    @return: duration of media item or -1 on error.
    '''
    f = _Cfunctions.get('libvlc_media_get_duration', None) or \
        _Cfunction('libvlc_media_get_duration', ((1,),), None,
                    ctypes.c_longlong, Media)
    return f(p_md)

def libvlc_media_parse(p_md):
    '''Parse a media.
    This fetches (local) art, meta data and tracks information.
    The method is synchronous.
    See L{libvlc_media_parse_with_options}
    See L{libvlc_media_get_meta}
    See libvlc_media_get_tracks_info.
    @param p_md: media descriptor object.
    '''
    f = _Cfunctions.get('libvlc_media_parse', None) or \
        _Cfunction('libvlc_media_parse', ((1,),), None,
                    None, Media)
    return f(p_md)

def libvlc_media_parse_with_options(p_md, parse_flag, timeout):
    '''Parse the media asynchronously with options.
    This fetches (local or network) art, meta data and/or tracks information.
    This method is the extended version of L{libvlc_media_parse_with_options}().
    To track when this is over you can listen to libvlc_MediaParsedChanged
    event. However if this functions returns an error, you will not receive any
    events.
    It uses a flag to specify parse options (see libvlc_media_parse_flag_t). All
    these flags can be combined. By default, media is parsed if it's a local
    file.
    See libvlc_MediaParsedChanged
    See L{libvlc_media_get_meta}
    See L{libvlc_media_tracks_get}
    See L{libvlc_media_get_parsed_status}
    See libvlc_media_parse_flag_t.
    @param p_md: media descriptor object.
    @param parse_flag: parse options:
    @param timeout: maximum time allowed to preparse the media. If -1, the default "preparse-timeout" option will be used as a timeout. If 0, it will wait indefinitely. If > 0, the timeout will be used (in milliseconds).
    @return: -1 in case of error, 0 otherwise.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_parse_with_options', None) or \
        _Cfunction('libvlc_media_parse_with_options', ((1,), (1,), (1,),), None,
                    ctypes.c_int, Media, MediaParseFlag, ctypes.c_int)
    return f(p_md, parse_flag, timeout)

def libvlc_media_get_parsed_status(p_md):
    '''Get Parsed status for media descriptor object.
    See libvlc_MediaParsedChanged
    See libvlc_media_parsed_status_t.
    @param p_md: media descriptor object.
    @return: a value of the libvlc_media_parsed_status_t enum.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_get_parsed_status', None) or \
        _Cfunction('libvlc_media_get_parsed_status', ((1,),), None,
                    MediaParsedStatus, Media)
    return f(p_md)

def libvlc_media_set_user_data(p_md, p_new_user_data):
    '''Sets media descriptor's user_data. user_data is specialized data
    accessed by the host application, VLC.framework uses it as a pointer to
    an native object that references a L{Media} pointer.
    @param p_md: media descriptor object.
    @param p_new_user_data: pointer to user data.
    '''
    f = _Cfunctions.get('libvlc_media_set_user_data', None) or \
        _Cfunction('libvlc_media_set_user_data', ((1,), (1,),), None,
                    None, Media, ctypes.c_void_p)
    return f(p_md, p_new_user_data)

def libvlc_media_get_user_data(p_md):
    '''Get media descriptor's user_data. user_data is specialized data
    accessed by the host application, VLC.framework uses it as a pointer to
    an native object that references a L{Media} pointer.
    @param p_md: media descriptor object.
    '''
    f = _Cfunctions.get('libvlc_media_get_user_data', None) or \
        _Cfunction('libvlc_media_get_user_data', ((1,),), None,
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_tracks_get(p_md, tracks):
    '''Get media descriptor's elementary streams description
    Note, you need to call L{libvlc_media_parse}() or play the media at least once
    before calling this function.
    Not doing this will result in an empty array.
    @param p_md: media descriptor object.
    @param tracks: address to store an allocated array of Elementary Streams descriptions (must be freed with L{libvlc_media_tracks_release}.
    @return: the number of Elementary Streams (zero on error).
    @version: LibVLC 2.1.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_tracks_get', None) or \
        _Cfunction('libvlc_media_tracks_get', ((1,), (1,),), None,
                    ctypes.c_uint, Media, ctypes.POINTER(ctypes.POINTER(MediaTrack)))
    return f(p_md, tracks)

def libvlc_media_get_codec_description(i_type, i_codec):
    '''Get codec description from media elementary stream.
    @param i_type: i_type from L{MediaTrack}.
    @param i_codec: i_codec or i_original_fourcc from L{MediaTrack}.
    @return: codec description.
    @version: LibVLC 3.0.0 and later. See L{MediaTrack}.
    '''
    f = _Cfunctions.get('libvlc_media_get_codec_description', None) or \
        _Cfunction('libvlc_media_get_codec_description', ((1,), (1,),), None,
                    ctypes.c_char_p, TrackType, ctypes.c_uint32)
    return f(i_type, i_codec)

def libvlc_media_tracks_release(p_tracks, i_count):
    '''Release media descriptor's elementary streams description array.
    @param p_tracks: tracks info array to release.
    @param i_count: number of elements in the array.
    @version: LibVLC 2.1.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_tracks_release', None) or \
        _Cfunction('libvlc_media_tracks_release', ((1,), (1,),), None,
                    None, ctypes.POINTER(MediaTrack), ctypes.c_uint)
    return f(p_tracks, i_count)

def libvlc_media_get_type(p_md):
    '''Get the media type of the media descriptor object.
    @param p_md: media descriptor object.
    @return: media type.
    @version: LibVLC 3.0.0 and later. See libvlc_media_type_t.
    '''
    f = _Cfunctions.get('libvlc_media_get_type', None) or \
        _Cfunction('libvlc_media_get_type', ((1,),), None,
                    MediaType, Media)
    return f(p_md)

def libvlc_media_slaves_add(p_md, i_type, i_priority, psz_uri):
    '''Add a slave to the current media.
    A slave is an external input source that may contains an additional subtitle
    track (like a .srt) or an additional audio track (like a .ac3).
    @note: This function must be called before the media is parsed (via
    L{libvlc_media_parse_with_options}()) or before the media is played (via
    L{libvlc_media_player_play}()).
    @param p_md: media descriptor object.
    @param i_type: subtitle or audio.
    @param i_priority: from 0 (low priority) to 4 (high priority).
    @param psz_uri: Uri of the slave (should contain a valid scheme).
    @return: 0 on success, -1 on error.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_slaves_add', None) or \
        _Cfunction('libvlc_media_slaves_add', ((1,), (1,), (1,), (1,),), None,
                    ctypes.c_int, Media, MediaSlaveType, ctypes.c_int, ctypes.c_char_p)
    return f(p_md, i_type, i_priority, psz_uri)

def libvlc_media_slaves_clear(p_md):
    '''Clear all slaves previously added by L{libvlc_media_slaves_add}() or
    internally.
    @param p_md: media descriptor object.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_slaves_clear', None) or \
        _Cfunction('libvlc_media_slaves_clear', ((1,),), None,
                    None, Media)
    return f(p_md)

def libvlc_media_slaves_get(p_md, ppp_slaves):
    '''Get a media descriptor's slave list
    The list will contain slaves parsed by VLC or previously added by
    L{libvlc_media_slaves_add}(). The typical use case of this function is to save
    a list of slave in a database for a later use.
    @param p_md: media descriptor object.
    @param ppp_slaves: address to store an allocated array of slaves (must be freed with L{libvlc_media_slaves_release}()) [OUT].
    @return: the number of slaves (zero on error).
    @version: LibVLC 3.0.0 and later. See L{libvlc_media_slaves_add}.
    '''
    f = _Cfunctions.get('libvlc_media_slaves_get', None) or \
        _Cfunction('libvlc_media_slaves_get', ((1,), (1,),), None,
                    ctypes.c_int, Media, ctypes.POINTER(ctypes.POINTER(MediaSlave)))
    return f(p_md, ppp_slaves)

def libvlc_media_slaves_release(pp_slaves, i_count):
    '''Release a media descriptor's slave list.
    @param pp_slaves: slave array to release.
    @param i_count: number of elements in the array.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_slaves_release', None) or \
        _Cfunction('libvlc_media_slaves_release', ((1,), (1,),), None,
                    None, ctypes.POINTER(MediaSlave), ctypes.c_int)
    return f(pp_slaves, i_count)

def libvlc_media_discoverer_new(p_inst, psz_name):
    '''Create a media discoverer object by name.
    After this object is created, you should attach to media_list events in
    order to be notified of new items discovered.
    You need to call L{libvlc_media_discoverer_start}() in order to start the
    discovery.
    See L{libvlc_media_discoverer_media_list}
    See libvlc_media_discoverer_event_manager
    See L{libvlc_media_discoverer_start}.
    @param p_inst: libvlc instance.
    @param psz_name: service name; use L{libvlc_media_discoverer_list_get}() to get a list of the discoverer names available in this libVLC instance.
    @return: media discover object or None in case of error.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_new', None) or \
        _Cfunction('libvlc_media_discoverer_new', ((1,), (1,),), class_result(MediaDiscoverer),
                    ctypes.c_void_p, Instance, ctypes.c_char_p)
    return f(p_inst, psz_name)

def libvlc_media_discoverer_start(p_mdis):
    '''Start media discovery.
    To stop it, call L{libvlc_media_discoverer_stop}() or
    L{libvlc_media_discoverer_list_release}() directly.
    See L{libvlc_media_discoverer_stop}.
    @param p_mdis: media discover object.
    @return: -1 in case of error, 0 otherwise.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_start', None) or \
        _Cfunction('libvlc_media_discoverer_start', ((1,),), None,
                    ctypes.c_int, MediaDiscoverer)
    return f(p_mdis)

def libvlc_media_discoverer_stop(p_mdis):
    '''Stop media discovery.
    See L{libvlc_media_discoverer_start}.
    @param p_mdis: media discover object.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_stop', None) or \
        _Cfunction('libvlc_media_discoverer_stop', ((1,),), None,
                    None, MediaDiscoverer)
    return f(p_mdis)

def libvlc_media_discoverer_release(p_mdis):
    '''Release media discover object. If the reference count reaches 0, then
    the object will be released.
    @param p_mdis: media service discover object.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_release', None) or \
        _Cfunction('libvlc_media_discoverer_release', ((1,),), None,
                    None, MediaDiscoverer)
    return f(p_mdis)

def libvlc_media_discoverer_media_list(p_mdis):
    '''Get media service discover media list.
    @param p_mdis: media service discover object.
    @return: list of media items.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_media_list', None) or \
        _Cfunction('libvlc_media_discoverer_media_list', ((1,),), class_result(MediaList),
                    ctypes.c_void_p, MediaDiscoverer)
    return f(p_mdis)

def libvlc_media_discoverer_is_running(p_mdis):
    '''Query if media service discover object is running.
    @param p_mdis: media service discover object.
    @return: true if running, false if not \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_is_running', None) or \
        _Cfunction('libvlc_media_discoverer_is_running', ((1,),), None,
                    ctypes.c_int, MediaDiscoverer)
    return f(p_mdis)

def libvlc_media_discoverer_list_get(p_inst, i_cat, ppp_services):
    '''Get media discoverer services by category.
    @param p_inst: libvlc instance.
    @param i_cat: category of services to fetch.
    @param ppp_services: address to store an allocated array of media discoverer services (must be freed with L{libvlc_media_discoverer_list_release}() by the caller) [OUT].
    @return: the number of media discoverer services (0 on error).
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_list_get', None) or \
        _Cfunction('libvlc_media_discoverer_list_get', ((1,), (1,), (1,),), None,
                    ctypes.c_size_t, Instance, MediaDiscovererCategory, ctypes.POINTER(ctypes.POINTER(MediaDiscovererDescription)))
    return f(p_inst, i_cat, ppp_services)

def libvlc_media_discoverer_list_release(pp_services, i_count):
    '''Release an array of media discoverer services.
    @param pp_services: array to release.
    @param i_count: number of elements in the array.
    @version: LibVLC 3.0.0 and later. See L{libvlc_media_discoverer_list_get}().
    '''
    f = _Cfunctions.get('libvlc_media_discoverer_list_release', None) or \
        _Cfunction('libvlc_media_discoverer_list_release', ((1,), (1,),), None,
                    None, ctypes.POINTER(MediaDiscovererDescription), ctypes.c_size_t)
    return f(pp_services, i_count)

def libvlc_media_library_new(p_instance):
    '''Create an new Media Library object.
    @param p_instance: the libvlc instance.
    @return: a new object or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_library_new', None) or \
        _Cfunction('libvlc_media_library_new', ((1,),), class_result(MediaLibrary),
                    ctypes.c_void_p, Instance)
    return f(p_instance)

def libvlc_media_library_release(p_mlib):
    '''Release media library object. This functions decrements the
    reference count of the media library object. If it reaches 0,
    then the object will be released.
    @param p_mlib: media library object.
    '''
    f = _Cfunctions.get('libvlc_media_library_release', None) or \
        _Cfunction('libvlc_media_library_release', ((1,),), None,
                    None, MediaLibrary)
    return f(p_mlib)

def libvlc_media_library_retain(p_mlib):
    '''Retain a reference to a media library object. This function will
    increment the reference counting for this object. Use
    L{libvlc_media_library_release}() to decrement the reference count.
    @param p_mlib: media library object.
    '''
    f = _Cfunctions.get('libvlc_media_library_retain', None) or \
        _Cfunction('libvlc_media_library_retain', ((1,),), None,
                    None, MediaLibrary)
    return f(p_mlib)

def libvlc_media_library_load(p_mlib):
    '''Load media library.
    @param p_mlib: media library object.
    @return: 0 on success, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_media_library_load', None) or \
        _Cfunction('libvlc_media_library_load', ((1,),), None,
                    ctypes.c_int, MediaLibrary)
    return f(p_mlib)

def libvlc_media_library_media_list(p_mlib):
    '''Get media library subitems.
    @param p_mlib: media library object.
    @return: media list subitems.
    '''
    f = _Cfunctions.get('libvlc_media_library_media_list', None) or \
        _Cfunction('libvlc_media_library_media_list', ((1,),), class_result(MediaList),
                    ctypes.c_void_p, MediaLibrary)
    return f(p_mlib)

def libvlc_media_list_new(p_instance):
    '''Create an empty media list.
    @param p_instance: libvlc instance.
    @return: empty media list, or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_list_new', None) or \
        _Cfunction('libvlc_media_list_new', ((1,),), class_result(MediaList),
                    ctypes.c_void_p, Instance)
    return f(p_instance)

def libvlc_media_list_release(p_ml):
    '''Release media list created with L{libvlc_media_list_new}().
    @param p_ml: a media list created with L{libvlc_media_list_new}().
    '''
    f = _Cfunctions.get('libvlc_media_list_release', None) or \
        _Cfunction('libvlc_media_list_release', ((1,),), None,
                    None, MediaList)
    return f(p_ml)

def libvlc_media_list_retain(p_ml):
    '''Retain reference to a media list.
    @param p_ml: a media list created with L{libvlc_media_list_new}().
    '''
    f = _Cfunctions.get('libvlc_media_list_retain', None) or \
        _Cfunction('libvlc_media_list_retain', ((1,),), None,
                    None, MediaList)
    return f(p_ml)

def libvlc_media_list_set_media(p_ml, p_md):
    '''Associate media instance with this media list instance.
    If another media instance was present it will be released.
    The L{libvlc_media_list_lock} should NOT be held upon entering this function.
    @param p_ml: a media list instance.
    @param p_md: media instance to add.
    '''
    f = _Cfunctions.get('libvlc_media_list_set_media', None) or \
        _Cfunction('libvlc_media_list_set_media', ((1,), (1,),), None,
                    None, MediaList, Media)
    return f(p_ml, p_md)

def libvlc_media_list_media(p_ml):
    '''Get media instance from this media list instance. This action will increase
    the refcount on the media instance.
    The L{libvlc_media_list_lock} should NOT be held upon entering this function.
    @param p_ml: a media list instance.
    @return: media instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_media', None) or \
        _Cfunction('libvlc_media_list_media', ((1,),), class_result(Media),
                    ctypes.c_void_p, MediaList)
    return f(p_ml)

def libvlc_media_list_add_media(p_ml, p_md):
    '''Add media instance to media list
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @param p_md: a media instance.
    @return: 0 on success, -1 if the media list is read-only.
    '''
    f = _Cfunctions.get('libvlc_media_list_add_media', None) or \
        _Cfunction('libvlc_media_list_add_media', ((1,), (1,),), None,
                    ctypes.c_int, MediaList, Media)
    return f(p_ml, p_md)

def libvlc_media_list_insert_media(p_ml, p_md, i_pos):
    '''Insert media instance in media list on a position
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @param p_md: a media instance.
    @param i_pos: position in array where to insert.
    @return: 0 on success, -1 if the media list is read-only.
    '''
    f = _Cfunctions.get('libvlc_media_list_insert_media', None) or \
        _Cfunction('libvlc_media_list_insert_media', ((1,), (1,), (1,),), None,
                    ctypes.c_int, MediaList, Media, ctypes.c_int)
    return f(p_ml, p_md, i_pos)

def libvlc_media_list_remove_index(p_ml, i_pos):
    '''Remove media instance from media list on a position
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @param i_pos: position in array where to insert.
    @return: 0 on success, -1 if the list is read-only or the item was not found.
    '''
    f = _Cfunctions.get('libvlc_media_list_remove_index', None) or \
        _Cfunction('libvlc_media_list_remove_index', ((1,), (1,),), None,
                    ctypes.c_int, MediaList, ctypes.c_int)
    return f(p_ml, i_pos)

def libvlc_media_list_count(p_ml):
    '''Get count on media list items
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @return: number of items in media list.
    '''
    f = _Cfunctions.get('libvlc_media_list_count', None) or \
        _Cfunction('libvlc_media_list_count', ((1,),), None,
                    ctypes.c_int, MediaList)
    return f(p_ml)

def libvlc_media_list_item_at_index(p_ml, i_pos):
    '''List media instance in media list at a position
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @param i_pos: position in array where to insert.
    @return: media instance at position i_pos, or None if not found. In case of success, L{libvlc_media_retain}() is called to increase the refcount on the media.
    '''
    f = _Cfunctions.get('libvlc_media_list_item_at_index', None) or \
        _Cfunction('libvlc_media_list_item_at_index', ((1,), (1,),), class_result(Media),
                    ctypes.c_void_p, MediaList, ctypes.c_int)
    return f(p_ml, i_pos)

def libvlc_media_list_index_of_item(p_ml, p_md):
    '''Find index position of List media instance in media list.
    Warning: the function will return the first matched position.
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    @param p_md: media instance.
    @return: position of media instance or -1 if media not found.
    '''
    f = _Cfunctions.get('libvlc_media_list_index_of_item', None) or \
        _Cfunction('libvlc_media_list_index_of_item', ((1,), (1,),), None,
                    ctypes.c_int, MediaList, Media)
    return f(p_ml, p_md)

def libvlc_media_list_is_readonly(p_ml):
    '''This indicates if this media list is read-only from a user point of view.
    @param p_ml: media list instance.
    @return: 1 on readonly, 0 on readwrite \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_list_is_readonly', None) or \
        _Cfunction('libvlc_media_list_is_readonly', ((1,),), None,
                    ctypes.c_int, MediaList)
    return f(p_ml)

def libvlc_media_list_lock(p_ml):
    '''Get lock on media list items.
    @param p_ml: a media list instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_lock', None) or \
        _Cfunction('libvlc_media_list_lock', ((1,),), None,
                    None, MediaList)
    return f(p_ml)

def libvlc_media_list_unlock(p_ml):
    '''Release lock on media list items
    The L{libvlc_media_list_lock} should be held upon entering this function.
    @param p_ml: a media list instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_unlock', None) or \
        _Cfunction('libvlc_media_list_unlock', ((1,),), None,
                    None, MediaList)
    return f(p_ml)

def libvlc_media_list_event_manager(p_ml):
    '''Get libvlc_event_manager from this media list instance.
    The p_event_manager is immutable, so you don't have to hold the lock.
    @param p_ml: a media list instance.
    @return: libvlc_event_manager.
    '''
    f = _Cfunctions.get('libvlc_media_list_event_manager', None) or \
        _Cfunction('libvlc_media_list_event_manager', ((1,),), class_result(EventManager),
                    ctypes.c_void_p, MediaList)
    return f(p_ml)

def libvlc_media_list_player_new(p_instance):
    '''Create new media_list_player.
    @param p_instance: libvlc instance.
    @return: media list player instance or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_new', None) or \
        _Cfunction('libvlc_media_list_player_new', ((1,),), class_result(MediaListPlayer),
                    ctypes.c_void_p, Instance)
    return f(p_instance)

def libvlc_media_list_player_release(p_mlp):
    '''Release a media_list_player after use
    Decrement the reference count of a media player object. If the
    reference count is 0, then L{libvlc_media_list_player_release}() will
    release the media player object. If the media player object
    has been released, then it should not be used again.
    @param p_mlp: media list player instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_release', None) or \
        _Cfunction('libvlc_media_list_player_release', ((1,),), None,
                    None, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_retain(p_mlp):
    '''Retain a reference to a media player list object. Use
    L{libvlc_media_list_player_release}() to decrement reference count.
    @param p_mlp: media player list object.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_retain', None) or \
        _Cfunction('libvlc_media_list_player_retain', ((1,),), None,
                    None, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_event_manager(p_mlp):
    '''Return the event manager of this media_list_player.
    @param p_mlp: media list player instance.
    @return: the event manager.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_event_manager', None) or \
        _Cfunction('libvlc_media_list_player_event_manager', ((1,),), class_result(EventManager),
                    ctypes.c_void_p, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_set_media_player(p_mlp, p_mi):
    '''Replace media player in media_list_player with this instance.
    @param p_mlp: media list player instance.
    @param p_mi: media player instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_set_media_player', None) or \
        _Cfunction('libvlc_media_list_player_set_media_player', ((1,), (1,),), None,
                    None, MediaListPlayer, MediaPlayer)
    return f(p_mlp, p_mi)

def libvlc_media_list_player_get_media_player(p_mlp):
    '''Get media player of the media_list_player instance.
    @param p_mlp: media list player instance.
    @return: media player instance @note the caller is responsible for releasing the returned instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_get_media_player', None) or \
        _Cfunction('libvlc_media_list_player_get_media_player', ((1,),), class_result(MediaPlayer),
                    ctypes.c_void_p, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_set_media_list(p_mlp, p_mlist):
    '''Set the media list associated with the player.
    @param p_mlp: media list player instance.
    @param p_mlist: list of media.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_set_media_list', None) or \
        _Cfunction('libvlc_media_list_player_set_media_list', ((1,), (1,),), None,
                    None, MediaListPlayer, MediaList)
    return f(p_mlp, p_mlist)

def libvlc_media_list_player_play(p_mlp):
    '''Play media list.
    @param p_mlp: media list player instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_play', None) or \
        _Cfunction('libvlc_media_list_player_play', ((1,),), None,
                    None, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_pause(p_mlp):
    '''Toggle pause (or resume) media list.
    @param p_mlp: media list player instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_pause', None) or \
        _Cfunction('libvlc_media_list_player_pause', ((1,),), None,
                    None, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_is_playing(p_mlp):
    '''Is media list playing?
    @param p_mlp: media list player instance.
    @return: true for playing and false for not playing \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_is_playing', None) or \
        _Cfunction('libvlc_media_list_player_is_playing', ((1,),), None,
                    ctypes.c_int, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_get_state(p_mlp):
    '''Get current libvlc_state of media list player.
    @param p_mlp: media list player instance.
    @return: libvlc_state_t for media list player.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_get_state', None) or \
        _Cfunction('libvlc_media_list_player_get_state', ((1,),), None,
                    State, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_play_item_at_index(p_mlp, i_index):
    '''Play media list item at position index.
    @param p_mlp: media list player instance.
    @param i_index: index in media list to play.
    @return: 0 upon success -1 if the item wasn't found.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_play_item_at_index', None) or \
        _Cfunction('libvlc_media_list_player_play_item_at_index', ((1,), (1,),), None,
                    ctypes.c_int, MediaListPlayer, ctypes.c_int)
    return f(p_mlp, i_index)

def libvlc_media_list_player_play_item(p_mlp, p_md):
    '''Play the given media item.
    @param p_mlp: media list player instance.
    @param p_md: the media instance.
    @return: 0 upon success, -1 if the media is not part of the media list.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_play_item', None) or \
        _Cfunction('libvlc_media_list_player_play_item', ((1,), (1,),), None,
                    ctypes.c_int, MediaListPlayer, Media)
    return f(p_mlp, p_md)

def libvlc_media_list_player_stop(p_mlp):
    '''Stop playing media list.
    @param p_mlp: media list player instance.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_stop', None) or \
        _Cfunction('libvlc_media_list_player_stop', ((1,),), None,
                    None, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_next(p_mlp):
    '''Play next item from media list.
    @param p_mlp: media list player instance.
    @return: 0 upon success -1 if there is no next item.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_next', None) or \
        _Cfunction('libvlc_media_list_player_next', ((1,),), None,
                    ctypes.c_int, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_previous(p_mlp):
    '''Play previous item from media list.
    @param p_mlp: media list player instance.
    @return: 0 upon success -1 if there is no previous item.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_previous', None) or \
        _Cfunction('libvlc_media_list_player_previous', ((1,),), None,
                    ctypes.c_int, MediaListPlayer)
    return f(p_mlp)

def libvlc_media_list_player_set_playback_mode(p_mlp, e_mode):
    '''Sets the playback mode for the playlist.
    @param p_mlp: media list player instance.
    @param e_mode: playback mode specification.
    '''
    f = _Cfunctions.get('libvlc_media_list_player_set_playback_mode', None) or \
        _Cfunction('libvlc_media_list_player_set_playback_mode', ((1,), (1,),), None,
                    None, MediaListPlayer, PlaybackMode)
    return f(p_mlp, e_mode)

def libvlc_media_player_new(p_libvlc_instance):
    '''Create an empty Media Player object.
    @param p_libvlc_instance: the libvlc instance in which the Media Player should be created.
    @return: a new media player object, or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_player_new', None) or \
        _Cfunction('libvlc_media_player_new', ((1,),), class_result(MediaPlayer),
                    ctypes.c_void_p, Instance)
    return f(p_libvlc_instance)

def libvlc_media_player_new_from_media(p_md):
    '''Create a Media Player object from a Media.
    @param p_md: the media. Afterwards the p_md can be safely destroyed.
    @return: a new media player object, or None on error.
    '''
    f = _Cfunctions.get('libvlc_media_player_new_from_media', None) or \
        _Cfunction('libvlc_media_player_new_from_media', ((1,),), class_result(MediaPlayer),
                    ctypes.c_void_p, Media)
    return f(p_md)

def libvlc_media_player_release(p_mi):
    '''Release a media_player after use
    Decrement the reference count of a media player object. If the
    reference count is 0, then L{libvlc_media_player_release}() will
    release the media player object. If the media player object
    has been released, then it should not be used again.
    @param p_mi: the Media Player to free.
    '''
    f = _Cfunctions.get('libvlc_media_player_release', None) or \
        _Cfunction('libvlc_media_player_release', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_retain(p_mi):
    '''Retain a reference to a media player object. Use
    L{libvlc_media_player_release}() to decrement reference count.
    @param p_mi: media player object.
    '''
    f = _Cfunctions.get('libvlc_media_player_retain', None) or \
        _Cfunction('libvlc_media_player_retain', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_media(p_mi, p_md):
    '''Set the media that will be used by the media_player. If any,
    previous md will be released.
    @param p_mi: the Media Player.
    @param p_md: the Media. Afterwards the p_md can be safely destroyed.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_media', None) or \
        _Cfunction('libvlc_media_player_set_media', ((1,), (1,),), None,
                    None, MediaPlayer, Media)
    return f(p_mi, p_md)

def libvlc_media_player_get_media(p_mi):
    '''Get the media used by the media_player.
    @param p_mi: the Media Player.
    @return: the media associated with p_mi, or None if no media is associated.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_media', None) or \
        _Cfunction('libvlc_media_player_get_media', ((1,),), class_result(Media),
                    ctypes.c_void_p, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_event_manager(p_mi):
    '''Get the Event Manager from which the media player send event.
    @param p_mi: the Media Player.
    @return: the event manager associated with p_mi.
    '''
    f = _Cfunctions.get('libvlc_media_player_event_manager', None) or \
        _Cfunction('libvlc_media_player_event_manager', ((1,),), class_result(EventManager),
                    ctypes.c_void_p, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_is_playing(p_mi):
    '''is_playing.
    @param p_mi: the Media Player.
    @return: 1 if the media player is playing, 0 otherwise \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_player_is_playing', None) or \
        _Cfunction('libvlc_media_player_is_playing', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_play(p_mi):
    '''Play.
    @param p_mi: the Media Player.
    @return: 0 if playback started (and was already started), or -1 on error.
    '''
    f = _Cfunctions.get('libvlc_media_player_play', None) or \
        _Cfunction('libvlc_media_player_play', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_pause(mp, do_pause):
    '''Pause or resume (no effect if there is no media).
    @param mp: the Media Player.
    @param do_pause: play/resume if zero, pause if non-zero.
    @version: LibVLC 1.1.1 or later.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_pause', None) or \
        _Cfunction('libvlc_media_player_set_pause', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_int)
    return f(mp, do_pause)

def libvlc_media_player_pause(p_mi):
    '''Toggle pause (no effect if there is no media).
    @param p_mi: the Media Player.
    '''
    f = _Cfunctions.get('libvlc_media_player_pause', None) or \
        _Cfunction('libvlc_media_player_pause', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_stop(p_mi):
    '''Stop (no effect if there is no media).
    @param p_mi: the Media Player.
    '''
    f = _Cfunctions.get('libvlc_media_player_stop', None) or \
        _Cfunction('libvlc_media_player_stop', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_renderer(p_mi, p_item):
    '''Set a renderer to the media player
    @note: must be called before the first call of L{libvlc_media_player_play}() to
    take effect.
    See L{libvlc_renderer_discoverer_new}.
    @param p_mi: the Media Player.
    @param p_item: an item discovered by L{libvlc_renderer_discoverer_start}().
    @return: 0 on success, -1 on error.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_renderer', None) or \
        _Cfunction('libvlc_media_player_set_renderer', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_void_p)
    return f(p_mi, p_item)

def libvlc_video_set_callbacks(mp, lock, unlock, display, opaque):
    '''Set callbacks and private data to render decoded video to a custom area
    in memory.
    Use L{libvlc_video_set_format}() or L{libvlc_video_set_format_callbacks}()
    to configure the decoded format.
    @warning: Rendering video into custom memory buffers is considerably less
    efficient than rendering in a custom window as normal.
    For optimal perfomances, VLC media player renders into a custom window, and
    does not use this function and associated callbacks. It is B{highly
    recommended} that other LibVLC-based application do likewise.
    To embed video in a window, use libvlc_media_player_set_xid() or equivalent
    depending on the operating system.
    If window embedding does not fit the application use case, then a custom
    LibVLC video output display plugin is required to maintain optimal video
    rendering performances.
    The following limitations affect performance:
    - Hardware video decoding acceleration will either be disabled completely,
      or require (relatively slow) copy from video/DSP memory to main memory.
    - Sub-pictures (subtitles, on-screen display, etc.) must be blent into the
      main picture by the CPU instead of the GPU.
    - Depending on the video format, pixel format conversion, picture scaling,
      cropping and/or picture re-orientation, must be performed by the CPU
      instead of the GPU.
    - Memory copying is required between LibVLC reference picture buffers and
      application buffers (between lock and unlock callbacks).
    @param mp: the media player.
    @param lock: callback to lock video memory (must not be None).
    @param unlock: callback to unlock video memory (or None if not needed).
    @param display: callback to display video (or None if not needed).
    @param opaque: private pointer for the three callbacks (as first parameter).
    @version: LibVLC 1.1.1 or later.
    '''
    f = _Cfunctions.get('libvlc_video_set_callbacks', None) or \
        _Cfunction('libvlc_video_set_callbacks', ((1,), (1,), (1,), (1,), (1,),), None,
                    None, MediaPlayer, VideoLockCb, VideoUnlockCb, VideoDisplayCb, ctypes.c_void_p)
    return f(mp, lock, unlock, display, opaque)

def libvlc_video_set_format(mp, chroma, width, height, pitch):
    '''Set decoded video chroma and dimensions.
    This only works in combination with L{libvlc_video_set_callbacks}(),
    and is mutually exclusive with L{libvlc_video_set_format_callbacks}().
    @param mp: the media player.
    @param chroma: a four-characters string identifying the chroma (e.g. "RV32" or "YUYV").
    @param width: pixel width.
    @param height: pixel height.
    @param pitch: line pitch (in bytes).
    @version: LibVLC 1.1.1 or later.
    @bug: All pixel planes are expected to have the same pitch. To use the YCbCr color space with chrominance subsampling, consider using L{libvlc_video_set_format_callbacks}() instead.
    '''
    f = _Cfunctions.get('libvlc_video_set_format', None) or \
        _Cfunction('libvlc_video_set_format', ((1,), (1,), (1,), (1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint)
    return f(mp, chroma, width, height, pitch)

def libvlc_video_set_format_callbacks(mp, setup, cleanup):
    '''Set decoded video chroma and dimensions. This only works in combination with
    L{libvlc_video_set_callbacks}().
    @param mp: the media player.
    @param setup: callback to select the video format (cannot be None).
    @param cleanup: callback to release any allocated resources (or None).
    @version: LibVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_video_set_format_callbacks', None) or \
        _Cfunction('libvlc_video_set_format_callbacks', ((1,), (1,), (1,),), None,
                    None, MediaPlayer, VideoFormatCb, VideoCleanupCb)
    return f(mp, setup, cleanup)

def libvlc_media_player_set_nsobject(p_mi, drawable):
    '''Set the NSView handler where the media player should render its video output.
    Use the vout called "macosx".
    The drawable is an NSObject that follow the VLCOpenGLVideoViewEmbedding
    protocol:
    @code.m
    \@protocol VLCOpenGLVideoViewEmbedding <NSObject>
    - (void)addVoutSubview:(NSView *)view;
    - (void)removeVoutSubview:(NSView *)view;
    \@end
    @endcode
    Or it can be an NSView object.
    If you want to use it along with Qt see the QMacCocoaViewContainer. Then
    the following code should work:
    @code.mm

        NSView *video = [[NSView alloc] init];
        QMacCocoaViewContainer *container = new QMacCocoaViewContainer(video, parent);
        L{libvlc_media_player_set_nsobject}(mp, video);
        [video release];

    @endcode
    You can find a live example in VLCVideoView in VLCKit.framework.
    @param p_mi: the Media Player.
    @param drawable: the drawable that is either an NSView or an object following the VLCOpenGLVideoViewEmbedding protocol.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_nsobject', None) or \
        _Cfunction('libvlc_media_player_set_nsobject', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_void_p)
    return f(p_mi, drawable)

def libvlc_media_player_get_nsobject(p_mi):
    '''Get the NSView handler previously set with L{libvlc_media_player_set_nsobject}().
    @param p_mi: the Media Player.
    @return: the NSView handler or 0 if none where set.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_nsobject', None) or \
        _Cfunction('libvlc_media_player_get_nsobject', ((1,),), None,
                    ctypes.c_void_p, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_xwindow(p_mi, drawable):
    '''Set an X Window System drawable where the media player should render its
    video output. The call takes effect when the playback starts. If it is
    already started, it might need to be stopped before changes apply.
    If LibVLC was built without X11 output support, then this function has no
    effects.
    By default, LibVLC will capture input events on the video rendering area.
    Use L{libvlc_video_set_mouse_input}() and L{libvlc_video_set_key_input}() to
    disable that and deliver events to the parent window / to the application
    instead. By design, the X11 protocol delivers input events to only one
    recipient.
    @warning
    The application must call the XInitThreads() function from Xlib before
    L{libvlc_new}(), and before any call to XOpenDisplay() directly or via any
    other library. Failure to call XInitThreads() will seriously impede LibVLC
    performance. Calling XOpenDisplay() before XInitThreads() will eventually
    crash the process. That is a limitation of Xlib.
    @param p_mi: media player.
    @param drawable: X11 window ID @note The specified identifier must correspond to an existing Input/Output class X11 window. Pixmaps are B{not} currently supported. The default X11 server is assumed, i.e. that specified in the DISPLAY environment variable. @warning LibVLC can deal with invalid X11 handle errors, however some display drivers (EGL, GLX, VA and/or VDPAU) can unfortunately not. Thus the window handle must remain valid until playback is stopped, otherwise the process may abort or crash.
    @bug No more than one window handle per media player instance can be specified. If the media has multiple simultaneously active video tracks, extra tracks will be rendered into external windows beyond the control of the application.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_xwindow', None) or \
        _Cfunction('libvlc_media_player_set_xwindow', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_uint32)
    return f(p_mi, drawable)

def libvlc_media_player_get_xwindow(p_mi):
    '''Get the X Window System window identifier previously set with
    L{libvlc_media_player_set_xwindow}(). Note that this will return the identifier
    even if VLC is not currently using it (for instance if it is playing an
    audio-only input).
    @param p_mi: the Media Player.
    @return: an X window ID, or 0 if none where set.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_xwindow', None) or \
        _Cfunction('libvlc_media_player_get_xwindow', ((1,),), None,
                    ctypes.c_uint32, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_hwnd(p_mi, drawable):
    '''Set a Win32/Win64 API window handle (HWND) where the media player should
    render its video output. If LibVLC was built without Win32/Win64 API output
    support, then this has no effects.
    @param p_mi: the Media Player.
    @param drawable: windows handle of the drawable.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_hwnd', None) or \
        _Cfunction('libvlc_media_player_set_hwnd', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_void_p)
    return f(p_mi, drawable)

def libvlc_media_player_get_hwnd(p_mi):
    '''Get the Windows API window handle (HWND) previously set with
    L{libvlc_media_player_set_hwnd}(). The handle will be returned even if LibVLC
    is not currently outputting any video to it.
    @param p_mi: the Media Player.
    @return: a window handle or None if there are none.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_hwnd', None) or \
        _Cfunction('libvlc_media_player_get_hwnd', ((1,),), None,
                    ctypes.c_void_p, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_android_context(p_mi, p_awindow_handler):
    '''Set the android context.
    @param p_mi: the media player.
    @param p_awindow_handler: org.videolan.libvlc.IAWindowNativeHandler jobject implemented by the org.videolan.libvlc.MediaPlayer class from the libvlc-android project.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_android_context', None) or \
        _Cfunction('libvlc_media_player_set_android_context', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_void_p)
    return f(p_mi, p_awindow_handler)

def libvlc_media_player_set_evas_object(p_mi, p_evas_object):
    '''Set the EFL Evas Object.
    @param p_mi: the media player.
    @param p_evas_object: a valid EFL Evas Object (Evas_Object).
    @return: -1 if an error was detected, 0 otherwise.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_evas_object', None) or \
        _Cfunction('libvlc_media_player_set_evas_object', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_void_p)
    return f(p_mi, p_evas_object)

def libvlc_audio_set_callbacks(mp, play, pause, resume, flush, drain, opaque):
    '''Sets callbacks and private data for decoded audio.
    Use L{libvlc_audio_set_format}() or L{libvlc_audio_set_format_callbacks}()
    to configure the decoded audio format.
    @note: The audio callbacks override any other audio output mechanism.
    If the callbacks are set, LibVLC will B{not} output audio in any way.
    @param mp: the media player.
    @param play: callback to play audio samples (must not be None).
    @param pause: callback to pause playback (or None to ignore).
    @param resume: callback to resume playback (or None to ignore).
    @param flush: callback to flush audio buffers (or None to ignore).
    @param drain: callback to drain audio buffers (or None to ignore).
    @param opaque: private pointer for the audio callbacks (as first parameter).
    @version: LibVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_set_callbacks', None) or \
        _Cfunction('libvlc_audio_set_callbacks', ((1,), (1,), (1,), (1,), (1,), (1,), (1,),), None,
                    None, MediaPlayer, AudioPlayCb, AudioPauseCb, AudioResumeCb, AudioFlushCb, AudioDrainCb, ctypes.c_void_p)
    return f(mp, play, pause, resume, flush, drain, opaque)

def libvlc_audio_set_volume_callback(mp, set_volume):
    '''Set callbacks and private data for decoded audio. This only works in
    combination with L{libvlc_audio_set_callbacks}().
    Use L{libvlc_audio_set_format}() or L{libvlc_audio_set_format_callbacks}()
    to configure the decoded audio format.
    @param mp: the media player.
    @param set_volume: callback to apply audio volume, or None to apply volume in software.
    @version: LibVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_set_volume_callback', None) or \
        _Cfunction('libvlc_audio_set_volume_callback', ((1,), (1,),), None,
                    None, MediaPlayer, AudioSetVolumeCb)
    return f(mp, set_volume)

def libvlc_audio_set_format_callbacks(mp, setup, cleanup):
    '''Sets decoded audio format via callbacks.
    This only works in combination with L{libvlc_audio_set_callbacks}().
    @param mp: the media player.
    @param setup: callback to select the audio format (cannot be None).
    @param cleanup: callback to release any allocated resources (or None).
    @version: LibVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_set_format_callbacks', None) or \
        _Cfunction('libvlc_audio_set_format_callbacks', ((1,), (1,), (1,),), None,
                    None, MediaPlayer, AudioSetupCb, AudioCleanupCb)
    return f(mp, setup, cleanup)

def libvlc_audio_set_format(mp, format, rate, channels):
    '''Sets a fixed decoded audio format.
    This only works in combination with L{libvlc_audio_set_callbacks}(),
    and is mutually exclusive with L{libvlc_audio_set_format_callbacks}().
    @param mp: the media player.
    @param format: a four-characters string identifying the sample format (e.g. "S16N" or "FL32").
    @param rate: sample rate (expressed in Hz).
    @param channels: channels count.
    @version: LibVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_set_format', None) or \
        _Cfunction('libvlc_audio_set_format', ((1,), (1,), (1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint)
    return f(mp, format, rate, channels)

def libvlc_media_player_get_length(p_mi):
    '''Get the current movie length (in ms).
    @param p_mi: the Media Player.
    @return: the movie length (in ms), or -1 if there is no media.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_length', None) or \
        _Cfunction('libvlc_media_player_get_length', ((1,),), None,
                    ctypes.c_longlong, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_get_time(p_mi):
    '''Get the current movie time (in ms).
    @param p_mi: the Media Player.
    @return: the movie time (in ms), or -1 if there is no media.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_time', None) or \
        _Cfunction('libvlc_media_player_get_time', ((1,),), None,
                    ctypes.c_longlong, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_time(p_mi, i_time):
    '''Set the movie time (in ms). This has no effect if no media is being played.
    Not all formats and protocols support this.
    @param p_mi: the Media Player.
    @param i_time: the movie time (in ms).
    '''
    f = _Cfunctions.get('libvlc_media_player_set_time', None) or \
        _Cfunction('libvlc_media_player_set_time', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_longlong)
    return f(p_mi, i_time)

def libvlc_media_player_get_position(p_mi):
    '''Get movie position as percentage between 0.0 and 1.0.
    @param p_mi: the Media Player.
    @return: movie position, or -1. in case of error.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_position', None) or \
        _Cfunction('libvlc_media_player_get_position', ((1,),), None,
                    ctypes.c_float, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_position(p_mi, f_pos):
    '''Set movie position as percentage between 0.0 and 1.0.
    This has no effect if playback is not enabled.
    This might not work depending on the underlying input format and protocol.
    @param p_mi: the Media Player.
    @param f_pos: the position.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_position', None) or \
        _Cfunction('libvlc_media_player_set_position', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_float)
    return f(p_mi, f_pos)

def libvlc_media_player_set_chapter(p_mi, i_chapter):
    '''Set movie chapter (if applicable).
    @param p_mi: the Media Player.
    @param i_chapter: chapter number to play.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_chapter', None) or \
        _Cfunction('libvlc_media_player_set_chapter', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_int)
    return f(p_mi, i_chapter)

def libvlc_media_player_get_chapter(p_mi):
    '''Get movie chapter.
    @param p_mi: the Media Player.
    @return: chapter number currently playing, or -1 if there is no media.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_chapter', None) or \
        _Cfunction('libvlc_media_player_get_chapter', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_get_chapter_count(p_mi):
    '''Get movie chapter count.
    @param p_mi: the Media Player.
    @return: number of chapters in movie, or -1.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_chapter_count', None) or \
        _Cfunction('libvlc_media_player_get_chapter_count', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_will_play(p_mi):
    '''Is the player able to play.
    @param p_mi: the Media Player.
    @return: boolean \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_player_will_play', None) or \
        _Cfunction('libvlc_media_player_will_play', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_get_chapter_count_for_title(p_mi, i_title):
    '''Get title chapter count.
    @param p_mi: the Media Player.
    @param i_title: title.
    @return: number of chapters in title, or -1.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_chapter_count_for_title', None) or \
        _Cfunction('libvlc_media_player_get_chapter_count_for_title', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_int)
    return f(p_mi, i_title)

def libvlc_media_player_set_title(p_mi, i_title):
    '''Set movie title.
    @param p_mi: the Media Player.
    @param i_title: title number to play.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_title', None) or \
        _Cfunction('libvlc_media_player_set_title', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_int)
    return f(p_mi, i_title)

def libvlc_media_player_get_title(p_mi):
    '''Get movie title.
    @param p_mi: the Media Player.
    @return: title number currently playing, or -1.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_title', None) or \
        _Cfunction('libvlc_media_player_get_title', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_get_title_count(p_mi):
    '''Get movie title count.
    @param p_mi: the Media Player.
    @return: title number count, or -1.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_title_count', None) or \
        _Cfunction('libvlc_media_player_get_title_count', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_previous_chapter(p_mi):
    '''Set previous chapter (if applicable).
    @param p_mi: the Media Player.
    '''
    f = _Cfunctions.get('libvlc_media_player_previous_chapter', None) or \
        _Cfunction('libvlc_media_player_previous_chapter', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_next_chapter(p_mi):
    '''Set next chapter (if applicable).
    @param p_mi: the Media Player.
    '''
    f = _Cfunctions.get('libvlc_media_player_next_chapter', None) or \
        _Cfunction('libvlc_media_player_next_chapter', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_get_rate(p_mi):
    '''Get the requested movie play rate.
    @warning: Depending on the underlying media, the requested rate may be
    different from the real playback rate.
    @param p_mi: the Media Player.
    @return: movie play rate.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_rate', None) or \
        _Cfunction('libvlc_media_player_get_rate', ((1,),), None,
                    ctypes.c_float, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_rate(p_mi, rate):
    '''Set movie play rate.
    @param p_mi: the Media Player.
    @param rate: movie play rate to set.
    @return: -1 if an error was detected, 0 otherwise (but even then, it might not actually work depending on the underlying media protocol).
    '''
    f = _Cfunctions.get('libvlc_media_player_set_rate', None) or \
        _Cfunction('libvlc_media_player_set_rate', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_float)
    return f(p_mi, rate)

def libvlc_media_player_get_state(p_mi):
    '''Get current movie state.
    @param p_mi: the Media Player.
    @return: the current state of the media player (playing, paused, ...) See libvlc_state_t.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_state', None) or \
        _Cfunction('libvlc_media_player_get_state', ((1,),), None,
                    State, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_has_vout(p_mi):
    '''How many video outputs does this media player have?
    @param p_mi: the media player.
    @return: the number of video outputs.
    '''
    f = _Cfunctions.get('libvlc_media_player_has_vout', None) or \
        _Cfunction('libvlc_media_player_has_vout', ((1,),), None,
                    ctypes.c_uint, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_is_seekable(p_mi):
    '''Is this media player seekable?
    @param p_mi: the media player.
    @return: true if the media player can seek \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_player_is_seekable', None) or \
        _Cfunction('libvlc_media_player_is_seekable', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_can_pause(p_mi):
    '''Can this media player be paused?
    @param p_mi: the media player.
    @return: true if the media player can pause \libvlc_return_bool.
    '''
    f = _Cfunctions.get('libvlc_media_player_can_pause', None) or \
        _Cfunction('libvlc_media_player_can_pause', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_program_scrambled(p_mi):
    '''Check if the current program is scrambled.
    @param p_mi: the media player.
    @return: true if the current program is scrambled \libvlc_return_bool.
    @version: LibVLC 2.2.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_player_program_scrambled', None) or \
        _Cfunction('libvlc_media_player_program_scrambled', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_next_frame(p_mi):
    '''Display the next frame (if supported).
    @param p_mi: the media player.
    '''
    f = _Cfunctions.get('libvlc_media_player_next_frame', None) or \
        _Cfunction('libvlc_media_player_next_frame', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_navigate(p_mi, navigate):
    '''Navigate through DVD Menu.
    @param p_mi: the Media Player.
    @param navigate: the Navigation mode.
    @version: libVLC 2.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_player_navigate', None) or \
        _Cfunction('libvlc_media_player_navigate', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_uint)
    return f(p_mi, navigate)

def libvlc_media_player_set_video_title_display(p_mi, position, timeout):
    '''Set if, and how, the video title will be shown when media is played.
    @param p_mi: the media player.
    @param position: position at which to display the title, or libvlc_position_disable to prevent the title from being displayed.
    @param timeout: title display timeout in milliseconds (ignored if libvlc_position_disable).
    @version: libVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_video_title_display', None) or \
        _Cfunction('libvlc_media_player_set_video_title_display', ((1,), (1,), (1,),), None,
                    None, MediaPlayer, Position, ctypes.c_int)
    return f(p_mi, position, timeout)

def libvlc_media_player_add_slave(p_mi, i_type, psz_uri, b_select):
    '''Add a slave to the current media player.
    @note: If the player is playing, the slave will be added directly. This call
    will also update the slave list of the attached L{Media}.
    @param p_mi: the media player.
    @param i_type: subtitle or audio.
    @param psz_uri: Uri of the slave (should contain a valid scheme).
    @param b_select: True if this slave should be selected when it's loaded.
    @return: 0 on success, -1 on error.
    @version: LibVLC 3.0.0 and later. See L{libvlc_media_slaves_add}.
    '''
    f = _Cfunctions.get('libvlc_media_player_add_slave', None) or \
        _Cfunction('libvlc_media_player_add_slave', ((1,), (1,), (1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, MediaSlaveType, ctypes.c_char_p, ctypes.c_bool)
    return f(p_mi, i_type, psz_uri, b_select)

def libvlc_track_description_list_release(p_track_description):
    '''Release (free) L{TrackDescription}.
    @param p_track_description: the structure to release.
    '''
    f = _Cfunctions.get('libvlc_track_description_list_release', None) or \
        _Cfunction('libvlc_track_description_list_release', ((1,),), None,
                    None, ctypes.POINTER(TrackDescription))
    return f(p_track_description)

def libvlc_audio_output_list_get(p_instance):
    '''Gets the list of available audio output modules.
    @param p_instance: libvlc instance.
    @return: list of available audio outputs. It must be freed with In case of error, None is returned.
    '''
    f = _Cfunctions.get('libvlc_audio_output_list_get', None) or \
        _Cfunction('libvlc_audio_output_list_get', ((1,),), None,
                    ctypes.POINTER(AudioOutput), Instance)
    return f(p_instance)

def libvlc_audio_output_list_release(p_list):
    '''Frees the list of available audio output modules.
    @param p_list: list with audio outputs for release.
    '''
    f = _Cfunctions.get('libvlc_audio_output_list_release', None) or \
        _Cfunction('libvlc_audio_output_list_release', ((1,),), None,
                    None, ctypes.POINTER(AudioOutput))
    return f(p_list)

def libvlc_audio_output_set(p_mi, psz_name):
    '''Selects an audio output module.
    @note: Any change will take be effect only after playback is stopped and
    restarted. Audio output cannot be changed while playing.
    @param p_mi: media player.
    @param psz_name: name of audio output, use psz_name of See L{AudioOutput}.
    @return: 0 if function succeeded, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_audio_output_set', None) or \
        _Cfunction('libvlc_audio_output_set', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_char_p)
    return f(p_mi, psz_name)

def libvlc_audio_output_device_enum(mp):
    '''Gets a list of potential audio output devices,
    See L{libvlc_audio_output_device_set}().
    @note: Not all audio outputs support enumerating devices.
    The audio output may be functional even if the list is empty (None).
    @note: The list may not be exhaustive.
    @warning: Some audio output devices in the list might not actually work in
    some circumstances. By default, it is recommended to not specify any
    explicit audio device.
    @param mp: media player.
    @return: A None-terminated linked list of potential audio output devices. It must be freed with L{libvlc_audio_output_device_list_release}().
    @version: LibVLC 2.2.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_output_device_enum', None) or \
        _Cfunction('libvlc_audio_output_device_enum', ((1,),), None,
                    ctypes.POINTER(AudioOutputDevice), MediaPlayer)
    return f(mp)

def libvlc_audio_output_device_list_get(p_instance, aout):
    '''Gets a list of audio output devices for a given audio output module,
    See L{libvlc_audio_output_device_set}().
    @note: Not all audio outputs support this. In particular, an empty (None)
    list of devices does B{not} imply that the specified audio output does
    not work.
    @note: The list might not be exhaustive.
    @warning: Some audio output devices in the list might not actually work in
    some circumstances. By default, it is recommended to not specify any
    explicit audio device.
    @param p_instance: libvlc instance.
    @param aout: audio output name (as returned by L{libvlc_audio_output_list_get}()).
    @return: A None-terminated linked list of potential audio output devices. It must be freed with L{libvlc_audio_output_device_list_release}().
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_output_device_list_get', None) or \
        _Cfunction('libvlc_audio_output_device_list_get', ((1,), (1,),), None,
                    ctypes.POINTER(AudioOutputDevice), Instance, ctypes.c_char_p)
    return f(p_instance, aout)

def libvlc_audio_output_device_list_release(p_list):
    '''Frees a list of available audio output devices.
    @param p_list: list with audio outputs for release.
    @version: LibVLC 2.1.0 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_output_device_list_release', None) or \
        _Cfunction('libvlc_audio_output_device_list_release', ((1,),), None,
                    None, ctypes.POINTER(AudioOutputDevice))
    return f(p_list)

def libvlc_audio_output_device_set(mp, module, device_id):

    f = _Cfunctions.get('libvlc_audio_output_device_set', None) or \
        _Cfunction('libvlc_audio_output_device_set', ((1,), (1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_char_p, ctypes.c_char_p)
    return f(mp, module, device_id)

def libvlc_audio_output_device_get(mp):

    f = _Cfunctions.get('libvlc_audio_output_device_get', None) or \
        _Cfunction('libvlc_audio_output_device_get', ((1,),), None,
                    ctypes.c_char_p, MediaPlayer)
    return f(mp)

def libvlc_audio_toggle_mute(p_mi):
    '''Toggle mute status.
    @param p_mi: media player @warning Toggling mute atomically is not always possible: On some platforms, other processes can mute the VLC audio playback stream asynchronously. Thus, there is a small race condition where toggling will not work. See also the limitations of L{libvlc_audio_set_mute}().
    '''
    f = _Cfunctions.get('libvlc_audio_toggle_mute', None) or \
        _Cfunction('libvlc_audio_toggle_mute', ((1,),), None,
                    None, MediaPlayer)
    return f(p_mi)

def libvlc_audio_get_mute(p_mi):
    '''Get current mute status.
    @param p_mi: media player.
    @return: the mute status (boolean) if defined, -1 if undefined/unapplicable.
    '''
    f = _Cfunctions.get('libvlc_audio_get_mute', None) or \
        _Cfunction('libvlc_audio_get_mute', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_audio_set_mute(p_mi, status):
    '''Set mute status.
    @param p_mi: media player.
    @param status: If status is true then mute, otherwise unmute @warning This function does not always work. If there are no active audio playback stream, the mute status might not be available. If digital pass-through (S/PDIF, HDMI...) is in use, muting may be unapplicable. Also some audio output plugins do not support muting at all. @note To force silent playback, disable all audio tracks. This is more efficient and reliable than mute.
    '''
    f = _Cfunctions.get('libvlc_audio_set_mute', None) or \
        _Cfunction('libvlc_audio_set_mute', ((1,), (1,),), None,
                    None, MediaPlayer, ctypes.c_int)
    return f(p_mi, status)

def libvlc_audio_get_volume(p_mi):
    '''Get current software audio volume.
    @param p_mi: media player.
    @return: the software volume in percents (0 = mute, 100 = nominal / 0dB).
    '''
    f = _Cfunctions.get('libvlc_audio_get_volume', None) or \
        _Cfunction('libvlc_audio_get_volume', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_audio_set_volume(p_mi, i_volume):
    '''Set current software audio volume.
    @param p_mi: media player.
    @param i_volume: the volume in percents (0 = mute, 100 = 0dB).
    @return: 0 if the volume was set, -1 if it was out of range.
    '''
    f = _Cfunctions.get('libvlc_audio_set_volume', None) or \
        _Cfunction('libvlc_audio_set_volume', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_int)
    return f(p_mi, i_volume)

def libvlc_audio_get_track_count(p_mi):
    '''Get number of available audio tracks.
    @param p_mi: media player.
    @return: the number of available audio tracks (int), or -1 if unavailable.
    '''
    f = _Cfunctions.get('libvlc_audio_get_track_count', None) or \
        _Cfunction('libvlc_audio_get_track_count', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_audio_get_track_description(p_mi):
    '''Get the description of available audio tracks.
    @param p_mi: media player.
    @return: list with description of available audio tracks, or None. It must be freed with L{libvlc_track_description_list_release}().
    '''
    f = _Cfunctions.get('libvlc_audio_get_track_description', None) or \
        _Cfunction('libvlc_audio_get_track_description', ((1,),), None,
                    ctypes.POINTER(TrackDescription), MediaPlayer)
    return f(p_mi)

def libvlc_audio_get_track(p_mi):
    '''Get current audio track.
    @param p_mi: media player.
    @return: the audio track ID or -1 if no active input.
    '''
    f = _Cfunctions.get('libvlc_audio_get_track', None) or \
        _Cfunction('libvlc_audio_get_track', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_audio_set_track(p_mi, i_track):
    '''Set current audio track.
    @param p_mi: media player.
    @param i_track: the track ID (i_id field from track description).
    @return: 0 on success, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_audio_set_track', None) or \
        _Cfunction('libvlc_audio_set_track', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_int)
    return f(p_mi, i_track)

def libvlc_audio_get_channel(p_mi):
    '''Get current audio channel.
    @param p_mi: media player.
    @return: the audio channel See libvlc_audio_output_channel_t.
    '''
    f = _Cfunctions.get('libvlc_audio_get_channel', None) or \
        _Cfunction('libvlc_audio_get_channel', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_audio_set_channel(p_mi, channel):
    '''Set current audio channel.
    @param p_mi: media player.
    @param channel: the audio channel, See libvlc_audio_output_channel_t.
    @return: 0 on success, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_audio_set_channel', None) or \
        _Cfunction('libvlc_audio_set_channel', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_int)
    return f(p_mi, channel)

def libvlc_audio_get_delay(p_mi):
    '''Get current audio delay.
    @param p_mi: media player.
    @return: the audio delay (microseconds).
    @version: LibVLC 1.1.1 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_get_delay', None) or \
        _Cfunction('libvlc_audio_get_delay', ((1,),), None,
                    ctypes.c_int64, MediaPlayer)
    return f(p_mi)

def libvlc_audio_set_delay(p_mi, i_delay):
    '''Set current audio delay. The audio delay will be reset to zero each time the media changes.
    @param p_mi: media player.
    @param i_delay: the audio delay (microseconds).
    @return: 0 on success, -1 on error.
    @version: LibVLC 1.1.1 or later.
    '''
    f = _Cfunctions.get('libvlc_audio_set_delay', None) or \
        _Cfunction('libvlc_audio_set_delay', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_int64)
    return f(p_mi, i_delay)

def libvlc_media_player_get_role(p_mi):
    '''Gets the media role.
    @param p_mi: media player.
    @return: the media player role (\ref libvlc_media_player_role_t).
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_media_player_get_role', None) or \
        _Cfunction('libvlc_media_player_get_role', ((1,),), None,
                    ctypes.c_int, MediaPlayer)
    return f(p_mi)

def libvlc_media_player_set_role(p_mi, role):
    '''Sets the media role.
    @param p_mi: media player.
    @param role: the media player role (\ref libvlc_media_player_role_t).
    @return: 0 on success, -1 on error.
    '''
    f = _Cfunctions.get('libvlc_media_player_set_role', None) or \
        _Cfunction('libvlc_media_player_set_role', ((1,), (1,),), None,
                    ctypes.c_int, MediaPlayer, ctypes.c_uint)
    return f(p_mi, role)

def libvlc_renderer_item_name(p_item):
    '''Get the human readable name of a renderer item.
    @return: the name of the item (can't be None, must *not* be freed).
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_item_name', None) or \
        _Cfunction('libvlc_renderer_item_name', ((1,),), None,
                    ctypes.c_char_p, ctypes.c_void_p)
    return f(p_item)

def libvlc_renderer_item_type(p_item):
    '''Get the type (not translated) of a renderer item. For now, the type can only
    be "chromecast" ("upnp", "airplay" may come later).
    @return: the type of the item (can't be None, must *not* be freed).
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_item_type', None) or \
        _Cfunction('libvlc_renderer_item_type', ((1,),), None,
                    ctypes.c_char_p, ctypes.c_void_p)
    return f(p_item)

def libvlc_renderer_item_icon_uri(p_item):
    '''Get the icon uri of a renderer item.
    @return: the uri of the item's icon (can be None, must *not* be freed).
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_item_icon_uri', None) or \
        _Cfunction('libvlc_renderer_item_icon_uri', ((1,),), None,
                    ctypes.c_char_p, ctypes.c_void_p)
    return f(p_item)

def libvlc_renderer_item_flags(p_item):
    '''Get the flags of a renderer item
    See LIBVLC_RENDERER_CAN_AUDIO
    See LIBVLC_RENDERER_CAN_VIDEO.
    @return: bitwise flag: capabilities of the renderer, see.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_item_flags', None) or \
        _Cfunction('libvlc_renderer_item_flags', ((1,),), None,
                    ctypes.c_int, ctypes.c_void_p)
    return f(p_item)

def libvlc_renderer_discoverer_new(p_inst, psz_name):
    '''Create a renderer discoverer object by name
    After this object is created, you should attach to events in order to be
    notified of the discoverer events.
    You need to call L{libvlc_renderer_discoverer_start}() in order to start the
    discovery.
    See L{libvlc_renderer_discoverer_event_manager}()
    See L{libvlc_renderer_discoverer_start}().
    @param p_inst: libvlc instance.
    @param psz_name: service name; use L{libvlc_renderer_discoverer_list_get}() to get a list of the discoverer names available in this libVLC instance.
    @return: media discover object or None in case of error.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_new', None) or \
        _Cfunction('libvlc_renderer_discoverer_new', ((1,), (1,),), None,
                    ctypes.c_void_p, Instance, ctypes.c_char_p)
    return f(p_inst, psz_name)

def libvlc_renderer_discoverer_release(p_rd):
    '''Release a renderer discoverer object.
    @param p_rd: renderer discoverer object.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_release', None) or \
        _Cfunction('libvlc_renderer_discoverer_release', ((1,),), None,
                    None, ctypes.c_void_p)
    return f(p_rd)

def libvlc_renderer_discoverer_start(p_rd):
    '''Start renderer discovery
    To stop it, call L{libvlc_renderer_discoverer_stop}() or
    L{libvlc_renderer_discoverer_release}() directly.
    See L{libvlc_renderer_discoverer_stop}().
    @param p_rd: renderer discoverer object.
    @return: -1 in case of error, 0 otherwise.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_start', None) or \
        _Cfunction('libvlc_renderer_discoverer_start', ((1,),), None,
                    ctypes.c_int, ctypes.c_void_p)
    return f(p_rd)

def libvlc_renderer_discoverer_stop(p_rd):
    '''Stop renderer discovery.
    See L{libvlc_renderer_discoverer_start}().
    @param p_rd: renderer discoverer object.
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_stop', None) or \
        _Cfunction('libvlc_renderer_discoverer_stop', ((1,),), None,
                    None, ctypes.c_void_p)
    return f(p_rd)

def libvlc_renderer_discoverer_event_manager(p_rd):
    '''Get the event manager of the renderer discoverer
    The possible events to attach are @ref libvlc_RendererDiscovererItemAdded
    and @ref libvlc_RendererDiscovererItemDeleted.
    The @ref libvlc_renderer_item_t struct passed to event callbacks is owned by
    VLC, users should take care of copying this struct for their internal usage.
    See libvlc_event_t.u.renderer_discoverer_item_added.item
    See libvlc_event_t.u.renderer_discoverer_item_removed.item.
    @return: a valid event manager (can't fail).
    @version: LibVLC 3.0.0 or later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_event_manager', None) or \
        _Cfunction('libvlc_renderer_discoverer_event_manager', ((1,),), class_result(EventManager),
                    ctypes.c_void_p, ctypes.c_void_p)
    return f(p_rd)

def libvlc_renderer_discoverer_list_get(p_inst, ppp_services):
    '''Get media discoverer services
    See libvlc_renderer_list_release().
    @param p_inst: libvlc instance.
    @param ppp_services: address to store an allocated array of renderer discoverer services (must be freed with libvlc_renderer_list_release() by the caller) [OUT].
    @return: the number of media discoverer services (0 on error).
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_list_get', None) or \
        _Cfunction('libvlc_renderer_discoverer_list_get', ((1,), (1,),), None,
                    ctypes.c_size_t, Instance, ctypes.POINTER(ctypes.POINTER(RDDescription)))
    return f(p_inst, ppp_services)

def libvlc_renderer_discoverer_list_release(pp_services, i_count):
    '''Release an array of media discoverer services
    See L{libvlc_renderer_discoverer_list_get}().
    @param pp_services: array to release.
    @param i_count: number of elements in the array.
    @version: LibVLC 3.0.0 and later.
    '''
    f = _Cfunctions.get('libvlc_renderer_discoverer_list_release', None) or \
        _Cfunction('libvlc_renderer_discoverer_list_release', ((1,), (1,),), None,
                    None, ctypes.POINTER(RDDescription), ctypes.c_size_t)
    return f(pp_services, i_count)
