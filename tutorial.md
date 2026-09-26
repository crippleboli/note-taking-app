# `translator.py` 技术教程：用 DeepSeek API 翻译文本

本文根据项目中的 `translator.py`，逐步说明脚本的组成、运行流程、环境配置和使用方法。这个程序通过 OpenAI Python SDK 兼容的接口调用 DeepSeek 的 `deepseek-chat` 模型，将输入文本翻译成英文，并把结果输出到终端。

## 1. 程序能做什么

脚本支持两种使用方式：

- **命令行运行**：在终端提供一段待翻译文本，程序打印英文翻译。
- **Python 代码调用**：导入 `llm_generate(prompt)`，将文本传给它并接收翻译字符串。

调用模型需要有效的 DeepSeek API Key。脚本从 `.env` 文件读取名为 `OPENAI_API_KEY` 的环境变量，不需要把密钥写进源代码。

## 2. 运行前的准备

### 安装依赖

项目的 `requirements.txt` 已包含脚本所需的两个包：

```text
openai==1.106.1
python-dotenv>=1.0.0
```

在项目根目录创建或激活 Python 虚拟环境，然后安装项目依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell 激活虚拟环境的命令是：

```powershell
.venv\Scripts\Activate.ps1
```

### 配置 API Key

在项目根目录创建 `.env` 文件，并写入自己的 API Key：

```dotenv
OPENAI_API_KEY=你的DeepSeek_API_Key
```

不要将真实 API Key 写入脚本、提交到 Git 或公开分享。项目的 `.gitignore` 已忽略 `.env` 文件；如果密钥曾经意外公开，应及时在服务提供方处撤销并重新生成。

## 3. 从文件顶部开始理解

### 导入模块

```python
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
```

- `os` 用于从进程环境中读取 API Key。
- `sys` 用于读取命令行参数，并在参数缺失时设置退出状态码。
- `load_dotenv` 用于把 `.env` 文件中的变量加载到当前进程环境。
- `OpenAI` 是 OpenAI Python SDK 的客户端。DeepSeek 提供兼容的 API 接口，因此可以使用该 SDK 指定 DeepSeek 的 `base_url` 来发起请求。

### 加载 `.env`

```python
load_dotenv()
```

这行代码在模块加载时执行。`python-dotenv` 会查找 `.env` 文件，并将其中的变量载入环境；默认不会覆盖进程中已经存在的同名环境变量。因此，终端、IDE 或部署环境中预先设置的 `OPENAI_API_KEY` 仍然可以优先生效。

## 4. `llm_generate(prompt)` 的工作过程

函数定义如下：

```python
def llm_generate(prompt: str) -> str:
```

类型标注表示函数接收一个字符串，并预期返回一个字符串。函数主体按以下顺序执行。

### 第一步：读取并检查密钥

```python
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Add it to the project .env file."
    )
```

`os.getenv` 从当前进程环境读取变量。若密钥未配置或为空，函数会明确抛出 `RuntimeError`，而不是继续发送无效请求。运行脚本时应先确认 `.env` 位于项目中可被加载的位置，且变量名拼写准确。

### 第二步：创建 API 客户端

```python
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)
```

`api_key` 用于请求认证；`base_url` 将 SDK 请求指向 DeepSeek API，而不是 OpenAI 的默认服务地址。这里每次调用 `llm_generate` 都会创建客户端。

### 第三步：构造对话并请求模型

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a professional translator. Translate the user's "
                "text into English and return only the translation."
            ),
        },
        {"role": "user", "content": prompt},
    ],
)
```

请求使用聊天补全接口，并指定模型 `deepseek-chat`。`messages` 中包含两条消息：

- **system 消息**：告诉模型它应扮演专业译者，将用户文本翻译成英文，并且只返回译文。这会引导模型的行为和输出格式。
- **user 消息**：包含函数参数 `prompt`，也就是实际待翻译的文本。

调用是同步的：程序会等待服务器返回结果后再继续执行。脚本没有启用流式输出，因此不会逐字显示翻译过程。

### 第四步：提取并返回译文

```python
translation = response.choices[0].message.content
if translation is None:
    raise RuntimeError("The translation response did not contain any text.")
return translation
```

聊天补全响应的 `choices` 列表包含模型生成的候选结果。脚本取第一个候选项 (`choices[0]`)，再读取其中的消息文本。若服务响应中没有文本内容，则抛出错误；正常情况下，函数返回译文字符串。

网络连接、认证、额度或服务端错误由 SDK 在请求阶段抛出。脚本没有捕获这些异常，所以它们会向上传递并显示错误信息，方便定位问题。

## 5. 命令行入口

```python
if __name__ == "__main__":
```

Python 直接执行 `translator.py` 时，`__name__` 的值为 `"__main__"`，入口代码因此运行。如果脚本被另一个 Python 文件导入，这部分不会自动执行，但 `llm_generate` 仍可供调用。

### 检查是否提供文本

```python
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <text to translate>", file=sys.stderr)
    sys.exit(2)
```

`sys.argv[0]` 是脚本名；后续元素是用户传入的参数。如果没有任何文本参数，程序将使用标准错误流显示用法，并以状态码 `2` 退出。非零状态码通常表示命令使用有误。

### 合并命令行参数并翻译

```python
input_text = " ".join(sys.argv[1:])
print(llm_generate(input_text))
```

程序把脚本名之后的所有参数用空格连接，作为完整输入传给 `llm_generate`，然后将返回的译文打印到终端。

例如，下面两种写法均可：

```bash
python translator.py "今天天气很好。"
python translator.py 今天天气 很好
```

推荐将整段文本放在引号中。否则，Shell 会把空格分隔的部分作为多个参数；程序虽然会用空格重新连接它们，但原有的连续空格和换行等格式不会被保留。

## 6. 完整运行示例

配置好 `.env` 并安装依赖后，在项目根目录运行：

```bash
python translator.py "请把这句话翻译成英文。"
```

程序会将输入发给 DeepSeek 模型，并在终端输出类似下面的译文：

```text
Please translate this sentence into English.
```

实际措辞由模型生成，可能与示例不同。

如果使用虚拟环境，也可以直接运行环境中的 Python：

```bash
.venv/bin/python translator.py "你好，欢迎使用这个翻译程序。"
```

## 7. 在其他 Python 程序中调用

可以在项目中的其他 Python 文件里导入函数：

```python
from translator import llm_generate

result = llm_generate("欢迎来到我们的团队。")
print(result)
```

导入 `translator` 时，文件顶层的 `load_dotenv()` 会执行，所以 `.env` 中的密钥也会被加载；但命令行入口不会执行。调用者仍需确保密钥存在，并处理可能出现的 `RuntimeError` 或 SDK 请求异常。

## 8. 常见问题

### 提示 `OPENAI_API_KEY is not set`

检查以下事项：

1. `.env` 文件是否存在，并放在 `python-dotenv` 可以找到的位置（通常是项目根目录）。
2. 变量名是否准确写成 `OPENAI_API_KEY`。
3. 文件内容是否采用 `OPENAI_API_KEY=...` 格式，等号两侧不要添加不必要的空格。
4. 如果通过 IDE 启动，确认其工作目录与预期一致，且没有其他设置影响 `.env` 加载。

### API 请求失败

检查 API Key 是否有效、账户/API 是否可用以及网络是否能连接 DeepSeek 服务。认证、连接或服务端错误由 SDK 报出；本脚本不会把错误转换成看似成功的翻译结果。

### 没有看到译文

确认命令行确实带有待翻译文本，并检查是否收到错误信息。没有参数时脚本只显示用法并以状态码 `2` 退出。

## 9. 执行流程小结

从命令行运行时，整体调用链为：

```text
启动脚本
  -> 加载 .env
  -> 检查是否提供命令行文本
  -> 合并文本参数
  -> llm_generate(prompt)
       -> 读取并验证 OPENAI_API_KEY
       -> 创建指向 DeepSeek 的 OpenAI SDK 客户端
       -> 发送 system 与 user 消息给 deepseek-chat
       -> 提取第一条候选回复文本
       -> 返回英文译文
  -> 打印译文
```

核心职责分工清晰：`load_dotenv()` 负责配置加载，`llm_generate()` 负责密钥检查和模型调用，`__main__` 入口负责命令行交互与输出。
