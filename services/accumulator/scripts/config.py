hikvision_url_default = {
    'auth': ('admin', 'admin123'),
    'device_url': 'http://172.22.61.80'}

urls = {
    'brightness':   '/Image/channels/1/Color',
    'framerate':    '/Streaming/channels/1',
    'quality':      '/Streaming/channels/1',
    'height':       '/Streaming/channels/1',
    'width':        '/Streaming/channels/1',
    'exposure':     '/Image/channels/1/shutter',
    'irlight':      '/Image/channels/1/IrcutFilter'
}


place = {
    'brightness':   ['Color', 'brightnessLevel'],
    'framerate':    ['StreamingChannel', 'Video', 'maxFrameRate'],
    'quality':      ['StreamingChannel', 'Video', 'fixedQuality'],
    'height':       ['StreamingChannel', 'Video', 'videoResolutionHeight'],
    'width':        ['StreamingChannel', 'Video', 'videoResolutionWidth'],
    'exposure':     ['Shutter', "ShutterLevel"],
    'irlight':      ['IrcutFilter', 'IrcutFilterType']
}