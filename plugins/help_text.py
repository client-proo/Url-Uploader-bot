#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3

# تنظیمات
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup


# --- دستور /help ---
@pyrogram.Client.on_message(filters.command(["help"]) & filters.private)
async def help_user(client, message: Message):
    if message.from_user.id in Config.AUTH_USERS:
        await message.reply_text(
            text=Translation.HELP_USER,
            parse_mode="html",
            disable_web_page_preview=True
        )


# --- دستور /start ---
@pyrogram.Client.on_message(filters.command(["start"]) & filters.private)
async def start(client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # کیبورد مشترک برای کاربران مجاز
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡️𝔖𝔲𝔭𝔭𝔬𝔯𝔱", url="https://t.me/LazyPrincessSupport"),
                InlineKeyboardButton("✪ ＹＴ ✪", url="https://youtube.com/@LazyDeveloperr"),
                InlineKeyboardButton("⚡️ U𝖕𝖉𝖆𝖙e", url="https://t.me/LazyDeveloper"),
            ],
            [InlineKeyboardButton("⭑💢 𝚂 𝙾 𝙲 𝚒 𝙰 𝙻 💢⭑", url="https://instagram.com/LazyDeveloper__")],
            [InlineKeyboardButton("🦋 ⭑┗━━┫⦀⦙ O W N E R ⦙⦀┣━━┛⭑ 🦋", url="https://t.me/LazyDeveloperr")],
        ]
    )

    # برای Lazy Developer
    if user_id in (Config.AUTH_USERS & getattr(Config, "LAZY_DEVELOPER", set())):
        text = Translation.LAZY_DEVELOPER_TEXT.format(first_name)
        await message.reply_text(text, reply_markup=keyboard)

    # برای کاربران مجاز
    elif user_id in Config.AUTH_USERS:
        text = Translation.START_TEXT.format(first_name)
        await message.reply_text(text, reply_markup=keyboard)

    # برای بقیه کاربران
    else:
        text = Translation.LAZY_START_TEXT.format(first_name)
        restricted_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🦋 ⭑┗━━┫⦀⦙ O W N E R ⦙⦀┣━━┛⭑ 🦋", url="https://t.me/LazyDeveloperr")],
                [InlineKeyboardButton("▍║▍▏║ UPDATE ║▍▏║▍", url="https://t.me/LazyPrincessSupport")],
                [InlineKeyboardButton("⭑💢 𝚂 𝙾 𝙲 𝚒 𝙰 𝙻 💢⭑", url="https://instagram.com/LazyDeveloper__")],
            ]
        )
        await message.reply_text(text, reply_markup=restricted_keyboard)