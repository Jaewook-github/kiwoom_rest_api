# app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from fastapi.staticfiles import StaticFiles
from multiprocessing import Process, Queue
from queue import Empty
import asyncio
import json
import pandas as pd
import os

# ---- 프로젝트 내부 임포트 ----
from main import auto_trade  # auto_trade(in_queue, out_queue)

# ---- 전역 큐 & 프로세스 ----
IN_Q: Queue = None
OUT_Q: Queue = None
TRADE_PROC: Process = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# ---- 라이프사이클 대체 구현 ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    global IN_Q, OUT_Q, TRADE_PROC
    IN_Q = Queue()
    OUT_Q = Queue()
    TRADE_PROC = Process(target=auto_trade, args=(IN_Q, OUT_Q), daemon=False)
    TRADE_PROC.start()

    # startup 끝
    yield

    # shutdown 시작
    try:
        if TRADE_PROC is not None and TRADE_PROC.is_alive():
            TRADE_PROC.join(timeout=1.0)
            if TRADE_PROC.is_alive():
                TRADE_PROC.terminate()
    except Exception:
        pass

# 기존 app 생성 부분을 lifespan 인자로 수정
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ========= 유틸 =========

def df_to_html(df: pd.DataFrame, table_id: str, caption: str = "") -> str:
    if isinstance(df, pd.DataFrame) and not df.empty:
        df = df.copy()  # 원본 보호

        if "수익률(%)" in df.columns:
            def colorize(val):
                try:
                    v = float(val)
                except (ValueError, TypeError):
                    return val
                color = "red" if v >= 0 else "blue"
                return f"<span style='color:{color};'>{v:.2f}</span>"

            df["수익률(%)"] = df["수익률(%)"].apply(colorize)

        table = df.to_html(
            classes="min-w-full",
            border=0,
            table_id=table_id,
            justify="center",
            index=True,
            escape=False  # HTML 태그 적용을 위해 escape 해제
        )

        cap = f"<div class='caption'>{caption}</div>" if caption else ""
        return f"{cap}<div class='tbl'>{table}</div>"

    return f"<div class='tbl text-sm text-gray-500' id='{table_id}'>데이터 없음</div>"


def sse_event(event: str, data: str) -> bytes:
    lines = str(data).splitlines()
    payload = "\n".join(f"data: {line}" for line in lines)
    return f"event: {event}\n{payload}\n\n".encode("utf-8")

# ========= 라우트 =========

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/action", response_class=HTMLResponse)
async def post_action(
    request: Request,
    action_id: str = Form(...),
    stock_code: str | None = Form(None),
):
    IN_Q.put({"action_id": action_id, "종목코드": stock_code})
    # 간단 알림 배너 조각 반환(HTMX swap)
    return HTMLResponse(
        """
        <div class="px-3 py-2 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200">
            명령 전송됨: <span class="font-semibold">{{action}}</span>
        </div>
        """.replace("{{action}}", action_id)
    )


@app.post("/settings", response_class=HTMLResponse)
async def update_settings(request: Request):
    form = await request.form()
    # 폼을 dict로 정리(체크박스/라디오/숫자 변환 포함)
    def to_bool(v):
        return True if str(v).lower() in ("1", "true", "on", "yes") else False

    payload = {
        "buyAmountLineEdit": form.get("buyAmountLineEdit", "200,000"),
        "marketBuyRadioButton": to_bool(form.get("marketBuyRadioButton")),
        "limitBuyRadioButton": to_bool(form.get("limitBuyRadioButton")),
        "marketSellRadioButton": to_bool(form.get("marketSellRadioButton")),
        "limitSellRadioButton": to_bool(form.get("limitSellRadioButton")),
        "stopLossCheckBox": to_bool(form.get("stopLossCheckBox")),
        "trailingStopCheckBox": to_bool(form.get("trailingStopCheckBox")),
        "limitBuySpinBox": int(form.get("limitBuySpinBox", 0)),
        "amendOrderSpinBox": int(form.get("amendOrderSpinBox", 60)),
        "maxAutoTradeCountSpinBox": int(form.get("maxAutoTradeCountSpinBox", 10)),
        "limitSellSpinBox": int(form.get("limitSellSpinBox", 0)),
        "stopLossDoubleSpinBox": float(form.get("stopLossDoubleSpinBox", -2.0)),
        "trailingStopDoubleSpinBox1": float(form.get("trailingStopDoubleSpinBox1", 2.0)),
        "trailingStopDoubleSpinBox2": float(form.get("trailingStopDoubleSpinBox2", -1.0)),
        "buyConditionComboBox": int(form.get("buyConditionComboBox", 0)),
        "sellConditionComboBox": int(form.get("sellConditionComboBox", 0)),
        "marketStartTimeEdit": form.get("marketStartTimeEdit", "090000"),
        "marketEndTimeEdit": form.get("marketEndTimeEdit", "153000"),
    }
    IN_Q.put({"action_id": "설정변경", "settings": payload})
    return HTMLResponse(
        """
        <div class="px-3 py-2 rounded-xl bg-sky-50 text-sky-700 border border-sky-200">
            설정을 업데이트했습니다.
        </div>
        """
    )

@app.get("/events")
async def sse_events():
    async def event_generator():
        loop = asyncio.get_event_loop()
        last_ping = loop.time()

        while True:
            await asyncio.sleep(0.01)

            # 하트비트(10초)
            now = loop.time()
            if now - last_ping > 10:
                last_ping = now
                yield b": ping\n\n"

            try:
                data = OUT_Q.get_nowait()
            except Empty:
                continue

            aid = data.get("action_id")

            if aid == "update_pandas_models":
                acc_html = df_to_html(
                    data.get("account_info_df", pd.DataFrame()),
                    table_id="account_info_table",
                    caption="계좌정보",
                )
                rt_html = df_to_html(
                    data.get("realtime_tracking_df", pd.DataFrame()),
                    table_id="realtime_tracking_table",
                    caption="자동매매 현황",
                )

                fragment = f"""
<div hx-swap-oob="true" id="account_info_panel">
  {acc_html}
</div>
<div hx-swap-oob="true" id="realtime_panel">
  {rt_html}
</div>
""".strip()
                yield sse_event("update_pandas_models", fragment)

            elif aid == "settings_loaded":

                S = data.get("settings", {})

                settings_json = json.dumps(S, ensure_ascii=False)

                fragment = f"""

            <div hx-swap-oob="true" id="__settings_inject__"

                 hx-on::load='

                  (function(){{

                    const S = {settings_json};


                    const setValue = (id, val) => {{

                      const el = document.getElementById(id);

                      if (!el) return;

                      if (el.type === "checkbox") el.checked = !!val;

                      else el.value = (val ?? "");

                    }};

                    const setRadioPair = (idA, idB, aChecked) => {{

                      const A = document.getElementById(idA);

                      const B = document.getElementById(idB);

                      if (A) A.checked = !!aChecked;

                      if (B) B.checked = !aChecked;

                    }};


                    // 일반 값 주입

                    setValue("buyAmountLineEdit", S.buyAmountLineEdit);

                    ["limitBuySpinBox","amendOrderSpinBox","maxAutoTradeCountSpinBox","limitSellSpinBox",

                     "stopLossDoubleSpinBox","trailingStopDoubleSpinBox1","trailingStopDoubleSpinBox2"]

                     .forEach(k=>setValue(k, S[k]));

                    setValue("marketStartTimeEdit", S.marketStartTimeEdit);

                    setValue("marketEndTimeEdit",   S.marketEndTimeEdit);

                    ["stopLossCheckBox","trailingStopCheckBox"].forEach(k=>setValue(k, S[k]));

                    setRadioPair("marketBuyRadioButton","limitBuyRadioButton",!!S.marketBuyRadioButton);

                    setRadioPair("marketSellRadioButton","limitSellRadioButton",!!S.marketSellRadioButton);


                    // hidden 동기화

                    (function syncHidden(){{

                      const mb  = document.getElementById("marketBuyRadioButton");

                      const ms  = document.getElementById("marketSellRadioButton");

                      const mbH = document.getElementById("marketBuyHidden");

                      const lbH = document.getElementById("limitBuyHidden");

                      const msH = document.getElementById("marketSellHidden");

                      const lsH = document.getElementById("limitSellHidden");

                      if (mb && mbH && lbH) {{ mbH.value = mb.checked ? "on" : ""; lbH.value = mb.checked ? "" : "on"; }}

                      if (ms && msH && lsH) {{ msH.value = ms.checked ? "on" : ""; lsH.value = ms.checked ? "" : "on"; }}

                    }})();


                    // ✅ 콤보 선호 상태: 기존값이 있으면 유지, 없으면 settings 값을 초기값으로

                    const cur = window.__comboDesired || {{}};

                    if (typeof cur.buyIndex  === "undefined") cur.buyIndex  = (S.buyConditionComboBox ?? 0);

                    if (typeof cur.sellIndex === "undefined") cur.sellIndex = (S.sellConditionComboBox ?? 0);

                    window.__comboDesired = cur;


                    // 목록이 이미 렌더된 상태라면 즉시 적용 시도

                    (function applyIfReady(){{

                      const pref = window.__comboDesired || {{}};

                      function apply(sel, which){{

                        if (!sel || !sel.options || sel.options.length === 0) return;

                        // 이름 우선, 없으면 인덱스

                        if (pref[which+"Name"]) {{

                          const v = pref[which+"Name"];

                          for (let i=0;i<sel.options.length;i++) {{

                            if (sel.options[i].value === v) {{ sel.selectedIndex = i; return; }}

                          }}

                        }}

                        if (Number.isInteger(pref[which+"Index"])) {{

                          const idx = pref[which+"Index"];

                          if (idx >= 0 && idx < sel.options.length) sel.selectedIndex = idx;

                        }}

                      }}

                      apply(document.getElementById("buyConditionComboBox"),  "buy");

                      apply(document.getElementById("sellConditionComboBox"), "sell");

                    }})();


                    // (선택) 자동매매 버튼 색 동기화

                    if (typeof S.autoTradeOn !== "undefined") {{

                      const setActive = (el, active) => {{

                        const activeCls = ["bg-indigo-600","text-white","border-indigo-600","hover:bg-indigo-700"];

                        const idleCls   = ["bg-gray-50","text-gray-700","border-gray-200","hover:bg-gray-100"];

                        const all = activeCls.concat(idleCls);

                        el.classList.remove(...all);

                        el.classList.add("px-4","py-2","rounded-xl","border","text-sm","font-medium","transition","hover:shadow");

                        (active ? activeCls : idleCls).forEach(c=>el.classList.add(c));

                      }};

                      const on  = document.getElementById("btn-on");

                      const off = document.getElementById("btn-off");

                      if (on && off) {{ setActive(on, !!S.autoTradeOn); setActive(off, !S.autoTradeOn); }}

                    }}

                  }})();

                 '>

            </div>

            """.strip()

                yield sse_event("settings_loaded", fragment)

            elif aid == "on_receive_condition_list":
                names = data.get("조건명리스트", [])

                buy_idx = data.get("buy_index")  # 예: 3  (없으면 None)

                sell_idx = data.get("sell_index")  # 예: 1  (없으면 None)


                def build_options(selected_idx):
                    if not names:
                        return "<option value='0'>조건식 없음</option>"

                    opts = []

                    for i, name in enumerate(names):
                        sel = " selected" if (selected_idx is not None and i == int(selected_idx)) else ""

                        opts.append(f"<option value='{i}' data-name='{name}'{sel}>{name}</option>")

                    return "".join(opts)


                buy_options = build_options(buy_idx)

                sell_options = build_options(sell_idx)

                fragment = f"""
                
                <div hx-swap-oob="true" id="buyConditionComboBox">
                
                  <select id="buyConditionComboBox" name="buyConditionComboBox"
                
                          class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                
                    {buy_options}
                
                  </select>
                
                </div>
                
                <div hx-swap-oob="true" id="sellConditionComboBox">
                
                  <select id="sellConditionComboBox" name="sellConditionComboBox"
                
                          class="w-full px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                
                    {sell_options}
                
                  </select>
                
                </div>
                
                <script>
                
                (function(){{
                
                  // 선택 상태를 선호값으로 기록(이후 재로드/재수신에도 유지)
                
                  const buySel  = document.getElementById("buyConditionComboBox");
                
                  const sellSel = document.getElementById("sellConditionComboBox");
                
                
                  function save(which, sel){{
                
                    if (!sel || !sel.options || sel.selectedIndex < 0) return;
                
                    const opt = sel.options[sel.selectedIndex];
                
                    window.__comboDesired = Object.assign({{}}, window.__comboDesired, {{
                
                      [which+"Index"]: sel.selectedIndex,
                
                      [which+"Name"]:  opt ? (opt.dataset.name || opt.text) : undefined
                
                    }});
                
                  }}
                
                  // 서버가 인덱스를 줬다면 이미 selected 반영됨 → 그 값을 곧바로 저장
                
                  save("buy",  buySel);
                
                  save("sell", sellSel);
                
                
                  // 사용자가 바꾸면 갱신
                
                  if (buySel)  buySel.addEventListener("change", ()=>save("buy",  buySel));
                
                  if (sellSel) sellSel.addEventListener("change", ()=>save("sell", sellSel));
                
                
                  // 서버 인덱스가 없고(=null) 예전 pending 인덱스가 있으면 fallback 적용
                
                  const provided = {{ buy: {'null' if buy_idx is None else int(buy_idx)},
                
                                      sell: {'null' if sell_idx is None else int(sell_idx)} }};
                
                  const p = window.__pendingComboIndex || {{buy:0, sell:0}};
                
                  if (provided.buy === null && buySel && buySel.options.length > p.buy)  buySel.selectedIndex  = p.buy,  save("buy",  buySel);
                
                  if (provided.sell === null && sellSel && sellSel.options.length > p.sell) sellSel.selectedIndex = p.sell, save("sell", sellSel);
                
                }})();
                
                </script>
                
                """.strip()

                yield sse_event("on_receive_condition_list", fragment)
            else:
                yield sse_event("misc", json.dumps(data, ensure_ascii=False))

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
        "Connection": "keep-alive",
    }
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
    )
