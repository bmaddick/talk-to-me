def check(cmd, mf):
    m = mf.findNode('pyaudio')
    if m is None:
        return None

    # Tell py2app about the PortAudio dependency
    return dict(
        prescripts=['recipes/pyaudio_prescript.py'],
        resources=[],
        frameworks=['libportaudio.2.dylib']
    )
