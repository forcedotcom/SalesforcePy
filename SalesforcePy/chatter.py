"""
.. module:: chatter
   :synopsis: Module dedicated to Chatter requests.

.. moduleauthor:: Jose Garcia Ponce <jgarciaponce@salesforce.com>
.. versionadded:: 1.0.0

"""
from __future__ import absolute_import

from . import commons

FEED_COMMENT_SERVICE = '/services/data/v%s/chatter/feed-elements/%s/capabilities/comments/items'
FEED_ITEM_SERVICE = '/services/data/v%s/chatter/feed-elements'


class Chatter(commons.ApiNamespace):
    """ The Chatter namespace class from which all API calls to a Salesforce organisation are made.
        .. versionadded:: 1.0.0
    """
    @commons.kwarg_adder
    def feed_item(self, body, **kwargs):
        """ Performs a feed item request.

          :param: body: The feed item resource to post.
          :type: body: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Feed Item response
          :rtype: (dict, chatter.ChatterFeedItem)
        """
        client = self.client
        fi = ChatterFeedItem(client.session_id, client.instance_url, body, **kwargs)
        res = fi.request()

        return res, fi

    @commons.kwarg_adder
    def feed_comment(self, _id, body, **kwargs):
        """ Performs a feed item request.

          :param: _id: The feed comment id to post.
          :type: _id: string
          :param: body: The feed comment resource to post.
          :type: body: dict
          :param: **kwargs: kwargs
          :type: **kwargs: dict
          :return: Feed Comment response
          :rtype: (dict, chatter.ChatterFeedComment)
        """
        client = self.client
        fc = ChatterFeedComment(client.session_id, client.instance_url, _id, body, **kwargs)
        res = fc.request()

        return res, fc


class ChatterFeedComment(commons.BaseRequest):
    """ Performs a request to `'/services/data/v<api_version>/chatter/feed-elements/<id>/capabilities/comments/items'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, _id, body, **kwargs):
        super(ChatterFeedComment, self).__init__(session_id, instance_url, **kwargs)

        self.request_body = body
        self.http_method = 'POST'
        self.service = FEED_COMMENT_SERVICE % (self.api_version, _id)


class ChatterFeedItem(commons.BaseRequest):
    """ Performs a request to `'/services/data/v<api_version>/chatter/feed-elements'`
        .. versionadded:: 1.0.0
    """
    def __init__(self, session_id, instance_url, body, **kwargs):
        super(ChatterFeedItem, self).__init__(session_id, instance_url, **kwargs)

        self.request_body = body
        self.http_method = 'POST'
        self.service = FEED_ITEM_SERVICE % self.api_version
