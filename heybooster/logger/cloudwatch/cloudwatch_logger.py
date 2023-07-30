from __future__ import annotations

import boto3
import time
import logging
import botocore.errorfactory as boto_error

logging.basicConfig(level=logging.INFO)


class CloudWatchLogger:
    def __init__(self, log_group_name: str, stream_name: str = '', region_name='eu-central-1'):
        self.logger = logging.getLogger('CloudWatchLogger')

        self.log_group_name = log_group_name
        self.log_stream_name = stream_name
        self.region_name = region_name
        self.log_stream_created = False

        self.__set_client()
        self.__create_log_stream()

    def create_new_stream(self, name: str):
        """
        This function create new stream on cloudwatch logs
        Args:
            name:

        Returns: None

        """
        if self.log_stream_name == name:
            self.logger.info('Stream Name Already Exists')

            return

        self.log_stream_name = name
        self.__create_log_stream()

    def __set_client(self):
        """
        Connect AWS with boto3 library
        Returns:

        """
        self.logs_client = boto3.client('logs', region_name=self.region_name)

    def __create_log_stream(self):
        """
        Call create log stream api on boto3 before control log stream name
        Returns: None

        """
        if not self.log_stream_name or not isinstance(self.log_stream_name, str):
            self.logger.info('Log Saver Not Running Because Stream Name Invalid')

            return

        try:
            self.logs_client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name
            )
        except boto_error.ClientError:
            pass
        except Exception as error:
            self.logger.error(error)

            return

        self.log_stream_created = True

    def info(self, message: object):
        self.__put_events(
            message=f'INFO: {message}'
        )

    def warning(self, message: object):
        self.__put_events(
            message=f'WARNING: {message}',
            _type='warning'
        )

    def error(self, message: object):
        self.__put_events(
            message=f'ERROR: {message}',
            _type='error'

        )

    def __put_events(self, message: str, _type: str = "info"):
        """
        Put Message to Cloudwatch Events and Write Logs
        Args:
            message:
            _type:

        Returns: None

        """
        try:
            if message and self.log_stream_name:
                self.logs_client.put_log_events(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name,
                    logEvents=[
                        {
                            'timestamp': int(round(time.time() * 1000)),
                            'message': message
                        }
                    ]
                )
                getattr(self.logger, _type)(message)
        except Exception as e:
            self.logger.error(f'Put Events Error -> {e}')
