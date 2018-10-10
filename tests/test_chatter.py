import testutil
import responses


def create_message_segments(subject, recipients, text_to_post):
    """ Creates a chatter post with simple text, it can also @mention, post to groups, users or records.
        To facilitate its usage, it build the message based on the arguments provided as required, see link below
                    https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/quickreference_post_comment_or_feed_item_with_mention.htm?search_text=mention
            """
    if text_to_post is None:
        text_to_post = ""

    # we raise an exception here as the default API response when missing
    # these values is not user-friendly.
    if subject is None or (recipients is None and len(text_to_post) < 1):
        raise ValueError(
            "You must provide a subject and you must provide a text or @mention someone.")

    messages = list()
    messages.append({"type": "text", "text": " " + text_to_post + " "})
    message_segments = {"messageSegments": ""}

    if recipients:
        [messages.append({"type": "Mention", "id": i})
         for i in recipients if len(i) > 0]

    message_segments["messageSegments"] = messages
    body = {
        "body": message_segments,
        "feedElementType": "FeedItem",
        "subjectId": subject}

    return body


@responses.activate
def test_chatter_feed_item():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("chatter_feed_item_201")
    client = testutil.get_client()
    body = create_message_segments(
        "005B0000001mOGj",
        ["005B0000001nDnV"],
        "Money, get away ")
    ch = client.chatter.feed_item(body)
    assert ch[1].status == 201
    chatter_response = ch[0]
    assert chatter_response.get("actor").get("type") == "TextPost"


@responses.activate
def test_chatter_comment():
    testutil.add_response("login_response_200")
    testutil.add_response("api_version_response_200")
    testutil.add_response("chatter_feed_comment_201")
    client = testutil.get_client()

    body = {
        "body": {
            "messageSegments": [
                {
                    "type": "Text",
                    "text": "New comment 2"
                }
            ]
        }
    }
    ch = client.chatter.feed_comment(_id="0D5B000000T7MxR", body=body)
    assert ch[1].status == 201
