from trezor import wire
from trezor.messages import OntologyAsset
from trezor.messages.OntologySignedTransfer import OntologySignedTransfer
from trezor.messages.OntologySignTransfer import OntologySignTransfer
from trezor.messages.OntologyTransaction import OntologyTransaction
from trezor.messages.OntologyTransfer import OntologyTransfer

from .helpers import CURVE, validate_full_path
from .layout import require_confirm_transfer_ong, require_confirm_transfer_ont
from .serialize import serialize_transfer
from .sign import sign

from apps.common import paths


async def sign_transfer(ctx, msg: OntologySignTransfer, keychain):
    await paths.validate_path(ctx, validate_full_path, keychain, msg.address_n, CURVE)
    await _require_confirm(ctx, msg.transaction, msg.transfer)

    node = keychain.derive(msg.address_n, CURVE)
    [raw_data, payload] = serialize_transfer(msg.transaction, msg.transfer)
    signature = await sign(raw_data, node.private_key())

    return OntologySignedTransfer(signature=signature, payload=payload)


async def _require_confirm(
    ctx, transaction: OntologyTransaction, transfer: OntologyTransfer
):
    if transaction.type == 0xD1:
        if transfer.asset == OntologyAsset.ONT:
            return await require_confirm_transfer_ont(
                ctx, transfer.to_address, transfer.amount
            )
        if transfer.asset == OntologyAsset.ONG:
            return await require_confirm_transfer_ong(
                ctx, transfer.to_address, transfer.amount
            )

    raise wire.DataError("Invalid transaction type")
