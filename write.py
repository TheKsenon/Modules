#-------------------------------------------------------------------
# This module was created by XenonModules
# Telegram: @officialksenon
# Commands:
# .write
#-------------------------------------------------------------------
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class writeMod(loader.Module):
    """Writes a message one letter at a time. @XenonModules"""

    strings = {
        "name": "Write",
        "no_message": "<b>.write TEXT</b>",
        "delay_typer_cfg_doc": "Time to write:",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "DELAY_WRITE", 0.03, lambda m: self.strings("delay_write_cfg_doc", m)
        )

    @loader.ratelimit
    async def writecmd(self, message):
        """.write TEXT"""
        a = utils.get_args_raw(message)
        if not a:
            await utils.answer(message, self.strings("no_message", message))
            return
        text = ""
        for c in a:
            text += c
            await utils.answer(message, f"⁠⁠⁠⁠⁠ {text} ⁠⁠⁠⁠⁠")
            await asyncio.sleep(0.3)
