import ai21
from ai21.errors import APIError
from libs.text_utils import get_text_segments, translate_text, detect_text_language


def summarize_long_text(text: str) -> str:
    """
    Summarizes long text using the AI21 Studio API.

    :param text: The text to summarize.
    :type text: str
    :return: The summary of the text.
    :rtype: str
    """
    # Initialize an empty list to store the text segments
    texts: list[str] = []

    # Initialize an empty string to store the summary
    summary = ""

    # Initialize a flag variable to indicate whether there is only one text segment
    only_one_text_segment = True

    if len(text) > 50000:
        # Set the flag variable to False
        only_one_text_segment = False

        # Append a new empty string to the texts list
        texts.append("")

        # Use the get_text_segments function to split the text into segments
        text_segments = get_text_segments(text, "TEXT")

        # Iterate over the text segments
        for segment in text_segments:
            # If the last text in the texts list plus the current segment is longer than 50000 characters
            if len(texts[-1]) + len(segment) > 50000:
                # Append a new empty string to the texts list
                texts.append("")

            # Append the current segment to the last text in the texts list
            texts[-1] += segment
    else:
        # If the text is not longer than 50000 characters, append it to the texts list as a single segment
        texts.append(text)

    # Iterate over the texts in the texts list
    for item in texts:
        # Use the summarize_a121 function to summarize each text and append it to the summary string
        summary += summarize_a121(item, "TEXT", detect_text_language(item))

    # If there was more than one text segment
    if not only_one_text_segment:
        # Use the summarize_long_text function recursively to summarize the concatenated summaries
        summary = summarize_long_text(summary)

    # Return the final summary
    return summary


def summarize_url(url: str) -> str:
    """
    Summarizes the text content of a URL using the AI21 Studio API.

    :param url: The URL to summarize the text content of.
    :type url: str
    :return: The summary of the text content.
    :rtype: str
    """
    # Use the summarize_a121 function to summarize the text content of the URL
    summary = summarize_a121(url, "URL")

    # If the summary contains an error message indicating that the text exceeds the maximum character limit
    if summary.find("exceeds max character limit: 50,000") != -1:
        # Use the get_text_segments function to split the text into segments
        segments = get_text_segments(url, "URL")

        # Initialize an empty string to store the concatenated segments
        text = ""

        # Concatenate the segments into a single string
        for item in segments:
            text += item

        # Use the summarize_long_text function to summarize the concatenated segments
        summary = summarize_long_text(text)

    # Return the summary
    return summary


def summarize_a121(source: str, source_type: str, source_lang: str = 'en') -> str:
    """
    Summarizes text or the text content of a URL using the AI21 Studio API.

    :param source: The text or URL to summarize.
    :type source: str
    :param source_type: The type of the source. Must be "TEXT" or "URL".
    :type source_type: str
    :param source_lang: The language of the source. Defaults to 'en' from english.
    :type source_lang: str, optional
    :return: The summary of the text or text content.
    :rtype: str
    """
    # If the source language is not English
    if source_lang != 'en':
        # Translate the source into English using the translate_text function
        source = translate_text(source, 'en')

    try:
        # Use the AI21 Studio API to summarize the text or text content
        result = ai21.Summarize.execute(
            source=source,
            sourceType=source_type
        )

        # Extract the summary from the result
        summary = result['summary']

        # If the source language is not English
        if source_lang != 'en':
            # Translate the summary back into the original language using the translate_text function
            summary = translate_text(summary, source_lang)

        # Return the summary
        return summary
    except APIError as e:
        # If an APIError occurs, return its details
        return e.details
    except Exception as e:
        # If any other exception occurs, return its string representation
        return str(e)
