from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib
matplotlib.use("Agg")  # 使用无界面后端，便于服务器环境保存图片
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors


PeriodName = str


def _default_corpora() -> Dict[PeriodName, List[List[str]]]:
    """提供演示用的极小语料，生产中请替换为真实语料。

    返回：period -> tokenized sentences
    """

    return {
        "greek": [
            "philosophy virtue polis academy plato aristotle".split(),
            "myth logos ethos pathos".split(),
        ],
        "medieval": [
            "theology church scholasticism virtue faith reason".split(),
            "monastery scripture allegory".split(),
        ],
        "modern": [
            "science technology democracy reason experiment".split(),
            "industry capitalism modernity liberty".split(),
        ],
    }


def train_or_load_models(
    periods: Sequence[PeriodName] | None = None,
    models_dir: Path | None = None,
    corpora: Dict[PeriodName, List[List[str]]] | None = None,
    vector_size: int = 100,
    window: int = 5,
    min_count: int = 1,
    workers: int = 1,
    epochs: int = 50,
) -> Dict[PeriodName, KeyedVectors]:
    """为每个时期训练或加载 Word2Vec 模型，返回 KeyedVectors 映射。

    - 若 models_dir 下存在 `{period}.kv`（KeyedVectors）或 `{period}.model` 则优先加载
    - 否则使用提供或默认的小语料训练并保存
    """

    models_dir = Path(models_dir or (Path(__file__).resolve().parent.parent / "models"))
    models_dir.mkdir(parents=True, exist_ok=True)

    corpora = corpora or _default_corpora()
    if periods is None:
        periods = list(corpora.keys())

    period_to_kv: Dict[PeriodName, KeyedVectors] = {}

    for period in periods:
        kv_path = models_dir / f"{period}.kv"
        model_path = models_dir / f"{period}.model"

        if kv_path.exists():
            kv = KeyedVectors.load(str(kv_path), mmap='r')
            period_to_kv[period] = kv
            continue

        if model_path.exists():
            model = Word2Vec.load(str(model_path))
            period_to_kv[period] = model.wv
            # 同步保存一份 kv，便于下次更快加载
            model.wv.save(str(kv_path))
            continue

        # 训练
        sentences = corpora.get(period)
        if not sentences:
            raise ValueError(f"缺少时期 {period} 的训练语料")

        model = Word2Vec(
            sentences=sentences,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            workers=workers,
            epochs=epochs,
        )
        model.save(str(model_path))
        model.wv.save(str(kv_path))
        period_to_kv[period] = model.wv

    return period_to_kv


def extract_vectors_for_word(
    word: str,
    period_to_kv: Dict[PeriodName, KeyedVectors],
) -> Tuple[List[str], List[List[float]]]:
    """从各时期模型中提取目标词的向量。

    返回：(periods, vectors)
    若某些时期缺失该词，将跳过该时期。
    若全部缺失，抛出异常。
    """

    periods: List[str] = []
    vectors: List[List[float]] = []

    for period, kv in period_to_kv.items():
        if word in kv.key_to_index:
            vec = kv.get_vector(word)
            periods.append(period)
            vectors.append(vec.tolist())

    if not vectors:
        available = {p: list(kv.key_to_index)[:10] for p, kv in period_to_kv.items()}
        raise ValueError(f"词 '{word}' 在所有时期模型中均不存在。可用示例: {available}")

    return periods, vectors


def tsne_reduce(vectors: Sequence[Sequence[float]], random_state: int = 42) -> List[Tuple[float, float]]:
    """使用 TSNE 将向量降维至二维。

    自动根据样本数调整 perplexity，避免过大导致报错。
    """

    n = len(vectors)
    if n < 2:
        return [(0.0, 0.0)]

    # perplexity 必须 < n
    perplexity = max(2.0, min(30.0, float(n - 1)))
    tsne = TSNE(n_components=2, perplexity=perplexity, learning_rate='auto', init='random', random_state=random_state)
    emb = tsne.fit_transform(vectors)
    return [(float(x), float(y)) for x, y in emb]


def plot_semantic_shift(
    word: str,
    coords: Sequence[Tuple[float, float]],
    periods: Sequence[str],
    out_dir: Path | None = None,
) -> str:
    """绘制连线散点图并保存至 static/{word}.png，返回文件路径字符串。"""

    out_dir = Path(out_dir or (Path(__file__).resolve().parent.parent / "static"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{word}.png"

    plt.figure(figsize=(8, 4.5), dpi=120)
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]

    # 连线
    if len(coords) >= 2:
        plt.plot(xs, ys, color="#2196F3", linewidth=2, alpha=0.9)

    # 散点与标注
    plt.scatter(xs, ys, color="#F44336", s=50, zorder=3)
    for (x, y), period in zip(coords, periods):
        plt.text(x + 0.5, y + 0.5, period, fontsize=9)

    plt.title(f"{word} 的语义漂移（TSNE）")
    plt.xlabel("TSNE-1")
    plt.ylabel("TSNE-2")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, format="png")
    plt.close()

    return str(out_path)


def generate_semantic_shift_figure(
    word: str,
    periods: Sequence[PeriodName] | None = None,
    models_dir: Path | None = None,
    corpora: Dict[PeriodName, List[List[str]]] | None = None,
) -> str:
    """端到端：训练/加载 -> 提取向量 -> TSNE -> 绘图保存，返回文件路径。

    示例：
        generate_semantic_shift_figure("virtue")
    """

    period_to_kv = train_or_load_models(periods=periods, models_dir=models_dir, corpora=corpora)
    used_periods, vectors = extract_vectors_for_word(word, period_to_kv)
    coords = tsne_reduce(vectors)
    out_path = plot_semantic_shift(word, coords, used_periods)
    return out_path



