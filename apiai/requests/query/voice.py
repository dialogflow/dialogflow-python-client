# -*- coding: utf-8 -*-

from . import QueryRequest

import sys
import uuid
import json
import warnings

PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
else:
    def b(s):
        return s


class VoiceRequest(QueryRequest):
    """
        .. deprecated:: 1.0.3

        VoiceRequest request class

        Send voice data by chunks.

        This is method deprecated. Will be removed on 1 Feb 2016.
        THis is method working only for for old paid plans and
        doesn't work for all new users.

        Basic Usage::
            >>> ...
            >>> voice_request = ai.voice_request()
            >>> bytessize = 2048
            >>>
            >>> with open('log.raw', 'rb') as f:
            >>>     data = f.read(bytessize)
            >>>     while data:
            >>>         request.send(data)
            >>>         data = f.read(bytessize)
            >>>
            >>> request.getresponse()
            <JSON response>
    """

    def __init__(self, client_access_token, base_url, version, session_id):
        warnings.warn('VoiceRequest will be removed on 1 Feb 2016', DeprecationWarning)

        super(VoiceRequest, self).__init__(
            client_access_token,
            base_url,
            version,
            session_id
        )

        self._audio_mime_type = None

    @property
    def audio_mime_type(self):
        """
            audio mime type, default value equal None. If value is None then
            uses 'audio/wav' mime type.

            :rtype: str or unicode
        """

        return self._audio_mime_type

    @audio_mime_type.setter
    def audio_mime_type(self, value):
        """
            audio mime type setter
            :type value: str or unicode
        """

        self._audio_mime_type = value

    def send(self, chunk):
        """
            Send a given data chunk of voice data.
        """

        parts = []

        parts.append('%x' % len(chunk))

        if PY3:
            parts.append(chunk.decode('latin-1'))
        else:
            parts.append(chunk)

        parts.append('')

        newChunk = '\r\n'.join(parts)

        super(VoiceRequest, self).send(b(newChunk))

    def _prepare_headers(self):
        uuid_hex = uuid.uuid4().hex
        self.boundary = ('--------{0}'.format(uuid_hex)).encode('utf-8')

        return {
            'Content-Type': 'multipart/form-data; boundary=%s' % self.boundary,
            'Transfer-Encoding': 'chunked',
            'Connection': 'keep-alive',
        }

    def _prepage_begin_request_data(self):
        data = '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="request"\r\n'
        data += 'Content-Type: application/json\r\n\r\n'

        data += json.dumps(
            {
                'lang': self.lang or 'en',
                'sessionId': self.session_id,
                'contexts': self.contexts,
                'timezone': self.time_zone,
                'resetContexts': self.resetContexts,
                'entities': self._prepare_entities()
            }
        )

        data += '\r\n'
        data += '--%s\r\n' % self.boundary
        data += 'Content-Disposition: form-data; name="voiceData"\r\n'
        data += 'Content-Type: %s\r\n\r\n' % (self._audio_mime_type_prepare())

        return data

    def _audio_mime_type_prepare(self):
        current_audio_mime_type = self.audio_mime_type
        if current_audio_mime_type is None:
            current_audio_mime_type = 'audio/wav'

        return current_audio_mime_type

    def _prepage_end_request_data(self):
        return '\r\n--%s--\r\n' % self.boundary

    def _beforegetresponce(self):
        self._connection.send(b('0\r\n\r\n'))
