import pytest
from unittest.mock import MagicMock, patch

from ..main import list_pods, delete_random_pod


@patch("config.NAMESPACE")
@patch("kubernetes.client.api.core_v1_api.CoreV1Api")
def test_list_pods(api, namespace):
    pod1 = MagicMock()
    pod1.metadata.name = "my-app-1"
    pod1.metadata.namespace = namespace

    pod2 = MagicMock()
    pod2.metadata.name = "my-app-2"
    pod2.metadata.namespace = namespace

    pod3 = MagicMock()
    pod3.metadata.name = "my-app-3"
    pod3.metadata.namespace = namespace

    items = [pod1, pod2, pod3]

    api.list_namespaced_pod(namespace, watch=False).items = items

    pods_list = list_pods(api, namespace)

    assert pods_list == items


@patch("random.choice")
@patch("config.NAMESPACE")
@patch("kubernetes.client.api.core_v1_api.CoreV1Api")
def test_delete_random_pod(api, namespace, choice_mock):
    pod1 = MagicMock()
    pod1.metadata.name = "my-app-1"
    pod1.metadata.namespace = namespace

    pod2 = MagicMock()
    pod2.metadata.name = "my-app-2"
    pod2.metadata.namespace = namespace

    pod3 = MagicMock()
    pod3.metadata.name = "my-app-3"
    pod3.metadata.namespace = namespace

    items = [pod1, pod2, pod3]

    choice_mock.return_value = pod2

    deleted_pod = delete_random_pod(api, items)

    assert api.delete_namespaced_pod.call_count == 1
    api.delete_namespaced_pod.assert_called_with(
        name=pod2.metadata.name,
        namespace=pod2.metadata.namespace
    )