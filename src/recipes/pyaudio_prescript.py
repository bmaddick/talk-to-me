import os
import sys
import ctypes

def _initialize_portaudio():
    # Look for PortAudio in the app bundle first
    bundle_lib = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'Frameworks', 'libportaudio.2.dylib')
    try:
        return ctypes.CDLL(bundle_lib)
    except OSError:
        # Fallback to system locations
        try:
            return ctypes.CDLL('libportaudio.2.dylib')
        except OSError:
            print("Error: Could not load PortAudio library", file=sys.stderr)
            sys.exit(1)

# Initialize PortAudio when the script is loaded
_initialize_portaudio()
