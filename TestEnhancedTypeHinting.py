"""
Unit tests for EnhancedTypeHinting
"""

import unittest
import EnhancedTypeHinting


class TestEnhancedTypeHinting(unittest.TestCase):

    data_nested: dict[
        str,
        int | list[int | list[int | list[int]] | dict[str, int | list[int]]] | tuple[int, list[int], dict[str, int]] |
        dict[str, list[int] | dict[str, list[int] | int] | tuple[int, int, list[int]]]
    ] = {
        "int": 1,
        "list": [1, 2, [3, 4, [5, 6]], {"a": 7, "b": [8, 9]}],
        "tuple": (1, [2, 3], {"a": 4, "b": 5}),
        "dict": {"key1": [1, 2, 3], "key2": {"subkey1": [4, 5], "subkey2": 6}, "key3": (7, 8, [9, 10])}
    }

    @staticmethod
    def type_hint_components_equal(type_hint_1: str, type_hint_2: str) -> bool:
        """
        Compares two type hint strings by breaking them into their constituent parts.
        """
        components_1 = set(type_hint_1.replace(" ", "").split("|"))
        components_2 = set(type_hint_2.replace(" ", "").split("|"))
        return components_1 == components_2

    def test_primitive_types(self):
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(123).construct_general_type_hint(), "int")
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(12.34).construct_general_type_hint(), "float")
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting("hello").construct_general_type_hint(), "str")
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(True).construct_general_type_hint(), "bool")
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(None).construct_general_type_hint(), "NoneType")
        )

    def test_complex_types(self):
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting([1, 2.3, "test", [1, 2], {"a": 1, "b": 2}]).construct_general_type_hint(),
                "list[int | float | str | list[int] | dict[str, int]]"
            )
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting((1, "test", 3.4, [1, 2], {"a": 1, "b": 2})).construct_general_type_hint(),
                "tuple[int, str, float, list[int], dict[str, int]]"
            )
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting({1, 2, 3, "test"}).construct_general_type_hint(),
                "set[int | str]"
            )
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting(frozenset([1, 2, 3, "test"])).construct_general_type_hint(),
                "frozenset[int | str]"
            )
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting({"a": 1, "b": [1, 2, 3]}).construct_general_type_hint(),
                "dict[str, int | list[int]]"
            )
        )

    def test_special_types(self):
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(b'test').construct_general_type_hint(), "bytes")
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting(bytearray([65, 66, 67])).construct_general_type_hint(),
                "bytearray"
            )
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(1+2j).construct_general_type_hint(), "complex")
        )
        self.assertTrue(
            self.type_hint_components_equal(EnhancedTypeHinting(range(5)).construct_general_type_hint(), "range")
        )
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting(memoryview(b"hello")).construct_general_type_hint(),
                "memoryview"
            )
        )

    def test_nested_types(self):
        self.assertTrue(
            self.type_hint_components_equal(
                EnhancedTypeHinting(self.data_nested).construct_general_type_hint(),
                "dict[str, int | list[int | list[int | list[int]] | dict[str, int | list[int]]] | "
                "tuple[int, list[int], dict[str, int]] | dict[str, list[int] | dict[str, list[int] | int] | "
                "tuple[int, int, list[int]]]]"
            )
        )
