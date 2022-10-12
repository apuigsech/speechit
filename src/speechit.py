import requests
import tempfile

from bs4 import BeautifulSoup as soup
from argparse import ArgumentParser
from configobj import ConfigObj
from moviepy.editor import concatenate_audioclips, AudioFileClip
from joblib import Parallel, delayed

from .translators import Translator
from .voicers import Voicer


def html_request(url, query=None, cookies=None):
    r = requests.get(url, cookies=cookies)
    return soup(r.content, 'html.parser').select(query)[0]

def html_clean(html, tags=['a', 'span', 'em', 'strong']):
	for tag in tags:
		for item in html.find_all(tag):
			item.replaceWith(item.text)
	return(html)    


def html_translate_parallel(html, translator, target, tags=['p', 'h1', 'h2', 'h3', 'h4']):
    Parallel(n_jobs=50, backend="threading")(delayed(html_translate_item)(item, translator, target, mime_type='text/html') for item in html.find_all(tags))
    return(html)

def html_translate_item(item, translator, target, mime_type):
    new = translator.translate(str(item), target, mime_type='text/html')
    item.replaceWith(soup(new, 'html.parser'))



def html_voice_parallel(html, voicer, lang,  tags=['p', 'h1', 'h2', 'h3', 'h4']):
    clips = Parallel(n_jobs=50, backend="threading")(delayed(html_voice_item)(item, voicer, lang) for item in html.find_all(tags))
    final_clip = concatenate_audioclips(list(filter(lambda x: x != None, clips)))
    return final_clip

def html_voice_item(item, voicer, lang):
    if len(item.get_text()) > 5:
        return AudioFileClip(voicer.voice(str(item.get_text()), lang))


def main():
    args_parser = ArgumentParser(prog='speechit')
    args_parser.add_argument("-c", "--config", help="read config from a file", default="default.conf")

    args_parser.add_argument("-i", "--input", help="input url", required=True)
    args_parser.add_argument("--input.query", help="", default=None)
    args_parser.add_argument("--input.cookie", nargs=2, action='append', help="")

    args_parser.add_argument("-o", "--output", help="output file", default='out')
    args_parser.add_argument("--output.format", help="", choices=['html', 'plain_html', 'mp3'], default='html')
    args_parser.add_argument("--output.translate", help="", default=None)

    args = args_parser.parse_args()

    try:
        config = ConfigObj(args.config)
    except Exception as exc:
        print(f"Unable to read config: {str(exc)}")
        exit(0)

    input_url = args.input
    for input in config['inputs']:
        if input in input_url:
            input_query = config['inputs'][input]['query']
            input_cookies = {}
            for cookie in filter(lambda x: x.startswith('cookie.'), config['inputs'][input]):
                input_cookies[cookie.removeprefix('cookie.')] = config['inputs'][input][cookie]

    if args.__dict__['input.query']:
        input_query = args.__dict__['input.query']

    if args.__dict__['input.cookie']:
        for c in args.__dict__['input.cookie']:
            input_cookies[c[0]] = c[1]

    html = html_request(input_url, input_query, input_cookies)

    if args.__dict__['output.format'] in ['plain_html', 'mp3']:
        html = html_clean(html, tags=['a', 'span', 'em', 'strong'])

    if args.__dict__['output.translate']:
        t = Translator(config['service.translator']['service'], config=config['service.translator'])
        html = html_translate_parallel(html, t, args.__dict__['output.translate'])

    if args.__dict__['output.format'] in ['html', 'plain_html']:
        html = html.prettify("utf-8")
        with open(args.output, "wb") as fh:
            fh.write(html)
    elif args.__dict__['output.format'] == 'mp3':
        t = Translator(config['service.translator']['service'], config=config['service.translator'])
        v = Voicer(config['service.voicer']['service'], config=config['service.voicer'])
        clip = html_voice_parallel(html, v, t.detect_language(str(html)))
        clip.write_audiofile(args.output)