import datetime
from urllib import parse

class HttpSimpleObfs:

    HTTP_HEAD_END_FLAG = b"\r\n\r\n"

    def __init__(self, method="http_simple"):
        self.method = method
        self.has_sent_header = False
        self.has_recv_header = False
        self.should_add_header = False
        self.header = None

    def __repr__(self):
        return f"<OBFS:{self.method}>"

    def server_encode(self, buf):
        if not self.should_add_header:
            return buf
        if self.has_sent_header:
            return buf
        header = b"HTTP/1.1 200 OK\r\nConnection: keep-alive\r\n"
        header += b"Content-Encoding: gzip\r\nContent-Type: text/html\r\nDate: "
        header += datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT").encode()
        header += b"\r\nServer: nginx\r\nVary: Accept-Encoding"
        header += self.HTTP_HEAD_END_FLAG
        self.has_sent_header = True
        return header + buf

    def _split_header_from_buf(self, buf):
        """return ret_buf,header_buf"""
        head_index = buf.find(self.HTTP_HEAD_END_FLAG) + len(self.HTTP_HEAD_END_FLAG)
        return buf[head_index:], buf[:head_index]

    def server_decode(self, buf):
        """return：ret_buf,header"""
        if self.has_recv_header:
            return buf
        self.has_recv_header = True
        if buf.startswith(b"GET "):
            self.should_add_header = True
            ret_buf, _ = self._split_header_from_buf(buf)
            return ret_buf
        else:
            return buf

