---
name: doubao-tts
description: 使用豆包语音合成（Volcengine TTS）将文本转为语音文件。当用户提到"豆包TTS"、"豆包语音合成"、"doubao tts"、"火山引擎TTS"、"volcengine tts"、"语音合成"、"文字转语音"、"TTS"、"生成音频"、"朗读文字"，或任何需要调用豆包/火山引擎语音合成 API 的场景，必须触发本技能。
---

# Doubao TTS

使用火山引擎豆包语音合成 V3 HTTP SSE 单向流式接口把文本生成音频文件。

## 文件位置

- 技能目录：`/Users/zhuyuhua/.cc-switch/skills/doubao-tts`
- 主脚本：`/Users/zhuyuhua/.cc-switch/skills/doubao-tts/scripts/tts.py`

## 必要环境变量

| 变量名 | 说明 |
|---|---|
| `DOUBAO_TTS_APPID` | 火山引擎控制台里的 AppID，对应 `X-Api-App-Id` |
| `DOUBAO_TTS_TOKEN` | Access Token，对应 `X-Api-Access-Key` |
| `DOUBAO_TTS_RESOURCE_ID` | 可选，默认留空时脚本走 `seed-tts-2.0` |

快速检查：

```sh
[ -n "$DOUBAO_TTS_APPID" ] && echo "APPID set" || echo "APPID missing"
[ -n "$DOUBAO_TTS_TOKEN" ] && echo "TOKEN set" || echo "TOKEN missing"
```

如果没配，不要引用旧的 `minis://` 设置链接，直接告诉用户需要在当前本地环境里设置这些变量。

## 获取凭证

1. 打开 [火山引擎语音应用管理](https://console.volcengine.com/speech/app)
2. 进入豆包语音合成应用详情
3. 取出：
   - App ID -> `DOUBAO_TTS_APPID`
   - Access Token -> `DOUBAO_TTS_TOKEN`

如未开通服务，先在 [语音合成大模型页面](https://console.volcengine.com/speech/service/10) 开通。

## 调用方式

基础用法：

```bash
uv run --script /Users/zhuyuhua/.cc-switch/skills/doubao-tts/scripts/tts.py \
  --text "你好，欢迎使用豆包语音合成" \
  --output /Users/zhuyuhua/Documents/Codex/output/doubao-tts/hello.mp3
```

指定音色和语速：

```bash
uv run --script /Users/zhuyuhua/.cc-switch/skills/doubao-tts/scripts/tts.py \
  --text "今天天气真好" \
  --speaker zh_female_cancan_uranus_bigtts \
  --speech-rate 10 \
  --output /Users/zhuyuhua/Documents/Codex/output/doubao-tts/weather.mp3
```

英文：

```bash
uv run --script /Users/zhuyuhua/.cc-switch/skills/doubao-tts/scripts/tts.py \
  --text "Hello! Nice to meet you." \
  --speaker en_female_dacey_uranus_bigtts \
  --output /Users/zhuyuhua/Documents/Codex/output/doubao-tts/hello-en.mp3
```

## 参数要点

常用参数：

| 参数 | 说明 |
|---|---|
| `--text` | 要合成的文本，必填 |
| `--output` | 输出音频路径，必填 |
| `--speaker` | 音色，默认 `zh_female_xiaohe_uranus_bigtts` |
| `--encoding` | `mp3` / `pcm` / `ogg_opus` |
| `--speech-rate` | 语速，范围 `-50` 到 `100` |
| `--loudness` | 音量，范围 `-50` 到 `100` |
| `--emotion` | 情感，例如 `happy` / `sad` / `narrator` |
| `--emotion-scale` | 情感强度 `1` 到 `5` |
| `--resource-id` | 覆盖环境变量中的资源 ID |
| `--json` | 用 JSON 输出结果摘要 |

## 模型与音色

推荐用 2.0：

| Resource ID | 说明 |
|---|---|
| `seed-tts-2.0` | 默认，支持 `*_uranus_bigtts` 音色 |
| `seed-tts-1.0` | 支持 `BV*_streaming` 音色 |
| `seed-tts-1.0-concurr` | 1.0 并发版 |

常用 2.0 音色：

| speaker | 说明 |
|---|---|
| `zh_female_shuangkuaisisi_uranus_bigtts` | 爽快思思 |
| `zh_female_cancan_uranus_bigtts` | 知性灿灿 |
| `zh_female_xiaohe_uranus_bigtts` | 小何 |
| `zh_male_m191_uranus_bigtts` | 云舟 |
| `en_female_dacey_uranus_bigtts` | 美式英语女声 |
| `en_male_tim_uranus_bigtts` | 美式英语男声 |

注意：
- `seed-tts-2.0` 只配 `*_uranus_bigtts`
- `seed-tts-1.0` 才配 `BV*_streaming`

## 工作流

1. 检查环境变量是否存在
2. 运行 `tts.py` 生成音频
3. 把输出路径返回给用户
4. 如果用户要试听，可在回复里引用本地文件路径

## 故障处理

- 报未设置 AppID 或 Token：提醒用户配置对应环境变量
- 报网络错误：提示检查网络
- 报权限或音色不可用：建议切换到默认 2.0 音色重试
- 报文本过长：让用户缩短文本

## 输出规则

- 成功时，直接告诉用户生成到了哪个文件
- 不要暴露 Token
- 不要再返回旧环境的 `minis://workspace/...` 链接
