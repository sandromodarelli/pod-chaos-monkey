#!/usr/bin/env python

"""
Main module
"""

import logging
import random
import sys
import time

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from config import NAMESPACE, LOGLEVEL, SLEEP


# Setting up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=LOGLEVEL)

# debugging ENVs
logger.debug("NAMESPACE: %s", NAMESPACE)
logger.debug("LOGLEVEL: %s", LOGLEVEL)
logger.debug("SLEEP: %s", SLEEP)

# Configs can be set in Configuration class directly or using helper utility
try:
    config.load_incluster_config()
except ConfigException as e:
    logger.error(e)
    sys.exit(1)

v1 = client.CoreV1Api()


def _list_pods(namespace: str) -> dict:
    """
    List pods in a single namespace
    :param namespace: a kubernetes namespace name
    :return: list of pods
    """
    logger.info("Retrieving pods in %s namespace", namespace)
    pod_list = v1.list_namespaced_pod(NAMESPACE, watch=False).items
    logging.debug(pod_list)
    return pod_list


def _delete_random_pod(pod_list: dict):
    """
    Deletes a random chosen pod from the input list
    :param pod_list: pod list
    :return: None
    """
    if pod_list:
        pod = random.choice(pod_list)

        # Deleting the selected pod
        logger.info("Deleting pod %s", pod.metadata.name)
        v1.delete_namespaced_pod(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace
        )
    else:
        logger.info("No pods in %s namespace", NAMESPACE)


def main(namespace):
    """
    Delete a random pod from a selected namespace

    Main function to startup the script
    :parameter: None
    :return: None

    """
    while True:
        pods = _list_pods(namespace)
        _delete_random_pod(pods)

        # Sleep to next round, if 0 stop running
        if SLEEP == 0:
            break
        time.sleep(SLEEP)


if __name__ == '__main__':
    main(NAMESPACE)
