import ubinascii
import sys


from cbor.tagmap import ClassTag, TagMapper, Tag, UnknownTagException

from cbor.tests.test_cbor import hexstr


class SomeType(object):
    "target type for translator tests"
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def to_cbor(ob):
        assert isinstance(ob, SomeType)
        return (ob.a, ob.b)

    @staticmethod
    def from_cbor(data):
        return SomeType(*data)

    def __eq__(self, other):
        # why isn't this just the default implementation in the object class?
        return isinstance(other, type(self)) and (self.__dict__ == other.__dict__)


class UnknownType(object):
    pass


known_tags = [
    ClassTag(4325, SomeType, SomeType.to_cbor, SomeType.from_cbor)
]


class TestObjects():
    def __init__(self):
        self.tx = TagMapper(known_tags)

    def _oso(self, ob):
        ser = self.tx.dumps(ob)
        try:
            o2 = self.tx.loads(ser)
            assert ob == o2, '%r != %r from %s' % (ob, o2, ubinascii.hexlify(ser))
        except Exception as e:
            print('failure on buf len={0} {1!r} ob={2!r} {3!r}; {4}\n'.format(len(ser), hexstr(ser), ob, ser, e))
            raise

    def test_basic(self):
        self._oso(SomeType(1,2))

    def test_unk_fail(self):
        ok = False
        try:
            self.tx.dumps(UnknownType())
        except:
            ok = True
        assert ok

    def test_tag_passthrough(self):
        self.tx.raise_on_unknown_tag = False
        self._oso(Tag(1234, 'aoeu'))

    def test_unk_tag_fail(self):
        ok = False
        self.tx.raise_on_unknown_tag = True
        try:
            self._oso(Tag(1234, 'aoeu'))
        except UnknownTagException as ute:
            ok = True
        assert ok


if __name__ == '__main__':
    unit_test = TestObjects()

    try:
        unit_test.test_basic()
        print('test_basic(): OK.')
    except:
        print('test_basic(): NOK.')

    try:
        unit_test.test_unk_fail()
        print('test_unk_fail(): OK.')
    except:
        print('test_unk_fail(): NOK.')

    try:
        unit_test.test_tag_passthrough()
        print('test_tag_passthrough(): OK.')
    except:
        print('test_tag_passthrough(): NOK.')

    try:
        unit_test.test_unk_tag_fail()
        print('test_unk_tag_fail(): OK.')
    except:
        print('test_unk_tag_fail(): NOK.')
