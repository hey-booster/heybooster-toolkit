import requests
import asyncio
import logging

from raven import Client

logger = logging.getLogger(__name__)


class HeyboosterException:
    """ Heybooster Exception Class """

    def __init__(self, sentry_dns=None):
        """ Init Function """
        self.dns = sentry_dns

    @staticmethod
    def __post_error_message(url: str, message: str, extra: object):
        """
        This function send post request of error message and extra data
        """
        try:
            body = {"error": message, "extra": extra}
            requests.post(
                url=url,
                json=body
            )
        except Exception as e:
            logger.error(e)

    def exception_catcher(self, **kwargs):
        """ Exception Decarator """
        default = kwargs.get('default')
        default_callback = kwargs.get('callback')
        error_callback = kwargs.get('error_callback')
        post_endpoint = kwargs.get('post_endpoint')
        extra_data = kwargs.get('extra')

        def wrapper(func):
            def run_func(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    err = " Path : {path} \n" \
                          " Function : {func} \n" \
                          " Error: {error}".format(
                        path=str(func.__code__.co_filename),
                        func=func.__name__,
                        error=e
                    )

                    if self.dns:
                        sentry = Client(self.dns)
                        sentry.tags_context({
                            'function_name': str(func.__name__),
                            'related_file_name': str(func.__code__.co_filename),
                            "annotations": str(func.__annotations__)
                        })
                        sentry.captureException()

                    if post_endpoint and isinstance(post_endpoint, str):
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(
                            self.__post_error_message(url=post_endpoint, message=str(e), extra=extra_data)
                        )
                        loop.close()

                    if error_callback is not None:
                        error_callback(e)

                    logger.error(err)

                    if default_callback is not None:
                        return default_callback(default)

                    return default

            return run_func

        return wrapper
