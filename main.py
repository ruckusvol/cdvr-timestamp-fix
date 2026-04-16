import re
import logging
from apps.output import views as output_views
from django.http import HttpResponse

logger = logging.getLogger(__name__)

# Safely store the original generator
if not hasattr(output_views, '_original_generate_m3u'):
    output_views._original_generate_m3u = output_views.generate_m3u

def patched_generate_m3u(request, profile_name=None, user=None):
    # 1. Generate the standard M3U
    response = output_views._original_generate_m3u(request, profile_name, user)
    
    # 2. Verify it's a valid text response
    if not response or not isinstance(response, HttpResponse):
        return response
        
    content_type = response.get('Content-Type', '')
    if 'audio/x-mpegurl' not in content_type or request.method == "HEAD":
        return response

    # 3. Universally apply the regex patch to all M3U outputs
    try:
        content = response.content.decode('utf-8')
        attribute = 'tvc-stream-timestamps="rewrite"'
        modified_lines = []
        
        for line in content.splitlines():
            if line.startswith("#EXTINF:") and attribute not in line:
                line = re.sub(r"(#EXTINF:-?\d+)", rf"\1 {attribute}", line, count=1)
            modified_lines.append(line)
            
        new_content = "\n".join(modified_lines) + "\n"
        response.content = new_content.encode('utf-8')
        logger.debug(f"Timestamp Fixer: Universally patched M3U for profile '{profile_name}'")
    except Exception as e:
        logger.error(f"Timestamp Fixer: Regex patch failed - {e}")

    return response

# Apply the monkey patch
output_views.generate_m3u = patched_generate_m3u

class Plugin:
    def __init__(self):
        logger.info("M3U Timestamp Fixer: Initialized global patch on output_views.generate_m3u")

    def run(self, action, params, context):
        pass
