import chardet
import codecs


def bytes2unicode(raw, errors="replace"):
    # This way we don't leave the bom at the start of the string, should it exist
    encoding_map = {
        'utf-8-sig': (codecs.BOM_UTF8,),
        'utf-16': (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE),
        'utf-32': (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)
    }
    for enc, boms in encoding_map.items():
        if any(raw.startswith(bom) for bom in boms):
            encoding = enc
            break
    else:
        # No BOM found, so use chardet
        detection = chardet.detect(raw)
        encoding = detection.get('encoding') or "utf-8"
    return raw.decode(encoding, errors=errors)
