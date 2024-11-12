from __future__ import annotations


class FilterModule(object):

    def filters(self) -> dict:
        """
        :return: filters dict
        """
        return {
            "os_dist_code": self.os_dist_code,
            "os_name_code": self.os_name_code,
        }

    @staticmethod
    def os_dist_code(var: str) -> str:
        """
        Return short code for os
        :param var:
        :return: str
        """
        var = str(var).lower().replace("linux", "")

        if var in ["alma"]:
            return "al"
        if var in ["centos"]:
            return "co"
        if var in ["oracle"]:
            return "ol"
        if var in ["redhat"]:
            return "rh"
        if var in ["rocky"]:
            return "rl"
        if var in ["debian"]:
            return "debian"
        if var in ["ubuntu"]:
            return "ubuntu"

        return ""

    @staticmethod
    def os_name_code(var: str, version: str) -> str:
        """
        Return short code for os
        :param var:
        :param version:
        :return: str
        """
        var = str(var).lower()
        version = str(version).lower()

        if var in ["alma", "almalinux"]:
            return f"al-{version}"
        if var in ["centos"]:
            return f"co-{version}"
        if var in ["oracle", "oraclelinux"]:
            return f"ol-{version}"
        if var in ["redhat"]:
            return f"rh-{version}"
        if var in ["rocky", "rockylinux"]:
            return f"rl-{version}"
        if var in ["debian"]:
            return f"debian-{version}"
        if var in ["ubuntu"]:
            return f"ubuntu-{version}"

        return ""
