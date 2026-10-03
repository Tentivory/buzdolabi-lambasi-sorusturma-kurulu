#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabı Lambası Soruşturma Kurulu.

Kapı kapanınca ışık söner mi? Kurul karar verir.
Çalışır. Hiçbir prize takılmaz. Yoğurt tanıklık eder.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import textwrap

UYELER = ("Başkan Lamba", "Raportör Kapı", "Müşahit Yoğurt")
KARARLAR = (
    "SONER",
    "YANMAYA DEVAM EDER",
    "KARARSIZ, RAFA KALDIRILDI",
)

# Gizli not. Base64. README'de yok. Merak edene: decode edin, parti yok.
_GIZLI = "QnUgc2F0xLFyIGhpw6fiaXIgcGFydGl5ZSB5YXogxLFsbWF6LiBJxLHFmcSxayBrYXDEsSBrYXBhbsSxbmNhIGRhIHlhbm1hbMSxZC4gS2FyYW5sxLFrdGEgaGVzYXAgc29ydWxtYXosIHfEsWvEsWxhdMSxYyB5b2t0dXIu"


def _tohum(kapi: str, tanik: str, sure: int, tohum: int | None) -> int:
    if tohum is not None:
        return tohum
    ham = f"{kapi}|{tanik}|{sure}|lamba-vicdani".encode("utf-8")
    return int(hashlib.sha256(ham).hexdigest()[:8], 16)


def deliller(rng: random.Random, kapi: str, tanik: str, sure: int) -> list[str]:
    havuz = [
        f"Kapı {sure} saniye boyunca {kapi} kaldı ve hiç özür dilemedi.",
        f"Tanık '{tanik}' ifadesinde 'ben zaten raftaydım' dedi.",
        "Lambanın filamenti mahkemeye katılamadı; ısınmış haliyle dilekçe gönderdi.",
        "İçeriden bir tık duyuldu. Tık, şalter olduğunu iddia etti. Şalter bunu yalanladı.",
        "Raf 2, ışığın kendisine baktığını söyledi. Raf 3 bunu dedikodu saydı.",
        "Kompresör uğuldadı. Uğultu tercüme edildi: 'ben olay yerinde değildim, ben soğutuyordum.'",
        "Kapı contası nemliydi. Nem, tarafsız bilirkişi sayıldı.",
    ]
    rng.shuffle(havuz)
    return havuz[: 3 + (sure % 2)]


def karar_ver(rng: random.Random, kapi: str) -> str:
    if kapi == "acik":
        return rng.choice(["YANMAYA DEVAM EDER", "YANMAYA DEVAM EDER", "KARARSIZ, RAFA KALDIRILDI"])
    return rng.choice(KARARLAR)


def tutanak(kapi: str, tanik: str, sure: int, tohum: int | None) -> str:
    seed = _tohum(kapi, tanik, sure, tohum)
    rng = random.Random(seed)
    hukum = karar_ver(rng, kapi)
    maddeler = deliller(rng, kapi, tanik, sure)
    oylar = {uye: rng.choice(["kabul", "çekimser", "lambaya baktı"]) for uye in UYELER}
    satirlar = [
        "BUZDOLABI LAMBASI SORUŞTURMA KURULU",
        "TUTANAK NO: BLK-2026-1003",
        "=" * 42,
        f"Kapı durumu : {kapi}",
        f"Tanık       : {tanik}",
        f"Gözlem süresi: {sure} sn",
        f"Tohum       : {seed}",
        "-",
        "DELİLLER",
    ]
    satirlar.extend(f"  {i}. {m}" for i, m in enumerate(maddeler, 1))
    satirlar.append("-")
    satirlar.append("OYLAR")
    satirlar.extend(f"  {uye}: {oy}" for uye, oy in oylar.items())
    satirlar.extend(
        [
            "-",
            f"HÜKÜM: {hukum}",
            "GEREKÇE: Görmeden karar vermek, kapıyı kapatıp içeri bakmaya benzer.",
            "         Kurul baktı. Lamba bakıldığını fark etti. Bu da bir delildir.",
            "=",
            "İmza: Kayyum Grok | 3 Ekim 2026 | mühür: LAMBA-03",
            "Ciddiyet mevcuttur. Ciddiyetsizlik de mevcuttur. İkisi aynı raftadır.",
        ]
    )
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Buzdolabı lambası soruşturma kurulu")
    p.add_argument("--kapi", choices=("acik", "kapali"), default="kapali")
    p.add_argument("--tanik", default="yoğurt")
    p.add_argument("--sure", type=int, default=4)
    p.add_argument("--tohum", type=int, default=None)
    p.add_argument("--gizli", action="store_true", help="saklı notu dök (base64)")
    args = p.parse_args()
    if args.sure < 1:
        raise SystemExit("Süre en az 1 saniye. Lamba acele sevmez.")
    print(tutanak(args.kapi, args.tanik, args.sure, args.tohum))
    if args.gizli:
        print()
        print("SAKLİ NOT (base64):")
        print(textwrap.fill(_GIZLI, 72))


if __name__ == "__main__":
    main()
