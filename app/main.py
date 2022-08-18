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


def list_pods(api, namespace: str) -> dict:
    """
    List pods in a single namespace
    :param api: versioned kubernetes api
    :param namespace: a kubernetes namespace name
    :return: list of pods
    """
    logger.info("Retrieving pods in %s namespace", namespace)
    pod_list = api.list_namespaced_pod(NAMESPACE, watch=False).items
    logging.debug(pod_list)
    return pod_list


def delete_random_pod(api, pod_list: dict):
    """
    Deletes a random chosen pod from the input list
    :param api: versioned kubernetes api
    :param pod_list: pod list
    :return: None
    """
    if pod_list:
        pod = random.choice(pod_list)

        # Deleting the selected pod
        logger.info("Deleting pod %s", pod.metadata.name)
        return api.delete_namespaced_pod(
            name=pod.metadata.name,
            namespace=pod.metadata.namespace
        )
    else:
        logger.info("No pods in %s namespace", NAMESPACE)
        return None


def main(namespace, sleep):
    """
    Delete a random pod from a selected namespace

    Main function to startup the script
    :parameter: None
    :return: None

    """
    # Configs can be set in Configuration class directly or using helper utility
    try:
        config.load_incluster_config()
        # config.load_kube_config() # use this for local debugging
    except ConfigException as e:
        logger.error(e)
        sys.exit(1)

    v1 = client.CoreV1Api()

    while True:
        pods = list_pods(v1, namespace)
        deleted_pod = delete_random_pod(v1, pods)

        # Sleep to next round, if 0 stop running
        if sleep == 0:
            break
        time.sleep(sleep)


if __name__ == '__main__':
    main(NAMESPACE, SLEEP)
