# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import btc, messages as proto
from trezorlib.tools import parse_path

from ..tx_cache import TxCache
from .signtx import (
    request_extra_data,
    request_finished,
    request_input,
    request_meta,
    request_output,
)

B = proto.ButtonRequestType
TX_API = TxCache("Komodo")

# test signing VOTE2020 transaction
# https://vote2020.explorer.dexstats.info/insight-api-komodo/tx/3f530ae01546fe36c9314b247c3a1d24664e0f81332cfaa7324a545a6a144230
TXHASH_3f53 = bytes.fromhex(
    "3f530ae01546fe36c9314b247c3a1d24664e0f81332cfaa7324a545a6a144230"
)


@pytest.mark.altcoin
@pytest.mark.komodo
class TestMsgSigntxKomodoSC:
    def test_one_one_vote2020(self, client):
        inp1 = proto.TxInputType(
            # R9HgJZo6JBKmPvhm7whLSR8wiHyZrEDVRi
            address_n=parse_path("44'/141'/0'/0/8"),
            amount=3156850732,
            prev_hash=TXHASH_3f53,
            prev_index=3,
        )

        out1 = proto.TxOutputType(
            address="R9HgJZo6JBKmPvhm7whLSR8wiHyZrEDVRi",
            amount=100000000,
            script_type=proto.OutputScriptType.PAYTOADDRESS,
        )

        trezor_core = client.features.model != "1"
        with client:
            client.set_expected_responses(
                [
                    request_input(0),
                    request_meta(TXHASH_3f53),
                    request_input(0, TXHASH_3f53),
                    request_output(0, TXHASH_3f53),
                    request_output(1, TXHASH_3f53),
                    request_output(2, TXHASH_3f53),
                    request_output(3, TXHASH_3f53),
                    request_output(4, TXHASH_3f53),
                    request_output(5, TXHASH_3f53),
                    request_output(6, TXHASH_3f53),
                    request_output(7, TXHASH_3f53),
                    request_output(8, TXHASH_3f53),
                    request_output(9, TXHASH_3f53),
                    request_output(10, TXHASH_3f53),
                    request_extra_data(0, 11, TXHASH_3f53),
                    request_output(0),
                    proto.ButtonRequest(code=B.ConfirmOutput),
                    (trezor_core, proto.ButtonRequest(code=B.SignTx)),
                    proto.ButtonRequest(code=B.SignTx),
                    request_input(0),
                    request_output(0),
                    request_finished(),
                ]
            )

            details = proto.SignTx(
                version=4,
                version_group_id=0x892F2085,
                branch_id=0x76B809BB,
                lock_time=0,
            )
            _, serialized_tx = btc.sign_tx(
                client, "Komodo", [inp1], [out1], details=details, prev_txes=TX_API
            )

        assert (
            serialized_tx.hex()
            == "0400008085202f89011d0f8e0c6ba2dcf8be8e5f9024771dceb4c8e4120fab8c072b8eec26b1c50728000000006a4730440220158c970ca2fc6bcc33026eb5366f0342f63b35d178f7efb334b1df78fe90b67202207bc4ff69f67cf843b08564a5adc77bf5593e28ab4d5104911824ac13fe885d8f012102a87aef7b1a8f676e452d6240767699719cd58b0261c822472c25df146938bca5ffffffff01d0359041000000001976a91400178fa0b6fc253a3a402ee2cadd8a7bfec08f6388acb8302a5d000000000000000000000000000000"
        )