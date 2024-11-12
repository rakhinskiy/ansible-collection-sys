from __future__ import annotations

from typing import Any

from ansible.parsing.yaml.objects import (
    AnsibleUnicode,
    AnsibleVaultEncryptedUnicode,
)
from ansible.utils.unsafe_proxy import AnsibleUnsafe


class TestModule(object):

    ANSIBLE_STRINGS = (
        str,
        AnsibleUnicode,
        AnsibleVaultEncryptedUnicode,
        AnsibleUnsafe,
    )

    def tests(self):
        return {
            "list": self.is_list,
            "list_dicts": self.is_list_dicts,
            "dict": self.is_dict,
            "str": self.is_str,
        }

    @staticmethod
    def is_list(var: Any) -> bool:
        """
        :param var: any variable
        :return: true if var is not empty list
        """
        return var and isinstance(var, list) and len(var) > 0

    def is_list_dicts(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is list of dicts
        """
        if not self.is_list(var):
            return False

        for element in var:
            if not self.is_dict(element):
                return False

        return True

    @staticmethod
    def is_dict(var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is not empty dict
        """
        return var and isinstance(var, dict) and var != {}

    def is_str(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is one of instance of string and not empty
        """
        return var and isinstance(var, self.ANSIBLE_STRINGS) and len(var) > 0
