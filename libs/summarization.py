import ai21
from ai21.errors import APIError
from libs.text_utils import get_text_segments, translate_text, detect_text_language


def summarize_long_text(text: str) -> str:
    texts: list[str] = []
    summary = ""
    only_one_text_segment = True

    if len(text) > 50000:
        only_one_text_segment = False
        text_segments = get_text_segments(text, "TEXT")

        while len(text_segments) > 0:
            texts.append("")
            while len(text_segments) > 0 and len(text_segments[0]) + len(texts[-1]) < 50000:
                texts[-1] += text_segments.pop(0)
    else:
        texts.append(text)

    for item in texts:
        summary += summarize_a121(item, "TEXT", detect_text_language(item))

    if not only_one_text_segment:
        summary = summarize_long_text(summary)

    return summary


def summarize_url(url: str) -> str:
    summary = summarize_a121(url, "URL")

    if summary.find("exceeds max character limit: 50,000") != -1:
        segments = get_text_segments(url, "URL")
        text = ""

        for item in segments:
            text += item

        summary = summarize_long_text(text)

    return summary


def summarize_a121(source: str, source_type: str, source_lang: str = 'en') -> str:
    """
    The parameter source_type must be "TEXT" or "URL"
    """
    if source_lang != 'en':
        source = translate_text(source, 'en')

    try:
        result = ai21.Summarize.execute(
            source=source,
            sourceType=source_type
        )
        summary = result['summary']

        if source_lang != 'en':
            summary = translate_text(summary, source_lang)

        return summary
    except APIError as e:
        return e.details
    except Exception as e:
        return str(e)
