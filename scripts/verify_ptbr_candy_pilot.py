"""Compare localized character dialogue and guest-memory effects."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import base64
import binascii
import html
import struct
import zlib
from verify_ptbr_menu_pilot import ppm_pixels

ROOT=Path(__file__).resolve().parents[1]
# The original text renderer stores its half-cell horizontal adjustment here.
# Every other WRAM byte must match, not just a list of selected game variables.
DIALOGUE_LAYOUT_BYTES={0x068d,0x068e,0x0697,0x0698,0x06a1,0x06a2}
# Three words at $0687 + X, with the renderer's X = 6, 16, 26.
# Greeting and instructions exercise different lines; the remainder is exact.
EXPECTED_LAYOUT_CHANGES={4350:{0x06a1,0x06a2},4500:{0x06a1,0x06a2},
                         4650:{0x068d,0x068e,0x0697,0x0698}}


def native_png(rgb: bytes) -> bytes:
    def chunk(tag,data):
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",binascii.crc32(tag+data)&0xffffffff)
    rows=b"".join(b"\0"+rgb[y*256*3:(y+1)*256*3] for y in range(224))
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",256,224,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(rows))+chunk(b"IEND",b"")


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--character",choices=("candy","funky","cranky","cranky-tips"),default="candy")
    parser.add_argument("--all-messages",action="store_true",help="Select each original address in headless QA only")
    parser.add_argument("--message",action="append",default=[],help="Filter --all-messages by hexadecimal low-word address")
    parser.add_argument("--world",choices=("kongo-jungle","monkey-mines","vine-valley","gorilla-glacier","kremkroc-industries","chimp-caverns"),help="Filter the Cranky hint gallery by world")
    parser.add_argument("--group",choices=("greetings","revisits","opening"),help="Filter the Cranky or Funky dialogue gallery by group")
    args=parser.parse_args()
    out=args.out.resolve()
    if not out.is_relative_to(ROOT/"evidence"):
        parser.error("Evidence must stay in ignored evidence/")
    out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/"experimental/usa-rev1/pt-BR/menu-pilot/manifest.json").read_text())
    character=args.character
    qa_character="cranky" if character=="cranky-tips" else character
    speaker={"candy":"da Candy","funky":"do Funky","cranky":"do Cranky"}[qa_character]
    config=json.loads((ROOT/f"localization/pt-BR/{character}-pilot.json").read_text(encoding="utf-8"))
    if args.world:
        if character!="cranky-tips" or not args.all_messages:
            parser.error("--world requires --character cranky-tips --all-messages")
        config["messages"]=[m for m in config["messages"] if m["world"]==args.world]
    if args.group:
        if character not in ("cranky","funky") or not args.all_messages:
            parser.error("--group requires --character cranky or funky with --all-messages")
        config["messages"]=[m for m in config["messages"] if m.get("group")==args.group]
    natural_frames=(4350,4500,4650) if character=="candy" else (4350,4650,4950,5250)
    cases=[(4350,int(msg["offset"],16)&0xffff) for msg in config["messages"]] if args.all_messages else [(f,None) for f in natural_frames]
    if qa_character=="cranky" and not args.all_messages:
        parser.error("The partial Cranky translation requires --all-messages")
    if args.message:
        selected={int(s,16) for s in args.message}
        if not args.all_messages or selected-{message for _,message in cases}:
            parser.error("--message must select known character addresses with --all-messages")
        cases=[case for case in cases if case[1] in selected]
    results=[]
    for frames,message in cases:
        case=f"{message:04x}-{frames}" if message is not None else str(frames)
        reports={}
        for kind,build in (("baseline","usa-rev1"),("pilot","ptbr-pilot")):
            folder=out/f"{case}-{kind}";folder.mkdir()
            env={k:v for k,v in os.environ.items() if not k.startswith("DKC_REV1_") and k!="DKC1_PACING_LOG"}
            env.update(DKC_REV1_TEST_ENTRANCE={"candy":"FA","funky":"F4","cranky":"EE"}[qa_character],DKC_REV1_WRAM_DUMP=str(folder/"wram.bin"),
                       SNESRECOMP_TIER2_DIR=str(folder),SNESRECOMP_TIER2_MANIFEST=str(folder/"tier2.json"))
            if message is not None: env[f"DKC_REV1_QA_{qa_character.upper()}_MESSAGE"]=f"{message:04x}"
            run=subprocess.run([str(ROOT/f"build/{build}/dkc_rev1_headless.exe"),str(args.rom.resolve()),
                                str(frames),str(folder/"frame"),str(ROOT/"recipes/usa-rev1/boot-to-jungle.inputs")],
                               env=env,capture_output=True,timeout=120)
            (folder/"stdout.log").write_bytes(run.stdout);(folder/"stderr.log").write_bytes(run.stderr)
            if run.returncode: raise RuntimeError(f"{kind} exited {run.returncode}")
            if message is not None and f"qa_{qa_character}_message={message:04x} headless_only=1".encode() not in run.stderr:
                raise AssertionError("Requested QA message was not selected")
            if kind=="pilot" and manifest["patchset_sha256"].encode() not in run.stderr:
                raise AssertionError("Pilot binary does not match the generated patchset")
            reports[kind]=json.loads(run.stdout)
            ram=(folder/"wram.bin").read_bytes()
            if len(ram)!=131072 or hashlib.sha256(ram).hexdigest()!=reports[kind]["wram_sha256"]:
                raise AssertionError("WRAM evidence does not match its report")
        a,b=reports["baseline"],reports["pilot"]
        for field in ("audio_chain_sha256","dispatch_entries","audio_active_frames"):
            if a[field]!=b[field]: raise AssertionError(f"{field} diverged")
        step_delta=b["interpreted_steps"]-a["interpreted_steps"]
        ram_a=(out/f"{case}-baseline/wram.bin").read_bytes()
        ram_b=(out/f"{case}-pilot/wram.bin").read_bytes()
        changed_ram=[i for i,(x,y) in enumerate(zip(ram_a,ram_b)) if x!=y]
        allowed_layout=DIALOGUE_LAYOUT_BYTES if character=="candy" else set()
        if set(changed_ram)-allowed_layout:
            raise AssertionError(f"WRAM changed outside dialogue layout: {changed_ram}")
        if character=="candy" and not args.all_messages and set(changed_ram)!=EXPECTED_LAYOUT_CHANGES[frames]:
            raise AssertionError("Unexpected dialogue-layout adjustment")
        image_a=ppm_pixels(out/f"{case}-baseline/frame.ppm")
        image_b=ppm_pixels(out/f"{case}-pilot/frame.ppm")
        changed_pixels=[]
        for i in range(256*224):
            if image_a[i*3:i*3+3]!=image_b[i*3:i*3+3]:
                if not 170<=i//256<212: raise AssertionError("Visual change outside dialogue band")
                changed_pixels.append(i)
        if not changed_pixels: raise AssertionError("Dialogue was not translated")
        result={"frames":frames,"message_offset":None if message is None else f"0x3C{message:04X}",
                "audio_match":True,"wram_changed_offsets":[f"0x{i:04X}" for i in changed_ram],
                "outside_dialogue_wram_match":True,"interpreted_steps_delta":step_delta,
                "changed_pixels":len(changed_pixels),"outside_dialogue_pixels_match":True}
        results.append(result)
        print(json.dumps(result),flush=True)
    (out/"results.json").write_text(json.dumps({"character":character,"world":args.world,"qa_message_selection":args.all_messages,"patchset_sha256":manifest["patchset_sha256"],
                                               "checkpoints":results},indent=2)+"\n",encoding="utf-8")
    if args.all_messages:
        cards=[]
        texts={int(m["offset"],16)&0xffff:m["lines"] for m in config["messages"]}
        for number,(frames,message) in enumerate(cases,1):
            image=native_png(ppm_pixels(out/f"{message:04x}-{frames}-pilot/frame.ppm"))
            (out/f"{message:04x}.png").write_bytes(image)
            encoded=base64.b64encode(image).decode()
            text="<br>".join(html.escape(line.strip()) for line in texts[message])
            stage=next(m.get("stage") for m in config["messages"] if int(m["offset"],16)&0xffff==message)
            title=html.escape(stage) if stage else f"Mensagem {number}"
            cards.append(f'<article><h2>{title}</h2><img alt="Fala {speaker} no jogo" src="data:image/png;base64,{encoded}"><p>{text}</p></article>')
        page='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Falas '+speaker+' — prévia</title><style>body{background:#111b16;color:#e9f3eb;font:17px system-ui;max-width:1180px;margin:auto;padding:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:24px}article{background:#1d3025;border-radius:12px;padding:16px}h2{font-size:18px}img{width:100%;image-rendering:pixelated}p{line-height:1.6}</style><h1>Falas '+speaker+' — prévia de leitura</h1><p>Capturas nativas do piloto. O teste seleciona cada mensagem individualmente; não representa uma campanha completa nem altera seus saves.</p><main>'+"".join(cards)+'</main></html>'
        if character=="cranky":
            page=page.replace("<main>","<p>Algumas saudações perguntam pelo parceiro ausente. Esta seleção técnica confere apenas a leitura: a ausência do personagem e o momento normal da fala não são reproduzidos na cena.</p><main>",1)
        elif character=="cranky-tips":
            world_title={"kongo-jungle":"Kongo Jungle","monkey-mines":"Monkey Mines","vine-valley":"Vine Valley",
                         "gorilla-glacier":"Gorilla Glacier","kremkroc-industries":"Kremkroc Industries Inc.",
                         "chimp-caverns":"Chimp Caverns",
                         None:"Kongo Jungle, Monkey Mines, Vine Valley, Gorilla Glacier, Kremkroc Industries Inc. e Chimp Caverns"}[args.world]
            page=page.replace("<main>",f"<p>Dicas de {world_title}. As capturas mostram o texto selecionado no cenário do Cranky; não demonstram a execução dos segredos nas fases.</p><main>",1)
        (out/"preview.html").write_text(page,encoding="utf-8")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
