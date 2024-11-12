from __future__ import annotations

from typing import Any


class FilterModule(object):

    def filters(self) -> dict:
        """
        :return: filters dict
        """
        return {
            "justify_hash": self.justify_hash,
            "justify_list": self.justify_list,
            "to_list": self.to_list,
        }

    @staticmethod
    def justify_hash(var: dict) -> int:
        """
        Return short code for os
        :param var:
        :return: int
        """

        result = []

        for k in var.keys():
            result.append(len(k))

        return max(result)

    @staticmethod
    def justify_list(var: list, key: str) -> int:
        """
        Return short code for os
        :param var:
        :param key:
        :return: int
        """

        result = []
        for item in var:
            result.append(len(item.get(key, "")))

        return max(result)

    @staticmethod
    def to_list(var: Any) -> list:
        """
        Return short code for os
        :param var:
        :return: list
        """

        if not isinstance(var, list):
            return [
                var,
            ]
        return var
