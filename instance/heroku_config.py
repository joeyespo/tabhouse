"""\
Epio Config

The recommended usage of this file is to rename it to <servername>_config.py.
This can be loaded by setting the SETTINGS_MODULE environment variable to here.

See default_config for a complete list of overridable settings.
"""


# Security settings
SECRET_KEY = 'uZLgrzmxYzBRBhzAiffm'

# Logging settings
ERROR_EMAIL_INFO = (('smtp.gmail.com', 587),
                    '"Epio Error Notification" <epio.errors@gmail.com>', ['espo58@gmail.com'],
                    'Tabhouse Error', ('epio.errors@gmail.com', '1UMbJXCNgCHvEoEiMiv9'))

# Analytics settings
ANALYTICS_SCRIPT = """\
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-26864275-1']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
"""

# User feedback settings
FEEDBACK_BLOCK = """\
<style>
#uvTab { top: 30% !important; }
@media only screen and (max-device-width: 480px) {
    #uvTab { display: none !important; }
}
@media handheld {
    #uvTab { display: none !important; }
}
</style>
<script>
var uvOptions = {};
(function() {
var uv = document.createElement('script'); uv.type = 'text/javascript'; uv.async = true;
uv.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + 'widget.uservoice.com/eY2YtrTu2YUkWsocmUlmg.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(uv, s);
})();
</script>
"""
