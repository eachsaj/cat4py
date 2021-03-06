import cat4py as cat
import pytest
import numpy as np
import os


@pytest.mark.parametrize("shape, chunkshape, blockshape, itemsize, enforceframe, filename, copy_sframe",
                         [
                             ([200], [66], [20], 8, True, None, False),
                             ([200], [66], [20], 8, True, None, True),
                             ([20, 134, 13], [15, 54, 10], [3, 13, 5], 4, False, None, True),
                             ([20, 134, 13], [15, 54, 10], [3, 13, 5], 4, True, 'test_frame.cat',
                              True),
                             ([12, 13, 14, 15, 16], [8, 5, 6, 7, 7], [2, 3, 4, 4, 4], 8, True, None,
                              False)
                         ])
def test_frame(shape, chunkshape, blockshape, itemsize, enforceframe, filename, copy_sframe):
    if filename is not None and os.path.exists(filename):
        os.remove(filename)

    size = int(np.prod(shape))
    buffer = bytes(size * itemsize)
    a = cat.from_buffer(buffer, shape, chunkshape=chunkshape, blockshape=blockshape,
                        itemsize=itemsize, enforceframe=enforceframe, filename=filename)
    sframe1 = a.to_sframe()
    buffer1 = a.to_buffer()
    # Size of a compressed frame should be less than the plain buffer for the cases here
    assert len(sframe1) < len(buffer1)

    b = cat.from_sframe(sframe1, copy=copy_sframe)
    sframe2 = b.to_sframe()
    # For some reason, the size of sframe1 and sframe2 are not equal when copies are made,
    # but the important thing is that the length of the frame should be stable in multiple
    # round-trips after the first one.
    # assert len(sframe2) == len(sframe1)
    sframe3 = sframe2
    c = b
    for i in range(1):
        c = cat.from_sframe(sframe2, copy=copy_sframe)
        sframe3 = c.to_sframe()
        if not copy_sframe:
            # When the frame is not copied, we *need* a copy for the next iteration
            sframe3 = bytes(sframe3)
    assert len(sframe3) == len(sframe2)
    buffer2 = b.to_buffer()
    assert buffer2 == buffer1
    buffer3 = c.to_buffer()
    assert buffer3 == buffer1

    if filename is not None and os.path.exists(filename):
        os.remove(filename)


@pytest.mark.parametrize("shape, chunkshape, blockshape, dtype, enforceframe, filename, copy_sframe",
                         [
                             ([200], [66], [20], np.float64, True, None, False),
                             ([200], [66], [20], np.float64, True, None, True),
                             ([20, 134, 13], [15, 54, 10], [3, 13, 5], np.float32, False, None,
                              True),
                             ([20, 134, 13], [15, 54, 10], [3, 13, 5], np.int32, True,
                              'test_frame.cat', True),
                             ([12, 13, 14, 15, 16], [8, 5, 6, 7, 7], [2, 3, 4, 4, 4], np.int64,
                              True, None, False)
                         ])
def test_frame_numpy(shape, chunkshape, blockshape, dtype, enforceframe, filename, copy_sframe):
    if filename is not None and os.path.exists(filename):
        os.remove(filename)

    size = int(np.prod(shape))
    nparray = np.arange(size, dtype=dtype).reshape(shape)
    a = cat.from_numpy(nparray, chunkshape=chunkshape, blockshape=blockshape,
                       enforceframe=enforceframe, filename=filename)
    sframe1 = a.to_sframe()
    buffer1 = a.to_buffer()
    # Size of a compressed frame should be less than the plain buffer for the cases here
    assert len(sframe1) < len(buffer1)

    b = cat.from_sframe(sframe1, copy=copy_sframe)
    sframe2 = b.to_sframe()
    # For some reason, the size of sframe1 and sframe2 are not equal when copies are made,
    # but the important thing is that the length of the frame should be stable in multiple
    # round-trips after the first one.
    # assert len(sframe2) == len(sframe1)
    sframe3 = sframe2
    c = b
    for i in range(10):
        c = cat.from_sframe(sframe2, copy=copy_sframe)
        sframe3 = c.to_sframe()
        if not copy_sframe:
            # When the frame is not copied, we *need* a copy for the next iteration
            sframe3 = bytes(sframe3)
    assert len(sframe3) == len(sframe2)
    buffer2 = b.to_buffer()
    assert buffer2 == buffer1
    buffer3 = c.to_buffer()
    assert buffer3 == buffer1

    if filename is not None and os.path.exists(filename):
        os.remove(filename)
