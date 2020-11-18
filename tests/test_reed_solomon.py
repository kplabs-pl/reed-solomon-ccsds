import pytest
from reed_solomon_ccsds import UncorrectableError, decode, encode

GOOD_BLOCK = bytes([
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,
    0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f,
    0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
    0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f,
    0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f,
    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f,
    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
    0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f,
    0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf,
    0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf,
    0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf,
    0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xdb, 0xdc, 0xdd, 0xde, 0x2f,
    0xbd, 0x4f, 0xb4, 0x74, 0x84, 0x94, 0xb9, 0xac, 0xd5, 0x54, 0x62, 0x72, 0x12, 0xee, 0xb3, 0xeb,
    0xed, 0x41, 0x19, 0x1d, 0xe1, 0xd3, 0x63, 0x20, 0xea, 0x49, 0x29, 0x0b, 0x25, 0xab, 0xcf
])  # yapf: disable

GOOD_BLOCK_DUAL_BASIS = bytes([
    0x00, 0x07, 0x0e, 0x15, 0x1c, 0x23, 0x2a, 0x31, 0x37, 0x3e, 0x44, 0x4a, 0x50, 0x55, 0x5a, 0x5f,
    0x64, 0x68, 0x6c, 0x70, 0x73, 0x76, 0x79, 0x7b, 0x7c, 0x7e, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7e,
    0x7c, 0x7a, 0x78, 0x75, 0x72, 0x6f, 0x6b, 0x67, 0x63, 0x5e, 0x59, 0x54, 0x4e, 0x48, 0x42, 0x3c,
    0x36, 0x2f, 0x28, 0x21, 0x1a, 0x13, 0x0c, 0x05, 0xfe, 0xf6, 0xef, 0xe8, 0xe1, 0xda, 0xd3, 0xcd,
    0xc6, 0xc0, 0xba, 0xb4, 0xae, 0xa9, 0xa3, 0x9f, 0x9a, 0x96, 0x92, 0x8e, 0x8b, 0x88, 0x86, 0x84,
    0x82, 0x81, 0x80, 0x80, 0x80, 0x80, 0x81, 0x82, 0x83, 0x85, 0x88, 0x8a, 0x8d, 0x91, 0x95, 0x99,
    0x9d, 0xa2, 0xa7, 0xad, 0xb2, 0xb8, 0xbe, 0xc5, 0xcb, 0xd2, 0xd8, 0xdf, 0xe6, 0xee, 0xf5, 0xfc,
    0x03, 0x0a, 0x11, 0x19, 0x20, 0x27, 0x2d, 0x34, 0x3a, 0x41, 0x47, 0x4d, 0x52, 0x58, 0x5d, 0x62,
    0x66, 0x6a, 0x6e, 0x72, 0x75, 0x77, 0x7a, 0x7c, 0x7d, 0x7e, 0x7f, 0x7f, 0x7f, 0x7f, 0x7e, 0x7d,
    0x7b, 0x79, 0x77, 0x74, 0x71, 0x6d, 0x69, 0x65, 0x60, 0x5c, 0x56, 0x51, 0x4b, 0x45, 0x3f, 0x39,
    0x32, 0x2c, 0x25, 0x1e, 0x17, 0x10, 0x09, 0x01, 0xfa, 0xf3, 0xec, 0xe5, 0xde, 0xd7, 0xd0, 0xc9,
    0xc3, 0xbd, 0xb7, 0xb1, 0xab, 0xa6, 0xa1, 0x9c, 0x98, 0x94, 0x90, 0x8d, 0x8a, 0x87, 0x85, 0x83,
    0x81, 0x80, 0x80, 0x80, 0x80, 0x80, 0x81, 0x83, 0x84, 0x86, 0x89, 0x8c, 0x8f, 0x93, 0x97, 0x9b,
    0xa0, 0xa5, 0xaa, 0xaf, 0xb5, 0xbb, 0xc1, 0xc8, 0xce, 0xd5, 0xdc, 0xe3, 0xea, 0xf1, 0xf8, 0x42,
    0x8d, 0xff, 0xb3, 0x44, 0xbe, 0x5f, 0x28, 0x6d, 0xb8, 0x66, 0xa3, 0x51, 0xfb, 0xb6, 0xff, 0xf4,
    0x76, 0x6e, 0x2b, 0x80, 0x80, 0x64, 0x86, 0x2e, 0x87, 0xac, 0xe4, 0xf8, 0x63, 0x19, 0x51
])  # yapf: disable


def test_encode() -> None:
    data = GOOD_BLOCK[0:223]
    encoded = encode(data, dual_basis=False)
    assert encoded == GOOD_BLOCK


def test_decode() -> None:
    data = bytearray()
    data.extend(GOOD_BLOCK)
    mask = [
        0x58, 0x00, 0xA3, 0x00, 0x00, 0xCD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xCA, 0x96, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA2, 0x00, 0xAC, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0xB9, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0xE5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x94, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x97, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x29, 0x00, 0x00, 0x00, 0x00
    ]  # yapf: disable

    for i in range(len(data)):
        data[i] ^= mask[i]

    nr_of_corrections, decoded = decode(data, dual_basis=False)
    assert nr_of_corrections == [16]
    assert decoded == GOOD_BLOCK[:223]


def test_dual_basis() -> None:
    encoded = bytearray()
    encoded.extend(encode(GOOD_BLOCK_DUAL_BASIS[0:223], True))
    assert encoded == GOOD_BLOCK_DUAL_BASIS

    encoded[0] = 19
    encoded[8] = 10
    encoded[45] = 0
    encoded[76] = 54
    encoded[117] = 0xFF
    corrections, decoded = decode(encoded, True)
    assert corrections == [5]
    assert decoded == GOOD_BLOCK_DUAL_BASIS[:223]


def test_data_modification() -> None:
    data = bytearray(GOOD_BLOCK[:223])
    data[5] = 0xAA
    data[7] = 0xAA
    data[15] = 0xAA
    data[50] = 0xAA
    expected = bytes(data)
    encode(data, False)
    assert data == expected


def test_interleaving_constants() -> None:
    d = [0, 0xFF, 0xDE, 0xAD] * 223
    encoded = bytearray()
    encoded.extend(encode(bytes(d), dual_basis=False, interleaving=4))

    assert len(encoded) == 255 * 4
    assert encoded == bytes(255 * [0, 0xFF, 0xDE, 0xAD])

    bytes_to_modify = [
        274, 934, 366, 137, 897, 710, 815, 318, 580, 497, 953, 816, 211, 331, 15, 315, 337, 775, 27, 721, 24, 963,
        293, 620, 645, 814, 805, 475, 892, 729, 830, 869, 705, 149, 584, 623, 724, 983, 189, 279,
        361, 687, 783, 226, 250, 306, 232, 661, 897, 988, 846, 927, 563, 242, 58
    ]  # yapf: disable

    for i in bytes_to_modify:
        encoded[i] = 0xAA

    for dual_basis in [False, True]:
        stats, data = decode(encoded, dual_basis=dual_basis, interleaving=4)
        assert stats == [9, 16, 13, 16]
        for i in range(223):
            assert data[4 * i + 0] == 0
            assert data[4 * i + 2] == 0xDE
            assert data[4 * i + 3] == 0xAD


def test_uncorrectable_error() -> None:
    encoded = bytearray()
    encoded.extend(encode(GOOD_BLOCK[0:223], False))

    bytes_to_modify = [
        14, 28, 39, 50, 63, 78, 91, 114, 115, 116, 145, 156, 169, 192, 197, 200, 223
    ]  # yapf: disable

    for index in bytes_to_modify:
        encoded[index] ^= index

    with pytest.raises(UncorrectableError):
        decode(encoded, dual_basis=False)


def test_interleaving_frames() -> None:
    data = []
    for i in range(223):
        data.append(GOOD_BLOCK_DUAL_BASIS[i])
        data.append(0xAA)
        data.append(GOOD_BLOCK_DUAL_BASIS[i])
        data.append(0x0F)
        data.append(0xEA)

    encoded = encode(bytes(data), dual_basis=True, interleaving=5)
    for i in range(0, 225 * 5, 5):
        assert encoded[i] == GOOD_BLOCK_DUAL_BASIS[i // 5]
        assert encoded[i + 1] == 0xAA
        assert encoded[i + 2] == GOOD_BLOCK_DUAL_BASIS[i // 5]
        assert encoded[i + 3] == 0x0F
        assert encoded[i + 4] == 0xEA
