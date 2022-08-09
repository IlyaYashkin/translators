import sys
import json
import base64
import requests
import translators as ts

def main():
  while True:
    input_string = input()

    if input_string == ".exit": break
    try:
      input_dict = json.loads(input_string)
    except json.decoder.JSONDecodeError as e:
      sys.stderr.buffer.write(f'Wrong JSON Error\n{str(e)}\n'.encode("utf8"))
      continue

    try:
      ts_engine = getattr(ts, input_dict['engine'])
    except AttributeError as e: 
      sys.stderr.buffer.write(f'Translation engine not found\n{str(e)}\n'.encode("utf8"))
      continue

    try:
      translated_string = ts_engine(
        base64.b64decode(input_dict['text']).decode("utf8"),
        from_language=input_dict['from'],
        to_language=input_dict['to'],
        proxies=input_dict['proxies']
      )
      translated_string += "\n"
      sys.stdout.buffer.write(translated_string.encode("utf8"))
    except requests.exceptions.HTTPError as e:
      sys.stderr.buffer.write(f'HTTP Error\n{str(e)}\n'.encode("utf8"))
    except ts.apis.TranslatorError as e:
      sys.stderr.buffer.write(f'Translation Error\n{str(e)}\n'.encode("utf-8"))
    except Exception as e:
      sys.stderr.buffer.write(f'Some Error\n{str(e)}\n'.encode("utf8"))


if __name__ == "__main__":
  main()
