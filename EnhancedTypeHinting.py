"""
EnhancedTypeHinting program.
"""

import re


class EnhancedTypeHinting:

    """
    This class implements enhanced type hinting system which helps in creation of advanced type hints for objects.
    """

    def __init__(self, data: object) -> None:
        """
        Constructor for the EnhancedTypeHinting class.

        :param data: The object to determine its type hint.
        """
        self.__data: object = data

    @staticmethod
    def __consolidate_types(type_strs) -> str:

        """
        Consolidate repeated types in the given type hint list.

        :param type_strs: The list of type hint strings to consolidate.
        :return: Fixed string.
        """

        # Deduplicate while preserving order
        seen = set()
        return ' | '.join([x for x in type_strs if x not in seen and not seen.add(x)])

    def __determine_general_type_hint(self, value: object) -> str:

        """
        Determine a general type hint for the given value.

        :param value: Object to determine the type of.
        :return: General type hint.
        """

        if value is None:
            return "NoneType"
        elif isinstance(value, list):
            return f"list[{self.__consolidate_types([self.__determine_general_type_hint(v) for v in value])}]"
        elif isinstance(value, tuple):
            return f"tuple[{', '.join([self.__determine_general_type_hint(v) for v in value])}]"
        elif isinstance(value, dict):
            return f"dict[" \
                   f"{self.__consolidate_types([self.__determine_general_type_hint(k) for k in value.keys()])}, " \
                   f"{self.__consolidate_types([self.__determine_general_type_hint(v) for v in value.values()])}]"
        elif isinstance(value, set):
            return f"set[{self.__consolidate_types([self.__determine_general_type_hint(v) for v in value])}]"
        elif isinstance(value, frozenset):
            return f"frozenset[{self.__consolidate_types([self.__determine_general_type_hint(v) for v in value])}]"
        else:
            return type(value).__name__

    def construct_general_type_hint(self) -> str:

        """
        Construct a general type hint for the given data.

        :return: General type hint string for the provided data.

        Note:
            Properly formats the type hint by removing extra spaces
        """

        return re.sub(r'\s+', ' ', self.__determine_general_type_hint(self.__data)).strip()
