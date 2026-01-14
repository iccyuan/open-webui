"""
title: Context Clear & Token Statistics
author: Combined (Leon + Antigravity)
version: 1.0.0
description: 结合上下文清除（保留System Prompt）和Token统计。Token统计基于截断后的消息计算。
"""

import time
from typing import Optional, Callable, Awaitable, Any
from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Filter priority (lower runs first)"
        )
        enabled: bool = Field(default=True, description="Enable token statistics")
        show_in_message: bool = Field(
            default=True, description="Show statistics in response message"
        )
        model_name: str = Field(
            default="gpt-3.5-turbo",
            description="Model name for token counting (e.g., gpt-3.5-turbo, gpt-4, cl100k_base)",
        )
        use_tiktoken: bool = Field(
            default=True, description="Use tiktoken library for accurate counting"
        )

    class UserValves(BaseModel):
        keep_recent_messages: str = Field(
            default="1",
            description=("默认选择1 = 只保留你的最后一条输入信息。"),
            json_schema_extra={
                "enum": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "8",
                    "10",
                    "12",
                    "15",
                    "18",
                    "20",
                    "32",
                    "64",
                ],
                "input": {
                    "type": "select",
                    "options": [
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "8",
                        "10",
                        "12",
                        "15",
                        "18",
                        "20",
                        "32",
                        "64",
                    ],
                },
            },
        )

    def __init__(self):
        self.valves = self.Valves()
        self.toggle = True
        self.icon = ""
        self.start_time: Optional[float] = None
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.input_message_count: int = 0
        self.output_message_count: int = 0
        self.tokenizer = None
        self._init_tokenizer()

    def _init_tokenizer(self):
        """初始化 tokenizer"""
        if not self.valves.use_tiktoken:
            return

        try:
            import tiktoken

            try:
                self.tokenizer = tiktoken.encoding_for_model(self.valves.model_name)
                print(f"✅ Loaded tiktoken encoder for model: {self.valves.model_name}")
            except KeyError:
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
                print(
                    f"⚠️ Model {self.valves.model_name} not found, using cl100k_base encoding"
                )
        except ImportError:
            print(
                "⚠️ tiktoken not installed. Install with: pip install tiktoken\n"
                "   Falling back to simple estimation method."
            )
            self.tokenizer = None
        except Exception as e:
            print(f"⚠️ Error initializing tiktoken: {e}\n   Using fallback method.")
            self.tokenizer = None

    def _count_tokens_tiktoken(self, text: str) -> int:
        """使用 tiktoken 精确计数 tokens"""
        if not text:
            return 0

        try:
            tokens = self.tokenizer.encode(text)
            return len(tokens)
        except Exception as e:
            print(f"⚠️ Error counting tokens with tiktoken: {e}")
            return self._count_tokens_fallback(text)

    def _count_tokens_fallback(self, text: str) -> int:
        """
        降级方案：简单的 token 计数方法
        使用空格和标点符号分割来估算 token 数量
        """
        if not text:
            return 0

        words = text.split()
        english_tokens = len(words)
        chinese_chars = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
        estimated_tokens = int(english_tokens * 1.3 + chinese_chars * 1.5)
        return max(estimated_tokens, 1)

    def _count_tokens(self, text: str) -> int:
        """统一的 token 计数接口"""
        if self.tokenizer is not None:
            return self._count_tokens_tiktoken(text)
        else:
            return self._count_tokens_fallback(text)

    def _count_messages_tokens(self, messages: list) -> int:
        """
        计算消息列表的 token 数（包括消息格式的开销）
        参考 OpenAI 的计算方式
        """
        if not messages:
            return 0

        total_tokens = 0
        tokens_per_message = 3
        tokens_per_name = 1

        for message in messages:
            total_tokens += tokens_per_message

            role = message.get("role", "")
            if role:
                total_tokens += self._count_tokens(role)

            content = message.get("content", "")
            if isinstance(content, str):
                total_tokens += self._count_tokens(content)
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        total_tokens += self._count_tokens(item.get("text", ""))

            if "name" in message:
                total_tokens += tokens_per_name
                total_tokens += self._count_tokens(message["name"])

        total_tokens += 3
        return total_tokens

    def _get_user_valves(
        self, __user__: Optional[dict]
    ) -> Optional["Filter.UserValves"]:
        if not (__user__ and isinstance(__user__, dict)):
            return None
        try:
            uv = __user__.get("valves", None)
        except Exception:
            return None
        if isinstance(uv, self.UserValves):
            return uv
        return None

    async def inlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
    ) -> dict:
        """
        处理输入请求：
        1. 先执行消息截断（Context Clear）
        2. 再基于截断后的消息进行 Token 统计
        """
        # Toggle 关掉就不截断
        if not getattr(self, "enabled", True):
            return body

        # ========================================
        # 第一步：消息截断逻辑 (Context Clear)
        # ========================================
        messages = body.get("messages", [])
        if not isinstance(messages, list) or not messages:
            return body

        user_valves = self._get_user_valves(__user__)

        keep_setting = "1"
        if user_valves is not None:
            keep_setting = (user_valves.keep_recent_messages or "1").strip()

        try:
            keep_n = int(keep_setting)
            if keep_n < 1:
                keep_n = 1
        except ValueError:
            keep_n = 1

        system_prompt = next(
            (m for m in messages if m.get("role") == "system"),
            None,
        )
        non_system_messages = [m for m in messages if m.get("role") != "system"]

        if not non_system_messages:
            return body

        # 执行截断
        tail = non_system_messages[-keep_n:]

        new_messages = []
        if system_prompt is not None:
            new_messages.append(system_prompt)
        new_messages.extend(tail)

        body["messages"] = new_messages

        # ========================================
        # 第二步：Token 统计逻辑（基于截断后的消息）
        # ========================================
        if not self.valves.enabled:
            return body

        # 记录开始时间
        self.start_time = time.time()

        # 使用截断后的消息列表进行统计
        messages = body.get("messages", [])

        # 只计算非系统消息的数量
        non_system_messages = [m for m in messages if m.get("role") != "system"]
        self.input_message_count = len(non_system_messages)

        # 计算输入 token 数（保持计算所有消息的 tokens，包括 system）
        self.input_tokens = self._count_messages_tokens(messages)

        # 发送状态事件
        if __event_emitter__:
            method = "tiktoken" if self.tokenizer else "估算"
            description = f"📊 输入 tokens: {self.input_tokens} ({method})"

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": description,
                        "done": False,
                    },
                }
            )

        return body

    async def outlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
    ) -> dict:
        """
        处理输出响应，计算输出 token 数、消息条数和响应时间
        """
        if not self.valves.enabled:
            return body

        # 计算响应时间
        end_time = time.time()
        response_time = end_time - self.start_time if self.start_time else 0

        # 从 HTTP 响应中获取消息列表
        messages = body.get("messages", [])

        # 只计算非系统消息的数量
        non_system_messages = [m for m in messages if m.get("role") != "system"]
        self.output_message_count = len(non_system_messages)

        # 计算新增的消息条数（助手的回复数量）
        new_messages = self.output_message_count - self.input_message_count

        # 计算输出 token 数
        if messages:
            # 获取最后一条消息（助手的回复）
            last_message = messages[-1]
            output_text = last_message.get("content", "")
            if isinstance(output_text, str):
                self.output_tokens = self._count_tokens(output_text)
            else:
                self.output_tokens = 0

        # 计算 tokens per second
        tokens_per_second = (
            self.output_tokens / response_time if response_time > 0 else 0
        )

        # 确定使用的计数方法
        method = "tiktoken" if self.tokenizer else "估算"

        # 构建统计信息
        stats_message = (
            f"\n\n---\n"
            f"📊 **Token 统计** ({method})\n"
            f"- 输入 tokens: `{self.input_tokens}`\n"
            f"- 输出 tokens: `{self.output_tokens}`\n"
            f"- 总计 tokens: `{self.input_tokens + self.output_tokens}`\n"
            f"- 响应时间: `{response_time:.2f}` 秒\n"
            f"- 生成速度: `{tokens_per_second:.1f}` tokens/秒"
        )

        # 发送完成状态
        if __event_emitter__:
            description = f"✅ 完成 | 输入: {self.input_tokens} | 输出: {self.output_tokens} | 耗时: {response_time:.2f}s ({method})"

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": description,
                        "done": True,
                    },
                }
            )

        # 如果启用，将统计信息添加到消息末尾
        if self.valves.show_in_message and messages:
            last_message = messages[-1]
            if last_message.get("role") == "assistant":
                content = last_message.get("content", "")
                if isinstance(content, str):
                    last_message["content"] = content + stats_message

        # 重置计数器
        self.start_time = None
        self.input_tokens = 0
        self.output_tokens = 0
        self.input_message_count = 0
        self.output_message_count = 0

        return body
