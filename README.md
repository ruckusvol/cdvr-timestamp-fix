# Channels DVR Timestamp Fix for Dispatcharr

This plugin intercepts Dispatcharr's native M3U generation and universally injects the `tvc-stream-timestamps="rewrite"` tag into every `#EXTINF` line. 

This is specifically designed for users piping Dispatcharr into Channels DVR. It forces the Channels DVR transcoder engine to rewrite broken or drifting timestamps on the fly, preventing buffering and looping issues on proxy streams.

## Installation
1. Install via the Dispatcharr Plugin UI.
2. **You must restart Dispatcharr** for the core code patch to take effect.
3. No further configuration is required. The patch applies globally to all M3U endpoints.
