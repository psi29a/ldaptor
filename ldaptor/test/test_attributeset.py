"""
Test cases for ldaptor.attributeset
"""

from twisted.trial import unittest
from ldaptor import attributeset


class TestComparison(unittest.TestCase):
    def testEquality_True_Set(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        self.assertEqual(a, b)

    def testEquality_True_Set_Ordering(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'd', 'c'])
        self.assertEqual(a, b)

    def testEquality_True_List(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = ['b', 'c', 'd']
        self.assertEqual(a, b)

    def testEquality_True_List_Ordering(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = ['b', 'd', 'c']
        self.assertEqual(a, b)

    def testEquality_False_Value(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'e'])
        self.assertNotEqual(a, b)

    def testEquality_False_Key(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('l', ['b', 'c', 'd'])
        self.assertNotEqual(a, b)


class TestSetOperations(unittest.TestCase):
    def testDifference(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'e'])
        self.assertEqual(a - b, {'d'})

    def testUnion(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'e'])
        self.assertEqual(a | b, {'b', 'c', 'd', 'e'})

    def testIntersection(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'e'])
        self.assertEqual(a & b, {'b', 'c'})

    def testSymmetricDifference(self):
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd'])
        b = attributeset.LDAPAttributeSet('k', ['b', 'c', 'e'])
        self.assertEqual(a ^ b, {'d', 'e'})

    def testCopy(self):
        class Magic:
            def __lt__(self, other):
                return False

            def __gt__(self, other):
                return True

        m1 = Magic()
        a = attributeset.LDAPAttributeSet('k', ['b', 'c', 'd', m1])
        b = a.__copy__()
        self.assertEqual(a, b)
        self.assertNotIdentical(a, b)

        magicFromA = [val for val in a if isinstance(val, Magic)][0]
        magicFromB = [val for val in b if isinstance(val, Magic)][0]
        self.assertEqual(magicFromA, magicFromB)
        self.assertIdentical(magicFromA, magicFromB)

        a.update('x')
        self.assertEqual(a, {'b', 'c', 'd', m1, 'x'})
        self.assertEqual(b, {'b', 'c', 'd', m1})

    def testDeepCopy(self):
        class Magic:
            def __eq__(self, other):
                return isinstance(other, self.__class__)

            def __hash__(self):
                return 42

            def __lt__(self, other):
                return False

            def __gt__(self, other):
                return True

        m1 = Magic()
        a = attributeset.LDAPAttributeSet('k', ['a', m1])
        b = a.__deepcopy__({})
        self.assertEqual(a, b)
        self.assertNotIdentical(a, b)

        magicFromA = [val for val in a if isinstance(val, Magic)][0]
        magicFromB = [val for val in b if isinstance(val, Magic)][0]
        self.assertEqual(magicFromA, magicFromB)
        self.assertNotIdentical(magicFromA, magicFromB)

        a.update('x')
        self.assertEqual(a, {'a', m1, 'x'})
        self.assertEqual(b, {'a', m1})
