from google.cloud import translate

class TranslatorBase:
	def __init__(self, config=None):
		self.config = config
		pass

class TranslatorGCP(TranslatorBase):
	def __init__(self, config=None):
		super().__init__(config)
		self.project_id = config['gcp.project_id']
		self.location = config['gcp.location']
		self.client = translate.TranslationServiceClient()

	def detect_language(self, text, mime_type="text/plain"):
		parent = f"projects/{self.project_id}/locations/{self.location}"

		response = self.client.detect_language(
			content=text,
			parent=parent,
			mime_type=mime_type,
		)

		if response.languages[0].language_code == "und":
			response.languages[0].language_code = None

		return response.languages[0].language_code

	def translate(self, text, target, source=None, mime_type="text/plain"):
		parent = f"projects/{self.project_id}/locations/{self.location}"

		if source is None:
			source = self.detect_language(text, mime_type)
		if source is None:
			return text

		response = self.client.translate_text(
        	request={
            	"parent": parent,
            	"contents": [text],
            	"mime_type": "text/html",
            	"source_language_code": source,
            	"target_language_code": target,
        	}
		)

		return response.translations[0].translated_text

def Translator(service, config=None):
	if service == "gcp":
		return TranslatorGCP(config)