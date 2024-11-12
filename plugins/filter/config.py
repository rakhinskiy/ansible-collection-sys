from __future__ import annotations

from typing import Any
from deepmerge import Merger


class FilterModule(object):

    def filters(self) -> dict:
        """
        :return: filters dict
        """
        return {
            "config_role": self.config_role,
            "config_search_nodes": self.config_search_nodes,
            "config_search_keys": self.config_search_keys,
            "config_check_key": self.config_check_key,
            "config_get_key": self.config_get_key,
        }

    def config_check_key(self, data: dict, key: str) -> bool:
        if "." in key:
            _current, _next = key.split(".", 1)
            _data = data.get(_current, None)

            if not _data or not isinstance(_data, dict):
                return False

            return self.config_check_key(data=_data, key=_next)

        if key in data.keys():
            return True

        return False

    def config_get_key(self, data: dict, key: str, default: Any = None) -> Any:
        if "." in key:
            _current, _next = key.split(".", 1)
            _data = data.get(_current, None)

            if not _data or not isinstance(_data, dict):
                return default

            return self.config_get_key(data=_data, key=_next, default=default)

        result = data.get(key)

        if result:
            return result

        return default

    def config_role(
        self,
        var: dict,
        host: str,
        role: str,
        defaults: dict = None,
        instances: bool = False,
    ) -> dict:

        result = {}

        merger = Merger(
            type_strategies=[
                (list, ["append_unique"]),
                (dict, ["merge"]),
                (set, ["union"]),
            ],
            fallback_strategies=["override"],
            type_conflict_strategies=["override"],
        )

        data = var.get(host, {})

        _node_ = self.config_get_key(data=data, key="node", default={})
        _role_ = self.config_get_key(data=data, key=f"role.{role}", default={})
        _instances_ = self.config_get_key(
            data=_node_, key=f"{role}.instances", default={}
        )

        if instances:
            for instance in _instances_.keys():
                result[instance] = defaults or {}
                result[instance] = merger.merge(
                    result[instance],
                    _role_.get("defaults", {}) or {},
                )
                result[instance] = merger.merge(
                    result[instance], _role_.get(instance, {}) or {}
                )
                result[instance] = merger.merge(
                    result[instance], _instances_.get(instance, {}) or {}
                )
        else:
            result = defaults or {}
            result = merger.merge(result, _role_.get("defaults", {}) or {})
            result = merger.merge(result, _node_.get(role, {}) or {})

        return result

    def config_search_nodes(
        self,
        var: dict,
        host: str,
        role: str,
        instance: str = None,
        exclude: bool | str = None,
    ) -> list:
        # Return all nodes in role instance
        result = []

        if isinstance(exclude, bool) and exclude:
            exclude = host

        nodes = var.keys()

        for node in nodes:
            data = var.get(node)
            if isinstance(exclude, str) and node == exclude:
                continue
            if (
                instance
                and instance
                in self.config_get_key(
                    data=data, key=f"{role}.instances", default={}
                ).keys()
            ):
                result.append(node)
                continue
            if (
                not instance
                and role
                in self.config_get_key(
                    data=data, key="roles", default={}
                ).keys()
            ):
                result.append(node)

        return result

    def config_search_keys(
        self,
        var: dict,
        host: str,
        get: str,
        check: str = None,
        exclude: bool | str = None,
    ) -> list:
        # Return all nodes in role instance
        result = []

        if isinstance(exclude, bool) and exclude:
            exclude = host

        nodes = var.keys()

        for node in nodes:
            data = var.get(node, {})
            if isinstance(exclude, str) and node == exclude:
                continue
            if (
                check
                and self.config_check_key(data=data, key=check)
                and self.config_get_key(data=data, key=get)
            ):
                result.append(self.config_get_key(data=data, key=get))
                continue
            if not check and self.config_get_key(data=data, key=get):
                result.append(self.config_get_key(data=data, key=get))

        return result
