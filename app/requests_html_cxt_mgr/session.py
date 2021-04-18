from requests_html import AsyncHTMLSession


class AsyncHTMLSessionCxt(AsyncHTMLSession):
    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, type, exc_type, tb):
        await self.close()

