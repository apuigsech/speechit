import tempfile
from voicemaker import Voicemaker


class VoicerBase:
    def __init__(self, config=None):
        self.config = config
        pass

class VoicerVoicemaker(VoicerBase):
    def __init__(self, config=None):
        super().__init__(config)
        self.vm = Voicemaker()
        self.vm.set_token(config['voicemaker.access_token'])

    def voice(self, text, lang):
        language_code, voice_id = self.config[f'voicemaker.voice.{lang}'].split('/')
        filename=tempfile.mkstemp()[1]
        self.vm.generate_audio_to_file(filename, text, language_code=language_code, voice_id=voice_id)
        return filename

def Voicer(service, config=None):
	if service == "voicemaker":
		return VoicerVoicemaker(config)