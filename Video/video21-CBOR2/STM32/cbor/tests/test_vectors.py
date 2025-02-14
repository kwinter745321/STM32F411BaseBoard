#!/usr/bin/env python

"""
Test CBOR implementation against common "test vectors" set from
https://github.com/cbor/test-vectors/
"""

import ubinascii
import ujson
import math
import uos






from cbor.cbor import loads
from cbor import Tag


# Accomodate several test vectors that have diagnostic descriptors but not JSON
_DIAGNOSTIC_TESTS = {
    'Infinity': lambda x: x == float('Inf'),
    '-Infinity': lambda x: x == float('-Inf'),
    'NaN': math.isnan,
    'undefined': lambda x: x is None,

    '0("2013-03-21T20:04:00Z")': lambda x: isinstance(x, Tag) and (x.tag == 0) and (x.value == '2013-03-21T20:04:00Z'),

    "h''": lambda x: x == b'',
    "(_ h'0102', h'030405')": lambda x: x == b'\x01\x02\x03\x04\x05',
    '{1: 2, 3: 4}': lambda x: x == {1: 2, 3: 4},
    "h'01020304'": lambda x: x == b'\x01\x02\x03\x04',
}


# We expect these to raise exception because they encode reserved/unused codes in the spec.
# ['hex'] values of tests we expect to raise
_EXPECT_EXCEPTION = set(['f0', 'f818', 'f8ff'])


def _check(row, decoded):
    anyerr = False
    cbdata = ubinascii.a2b_base64(row['cbor'])
    cb = loads(cbdata)
    if cb != decoded:
        anyerr = True
        print('Expected {0!r} got {1!r}. Failed to decode CBOR {2}.\n'.format(cb, decoded, ubinascii.hexlify(cbdata)))

    return anyerr


def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    """Reimplementation of math.isclose() as it does not exist in Micropython."""
    return abs(a-b) <= max( rel_tol * max(abs(a), abs(b)), abs_tol )


def _check_float(row, decoded):
    anyerr = False
    cbdata = ubinascii.a2b_base64(row['cbor'])
    cb = loads(cbdata)
    if not isclose(cb, decoded):
        anyerr = True
        print('Expected {0!r} got {1!r}. Failed to decode CBOR {2}.\n'.format(cb, decoded, ubinascii.hexlify(cbdata)))

    return anyerr


def _check_foo(row, checkf):
    anyerr = False
    cbdata = ubinascii.a2b_base64(row['cbor'])
    cb = loads(cbdata)
    if not checkf(cb):
        anyerr = True
        print('Expected {0!r} got {1!r}. Failed to decode CBOR {2}.\n'.format(cb, checkf, ubinascii.hexlify(cbdata)))

    return anyerr


class TestVectors():
        def test_vectors(self):
            jf = 'test-vectors/appendix_a.json'

            try:
                testfile = open(jf, 'r')
            except:
                print('Error: cannot open ' + jf + '.')
                raise

            try:
                tv = ujson.load(testfile)
            except:
                print('Error: cannot load ' + jf + ' using ujson.load().')
                raise

            anyerr = False
            for row in tv:
                rhex = row.get('hex')
                if 'decoded' in row:
                    decoded = row['decoded']

                    if(type(decoded) is float):
                        status = _check_float(row, decoded)
                    else:
                        status = _check(row, decoded)
                    if(status):
                        anyerr = True
                    continue
                elif 'diagnostic' in row:
                    diag = row['diagnostic']
                    checkf = _DIAGNOSTIC_TESTS.get(diag)
                    if checkf is not None:
                        status = _check_foo(row, checkf)
                        if(status):
                            anyerr = True
                        continue

                # variously verbose log of what we're not testing:
                cbdata = ubinascii.a2b_base64(row['cbor'])
                try:
                    pd = loads(cbdata)
                except:
                    if rhex and (rhex in _EXPECT_EXCEPTION):
                        pass
                    else:
                        print('Failed to load hex=' + str(rhex) + ' diag=' + str(row.get('diagnostic') + '.'))
                    pd = ''
                cd = None
                print('Skipping hex=' + str(rhex) + ' diag=' + str(row.get('diagnostic')) + ' py=' + str(pd) + ' c=' + str(cd) + '.')

            testfile.close()

            assert not anyerr


if __name__ == '__main__':
    unit_test = TestVectors()

    try:
        unit_test.test_vectors()
        print('test_vectors(): OK.')
    except Exception as e:
        print(e)
        print('test_vectors(): NOK.')
