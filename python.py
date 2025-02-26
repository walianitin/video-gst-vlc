import threading
import time
import gi

gi.require_version("Gst", "1.0")
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GstRtspServer

Gst.init(None)

class TestRtspServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.server.set_service("8554")

        # Create a media factory
        self.factory = GstRtspServer.RTSPMediaFactory()
        pipeline = (
            "( autovideosrc ! videoconvert "
            "! x264enc tune=zerolatency ! queue "
            "! rtph264pay name=pay0 pt=96 )"
        )
        self.factory.set_launch(pipeline)

        # Attach the factory to the server
        self.server.get_mount_points().add_factory("/stream", self.factory)

        # Start the server
        self.server.attach(None)

def main():
    server = TestRtspServer()
    print("RTSP stream available at: rtsp://127.0.0.1:8554/stream")

    # GLib main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()

if __name__ == "__main__":
    main()
