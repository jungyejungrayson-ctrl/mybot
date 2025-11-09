import os
import discord
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# OpenAI 클라이언트 초기화
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Discord 봇 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 봇이 켜질 때 실행
@bot.event
async def on_ready():
    print(f"✅ 로그인 성공: {bot.user}")

# 명령어: !ask
@bot.command(name="ask")
async def ask(ctx, *, question: str = None):
    if not question:
        await ctx.reply("질문을 입력해주세요. 예: `!ask 오늘 날씨 어때?`")
        return

    # 사용자에게 응답 준비 메시지
    msg = await ctx.reply("🤖 생성형 AI에게 물어보는 중이에요...")

    try:
        # OpenAI에 요청
        response = client_ai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply in Korean when possible."},
                {"role": "user", "content": question},
            ],
            temperature=0.2,
            max_tokens=800
        )

        answer = response.choices[0].message.content.strip()

        # 결과 출력
        embed = discord.Embed(
            title="💬 AI의 응답",
            description=answer[:4000],
            color=0x2B6CB0
        )
        embed.set_footer(text=f"질문자: {ctx.author}")
        await msg.edit(content=None, embed=embed)

    except Exception as e:
        await msg.edit(content=f"⚠️ 오류 발생: {e}")
        print("Error:", e)

# 실행
if __name__ == "__main__":
    bot.run(MTQzNjk0NTU2MDcyNzk4MjI3MQ.Gk63Ku.KrANa_0mp3Jk49SE3Cwz2ffmgBTsf71u4iYA_o)
