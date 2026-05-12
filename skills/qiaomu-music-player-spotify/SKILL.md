---
name: qiaomu-music-player-spotify
description: |
  Spotify 音乐播放控制 + 5947 风格数据库。搜索、播放、暂停、队列管理、场景音乐推荐、风格查询与探索。

  USE THIS SKILL when user mentions:
  - Playback: "播放音乐", "来首歌", "放点音乐", "播放", "想听XX", "来点XX音乐"
  - Controls: "暂停", "继续", "下一首", "上一首", "音量", "正在播放什么"
  - Genre lookup: /genre, "查询音乐风格", "推荐音乐类型", "XX风格有哪些子分类"
  - Scene/mood: "适合深夜的音乐", "有活力的", "空灵的", "推荐一些XX特点的音乐风格"
  - Suno integration: 用 Suno 生成音乐但未指定风格时
  - /spotify
---

# Qiaomu Music Player Spotify

统一处理两类任务：
- **Spotify 播放控制**：搜索、播放、暂停、续播、切歌、队列、设备、音量、最近播放、歌单
- **5947 风格数据库查询**：风格解释、子分类探索、按场景推荐风格，必要时再落到具体播放内容

## 文件位置

当前技能目录就是：
`/Users/zhuyuhua/.cc-switch/skills/qiaomu-music-player-spotify`

核心文件：
- `spotify.py`：Spotify Web API CLI
- `auth_setup.py`：OAuth 授权脚本
- `references/_index.json`：49 个主分类索引，风格查询先读这个
- `references/main/*.json`：主分类下的直接子分类
- `references/detailed/*.json`：更细的子分类详情
- `references/DATA_SOURCE.md`：数据来源说明

## 调用原则

1. 用户要的是**直接控制播放**，就直接调用 `spotify.py`，不要先讲理论。
2. 用户说的是**具体歌曲 / 歌手 / 专辑 / 播放列表**，先搜再播。
3. 用户说的是**明确风格或明确场景**，优先走内置映射播放列表；如果只是推荐，不要自动播放。
4. 用户说的是**模糊氛围**，先给 3-5 个具体方案，等用户确认后再播。
5. 用户问**风格知识**时，先查风格库，不要硬凭印象乱答。

## Spotify 命令

从技能目录运行：

```bash
python3 spotify.py
python3 spotify.py search "Radiohead" artist 5
python3 spotify.py play spotify:playlist:37i9dQZF1DX8NTLI2TtZa6
```

支持的真实命令如下：

| 命令 | 用法 |
|------|------|
| `search` | `python3 spotify.py search "<query>" [track\|artist\|album\|playlist] [limit]` |
| `play` | `python3 spotify.py play <spotify_uri或track_id> [device_id]` |
| `pause` | `python3 spotify.py pause` |
| `resume` | `python3 spotify.py resume` |
| `next` | `python3 spotify.py next` |
| `prev` | `python3 spotify.py prev` |
| `queue` | `python3 spotify.py queue <spotify_uri或track_id>` |
| `now` | `python3 spotify.py now` |
| `show-queue` | `python3 spotify.py show-queue [limit]` |
| `volume` | `python3 spotify.py volume <0-100>` |
| `devices` | `python3 spotify.py devices` |
| `recent` | `python3 spotify.py recent [limit]` |
| `playlists` | `python3 spotify.py playlists [limit]` |
| `batch-play` | `python3 spotify.py batch-play <uri1> <uri2> ...` |
| `shuffle` | `python3 spotify.py shuffle <on\|off>` |
| `repeat` | `python3 spotify.py repeat <track\|context\|off>` |
| `artist-top` | `python3 spotify.py artist-top <artist_id>` |
| `artist-albums` | `python3 spotify.py artist-albums <artist_id> [album\|single\|compilation] [limit]` |
| `album-tracks` | `python3 spotify.py album-tracks <album_id>` |

补充：
- `python3 spotify.py` 不带参数会打印 usage
- 所有结果是 JSON，优先按 JSON 解析再回复用户
- `play` 传普通 ID 时默认按 `track` 处理；专辑和歌单请传完整 `spotify:` URI

## 决策流程

### 1. 控制类请求

用户说：
- “暂停” → `python3 spotify.py pause`
- “继续” → `python3 spotify.py resume`
- “下一首” → `python3 spotify.py next`
- “上一首” → `python3 spotify.py prev`
- “正在播放什么” → `python3 spotify.py now`
- “队列里有什么” → `python3 spotify.py show-queue 10`
- “音量调到 40” → `python3 spotify.py volume 40`
- “我最近听了什么” → `python3 spotify.py recent 10`

这类请求不要做多余确认，直接执行。

### 2. 精确播放请求

用户说的是具体歌手 / 歌曲 / 专辑 / 歌单时：

1. 用最合适的类型 `search`
2. 取第一个高置信结果
3. 用对应 URI `play`
4. 需要时用 `now` 回读

示例：

```bash
python3 spotify.py search "Bohemian Rhapsody" track 1
python3 spotify.py play spotify:track:<id>
```

如果用户说“播放 Radiohead 的专辑”：

```bash
python3 spotify.py search "Radiohead" artist 1
python3 spotify.py artist-albums <artist_id> album 10
```

先给 3-5 张高相关专辑让用户选；不要替用户假定是哪一张。

### 3. 多首代表作

用户说“来 3 首最经典的 surf rock”这类请求时：

1. 先自己挑出合理的代表曲
2. 分别 `search`
3. 用 `batch-play` 一次播第一首并把其余加入队列
4. 回复里列出完整播放清单

### 4. 明确风格或明确场景

如果用户说的是明确方向，且目的是**直接听**，优先用内置歌单映射直接播，不必先搜散曲。

常用映射：

| 方向 | Playlist URI |
|------|--------------|
| Jazz | `spotify:playlist:37i9dQZF1DXbITWG1ZJKYt` |
| Lo-fi / 写代码 | `spotify:playlist:37i9dQZF1DWWQRwui0ExPn` |
| Ambient | `spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY` |
| Classical | `spotify:playlist:37i9dQZF1DWWEJlAGA9gs0` |
| Electronic | `spotify:playlist:37i9dQZF1DX4dyzvuaRJ0n` |
| Rock | `spotify:playlist:37i9dQZF1DXcF6B6QPhFDv` |
| R&B | `spotify:playlist:37i9dQZF1DX4SBhb3fqCJd` |
| Hip Hop | `spotify:playlist:37i9dQZF1DX0XUsuxWHRQd` |
| Pop | `spotify:playlist:37i9dQZF1DXcBWIGoYBM5M` |
| Chill / 放松 | `spotify:playlist:37i9dQZF1DX4WYpdgoIcn6` |
| Focus / 专注 | `spotify:playlist:37i9dQZF1DX8NTLI2TtZa6` |
| Sleep / 睡眠 | `spotify:playlist:37i9dQZF1DWZd79rJ6a7lp` |
| Workout / 运动 | `spotify:playlist:37i9dQZF1DX76Wlfdnj7AP` |
| Indie | `spotify:playlist:37i9dQZF1DX2Nc3B70tvx0` |
| Blues | `spotify:playlist:37i9dQZF1DXd9rSDyQguIk` |
| Country | `spotify:playlist:37i9dQZF1DX1lVhptIYRda` |
| Latin | `spotify:playlist:37i9dQZF1DX10zKzsJ2jva` |
| K-Pop | `spotify:playlist:37i9dQZF1DX9tPFwDMOaN1` |
| Punk | `spotify:playlist:37i9dQZF1DX0KpeLYR2IHH` |
| Metal | `spotify:playlist:37i9dQZF1DWTcqUzwhNmKv` |
| Synthwave | `spotify:playlist:37i9dQZF1DX6GJXiuZRisr` |
| Bossa Nova | `spotify:playlist:37i9dQZF1DX4AyFl3yqHeK` |
| Surf Rock | `spotify:playlist:37i9dQZF1DX5hR0J49CmXC` |
| Reggae | `spotify:playlist:37i9dQZF1DXbSbnqxMTGx9` |
| Soul | `spotify:playlist:37i9dQZF1DWULEW2JjEkIS` |
| Funk | `spotify:playlist:37i9dQZF1DWWvhKV4FBciw` |
| Disco | `spotify:playlist:37i9dQZF1DX1MUPbVKMBel` |
| Grunge | `spotify:playlist:37i9dQZF1DX0FOF1IUWK1W` |
| Post-Rock | `spotify:playlist:37i9dQZF1DX9bubh97wEfA` |
| Shoegaze | `spotify:playlist:37i9dQZF1DX6ujZpAN0v9r` |

兜底：
- 如果映射里没有，先 `search "<genre>" playlist 5`
- 如果用户只是问“推荐什么风格”，不要自动播放

### 5. 模糊场景 / 心情

用户说“适合深夜的音乐”“有点空灵”“雨天听什么”这类时：

1. 先读 `references/_index.json`
2. 再读 2-3 个相关的 `references/main/*.json`
3. 必要时补读 `references/detailed/*.json`
4. 选 3-5 个风格方向
5. 每个方向给出一个**具体到歌手 + 专辑或歌曲**的落地推荐
6. 等用户选，再播放

这里的硬规则：
- **模糊需求不要直接播**
- 推荐不能只给风格名，必须给可播放对象
- 用户说“换一个”，从剩余方向里切，不要重复

## 风格查询流程

### 精确查风格

用户说“查一下 Shoegaze”时：

1. 先读 `references/_index.json`
2. 如果是主分类，直接回答主分类描述
3. 如果不是主分类，去 `references/main/*.json` 找
4. 还不够就读对应 `references/detailed/*.json`
5. 输出：
   - 风格名
   - 简短定义
   - 所属父级
   - 子分类或相关分支
   - 数据源链接

### 按特征推荐风格

用户说“推荐一些适合深夜、有点空灵的风格”时：

1. 从描述词抽关键词，例如 `deep night`、`ethereal`、`dreamy`
2. 先匹配主分类，再下钻子分类
3. 给 3-5 个风格，每个带一句理由
4. 如果用户接着要听，再进入播放流程

## 故障处理

- 报 `No tokens found`：运行 `python3 auth_setup.py`
- 报 `401`：脚本会自动刷新一次；还失败通常是 OAuth 失效，需要重授
- 没有活跃设备或播放失败：先 `python3 spotify.py devices`
- 用户指定设备时，把 `device_id` 作为 `play` 的第二个参数传入
- 如果歌单 URI 失效，用 `search ... playlist` 重新找替代

## 输出风格

- 执行成功：直接告诉用户结果，不要贴大段原始 JSON
- 查询风格：优先短答，可附 3-5 个子分类或相关方向
- 推荐播放：给用户明确下一步，例如“要播哪个，回我序号”
- 不要假装真的已经播放；只有脚本成功后才能说“正在播放”
