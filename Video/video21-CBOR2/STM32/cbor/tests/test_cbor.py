#!python
# -*- coding: utf-8 -*-

import ubinascii



from cbor.cbor import dumps
from cbor.cbor import loads
from cbor.cbor import dump
from cbor.cbor import load
from cbor.cbor import Tag

_range = range
from uio import BytesIO as StringIO

def hexstr(bs):
    return ' '.join(map(lambda x: '{0:02x}'.format(x), bs))


class XTestCBOR(object):
    def _oso(self, ob):
        ser = dumps(ob)
        try:
            o2 = loads(ser)
            assert ob == o2, '%r != %r from %s' % (ob, o2, ubinascii.hexlify(ser))
        except Exception as e:
            print('failure on buf len={0} {1!r} ob={2!r} {3!r}; {4}\n'.format(len(ser), hexstr(ser), ob, ser, e))
            raise

    def _osos(self, ob):
        obs = dumps(ob)
        o2 = loads(obs)
        o2s = dumps(o2)
        assert obs == o2s

    def _oso_bytearray(self, ob):
        ser = dumps(ob)
        try:
            o2 = loads(bytearray(ser))
            assert ob == o2, '%r != %r from %s' % (ob, o2, ubinascii.hexlify(ser))
        except Exception as e:
            print('failure on buf len={0} {1!r} ob={2!r} {3!r}; {4}\n'.format(len(ser), hexstr(ser), ob, ser, e))
            raise

    test_objects = [
        1,
        0,
        True,
        False,
        None,
        -1,
        -1.5,
        1.5,
        1000,
        -1000,
        1000000000,
        2376030000,
        -1000000000,
        1000000000000000,
        -1000000000000000,
        [],
        [1,2,3],
        {},
        b'aoeu1234\x00\xff',
        u'åöéûのかめ亀',
        b'',
        u'',
        Tag(1234, 'aoeu'),
    ]

    def test_basic(self):
        for ob in self.test_objects:
            self._oso(ob)

    def test_basic_bytearray(self):
        xoso = self._oso
        self._oso = self._oso_bytearray
        try:
            self.test_basic()
        finally:
            self._oso = xoso

    def test_random_ints(self):
        #v = random.randint(-4294967295, 0xffffffff)
        v = 4009372298
        self._oso(v)

        #v = random.randint(-1000000000000000000000, 1000000000000000000000)
        v = -3875820019684212735
        self._oso(v)

    def test_tuple(self):
        l = [1,2,3]
        t = tuple(l)
        ser = dumps(t)
        o2 = loads(ser)
        assert l == o2

    def test_loads_none(self):
        try:
            loads(None)
            assert False, "expected ValueError when passing in None"
        except ValueError:
            pass

    def test_concat(self):
        "Test that we can concatenate output and retrieve the objects back out."
        self._oso(self.test_objects)
        fob = StringIO()

        for ob in self.test_objects:
            dump(ob, fob)
        fob.seek(0)
        obs2 = []
        try:
            while True:
                obs2.append(load(fob))
        except EOFError:
            pass
        assert obs2 == self.test_objects

    # TODO: find more bad strings with which to fuzz CBOR
    def test_badread(self):
        try:
            loads(b'\xff')
            assert False, 'badread should have failed'
        except ValueError as ve:
            #logger.info('error', exc_info=True)
            pass
        except Exception as ex:
            print('unexpected error!', exc_info=True)
            assert False, 'unexpected error' + str(ex)

    def test_datetime(self):
        # right now we're just testing that it's possible to dumps()
        # Tag(0,...) because there was a bug around that.
        dumps(Tag(0, '1984-01-24T23:22:21'))

    def test_sortkeys(self):
        obytes = []
        xbytes = []
        for n in _range(2, 27):
            ob = {u'{:02x}'.format(x):x for x in _range(n)}
            obytes.append(dumps(ob, sort_keys=True))
            xbytes.append(dumps(ob, sort_keys=False))
        allOGood = True
        someXMiss = False
        for i, g in enumerate(_GOLDEN_SORTED_KEYS_BYTES):
            if g != obytes[i]:
                print('bad sorted result, wanted %r got %r', g, obytes[i])
                allOGood = False
            if g != xbytes[i]:
                someXMiss = True

        assert allOGood
        assert someXMiss


_GOLDEN_SORTED_KEYS_BYTES = [
b'\xa2b00\x00b01\x01',
b'\xa3b00\x00b01\x01b02\x02',
b'\xa4b00\x00b01\x01b02\x02b03\x03',
b'\xa5b00\x00b01\x01b02\x02b03\x03b04\x04',
b'\xa6b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05',
b'\xa7b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06',
b'\xa8b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07',
b'\xa9b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08',
b'\xaab00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\t',
b'\xabb00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\n',
b'\xacb00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0b',
b'\xadb00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0c',
b'\xaeb00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\r',
b'\xafb00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0e',
b'\xb0b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0f',
b'\xb1b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10',
b'\xb2b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11',
b'\xb3b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12',
b'\xb4b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13',
b'\xb5b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14',
b'\xb6b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14b15\x15',
b'\xb7b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14b15\x15b16\x16',
b'\xb8\x18b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14b15\x15b16\x16b17\x17',
b'\xb8\x19b00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14b15\x15b16\x16b17\x17b18\x18\x18',
b'\xb8\x1ab00\x00b01\x01b02\x02b03\x03b04\x04b05\x05b06\x06b07\x07b08\x08b09\tb0a\nb0b\x0bb0c\x0cb0d\rb0e\x0eb0f\x0fb10\x10b11\x11b12\x12b13\x13b14\x14b15\x15b16\x16b17\x17b18\x18\x18b19\x18\x19',
]


if __name__ == '__main__':
    unit_test = XTestCBOR()

    try:
        unit_test.test_basic()
        print('test_basic(): OK.')
    except:
        print('test_basic(): NOK.')

    try:
        unit_test.test_basic_bytearray()
        print('test_basic_bytearray(): OK.')
    except:
        print('test_basic_bytearray(): NOK.')

    try:
        unit_test.test_random_ints()
        print('test_random_ints(): OK.')
    except:
        print('test_random_ints(): NOK.')

    try:
        unit_test.test_tuple()
        print('test_tuple(): OK.')
    except:
        print('test_tuple(): NOK.')

    try:
        unit_test.test_loads_none()
        print('test_loads_none(): OK.')
    except:
        print('test_loads_none(): NOK.')

    try:
        unit_test.test_concat()
        print('test_concat(): OK.')
    except:
        print('test_concat(): NOK.')

    try:
        unit_test.test_badread()
        print('test_badread(): OK.')
    except:
        print('test_badread(): NOK.')

    try:
        unit_test.test_datetime()
        print('test_datetime(): OK.')
    except:
        print('test_datetime(): NOK.')

    try:
        unit_test.test_sortkeys()
        print('test_sortkeys(): OK.')
    except:
        print('test_sortkeys(): NOK.')
