import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    Defaults,
)
from telegram.constants import ParseMode

from config import BOT_TOKEN
# 【修复1】这里原来是 from database import ... 改正为 database_mysql
from database_mysql import Database 
from handlers.user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
    checkin_command,
    invite_command,
    use_command,
)
from handlers.verify_commands import (
    verify_command,
    verify2_command,
    # 【修复2】删除了 verify3_command，因为它不存在
    verify4_command,
    getV4Code_command,
)
from handlers.admin_commands import (
    addbalance_command,
    block_command,
    white_command,
    blacklist_command,
    genkey_command,
    listkeys_command,
    broadcast_command,
)

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """全局错误处理"""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """启动机器人"""
    # 初始化数据库
    db = Database()
    
    # 创建应用
    defaults = Defaults(parse_mode=ParseMode.HTML)
    application = Application.builder().token(BOT_TOKEN).defaults(defaults).build()

    # 注册错误处理器
    application.add_error_handler(error_handler)

    # --- 注册用户命令 ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("qd", checkin_command))     # 签到
    application.add_handler(CommandHandler("invite", invite_command))  # 邀请
    application.add_handler(CommandHandler("use", use_command))        # 使用卡密

    # --- 注册验证命令 ---
    application.add_handler(CommandHandler("verify", verify_command))   # Gemini
    application.add_handler(CommandHandler("verify2", verify2_command)) # K12
    # 【修复2】verify3 已被删除，这里不要注册
    application.add_handler(CommandHandler("verify4", verify4_command)) # Bolt
    application.add_handler(CommandHandler("getV4Code", getV4Code_command))

    # --- 注册管理员命令 ---
    application.add_handler(CommandHandler("addbalance", addbalance_command))
    application.add_handler(CommandHandler("block", block_command))
    application.add_handler(CommandHandler("white", white_command))
    application.add_handler(CommandHandler("blacklist", blacklist_command))
    application.add_handler(CommandHandler("genkey", genkey_command))
    application.add_handler(CommandHandler("listkeys", listkeys_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))

    # 启动
    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
