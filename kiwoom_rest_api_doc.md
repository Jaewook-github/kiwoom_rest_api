# 키움증권 API 문서

## 국내주식 REST API

### ELW

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |

### ELW일별민감도지표요청 (ka10048)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| elwdaly_snst_ix        | ELW일별민감도지표    | LIST   | N        |        |             |
| - dt                   | 일자                 | String | N        | 20     |             |
| - iv                   | IV                   | String | N        | 20     |             |
| - delta                | 델타                 | String | N        | 20     |             |
| - gam                  | 감마                 | String | N        | 20     |             |
| - theta                | 쎄타                 | String | N        | 20     |             |
| - vega                 | 베가                 | String | N        | 20     |             |
| - law                  | 로                   | String | N        | 20     |             |
| - lp                   | LP                   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "57JBHH"
}
```

#### 응답 예시

```json
{
	"elwdaly_snst_ix":
		[
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			},
			{
				"dt":"000000",
				"iv":"1901",
				"delta":"126664",
				"gam":"5436",
				"theta":"-5271886",
				"vega":"41752995",
				"law":"13982453",
				"lp":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW민감도지표요청 (ka10050)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| elwsnst_ix_array       | ELW민감도지표배열    | LIST   | N        |        |             |
| - cntr_tm              | 체결시간             | String | N        | 20     |             |
| - cur_prc              | 현재가               | String | N        | 20     |             |
| - elwtheory_pric       | ELW이론가            | String | N        | 20     |             |
| - iv                   | IV                   | String | N        | 20     |             |
| - delta                | 델타                 | String | N        | 20     |             |
| - gam                  | 감마                 | String | N        | 20     |             |
| - theta                | 쎄타                 | String | N        | 20     |             |
| - vega                 | 베가                 | String | N        | 20     |             |
| - law                  | 로                   | String | N        | 20     |             |
| - lp                   | LP                   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "57JBHH"
}
```

#### 응답 예시

```json
{
	"elwsnst_ix_array":
		[
			{
				"cntr_tm":"095820",
				"cur_prc":"5",
				"elwtheory_pric":"4",
				"iv":"3336",
				"delta":"7128",
				"gam":"904",
				"theta":"-2026231",
				"vega":"1299294",
				"law":"95218",
				"lp":"0"
			},
			{
				"cntr_tm":"095730",
				"cur_prc":"5",
				"elwtheory_pric":"4",
				"iv":"3342",
				"delta":"7119",
				"gam":"902",
				"theta":"-2026391",
				"vega":"1297498",
				"law":"95078",
				"lp":"0"
			},
			{
				"cntr_tm":"095640",
				"cur_prc":"5",
				"elwtheory_pric":"4",
				"iv":"3345",
				"delta":"7114",
				"gam":"900",
				"theta":"-2026285",
				"vega":"1296585",
				"law":"95012",
				"lp":"0"
			},
			{
				"cntr_tm":"095550",
				"cur_prc":"5",
				"elwtheory_pric":"4",
				"iv":"3346",
				"delta":"7111",
				"gam":"900",
				"theta":"-2026075",
				"vega":"1296025",
				"law":"94974",
				"lp":"0"
			},
			{
				"cntr_tm":"095500",
				"cur_prc":"5",
				"elwtheory_pric":"4",
				"iv":"3339",
				"delta":"7121",
				"gam":"902",
				"theta":"-2025002",
				"vega":"1298269",
				"law":"95168",
				"lp":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW가격급등락요청 (ka30001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element              | 한글명             | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------- | ------------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| flu_tp               | 등락구분           | String | Y        | 1      | 1:급등, 2:급락                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| tm_tp                | 시간구분           | String | Y        | 1      | 1:분전, 2:일전                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| tm                   | 시간               | String | Y        | 2      | 분 혹은 일입력 (예 1, 3, 5)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| trde_qty_tp          | 거래량구분         | String | Y        | 4      | 0:전체, 10:만주이상, 50:5만주이상, 100:10만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| isscomp_cd           | 발행사코드         | String | Y        | 12     | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| bsis_aset_cd         | 기초자산코드       | String | Y        | 12     | 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| rght_tp              | 권리구분           | String | Y        | 3      | 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 005:EX, 006:조기종료콜, 007:조기종료풋                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| lpcd                 | LP코드             | String | Y        | 12     | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| trde_end_elwskip     | 거래종료ELW제외    | String | Y        | 1      | 0:포함, 1:제외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| base_pric_tm                   | 기준가시간               | String | N        | 20     |             |
| elwpric_jmpflu                 | ELW가격급등락            | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - rank                         | 순위                     | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - pre_sig                      | 대비기호                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - trde_end_elwbase_pric        | 거래종료ELW기준가        | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - base_pre                     | 기준대비                 | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - jmp_rt                       | 급등율                   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"flu_tp": "1",
	"tm_tp": "2",
	"tm": "1",
	"trde_qty_tp": "0",
	"isscomp_cd": "000000000000",
	"bsis_aset_cd": "000000000000",
	"rght_tp": "000",
	"lpcd": "000000000000",
	"trde_end_elwskip": "0"
}
```

#### 응답 예시

```json
{
	"base_pric_tm":"기준가(11/21)",
	"elwpric_jmpflu":
		[
			{
			"stk_cd":"57JBHH",
			"rank":"1",
			"stk_nm":"한국JBHHKOSPI200풋",
			"pre_sig":"2",
			"pred_pre":"+10",
			"trde_end_elwbase_pric":"20",
			"cur_prc":"+30",
			"base_pre":"10",
			"trde_qty":"30",
			"jmp_rt":"+50.00"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 거래원별ELW순매매상위요청 (ka30002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element              | 한글명             | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------- | ------------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| isscomp_cd           | 발행사코드         | String | Y        | 3      | 3자리, 영웅문4 0273화면참조 (교보:001, 신한금융투자:002, 한국투자증권:003, 대신:004, 미래대우:005, ,,,)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_qty_tp          | 거래량구분         | String | Y        | 4      | 0:전체, 5:5천주, 10:만주, 50:5만주, 100:10만주, 500:50만주, 1000:백만주                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_tp              | 매매구분           | String | Y        | 1      | 1:순매수, 2:순매도                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| dt                   | 기간               | String | Y        | 2      | 1:전일, 5:5일, 10:10일, 40:40일, 60:60일                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| trde_end_elwskip     | 거래종료ELW제외    | String | Y        | 1      | 0:포함, 1:제외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| trde_ori_elwnettrde_upper      | 거래원별ELW순매매상위    | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - stkpc_flu                    | 주가등락                 | String | N        | 20     |             |
| - flu_rt                       | 등락율                   | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - netprps                      | 순매수                   | String | N        | 20     |             |
| - buy_trde_qty                 | 매수거래량               | String | N        | 20     |             |
| - sel_trde_qty                 | 매도거래량               | String | N        | 20     |             |

#### 요청 예시

```json
{
	"isscomp_cd": "003",
	"trde_qty_tp": "0",
	"trde_tp": "2",
	"dt": "60",
	"trde_end_elwskip": "0"
}
```

#### 응답 예시

```json
{
	"trde_ori_elwnettrde_upper":
		[
			{
				"stk_cd":"57JBHH",
				"stk_nm":"한국JBHHKOSPI200풋",
				"stkpc_flu":"--3140",
				"flu_rt":"-88.95",
				"trde_qty":"500290",
				"netprps":"--846970",
				"buy_trde_qty":"+719140",
				"sel_trde_qty":"-1566110"
			},
			{
				"stk_cd":"57JBHH",
				"stk_nm":"한국JBHHKOSPI200풋",
				"stkpc_flu":"+205",
				"flu_rt":"+73.21",
				"trde_qty":"4950000",
				"netprps":"--108850",
				"buy_trde_qty":"+52450",
				"sel_trde_qty":"-161300"
			},
			{
				"stk_cd":"57JBHH",
				"stk_nm":"한국JBHHKOSPI200풋",
				"stkpc_flu":"+340",
				"flu_rt":"+115.25",
				"trde_qty":"60",
				"netprps":"--73960",
				"buy_trde_qty":"+29560",
				"sel_trde_qty":"-103520"
			},
			{
				"stk_cd":"57JBHH",
				"stk_nm":"한국JBHHKOSPI200풋",
				"stkpc_flu":"--65",
				"flu_rt":"-86.67",
				"trde_qty":"20",
				"netprps":"--23550",
				"buy_trde_qty":"+422800",
				"sel_trde_qty":"-446350"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELWLP보유일별추이요청 (ka30003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                             |
| -------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| bsis_aset_cd   | 기초자산코드 | String | Y        | 12     |                                                                                         |
| base_dt        | 기준일자     | String | Y        | 8      | YYYYMMDD                                                                                |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| ---------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| elwlpposs_daly_trnsn       | ELWLP보유일별추이    | LIST   | N        |        |             |
| - dt                       | 일자                 | String | N        | 20     |             |
| - cur_prc                  | 현재가               | String | N        | 20     |             |
| - pre_tp                   | 대비구분             | String | N        | 20     |             |
| - pred_pre                 | 전일대비             | String | N        | 20     |             |
| - flu_rt                   | 등락율               | String | N        | 20     |             |
| - trde_qty                 | 거래량               | String | N        | 20     |             |
| - trde_prica               | 거래대금             | String | N        | 20     |             |
| - chg_qty                  | 변동수량             | String | N        | 20     |             |
| - lprmnd_qty               | LP보유수량           | String | N        | 20     |             |
| - wght                     | 비중                 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"bsis_aset_cd": "57KJ99",
	"base_dt": "20241122"
}
```

#### 응답 예시

```json
{
	"elwlpposs_daly_trnsn":
		[
			{
				"dt":"20241122",
				"cur_prc":"-125700",
				"pre_tp":"5",
				"pred_pre":"-900",
				"flu_rt":"-0.71",
				"trde_qty":"54",
				"trde_prica":"7",
				"chg_qty":"0",
				"lprmnd_qty":"0",
				"wght":"0.00"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW괴리율요청 (ka30004)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element              | 한글명             | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------- | ------------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| isscomp_cd           | 발행사코드         | String | Y        | 12     | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| bsis_aset_cd         | 기초자산코드       | String | Y        | 12     | 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200..                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| rght_tp              | 권리구분           | String | Y        | 3      | 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 005:EX, 006:조기종료콜, 007:조기종료풋                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| lpcd                 | LP코드             | String | Y        | 12     | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| trde_end_elwskip     | 거래종료ELW제외    | String | Y        | 1      | 1:거래종료ELW제외, 0:거래종료ELW포함                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| elwdispty_rt                   | ELW괴리율                | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - isscomp_nm                   | 발행사명                 | String | N        | 20     |             |
| - sqnc                         | 회차                     | String | N        | 20     |             |
| - base_aset_nm                 | 기초자산명               | String | N        | 20     |             |
| - rght_tp                      | 권리구분                 | String | N        | 20     |             |
| - dispty_rt                    | 괴리율                   | String | N        | 20     |             |
| - basis                        | 베이시스                 | String | N        | 20     |             |
| - srvive_dys                   | 잔존일수                 | String | N        | 20     |             |
| - theory_pric                  | 이론가                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pre_tp                       | 대비구분                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락율                   | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"isscomp_cd": "000000000000",
	"bsis_aset_cd": "000000000000",
	"rght_tp": "000",
	"lpcd": "000000000000",
	"trde_end_elwskip": "0"
}
```

#### 응답 예시

```json
{
	"elwdispty_rt":
		[
			{
				"stk_cd":"57JBHH",
				"isscomp_nm":"키움증권",
				"sqnc":"KK27",
				"base_aset_nm":"삼성전자",
				"rght_tp":"콜",
				"dispty_rt":"0",
				"basis":"+5.00",
				"srvive_dys":"21",
				"theory_pric":"0",
				"cur_prc":"5",
				"pre_tp":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"trde_qty":"0",
				"stk_nm":"한국JBHHKOSPI200풋"
			},
			{
				"stk_cd":"57JBHH",
				"isscomp_nm":"키움증권",
				"sqnc":"KL57",
				"base_aset_nm":"삼성전자",
				"rght_tp":"콜",
				"dispty_rt":"0",
				"basis":"+10.00",
				"srvive_dys":"49",
				"theory_pric":"0",
				"cur_prc":"10",
				"pre_tp":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"trde_qty":"0",
				"stk_nm":"한국JBHHKOSPI200풋"
			},
			{
				"stk_cd":"57JBHH",
				"isscomp_nm":"키움증권",
				"sqnc":"KK28",
				"base_aset_nm":"삼성전자",
				"rght_tp":"콜",
				"dispty_rt":"0",
				"basis":"+5.00",
				"srvive_dys":"49",
				"theory_pric":"0",
				"cur_prc":"5",
				"pre_tp":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"trde_qty":"0",
				"stk_nm":"한국JBHHKOSPI200풋"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW조건검색요청 (ka30005)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                             |
| -------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| isscomp_cd     | 발행사코드   | String | Y        | 12     | 12자리입력(전체:000000000000, 한국투자증권:000,,,3, 미래대우:000,,,5, 신영:000,,,6, NK투자증권:000,,,12, KB증권:000,,,17)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| bsis_aset_cd   | 기초자산코드 | String | Y        | 12     | 전체일때만 12자리입력(전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼정전자:005930, KT:030200,,)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| rght_tp        | 권리구분     | String | Y        | 1      | 0:전체, 1:콜, 2:풋, 3:DC, 4:DP, 5:EX, 6:조기종료콜, 7:조기종료풋                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| lpcd           | LP코드       | String | Y        | 12     | 전체일때만 12자리입력(전체:000000000000, 한국투자증권:003, 미래대우:005, 신영:006, NK투자증권:012, KB증권:017)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| sort_tp        | 정렬구분     | String | Y        | 1      | 0:정렬없음, 1:상승율순, 2:상승폭순, 3:하락율순, 4:하락폭순, 5:거래량순, 6:거래대금순, 7:잔존일순                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| elwcnd_qry                     | ELW조건검색              | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - isscomp_nm                   | 발행사명                 | String | N        | 20     |             |
| - sqnc                         | 회차                     | String | N        | 20     |             |
| - base_aset_nm                 | 기초자산명               | String | N        | 20     |             |
| - rght_tp                      | 권리구분                 | String | N        | 20     |             |
| - expr_dt                      | 만기일                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pre_tp                       | 대비구분                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락율                   | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - trde_qty_pre                 | 거래량대비               | String | N        | 20     |             |
| - trde_prica                   | 거래대금                 | String | N        | 20     |             |
| - pred_trde_qty                | 전일거래량               | String | N        | 20     |             |
| - sel_bid                      | 매도호가                 | String | N        | 20     |             |
| - buy_bid                      | 매수호가                 | String | N        | 20     |             |
| - prty                         | 패리티                   | String | N        | 20     |             |
| - gear_rt                      | 기어링비율               | String | N        | 20     |             |
| - pl_qutr_rt                   | 손익분기율               | String | N        | 20     |             |
| - cfp                          | 자본지지점               | String | N        | 20     |             |
| - theory_pric                  | 이론가                   | String | N        | 20     |             |
| - innr_vltl                    | 내재변동성               | String | N        | 20     |             |
| - delta                        | 델타                     | String | N        | 20     |             |
| - lvrg                         | 레버리지                 | String | N        | 20     |             |
| - exec_pric                    | 행사가격                 | String | N        | 20     |             |
| - cnvt_rt                      | 전환비율                 | String | N        | 20     |             |
| - lpposs_rt                    | LP보유비율               | String | N        | 20     |             |
| - pl_qutr_pt                   | 손익분기점               | String | N        | 20     |             |
| - fin_trde_dt                  | 최종거래일               | String | N        | 20     |             |
| - flo_dt                       | 상장일                   | String | N        | 20     |             |
| - lpinitlast_suply_dt          | LP초종공급일             | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - srvive_dys                   | 잔존일수                 | String | N        | 20     |             |
| - dispty_rt                    | 괴리율                   | String | N        | 20     |             |
| - lpmmcm_nm                    | LP회원사명               | String | N        | 20     |             |
| - lpmmcm_nm_1                  | LP회원사명1              | String | N        | 20     |             |
| - lpmmcm_nm_2                  | LP회원사명2              | String | N        | 20     |             |
| - xraymont_cntr_qty_arng_trde_tp | Xray순간체결량정리매매구분 | String | N        | 20     |             |
| - xraymont_cntr_qty_profa_100tp | Xray순간체결량증거금100구분 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"isscomp_cd": "000000000017",
	"bsis_aset_cd": "201",
	"rght_tp": "1",
	"lpcd": "000000000000",
	"sort_tp": "0"
}
```

#### 응답 예시

```json
{
	"elwcnd_qry":
		[
			{
				"stk_cd":"57JBHH",
				"isscomp_nm":"키움증권",
				"sqnc":"K411",
				"base_aset_nm":"KOSPI200",
				"rght_tp":"콜",
				"expr_dt":"20241216",
				"cur_prc":"15",
				"pre_tp":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"trde_qty":"0",
				"trde_qty_pre":"0.00",
				"trde_prica":"0",
				"pred_trde_qty":"0",
				"sel_bid":"0",
				"buy_bid":"0",
				"prty":"90.10",
				"gear_rt":"2267.53",
				"pl_qutr_rt":"+11.03",
				"cfp":"",
				"theory_pric":"65637",
				"innr_vltl":"2015",
				"delta":"282426",
				"lvrg":"640.409428",
				"exec_pric":"377.50",
				"cnvt_rt":"100.0000",
				"lpposs_rt":"+99.90",
				"pl_qutr_pt":"+377.65",
				"fin_trde_dt":"20241212",
				"flo_dt":"20240320",
				"lpinitlast_suply_dt":"20241212",
				"stk_nm":"한국JBHHKOSPI200풋",
				"srvive_dys":"21",
				"dispty_rt":"--97.71",
				"lpmmcm_nm":"키움증권",
				"lpmmcm_nm_1":"0.00",
				"lpmmcm_nm_2":"",
				"xraymont_cntr_qty_arng_trde_tp":"",
				"xraymont_cntr_qty_profa_100tp":""
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW등락율순위요청 (ka30009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                             |
| -------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| sort_tp        | 정렬구분     | String | Y        | 1      | 1:상승률, 2:상승폭, 3:하락률, 4:하락폭                                                |
| rght_tp        | 권리구분     | String | Y        | 3      | 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 006:조기종료콜, 007:조기종료풋                |
| trde_end_skip  | 거래종료제외 | String | Y        | 1      | 0:거래종료포함, 1:거래종료제외                                                          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| elwflu_rt_rank                 | ELW등락율순위            | LIST   | N        |        |             |
| - rank                         | 순위                     | String | N        | 20     |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pre_sig                      | 대비기호                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락률                   | String | N        | 20     |             |
| - sel_req                      | 매도잔량                 | String | N        | 20     |             |
| - buy_req                      | 매수잔량                 | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - trde_prica                   | 거래대금                 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"sort_tp": "1",
	"rght_tp": "000",
	"trde_end_skip": "0"
}
```

#### 응답 예시

```json
{
	"elwflu_rt_rank":
		[
			{
				"rank":"1",
				"stk_cd":"57JBHH",
				"stk_nm":"한국JBHHKOSPI200풋",
				"cur_prc":"+30",
				"pre_sig":"2",
				"pred_pre":"+10",
				"flu_rt":"+50.00",
				"sel_req":"0",
				"buy_req":"0",
				"trde_qty":"30",
				"trde_prica":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW잔량순위요청 (ka30010)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                             |
| -------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| sort_tp        | 정렬구분     | String | Y        | 1      | 1:순매수잔량상위, 2: 순매도 잔량상위                                                |
| rght_tp        | 권리구분     | String | Y        | 3      | 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 006:조기종료콜, 007:조기종료풋                |
| trde_end_skip  | 거래종료제외 | String | Y        | 1      | 1:거래종료제외, 0:거래종료포함                                                          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| elwreq_rank                    | ELW잔량순위              | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - rank                         | 순위                     | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pre_sig                      | 대비기호                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락률                   | String | N        | 20     |             |
| - trde_qty                     | 거래량                   | String | N        | 20     |             |
| - sel_req                      | 매도잔량                 | String | N        | 20     |             |
| - buy_req                      | 매수잔량                 | String | N        | 20     |             |
| - netprps_req                  | 순매수잔량               | String | N        | 20     |             |
| - trde_prica                   | 거래대금                 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"sort_tp": "1",
	"rght_tp": "000",
	"trde_end_skip": "0"
}
```

#### 응답 예시

```json
{
	"elwreq_rank":
		[
			{
				"stk_cd":"57JBHH",
				"rank":"1",
				"stk_nm":"한국JBHHKOSPI200풋",
				"cur_prc":"170",
				"pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"trde_qty":"0",
				"sel_req":"0",
				"buy_req":"20",
				"netprps_req":"20",
				"trde_prica":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW근접율요청 (ka30011)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| elwalacc_rt                    | ELW근접율                | LIST   | N        |        |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pre_sig                      | 대비기호                 | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락율                   | String | N        | 20     |             |
| - acc_trde_qty                 | 누적거래량               | String | N        | 20     |             |
| - alacc_rt                     | 근접율                   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "57JBHH"
}
```

#### 응답 예시

```json
{
	"elwalacc_rt":
		[
			{
				"stk_cd":"201",
				"stk_nm":"KOSPI200",
				"cur_prc":"+431.78",
				"pre_sig":"2",
				"pred_pre":"+0.03",
				"flu_rt":"+0.01",
				"acc_trde_qty":"31",
				"alacc_rt":"0.00"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### ELW종목상세정보요청 (ka30012)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/elw
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                      | 한글명                 | Type   | Required | Length | Description |
| ---------------------------- | ---------------------- | ------ | -------- | ------ | ----------- |
| aset_cd                      | 자산코드               | String | N        | 20     |             |
| cur_prc                      | 현재가                 | String | N        | 20     |             |
| pred_pre_sig                 | 전일대비기호           | String | N        | 20     |             |
| pred_pre                     | 전일대비               | String | N        | 20     |             |
| flu_rt                       | 등락율                 | String | N        | 20     |             |
| lpmmcm_nm                    | LP회원사명             | String | N        | 20     |             |
| lpmmcm_nm_1                  | LP회원사명1            | String | N        | 20     |             |
| lpmmcm_nm_2                  | LP회원사명2            | String | N        | 20     |             |
| elwrght_cntn                 | ELW권리내용            | String | N        | 20     |             |
| elwexpr_evlt_pric            | ELW만기평가가격        | String | N        | 20     |             |
| elwtheory_pric               | ELW이론가              | String | N        | 20     |             |
| dispty_rt                    | 괴리율                 | String | N        | 20     |             |
| elwinnr_vltl                 | ELW내재변동성          | String | N        | 20     |             |
| exp_rght_pric                | 예상권리가             | String | N        | 20     |             |
| elwpl_qutr_rt                | ELW손익분기율          | String | N        | 20     |             |
| elwexec_pric                 | ELW행사가              | String | N        | 20     |             |
| elwcnvt_rt                   | ELW전환비율            | String | N        | 20     |             |
| elwcmpn_rt                   | ELW보상율              | String | N        | 20     |             |
| elwpric_rising_part_rt       | ELW가격상승참여율      | String | N        | 20     |             |
| elwrght_type                 | ELW권리유형            | String | N        | 20     |             |
| elwsrvive_dys                | ELW잔존일수            | String | N        | 20     |             |
| stkcnt                       | 주식수                 | String | N        | 20     |             |
| elwlpord_pos                 | ELWLP주문가능          | String | N        | 20     |             |
| lpposs_rt                    | LP보유비율             | String | N        | 20     |             |
| lprmnd_qty                   | LP보유수량             | String | N        | 20     |             |
| elwspread                    | ELW스프레드            | String | N        | 20     |             |
| elwprty                      | ELW패리티              | String | N        | 20     |             |
| elwgear                      | ELW기어링              | String | N        | 20     |             |
| elwflo_dt                    | ELW상장일              | String | N        | 20     |             |
| elwfin_trde_dt               | ELW최종거래일          | String | N        | 20     |             |
| expr_dt                      | 만기일                 | String | N        | 20     |             |
| exec_dt                      | 행사일                 | String | N        | 20     |             |
| lpsuply_end_dt               | LP공급종료일           | String | N        | 20     |             |
| elwpay_dt                    | ELW지급일              | String | N        | 20     |             |
| elwinvt_ix_comput            | ELW투자지표산출        | String | N        |        |             |
| elwpay_agnt                  | ELW지급대리인          | String | N        |        |             |
| elwappr_way                  | ELW결재방법            | String | N        |        |             |
| elwrght_exec_way             | ELW권리행사방식        | String | N        |        |             |
| elwpblicte_orgn              | ELW발행기관            | String | N        |        |             |
| dcsn_pay_amt                 | 확정지급액             | String | N        |        |             |
| kobarr                       | KO베리어               | String | N        |        |             |
| iv                           | IV                     | String | N        |        |             |
| clsprd_end_elwocr            | 종기종료ELW발생        | String | N        |        |             |
| bsis_aset_1                  | 기초자산1              | String | N        |        |             |
| bsis_aset_comp_rt_1          | 기초자산구성비율1      | String | N        |        |             |
| bsis_aset_2                  | 기초자산2              | String | N        |        |             |
| bsis_aset_comp_rt_2          | 기초자산구성비율2      | String | N        |        |             |
| bsis_aset_3                  | 기초자산3              | String | N        |        |             |
| bsis_aset_comp_rt_3          | 기초자산구성비율3      | String | N        |        |             |
| bsis_aset_4                  | 기초자산4              | String | N        |        |             |
| bsis_aset_comp_rt_4          | 기초자산구성비율4      | String | N        |        |             |
| bsis_aset_5                  | 기초자산5              | String | N        |        |             |
| bsis_aset_comp_rt_5          | 기초자산구성비율5      | String | N        |        |             |
| fr_dt                        | 평가시작일자           | String | N        |        |             |
| to_dt                        | 평가종료일자           | String | N        |        |             |
| fr_tm                        | 평가시작시간           | String | N        |        |             |
| evlt_end_tm                  | 평가종료시간           | String | N        |        |             |
| evlt_pric                    | 평가가격               | String | N        |        |             |
| evlt_fnsh_yn                 | 평가완료여부           | String | N        |        |             |
| all_hgst_pric                | 전체최고가             | String | N        |        |             |
| all_lwst_pric                | 전체최저가             | String | N        |        |             |
| imaf_hgst_pric               | 직후최고가             | String | N        |        |             |
| imaf_lwst_pric               | 직후최저가             | String | N        |        |             |
| sndhalf_mrkt_hgst_pric       | 후반장최고가           | String | N        |        |             |
| sndhalf_mrkt_lwst_pric       | 후반장최저가           | String | N        |        |             |

#### 요청 예시

```json
{
	"stk_cd": "57JBHH"
}
```

#### 응답 예시

```json
{
	"aset_cd":"201",
	"cur_prc":"10",
	"pred_pre_sig":"3",
	"pred_pre":"0",
	"flu_rt":"0.00",
	"lpmmcm_nm":"",
	"lpmmcm_nm_1":"키움증권",
	"lpmmcm_nm_2":"",
	"elwrght_cntn":"만기평가가격이 행사가격 초과인 경우,\n\t 1워런트당 (만기평가가격-행사가격)*전환비율",
	"elwexpr_evlt_pric":"최종거래일 종가",
	"elwtheory_pric":"27412",
	"dispty_rt":"--96.35",
	"elwinnr_vltl":"1901",
	"exp_rght_pric":"3179.00",
	"elwpl_qutr_rt":"--7.33",
	"elwexec_pric":"400.00",
	"elwcnvt_rt":"100.0000",
	"elwcmpn_rt":"0.00",
	"elwpric_rising_part_rt":"0.00",
	"elwrght_type":"CALL",
	"elwsrvive_dys":"15",
	"stkcnt":"8000",
	"elwlpord_pos":"가능",
	"lpposs_rt":"+95.20",
	"lprmnd_qty":"7615830",
	"elwspread":"15.00",
	"elwprty":"107.94",
	"elwgear":"4317.90",
	"elwflo_dt":"20240124",
	"elwfin_trde_dt":"20241212",
	"expr_dt":"20241216",
	"exec_dt":"20241216",
	"lpsuply_end_dt":"20241212",
	"elwpay_dt":"20241218",
	"elwinvt_ix_comput":"산출종목",
	"elwpay_agnt":"국민은행증권타운지점",
	"elwappr_way":"현금 결제",
	"elwrght_exec_way":"유럽형",
	"elwpblicte_orgn":"키움증권(주)",
	"dcsn_pay_amt":"0.000",
	"kobarr":"0",
	"iv":"0.00",
	"clsprd_end_elwocr":"",
	"bsis_aset_1":"KOSPI200",
	"bsis_aset_comp_rt_1":"0.00",
	"bsis_aset_2":"",
	"bsis_aset_comp_rt_2":"0.00",
	"bsis_aset_3":"",
	"bsis_aset_comp_rt_3":"0.00",
	"bsis_aset_4":"",
	"bsis_aset_comp_rt_4":"0.00",
	"bsis_aset_5":"",
	"bsis_aset_comp_rt_5":"0.00",
	"fr_dt":"",
	"to_dt":"",
	"fr_tm":"",
	"evlt_end_tm":"",
	"evlt_pric":"",
	"evlt_fnsh_yn":"",
	"all_hgst_pric":"0.00",
	"all_lwst_pric":"0.00",
	"imaf_hgst_pric":"0.00",
	"imaf_lwst_pric":"0.00",
	"sndhalf_mrkt_hgst_pric":"0.00",
	"sndhalf_mrkt_lwst_pric":"0.00",
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### ETF

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| ETF수익율요청 | ka40001 | ETF 수익률 정보 조회 |
| ETF종목정보요청 | ka40002 | ETF 종목 정보 조회 |
| ETF일별추이요청 | ka40003 | ETF 일별 추이 정보 조회 |
| ETF전체시세요청 | ka40004 | ETF 전체 시세 정보 조회 |
| ETF시간대별추이요청 | ka40006 | ETF 시간대별 추이 정보 조회 |
| ETF시간대별체결요청 | ka40007 | ETF 시간대별 체결 정보 조회 |
| ETF일자별체결요청 | ka40008 | ETF 일자별 체결 정보 조회 |
| ETF시간대별체결요청 | ka40009 | ETF 시간대별 체결 정보 조회 |
| ETF시간대별추이요청 | ka40010 | ETF 시간대별 추이 정보 조회 |

### ETF수익율요청 (ka40001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element            | 한글명           | Type   | Required | Length | Description                   |
| ------------------ | ---------------- | ------ | -------- | ------ | ----------------------------- |
| stk_cd             | 종목코드         | String | Y        | 6      |                               |
| etfobjt_idex_cd    | ETF대상지수코드  | String | Y        | 3      |                               |
| dt                 | 기간             | String | Y        | 1      | 0:1주, 1:1달, 2:6개월, 3:1년  |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| etfprft_rt_lst                 | ETF수익율                | LIST   | N        |        |             |
| - etfprft_rt                   | ETF수익률                | String | N        | 20     |             |
| - cntr_prft_rt                 | 체결수익률               | String | N        | 20     |             |
| - for_netprps_qty              | 외인순매수수량           | String | N        | 20     |             |
| - orgn_netprps_qty             | 기관순매수수량           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500",
	"etfobjt_idex_cd": "207",
	"dt": "3"
}
```

#### 응답 예시

```json
{
	"etfprft_rt_lst":
		[
			{
				"etfprft_rt":"-1.33",
				"cntr_prft_rt":"-1.75",
				"for_netprps_qty":"0",
				"orgn_netprps_qty":""
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF종목정보요청 (ka40002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description |
| ------------------ | ---------------- | ------ | -------- | ------ | ----------- |
| stk_nm             | 종목명           | String | N        | 20     |             |
| etfobjt_idex_nm    | ETF대상지수명    | String | N        | 20     |             |
| wonju_pric         | 원주가격         | String | N        | 20     |             |
| etftxon_type       | ETF과세유형      | String | N        | 20     |             |
| etntxon_type       | ETN과세유형      | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"stk_nm":"KODEX 200",
	"etfobjt_idex_nm":"",
	"wonju_pric":"10",
	"etftxon_type":"보유기간과세",
	"etntxon_type":"보유기간과세",
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF일별추이요청 (ka40003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| etfdaly_trnsn          | ETF일별추이      | LIST   | N        |        |             |
| - cntr_dt              | 체결일자         | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pre_sig              | 대비기호         | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - pre_rt               | 대비율           | String | N        | 20     |             |
| - trde_qty             | 거래량           | String | N        | 20     |             |
| - nav                  | NAV              | String | N        | 20     |             |
| - acc_trde_prica       | 누적거래대금     | String | N        | 20     |             |
| - navidex_dispty_rt    | NAV/지수괴리율   | String | N        | 20     |             |
| - navetfdispty_rt      | NAV/ETF괴리율    | String | N        | 20     |             |
| - trace_eor_rt         | 추적오차율       | String | N        | 20     |             |
| - trace_cur_prc        | 추적현재가       | String | N        | 20     |             |
| - trace_pred_pre       | 추적전일대비     | String | N        | 20     |             |
| - trace_pre_sig        | 추적대비기호     | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"etfdaly_trnsn":
		[
			{
				"cntr_dt":"20241125",
				"cur_prc":"100535",
				"pre_sig":"0",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"0.00",
				"acc_trde_prica":"0",
				"navidex_dispty_rt":"0.00",
				"navetfdispty_rt":"0.00",
				"trace_eor_rt":"0",
				"trace_cur_prc":"0",
				"trace_pred_pre":"0",
				"trace_pre_sig":"3"
			},
			{
				"cntr_dt":"20241122",
				"cur_prc":"100535",
				"pre_sig":"0",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"+100584.57",
				"acc_trde_prica":"0",
				"navidex_dispty_rt":"0.00",
				"navetfdispty_rt":"-0.05",
				"trace_eor_rt":"0",
				"trace_cur_prc":"0",
				"trace_pred_pre":"0",
				"trace_pre_sig":"3"
			},
			{
				"cntr_dt":"20241121",
				"cur_prc":"100535",
				"pre_sig":"0",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"+100563.36",
				"acc_trde_prica":"0",
				"navidex_dispty_rt":"0.00",
				"navetfdispty_rt":"-0.03",
				"trace_eor_rt":"0",
				"trace_cur_pric":"0",
				"trace_pred_pre":"0",
				"trace_pre_sig":"3"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF전체시세요청 (ka40004)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명       | Type   | Required | Length | Description                                                                                                                                                      |
| ---------- | ------------ | ------ | -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| txon_type  | 과세유형     | String | Y        | 1      | 0:전체, 1:비과세, 2:보유기간과세, 3:회사형, 4:외국, 5:비과세해외(보유기간관세)                                                                                   |
| navpre     | NAV대비      | String | Y        | 1      | 0:전체, 1:NAV > 전일종가, 2:NAV < 전일종가                                                                                                                       |
| mngmcomp   | 운용사       | String | Y        | 4      | 0000:전체, 3020:KODEX(삼성), 3027:KOSEF(키움), 3191:TIGER(미래에셋), 3228:KINDEX(한국투자), 3023:KStar(KB), 3022:아리랑(한화), 9999:기타운용사                 |
| txon_yn    | 과세여부     | String | Y        | 1      | 0:전체, 1:과세, 2:비과세                                                                                                                                         |
| trace_idex | 추적지수     | String | Y        | 1      | 0:전체                                                                                                                                                           |
| stex_tp    | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명       | Type   | Required | Length | Description |
| ------------------ | ------------ | ------ | -------- | ------ | ----------- |
| etfall_mrpr        | ETF전체시세  | LIST   | N        |        |             |
| - stk_cd           | 종목코드     | String | N        | 20     |             |
| - stk_cls          | 종목분류     | String | N        | 20     |             |
| - stk_nm           | 종목명       | String | N        | 20     |             |
| - close_pric       | 종가         | String | N        | 20     |             |
| - pre_sig          | 대비기호     | String | N        | 20     |             |
| - pred_pre         | 전일대비     | String | N        | 20     |             |
| - pre_rt           | 대비율       | String | N        | 20     |             |
| - trde_qty         | 거래량       | String | N        | 20     |             |
| - nav              | NAV          | String | N        | 20     |             |
| - trace_eor_rt     | 추적오차율   | String | N        | 20     |             |
| - txbs             | 과표기준     | String | N        | 20     |             |
| - dvid_bf_base     | 배당전기준   | String | N        | 20     |             |
| - pred_dvida       | 전일배당금   | String | N        | 20     |             |
| - trace_idex_nm    | 추적지수명   | String | N        | 20     |             |
| - drng             | 배수         | String | N        | 20     |             |
| - trace_idex_cd    | 추적지수코드 | String | N        | 20     |             |
| - trace_idex       | 추적지수     | String | N        | 20     |             |
| - trace_flu_rt     | 추적등락율   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"txon_type": "0",
	"navpre": "0",
	"mngmcomp": "0000",
	"txon_yn": "0",
	"trace_idex": "0",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"etfall_mrpr":
		[
			{
				"stk_cd":"069500",
				"stk_cls":"19",
				"stk_nm":"KODEX 200",
				"close_pric":"24200",
				"pre_sig":"3",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"25137.83",
				"trace_eor_rt":"0.00",
				"txbs":"",
				"dvid_bf_base":"",
				"pred_dvida":"",
				"trace_idex_nm":"KOSPI100",
				"drng":"",
				"trace_idex_cd":"",
				"trace_idex":"24200",
				"trace_flu_rt":"0.00"
			},
			{
				"stk_cd":"069500",
				"stk_cls":"19",
				"stk_nm":"KODEX 200",
				"close_pric":"33120",
				"pre_sig":"3",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"33351.27",
				"trace_eor_rt":"0.00",
				"txbs":"",
				"dvid_bf_base":"",
				"pred_dvida":"",
				"trace_idex_nm":"KOSPI200",
				"drng":"",
				"trace_idex_cd":"",
				"trace_idex":"33120",
				"trace_flu_rt":"0.00"
			},
			{
				"stk_cd":"069660",
				"stk_cls":"19",
				"stk_nm":"KOSEF 200",
				"close_pric":"32090",
				"pre_sig":"3",
				"pred_pre":"0",
				"pre_rt":"0.00",
				"trde_qty":"0",
				"nav":"33316.97",
				"trace_eor_rt":"0.00",
				"txbs":"",
				"dvid_bf_base":"",
				"pred_dvida":"",
				"trace_idex_nm":"KOSPI200",
				"drng":"",
				"trace_idex_cd":"",
				"trace_idex":"32090",
				"trace_flu_rt":"0.00"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF시간대별추이요청 (ka40006)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| stk_nm                     | 종목명               | String | N        | 20     |             |
| etfobjt_idex_nm            | ETF대상지수명        | String | N        | 20     |             |
| wonju_pric                 | 원주가격             | String | N        | 20     |             |
| etftxon_type               | ETF과세유형          | String | N        | 20     |             |
| etntxon_type               | ETN과세유형          | String | N        | 20     |             |
| etftisl_trnsn              | ETF시간대별추이      | LIST   | N        |        |             |
| - tm                       | 시간                 | String | N        | 20     |             |
| - close_pric               | 종가                 | String | N        | 20     |             |
| - pre_sig                  | 대비기호             | String | N        | 20     |             |
| - pred_pre                 | 전일대비             | String | N        | 20     |             |
| - flu_rt                   | 등락율               | String | N        | 20     |             |
| - trde_qty                 | 거래량               | String | N        | 20     |             |
| - nav                      | NAV                  | String | N        | 20     |             |
| - trde_prica               | 거래대금             | String | N        | 20     |             |
| - navidex                  | NAV지수              | String | N        | 20     |             |
| - navetf                   | NAVETF               | String | N        | 20     |             |
| - trace                    | 추적                 | String | N        | 20     |             |
| - trace_idex               | 추적지수             | String | N        | 20     |             |
| - trace_idex_pred_pre      | 추적지수전일대비     | String | N        | 20     |             |
| - trace_idex_pred_pre_sig  | 추적지수전일대비기호 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"stk_nm":"KODEX 200",
	"etfobjt_idex_nm":"KOSPI200",
	"wonju_pric":"-10",
	"etftxon_type":"보유기간과세",
	"etntxon_type":"보유기간과세",
	"etftisl_trnsn":
		[
			{
				"tm":"132211",
				"close_pric":"+4900",
				"pre_sig":"2",
				"pred_pre":"+450",
				"flu_rt":"+10.11",
				"trde_qty":"1",
				"nav":"-4548.33",
				"trde_prica":"0",
				"navidex":"-72.38",
				"navetf":"+7.18",
				"trace":"0.00",
				"trace_idex":"+164680",
				"trace_idex_pred_pre":"+123",
				"trace_idex_pred_pre_sig":"2"
			},
			{
				"tm":"132210",
				"close_pric":"+4900",
				"pre_sig":"2",
				"pred_pre":"+450",
				"flu_rt":"+10.11",
				"trde_qty":"1",
				"nav":"-4548.33",
				"trde_prica":"0",
				"navidex":"-72.38",
				"navetf":"+7.18",
				"trace":"0.00",
				"trace_idex":"+164680",
				"trace_idex_pred_pre":"+123",
				"trace_idex_pred_pre_sig":"2"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF시간대별체결요청 (ka40007)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description         |
| ---------------------- | -------------------- | ------ | -------- | ------ | ------------------- |
| stk_cls                | 종목분류             | String | N        | 20     |                     |
| stk_nm                 | 종목명               | String | N        | 20     |                     |
| etfobjt_idex_nm        | ETF대상지수명        | String | N        | 20     |                     |
| etfobjt_idex_cd        | ETF대상지수코드      | String | N        | 20     |                     |
| objt_idex_pre_rt       | 대상지수대비율       | String | N        | 20     |                     |
| wonju_pric             | 원주가격             | String | N        | 20     |                     |
| etftisl_cntr_array     | ETF시간대별체결배열  | LIST   | N        |        |                     |
| - cntr_tm              | 체결시간             | String | N        | 20     |                     |
| - cur_prc              | 현재가               | String | N        | 20     |                     |
| - pre_sig              | 대비기호             | String | N        | 20     |                     |
| - pred_pre             | 전일대비             | String | N        | 20     |                     |
| - trde_qty             | 거래량               | String | N        | 20     |                     |
| - stex_tp              | 거래소구분           | String | N        | 20     | KRX, NXT, 통합      |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"stk_cls":"20",
	"stk_nm":"KODEX 200",
	"etfobjt_idex_nm":"KOSPI200",
	"etfobjt_idex_cd":"207",
	"objt_idex_pre_rt":"10.00",
	"wonju_pric":"-10",
	"etftisl_cntr_array":
		[
			{
				"cntr_tm":"130747",
				"cur_prc":"+4900",
				"pre_sig":"2",
				"pred_pre":"+450",
				"trde_qty":"1",
				"stex_tp":"KRX"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF일자별체결요청 (ka40008)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| cntr_tm                | 체결시간             | String | N        | 20     |             |
| cur_prc                | 현재가               | String | N        | 20     |             |
| pre_sig                | 대비기호             | String | N        | 20     |             |
| pred_pre               | 전일대비             | String | N        | 20     |             |
| trde_qty               | 거래량               | String | N        | 20     |             |
| etfnetprps_qty_array   | ETF순매수수량배열    | LIST   | N        |        |             |
| - dt                   | 일자                 | String | N        | 20     |             |
| - cur_prc_n            | 현재가n              | String | N        | 20     |             |
| - pre_sig_n            | 대비기호n            | String | N        | 20     |             |
| - pred_pre_n           | 전일대비n            | String | N        | 20     |             |
| - acc_trde_qty         | 누적거래량           | String | N        | 20     |             |
| - for_netprps_qty      | 외인순매수수량       | String | N        | 20     |             |
| - orgn_netprps_qty     | 기관순매수수량       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"cntr_tm":"130747",
	"cur_prc":"+4900",
	"pre_sig":"2",
	"pred_pre":"+450",
	"trde_qty":"1",
	"etfnetprps_qty_array":
		[
			{
				"dt":"20241125",
				"cur_prc_n":"+4900",
				"pre_sig_n":"2",
				"pred_pre_n":"+450",
				"acc_trde_qty":"1",
				"for_netprps_qty":"0",
				"orgn_netprps_qty":"0"
			},
			{
				"dt":"20241122",
				"cur_prc_n":"-4450",
				"pre_sig_n":"5",
				"pred_pre_n":"-60",
				"acc_trde_qty":"46",
				"for_netprps_qty":"--10558895",
				"orgn_netprps_qty":"0"
			},
			{
				"dt":"20241121",
				"cur_prc_n":"4510",
				"pre_sig_n":"3",
				"pred_pre_n":"0",
				"acc_trde_qty":"0",
				"for_netprps_qty":"--8894146",
				"orgn_netprps_qty":"0"
			},
			{
				"dt":"20241120",
				"cur_prc_n":"-4510",
				"pre_sig_n":"5",
				"pred_pre_n":"-160",
				"acc_trde_qty":"0",
				"for_netprps_qty":"--3073507",
				"orgn_netprps_qty":"0"
			},
			{
				"dt":"20241119",
				"cur_prc_n":"+4670",
				"pre_sig_n":"2",
				"pred_pre_n":"+160",
				"acc_trde_qty":"94",
				"for_netprps_qty":"--2902200",
				"orgn_netprps_qty":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF시간대별체결요청 (ka40009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| etfnavarray            | ETFNAV배열           | LIST   | N        |        |             |
| - nav                  | NAV                  | String | N        | 20     |             |
| - navpred_pre          | NAV전일대비          | String | N        | 20     |             |
| - navflu_rt            | NAV등락율            | String | N        | 20     |             |
| - trace_eor_rt         | 추적오차율           | String | N        | 20     |             |
| - dispty_rt            | 괴리율               | String | N        | 20     |             |
| - stkcnt               | 주식수               | String | N        | 20     |             |
| - base_pric            | 기준가               | String | N        | 20     |             |
| - for_rmnd_qty         | 외인보유수량         | String | N        | 20     |             |
| - repl_pric            | 대용가               | String | N        | 20     |             |
| - conv_pric            | 환산가격             | String | N        | 20     |             |
| - drstk                | DR/주                | String | N        | 20     |             |
| - wonju_pric           | 원주가격             | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"etfnavarray":
		[
			{
				"nav":"",
				"navpred_pre":"",
				"navflu_rt":"",
				"trace_eor_rt":"",
				"dispty_rt":"",
				"stkcnt":"133100",
				"base_pric":"4450",
				"for_rmnd_qty":"",
				"repl_pric":"",
				"conv_pric":"",
				"drstk":"",
				"wonju_pric":""
			},
			{
				"nav":"",
				"navpred_pre":"",
				"navflu_rt":"",
				"trace_eor_rt":"",
				"dispty_rt":"",
				"stkcnt":"133100",
				"base_pric":"4510",
				"for_rmnd_qty":"",
				"repl_pric":"",
				"conv_pric":"",
				"drstk":"",
				"wonju_pric":""
			},
			{
				"nav":"",
				"navpred_pre":"",
				"navflu_rt":"",
				"trace_eor_rt":"",
				"dispty_rt":"",
				"stkcnt":"133100",
				"base_pric":"4510",
				"for_rmnd_qty":"",
				"repl_pric":"",
				"conv_pric":"",
				"drstk":"",
				"wonju_pric":""
			},
			{
				"nav":"",
				"navpred_pre":"",
				"navflu_rt":"",
				"trace_eor_rt":"",
				"dispty_rt":"",
				"stkcnt":"133100",
				"base_pric":"4670",
				"for_rmnd_qty":"",
				"repl_pric":"",
				"conv_pric":"",
				"drstk":"",
				"wonju_pric":""
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### ETF시간대별추이요청 (ka40010)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/etf
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| etftisl_trnsn          | ETF시간대별추이      | LIST   | N        |        |             |
| - cur_prc              | 현재가               | String | N        | 20     |             |
| - pre_sig              | 대비기호             | String | N        | 20     |             |
| - pred_pre             | 전일대비             | String | N        | 20     |             |
| - trde_qty             | 거래량               | String | N        | 20     |             |
| - for_netprps          | 외인순매수           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "069500"
}
```

#### 응답 예시

```json
{
	"etftisl_trnsn":
		[
			{
				"cur_prc":"4450",
				"pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0",
				"for_netprps":"0"
			},
			{
				"cur_prc":"-4450",
				"pre_sig":"5",
				"pred_pre":"-60",
				"trde_qty":"46",
				"for_netprps":"--10558895"
			},
			{
				"cur_prc":"4510",
				"pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0",
				"for_netprps":"--8894146"
			},
			{
				"cur_prc":"-4510",
				"pre_sig":"5",
				"pred_pre":"-160",
				"trde_qty":"0",
				"for_netprps":"--3073507"
			},
			{
				"cur_prc":"+4670",
				"pre_sig":"2",
				"pred_pre":"+160",
				"trde_qty":"94",
				"for_netprps":"--2902200"
			},
			{
				"cur_prc":"-4510",
				"pre_sig":"5",
				"pred_pre":"-275",
				"trde_qty":"0",
				"for_netprps":"--1249609"
			},
			{
				"cur_prc":"-4510",
				"pre_sig":"5",
				"pred_pre":"-315",
				"trde_qty":"0",
				"for_netprps":"--2634816"
			},
			{
				"cur_prc":"-4510",
				"pre_sig":"5",
				"pred_pre":"-285",
				"trde_qty":"0",
				"for_netprps":"--2365477"
			},
			{
				"cur_prc":"-4450",
				"pre_sig":"5",
				"pred_pre":"-225",
				"trde_qty":"6",
				"for_netprps":"--571909"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 계좌 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### TR 목록
- **일자별종목별실현손익요청_일자** (ka10072)
- **일자별종목별실현손익요청_기간** (ka10073)
- **일자별실현손익요청** (ka10074)
- **미체결요청** (ka10075)
- **체결요청** (ka10076)
- **당일실현손익상세요청** (ka10077)
- **계좌수익률요청** (ka10085)
- **미체결 분할주문 상세** (ka10088)
- **당일매매일지요청** (ka10170)
- **예수금상세현황요청** (kt00001)
- **일별추정예탁자산현황요청** (kt00002)
- **추정자산조회요청** (kt00003)
- **계좌평가현황요청** (kt00004)
- **체결잔고요청** (kt00005)
- **계좌별주문체결내역상세요청** (kt00007)
- **계좌별익일결제예정내역요청** (kt00008)
- **계좌별주문체결현황요청** (kt00009)
- **주문인출가능금액요청** (kt00010)
- **증거금율별주문가능수량조회요청** (kt00011)
- **신용보증금율별주문가능수량조회요청** (kt00012)
- **증거금세부내역조회요청** (kt00013)
- **위탁종합거래내역요청** (kt00015)
- **일별계좌수익률상세현황요청** (kt00016)
- **계좌별당일현황요청** (kt00017)
- **계좌평가잔고내역요청** (kt00018)

--

#### 일자별종목별실현손익요청_일자 (ka10072)

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | |
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| dt_stk_div_rlzt_pl | 일자별종목별실현손익 | LIST | N | - | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - buy_uv | 매입단가 | String | N | 20 | |
| - cntr_pric | 체결가 | String | N | 20 | |
| - tdy_sel_pl | 당일매도손익 | String | N | 20 | |
| - pl_rt | 손익율 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - wthd_alowa | 인출가능금액 | String | N | 20 | |
| - loan_dt | 대출일 | String | N | 20 | |
| - crd_tp | 신용구분 | String | N | 20 | |
| - stk_cd_1 | 종목코드1 | String | N | 20 | |
| - tdy_sel_pl_1 | 당일매도손익1 | String | N | 20 | |

---

## 일자별종목별실현손익요청_기간 (ka10073)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | |
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| dt_stk_rlzt_pl | 일자별종목별실현손익 | LIST | N | - | |
| - dt | 일자 | String | N | 20 | |
| - tdy_htssel_cmsn | 당일hts매도수수료 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - buy_uv | 매입단가 | String | N | 20 | |
| - cntr_pric | 체결가 | String | N | 20 | |
| - tdy_sel_pl | 당일매도손익 | String | N | 20 | |
| - pl_rt | 손익율 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - wthd_alowa | 인출가능금액 | String | N | 20 | |
| - loan_dt | 대출일 | String | N | 20 | |
| - crd_tp | 신용구분 | String | N | 20 | |

### Python 예제 코드

```python
import requests
import json

# 일자별종목별실현손익요청_기간
def fn_ka10073(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10073', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stk_cd': '005930', # 종목코드 
        'strt_dt': '20241128', # 시작일자 YYYYMMDD
        'end_dt': '20241128', # 종료일자 YYYYMMDD
    }

    # 3. API 실행
    fn_ka10073(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10073(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stk_cd" : "005930",
    "strt_dt" : "20241128",
    "end_dt" : "20241128"
}
```

#### Response
```json
{
    "dt_stk_rlzt_pl": [
        {
            "dt":"20241128",
            "tdy_htssel_cmsn":"현금",
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.96",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.04",
            "pl_rt":"+61.28",
            "stk_cd":"A005930",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "wthd_alowa":"0",
            "loan_dt":"",
            "crd_tp":"현금잔고"
        },
        {
            "dt":"20241128",
            "tdy_htssel_cmsn":"현금",
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.96",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.04",
            "pl_rt":"+61.28",
            "stk_cd":"A005930",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "wthd_alowa":"0",
            "loan_dt":"",
            "crd_tp":"현금잔고"
        },
        {
            "dt":"20241128",
            "tdy_htssel_cmsn":"현금",
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.96",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.04",
            "pl_rt":"+61.28",
            "stk_cd":"A005930",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "wthd_alowa":"0",
            "loan_dt":"",
            "crd_tp":"현금잔고"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 일자별실현손익요청 (ka10074)

**⚠️ 주의사항:** 실현손익이 발생한 일자에대해서만 데이터가 채워짐.

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| tot_buy_amt | 총매수금액 | String | N | - | |
| tot_sell_amt | 총매도금액 | String | N | - | |
| rlzt_pl | 실현손익 | String | N | - | |
| trde_cmsn | 매매수수료 | String | N | - | |
| trde_tax | 매매세금 | String | N | - | |
| dt_rlzt_pl | 일자별실현손익 | LIST | N | - | |
| - dt | 일자 | String | N | 20 | |
| - buy_amt | 매수금액 | String | N | 20 | |
| - sell_amt | 매도금액 | String | N | 20 | |
| - tdy_sel_pl | 당일매도손익 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |

### Python 예제 코드

```python
import requests
import json

# 일자별실현손익요청
def fn_ka10074(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10074', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'strt_dt': '20241128', # 시작일자 
        'end_dt': '20241128', # 종료일자 
    }

    # 3. API 실행
    fn_ka10074(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10074(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "strt_dt" : "20241128",
    "end_dt" : "20241128"
}
```

#### Response
```json
{
    "tot_buy_amt":"0",
    "tot_sell_amt":"474600",
    "rlzt_pl":"179419",
    "trde_cmsn":"940",
    "trde_tax":"852",
    "dt_rlzt_pl": [
        {
            "dt":"20241128",
            "buy_amt":"0",
            "sell_amt":"474600",
            "tdy_sel_pl":"179419",
            "tdy_trde_cmsn":"940",
            "tdy_trde_tax":"852"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 미체결요청 (ka10075)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| all_stk_tp | 전체종목구분 | String | Y | 1 | 0:전체, 1:종목 |
| trde_tp | 매매구분 | String | Y | 1 | 0:전체, 1:매도, 2:매수 |
| stk_cd | 종목코드 | String | N | 6 | |
| stex_tp | 거래소구분 | String | Y | 1 | 0:통합, 1:KRX, 2:NXT |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| oso | 미체결 | LIST | N | - | |
| - acnt_no | 계좌번호 | String | N | 20 | |
| - ord_no | 주문번호 | String | N | 20 | |
| - mang_empno | 관리사번 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - tsk_tp | 업무구분 | String | N | 20 | |
| - ord_stt | 주문상태 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - ord_qty | 주문수량 | String | N | 20 | |
| - ord_pric | 주문가격 | String | N | 20 | |
| - oso_qty | 미체결수량 | String | N | 20 | |
| - cntr_tot_amt | 체결누계금액 | String | N | 20 | |
| - orig_ord_no | 원주문번호 | String | N | 20 | |
| - io_tp_nm | 주문구분 | String | N | 20 | |
| - trde_tp | 매매구분 | String | N | 20 | |
| - tm | 시간 | String | N | 20 | |
| - cntr_no | 체결번호 | String | N | 20 | |
| - cntr_pric | 체결가 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - sel_bid | 매도호가 | String | N | 20 | |
| - buy_bid | 매수호가 | String | N | 20 | |
| - unit_cntr_pric | 단위체결가 | String | N | 20 | |
| - unit_cntr_qty | 단위체결량 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - ind_invsr | 개인투자자 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | 0:통합, 1:KRX, 2:NXT |
| - stex_tp_txt | 거래소구분텍스트 | String | N | 20 | 통합,KRX,NXT |
| - sor_yn | SOR 여부값 | String | N | 20 | Y,N |
| - stop_pric | 스톱가 | String | N | 20 | 스톱지정가주문 스톱가 |

### Python 예제 코드

```python
import requests
import json

# 미체결요청
def fn_ka10075(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10075', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'all_stk_tp': '1', # 전체종목구분 0:전체, 1:종목
        'trde_tp': '0', # 매매구분 0:전체, 1:매도, 2:매수
        'stk_cd': '005930', # 종목코드 
        'stex_tp': '0', # 거래소구분 0 : 통합, 1 : KRX, 2 : NXT
    }

    # 3. API 실행
    fn_ka10075(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10075(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "all_stk_tp" : "1",
    "trde_tp" : "0",
    "stk_cd" : "005930",
    "stex_tp" : "0"
}
```

#### Response
```json
{
    "oso": [
        {
            "acnt_no":"1234567890",
            "ord_no":"0000069",
            "mang_empno":"",
            "stk_cd":"005930",
            "tsk_tp":"",
            "ord_stt":"접수",
            "stk_nm":"삼성전자",
            "ord_qty":"1",
            "ord_pric":"0",
            "oso_qty":"1",
            "cntr_tot_amt":"0",
            "orig_ord_no":"0000000",
            "io_tp_nm":"+매수",
            "trde_tp":"시장가",
            "tm":"154113",
            "cntr_no":"",
            "cntr_pric":"0",
            "cntr_qty":"0",
            "cur_prc":"+74100",
            "sel_bid":"0",
            "buy_bid":"+74100",
            "unit_cntr_pric":"",
            "unit_cntr_qty":"",
            "tdy_trde_cmsn":"0",
            "tdy_trde_tax":"0",
            "ind_invsr":"",
            "stex_tp":"1",
            "stex_tp_txt":"KRX",
            "sor_yn":"N"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 체결요청 (ka10076)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목코드 | String | N | 6 | |
| qry_tp | 조회구분 | String | Y | 1 | 0:전체, 1:종목 |
| sell_tp | 매도수구분 | String | Y | 1 | 0:전체, 1:매도, 2:매수 |
| ord_no | 주문번호 | String | N | 10 | 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이 조회됩니다. |
| stex_tp | 거래소구분 | String | Y | 1 | 0:통합, 1:KRX, 2:NXT |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cntr | 체결 | LIST | N | - | |
| - ord_no | 주문번호 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - io_tp_nm | 주문구분 | String | N | 20 | |
| - ord_pric | 주문가격 | String | N | 20 | |
| - ord_qty | 주문수량 | String | N | 20 | |
| - cntr_pric | 체결가 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - oso_qty | 미체결수량 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - ord_stt | 주문상태 | String | N | 20 | |
| - trde_tp | 매매구분 | String | N | 20 | |
| - orig_ord_no | 원주문번호 | String | N | 20 | |
| - ord_tm | 주문시간 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | 0:통합, 1:KRX, 2:NXT |
| - stex_tp_txt | 거래소구분텍스트 | String | N | 20 | 통합,KRX,NXT |
| - sor_yn | SOR 여부값 | String | N | 20 | Y,N |
| - stop_pric | 스톱가 | String | N | 20 | 스톱지정가주문 스톱가 |

### Python 예제 코드

```python
import requests
import json

# 체결요청
def fn_ka10076(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10076', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stk_cd': '005930', # 종목코드 
        'qry_tp': '1', # 조회구분 0:전체, 1:종목
        'sell_tp': '0', # 매도수구분 0:전체, 1:매도, 2:매수
        'ord_no': '', # 주문번호 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이 조회됩니다. 
        'stex_tp': '0', # 거래소구분  0 : 통합, 1 : KRX, 2 : NXT
    }

    # 3. API 실행
    fn_ka10076(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10076(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stk_cd" : "005930",
    "qry_tp" : "1",
    "sell_tp" : "0",
    "ord_no" : "",
    "stex_tp" : "0"
}
```

#### Response
```json
{
    "cntr": [
        {
            "ord_no":"0000037",
            "stk_nm":"삼성전자",
            "io_tp_nm":"-매도",
            "ord_pric":"158200",
            "ord_qty":"1",
            "cntr_pric":"158200",
            "cntr_qty":"1",
            "oso_qty":"0",
            "tdy_trde_cmsn":"310",
            "tdy_trde_tax":"284",
            "ord_stt":"체결",
            "trde_tp":"보통",
            "orig_ord_no":"0000000",
            "ord_tm":"153815",
            "stk_cd":"005930",
            "stex_tp":"0",
            "stex_tp_txt":"SOR",
            "sor_yn":"Y"
        },
        {
            "ord_no":"0000036",
            "stk_nm":"삼성전자",
            "io_tp_nm":"-매도",
            "ord_pric":"158200",
            "ord_qty":"1",
            "cntr_pric":"158200",
            "cntr_qty":"1",
            "oso_qty":"0",
            "tdy_trde_cmsn":"310",
            "tdy_trde_tax":"284",
            "ord_stt":"체결",
            "trde_tp":"보통",
            "orig_ord_no":"0000000",
            "ord_tm":"153806",
            "stk_cd":"005930",
            "stex_tp":"0",
            "stex_tp_txt":"SOR",
            "sor_yn":"Y"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 당일실현손익상세요청 (ka10077)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| tdy_rlzt_pl | 당일실현손익 | String | N | - | |
| tdy_rlzt_pl_dtl | 당일실현손익상세 | LIST | N | - | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - buy_uv | 매입단가 | String | N | 20 | |
| - cntr_pric | 체결가 | String | N | 20 | |
| - tdy_sel_pl | 당일매도손익 | String | N | 20 | |
| - pl_rt | 손익율 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |

### Python 예제 코드

```python
import requests
import json

# 당일실현손익상세요청
def fn_ka10077(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10077', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stk_cd': '005930', # 종목코드 
    }

    # 3. API 실행
    fn_ka10077(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10077(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stk_cd" : "005930"
}
```

#### Response
```json
{
    "tdy_rlzt_pl":"179439",
    "tdy_rlzt_pl_dtl": [
        {
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.9573459",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.0426541",
            "pl_rt":"+61.28",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "stk_cd":"A005930"
        },
        {
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.9573459",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.0426541",
            "pl_rt":"+61.28",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "stk_cd":"A005930"
        },
        {
            "stk_nm":"삼성전자",
            "cntr_qty":"1",
            "buy_uv":"97602.9573459",
            "cntr_pric":"158200",
            "tdy_sel_pl":"59813.0426541",
            "pl_rt":"+61.28",
            "tdy_trde_cmsn":"500",
            "tdy_trde_tax":"284",
            "stk_cd":"A005930"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 계좌수익률요청 (ka10085)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stex_tp | 거래소구분 | String | Y | 1 | 0:통합, 1:KRX, 2:NXT |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| acnt_prft_rt | 계좌수익률 | LIST | N | - | |
| - dt | 일자 | String | N | 20 | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pur_pric | 매입가 | String | N | 20 | |
| - pur_amt | 매입금액 | String | N | 20 | |
| - rmnd_qty | 보유수량 | String | N | 20 | |
| - tdy_sel_pl | 당일매도손익 | String | N | 20 | |
| - tdy_trde_cmsn | 당일매매수수료 | String | N | 20 | |
| - tdy_trde_tax | 당일매매세금 | String | N | 20 | |
| - crd_tp | 신용구분 | String | N | 20 | |
| - loan_dt | 대출일 | String | N | 20 | |
| - setl_remn | 결제잔고 | String | N | 20 | |
| - clrn_alow_qty | 청산가능수량 | String | N | 20 | |
| - crd_amt | 신용금액 | String | N | 20 | |
| - crd_int | 신용이자 | String | N | 20 | |
| - expr_dt | 만기일 | String | N | 20 | |

### Python 예제 코드

```python
import requests
import json

# 계좌수익률요청
def fn_ka10085(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10085', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stex_tp': '0', # 거래소구분  0 : 통합, 1 : KRX, 2 : NXT
    }

    # 3. API 실행
    fn_ka10085(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10085(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stex_tp" : "0"
}
```

#### Response
```json
{
    "acnt_prft_rt": [
        {
            "dt":"",
            "stk_cd":"005930",
            "stk_nm":"삼성전자",
            "cur_prc":"-63000",
            "pur_pric":"124500",
            "pur_amt":"373500",
            "rmnd_qty":"3",
            "tdy_sel_pl":"0",
            "tdy_trde_cmsn":"0",
            "tdy_trde_tax":"0",
            "crd_tp":"00",
            "loan_dt":"00000000",
            "setl_remn":"3",
            "clrn_alow_qty":"3",
            "crd_amt":"0",
            "crd_int":"0",
            "expr_dt":"00000000"
        },
        {
            "dt":"",
            "stk_cd":"005930",
            "stk_nm":"삼성전자",
            "cur_prc":"+256500",
            "pur_pric":"209179",
            "pur_amt":"1673429",
            "rmnd_qty":"8",
            "tdy_sel_pl":"0",
            "tdy_trde_cmsn":"0",
            "tdy_trde_tax":"0",
            "crd_tp":"00",
            "loan_dt":"00000000",
            "setl_remn":"8",
            "clrn_alow_qty":"8",
            "crd_amt":"0",
            "crd_int":"0",
            "expr_dt":"00000000"
        },
        {
            "dt":"",
            "stk_cd":"005930",
            "stk_nm":"삼성전자",
            "cur_prc":"+156600",
            "pur_pric":"97603",
            "pur_amt":"3513706",
            "rmnd_qty":"36",
            "tdy_sel_pl":"0",
            "tdy_trde_cmsn":"0",
            "tdy_trde_tax":"0",
            "crd_tp":"00",
            "loan_dt":"00000000",
            "setl_remn":"39",
            "clrn_alow_qty":"36",
            "crd_amt":"0",
            "crd_int":"0",
            "expr_dt":"00000000"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 미체결 분할주문 상세 (ka10088)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| ord_no | 주문번호 | String | Y | 20 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| osop | 미체결분할주문리스트 | LIST | N | - | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - ord_no | 주문번호 | String | N | 20 | |
| - ord_qty | 주문수량 | String | N | 20 | |
| - ord_pric | 주문가격 | String | N | 20 | |
| - osop_qty | 미체결수량 | String | N | 20 | |
| - io_tp_nm | 주문구분 | String | N | 20 | |
| - trde_tp | 매매구분 | String | N | 20 | |
| - sell_tp | 매도/수 구분 | String | N | 20 | |
| - cntr_qty | 체결량 | String | N | 20 | |
| - ord_stt | 주문상태 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | 0:통합, 1:KRX, 2:NXT |
| - stex_tp_txt | 거래소구분텍스트 | String | N | 20 | 통합,KRX,NXT |

### Python 예제 코드

```python
import requests
import json

# 미체결 분할주문 상세
def fn_ka10088(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10088', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'ord_no': '8', # 주문번호 
    }

    # 3. API 실행
    fn_ka10088(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10088(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "ord_no" : "8"
}
```

#### Response
```json
{
    "osop": [
        {
            "stk_cd": "005930",
            "acnt_no": "1234567890",
            "stk_nm": "삼성전자",
            "ord_no": "0000008",
            "ord_qty": "1",
            "ord_pric": "5150",
            "osop_qty": "1",
            "io_tp_nm": "+매수정정",
            "trde_tp": "보통",
            "sell_tp": "2",
            "cntr_qty": "0",
            "ord_stt": "접수",
            "cur_prc": "5250",
            "stex_tp": "1",
            "stex_tp_txt": "S-KRX"
        }
    ],
    "return_code": 0,
    "return_msg": " 조회가 완료되었습니다."
}
```

---

## 당일매매일지요청 (ka10170)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| base_dt | 기준일자 | String | N | 8 | YYYYMMDD (공백입력시 금일데이터, 최근 2개월까지 제공) |
| ottks_tp | 단주구분 | String | Y | 1 | 1:당일매수에 대한 당일매도, 2:당일매도 전체 |
| ch_crd_tp | 현금신용구분 | String | Y | 1 | 0:전체, 1:현금매매만, 2:신용매매만 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| tot_sell_amt | 총매도금액 | String | N | - | |
| tot_buy_amt | 총매수금액 | String | N | - | |
| tot_cmsn_tax | 총수수료_세금 | String | N | - | |
| tot_exct_amt | 총정산금액 | String | N | - | |
| tot_pl_amt | 총손익금액 | String | N | - | |
| tot_prft_rt | 총수익률 | String | N | - | |
| tdy_trde_diary | 당일매매일지 | LIST | N | - | |
| - stk_nm | 종목명 | String | N | 20 | |
| - buy_avg_pric | 매수평균가 | String | N | - | |
| - buy_qty | 매수수량 | String | N | - | |
| - sel_avg_pric | 매도평균가 | String | N | - | |
| - sell_qty | 매도수량 | String | N | - | |
| - cmsn_alm_tax | 수수료_제세금 | String | N | - | |
| - pl_amt | 손익금액 | String | N | - | |
| - sell_amt | 매도금액 | String | N | - | |
| - buy_amt | 매수금액 | String | N | - | |
| - prft_rt | 수익률 | String | N | - | |
| - stk_cd | 종목코드 | String | N | 6 | |

### Python 예제 코드

```python
import requests
import json

# 당일매매일지요청
def fn_ka10170(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka10170', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'base_dt': '20241120', # 기준일자 YYYYMMDD(공백입력시 금일데이터,최근 2개월까지 제공)
        'ottks_tp': '1', # 단주구분 1:당일매수에 대한 당일매도,2:당일매도 전체
        'ch_crd_tp': '0', # 현금신용구분 0:전체, 1:현금매매만, 2:신용매매만
    }

    # 3. API 실행
    fn_ka10170(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_ka10170(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "base_dt" : "20241120",
    "ottks_tp" : "1",
    "ch_crd_tp" : "0"
}
```

#### Response
```json
{
    "tot_sell_amt":"48240",
    "tot_buy_amt":"48240",
    "tot_cmsn_tax":"174",
    "tot_exct_amt":"-174",
    "tot_pl_amt":"-174",
    "tot_prft_rt":"-0.36",
    "tdy_trde_diary": [
        {
            "stk_nm":"삼성전자",
            "buy_avg_pric":"16080",
            "buy_qty":"3",
            "sel_avg_pric":"16080",
            "sell_qty":"3",
            "cmsn_alm_tax":"174",
            "pl_amt":"-174",
            "sell_amt":"48240",
            "buy_amt":"48240",
            "prft_rt":"-0.36",
            "stk_cd":"005930"
        }
    ],
    "return_code":0,
    "return_msg":" 조회가 완료되었습니다."
}
```

---

## 예수금상세현황요청 (kt00001)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| qry_tp | 조회구분 | String | Y | 1 | 3:추정조회, 2:일반조회 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| entr | 예수금 | String | N | 15 | |
| profa_ch | 주식증거금현금 | String | N | 15 | |
| bncr_profa_ch | 수익증권증거금현금 | String | N | 15 | |
| nxdy_bncr_sell_exct | 익일수익증권매도정산대금 | String | N | 15 | |
| fc_stk_krw_repl_set_amt | 해외주식원화대용설정금 | String | N | 15 | |
| crd_grnta_ch | 신용보증금현금 | String | N | 15 | |
| crd_grnt_ch | 신용담보금현금 | String | N | 15 | |
| add_grnt_ch | 추가담보금현금 | String | N | 15 | |
| etc_profa | 기타증거금 | String | N | 15 | |
| uncl_stk_amt | 미수확보금 | String | N | 15 | |
| shrts_prica | 공매도대금 | String | N | 15 | |
| crd_set_grnta | 신용설정평가금 | String | N | 15 | |
| chck_ina_amt | 수표입금액 | String | N | 15 | |
| etc_chck_ina_amt | 기타수표입금액 | String | N | 15 | |
| crd_grnt_ruse | 신용담보재사용 | String | N | 15 | |
| knx_asset_evltv | 코넥스기본예탁금 | String | N | 15 | |
| elwdpst_evlta | ELW예탁평가금 | String | N | 15 | |
| crd_ls_rght_frcs_amt | 신용대주권리예정금액 | String | N | 15 | |
| lvlh_join_amt | 생계형가입금액 | String | N | 15 | |
| lvlh_trns_alowa | 생계형입금가능금액 | String | N | 15 | |
| repl_amt | 대용금평가금액(합계) | String | N | 15 | |
| remn_repl_evlta | 잔고대용평가금액 | String | N | 15 | |
| trst_remn_repl_evlta | 위탁대용잔고평가금액 | String | N | 15 | |
| bncr_remn_repl_evlta | 수익증권대용평가금액 | String | N | 15 | |
| profa_repl | 위탁증거금대용 | String | N | 15 | |
| crd_grnta_repl | 신용보증금대용 | String | N | 15 | |
| crd_grnt_repl | 신용담보금대용 | String | N | 15 | |
| add_grnt_repl | 추가담보금대용 | String | N | 15 | |
| rght_repl_amt | 권리대용금 | String | N | 15 | |
| pymn_alow_amt | 출금가능금액 | String | N | 15 | |
| wrap_pymn_alow_amt | 랩출금가능금액 | String | N | 15 | |
| ord_alow_amt | 주문가능금액 | String | N | 15 | |
| bncr_buy_alowa | 수익증권매수가능금액 | String | N | 15 | |
| 20stk_ord_alow_amt | 20%종목주문가능금액 | String | N | 15 | |
| 30stk_ord_alow_amt | 30%종목주문가능금액 | String | N | 15 | |
| 40stk_ord_alow_amt | 40%종목주문가능금액 | String | N | 15 | |
| 100stk_ord_alow_amt | 100%종목주문가능금액 | String | N | 15 | |
| ch_uncla | 현금미수금 | String | N | 15 | |
| ch_uncla_dlfe | 현금미수연체료 | String | N | 15 | |
| ch_uncla_tot | 현금미수금합계 | String | N | 15 | |
| crd_int_npay | 신용이자미납 | String | N | 15 | |
| int_npay_amt_dlfe | 신용이자미납연체료 | String | N | 15 | |
| int_npay_amt_tot | 신용이자미납합계 | String | N | 15 | |
| etc_loana | 기타대여금 | String | N | 15 | |
| etc_loana_dlfe | 기타대여금연체료 | String | N | 15 | |
| etc_loan_tot | 기타대여금합계 | String | N | 15 | |
| nrpy_loan | 미상환융자금 | String | N | 15 | |
| loan_sum | 융자금합계 | String | N | 15 | |
| ls_sum | 대주금합계 | String | N | 15 | |
| crd_grnt_rt | 신용담보비율 | String | N | 15 | |
| mdstrm_usfe | 중도이용료 | String | N | 15 | |
| min_ord_alow_yn | 최소주문가능금액 | String | N | 15 | |
| loan_remn_evlt_amt | 대출총평가금액 | String | N | 15 | |
| dpst_grntl_remn | 예탁담보대출잔고 | String | N | 15 | |
| sell_grntl_remn | 매도담보대출잔고 | String | N | 15 | |
| d1_entra | d+1추정예수금 | String | N | 15 | |
| d1_slby_exct_amt | d+1매도매수정산금 | String | N | 15 | |
| d1_buy_exct_amt | d+1매수정산금 | String | N | 15 | |
| d1_out_rep_mor | d+1미수변제소요금 | String | N | 15 | |
| d1_sel_exct_amt | d+1매도정산금 | String | N | 15 | |
| d1_pymn_alow_amt | d+1출금가능금액 | String | N | 15 | |
| d2_entra | d+2추정예수금 | String | N | 15 | |
| d2_slby_exct_amt | d+2매도매수정산금 | String | N | 15 | |
| d2_buy_exct_amt | d+2매수정산금 | String | N | 15 | |
| d2_out_rep_mor | d+2미수변제소요금 | String | N | 15 | |
| d2_sel_exct_amt | d+2매도정산금 | String | N | 15 | |
| d2_pymn_alow_amt | d+2출금가능금액 | String | N | 15 | |
| 50stk_ord_alow_amt | 50%종목주문가능금액 | String | N | 15 | |
| 60stk_ord_alow_amt | 60%종목주문가능금액 | String | N | 15 | |
| stk_entr_prst | 종목별예수금 | LIST | N | - | |
| - crnc_cd | 통화코드 | String | N | 3 | |
| - fx_entr | 외화예수금 | String | N | 15 | |
| - fc_krw_repl_evlta | 원화대용평가금 | String | N | 15 | |
| - fc_trst_profa | 해외주식증거금 | String | N | 15 | |
| - pymn_alow_amt | 출금가능금액 | String | N | 15 | |
| - pymn_alow_amt_entr | 출금가능금액(예수금) | String | N | 15 | |
| - ord_alow_amt_entr | 주문가능금액(예수금) | String | N | 15 | |
| - fc_uncla | 외화미수(합계) | String | N | 15 | |
| - fc_ch_uncla | 외화현금미수금 | String | N | 15 | |
| - dly_amt | 연체료 | String | N | 15 | |
| - d1_fx_entr | d+1외화예수금 | String | N | 15 | |
| - d2_fx_entr | d+2외화예수금 | String | N | 15 | |
| - d3_fx_entr | d+3외화예수금 | String | N | 15 | |
| - d4_fx_entr | d+4외화예수금 | String | N | 15 | |

### Python 예제 코드

```python
import requests
import json

# 예수금상세현황요청
def fn_kt00001(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00001', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'qry_tp': '3', # 조회구분 3:추정조회, 2:일반조회
    }

    # 3. API 실행
    fn_kt00001(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00001(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "qry_tp" : "3"
}
```

#### Response
```json
{
    "entr":"000000000017534",
    "profa_ch":"000000000032193",
    "bncr_profa_ch":"000000000000000",
    "nxdy_bncr_sell_exct":"000000000000000",
    "fc_stk_krw_repl_set_amt":"000000000000000",
    "crd_grnta_ch":"000000000000000",
    "crd_grnt_ch":"000000000000000",
    "add_grnt_ch":"000000000000000",
    "etc_profa":"000000000000000",
    "uncl_stk_amt":"000000000000000",
    "shrts_prica":"000000000000000",
    "crd_set_grnta":"000000000000000",
    "chck_ina_amt":"000000000000000",
    "etc_chck_ina_amt":"000000000000000",
    "crd_grnt_ruse":"000000000000000",
    "knx_asset_evltv":"000000000000000",
    "elwdpst_evlta":"000000000031269",
    "crd_ls_rght_frcs_amt":"000000000000000",
    "lvlh_join_amt":"000000000000000",
    "lvlh_trns_alowa":"000000000000000",
    "repl_amt":"000000003915500",
    "remn_repl_evlta":"000000003915500",
    "trst_remn_repl_evlta":"000000000000000",
    "bncr_remn_repl_evlta":"000000000000000",
    "profa_repl":"000000000000000",
    "crd_grnta_repl":"000000000000000",
    "crd_grnt_repl":"000000000000000",
    "add_grnt_repl":"000000000000000",
    "rght_repl_amt":"000000000000000",
    "pymn_alow_amt":"000000000085341",
    "wrap_pymn_alow_amt":"000000000000000",
    "ord_alow_amt":"000000000085341",
    "bncr_buy_alowa":"000000000085341",
    "20stk_ord_alow_amt":"000000000012550",
    "30stk_ord_alow_amt":"000000000012550",
    "40stk_ord_alow_amt":"000000000012550",
    "100stk_ord_alow_amt":"000000000012550",
    "ch_uncla":"000000000000000",
    "ch_uncla_dlfe":"000000000000000",
    "ch_uncla_tot":"000000000000000",
    "crd_int_npay":"000000000000000",
    "int_npay_amt_dlfe":"000000000000000",
    "int_npay_amt_tot":"000000000000000",
    "etc_loana":"000000000000000",
    "etc_loana_dlfe":"000000000000000",
    "etc_loan_tot":"000000000000000",
    "nrpy_loan":"000000000000000",
    "loan_sum":"000000000000000",
    "ls_sum":"000000000000000",
    "crd_grnt_rt":"0.00",
    "mdstrm_usfe":"000000000388388",
    "min_ord_alow_yn":"000000000000000",
    "loan_remn_evlt_amt":"000000000000000",
    "dpst_grntl_remn":"000000000000000",
    "sell_grntl_remn":"000000000000000",
    "d1_entra":"000000000017450",
    "d1_slby_exct_amt":"-00000000000084",
    "d1_buy_exct_amt":"000000000048240",
    "d1_out_rep_mor":"000000000000000",
    "d1_sel_exct_amt":"000000000048156",
    "d1_pymn_alow_amt":"000000000012550",
    "d2_entra":"000000000012550",
    "d2_slby_exct_amt":"-00000000004900",
    "d2_buy_exct_amt":"000000000004900",
    "d2_out_rep_mor":"000000000000000",
    "d2_sel_exct_amt":"000000000000000",
    "d2_pymn_alow_amt":"000000000012550",
    "50stk_ord_alow_amt":"000000000012550",
    "60stk_ord_alow_amt":"000000000012550",
    "stk_entr_prst": [],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다."
}
```

---

## 일별추정예탁자산현황요청 (kt00002)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| start_dt | 시작조회기간 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료조회기간 | String | Y | 8 | YYYYMMDD |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| daly_prsm_dpst_aset_amt_prst | 일별추정예탁자산현황 | LIST | N | - | |
| - dt | 일자 | String | N | 8 | |
| - entr | 예수금 | String | N | 12 | |
| - grnt_use_amt | 담보대출금 | String | N | 12 | |
| - crd_loan | 신용융자금 | String | N | 12 | |
| - ls_grnt | 대주담보금 | String | N | 12 | |
| - repl_amt | 대용금 | String | N | 12 | |
| - prsm_dpst_aset_amt | 추정예탁자산 | String | N | 12 | |
| - prsm_dpst_aset_amt_bncr_skip | 추정예탁자산수익증권제외 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 일별추정예탁자산현황요청
def fn_kt00002(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00002', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'start_dt': '20241111', # 시작조회기간 YYYYMMDD
        'end_dt': '20241125', # 종료조회기간 YYYYMMDD
    }

    # 3. API 실행
    fn_kt00002(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00002(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "start_dt" : "20241111",
    "end_dt" : "20241125"
}
```

#### Response
```json
{
    "daly_prsm_dpst_aset_amt_prst": [
        {
            "dt":"20241111",
            "entr":"000000100000",
            "grnt_use_amt":"000000000000",
            "crd_loan":"000000000000",
            "ls_grnt":"000000000000",
            "repl_amt":"000000000000",
            "prsm_dpst_aset_amt":"000000000000",
            "prsm_dpst_aset_amt_bncr_skip":"000000000000"
        },
        {
            "dt":"20241112",
            "entr":"000000100000",
            "grnt_use_amt":"000000000000",
            "crd_loan":"000000000000",
            "ls_grnt":"000000000000",
            "repl_amt":"000000000000",
            "prsm_dpst_aset_amt":"000000000000",
            "prsm_dpst_aset_amt_bncr_skip":"000000000000"
        },
        {
            "dt":"20241113",
            "entr":"000000100000",
            "grnt_use_amt":"000000000000",
            "crd_loan":"000000000000",
            "ls_grnt":"000000000000",
            "repl_amt":"000000000000",
            "prsm_dpst_aset_amt":"000000000000",
            "prsm_dpst_aset_amt_bncr_skip":"000000000000"
        },
        {
            "dt":"20241114",
            "entr":"000000999748",
            "grnt_use_amt":"000000000000",
            "crd_loan":"000000000000",
            "ls_grnt":"000000000000",
            "repl_amt":"000000000165",
            "prsm_dpst_aset_amt":"000000000000",
            "prsm_dpst_aset_amt_bncr_skip":"000000000000"
        }
    ],
    "return_code":0,
    "return_msg":"일자별 계좌별 추정예탁자산 내역이 조회 되었습니다."
}
```

---

## 추정자산조회요청 (kt00003)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| qry_tp | 상장폐지조회구분 | String | Y | 1 | 0:전체, 1:상장폐지종목제외 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| prsm_dpst_aset_amt | 추정예탁자산 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 추정자산조회요청
def fn_kt00003(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00003', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'qry_tp': '0', # 상장폐지조회구분 0:전체, 1:상장폐지종목제외
    }

    # 3. API 실행
    fn_kt00003(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00003(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "qry_tp" : "0"
}
```

#### Response
```json
{
    "prsm_dpst_aset_amt":"00000530218",
    "return_code":0,
    "return_msg":"조회가 완료되었습니다.."
}
```

---

## 계좌평가현황요청 (kt00004)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| qry_tp | 상장폐지조회구분 | String | Y | 1 | 0:전체, 1:상장폐지종목제외 |
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | KRX:한국거래소, NXT:넥스트트레이드 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| acnt_nm | 계좌명 | String | N | 30 | |
| brch_nm | 지점명 | String | N | 30 | |
| entr | 예수금 | String | N | 12 | |
| d2_entra | D+2추정예수금 | String | N | 12 | |
| tot_est_amt | 유가잔고평가액 | String | N | 12 | |
| aset_evlt_amt | 예탁자산평가액 | String | N | 12 | |
| tot_pur_amt | 총매입금액 | String | N | 12 | |
| prsm_dpst_aset_amt | 추정예탁자산 | String | N | 12 | |
| tot_grnt_sella | 매도담보대출금 | String | N | 12 | |
| tdy_lspft_amt | 당일투자원금 | String | N | 12 | |
| invt_bsamt | 당월투자원금 | String | N | 12 | |
| lspft_amt | 누적투자원금 | String | N | 12 | |
| tdy_lspft | 당일투자손익 | String | N | 12 | |
| lspft2 | 당월투자손익 | String | N | 12 | |
| lspft | 누적투자손익 | String | N | 12 | |
| tdy_lspft_rt | 당일손익율 | String | N | 12 | |
| lspft_ratio | 당월손익율 | String | N | 12 | |
| lspft_rt | 누적손익율 | String | N | 12 | |
| stk_acnt_evlt_prst | 종목별계좌평가현황 | LIST | N | - | |
| - stk_cd | 종목코드 | String | N | 12 | |
| - stk_nm | 종목명 | String | N | 30 | |
| - rmnd_qty | 보유수량 | String | N | 12 | |
| - avg_prc | 평균단가 | String | N | 12 | |
| - cur_prc | 현재가 | String | N | 12 | |
| - evlt_amt | 평가금액 | String | N | 12 | |
| - pl_amt | 손익금액 | String | N | 12 | |
| - pl_rt | 손익율 | String | N | 12 | |
| - loan_dt | 대출일 | String | N | 10 | |
| - pur_amt | 매입금액 | String | N | 12 | |
| - setl_remn | 결제잔고 | String | N | 12 | |
| - pred_buyq | 전일매수수량 | String | N | 12 | |
| - pred_sellq | 전일매도수량 | String | N | 12 | |
| - tdy_buyq | 금일매수수량 | String | N | 12 | |
| - tdy_sellq | 금일매도수량 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 계좌평가현황요청
def fn_kt00004(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00004', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'qry_tp': '0', # 상장폐지조회구분 0:전체, 1:상장폐지종목제외
        'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
    }

    # 3. API 실행
    fn_kt00004(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00004(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..)
```

### 요청/응답 예제

#### Request
```json
{
    "qry_tp" : "0",
    "dmst_stex_tp" : "KRX"
}
```

#### Response
```json
{
    "acnt_nm":"김키움",
    "brch_nm":"키움은행",
    "entr":"000000017534",
    "d2_entra":"000000012550",
    "tot_est_amt":"000000000342",
    "aset_evlt_amt":"000000761950",
    "tot_pur_amt":"000000002786",
    "prsm_dpst_aset_amt":"000000749792",
    "tot_grnt_sella":"000000000000",
    "tdy_lspft_amt":"000000000000",
    "invt_bsamt":"000000000000",
    "lspft_amt":"000000000000",
    "tdy_lspft":"000000000000",
    "lspft2":"000000000000",
    "lspft":"000000000000",
    "tdy_lspft_rt":"0.00",
    "lspft_ratio":"0.00",
    "lspft_rt":"0.00",
    "stk_acnt_evlt_prst": [
        {
            "stk_cd":"A005930",
            "stk_nm":"삼성전자",
            "rmnd_qty":"000000000003",
            "avg_prc":"000000124500",
            "cur_prc":"000000070000",
            "evlt_amt":"000000209542",
            "pl_amt":"-00000163958",
            "pl_rt":"-43.8977",
            "loan_dt":"",
            "pur_amt":"000000373500",
            "setl_remn":"000000000003",
            "pred_buyq":"000000000000",
            "pred_sellq":"000000000000",
            "tdy_buyq":"000000000000",
            "tdy_sellq":"000000000000"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다."
}
```

---

## 체결잔고요청 (kt00005)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | KRX:한국거래소, NXT:넥스트트레이드 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| entr | 예수금 | String | N | 12 | |
| entr_d1 | 예수금D+1 | String | N | 12 | |
| entr_d2 | 예수금D+2 | String | N | 12 | |
| pymn_alow_amt | 출금가능금액 | String | N | 12 | |
| uncl_stk_amt | 미수확보금 | String | N | 12 | |
| repl_amt | 대용금 | String | N | 12 | |
| rght_repl_amt | 권리대용금 | String | N | 12 | |
| ord_alowa | 주문가능현금 | String | N | 12 | |
| ch_uncla | 현금미수금 | String | N | 12 | |
| crd_int_npay_gold | 신용이자미납금 | String | N | 12 | |
| etc_loana | 기타대여금 | String | N | 12 | |
| nrpy_loan | 미상환융자금 | String | N | 12 | |
| profa_ch | 증거금현금 | String | N | 12 | |
| repl_profa | 증거금대용 | String | N | 12 | |
| stk_buy_tot_amt | 주식매수총액 | String | N | 12 | |
| evlt_amt_tot | 평가금액합계 | String | N | 12 | |
| tot_pl_tot | 총손익합계 | String | N | 12 | |
| tot_pl_rt | 총손익률 | String | N | 12 | |
| tot_re_buy_alowa | 총재매수가능금액 | String | N | 12 | |
| 20ord_alow_amt | 20%주문가능금액 | String | N | 12 | |
| 30ord_alow_amt | 30%주문가능금액 | String | N | 12 | |
| 40ord_alow_amt | 40%주문가능금액 | String | N | 12 | |
| 50ord_alow_amt | 50%주문가능금액 | String | N | 12 | |
| 60ord_alow_amt | 60%주문가능금액 | String | N | 12 | |
| 100ord_alow_amt | 100%주문가능금액 | String | N | 12 | |
| crd_loan_tot | 신용융자합계 | String | N | 12 | |
| crd_loan_ls_tot | 신용융자대주합계 | String | N | 12 | |
| crd_grnt_rt | 신용담보비율 | String | N | 12 | |
| dpst_grnt_use_amt_amt | 예탁담보대출금액 | String | N | 12 | |
| grnt_loan_amt | 매도담보대출금액 | String | N | 12 | |
| stk_cntr_remn | 종목별체결잔고 | LIST | N | - | |
| - crd_tp | 신용구분 | String | N | 2 | |
| - loan_dt | 대출일 | String | N | 8 | |
| - expr_dt | 만기일 | String | N | 8 | |
| - stk_cd | 종목번호 | String | N | 12 | |
| - stk_nm | 종목명 | String | N | 30 | |
| - setl_remn | 결제잔고 | String | N | 12 | |
| - cur_qty | 현재잔고 | String | N | 12 | |
| - cur_prc | 현재가 | String | N | 12 | |
| - buy_uv | 매입단가 | String | N | 12 | |
| - pur_amt | 매입금액 | String | N | 12 | |
| - evlt_amt | 평가금액 | String | N | 12 | |
| - evltv_prft | 평가손익 | String | N | 12 | |
| - pl_rt | 손익률 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 체결잔고요청
def fn_kt00005(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00005', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
    }

    # 3. API 실행
    fn_kt00005(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00005(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "dmst_stex_tp" : "KRX"
}
```

#### Response
```json
{
    "entr":"000000017534",
    "entr_d1":"000000017450",
    "entr_d2":"000000012550",
    "pymn_alow_amt":"000000085341",
    "uncl_stk_amt":"000000000000",
    "repl_amt":"000003915500",
    "rght_repl_amt":"000000000000",
    "ord_alowa":"000000085341",
    "ch_uncla":"000000000000",
    "crd_int_npay_gold":"000000000000",
    "etc_loana":"000000000000",
    "nrpy_loan":"000000000000",
    "profa_ch":"000000032193",
    "repl_profa":"000000000000",
    "stk_buy_tot_amt":"000006122786",
    "evlt_amt_tot":"000006236342",
    "tot_pl_tot":"000000113556",
    "tot_pl_rt":"1.8546",
    "tot_re_buy_alowa":"000000135970",
    "20ord_alow_amt":"000000012550",
    "30ord_alow_amt":"000000012550",
    "40ord_alow_amt":"000000012550",
    "50ord_alow_amt":"000000012550",
    "60ord_alow_amt":"000000012550",
    "100ord_alow_amt":"000000012550",
    "crd_loan_tot":"000000000000",
    "crd_loan_ls_tot":"000000000000",
    "crd_grnt_rt":"0.00",
    "dpst_grnt_use_amt_amt":"000000000000",
    "grnt_loan_amt":"000000000000",
    "stk_cntr_remn": [
        {
            "crd_tp":"00",
            "loan_dt":"",
            "expr_dt":"",
            "stk_cd":"A005930",
            "stk_nm":"삼성전자",
            "setl_remn":"000000000003",
            "cur_qty":"000000000003",
            "cur_prc":"000000070000",
            "buy_uv":"000000124500",
            "pur_amt":"000000373500",
            "evlt_amt":"000000209542",
            "evltv_prft":"-00000163958",
            "pl_rt":"-43.8977"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다."
}
```

---

## 계좌별주문체결내역상세요청 (kt00007)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| ord_dt | 주문일자 | String | N | 8 | YYYYMMDD |
| qry_tp | 조회구분 | String | Y | 1 | 1:주문순, 2:역순, 3:미체결, 4:체결내역만 |
| stk_bond_tp | 주식채권구분 | String | Y | 1 | 0:전체, 1:주식, 2:채권 |
| sell_tp | 매도수구분 | String | Y | 1 | 0:전체, 1:매도, 2:매수 |
| stk_cd | 종목코드 | String | N | 12 | 공백허용 (공백일때 전체종목) |
| fr_ord_no | 시작주문번호 | String | N | 7 | 공백허용 (공백일때 전체주문) |
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | %:(전체), KRX:한국거래소, NXT:넥스트트레이드, SOR:최선주문집행 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| acnt_ord_cntr_prps_dtl | 계좌별주문체결내역상세 | LIST | N | - | |
| - ord_no | 주문번호 | String | N | 7 | |
| - stk_cd | 종목번호 | String | N | 12 | |
| - trde_tp | 매매구분 | String | N | 20 | |
| - crd_tp | 신용구분 | String | N | 20 | |
| - ord_qty | 주문수량 | String | N | 10 | |
| - ord_uv | 주문단가 | String | N | 10 | |
| - cnfm_qty | 확인수량 | String | N | 10 | |
| - acpt_tp | 접수구분 | String | N | 20 | |
| - rsrv_tp | 반대여부 | String | N | 20 | |
| - ord_tm | 주문시간 | String | N | 8 | |
| - ori_ord | 원주문 | String | N | 7 | |
| - stk_nm | 종목명 | String | N | 40 | |
| - io_tp_nm | 주문구분 | String | N | 20 | |
| - loan_dt | 대출일 | String | N | 8 | |
| - cntr_qty | 체결수량 | String | N | 10 | |
| - cntr_uv | 체결단가 | String | N | 10 | |
| - ord_remnq | 주문잔량 | String | N | 10 | |
| - comm_ord_tp | 통신구분 | String | N | 20 | |
| - mdfy_cncl | 정정취소 | String | N | 20 | |
| - cnfm_tm | 확인시간 | String | N | 8 | |
| - dmst_stex_tp | 국내거래소구분 | String | N | 8 | |
| - cond_uv | 스톱가 | String | N | 10 | |

### Python 예제 코드

```python
import requests
import json

# 계좌별주문체결내역상세요청
def fn_kt00007(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00007', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'ord_dt': '', # 주문일자 YYYYMMDD
        'qry_tp': '1', # 조회구분 1:주문순, 2:역순, 3:미체결, 4:체결내역만
        'stk_bond_tp': '0', # 주식채권구분 0:전체, 1:주식, 2:채권
        'sell_tp': '0', # 매도수구분 0:전체, 1:매도, 2:매수
        'stk_cd': '005930', # 종목코드 공백허용 (공백일때 전체종목)
        'fr_ord_no': '', # 시작주문번호 공백허용 (공백일때 전체주문)
        'dmst_stex_tp': '%', # 국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행
    }

    # 3. API 실행
    fn_kt00007(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00007(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "ord_dt" : "",
    "qry_tp" : "1",
    "stk_bond_tp" : "0",
    "sell_tp" : "0",
    "stk_cd" : "005930",
    "fr_ord_no" : "",
    "dmst_stex_tp" : "%"
}
```

#### Response
```json
{
    "acnt_ord_cntr_prps_dtl": [
        {
            "ord_no":"0000050",
            "stk_cd":"A069500",
            "trde_tp":"시장가",
            "crd_tp":"보통매매",
            "ord_qty":"0000000001",
            "ord_uv":"0000000000",
            "cnfm_qty":"0000000000",
            "acpt_tp":"접수",
            "rsrv_tp":"",
            "ord_tm":"13:05:43",
            "ori_ord":"0000000",
            "stk_nm":"KODEX 200",
            "io_tp_nm":"현금매수",
            "loan_dt":"",
            "cntr_qty":"0000000001",
            "cntr_uv":"0000004900",
            "ord_remnq":"0000000000",
            "comm_ord_tp":"영웅문4",
            "mdfy_cncl":"",
            "cnfm_tm":"",
            "dmst_stex_tp":"KRX",
            "cond_uv":"0000000000"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다"
}
```

---

## 주문인출가능금액요청 (kt00010)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| io_amt | 입출금액 | String | N | 12 | |
| stk_cd | 종목번호 | String | Y | 12 | |
| trde_tp | 매매구분 | String | Y | 1 | 1:매도, 2:매수 |
| trde_qty | 매매수량 | String | N | 10 | |
| uv | 매수가격 | String | Y | 10 | |
| exp_buy_unp | 예상매수단가 | String | N | 10 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| profa_20ord_alow_amt | 증거금20%주문가능금액 | String | N | 12 | |
| profa_20ord_alowq | 증거금20%주문가능수량 | String | N | 10 | |
| profa_30ord_alow_amt | 증거금30%주문가능금액 | String | N | 12 | |
| profa_30ord_alowq | 증거금30%주문가능수량 | String | N | 10 | |
| profa_40ord_alow_amt | 증거금40%주문가능금액 | String | N | 12 | |
| profa_40ord_alowq | 증거금40%주문가능수량 | String | N | 10 | |
| profa_50ord_alow_amt | 증거금50%주문가능금액 | String | N | 12 | |
| profa_50ord_alowq | 증거금50%주문가능수량 | String | N | 10 | |
| profa_60ord_alow_amt | 증거금60%주문가능금액 | String | N | 12 | |
| profa_60ord_alowq | 증거금60%주문가능수량 | String | N | 10 | |
| profa_rdex_60ord_alow_amt | 증거금감면60%주문가능금 | String | N | 12 | |
| profa_rdex_60ord_alowq | 증거금감면60%주문가능수 | String | N | 10 | |
| profa_100ord_alow_amt | 증거금100%주문가능금액 | String | N | 12 | |
| profa_100ord_alowq | 증거금100%주문가능수량 | String | N | 10 | |
| pred_reu_alowa | 전일재사용가능금액 | String | N | 12 | |
| tdy_reu_alowa | 금일재사용가능금액 | String | N | 12 | |
| entr | 예수금 | String | N | 12 | |
| repl_amt | 대용금 | String | N | 12 | |
| uncla | 미수금 | String | N | 12 | |
| ord_pos_repl | 주문가능대용 | String | N | 12 | |
| ord_alowa | 주문가능현금 | String | N | 12 | |
| wthd_alowa | 인출가능금액 | String | N | 12 | |
| nxdy_wthd_alowa | 익일인출가능금액 | String | N | 12 | |
| pur_amt | 매입금액 | String | N | 12 | |
| cmsn | 수수료 | String | N | 12 | |
| pur_exct_amt | 매입정산금 | String | N | 12 | |
| d2entra | D2추정예수금 | String | N | 12 | |
| profa_rdex_aplc_tp | 증거금감면적용구분 | String | N | 1 | 0:일반, 1:60%감면 |

### Python 예제 코드

```python
import requests
import json

# 주문인출가능금액요청
def fn_kt00010(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00010', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'io_amt': '', # 입출금액 
        'stk_cd': '005930', # 종목번호 
        'trde_tp': '2', # 매매구분 1:매도, 2:매수
        'trde_qty': '', # 매매수량 
        'uv': '267000', # 매수가격 
        'exp_buy_unp': '', # 예상매수단가 
    }

    # 3. API 실행
    fn_kt00010(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00010(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "io_amt" : "",
    "stk_cd" : "005930",
    "trde_tp" : "2",
    "trde_qty" : "",
    "uv" : "267000",
    "exp_buy_unp" : ""
}
```

#### Response
```json
{
    "profa_20ord_alow_amt":"000000012550",
    "profa_20ord_alowq":"0000000000",
    "profa_30ord_alow_amt":"000000012550",
    "profa_30ord_alowq":"0000000000",
    "profa_40ord_alow_amt":"000000012550",
    "profa_40ord_alowq":"0000000000",
    "profa_50ord_alow_amt":"000000012550",
    "profa_50ord_alowq":"0000000000",
    "profa_60ord_alow_amt":"000000012550",
    "profa_60ord_alowq":"0000000000",
    "profa_rdex_60ord_alow_amt":"000000012550",
    "profa_rdex_60ord_alowq":"0000000000",
    "profa_100ord_alow_amt":"000000012550",
    "profa_100ord_alowq":"0000000000",
    "pred_reu_alowa":"000000027194",
    "tdy_reu_alowa":"000000000000",
    "entr":"000000017534",
    "repl_amt":"000003915500",
    "uncla":"000000000000",
    "ord_pos_repl":"000003915500",
    "ord_alowa":"000000085341",
    "wthd_alowa":"000000085341",
    "nxdy_wthd_alowa":"000000012550",
    "pur_amt":"000000000000",
    "cmsn":"000000000000",
    "pur_exct_amt":"000000000000",
    "d2entra":"000000012550",
    "profa_rdex_aplc_tp":"0",
    "return_code":0,
    "return_msg":"주문/인출가능금액 시뮬레이션 조회완료하였습니다."
}
```

---

## 계좌별주문체결현황요청 (kt00009)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| ord_dt | 주문일자 | String | N | 8 | YYYYMMDD |
| stk_bond_tp | 주식채권구분 | String | Y | 1 | 0:전체, 1:주식, 2:채권 |
| mrkt_tp | 시장구분 | String | Y | 1 | 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN |
| sell_tp | 매도수구분 | String | Y | 1 | 0:전체, 1:매도, 2:매수 |
| qry_tp | 조회구분 | String | Y | 1 | 0:전체, 1:체결 |
| stk_cd | 종목코드 | String | N | 12 | 전문 조회할 종목코드 |
| fr_ord_no | 시작주문번호 | String | N | 7 | |
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | %:(전체), KRX:한국거래소, NXT:넥스트트레이드, SOR:최선주문집행 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| sell_grntl_engg_amt | 매도약정금액 | String | N | 12 | |
| buy_engg_amt | 매수약정금액 | String | N | 12 | |
| engg_amt | 약정금액 | String | N | 12 | |
| acnt_ord_cntr_prst_array | 계좌별주문체결현황배열 | LIST | N | - | |
| - stk_bond_tp | 주식채권구분 | String | N | 1 | |
| - ord_no | 주문번호 | String | N | 7 | |
| - stk_cd | 종목번호 | String | N | 12 | |
| - trde_tp | 매매구분 | String | N | 15 | |
| - io_tp_nm | 주문유형구분 | String | N | 20 | |
| - ord_qty | 주문수량 | String | N | 10 | |
| - ord_uv | 주문단가 | String | N | 10 | |
| - cnfm_qty | 확인수량 | String | N | 10 | |
| - rsrv_oppo | 예약/반대 | String | N | 4 | |
| - cntr_no | 체결번호 | String | N | 7 | |
| - acpt_tp | 접수구분 | String | N | 8 | |
| - orig_ord_no | 원주문번호 | String | N | 7 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - setl_tp | 결제구분 | String | N | 8 | |
| - crd_deal_tp | 신용거래구분 | String | N | 20 | |
| - cntr_qty | 체결수량 | String | N | 10 | |
| - cntr_uv | 체결단가 | String | N | 10 | |
| - comm_ord_tp | 통신구분 | String | N | 8 | |
| - mdfy_cncl_tp | 정정/취소구분 | String | N | 12 | |
| - cntr_tm | 체결시간 | String | N | 8 | |
| - dmst_stex_tp | 국내거래소구분 | String | N | 6 | |
| - cond_uv | 스톱가 | String | N | 10 | |

### Python 예제 코드

```python
import requests
import json

# 계좌별주문체결현황요청
def fn_kt00009(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00009', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'ord_dt': '', # 주문일자 YYYYMMDD
        'stk_bond_tp': '0', # 주식채권구분 0:전체, 1:주식, 2:채권
        'mrkt_tp': '0', # 시장구분 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN
        'sell_tp': '0', # 매도수구분 0:전체, 1:매도, 2:매수
        'qry_tp': '0', # 조회구분 0:전체, 1:체결
        'stk_cd': '', # 종목코드 전문 조회할 종목코드
        'fr_ord_no': '', # 시작주문번호 
        'dmst_stex_tp': 'KRX', # 국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행
    }

    # 3. API 실행
    fn_kt00009(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00009(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "ord_dt" : "",
    "stk_bond_tp" : "0",
    "mrkt_tp" : "0",
    "sell_tp" : "0",
    "qry_tp" : "0",
    "stk_cd" : "",
    "fr_ord_no" : "",
    "dmst_stex_tp" : "KRX"
}
```

#### Response
```json
{
    "sell_grntl_engg_amt":"000000000000",
    "buy_engg_amt":"000000004900",
    "engg_amt":"000000004900",
    "acnt_ord_cntr_prst_array": [
        {
            "stk_bond_tp":"1",
            "ord_no":"0000050",
            "stk_cd":"A069500",
            "trde_tp":"시장가",
            "io_tp_nm":"현금매수",
            "ord_qty":"0000000001",
            "ord_uv":"0000000000",
            "cnfm_qty":"0000000000",
            "rsrv_oppo":"",
            "cntr_no":"0000001",
            "acpt_tp":"접수",
            "orig_ord_no":"0000000",
            "stk_nm":"KODEX 200",
            "setl_tp":"삼일결제",
            "crd_deal_tp":"보통매매",
            "cntr_qty":"0000000001",
            "cntr_uv":"0000004900",
            "comm_ord_tp":"영웅문4",
            "mdfy_cncl_tp":"",
            "cntr_tm":"13:07:47",
            "dmst_stex_tp":"KRX",
            "cond_uv":"0000000000"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다"
}
```

---

## 계좌별익일결제예정내역요청 (kt00008)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| strt_dcd_seq | 시작결제번호 | String | N | 7 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| trde_dt | 매매일자 | String | N | 8 | |
| setl_dt | 결제일자 | String | N | 8 | |
| sell_amt_sum | 매도정산합 | String | N | 12 | |
| buy_amt_sum | 매수정산합 | String | N | 12 | |
| acnt_nxdy_setl_frcs_prps_array | 계좌별익일결제예정내역배열 | LIST | N | - | |
| - seq | 일련번호 | String | N | 7 | |
| - stk_cd | 종목번호 | String | N | 12 | |
| - loan_dt | 대출일 | String | N | 8 | |
| - qty | 수량 | String | N | 12 | |
| - engg_amt | 약정금액 | String | N | 12 | |
| - cmsn | 수수료 | String | N | 12 | |
| - incm_tax | 소득세 | String | N | 12 | |
| - rstx | 농특세 | String | N | 12 | |
| - stk_nm | 종목명 | String | N | 40 | |
| - sell_tp | 매도수구분 | String | N | 10 | |
| - unp | 단가 | String | N | 12 | |
| - exct_amt | 정산금액 | String | N | 12 | |
| - trde_tax | 거래세 | String | N | 12 | |
| - resi_tax | 주민세 | String | N | 12 | |
| - crd_tp | 신용구분 | String | N | 20 | |

### Python 예제 코드

```python
import requests
import json

# 계좌별익일결제예정내역요청
def fn_kt00008(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00008', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'strt_dcd_seq': '', # 시작결제번호 
    }

    # 3. API 실행
    fn_kt00008(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00008(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "strt_dcd_seq" : ""
}
```

#### Response
```json
{
    "trde_dt":"20241122",
    "setl_dt":"20241126",
    "sell_amt_sum":"000000048156",
    "buy_amt_sum":"000000048240",
    "acnt_nxdy_setl_frcs_prps_array": [
        {
            "seq":"0010006",
            "stk_cd":"A005930",
            "loan_dt":"",
            "qty":"000000000001",
            "engg_amt":"000000016080",
            "cmsn":"000000000000",
            "incm_tax":"000000000000",
            "rstx":"000000000000",
            "stk_nm":"삼성전자",
            "sell_tp":"매도",
            "unp":"000000016080",
            "exct_amt":"000000016052",
            "trde_tax":"000000000028",
            "resi_tax":"000000000000",
            "crd_tp":"현금매도 K"
        },
        {
            "seq":"0010007",
            "stk_cd":"A005930",
            "loan_dt":"",
            "qty":"000000000002",
            "engg_amt":"000000032160",
            "cmsn":"000000000000",
            "incm_tax":"000000000000",
            "rstx":"000000000000",
            "stk_nm":"삼성전자",
            "sell_tp":"매도",
            "unp":"000000016080",
            "exct_amt":"000000032104",
            "trde_tax":"000000000056",
            "resi_tax":"000000000000",
            "crd_tp":"프로그램매도 K"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다"
}
```

---

## 증거금율별주문가능수량조회요청 (kt00011)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목번호 | String | Y | 12 | |
| uv | 매수가격 | String | N | 10 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_profa_rt | 종목증거금율 | String | N | 15 | |
| profa_rt | 계좌증거금율 | String | N | 15 | |
| aplc_rt | 적용증거금율 | String | N | 15 | |
| profa_20ord_alow_amt | 증거금20%주문가능금액 | String | N | 12 | |
| profa_20ord_alowq | 증거금20%주문가능수량 | String | N | 12 | |
| profa_20pred_reu_amt | 증거금20%전일재사용금액 | String | N | 12 | |
| profa_20tdy_reu_amt | 증거금20%금일재사용금액 | String | N | 12 | |
| profa_30ord_alow_amt | 증거금30%주문가능금액 | String | N | 12 | |
| profa_30ord_alowq | 증거금30%주문가능수량 | String | N | 12 | |
| profa_30pred_reu_amt | 증거금30%전일재사용금액 | String | N | 12 | |
| profa_30tdy_reu_amt | 증거금30%금일재사용금액 | String | N | 12 | |
| profa_40ord_alow_amt | 증거금40%주문가능금액 | String | N | 12 | |
| profa_40ord_alowq | 증거금40%주문가능수량 | String | N | 12 | |
| profa_40pred_reu_amt | 증거금40전일재사용금액 | String | N | 12 | |
| profa_40tdy_reu_amt | 증거금40%금일재사용금액 | String | N | 12 | |
| profa_50ord_alow_amt | 증거금50%주문가능금액 | String | N | 12 | |
| profa_50ord_alowq | 증거금50%주문가능수량 | String | N | 12 | |
| profa_50pred_reu_amt | 증거금50%전일재사용금액 | String | N | 12 | |
| profa_50tdy_reu_amt | 증거금50%금일재사용금액 | String | N | 12 | |
| profa_60ord_alow_amt | 증거금60%주문가능금액 | String | N | 12 | |
| profa_60ord_alowq | 증거금60%주문가능수량 | String | N | 12 | |
| profa_60pred_reu_amt | 증거금60%전일재사용금액 | String | N | 12 | |
| profa_60tdy_reu_amt | 증거금60%금일재사용금액 | String | N | 12 | |
| profa_100ord_alow_amt | 증거금100%주문가능금액 | String | N | 12 | |
| profa_100ord_alowq | 증거금100%주문가능수량 | String | N | 12 | |
| profa_100pred_reu_amt | 증거금100%전일재사용금액 | String | N | 12 | |
| profa_100tdy_reu_amt | 증거금100%금일재사용금액 | String | N | 12 | |
| min_ord_alow_amt | 미수불가주문가능금액 | String | N | 12 | |
| min_ord_alowq | 미수불가주문가능수량 | String | N | 12 | |
| min_pred_reu_amt | 미수불가전일재사용금액 | String | N | 12 | |
| min_tdy_reu_amt | 미수불가금일재사용금액 | String | N | 12 | |
| entr | 예수금 | String | N | 12 | |
| repl_amt | 대용금 | String | N | 12 | |
| uncla | 미수금 | String | N | 12 | |
| ord_pos_repl | 주문가능대용 | String | N | 12 | |
| ord_alowa | 주문가능현금 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 증거금율별주문가능수량조회요청
def fn_kt00011(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00011', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stk_cd': '005930', # 종목번호 
        'uv': '', # 매수가격 
    }

    # 3. API 실행
    fn_kt00011(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00011(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stk_cd" : "005930",
    "uv" : ""
}
```

#### Response
```json
{
    "stk_profa_rt":"20%",
    "profa_rt":"100%",
    "aplc_rt":"100%",
    "profa_20ord_alow_amt":"",
    "profa_20ord_alowq":"",
    "profa_20pred_reu_amt":"",
    "profa_20tdy_reu_amt":"",
    "profa_30ord_alow_amt":"",
    "profa_30ord_alowq":"",
    "profa_30pred_reu_amt":"",
    "profa_30tdy_reu_amt":"",
    "profa_40ord_alow_amt":"",
    "profa_40ord_alowq":"",
    "profa_40pred_reu_amt":"",
    "profa_40tdy_reu_amt":"",
    "profa_50ord_alow_amt":"",
    "profa_50ord_alowq":"",
    "profa_50pred_reu_amt":"",
    "profa_50tdy_reu_amt":"",
    "profa_60ord_alow_amt":"",
    "profa_60ord_alowq":"",
    "profa_60pred_reu_amt":"",
    "profa_60tdy_reu_amt":"",
    "profa_100ord_alow_amt":"",
    "profa_100ord_alowq":"",
    "profa_100pred_reu_amt":"",
    "profa_100tdy_reu_amt":"",
    "min_ord_alow_amt":"000000063380",
    "min_ord_alowq":"000000000000",
    "min_pred_reu_amt":"000000027194",
    "min_tdy_reu_amt":"000000000000",
    "entr":"000000017534",
    "repl_amt":"000003915500",
    "uncla":"000000000000",
    "ord_pos_repl":"000003915500",
    "ord_alowa":"000000085341",
    "return_code":0,
    "return_msg":"자료를 조회하였습니다."
}
```

---

## 신용보증금율별주문가능수량조회요청 (kt00012)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_cd | 종목번호 | String | Y | 12 | |
| uv | 매수가격 | String | N | 10 | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| stk_assr_rt | 종목보증금율 | String | N | 1 | |
| stk_assr_rt_nm | 종목보증금율명 | String | N | 4 | |
| assr_30ord_alow_amt | 보증금30%주문가능금액 | String | N | 12 | |
| assr_30ord_alowq | 보증금30%주문가능수량 | String | N | 12 | |
| assr_30pred_reu_amt | 보증금30%전일재사용금액 | String | N | 12 | |
| assr_30tdy_reu_amt | 보증금30%금일재사용금액 | String | N | 12 | |
| assr_40ord_alow_amt | 보증금40%주문가능금액 | String | N | 12 | |
| assr_40ord_alowq | 보증금40%주문가능수량 | String | N | 12 | |
| assr_40pred_reu_amt | 보증금40%전일재사용금액 | String | N | 12 | |
| assr_40tdy_reu_amt | 보증금40%금일재사용금액 | String | N | 12 | |
| assr_50ord_alow_amt | 보증금50%주문가능금액 | String | N | 12 | |
| assr_50ord_alowq | 보증금50%주문가능수량 | String | N | 12 | |
| assr_50pred_reu_amt | 보증금50%전일재사용금액 | String | N | 12 | |
| assr_50tdy_reu_amt | 보증금50%금일재사용금액 | String | N | 12 | |
| assr_60ord_alow_amt | 보증금60%주문가능금액 | String | N | 12 | |
| assr_60ord_alowq | 보증금60%주문가능수량 | String | N | 12 | |
| assr_60pred_reu_amt | 보증금60%전일재사용금액 | String | N | 12 | |
| assr_60tdy_reu_amt | 보증금60%금일재사용금액 | String | N | 12 | |
| entr | 예수금 | String | N | 12 | |
| repl_amt | 대용금 | String | N | 12 | |
| uncla | 미수금 | String | N | 12 | |
| ord_pos_repl | 주문가능대용 | String | N | 12 | |
| ord_alowa | 주문가능현금 | String | N | 12 | |
| out_alowa | 미수가능금액 | String | N | 12 | |
| out_pos_qty | 미수가능수량 | String | N | 12 | |
| min_amt | 미수불가금액 | String | N | 12 | |
| min_qty | 미수불가수량 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 신용보증금율별주문가능수량조회요청
def fn_kt00012(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00012', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'stk_cd': '005930', # 종목번호 
        'uv': '', # 매수가격 
    }

    # 3. API 실행
    fn_kt00012(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00012(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "stk_cd" : "005930",
    "uv" : ""
}
```

#### Response
```json
{
    "stk_assr_rt": "B",
    "stk_assr_rt_nm": "45%",
    "assr_30ord_alow_amt": "003312045139",
    "assr_30ord_alowq": "000000000000",
    "assr_30pred_reu_amt": "000000000000",
    "assr_30tdy_reu_amt": "000000048994",
    "assr_40ord_alow_amt": "002208030092",
    "assr_40ord_alowq": "000000000000",
    "assr_40pred_reu_amt": "000000000000",
    "assr_40tdy_reu_amt": "000000048994",
    "assr_50ord_alow_amt": "001987227084",
    "assr_50ord_alowq": "000000000000",
    "assr_50pred_reu_amt": "000000000000",
    "assr_50tdy_reu_amt": "000000048994",
    "assr_60ord_alow_amt": "001656022569",
    "assr_60ord_alowq": "000000000000",
    "assr_60pred_reu_amt": "000000000000",
    "assr_60tdy_reu_amt": "000000048994",
    "entr": "000994946131",
    "repl_amt": "000001643660",
    "uncla": "000000000000",
    "ord_pos_repl": "000002420949",
    "ord_alowa": "000993564548",
    "out_alowa": "002208030092",
    "out_pos_qty": "000000000000",
    "min_amt": "002207294240",
    "min_qty": "000000000000",
    "return_code": 0,
    "return_msg": "신용보증금율별 주문가능수량 조회(한도정상)"
}
```

---

## 증거금세부내역조회요청 (kt00013)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| | (입력 파라미터 없음) | | | | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| tdy_reu_objt_amt | 금일재사용대상금액 | String | N | 15 | |
| tdy_reu_use_amt | 금일재사용사용금액 | String | N | 15 | |
| tdy_reu_alowa | 금일재사용가능금액 | String | N | 15 | |
| tdy_reu_lmtt_amt | 금일재사용제한금액 | String | N | 15 | |
| tdy_reu_alowa_fin | 금일재사용가능금액최종 | String | N | 15 | |
| pred_reu_objt_amt | 전일재사용대상금액 | String | N | 15 | |
| pred_reu_use_amt | 전일재사용사용금액 | String | N | 15 | |
| pred_reu_alowa | 전일재사용가능금액 | String | N | 15 | |
| pred_reu_lmtt_amt | 전일재사용제한금액 | String | N | 15 | |
| pred_reu_alowa_fin | 전일재사용가능금액최종 | String | N | 15 | |
| ch_amt | 현금금액 | String | N | 15 | |
| ch_profa | 현금증거금 | String | N | 15 | |
| use_pos_ch | 사용가능현금 | String | N | 15 | |
| ch_use_lmtt_amt | 현금사용제한금액 | String | N | 15 | |
| use_pos_ch_fin | 사용가능현금최종 | String | N | 15 | |
| repl_amt_amt | 대용금액 | String | N | 15 | |
| repl_profa | 대용증거금 | String | N | 15 | |
| use_pos_repl | 사용가능대용 | String | N | 15 | |
| repl_use_lmtt_amt | 대용사용제한금액 | String | N | 15 | |
| use_pos_repl_fin | 사용가능대용최종 | String | N | 15 | |
| crd_grnta_ch | 신용보증금현금 | String | N | 15 | |
| crd_grnta_repl | 신용보증금대용 | String | N | 15 | |
| crd_grnt_ch | 신용담보금현금 | String | N | 15 | |
| crd_grnt_repl | 신용담보금대용 | String | N | 15 | |
| uncla | 미수금 | String | N | 12 | |
| ls_grnt_reu_gold | 대주담보금재사용금 | String | N | 15 | |
| 20ord_alow_amt | 20%주문가능금액 | String | N | 15 | |
| 30ord_alow_amt | 30%주문가능금액 | String | N | 15 | |
| 40ord_alow_amt | 40%주문가능금액 | String | N | 15 | |
| 50ord_alow_amt | 50%주문가능금액 | String | N | 15 | |
| 60ord_alow_amt | 60%주문가능금액 | String | N | 15 | |
| 100ord_alow_amt | 100%주문가능금액 | String | N | 15 | |
| tdy_crd_rpya_loss_amt | 금일신용상환손실금액 | String | N | 15 | |
| pred_crd_rpya_loss_amt | 전일신용상환손실금액 | String | N | 15 | |
| tdy_ls_rpya_loss_repl_profa | 금일대주상환손실대용증거금 | String | N | 15 | |
| pred_ls_rpya_loss_repl_profa | 전일대주상환손실대용증거금 | String | N | 15 | |
| evlt_repl_amt_spg_use_skip | 평가대용금(현물사용제외) | String | N | 15 | |
| evlt_repl_rt | 평가대용비율 | String | N | 15 | |
| crd_repl_profa | 신용대용증거금 | String | N | 15 | |
| ch_ord_repl_profa | 현금주문대용증거금 | String | N | 15 | |
| crd_ord_repl_profa | 신용주문대용증거금 | String | N | 15 | |
| crd_repl_conv_gold | 신용대용환산금 | String | N | 15 | |
| repl_alowa | 대용가능금액(현금제한) | String | N | 15 | |
| repl_alowa_2 | 대용가능금액2(신용제한) | String | N | 15 | |
| ch_repl_lck_gold | 현금대용부족금 | String | N | 15 | |
| crd_repl_lck_gold | 신용대용부족금 | String | N | 15 | |
| ch_ord_alow_repla | 현금주문가능대용금 | String | N | 15 | |
| crd_ord_alow_repla | 신용주문가능대용금 | String | N | 15 | |
| d2vexct_entr | D2가정산예수금 | String | N | 15 | |
| d2ch_ord_alow_amt | D2현금주문가능금액 | String | N | 15 | |

### Python 예제 코드

```python
import requests
import json

# 증거금세부내역조회요청
def fn_kt00013(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00013', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {}

    # 3. API 실행
    fn_kt00013(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00013(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{}
```

#### Response
```json
{
    "tdy_reu_objt_amt":"000000000000000",
    "tdy_reu_use_amt":"000000000000000",
    "tdy_reu_alowa":"000000000000000",
    "tdy_reu_lmtt_amt":"000000000000000",
    "tdy_reu_alowa_fin":"000000000000000",
    "pred_reu_objt_amt":"000000000048141",
    "pred_reu_use_amt":"000000000020947",
    "pred_reu_alowa":"000000000027194",
    "pred_reu_lmtt_amt":"000000000000000",
    "pred_reu_alowa_fin":"000000000027194",
    "ch_amt":"000000000017534",
    "ch_profa":"000000000032193",
    "use_pos_ch":"000000000085341",
    "ch_use_lmtt_amt":"000000000000000",
    "use_pos_ch_fin":"000000000085341",
    "repl_amt_amt":"000000003915500",
    "repl_profa":"000000000000000",
    "use_pos_repl":"000000003915500",
    "repl_use_lmtt_amt":"000000000000000",
    "use_pos_repl_fin":"000000003915500",
    "crd_grnta_ch":"000000000000000",
    "crd_grnta_repl":"000000000000000",
    "crd_grnt_ch":"000000000000000",
    "crd_grnt_repl":"000000000000000",
    "uncla":"000000000000",
    "ls_grnt_reu_gold":"000000000000000",
    "20ord_alow_amt":"000000000012550",
    "30ord_alow_amt":"000000000012550",
    "40ord_alow_amt":"000000000012550",
    "50ord_alow_amt":"000000000012550",
    "60ord_alow_amt":"000000000012550",
    "100ord_alow_amt":"000000000012550",
    "tdy_crd_rpya_loss_amt":"000000000000000",
    "pred_crd_rpya_loss_amt":"000000000000000",
    "tdy_ls_rpya_loss_repl_profa":"000000000000000",
    "pred_ls_rpya_loss_repl_profa":"000000000000000",
    "evlt_repl_amt_spg_use_skip":"000000006193400",
    "evlt_repl_rt":"0.6322053",
    "crd_repl_profa":"000000000000000",
    "ch_ord_repl_profa":"000000000000000",
    "crd_ord_repl_profa":"000000000000000",
    "crd_repl_conv_gold":"000000000000000",
    "repl_alowa":"000000003915500",
    "repl_alowa_2":"000000003915500",
    "ch_repl_lck_gold":"000000000000000",
    "crd_repl_lck_gold":"000000000000000",
    "ch_ord_alow_repla":"000000003915500",
    "crd_ord_alow_repla":"000000006193400",
    "d2vexct_entr":"000000000012550",
    "d2ch_ord_alow_amt":"000000000012550",
    "return_code":0,
    "return_msg":"조회가 완료되었습니다."
}
```

---

## 위탁종합거래내역요청 (kt00015)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |
| tp | 구분 | String | Y | 1 | 0:전체, 1:입출금, 2:입출고, 3:매매, 4:매수, 5:매도, 6:입금, 7:출금, A:예탁담보대출입금, B:매도담보대출입금, C:현금상환(융자,담보상환), F:환전, M:입출금+환전, G:외화매수, H:외화매도, I:환전정산입금, J:환전정산출금 |
| stk_cd | 종목코드 | String | N | 12 | |
| crnc_cd | 통화코드 | String | N | 3 | |
| gds_tp | 상품구분 | String | Y | 1 | 0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품 |
| frgn_stex_code | 해외거래소코드 | String | N | 10 | |
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | %:(전체), KRX:한국거래소, NXT:넥스트트레이드 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| trst_ovrl_trde_prps_array | 위탁종합거래내역배열 | LIST | N | - | |
| - trde_dt | 거래일자 | String | N | 8 | |
| - trde_no | 거래번호 | String | N | 9 | |
| - rmrk_nm | 적요명 | String | N | 60 | |
| - crd_deal_tp_nm | 신용거래구분명 | String | N | 20 | |
| - exct_amt | 정산금액 | String | N | 15 | |
| - loan_amt_rpya | 대출금상환 | String | N | 15 | |
| - fc_trde_amt | 거래금액(외) | String | N | 15 | |
| - fc_exct_amt | 정산금액(외) | String | N | 15 | |
| - entra_remn | 예수금잔고 | String | N | 15 | |
| - crnc_cd | 통화코드 | String | N | 3 | |
| - trde_ocr_tp | 거래종류구분 | String | N | 2 | 1:입출금, 2:펀드, 3:ELS, 4:채권, 5:해외채권, 6:외화RP, 7:외화발행어음 |
| - trde_kind_nm | 거래종류명 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 40 | |
| - trde_amt | 거래금액 | String | N | 15 | |
| - trde_agri_tax | 거래및농특세 | String | N | 15 | |
| - rpy_diffa | 상환차금 | String | N | 15 | |
| - fc_trde_tax | 거래세(외) | String | N | 15 | |
| - dly_sum | 연체합 | String | N | 15 | |
| - fc_entra | 외화예수금잔고 | String | N | 15 | |
| - mdia_tp_nm | 매체구분명 | String | N | 20 | |
| - io_tp | 입출구분 | String | N | 1 | |
| - io_tp_nm | 입출구분명 | String | N | 10 | |
| - orig_deal_no | 원거래번호 | String | N | 9 | |
| - stk_cd | 종목코드 | String | N | 12 | |
| - trde_qty_jwa_cnt | 거래수량/좌수 | String | N | 30 | |
| - cmsn | 수수료 | String | N | 15 | |
| - int_ls_usfe | 이자/대주이용 | String | N | 15 | |
| - fc_cmsn | 수수료(외) | String | N | 15 | |
| - fc_dly_sum | 연체합(외) | String | N | 15 | |
| - vlbl_nowrm | 유가금잔 | String | N | 30 | |
| - proc_tm | 처리시간 | String | N | 111 | |
| - isin_cd | ISIN코드 | String | N | 12 | |
| - stex_cd | 거래소코드 | String | N | 10 | |
| - stex_nm | 거래소명 | String | N | 20 | |
| - trde_unit | 거래단가/환율 | String | N | 20 | |
| - incm_resi_tax | 소득/주민세 | String | N | 15 | |
| - loan_dt | 대출일 | String | N | 8 | |
| - uncl_ocr | 미수(원/주) | String | N | 30 | |
| - rpym_sum | 변제합 | String | N | 30 | |
| - cntr_dt | 체결일 | String | N | 8 | |
| - rcpy_no | 출납번호 | String | N | 20 | |
| - prcsr | 처리자 | String | N | 20 | |
| - proc_brch | 처리점 | String | N | 20 | |
| - trde_stle | 매매형태 | String | N | 40 | |
| - txon_base_pric | 과세기준가 | String | N | 15 | |
| - tax_sum_cmsn | 세금수수료합 | String | N | 15 | |
| - frgn_pay_txam | 외국납부세액(외) | String | N | 15 | |
| - fc_uncl_ocr | 미수(외) | String | N | 15 | |
| - rpym_sum_fr | 변제합(외) | String | N | 30 | |
| - rcpmnyer | 입금자 | String | N | 20 | |
| - trde_prtc_tp | 거래내역구분 | String | N | 2 | |

### Python 예제 코드

```python
import requests
import json

# 위탁종합거래내역요청
def fn_kt00015(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00015', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'strt_dt': '20241121', # 시작일자 
        'end_dt': '20241125', # 종료일자 
        'tp': '0', # 구분 0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,6:입금,7:출금,A:예탁담보대출입금,B:매도담보대출입금,C:현금상환(융자,담보상환),F:환전,M:입출금+환전,G:외화매수,H:외화매도,I:환전정산입금,J:환전정산출금
        'stk_cd': '', # 종목코드 
        'crnc_cd': '', # 통화코드 
        'gds_tp': '0', # 상품구분 0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품
        'frgn_stex_code': '', # 해외거래소코드 
        'dmst_stex_tp': '%', # 국내거래소구분 %:(전체),KRX:한국거래소,NXT:넥스트트레이드
    }

    # 3. API 실행
    fn_kt00015(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00015(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "strt_dt" : "20241121",
    "end_dt" : "20241125",
    "tp" : "0",
    "stk_cd" : "",
    "crnc_cd" : "",
    "gds_tp" : "0",
    "frgn_stex_code" : "",
    "dmst_stex_tp" : "%"
}
```

#### Response
```json
{
    "acnt_no":"6081-2***-11 [김키움]",
    "trst_ovrl_trde_prps_array": [
        {
            "trde_dt":"20241121",
            "trde_no":"000000001",
            "rmrk_nm":"장내매도",
            "crd_deal_tp_nm":"보통매매",
            "exct_amt":"000000000056798",
            "loan_amt_rpya":"000000000000000",
            "fc_trde_amt":"0.00",
            "fc_exct_amt":"0.00",
            "entra_remn":"000000994658290",
            "crnc_cd":"KRW",
            "trde_ocr_tp":"9",
            "trde_kind_nm":"매매",
            "stk_nm":"삼성전자",
            "trde_amt":"000000000056900",
            "trde_agri_tax":"000000000000102",
            "rpy_diffa":"000000000000000",
            "fc_trde_tax":"0.00",
            "dly_sum":"000000000000000",
            "fc_entra":"0.00",
            "mdia_tp_nm":"REST API",
            "io_tp":"1",
            "io_tp_nm":"매도",
            "orig_deal_no":"000000000",
            "stk_cd":"A005930",
            "trde_qty_jwa_cnt":"1",
            "cmsn":"000000000000000",
            "int_ls_usfe":"000000000000000",
            "fc_cmsn":"0.00",
            "fc_dly_sum":"0.00",
            "vlbl_nowrm":"21",
            "proc_tm":"08:12:35",
            "isin_cd":"KR7005930003",
            "stex_cd":"",
            "stex_nm":"",
            "trde_unit":"56,900",
            "incm_resi_tax":"000000000000000",
            "loan_dt":"",
            "uncl_ocr":"",
            "rpym_sum":"",
            "cntr_dt":"20241119",
            "rcpy_no":"",
            "prcsr":"DAILY",
            "proc_brch":"키움은행",
            "trde_stle":"",
            "txon_base_pric":"0.00",
            "tax_sum_cmsn":"000000000000102",
            "frgn_pay_txam":"0.00",
            "fc_uncl_ocr":"0.00",
            "rpym_sum_fr":"",
            "rcpmnyer":"",
            "trde_prtc_tp":"11"
        }
    ],
    "return_code":0,
    "return_msg":"조회가 완료되었습니다"
}
```

---

## 일별계좌수익률상세현황요청 (kt00016)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| fr_dt | 평가시작일 | String | Y | 8 | YYYYMMDD |
| to_dt | 평가종료일 | String | Y | 8 | YYYYMMDD |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| mang_empno | 관리사원번호 | String | N | 8 | |
| mngr_nm | 관리자명 | String | N | 8 | |
| dept_nm | 관리자지점 | String | N | 30 | |
| entr_fr | 예수금_초 | String | N | 30 | |
| entr_to | 예수금_말 | String | N | 12 | |
| scrt_evlt_amt_fr | 유가증권평가금액_초 | String | N | 12 | |
| scrt_evlt_amt_to | 유가증권평가금액_말 | String | N | 12 | |
| ls_grnt_fr | 대주담보금_초 | String | N | 12 | |
| ls_grnt_to | 대주담보금_말 | String | N | 12 | |
| crd_loan_fr | 신용융자금_초 | String | N | 12 | |
| crd_loan_to | 신용융자금_말 | String | N | 12 | |
| ch_uncla_fr | 현금미수금_초 | String | N | 12 | |
| ch_uncla_to | 현금미수금_말 | String | N | 12 | |
| krw_asgna_fr | 원화대용금_초 | String | N | 12 | |
| krw_asgna_to | 원화대용금_말 | String | N | 12 | |
| ls_evlta_fr | 대주평가금_초 | String | N | 12 | |
| ls_evlta_to | 대주평가금_말 | String | N | 12 | |
| rght_evlta_fr | 권리평가금_초 | String | N | 12 | |
| rght_evlta_to | 권리평가금_말 | String | N | 12 | |
| loan_amt_fr | 대출금_초 | String | N | 12 | |
| loan_amt_to | 대출금_말 | String | N | 12 | |
| etc_loana_fr | 기타대여금_초 | String | N | 12 | |
| etc_loana_to | 기타대여금_말 | String | N | 12 | |
| crd_int_npay_gold_fr | 신용이자미납금_초 | String | N | 12 | |
| crd_int_npay_gold_to | 신용이자미납금_말 | String | N | 12 | |
| crd_int_fr | 신용이자_초 | String | N | 12 | |
| crd_int_to | 신용이자_말 | String | N | 12 | |
| tot_amt_fr | 순자산액계_초 | String | N | 12 | |
| tot_amt_to | 순자산액계_말 | String | N | 12 | |
| invt_bsamt | 투자원금평잔 | String | N | 12 | |
| evltv_prft | 평가손익 | String | N | 12 | |
| prft_rt | 수익률 | String | N | 12 | |
| tern_rt | 회전율 | String | N | 12 | |
| termin_tot_trns | 기간내총입금 | String | N | 12 | |
| termin_tot_pymn | 기간내총출금 | String | N | 12 | |
| termin_tot_inq | 기간내총입고 | String | N | 12 | |
| termin_tot_outq | 기간내총출고 | String | N | 12 | |
| futr_repl_sella | 선물대용매도금액 | String | N | 12 | |
| trst_repl_sella | 위탁대용매도금액 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 일별계좌수익률상세현황요청
def fn_kt00016(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00016', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'fr_dt': '20241111', # 평가시작일 
        'to_dt': '20241125', # 평가종료일 
    }

    # 3. API 실행
    fn_kt00016(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00016(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "fr_dt" : "20241111",
    "to_dt" : "20241125"
}
```

#### Response
```json
{
    "mang_empno":"081",
    "mngr_nm":"키움은행",
    "dept_nm":"키움은행",
    "entr_fr":"000000000000",
    "entr_to":"000000017534",
    "scrt_evlt_amt_fr":"000000000000",
    "scrt_evlt_amt_to":"000000000000",
    "ls_grnt_fr":"000000000000",
    "ls_grnt_to":"000000000000",
    "crd_loan_fr":"000000000000",
    "crd_loan_to":"000000000000",
    "ch_uncla_fr":"000000000000",
    "ch_uncla_to":"000000000000",
    "krw_asgna_fr":"000000000000",
    "krw_asgna_to":"000000000000",
    "ls_evlta_fr":"000000000000",
    "ls_evlta_to":"000000000000",
    "rght_evlta_fr":"000000000000",
    "rght_evlta_to":"000000000000",
    "loan_amt_fr":"000000000000",
    "loan_amt_to":"000000000000",
    "etc_loana_fr":"000000000000",
    "etc_loana_to":"000000000000",
    "crd_int_npay_gold_fr":"000000000000",
    "crd_int_npay_gold_to":"000000000000",
    "crd_int_fr":"000000000000",
    "crd_int_to":"000000000000",
    "tot_amt_fr":"000000000000",
    "tot_amt_to":"000000017534",
    "invt_bsamt":"000000000000",
    "evltv_prft":"-00005482466",
    "prft_rt":"-0.91",
    "tern_rt":"0.84",
    "termin_tot_trns":"000000000000",
    "termin_tot_pymn":"000000000000",
    "termin_tot_inq":"000000000000",
    "termin_tot_outq":"000000000000",
    "futr_repl_sella":"000000000000",
    "trst_repl_sella":"000000000000",
    "return_code":0,
    "return_msg":"조회가 완료되었습니다."
}
```

---

## 계좌별당일현황요청 (kt00017)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| | (입력 파라미터 없음) | | | | |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| d2_entra | D+2추정예수금 | String | N | 12 | |
| crd_int_npay_gold | 신용이자미납금 | String | N | 12 | |
| etc_loana | 기타대여금 | String | N | 12 | |
| gnrl_stk_evlt_amt_d2 | 일반주식평가금액D+2 | String | N | 12 | |
| dpst_grnt_use_amt_d2 | 예탁담보대출금D+2 | String | N | 12 | |
| crd_stk_evlt_amt_d2 | 예탁담보주식평가금액D+2 | String | N | 12 | |
| crd_loan_d2 | 신용융자금D+2 | String | N | 12 | |
| crd_loan_evlta_d2 | 신용융자평가금D+2 | String | N | 12 | |
| crd_ls_grnt_d2 | 신용대주담보금D+2 | String | N | 12 | |
| crd_ls_evlta_d2 | 신용대주평가금D+2 | String | N | 12 | |
| ina_amt | 입금금액 | String | N | 12 | |
| outa | 출금금액 | String | N | 12 | |
| inq_amt | 입고금액 | String | N | 12 | |
| outq_amt | 출고금액 | String | N | 12 | |
| sell_amt | 매도금액 | String | N | 12 | |
| buy_amt | 매수금액 | String | N | 12 | |
| cmsn | 수수료 | String | N | 12 | |
| tax | 세금 | String | N | 12 | |
| stk_pur_cptal_loan_amt | 주식매입자금대출금 | String | N | 12 | |
| rp_evlt_amt | RP평가금액 | String | N | 12 | |
| bd_evlt_amt | 채권평가금액 | String | N | 12 | |
| elsevlt_amt | ELS평가금액 | String | N | 12 | |
| crd_int_amt | 신용이자금액 | String | N | 12 | |
| sel_prica_grnt_loan_int_amt_amt | 매도대금담보대출이자금액 | String | N | 12 | |
| dvida_amt | 배당금액 | String | N | 12 | |

### Python 예제 코드

```python
import requests
import json

# 계좌별당일현황요청
def fn_kt00017(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00017', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {}

    # 3. API 실행
    fn_kt00017(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00017(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{}
```

#### Response
```json
{
    "d2_entra":"000000012550",
    "crd_int_npay_gold":"000000000000",
    "etc_loana":"000000000000",
    "gnrl_stk_evlt_amt_d2":"000005724100",
    "dpst_grnt_use_amt_d2":"000000000000",
    "crd_stk_evlt_amt_d2":"000000000000",
    "crd_loan_d2":"000000000000",
    "crd_loan_evlta_d2":"000000000000",
    "crd_ls_grnt_d2":"000000000000",
    "crd_ls_evlta_d2":"000000000000",
    "ina_amt":"000000000000",
    "outa":"000000000000",
    "inq_amt":"000000000000",
    "outq_amt":"000000000000",
    "sell_amt":"000000000000",
    "buy_amt":"000000000000",
    "cmsn":"000000000000",
    "tax":"000000000000",
    "stk_pur_cptal_loan_amt":"000000000000",
    "rp_evlt_amt":"000000000000",
    "bd_evlt_amt":"000000000000",
    "elsevlt_amt":"000000000000",
    "crd_int_amt":"000000000000",
    "sel_prica_grnt_loan_int_amt_amt":"000000000000",
    "dvida_amt":"000000000000",
    "return_code":0,
    "return_msg":"조회가 완료되었습니다.."
}
```

---

## 계좌평가잔고내역요청 (kt00018)

### 기본 정보

**Method:** POST  
**운영 도메인:** https://api.kiwoom.com  
**모의투자 도메인:** https://mockapi.kiwoom.com (KRX만 지원가능)  
**URL:** /api/dostk/acnt  
**Format:** JSON  
**Content-Type:** application/json;charset=UTF-8

### 요청 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출 예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| qry_tp | 조회구분 | String | Y | 1 | 1:합산, 2:개별 |
| dmst_stex_tp | 국내거래소구분 | String | Y | 6 | KRX:한국거래소, NXT:넥스트트레이드 |

### 응답 사양

#### Header

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

#### Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|---------|-------------|
| tot_pur_amt | 총매입금액 | String | N | 15 | |
| tot_evlt_amt | 총평가금액 | String | N | 15 | |
| tot_evlt_pl | 총평가손익금액 | String | N | 15 | |
| tot_prft_rt | 총수익률(%) | String | N | 12 | |
| prsm_dpst_aset_amt | 추정예탁자산 | String | N | 15 | |
| tot_loan_amt | 총대출금 | String | N | 15 | |
| tot_crd_loan_amt | 총융자금액 | String | N | 15 | |
| tot_crd_ls_amt | 총대주금액 | String | N | 15 | |
| acnt_evlt_remn_indv_tot | 계좌평가잔고개별합산 | LIST | N | - | |
| - stk_cd | 종목번호 | String | N | 12 | |
| - stk_nm | 종목명 | String | N | 40 | |
| - evltv_prft | 평가손익 | String | N | 15 | |
| - prft_rt | 수익률(%) | String | N | 12 | |
| - pur_pric | 매입가 | String | N | 15 | |
| - pred_close_pric | 전일종가 | String | N | 12 | |
| - rmnd_qty | 보유수량 | String | N | 15 | |
| - trde_able_qty | 매매가능수량 | String | N | 15 | |
| - cur_prc | 현재가 | String | N | 12 | |
| - pred_buyq | 전일매수수량 | String | N | 15 | |
| - pred_sellq | 전일매도수량 | String | N | 15 | |
| - tdy_buyq | 금일매수수량 | String | N | 15 | |
| - tdy_sellq | 금일매도수량 | String | N | 15 | |
| - pur_amt | 매입금액 | String | N | 15 | |
| - pur_cmsn | 매입수수료 | String | N | 15 | |
| - evlt_amt | 평가금액 | String | N | 15 | |
| - sell_cmsn | 평가수수료 | String | N | 15 | |
| - tax | 세금 | String | N | 15 | |
| - sum_cmsn | 수수료합 | String | N | 15 | 매입수수료 + 평가수수료 |
| - poss_rt | 보유비중(%) | String | N | 12 | |
| - crd_tp | 신용구분 | String | N | 2 | |
| - crd_tp_nm | 신용구분명 | String | N | 4 | |
| - crd_loan_dt | 대출일 | String | N | 8 | |

### Python 예제 코드

```python
import requests
import json

# 계좌평가잔고내역요청
def fn_kt00018(token, data, cont_yn='N', next_key=''):
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/acnt'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'kt00018', # TR명
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)

    # 4. 응답 상태 코드와 데이터 출력
    print('Code:', response.status_code)
    print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
    print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

    # 2. 요청 데이터
    params = {
        'qry_tp': '1', # 조회구분 1:합산, 2:개별
        'dmst_stex_tp': 'KRX', # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
    }

    # 3. API 실행
    fn_kt00018(token=MY_ACCESS_TOKEN, data=params)

    # next-key, cont-yn 값이 있을 경우
    # fn_kt00018(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### 요청/응답 예제

#### Request
```json
{
    "qry_tp" : "1",
    "dmst_stex_tp" : "KRX"
}
```

#### Response
```json
{
    "tot_pur_amt": "000005500000000",
    "tot_evlt_amt": "000005724100000",
    "tot_evlt_pl": "000000224100000",
    "tot_prft_rt": "4.08",
    "prsm_dpst_aset_amt": "000005736650000",
    "tot_loan_amt": "000000000000000",
    "tot_crd_loan_amt": "000000000000000",
    "tot_crd_ls_amt": "000000000000000",
    "acnt_evlt_remn_indv_tot": [
        {
            "stk_cd": "A005930",
            "stk_nm": "삼성전자",
            "evltv_prft": "000000113556000",
            "prft_rt": "1.85",
            "pur_pric": "000000124500",
            "pred_close_pric": "000000070000",
            "rmnd_qty": "000000000047",
            "trde_able_qty": "000000000047",
            "cur_prc": "000000070000",
            "pred_buyq": "000000000000",
            "pred_sellq": "000000000000",
            "tdy_buyq": "000000000000",
            "tdy_sellq": "000000000000",
            "pur_amt": "000006122786000",
            "pur_cmsn": "000000002500000",
            "evlt_amt": "000006236342000",
            "sell_cmsn": "000000003119000",
            "tax": "000000005602000",
            "sum_cmsn": "000000005619000",
            "poss_rt": "100.00",
            "crd_tp": "00",
            "crd_tp_nm": "보통",
            "crd_loan_dt": ""
        }
    ],
    "return_code": 0,
    "return_msg": "조회가 완료되었습니다."
}
```

---# 키움증권 API 문서

## 국내주식 REST API

### 공매도

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 공매도추이요청 | ka10014 | 공매도 추이 정보 조회 |

---

### 공매도추이요청 (ka10014)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/shsa
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명       | Type   | Required | Length | Description                                                                |
| -------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------------------- |
| stk_cd   | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)           |
| tm_tp    | 시간구분     | String | N        | 1      | 0:시작일, 1:기간                                                          |
| strt_dt  | 시작일자     | String | Y        | 8      | YYYYMMDD                                                                   |
| end_dt   | 종료일자     | String | Y        | 8      | YYYYMMDD                                                                   |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명           | Type   | Required | Length | Description                      |
| -------------------- | ---------------- | ------ | -------- | ------ | -------------------------------- |
| shrts_trnsn          | 공매도추이       | LIST   | N        |        |                                  |
| - dt                 | 일자             | String | N        | 20     |                                  |
| - close_pric         | 종가             | String | N        | 20     |                                  |
| - pred_pre_sig       | 전일대비기호     | String | N        | 20     |                                  |
| - pred_pre           | 전일대비         | String | N        | 20     |                                  |
| - flu_rt             | 등락율           | String | N        | 20     |                                  |
| - trde_qty           | 거래량           | String | N        | 20     |                                  |
| - shrts_qty          | 공매도량         | String | N        | 20     |                                  |
| - ovr_shrts_qty      | 누적공매도량     | String | N        | 20     | 설정 기간의 공매도량 합산데이터  |
| - trde_wght          | 매매비중         | String | N        | 20     |                                  |
| - shrts_trde_prica   | 공매도거래대금   | String | N        | 20     |                                  |
| - shrts_avg_pric     | 공매도평균가     | String | N        | 20     |                                  |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"tm_tp": "1",
	"strt_dt": "20250501",
	"end_dt": "20250519"
}
```

#### 응답 예시

```json
{
	"shrts_trnsn": [
		{
			"dt": "20250519",
			"close_pric": "-55800",
			"pred_pre_sig": "5",
			"pred_pre": "-1000",
			"flu_rt": "-1.76",
			"trde_qty": "9802105",
			"shrts_qty": "841407",
			"ovr_shrts_qty": "6424755",
			"trde_wght": "+8.58",
			"shrts_trde_prica": "46985302",
			"shrts_avg_pric": "55841"
		},
		{
			"dt": "20250516",
			"close_pric": "-56800",
			"pred_pre_sig": "5",
			"pred_pre": "-500",
			"flu_rt": "-0.87",
			"trde_qty": "10385352",
			"shrts_qty": "487354",
			"ovr_shrts_qty": "5583348",
			"trde_wght": "+4.69",
			"shrts_trde_prica": "27725268",
			"shrts_avg_pric": "56889"
		},
		{
			"dt": "20250515",
			"close_pric": "-57300",
			"pred_pre_sig": "5",
			"pred_pre": "-100",
			"flu_rt": "-0.17",
			"trde_qty": "13139736",
			"shrts_qty": "404120",
			"ovr_shrts_qty": "5095994",
			"trde_wght": "+3.08",
			"shrts_trde_prica": "23278677",
			"shrts_avg_pric": "57603"
		},
		{
			"dt": "20250514",
			"close_pric": "+57400",
			"pred_pre_sig": "2",
			"pred_pre": "+500",
			"flu_rt": "+0.88",
			"trde_qty": "12468089",
			"shrts_qty": "607315",
			"ovr_shrts_qty": "4691874",
			"trde_wght": "+4.87",
			"shrts_trde_prica": "34862170",
			"shrts_avg_pric": "57404"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 기관/외국인

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 주식외국인종목별매매동향 | ka10008 | 주식 외국인 종목별 매매 동향 조회 |
| 주식기관요청 | ka10009 | 주식 기관 정보 조회 |
| 기관외국인연속매매현황요청 | ka10131 | 기관/외국인 연속매매현황 조회 |

---

### 주식외국인종목별매매동향 (ka10008)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/frgnistt
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명           | Type   | Required | Length | Description |
| --------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| stk_frgnr             | 주식외국인       | LIST   | N        |        |             |
| - dt                  | 일자             | String | N        | 20     |             |
| - close_pric          | 종가             | String | N        | 20     |             |
| - pred_pre            | 전일대비         | String | N        | 20     |             |
| - trde_qty            | 거래량           | String | N        | 20     |             |
| - chg_qty             | 변동수량         | String | N        | 20     |             |
| - poss_stkcnt         | 보유주식수       | String | N        | 20     |             |
| - wght                | 비중             | String | N        | 20     |             |
| - gain_pos_stkcnt     | 취득가능주식수   | String | N        | 20     |             |
| - frgnr_limit         | 외국인한도       | String | N        | 20     |             |
| - frgnr_limit_irds    | 외국인한도증감   | String | N        | 20     |             |
| - limit_exh_rt        | 한도소진률       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"stk_frgnr": [
		{
			"dt": "20241105",
			"close_pric": "135300",
			"pred_pre": "0",
			"trde_qty": "0",
			"chg_qty": "0",
			"poss_stkcnt": "6663509",
			"wght": "+26.10",
			"gain_pos_stkcnt": "18863197",
			"frgnr_limit": "25526706",
			"frgnr_limit_irds": "0",
			"limit_exh_rt": "+26.10"
		},
		{
			"dt": "20241101",
			"close_pric": "65100",
			"pred_pre": "0",
			"trde_qty": "0",
			"chg_qty": "-3441",
			"poss_stkcnt": "6642402",
			"wght": "+26.02",
			"gain_pos_stkcnt": "18884304",
			"frgnr_limit": "25526706",
			"frgnr_limit_irds": "0",
			"limit_exh_rt": "+26.02"
		},
		{
			"dt": "20241031",
			"close_pric": "65100",
			"pred_pre": "0",
			"trde_qty": "0",
			"chg_qty": "4627",
			"poss_stkcnt": "6645843",
			"wght": "+26.03",
			"gain_pos_stkcnt": "18880863",
			"frgnr_limit": "25526706",
			"frgnr_limit_irds": "0",
			"limit_exh_rt": "+26.03"
		},
		{
			"dt": "20241030",
			"close_pric": "+65100",
			"pred_pre": "+100",
			"trde_qty": "1",
			"chg_qty": "-10245",
			"poss_stkcnt": "6641216",
			"wght": "+26.02",
			"gain_pos_stkcnt": "18885490",
			"frgnr_limit": "25526706",
			"frgnr_limit_irds": "0",
			"limit_exh_rt": "+26.02"
		},
		{
			"dt": "20241029",
			"close_pric": "-65000",
			"pred_pre": "-27300",
			"trde_qty": "4",
			"chg_qty": "249",
			"poss_stkcnt": "6651461",
			"wght": "+26.06",
			"gain_pos_stkcnt": "18875245",
			"frgnr_limit": "25526706",
			"frgnr_limit_irds": "0",
			"limit_exh_rt": "+26.06"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식기관요청 (ka10009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/frgnistt
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| date                   | 날짜                 | String | N        | 20     |             |
| close_pric             | 종가                 | String | N        | 20     |             |
| pre                    | 대비                 | String | N        | 20     |             |
| orgn_dt_acc            | 기관기간누적         | String | N        | 20     |             |
| orgn_daly_nettrde      | 기관일별순매매       | String | N        | 20     |             |
| frgnr_daly_nettrde     | 외국인일별순매매     | String | N        | 20     |             |
| frgnr_qota_rt          | 외국인지분율         | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"date": "20241105",
	"close_pric": "135300",
	"pre": "0",
	"orgn_dt_acc": "",
	"orgn_daly_nettrde": "",
	"frgnr_daly_nettrde": "",
	"frgnr_qota_rt": "",
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 기관외국인연속매매현황요청 (ka10131)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/frgnistt
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                                                                                          |
| ------------ | -------------- | ------ | -------- | ------ | ---------------------------------------------------------------------------------------------------- |
| dt           | 기간           | String | Y        | 3      | 1:최근일, 3:3일, 5:5일, 10:10일, 20:20일, 120:120일, 0:시작일자/종료일자로 조회                     |
| strt_dt      | 시작일자       | String | N        | 8      | YYYYMMDD                                                                                             |
| end_dt       | 종료일자       | String | N        | 8      | YYYYMMDD                                                                                             |
| mrkt_tp      | 장구분         | String | Y        | 3      | 001:코스피, 101:코스닥                                                                               |
| netslmt_tp   | 순매도수구분   | String | Y        | 1      | 2:순매수(고정값)                                                                                     |
| stk_inds_tp  | 종목업종구분   | String | Y        | 1      | 0:종목(주식),1:업종                                                                                  |
| amt_qty_tp   | 금액수량구분   | String | Y        | 1      | 0:금액, 1:수량                                                                                       |
| stex_tp      | 거래소구분     | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                          | 한글명                   | Type   | Required | Length | Description |
| -------------------------------- | ------------------------ | ------ | -------- | ------ | ----------- |
| orgn_frgnr_cont_trde_prst        | 기관외국인연속매매현황   | LIST   | N        |        |             |
| - rank                           | 순위                     | String | N        |        |             |
| - stk_cd                         | 종목코드                 | String | N        | 6      |             |
| - stk_nm                         | 종목명                   | String | N        | 20     |             |
| - prid_stkpc_flu_rt              | 기간중주가등락률         | String | N        |        |             |
| - orgn_nettrde_amt               | 기관순매매금액           | String | N        |        |             |
| - orgn_nettrde_qty               | 기관순매매량             | String | N        |        |             |
| - orgn_cont_netprps_dys          | 기관계연속순매수일수     | String | N        |        |             |
| - orgn_cont_netprps_qty          | 기관계연속순매수량       | String | N        |        |             |
| - orgn_cont_netprps_amt          | 기관계연속순매수금액     | String | N        |        |             |
| - frgnr_nettrde_qty              | 외국인순매매량           | String | N        |        |             |
| - frgnr_nettrde_amt              | 외국인순매매액           | String | N        |        |             |
| - frgnr_cont_netprps_dys         | 외국인연속순매수일수     | String | N        |        |             |
| - frgnr_cont_netprps_qty         | 외국인연속순매수량       | String | N        |        |             |
| - frgnr_cont_netprps_amt         | 외국인연속순매수금액     | String | N        |        |             |
| - nettrde_qty                    | 순매매량                 | String | N        |        |             |
| - nettrde_amt                    | 순매매액                 | String | N        |        |             |
| - tot_cont_netprps_dys           | 합계연속순매수일수       | String | N        |        |             |
| - tot_cont_nettrde_qty           | 합계연속순매매수량       | String | N        |        |             |
| - tot_cont_netprps_amt           | 합계연속순매수금액       | String | N        |        |             |

#### 요청 예시

```json
{
	"dt": "1",
	"strt_dt": "",
	"end_dt": "",
	"mrkt_tp": "001",
	"netslmt_tp": "2",
	"stk_inds_tp": "0",
	"amt_qty_tp": "0",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"orgn_frgnr_cont_trde_prst": [
		{
			"rank": "1",
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"prid_stkpc_flu_rt": "-5.80",
			"orgn_nettrde_amt": "+48",
			"orgn_nettrde_qty": "+173",
			"orgn_cont_netprps_dys": "+1",
			"orgn_cont_netprps_qty": "+173",
			"orgn_cont_netprps_amt": "+48",
			"frgnr_nettrde_qty": "+0",
			"frgnr_nettrde_amt": "+0",
			"frgnr_cont_netprps_dys": "+1",
			"frgnr_cont_netprps_qty": "+1",
			"frgnr_cont_netprps_amt": "+0",
			"nettrde_qty": "+173",
			"nettrde_amt": "+48",
			"tot_cont_netprps_dys": "+2",
			"tot_cont_nettrde_qty": "+174",
			"tot_cont_netprps_amt": "+48"
		},
		{
			"rank": "2",
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"prid_stkpc_flu_rt": "-4.21",
			"orgn_nettrde_amt": "+41",
			"orgn_nettrde_qty": "+159",
			"orgn_cont_netprps_dys": "+1",
			"orgn_cont_netprps_qty": "+159",
			"orgn_cont_netprps_amt": "+41",
			"frgnr_nettrde_qty": "+0",
			"frgnr_nettrde_amt": "+0",
			"frgnr_cont_netprps_dys": "+1",
			"frgnr_cont_netprps_qty": "+1",
			"frgnr_cont_netprps_amt": "+0",
			"nettrde_qty": "+159",
			"nettrde_amt": "+41",
			"tot_cont_netprps_dys": "+2",
			"tot_cont_nettrde_qty": "+160",
			"tot_cont_netprps_amt": "+42"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 대차거래

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 대차거래추이요청 | ka10068 | 대차거래 추이 정보 조회 |
| 대차거래상위10종목요청 | ka10069 | 대차거래 상위 10종목 조회 |
| 대차거래추이요청(종목별) | ka20068 | 대차거래 추이 정보 조회 (종목별) |
| 대차거래내역요청 | ka90012 | 대차거래 내역 조회 |

---

### 대차거래추이요청 (ka10068)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/slb
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description      |
| ------- | -------- | ------ | -------- | ------ | ---------------- |
| strt_dt | 시작일자 | String | N        | 8      | YYYYMMDD         |
| end_dt  | 종료일자 | String | N        | 8      | YYYYMMDD         |
| all_tp  | 전체구분 | String | Y        | 6      | 1: 전체표시      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description |
| ------------------------ | ---------------- | ------ | -------- | ------ | ----------- |
| dbrt_trde_trnsn          | 대차거래추이     | LIST   | N        |        |             |
| - dt                     | 일자             | String | N        | 8      |             |
| - dbrt_trde_cntrcnt      | 대차거래체결주수 | String | N        | 12     |             |
| - dbrt_trde_rpy          | 대차거래상환주수 | String | N        | 18     |             |
| - dbrt_trde_irds         | 대차거래증감     | String | N        | 60     |             |
| - rmnd                   | 잔고주수         | String | N        | 18     |             |
| - remn_amt               | 잔고금액         | String | N        | 18     |             |

#### 요청 예시

```json
{
	"strt_dt": "20250401",
	"end_dt": "20250430",
	"all_tp": "1"
}
```

#### 응답 예시

```json
{
	"dbrt_trde_trnsn": [
		{
			"dt": "20250430",
			"dbrt_trde_cntrcnt": "35330036",
			"dbrt_trde_rpy": "25217364",
			"dbrt_trde_irds": "10112672",
			"rmnd": "2460259444",
			"remn_amt": "73956254"
		},
		{
			"dt": "20250429",
			"dbrt_trde_cntrcnt": "23721553",
			"dbrt_trde_rpy": "13986586",
			"dbrt_trde_irds": "9734967",
			"rmnd": "2125919149",
			"remn_amt": "66422682"
		},
		{
			"dt": "20250428",
			"dbrt_trde_cntrcnt": "17165250",
			"dbrt_trde_rpy": "30883228",
			"dbrt_trde_irds": "-13717978",
			"rmnd": "2276180199",
			"remn_amt": "68480718"
		},
		{
			"dt": "20250425",
			"dbrt_trde_cntrcnt": "62932490",
			"dbrt_trde_rpy": "85148199",
			"dbrt_trde_irds": "-22215709",
			"rmnd": "2355269107",
			"remn_amt": "69882489"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 대차거래상위10종목요청 (ka10069)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/slb
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                 |
| ------- | -------- | ------ | -------- | ------ | ----------------------------------------------------------- |
| strt_dt | 시작일자 | String | Y        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)          |
| end_dt  | 종료일자 | String | N        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)          |
| mrkt_tp | 시장구분 | String | Y        | 3      | 001:코스피, 101:코스닥                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명               | Type   | Required | Length | Description |
| ------------------------ | -------------------- | ------ | -------- | ------ | ----------- |
| dbrt_trde_cntrcnt_sum    | 대차거래체결주수합   | String | N        |        |             |
| dbrt_trde_rpy_sum        | 대차거래상환주수합   | String | N        |        |             |
| rmnd_sum                 | 잔고주수합           | String | N        |        |             |
| remn_amt_sum             | 잔고금액합           | String | N        |        |             |
| dbrt_trde_cntrcnt_rt     | 대차거래체결주수비율 | String | N        |        |             |
| dbrt_trde_rpy_rt         | 대차거래상환주수비율 | String | N        |        |             |
| rmnd_rt                  | 잔고주수비율         | String | N        |        |             |
| remn_amt_rt              | 잔고금액비율         | String | N        |        |             |
| dbrt_trde_upper_10stk    | 대차거래상위10종목   | LIST   | N        |        |             |
| - stk_nm                 | 종목명               | String | N        | 20     |             |
| - stk_cd                 | 종목코드             | String | N        | 20     |             |
| - dbrt_trde_cntrcnt      | 대차거래체결주수     | String | N        | 20     |             |
| - dbrt_trde_rpy          | 대차거래상환주수     | String | N        | 20     |             |
| - rmnd                   | 잔고주수             | String | N        | 20     |             |
| - remn_amt               | 잔고금액             | String | N        | 20     |             |

#### 요청 예시

```json
{
	"strt_dt": "20241110",
	"end_dt": "20241125",
	"mrkt_tp": "001"
}
```

#### 응답 예시

```json
{
	"dbrt_trde_cntrcnt_sum": "3383301",
	"dbrt_trde_rpy_sum": "764254",
	"rmnd_sum": "173782689",
	"remn_amt_sum": "14218184",
	"dbrt_trde_cntrcnt_rt": "7061",
	"dbrt_trde_rpy_rt": "3196",
	"rmnd_rt": "2225",
	"remn_amt_rt": "3728",
	"dbrt_trde_upper_10stk": [
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "1209600",
			"dbrt_trde_rpy": "0",
			"rmnd": "1505173",
			"remn_amt": "1203"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "681807",
			"dbrt_trde_rpy": "304467",
			"rmnd": "122704705",
			"remn_amt": "9546426"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "297431",
			"dbrt_trde_rpy": "208222",
			"rmnd": "13731939",
			"remn_amt": "1691775"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "230866",
			"dbrt_trde_rpy": "301",
			"rmnd": "3012573",
			"remn_amt": "104838"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 대차거래추이요청(종목별) (ka20068)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/slb
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                           |
| ------- | -------- | ------ | -------- | ------ | ------------------------------------- |
| strt_dt | 시작일자 | String | N        | 8      | YYYYMMDD                              |
| end_dt  | 종료일자 | String | N        | 8      | YYYYMMDD                              |
| all_tp  | 전체구분 | String | N        | 1      | 0:종목코드 입력종목만 표시            |
| stk_cd  | 종목코드 | String | Y        | 6      |                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description |
| ------------------------ | ---------------- | ------ | -------- | ------ | ----------- |
| dbrt_trde_trnsn          | 대차거래추이     | LIST   | N        |        |             |
| - dt                     | 일자             | String | N        | 20     |             |
| - dbrt_trde_cntrcnt      | 대차거래체결주수 | String | N        | 20     |             |
| - dbrt_trde_rpy          | 대차거래상환주수 | String | N        | 20     |             |
| - dbrt_trde_irds         | 대차거래증감     | String | N        | 20     |             |
| - rmnd                   | 잔고주수         | String | N        | 20     |             |
| - remn_amt               | 잔고금액         | String | N        | 20     |             |

#### 요청 예시

```json
{
	"strt_dt": "20250401",
	"end_dt": "20250430",
	"all_tp": "0",
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"dbrt_trde_trnsn": [
		{
			"dt": "20250430",
			"dbrt_trde_cntrcnt": "1210354",
			"dbrt_trde_rpy": "2693108",
			"dbrt_trde_irds": "-1482754",
			"rmnd": "98242435",
			"remn_amt": "5452455"
		},
		{
			"dt": "20250429",
			"dbrt_trde_cntrcnt": "502018",
			"dbrt_trde_rpy": "1022714",
			"dbrt_trde_irds": "-520696",
			"rmnd": "99725189",
			"remn_amt": "5564666"
		},
		{
			"dt": "20250428",
			"dbrt_trde_cntrcnt": "958772",
			"dbrt_trde_rpy": "3122807",
			"dbrt_trde_irds": "-2164035",
			"rmnd": "100245885",
			"remn_amt": "5593720"
		},
		{
			"dt": "20250425",
			"dbrt_trde_cntrcnt": "1504273",
			"dbrt_trde_rpy": "5217540",
			"dbrt_trde_irds": "-3713267",
			"rmnd": "102409920",
			"remn_amt": "5704233"
		},
		{
			"dt": "20250424",
			"dbrt_trde_cntrcnt": "1803312",
			"dbrt_trde_rpy": "6076301",
			"dbrt_trde_irds": "-4272989",
			"rmnd": "106123187",
			"remn_amt": "5911062"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 대차거래내역요청 (ka90012)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/slb
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                 |
| ------- | -------- | ------ | -------- | ------ | --------------------------- |
| dt      | 일자     | String | Y        | 8      | YYYYMMDD                    |
| mrkt_tp | 시장구분 | String | Y        | 3      | 001:코스피, 101:코스닥      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description |
| ------------------------ | ---------------- | ------ | -------- | ------ | ----------- |
| dbrt_trde_prps           | 대차거래내역     | LIST   | N        |        |             |
| - stk_nm                 | 종목명           | String | N        | 20     |             |
| - stk_cd                 | 종목코드         | String | N        | 20     |             |
| - dbrt_trde_cntrcnt      | 대차거래체결주수 | String | N        | 20     |             |
| - dbrt_trde_rpy          | 대차거래상환주수 | String | N        | 20     |             |
| - rmnd                   | 잔고주수         | String | N        | 20     |             |
| - remn_amt               | 잔고금액         | String | N        | 20     |             |

#### 요청 예시

```json
{
	"dt": "20241101",
	"mrkt_tp": "101"
}
```

#### 응답 예시

```json
{
	"dbrt_trde_prps": [
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "20262",
			"dbrt_trde_rpy": "3493",
			"rmnd": "12812813",
			"remn_amt": "1026306"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "336116",
			"dbrt_trde_rpy": "145001",
			"rmnd": "9689378",
			"remn_amt": "1644287"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "55055",
			"dbrt_trde_rpy": "68866",
			"rmnd": "9341419",
			"remn_amt": "595983"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "6704",
			"dbrt_trde_rpy": "16000",
			"rmnd": "7167500",
			"remn_amt": "25803"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "0",
			"dbrt_trde_rpy": "6500",
			"rmnd": "6730107",
			"remn_amt": "13595"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "13550",
			"dbrt_trde_rpy": "1198",
			"rmnd": "5584633",
			"remn_amt": "27784"
		},
		{
			"stk_nm": "삼성전자",
			"stk_cd": "005930",
			"dbrt_trde_cntrcnt": "5000",
			"dbrt_trde_rpy": "0",
			"rmnd": "5568717",
			"remn_amt": "6755"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 순위정보

#### TR 목록

| TR명                           | 코드    | 설명                           |
| ------------------------------ | ------- | ------------------------------ |
| 호가잔량상위요청               | ka10020 | 호가잔량상위요청               |
| 호가잔량급증요청               | ka10021 | 호가잔량급증요청               |
| 잔량율급증요청                 | ka10022 | 잔량율급증요청                 |
| 거래량급증요청                 | ka10023 | 거래량급증요청                 |
| 전일대비등락률상위요청         | ka10027 | 전일대비등락률상위요청         |
| 예상체결등락률상위요청         | ka10029 | 예상체결등락률상위요청         |
| 당일거래량상위요청             | ka10030 | 당일거래량상위요청             |
| 전일거래량상위요청             | ka10031 | 전일거래량상위요청             |
| 거래대금상위요청               | ka10032 | 거래대금상위요청               |
| 신용비율상위요청               | ka10033 | 신용비율상위요청               |
| 외인기간별매매상위요청         | ka10034 | 외인기간별매매상위요청         |
| 외인연속순매매상위요청         | ka10035 | 외인연속순매매상위요청         |
| 외인한도소진율증가상위         | ka10036 | 외인한도소진율증가상위         |
| 외국계창구매매상위요청         | ka10037 | 외국계창구매매상위요청         |
| 종목별증권사순위요청           | ka10038 | 종목별증권사순위요청           |
| 증권사별매매상위요청           | ka10039 | 증권사별매매상위요청           |
| 당일주요거래원요청             | ka10040 | 당일주요거래원요청             |
| 순매수거래원순위요청           | ka10042 | 순매수거래원순위요청           |
| 당일상위이탈원요청             | ka10053 | 당일상위이탈원요청             |
| 동일순매매순위요청             | ka10062 | 동일순매매순위요청             |
| 장중투자자별매매상위요청       | ka10065 | 장중투자자별매매상위요청       |
| 시간외단일가등락율순위요청     | ka10098 | 시간외단일가등락율순위요청     |
| 외국인기관매매상위요청         | ka90009 | 외국인기관매매상위요청         |

---

### 호가잔량상위요청 (ka10020)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명       | Type   | Required | Length | Description                                                                                                                                      |
| ----------- | ------------ | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| mrkt_tp     | 시장구분     | String | Y        | 3      | 001:코스피, 101:코스닥                                                                                                                           |
| sort_tp     | 정렬구분     | String | Y        | 1      | 1:순매수잔량순, 2:순매도잔량순, 3:매수비율순, 4:매도비율순                                                                                       |
| trde_qty_tp | 거래량구분   | String | Y        | 4      | 0000:장시작전(0주이상), 0010:만주이상, 0050:5만주이상, 00100:10만주이상                                                                          |
| stk_cnd     | 종목조건     | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기                                                  |
| crd_cnd     | 신용조건     | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                           |
| stex_tp     | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| bid_req_upper  | 호가잔량상위 | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - trde_qty     | 거래량       | String | N        | 20     |             |
| - tot_sel_req  | 총매도잔량   | String | N        | 20     |             |
| - tot_buy_req  | 총매수잔량   | String | N        | 20     |             |
| - netprps_req  | 순매수잔량   | String | N        | 20     |             |
| - buy_rt       | 매수비율     | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "001",
	"sort_tp" : "1",
	"trde_qty_tp" : "0000",
	"stk_cnd" : "0",
	"crd_cnd" : "0",
	"stex_tp" : "1"
}
```

#### 응답 예시

```json
{
	"bid_req_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+65000",
				"pred_pre_sig":"2",
				"pred_pre":"+6300",
				"trde_qty":"214670",
				"tot_sel_req":"1",
				"tot_buy_req":"22287",
				"netprps_req":"22286",
				"buy_rt":"2228700.00"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+13335",
				"pred_pre_sig":"2",
				"pred_pre":"+385",
				"trde_qty":"0",
				"tot_sel_req":"0",
				"tot_buy_req":"9946",
				"netprps_req":"9946",
				"buy_rt":"0.00"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+10435",
				"pred_pre_sig":"2",
				"pred_pre":"+360",
				"trde_qty":"0",
				"tot_sel_req":"0",
				"tot_buy_req":"8013",
				"netprps_req":"8013",
				"buy_rt":"0.00"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+9530",
				"pred_pre_sig":"2",
				"pred_pre":"+275",
				"trde_qty":"0",
				"tot_sel_req":"0",
				"tot_buy_req":"5432",
				"netprps_req":"5432",
				"buy_rt":"0.00"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+13120",
				"pred_pre_sig":"2",
				"pred_pre":"+55",
				"trde_qty":"0",
				"tot_sel_req":"0",
				"tot_buy_req":"5335",
				"netprps_req":"5335",
				"buy_rt":"0.00"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 호가잔량급증요청 (ka10021)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명       | Type   | Required | Length | Description                                                                                                                 |
| ----------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp     | 시장구분     | String | Y        | 3      | 001:코스피, 101:코스닥                                                                                                      |
| trde_tp     | 매매구분     | String | Y        | 1      | 1:매수잔량, 2:매도잔량                                                                                                      |
| sort_tp     | 정렬구분     | String | Y        | 1      | 1:급증량, 2:급증률                                                                                                          |
| tm_tp       | 시간구분     | String | Y        | 2      | 분 입력                                                                                                                     |
| trde_qty_tp | 거래량구분   | String | Y        | 4      | 1:천주이상, 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상                                                          |
| stk_cnd     | 종목조건     | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기                             |
| stex_tp     | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| bid_req_sdnin  | 호가잔량급증 | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - int          | 기준률       | String | N        | 20     |             |
| - now          | 현재         | String | N        | 20     |             |
| - sdnin_qty    | 급증수량     | String | N        | 20     |             |
| - sdnin_rt     | 급증률       | String | N        | 20     |             |
| - tot_buy_qty  | 총매수량     | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "001",
	"trde_tp" : "1",
	"sort_tp" : "1",
	"tm_tp" : "30",
	"trde_qty_tp" : "1",
	"stk_cnd" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"bid_req_sdnin":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"8680",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"int":"5000",
				"now":"10000",
				"sdnin_qty":"5000",
				"sdnin_rt":"+100.00",
				"tot_buy_qty":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 잔량율급증요청 (ka10022)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명       | Type   | Required | Length | Description                                                                                                                 |
| ----------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp     | 시장구분     | String | Y        | 3      | 001:코스피, 101:코스닥                                                                                                      |
| rt_tp       | 비율구분     | String | Y        | 1      | 1:매수/매도비율, 2:매도/매수비율                                                                                            |
| tm_tp       | 시간구분     | String | Y        | 2      | 분 입력                                                                                                                     |
| trde_qty_tp | 거래량구분   | String | Y        | 1      | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상                                                                      |
| stk_cnd     | 종목조건     | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기                             |
| stex_tp     | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| req_rt_sdnin   | 잔량율급증   | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - int          | 기준률       | String | N        | 20     |             |
| - now_rt       | 현재비율     | String | N        | 20     |             |
| - sdnin_rt     | 급증률       | String | N        | 20     |             |
| - tot_sel_req  | 총매도잔량   | String | N        | 20     |             |
| - tot_buy_req  | 총매수잔량   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "001",
	"rt_tp" : "1",
	"tm_tp" : "1",
	"trde_qty_tp" : "5",
	"stk_cnd" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"req_rt_sdnin":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+74300",
				"pred_pre_sig":"2",
				"pred_pre":"+17000",
				"int":"+12600.00",
				"now_rt":"-21474836.00",
				"sdnin_rt":"-21474836.00",
				"tot_sel_req":"74",
				"tot_buy_req":"74337920"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 거래량급증요청 (ka10023)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명       | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------- | ------------ | ------ | -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp     | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                                                                                                                                                                                                                                                 |
| sort_tp     | 정렬구분     | String | Y        | 1      | 1:급증량, 2:급증률, 3:급감량, 4:급감률                                                                                                                                                                                                                                                                                                                                                                           |
| tm_tp       | 시간구분     | String | Y        | 1      | 1:분, 2:전일                                                                                                                                                                                                                                                                                                                                                                                                     |
| trde_qty_tp | 거래량구분   | String | Y        | 1      | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상                                                                                                                                                                                                                                                                                        |
| tm          | 시간         | String | N        | 2      | 분 입력                                                                                                                                                                                                                                                                                                                                                                                                          |
| stk_cnd     | 종목조건     | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 11:정리매매종목제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 17:ETN제외, 14:ETF제외, 18:ETF+ETN제외, 15:스팩제외, 20:ETF+ETN+스팩제외                                                                                                                                                   |
| pric_tp     | 가격구분     | String | Y        | 1      | 0:전체조회, 2:5만원이상, 5:1만원이상, 6:5천원이상, 8:1천원이상, 9:10만원이상                                                                                                                                                                                                                                                                                                                                    |
| stex_tp     | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                                                                                                                                                                                                                                                                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element         | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| trde_qty_sdnin         | 거래량급증       | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호     | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - flu_rt               | 등락률           | String | N        | 20     |             |
| - prev_trde_qty        | 이전거래량       | String | N        | 20     |             |
| - now_trde_qty         | 현재거래량       | String | N        | 20     |             |
| - sdnin_qty            | 급증량           | String | N        | 20     |             |
| - sdnin_rt             | 급증률           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"sort_tp" : "1",
	"tm_tp" : "2",
	"trde_qty_tp" : "5",
	"tm" : "",
	"stk_cnd" : "0",
	"pric_tp" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"trde_qty_sdnin":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-152000",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.07",
				"prev_trde_qty":"22532511",
				"now_trde_qty":"31103523",
				"sdnin_qty":"+8571012",
				"sdnin_rt":"+38.04"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-94400",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.11",
				"prev_trde_qty":"25027263",
				"now_trde_qty":"30535372",
				"sdnin_qty":"+5508109",
				"sdnin_rt":"+22.01"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-42900",
				"pred_pre_sig":"5",
				"pred_pre":"-150",
				"flu_rt":"-0.35",
				"prev_trde_qty":"25717492",
				"now_trde_qty":"31033221",
				"sdnin_qty":"+5315729",
				"sdnin_rt":"+20.67"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-22350",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.45",
				"prev_trde_qty":"25548474",
				"now_trde_qty":"30673438",
				"sdnin_qty":"+5124964",
				"sdnin_rt":"+20.06"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-56400",
				"pred_pre_sig":"5",
				"pred_pre":"-300",
				"flu_rt":"-0.53",
				"prev_trde_qty":"26185726",
				"now_trde_qty":"30990416",
				"sdnin_qty":"+4804690",
				"sdnin_rt":"+18.35"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 예상체결등락률상위요청 (ka10029)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------ | ------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp      | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| sort_tp      | 정렬구분     | String | Y        | 1      | 1:상승률, 2:상승폭, 3:보합, 4:하락률, 5:하락폭, 6:체결량, 7:상한, 8:하한                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| trde_qty_cnd | 거래량조건   | String | Y        | 5      | 0:전체조회, 1;천주이상, 3:3천주, 5:5천주, 10:만주이상, 50:5만주이상, 100:10만주이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| stk_cnd      | 종목조건     | String | Y        | 2      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 11:정리매매종목제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 17:ETN제외, 14:ETF제외, 18:ETF+ETN제외, 15:스팩제외, 20:ETF+ETN+스팩제외                                                                                                                                                   |
| crd_cnd      | 신용조건     | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 5:신용한도초과제외, 8:신용대주                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| pric_cnd     | 가격조건     | String | Y        | 2      | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10:1만원미만                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| stex_tp      | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명               | Type   | Required | Length | Description |
| ---------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| exp_cntr_flu_rt_upper  | 예상체결등락률상위   | LIST   | N        |        |             |
| - stk_cd               | 종목코드             | String | N        | 20     |             |
| - stk_nm               | 종목명               | String | N        | 20     |             |
| - exp_cntr_pric        | 예상체결가           | String | N        | 20     |             |
| - base_pric            | 기준가               | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호         | String | N        | 20     |             |
| - pred_pre             | 전일대비             | String | N        | 20     |             |
| - flu_rt               | 등락률               | String | N        | 20     |             |
| - exp_cntr_qty         | 예상체결량           | String | N        | 20     |             |
| - sel_req              | 매도잔량             | String | N        | 20     |             |
| - sel_bid              | 매도호가             | String | N        | 20     |             |
| - buy_bid              | 매수호가             | String | N        | 20     |             |
| - buy_req              | 매수잔량             | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"sort_tp" : "1",
	"trde_qty_cnd" : "0",
	"stk_cnd" : "0",
	"crd_cnd" : "0",
	"pric_cnd" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"exp_cntr_flu_rt_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"exp_cntr_pric":"+48100",
				"base_pric":"37000",
				"pred_pre_sig":"1",
				"pred_pre":"+11100",
				"flu_rt":"+30.00",
				"exp_cntr_qty":"1",
				"sel_req":"0",
				"sel_bid":"0",
				"buy_bid":"0",
				"buy_req":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"exp_cntr_pric":"+40000",
				"base_pric":"34135",
				"pred_pre_sig":"2",
				"pred_pre":"+5865",
				"flu_rt":"+17.18",
				"exp_cntr_qty":"1",
				"sel_req":"1",
				"sel_bid":"+40000",
				"buy_bid":"+35370",
				"buy_req":"1"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"exp_cntr_pric":"+37750",
				"base_pric":"36550",
				"pred_pre_sig":"2",
				"pred_pre":"+1200",
				"flu_rt":"+3.28",
				"exp_cntr_qty":"2",
				"sel_req":"0",
				"sel_bid":"0",
				"buy_bid":"+37850",
				"buy_req":"3"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 당일거래량상위요청 (ka10030)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp        | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| sort_tp        | 정렬구분     | String | Y        | 1      | 1:거래량, 2:거래회전율, 3:거래대금                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| mang_stk_incls | 관리종목포함 | String | Y        | 1      | 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외, 11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100만보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| crd_tp         | 신용구분     | String | Y        | 1      | 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| trde_qty_tp    | 거래량구분   | String | Y        | 1      | 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| pric_tp        | 가격구분     | String | Y        | 1      | 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원, 4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상, 9:10만원이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| trde_prica_tp  | 거래대금구분 | String | Y        | 1      | 0:전체조회, 1:1천만원이상, 3:3천만원이상, 4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| mrkt_open_tp   | 장운영구분   | String | Y        | 1      | 0:전체조회, 1:장중, 2:장전시간외, 3:장후시간외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| stex_tp        | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| tdy_trde_qty_upper     | 당일거래량상위   | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호     | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - flu_rt               | 등락률           | String | N        | 20     |             |
| - trde_qty             | 거래량           | String | N        | 20     |             |
| - pred_rt              | 전일비           | String | N        | 20     |             |
| - trde_tern_rt         | 거래회전율       | String | N        | 20     |             |
| - trde_amt             | 거래금액         | String | N        | 20     |             |
| - opmr_trde_qty        | 장중거래량       | String | N        | 20     |             |
| - opmr_pred_rt         | 장중전일비       | String | N        | 20     |             |
| - opmr_trde_rt         | 장중거래회전율   | String | N        | 20     |             |
| - opmr_trde_amt        | 장중거래금액     | String | N        | 20     |             |
| - af_mkrt_trde_qty     | 장후거래량       | String | N        | 20     |             |
| - af_mkrt_pred_rt      | 장후전일비       | String | N        | 20     |             |
| - af_mkrt_trde_rt      | 장후거래회전율   | String | N        | 20     |             |
| - af_mkrt_trde_amt     | 장후거래금액     | String | N        | 20     |             |
| - bf_mkrt_trde_qty     | 장전거래량       | String | N        | 20     |             |
| - bf_mkrt_pred_rt      | 장전전일비       | String | N        | 20     |             |
| - bf_mkrt_trde_rt      | 장전거래회전율   | String | N        | 20     |             |
| - bf_mkrt_trde_amt     | 장전거래금액     | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"sort_tp" : "1",
	"mang_stk_incls" : "1",
	"crd_tp" : "0",
	"trde_qty_tp" : "0",
	"pric_tp" : "0",
	"trde_prica_tp" : "0",
	"mrkt_open_tp" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"tdy_trde_qty_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-152000",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.07",
				"trde_qty":"34954641",
				"pred_rt":"+155.13",
				"trde_tern_rt":"+48.21",
				"trde_amt":"5308092",
				"opmr_trde_qty":"0",
				"opmr_pred_rt":"0.00",
				"opmr_trde_rt":"+0.00",
				"opmr_trde_amt":"0",
				"af_mkrt_trde_qty":"0",
				"af_mkrt_pred_rt":"0.00",
				"af_mkrt_trde_rt":"+0.00",
				"af_mkrt_trde_amt":"0",
				"bf_mkrt_trde_qty":"0",
				"bf_mkrt_pred_rt":"0.00",
				"bf_mkrt_trde_rt":"+0.00",
				"bf_mkrt_trde_amt":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-53700",
				"pred_pre_sig":"4",
				"pred_pre":"-23000",
				"flu_rt":"-29.99",
				"trde_qty":"31821639",
				"pred_rt":"+135.53",
				"trde_tern_rt":"+13.83",
				"trde_amt":"2436091",
				"opmr_trde_qty":"0",
				"opmr_pred_rt":"0.00",
				"opmr_trde_rt":"+0.00",
				"opmr_trde_amt":"0",
				"af_mkrt_trde_qty":"0",
				"af_mkrt_pred_rt":"0.00",
				"af_mkrt_trde_rt":"+0.00",
				"af_mkrt_trde_amt":"0",
				"bf_mkrt_trde_qty":"0",
				"bf_mkrt_pred_rt":"0.00",
				"bf_mkrt_trde_rt":"+0.00",
				"bf_mkrt_trde_amt":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-42950",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.23",
				"trde_qty":"34854261",
				"pred_rt":"+135.53",
				"trde_tern_rt":"+13.83",
				"trde_amt":"1501908",
				"opmr_trde_qty":"0",
				"opmr_pred_rt":"0.00",
				"opmr_trde_rt":"+0.00",
				"opmr_trde_amt":"0",
				"af_mkrt_trde_qty":"0",
				"af_mkrt_pred_rt":"0.00",
				"af_mkrt_trde_rt":"+0.00",
				"af_mkrt_trde_amt":"0",
				"bf_mkrt_trde_qty":"0",
				"bf_mkrt_pred_rt":"0.00",
				"bf_mkrt_trde_rt":"+0.00",
				"bf_mkrt_trde_amt":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 전일거래량상위요청 (ka10031)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명     | Type   | Required | Length | Description                                                          |
| ---------- | ---------- | ------ | -------- | ------ | -------------------------------------------------------------------- |
| mrkt_tp    | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                     |
| qry_tp     | 조회구분   | String | Y        | 1      | 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목                 |
| rank_strt  | 순위시작   | String | Y        | 3      | 0 ~ 100 값 중에 조회를 원하는 순위 시작값                           |
| rank_end   | 순위끝     | String | Y        | 3      | 0 ~ 100 값 중에 조회를 원하는 순위 끝값                             |
| stex_tp    | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                  |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| pred_trde_qty_upper    | 전일거래량상위   | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호     | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - trde_qty             | 거래량           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "101",
	"qry_tp" : "1",
	"rank_strt" : "0",
	"rank_end" : "10",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"pred_trde_qty_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"81",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"2050",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"2375",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-43750",
				"pred_pre_sig":"5",
				"pred_pre":"-50",
				"trde_qty":"34605668"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"70",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-56600",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"trde_qty":"33014975"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"11260",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-65300",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"trde_qty":"28117804"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-94400",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"trde_qty":"34289700"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-18610",
				"pred_pre_sig":"5",
				"pred_pre":"-20",
				"trde_qty":"33030086"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 거래대금상위요청 (ka10032)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                              |
| -------------- | ------------ | ------ | -------- | ------ | ---------------------------------------- |
| mrkt_tp        | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥         |
| mang_stk_incls | 관리종목포함 | String | Y        | 1      | 0:관리종목 포함, 1:관리종목 미포함       |
| stex_tp        | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명       | Type   | Required | Length | Description |
| -------------------- | ------------ | ------ | -------- | ------ | ----------- |
| trde_prica_upper     | 거래대금상위 | LIST   | N        |        |             |
| - stk_cd             | 종목코드     | String | N        | 20     |             |
| - now_rank           | 현재순위     | String | N        | 20     |             |
| - pred_rank          | 전일순위     | String | N        | 20     |             |
| - stk_nm             | 종목명       | String | N        | 20     |             |
| - cur_prc            | 현재가       | String | N        | 20     |             |
| - pred_pre_sig       | 전일대비기호 | String | N        | 20     |             |
| - pred_pre           | 전일대비     | String | N        | 20     |             |
| - flu_rt             | 등락률       | String | N        | 20     |             |
| - sel_bid            | 매도호가     | String | N        | 20     |             |
| - buy_bid            | 매수호가     | String | N        | 20     |             |
| - now_trde_qty       | 현재거래량   | String | N        | 20     |             |
| - pred_trde_qty      | 전일거래량   | String | N        | 20     |             |
| - trde_prica         | 거래대금     | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "001",
	"mang_stk_incls" : "1",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"trde_prica_upper":
		[
			{
				"stk_cd":"005930",
				"now_rank":"1",
				"pred_rank":"1",
				"stk_nm":"삼성전자",
				"cur_prc":"-152000",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.07",
				"sel_bid":"-152000",
				"buy_bid":"-150000",
				"now_trde_qty":"34954641",
				"pred_trde_qty":"22532511",
				"trde_prica":"5308092"
			},
			{
				"stk_cd":"005930",
				"now_rank":"2",
				"pred_rank":"2",
				"stk_nm":"삼성전자",
				"cur_prc":"-53700",
				"pred_pre_sig":"4",
				"pred_pre":"-23000",
				"flu_rt":"-29.99",
				"sel_bid":"-76500",
				"buy_bid":"+85100",
				"now_trde_qty":"31821639",
				"pred_trde_qty":"30279412",
				"trde_prica":"2436091"
			},
			{
				"stk_cd":"005930",
				"now_rank":"3",
				"pred_rank":"3",
				"stk_nm":"삼성전자",
				"cur_prc":"-42950",
				"pred_pre_sig":"5",
				"pred_pre":"-100",
				"flu_rt":"-0.23",
				"sel_bid":"-42950",
				"buy_bid":"+45250",
				"now_trde_qty":"34854261",
				"pred_trde_qty":"25717492",
				"trde_prica":"1501908"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 신용비율상위요청 (ka10033)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                                                                                                      |
| ------------ | ------------ | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| mrkt_tp      | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                 |
| trde_qty_tp  | 거래량구분   | String | Y        | 3      | 0:전체조회, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상                          |
| stk_cnd      | 종목조건     | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기                                                  |
| updown_incls | 상하한포함   | String | Y        | 1      | 0:상하한 미포함, 1:상하한포함                                                                                                                    |
| crd_cnd      | 신용조건     | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                           |
| stex_tp      | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명       | Type   | Required | Length | Description |
| -------------------- | ------------ | ------ | -------- | ------ | ----------- |
| crd_rt_upper         | 신용비율상위 | LIST   | N        |        |             |
| - stk_infr           | 종목정보     | String | N        | 20     |             |
| - stk_cd             | 종목코드     | String | N        | 20     |             |
| - stk_nm             | 종목명       | String | N        | 20     |             |
| - cur_prc            | 현재가       | String | N        | 20     |             |
| - pred_pre_sig       | 전일대비기호 | String | N        | 20     |             |
| - pred_pre           | 전일대비     | String | N        | 20     |             |
| - flu_rt             | 등락률       | String | N        | 20     |             |
| - crd_rt             | 신용비율     | String | N        | 20     |             |
| - sel_req            | 매도잔량     | String | N        | 20     |             |
| - buy_req            | 매수잔량     | String | N        | 20     |             |
| - now_trde_qty       | 현재거래량   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"trde_qty_tp" : "0",
	"stk_cnd" : "0",
	"updown_incls" : "1",
	"crd_cnd" : "0",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"crd_rt_upper":
		[
			{
				"stk_infr":"0",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"16420",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"crd_rt":"+9.49",
				"sel_req":"0",
				"buy_req":"0",
				"now_trde_qty":"0"
			},
			{
				"stk_infr":"0",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"3415",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"crd_rt":"+9.48",
				"sel_req":"1828",
				"buy_req":"0",
				"now_trde_qty":"0"
			},
			{
				"stk_infr":"0",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"3660",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"crd_rt":"+8.92",
				"sel_req":"0",
				"buy_req":"0",
				"now_trde_qty":"0"
			},
			{
				"stk_infr":"0",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"11050",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"crd_rt":"+8.73",
				"sel_req":"0",
				"buy_req":"0",
				"now_trde_qty":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 외인기간별매매상위요청 (ka10034)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                                |
| ------- | ---------- | ------ | -------- | ------ | ---------------------------------------------------------- |
| mrkt_tp | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                           |
| trde_tp | 매매구분   | String | Y        | 1      | 1:순매도, 2:순매수, 3:순매매                               |
| dt      | 기간       | String | Y        | 2      | 0:당일, 1:전일, 5:5일, 10:10일, 20:20일, 60:60일           |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명               | Type   | Required | Length | Description |
| --------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| for_dt_trde_upper     | 외인기간별매매상위   | LIST   | N        |        |             |
| - rank                | 순위                 | String | N        | 20     |             |
| - stk_cd              | 종목코드             | String | N        | 20     |             |
| - stk_nm              | 종목명               | String | N        | 20     |             |
| - cur_prc             | 현재가               | String | N        | 20     |             |
| - pred_pre_sig        | 전일대비기호         | String | N        | 20     |             |
| - pred_pre            | 전일대비             | String | N        | 20     |             |
| - sel_bid             | 매도호가             | String | N        | 20     |             |
| - buy_bid             | 매수호가             | String | N        | 20     |             |
| - trde_qty            | 거래량               | String | N        | 20     |             |
| - netprps_qty         | 순매수량             | String | N        | 20     |             |
| - gain_pos_stkcnt     | 취득가능주식수       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "001",
	"trde_tp" : "2",
	"dt" : "0",
	"stex_tp" : "1"
}
```

#### 응답 예시

```json
{
	"for_dt_trde_upper":
		[
			{
				"rank":"1",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+74800",
				"pred_pre_sig":"1",
				"pred_pre":"+17200",
				"sel_bid":"0",
				"buy_bid":"+74800",
				"trde_qty":"435771",
				"netprps_qty":"+290232191",
				"gain_pos_stkcnt":"2548278006"
			},
			{
				"rank":"2",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-183500",
				"pred_pre_sig":"5",
				"pred_pre":"-900",
				"sel_bid":"+184900",
				"buy_bid":"0",
				"trde_qty":"135",
				"netprps_qty":"+167189864",
				"gain_pos_stkcnt":"0"
			},
			{
				"rank":"3",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"4115",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"sel_bid":"0",
				"buy_bid":"0",
				"trde_qty":"0",
				"netprps_qty":"+59255646",
				"gain_pos_stkcnt":"430439234"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 외인연속순매매상위요청 (ka10035)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명       | Type   | Required | Length | Description                                      |
| ----------- | ------------ | ------ | -------- | ------ | ------------------------------------------------ |
| mrkt_tp     | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                 |
| trde_tp     | 매매구분     | String | Y        | 1      | 1:연속순매도, 2:연속순매수                       |
| base_dt_tp  | 기준일구분   | String | Y        | 1      | 0:당일기준, 1:전일기준                           |
| stex_tp     | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                     | 한글명               | Type   | Required | Length | Description |
| --------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| for_cont_nettrde_upper      | 외인연속순매매상위   | LIST   | N        |        |             |
| - stk_cd                    | 종목코드             | String | N        | 20     |             |
| - stk_nm                    | 종목명               | String | N        | 20     |             |
| - cur_prc                   | 현재가               | String | N        | 20     |             |
| - pred_pre_sig              | 전일대비기호         | String | N        | 20     |             |
| - pred_pre                  | 전일대비             | String | N        | 20     |             |
| - dm1                       | D-1                  | String | N        | 20     |             |
| - dm2                       | D-2                  | String | N        | 20     |             |
| - dm3                       | D-3                  | String | N        | 20     |             |
| - tot                       | 합계                 | String | N        | 20     |             |
| - limit_exh_rt              | 한도소진율           | String | N        | 20     |             |
| - pred_pre_1                | 전일대비1            | String | N        | 20     |             |
| - pred_pre_2                | 전일대비2            | String | N        | 20     |             |
| - pred_pre_3                | 전일대비3            | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"trde_tp" : "2",
	"base_dt_tp" : "1",
	"stex_tp" : "1"
}
```

#### 응답 예시

```json
{
	"for_cont_nettrde_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"10200",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"dm1":"+33928250",
				"dm2":"+234840",
				"dm3":"+233891",
				"tot":"+34396981",
				"limit_exh_rt":"+71.53",
				"pred_pre_1":"",
				"pred_pre_2":"",
				"pred_pre_3":""
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"-8540",
				"pred_pre_sig":"5",
				"pred_pre":"-140",
				"dm1":"+4033818",
				"dm2":"+12474308",
				"dm3":"+13173262",
				"tot":"+29681388",
				"limit_exh_rt":"+0.10",
				"pred_pre_1":"",
				"pred_pre_2":"",
				"pred_pre_3":""
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"23000",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"dm1":"+24595310",
				"dm2":"+247863",
				"dm3":"+247188",
				"tot":"+25090361",
				"limit_exh_rt":"+38.85",
				"pred_pre_1":"",
				"pred_pre_2":"",
				"pred_pre_3":""
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"195800",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"dm1":"+21220444",
				"dm2":"+213984",
				"dm3":"+104034",
				"tot":"+21538462",
				"limit_exh_rt":"+54.76",
				"pred_pre_1":"",
				"pred_pre_2":"",
				"pred_pre_3":""
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 외인한도소진율증가상위요청 (ka10036)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                         |
| ------- | ---------- | ------ | -------- | ------ | --------------------------------------------------- |
| mrkt_tp | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                    |
| dt      | 기간       | String | Y        | 2      | 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일    |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                            | 한글명                | Type   | Required | Length | Description |
| ---------------------------------- | --------------------- | ------ | -------- | ------ | ----------- |
| for_limit_exh_rt_incrs_upper       | 외인한도소진율증가상위 | LIST   | N        |        |             |
| - rank                             | 순위                  | String | N        | 20     |             |
| - stk_cd                           | 종목코드              | String | N        | 20     |             |
| - stk_nm                           | 종목명                | String | N        | 20     |             |
| - cur_prc                          | 현재가                | String | N        | 20     |             |
| - pred_pre_sig                     | 전일대비기호          | String | N        | 20     |             |
| - pred_pre                         | 전일대비              | String | N        | 20     |             |
| - trde_qty                         | 거래량                | String | N        | 20     |             |
| - poss_stkcnt                      | 보유주식수            | String | N        | 20     |             |
| - gain_pos_stkcnt                  | 취득가능주식수        | String | N        | 20     |             |
| - base_limit_exh_rt                | 기준한도소진율        | String | N        | 20     |             |
| - limit_exh_rt                     | 한도소진율            | String | N        | 20     |             |
| - exh_rt_incrs                     | 소진율증가            | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"dt" : "1",
	"stex_tp" : "1"
}
```

#### 응답 예시

```json
{
	"for_limit_exh_rt_incrs_upper":
		[
			{
				"rank":"1",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"14255",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0",
				"poss_stkcnt":"0",
				"gain_pos_stkcnt":"600000",
				"base_limit_exh_rt":"-283.33",
				"limit_exh_rt":"0.00",
				"exh_rt_incrs":"+283.33"
			},
			{
				"rank":"2",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"1590",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"trde_qty":"0",
				"poss_stkcnt":"519785",
				"gain_pos_stkcnt":"31404714",
				"base_limit_exh_rt":"-101.25",
				"limit_exh_rt":"+1.63",
				"exh_rt_incrs":"+102.87"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 외국계창구매매상위요청 (ka10037)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                         |
| ------- | ---------- | ------ | -------- | ------ | --------------------------------------------------- |
| mrkt_tp | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                    |
| dt      | 기간       | String | Y        | 2      | 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일    |
| trde_tp | 매매구분   | String | Y        | 1      | 1:순매수, 2:순매도, 3:매수, 4:매도                  |
| sort_tp | 정렬구분   | String | Y        | 1      | 1:금액, 2:수량                                      |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                   | 한글명               | Type   | Required | Length | Description |
| ------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| frgn_wicket_trde_upper    | 외국계창구매매상위   | LIST   | N        |        |             |
| - rank                    | 순위                 | String | N        | 20     |             |
| - stk_cd                  | 종목코드             | String | N        | 20     |             |
| - stk_nm                  | 종목명               | String | N        | 20     |             |
| - cur_prc                 | 현재가               | String | N        | 20     |             |
| - pred_pre_sig            | 전일대비기호         | String | N        | 20     |             |
| - pred_pre                | 전일대비             | String | N        | 20     |             |
| - flu_rt                  | 등락율               | String | N        | 20     |             |
| - sel_trde_qty            | 매도거래량           | String | N        | 20     |             |
| - buy_trde_qty            | 매수거래량           | String | N        | 20     |             |
| - netprps_trde_qty        | 순매수거래량         | String | N        | 20     |             |
| - netprps_prica           | 순매수대금           | String | N        | 20     |             |
| - trde_qty                | 거래량               | String | N        | 20     |             |
| - trde_prica              | 거래대금             | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp" : "000",
	"dt" : "0",
	"trde_tp" : "1",
	"sort_tp" : "2",
	"stex_tp" : "1"
}
```

#### 응답 예시

```json
{
	"frgn_wicket_trde_upper":
		[
			{
				"rank":"1",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"69",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"sel_trde_qty":"-0",
				"buy_trde_qty":"+0",
				"netprps_trde_qty":"0",
				"netprps_prica":"0",
				"trde_qty":"0",
				"trde_prica":"0"
			},
			{
				"rank":"2",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"316",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"sel_trde_qty":"-0",
				"buy_trde_qty":"+0",
				"netprps_trde_qty":"0",
				"netprps_prica":"0",
				"trde_qty":"0",
				"trde_prica":"0"
			},
			{
				"rank":"3",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"675",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"sel_trde_qty":"-0",
				"buy_trde_qty":"+0",
				"netprps_trde_qty":"0",
				"netprps_prica":"0",
				"trde_qty":"0",
				"trde_prica":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 종목별증권사순위요청 (ka10038)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                                                                      |
| ------- | ---------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------ |
| stk_cd  | 종목코드   | String | Y        | 6      | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)                                   |
| strt_dt | 시작일자   | String | Y        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                                |
| end_dt  | 종료일자   | String | Y        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                                |
| qry_tp  | 조회구분   | String | Y        | 1      | 1:순매도순위정렬, 2:순매수순위정렬                                                               |
| dt      | 기간       | String | Y        | 2      | 1:전일, 4:5일, 9:10일, 19:20일, 39:40일, 59:60일, 119:120일                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명               | Type   | Required | Length | Description |
| -------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| rank_1               | 순위1                | String | N        | 20     |             |
| rank_2               | 순위2                | String | N        | 20     |             |
| rank_3               | 순위3                | String | N        | 20     |             |
| prid_trde_qty        | 기간중거래량         | String | N        | 20     |             |
| stk_sec_rank         | 종목별증권사순위     | LIST   | N        |        |             |
| - rank               | 순위                 | String | N        | 20     |             |
| - mmcm_nm            | 회원사명             | String | N        | 20     |             |
| - buy_qty            | 매수수량             | String | N        | 20     |             |
| - sell_qty           | 매도수량             | String | N        | 20     |             |
| - acc_netprps_qty    | 누적순매수수량       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd" : "005930",
	"strt_dt" : "20241106",
	"end_dt" : "20241107",
	"qry_tp" : "2",
	"dt" : "1"
}
```

#### 응답 예시

```json
{
	"rank_1":"+34881",
	"rank_2":"-13253",
	"rank_3":"+21628",
	"prid_trde_qty":"43",
	"stk_sec_rank":
		[
			{
				"rank":"1",
				"mmcm_nm":"키움증권",
				"buy_qty":"+9800",
				"sell_qty":"-2813",
				"acc_netprps_qty":"+6987"
			},
			{
				"rank":"2",
				"mmcm_nm":"키움증권",
				"buy_qty":"+3459",
				"sell_qty":"-117",
                "acc_netprps_qty":"+3342"
			},
			{
				"rank":"3",
				"mmcm_nm":"키움증권",
				"buy_qty":"+3321",
				"sell_qty":"-125",
				"acc_netprps_qty":"+3196"
			},
			{
				"rank":"4",
				"mmcm_nm":"키움증권",
				"buy_qty":"+3941",
				"sell_qty":"-985",
				"acc_netprps_qty":"+2956"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 증권사별매매상위요청 (ka10039)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명     | Type   | Required | Length | Description                                                                                      |
| ----------- | ---------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------ |
| mmcm_cd     | 회원사코드 | String | Y        | 3      | 회원사 코드는 ka10102 조회                                                                       |
| trde_qty_tp | 거래량구분 | String | Y        | 4      | 0:전체, 5:5000주, 10:1만주, 50:5만주, 100:10만주, 500:50만주, 1000: 100만주                      |
| trde_tp     | 매매구분   | String | Y        | 2      | 1:순매수, 2:순매도                                                                               |
| dt          | 기간       | String | Y        | 2      | 1:전일, 5:5일, 10:10일, 60:60일                                                                  |
| stex_tp     | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명               | Type   | Required | Length | Description |
| -------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| sec_trde_upper       | 증권사별매매상위     | LIST   | N        |        |             |
| - rank               | 순위                 | String | N        | 20     |             |
| - stk_cd             | 종목코드             | String | N        | 20     |             |
| - stk_nm             | 종목명               | String | N        | 20     |             |
| - prid_stkpc_flu     | 기간중주가등락       | String | N        | 20     |             |
| - flu_rt             | 등락율               | String | N        | 20     |             |
| - prid_trde_qty      | 기간중거래량         | String | N        | 20     |             |
| - netprps            | 순매수               | String | N        | 20     |             |
| - buy_trde_qty       | 매수거래량           | String | N        | 20     |             |
| - sel_trde_qty       | 매도거래량           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mmcm_cd" : "001",
	"trde_qty_tp" : "0",
	"trde_tp" : "1",
	"dt" : "1",
	"stex_tp" : "3"
}
```

#### 응답 예시

```json
{
	"sec_trde_upper":
		[
			{
				"rank":"1",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"prid_stkpc_flu":"+1800",
				"flu_rt":"+0.93",
				"prid_trde_qty":"241",
				"netprps":"+27401",
				"buy_trde_qty":"+33131",
				"sel_trde_qty":"-5730"
			},
			{
				"rank":"2",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"prid_stkpc_flu":"0",
				"flu_rt":"0.00",
				"prid_trde_qty":"0",
				"netprps":"+154140",
				"buy_trde_qty":"+302708",
				"sel_trde_qty":"-148568"
			},
			{
				"rank":"3",
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"prid_stkpc_flu":"0",
				"flu_rt":"0.00",
				"prid_trde_qty":"0",
				"netprps":"+6724",
				"buy_trde_qty":"+12018",
				"sel_trde_qty":"-5294"
			}
		],
	"returnCode":0,
	"returnMsg":"정상적으로 처리되었습니다"
}
```

---

### 당일주요거래원요청 (ka10040)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                   | 한글명                | Type   | Required | Length | Description |
| ------------------------- | --------------------- | ------ | -------- | ------ | ----------- |
| sel_trde_ori_irds_1       | 매도거래원별증감1     | String | N        |        |             |
| sel_trde_ori_qty_1        | 매도거래원수량1       | String | N        |        |             |
| sel_trde_ori_1            | 매도거래원1           | String | N        |        |             |
| sel_trde_ori_cd_1         | 매도거래원코드1       | String | N        |        |             |
| buy_trde_ori_1            | 매수거래원1           | String | N        |        |             |
| buy_trde_ori_cd_1         | 매수거래원코드1       | String | N        |        |             |
| buy_trde_ori_qty_1        | 매수거래원수량1       | String | N        |        |             |
| buy_trde_ori_irds_1       | 매수거래원별증감1     | String | N        |        |             |
| sel_trde_ori_irds_2       | 매도거래원별증감2     | String | N        |        |             |
| sel_trde_ori_qty_2        | 매도거래원수량2       | String | N        |        |             |
| sel_trde_ori_2            | 매도거래원2           | String | N        |        |             |
| sel_trde_ori_cd_2         | 매도거래원코드2       | String | N        |        |             |
| buy_trde_ori_2            | 매수거래원2           | String | N        |        |             |
| buy_trde_ori_cd_2         | 매수거래원코드2       | String | N        |        |             |
| buy_trde_ori_qty_2        | 매수거래원수량2       | String | N        |        |             |
| buy_trde_ori_irds_2       | 매수거래원별증감2     | String | N        |        |             |
| sel_trde_ori_irds_3       | 매도거래원별증감3     | String | N        |        |             |
| sel_trde_ori_qty_3        | 매도거래원수량3       | String | N        |        |             |
| sel_trde_ori_3            | 매도거래원3           | String | N        |        |             |
| sel_trde_ori_cd_3         | 매도거래원코드3       | String | N        |        |             |
| buy_trde_ori_3            | 매수거래원3           | String | N        |        |             |
| buy_trde_ori_cd_3         | 매수거래원코드3       | String | N        |        |             |
| buy_trde_ori_qty_3        | 매수거래원수량3       | String | N        |        |             |
| buy_trde_ori_irds_3       | 매수거래원별증감3     | String | N        |        |             |
| sel_trde_ori_irds_4       | 매도거래원별증감4     | String | N        |        |             |
| sel_trde_ori_qty_4        | 매도거래원수량4       | String | N        |        |             |
| sel_trde_ori_4            | 매도거래원4           | String | N        |        |             |
| sel_trde_ori_cd_4         | 매도거래원코드4       | String | N        |        |             |
| buy_trde_ori_4            | 매수거래원4           | String | N        |        |             |
| buy_trde_ori_cd_4         | 매수거래원코드4       | String | N        |        |             |
| buy_trde_ori_qty_4        | 매수거래원수량4       | String | N        |        |             |
| buy_trde_ori_irds_4       | 매수거래원별증감4     | String | N        |        |             |
| sel_trde_ori_irds_5       | 매도거래원별증감5     | String | N        |        |             |
| sel_trde_ori_qty_5        | 매도거래원수량5       | String | N        |        |             |
| sel_trde_ori_5            | 매도거래원5           | String | N        |        |             |
| sel_trde_ori_cd_5         | 매도거래원코드5       | String | N        |        |             |
| buy_trde_ori_5            | 매수거래원5           | String | N        |        |             |
| buy_trde_ori_cd_5         | 매수거래원코드5       | String | N        |        |             |
| buy_trde_ori_qty_5        | 매수거래원수량5       | String | N        |        |             |
| buy_trde_ori_irds_5       | 매수거래원별증감5     | String | N        |        |             |
| frgn_sel_prsm_sum_chang   | 외국계매도추정합변동  | String | N        |        |             |
| frgn_sel_prsm_sum         | 외국계매도추정합      | String | N        |        |             |
| frgn_buy_prsm_sum         | 외국계매수추정합      | String | N        |        |             |
| frgn_buy_prsm_sum_chang   | 외국계매수추정합변동  | String | N        |        |             |
| tdy_main_trde_ori         | 당일주요거래원        | LIST   | N        |        |             |
| - sel_scesn_tm            | 매도이탈시간          | String | N        | 20     |             |
| - sell_qty                | 매도수량              | String | N        | 20     |             |
| - sel_upper_scesn_ori     | 매도상위이탈원        | String | N        | 20     |             |
| - buy_scesn_tm            | 매수이탈시간          | String | N        | 20     |             |
| - buy_qty                 | 매수수량              | String | N        | 20     |             |
| - buy_upper_scesn_ori     | 매수상위이탈원        | String | N        | 20     |             |
| - qry_dt                  | 조회일자              | String | N        | 20     |             |
| - qry_tm                  | 조회시간              | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd" : "005930"
}
```

#### 응답 예시

```json
{
	"sel_trde_ori_irds_1":"0",
	"sel_trde_ori_qty_1":"-5689",
	"sel_trde_ori_1":"모건스탠리",
	"sel_trde_ori_cd_1":"036",
	"buy_trde_ori_1":"모건스탠리",
	"buy_trde_ori_cd_1":"036",
	"buy_trde_ori_qty_1":"+6305",
	"buy_trde_ori_irds_1":"+615",
	"sel_trde_ori_irds_2":"+615",
	"sel_trde_ori_qty_2":"-615",
	"sel_trde_ori_2":"신  영",
	"sel_trde_ori_cd_2":"006",
	"buy_trde_ori_2":"키움증권",
	"buy_trde_ori_cd_2":"050",
	"buy_trde_ori_qty_2":"+7",
	"buy_trde_ori_irds_2":"0",
	"sel_trde_ori_irds_3":"0",
	"sel_trde_ori_qty_3":"-8",
	"sel_trde_ori_3":"키움증권",
	"sel_trde_ori_cd_3":"050",
	"buy_trde_ori_3":"",
	"buy_trde_ori_cd_3":"000",
	"buy_trde_ori_qty_3":"0",
	"buy_trde_ori_irds_3":"0",
	"sel_trde_ori_irds_4":"0",
	"sel_trde_ori_qty_4":"0",
	"sel_trde_ori_4":"",
	"sel_trde_ori_cd_4":"000",
	"buy_trde_ori_4":"",
    "buy_trde_ori_cd_4":"000",
	"buy_trde_ori_qty_4":"0",
	"buy_trde_ori_irds_4":"0",
	"sel_trde_ori_irds_5":"0",
	"sel_trde_ori_qty_5":"0",
	"sel_trde_ori_5":"",
	"sel_trde_ori_cd_5":"000",
	"buy_trde_ori_5":"",
	"buy_trde_ori_cd_5":"000",
	"buy_trde_ori_qty_5":"0",
	"buy_trde_ori_irds_5":"0",
	"frgn_sel_prsm_sum_chang":"0",
	"frgn_sel_prsm_sum":"-5689",
	"frgn_buy_prsm_sum":"+6305",
	"frgn_buy_prsm_sum_chang":"+615",
	"tdy_main_trde_ori":
		[
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 순매수거래원순위요청 (ka10042)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명         | Type   | Required | Length | Description                                                                             |
| ---------- | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| stk_cd     | 종목코드       | String | Y        | 6      | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)                         |
| strt_dt    | 시작일자       | String | N        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                       |
| end_dt     | 종료일자       | String | N        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                       |
| qry_dt_tp  | 조회기간구분   | String | Y        | 1      | 0:기간으로 조회, 1:시작일자, 종료일자로 조회                                            |
| pot_tp     | 시점구분       | String | Y        | 1      | 0:당일, 1:전일                                                                          |
| dt         | 기간           | String | N        | 4      | 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일                                    |
| sort_base  | 정렬기준       | String | Y        | 1      | 1:종가순, 2:날짜순                                                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                   | 한글명             | Type   | Required | Length | Description |
| ------------------------- | ------------------ | ------ | -------- | ------ | ----------- |
| netprps_trde_ori_rank     | 순매수거래원순위   | LIST   | N        |        |             |
| - rank                    | 순위               | String | N        | 20     |             |
| - mmcm_cd                 | 회원사코드         | String | N        | 20     |             |
| - mmcm_nm                 | 회원사명           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"strt_dt": "20241031",
	"end_dt": "20241107",
	"qry_dt_tp": "0",
	"pot_tp": "0",
	"dt": "5",
	"sort_base": "1"
}
```

#### 응답 예시

```json
{
	"netprps_trde_ori_rank":
		[
			{
				"rank":"1",
				"mmcm_cd":"36",
				"mmcm_nm":"키움증권"
			},
			{
				"rank":"2",
				"mmcm_cd":"50",
				"mmcm_nm":"키움증권"
			},
			{
				"rank":"3",
				"mmcm_cd":"45",
				"mmcm_nm":"키움증권"
			},
			{
				"rank":"4",
				"mmcm_cd":"6",
				"mmcm_nm":"키움증권"
			},
			{
				"rank":"5",
				"mmcm_cd":"64",
				"mmcm_nm":"키움증권"
			},
			{
				"rank":"6",
				"mmcm_cd":"31",
				"mmcm_nm":"키움증권"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 당일상위이탈원요청 (ka10053)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                             |
| ------- | -------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 6      | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                   | 한글명             | Type   | Required | Length | Description |
| ------------------------- | ------------------ | ------ | -------- | ------ | ----------- |
| tdy_upper_scesn_ori       | 당일상위이탈원     | LIST   | N        |        |             |
| - sel_scesn_tm            | 매도이탈시간       | String | N        | 20     |             |
| - sell_qty                | 매도수량           | String | N        | 20     |             |
| - sel_upper_scesn_ori     | 매도상위이탈원     | String | N        | 20     |             |
| - buy_scesn_tm            | 매수이탈시간       | String | N        | 20     |             |
| - buy_qty                 | 매수수량           | String | N        | 20     |             |
| - buy_upper_scesn_ori     | 매수상위이탈원     | String | N        | 20     |             |
| - qry_dt                  | 조회일자           | String | N        | 20     |             |
| - qry_tm                  | 조회시간           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"tdy_upper_scesn_ori":
		[
			{
				"sel_scesn_tm":"154706",
				"sell_qty":"32",
				"sel_upper_scesn_ori":"키움증권",
				"buy_scesn_tm":"151615",
				"buy_qty":"48",
				"buy_upper_scesn_ori":"키움증권",
				"qry_dt":"012",
				"qry_tm":"012"
			},
			{
				"sel_scesn_tm":"145127",
				"sell_qty":"14",
				"sel_upper_scesn_ori":"키움증권",
				"buy_scesn_tm":"144055",
				"buy_qty":"21",
				"buy_upper_scesn_ori":"키움증권",
				"qry_dt":"017",
				"qry_tm":"046"
			},
			{
				"sel_scesn_tm":"145117",
				"sell_qty":"10",
				"sel_upper_scesn_ori":"키움증권",
				"buy_scesn_tm":"140901",
				"buy_qty":"3",
				"buy_upper_scesn_ori":"키움증권",
				"qry_dt":"050",
				"qry_tm":"056"
			},
			{
				"sel_scesn_tm":"",
				"sell_qty":"",
				"sel_upper_scesn_ori":"",
				"buy_scesn_tm":"135548",
				"buy_qty":"2",
				"buy_upper_scesn_ori":"키움증권",
				"qry_dt":"",
				"qry_tm":"001"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 동일순매매순위요청 (ka10062)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element   | 한글명     | Type   | Required | Length | Description                                                                             |
| --------- | ---------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| strt_dt   | 시작일자   | String | Y        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                       |
| end_dt    | 종료일자   | String | N        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                       |
| mrkt_tp   | 시장구분   | String | Y        | 3      | 000:전체, 001: 코스피, 101:코스닥                                                      |
| trde_tp   | 매매구분   | String | Y        | 1      | 1:순매수, 2:순매도                                                                      |
| sort_cnd  | 정렬조건   | String | Y        | 1      | 1:수량, 2:금액                                                                          |
| unit_tp   | 단위구분   | String | Y        | 1      | 1:단주, 1000:천주                                                                       |
| stex_tp   | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                     |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| eql_nettrde_rank           | 동일순매매순위       | LIST   | N        |        |             |
| - stk_cd                   | 종목코드             | String | N        | 20     |             |
| - rank                     | 순위                 | String | N        | 20     |             |
| - stk_nm                   | 종목명               | String | N        | 20     |             |
| - cur_prc                  | 현재가               | String | N        | 20     |             |
| - pre_sig                  | 대비기호             | String | N        | 20     |             |
| - pred_pre                 | 전일대비             | String | N        | 20     |             |
| - flu_rt                   | 등락율               | String | N        | 20     |             |
| - acc_trde_qty             | 누적거래량           | String | N        | 20     |             |
| - orgn_nettrde_qty         | 기관순매매수량       | String | N        | 20     |             |
| - orgn_nettrde_amt         | 기관순매매금액       | String | N        | 20     |             |
| - orgn_nettrde_avg_pric    | 기관순매매평균가     | String | N        | 20     |             |
| - for_nettrde_qty          | 외인순매매수량       | String | N        | 20     |             |
| - for_nettrde_amt          | 외인순매매금액       | String | N        | 20     |             |
| - for_nettrde_avg_pric     | 외인순매매평균가     | String | N        | 20     |             |
| - nettrde_qty              | 순매매수량           | String | N        | 20     |             |
| - nettrde_amt              | 순매매금액           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"strt_dt": "20241106",
	"end_dt": "20241107",
	"mrkt_tp": "000",
	"trde_tp": "1",
	"sort_cnd": "1",
	"unit_tp": "1",
	"stex_tp": "3"
}
```

#### 응답 예시

```json
{
	"eql_nettrde_rank":
		[
			{
				"stk_cd":"005930",
				"rank":"1",
				"stk_nm":"삼성전자",
				"cur_prc":"-206000",
				"pre_sig":"5",
				"pred_pre":"-500",
				"flu_rt":"-0.24",
				"acc_trde_qty":"85",
				"orgn_nettrde_qty":"+2",
				"orgn_nettrde_amt":"0",
				"orgn_nettrde_avg_pric":"206000",
				"for_nettrde_qty":"+275",
				"for_nettrde_amt":"+59",
				"for_nettrde_avg_pric":"213342",
				"nettrde_qty":"+277",
				"nettrde_amt":"+59"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 장중투자자별매매상위요청 (ka10065)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                                                                                                                                                                                                                                           |
| -------- | ---------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| trde_tp  | 매매구분   | String | Y        | 1      | 1:순매수, 2:순매도                                                                                                                                                                                                                                                   |
| mrkt_tp  | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                                                                                                     |
| orgn_tp  | 기관구분   | String | Y        | 4      | 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계                                                                                                                           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| opmr_invsr_trde_upper      | 장중투자자별매매상위 | LIST   | N        |        |             |
| - stk_cd                   | 종목코드             | String | N        | 20     |             |
| - stk_nm                   | 종목명               | String | N        | 20     |             |
| - sel_qty                  | 매도량               | String | N        | 20     |             |
| - buy_qty                  | 매수량               | String | N        | 20     |             |
| - netslmt                  | 순매도               | String | N        | 20     |             |

#### 요청 예시

```json
{
	"trde_tp": "1",
	"mrkt_tp": "000",
	"orgn_tp": "9000"
}
```

#### 응답 예시

```json
{
	"opmr_invsr_trde_upper":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-39420",
				"buy_qty":"+73452",
				"netslmt":"+34033"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-13970",
				"buy_qty":"+25646",
				"netslmt":"+11676"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-10063",
				"buy_qty":"+21167",
				"netslmt":"+11104"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-37542",
				"buy_qty":"+47604",
				"netslmt":"+10061"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-2310",
				"buy_qty":"+10874",
				"netslmt":"+8564"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-24912",
				"buy_qty":"+33114",
				"netslmt":"+8203"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"sel_qty":"-27306",
				"buy_qty":"+34853",
				"netslmt":"+7547"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 시간외단일가등락율순위요청 (ka10098)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ------------ | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp        | 시장구분     | String | Y        | 3      | 000:전체,001:코스피,101:코스닥                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| sort_base      | 정렬기준     | String | Y        | 1      | 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| stk_cnd        | 종목조건     | String | Y        | 2      | 0:전체조회,1:관리종목제외,2:정리매매종목제외,3:우선주제외,4:관리종목우선주제외,5:증100제외,6:증100만보기,7:증40만보기,8:증30만보기,9:증20만보기,12:증50만보기,13:증60만보기,14:ETF제외,15:스팩제외,16:ETF+ETN제외,17:ETN제외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| trde_qty_cnd   | 거래량조건   | String | Y        | 5      | 0:전체조회, 10:백주이상,50:5백주이상,100;천주이상, 500:5천주이상, 1000:만주이상, 5000:5만주이상, 10000:10만주이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| crd_cnd        | 신용조건     | String | Y        | 1      | 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주, 5:신용한도초과제외                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| trde_prica     | 거래대금     | String | Y        | 5      | 0:전체조회, 5:5백만원이상,10:1천만원이상, 30:3천만원이상, 50:5천만원이상, 100:1억원이상, 300:3억원이상, 500:5억원이상, 1000:10억원이상, 3000:30억원이상, 5000:50억원이상, 10000:100억원이상                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| ovt_sigpric_flu_rt_rank        | 시간외단일가등락율순위   | LIST   | N        |        |             |
| - rank                         | 순위                     | String | N        | 20     |             |
| - stk_cd                       | 종목코드                 | String | N        | 20     |             |
| - stk_nm                       | 종목명                   | String | N        | 20     |             |
| - cur_prc                      | 현재가                   | String | N        | 20     |             |
| - pred_pre_sig                 | 전일대비기호             | String | N        | 20     |             |
| - pred_pre                     | 전일대비                 | String | N        | 20     |             |
| - flu_rt                       | 등락률                   | String | N        | 20     |             |
| - sel_tot_req                  | 매도총잔량               | String | N        | 20     |             |
| - buy_tot_req                  | 매수총잔량               | String | N        | 20     |             |
| - acc_trde_qty                 | 누적거래량               | String | N        | 20     |             |
| - acc_trde_prica               | 누적거래대금             | String | N        | 20     |             |
| - tdy_close_pric               | 당일종가                 | String | N        | 20     |             |
| - tdy_close_pric_flu_rt        | 당일종가등락률           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "000",
	"sort_base": "5",
	"stk_cnd": "0",
	"trde_qty_cnd": "0",
	"crd_cnd": "0",
	"trde_prica": "0"
}
```

#### 응답 예시

```json
{
	"ovt_sigpric_flu_rt_rank":
		[
			{
				"rank":"1",
				"stk_cd":"069500",
				"stk_nm":"KODEX 200",
				"cur_prc":"17140",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"sel_tot_req":"0",
				"buy_tot_req":"24",
				"acc_trde_qty":"42",
				"acc_trde_prica":"1",
				"tdy_close_pric":"17140",
				"tdy_close_pric_flu_rt":"-0.26"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---

### 외국인기관매매상위요청 (ka90009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/rkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명         | Type   | Required | Length | Description                                                                             |
| ----------- | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| mrkt_tp     | 시장구분       | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                      |
| amt_qty_tp  | 금액수량구분   | String | Y        | 1      | 1:금액(천만), 2:수량(천)                                                               |
| qry_dt_tp   | 조회일자구분   | String | Y        | 1      | 0:조회일자 미포함, 1:조회일자 포함                                                     |
| date        | 날짜           | String | N        | 8      | YYYYMMDD<br/>(연도4자리, 월 2자리, 일 2자리 형식)                                       |
| stex_tp     | 거래소구분     | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                   |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                        | 한글명                   | Type   | Required | Length | Description |
| ------------------------------ | ------------------------ | ------ | -------- | ------ | ----------- |
| frgnr_orgn_trde_upper          | 외국인기관매매상위       | LIST   | N        |        |             |
| - for_netslmt_stk_cd           | 외인순매도종목코드       | String | N        | 20     |             |
| - for_netslmt_stk_nm           | 외인순매도종목명         | String | N        | 20     |             |
| - for_netslmt_amt              | 외인순매도금액           | String | N        | 20     |             |
| - for_netslmt_qty              | 외인순매도수량           | String | N        | 20     |             |
| - for_netprps_stk_cd           | 외인순매수종목코드       | String | N        | 20     |             |
| - for_netprps_stk_nm           | 외인순매수종목명         | String | N        | 20     |             |
| - for_netprps_amt              | 외인순매수금액           | String | N        | 20     |             |
| - for_netprps_qty              | 외인순매수수량           | String | N        | 20     |             |
| - orgn_netslmt_stk_cd          | 기관순매도종목코드       | String | N        | 20     |             |
| - orgn_netslmt_stk_nm          | 기관순매도종목명         | String | N        | 20     |             |
| - orgn_netslmt_amt             | 기관순매도금액           | String | N        | 20     |             |
| - orgn_netslmt_qty             | 기관순매도수량           | String | N        | 20     |             |
| - orgn_netprps_stk_cd          | 기관순매수종목코드       | String | N        | 20     |             |
| - orgn_netprps_stk_nm          | 기관순매수종목명         | String | N        | 20     |             |
| - orgn_netprps_amt             | 기관순매수금액           | String | N        | 20     |             |
| - orgn_netprps_qty             | 기관순매수수량           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "000",
	"amt_qty_tp": "1",
	"qry_dt_tp": "1",
	"date": "20241101",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"frgnr_orgn_trde_upper":
		[
			{
				"for_netslmt_stk_cd":"069500",
				"for_netslmt_stk_nm":"KODEX 200",
				"for_netslmt_amt":"-130811",
				"for_netslmt_qty":"-50312",
				"for_netprps_stk_cd":"069500",
				"for_netprps_stk_nm":"KODEX 200",
				"for_netprps_amt":"-130811",
				"for_netprps_qty":"-50312",
				"orgn_netslmt_stk_cd":"069500",
				"orgn_netslmt_stk_nm":"KODEX 200",
				"orgn_netslmt_amt":"-130811",
				"orgn_netslmt_qty":"-50312",
				"orgn_netprps_stk_cd":"069500",
				"orgn_netprps_stk_nm":"KODEX 200",
				"orgn_netprps_amt":"-130811",
				"orgn_netprps_qty":"-50312"
			},
			{
				"for_netslmt_stk_cd":"069500",
				"for_netslmt_stk_nm":"KODEX 200",
				"for_netslmt_amt":"-130811",
				"for_netslmt_qty":"-50312",
				"for_netprps_stk_cd":"069500",
				"for_netprps_stk_nm":"KODEX 200",
				"for_netprps_amt":"-130811",
				"for_netprps_qty":"-50312",
				"orgn_netslmt_stk_cd":"069500",
				"orgn_netslmt_stk_nm":"KODEX 200",
				"orgn_netslmt_amt":"-130811",
				"orgn_netslmt_qty":"-50312",
				"orgn_netprps_stk_cd":"069500",
				"orgn_netprps_stk_nm":"KODEX 200",
				"orgn_netprps_amt":"-130811",
				"orgn_netprps_qty":"-50312"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```# 키움증권 API 문서

## 국내주식 REST API

### 시세

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 주식호가요청 | ka10004 | 주식호가 정보 조회 |
| 주식일주월시분요청 | ka10005 | 주식 일/주/월/시분 정보 조회 |
| 주식시분요청 | ka10006 | 주식 시분 정보 조회 |
| 시세표성정보요청 | ka10007 | 시세표성 정보 조회 |
| 신주인수권전체시세요청 | ka10011 | 신주인수권 전체시세 조회 |
| 일별기관매매종목요청 | ka10044 | 일별 기관매매종목 조회 |
| 종목별기관매매추이요청 | ka10045 | 종목별 기관매매추이 조회 |
| 체결강도추이시간별요청 | ka10046 | 체결강도추이 시간별 조회 |
| 체결강도추이일별요청 | ka10047 | 체결강도추이 일별 조회 |
| 장중투자자별매매요청 | ka10063 | 장중 투자자별매매 조회 |
| 장마감후투자자별매매요청 | ka10066 | 장마감후 투자자별매매 조회 |
| 증권사별종목매매동향요청 | ka10078 | 증권사별 종목매매동향 조회 |
| 일별주가요청 | ka10086 | 일별 주가 조회 |
| 시간외단일가요청 | ka10087 | 시간외 단일가 조회 |
| 프로그램매매추이요청 시간대별 | ka90005 | 프로그램매매추이 시간대별 조회 |
| 프로그램매매차익잔고추이요청 | ka90006 | 프로그램매매 차익잔고추이 조회 |
| 프로그램매매누적추이요청 | ka90007 | 프로그램매매 누적추이 조회 |
| 종목시간별프로그램매매추이요청 | ka90008 | 종목 시간별 프로그램매매추이 조회 |
| 프로그램매매추이요청 일자별 | ka90010 | 프로그램매매추이 일자별 조회 |
| 종목일별프로그램매매추이요청 | ka90013 | 종목 일별 프로그램매매추이 조회 |

---

### 주식호가요청 (ka10004)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명           | Type   | Required | Length | Description    |
| -------------------- | ---------------- | ------ | -------- | ------ | -------------- |
| bid_req_base_tm      | 호가잔량기준시간 | String | N        | 20     | 호가시간       |
| sel_10th_pre_req_pre | 매도10차선잔량대비 | String | N        | 20     | 매도호가직전대비10 |
| sel_10th_pre_req     | 매도10차선잔량   | String | N        | 20     | 매도호가수량10 |
| sel_10th_pre_bid     | 매도10차선호가   | String | N        | 20     | 매도호가10     |
| sel_9th_pre_req_pre  | 매도9차선잔량대비 | String | N        | 20     | 매도호가직전대비9 |
| sel_9th_pre_req      | 매도9차선잔량    | String | N        | 20     | 매도호가수량9  |
| sel_9th_pre_bid      | 매도9차선호가    | String | N        | 20     | 매도호가9      |
| sel_8th_pre_req_pre  | 매도8차선잔량대비 | String | N        | 20     | 매도호가직전대비8 |
| sel_8th_pre_req      | 매도8차선잔량    | String | N        | 20     | 매도호가수량8  |
| sel_8th_pre_bid      | 매도8차선호가    | String | N        | 20     | 매도호가8      |
| sel_7th_pre_req_pre  | 매도7차선잔량대비 | String | N        | 20     | 매도호가직전대비7 |
| sel_7th_pre_req      | 매도7차선잔량    | String | N        | 20     | 매도호가수량7  |
| sel_7th_pre_bid      | 매도7차선호가    | String | N        | 20     | 매도호가7      |
| sel_6th_pre_req_pre  | 매도6차선잔량대비 | String | N        | 20     | 매도호가직전대비6 |
| sel_6th_pre_req      | 매도6차선잔량    | String | N        | 20     | 매도호가수량6  |
| sel_6th_pre_bid      | 매도6차선호가    | String | N        | 20     | 매도호가6      |
| sel_5th_pre_req_pre  | 매도5차선잔량대비 | String | N        | 20     | 매도호가직전대비5 |
| sel_5th_pre_req      | 매도5차선잔량    | String | N        | 20     | 매도호가수량5  |
| sel_5th_pre_bid      | 매도5차선호가    | String | N        | 20     | 매도호가5      |
| sel_4th_pre_req_pre  | 매도4차선잔량대비 | String | N        | 20     | 매도호가직전대비4 |
| sel_4th_pre_req      | 매도4차선잔량    | String | N        | 20     | 매도호가수량4  |
| sel_4th_pre_bid      | 매도4차선호가    | String | N        | 20     | 매도호가4      |
| sel_3th_pre_req_pre  | 매도3차선잔량대비 | String | N        | 20     | 매도호가직전대비3 |
| sel_3th_pre_req      | 매도3차선잔량    | String | N        | 20     | 매도호가수량3  |
| sel_3th_pre_bid      | 매도3차선호가    | String | N        | 20     | 매도호가3      |
| sel_2th_pre_req_pre  | 매도2차선잔량대비 | String | N        | 20     | 매도호가직전대비2 |
| sel_2th_pre_req      | 매도2차선잔량    | String | N        | 20     | 매도호가수량2  |
| sel_2th_pre_bid      | 매도2차선호가    | String | N        | 20     | 매도호가2      |
| sel_1th_pre_req_pre  | 매도1차선잔량대비 | String | N        | 20     | 매도호가직전대비1 |
| sel_fpr_req          | 매도최우선잔량   | String | N        | 20     | 매도호가수량1  |
| sel_fpr_bid          | 매도최우선호가   | String | N        | 20     | 매도호가1      |
| buy_fpr_bid          | 매수최우선호가   | String | N        | 20     | 매수호가1      |
| buy_fpr_req          | 매수최우선잔량   | String | N        | 20     | 매수호가수량1  |
| buy_1th_pre_req_pre  | 매수1차선잔량대비 | String | N        | 20     | 매수호가직전대비1 |
| buy_2th_pre_bid      | 매수2차선호가    | String | N        | 20     | 매수호가2      |
| buy_2th_pre_req      | 매수2차선잔량    | String | N        | 20     | 매수호가수량2  |
| buy_2th_pre_req_pre  | 매수2차선잔량대비 | String | N        | 20     | 매수호가직전대비2 |
| buy_3th_pre_bid      | 매수3차선호가    | String | N        | 20     | 매수호가3      |
| buy_3th_pre_req      | 매수3차선잔량    | String | N        | 20     | 매수호가수량3  |
| buy_3th_pre_req_pre  | 매수3차선잔량대비 | String | N        | 20     | 매수호가직전대비3 |
| buy_4th_pre_bid      | 매수4차선호가    | String | N        | 20     | 매수호가4      |
| buy_4th_pre_req      | 매수4차선잔량    | String | N        | 20     | 매수호가수량4  |
| buy_4th_pre_req_pre  | 매수4차선잔량대비 | String | N        | 20     | 매수호가직전대비4 |
| buy_5th_pre_bid      | 매수5차선호가    | String | N        | 20     | 매수호가5      |
| buy_5th_pre_req      | 매수5차선잔량    | String | N        | 20     | 매수호가수량5  |
| buy_5th_pre_req_pre  | 매수5차선잔량대비 | String | N        | 20     | 매수호가직전대비5 |
| buy_6th_pre_bid      | 매수6차선호가    | String | N        | 20     | 매수호가6      |
| buy_6th_pre_req      | 매수6차선잔량    | String | N        | 20     | 매수호가수량6  |
| buy_6th_pre_req_pre  | 매수6차선잔량대비 | String | N        | 20     | 매수호가직전대비6 |
| buy_7th_pre_bid      | 매수7차선호가    | String | N        | 20     | 매수호가7      |
| buy_7th_pre_req      | 매수7차선잔량    | String | N        | 20     | 매수호가수량7  |
| buy_7th_pre_req_pre  | 매수7차선잔량대비 | String | N        | 20     | 매수호가직전대비7 |
| buy_8th_pre_bid      | 매수8차선호가    | String | N        | 20     | 매수호가8      |
| buy_8th_pre_req      | 매수8차선잔량    | String | N        | 20     | 매수호가수량8  |
| buy_8th_pre_req_pre  | 매수8차선잔량대비 | String | N        | 20     | 매수호가직전대비8 |
| buy_9th_pre_bid      | 매수9차선호가    | String | N        | 20     | 매수호가9      |
| buy_9th_pre_req      | 매수9차선잔량    | String | N        | 20     | 매수호가수량9  |
| buy_9th_pre_req_pre  | 매수9차선잔량대비 | String | N        | 20     | 매수호가직전대비9 |
| buy_10th_pre_bid     | 매수10차선호가   | String | N        | 20     | 매수호가10     |
| buy_10th_pre_req     | 매수10차선잔량   | String | N        | 20     | 매수호가수량10 |
| buy_10th_pre_req_pre | 매수10차선잔량대비 | String | N        | 20     | 매수호가직전대비10 |
| tot_sel_req_jub_pre  | 총매도잔량직전대비 | String | N        | 20     | 매도호가총잔량직전대비 |
| tot_sel_req          | 총매도잔량       | String | N        | 20     | 매도호가총잔량 |
| tot_buy_req          | 총매수잔량       | String | N        | 20     | 매수호가총잔량 |
| tot_buy_req_jub_pre  | 총매수잔량직전대비 | String | N        | 20     | 매수호가총잔량직전대비 |
| ovt_sel_req_pre      | 시간외매도잔량대비 | String | N        | 20     | 시간외 매도호가 총잔량 직전대비 |
| ovt_sel_req          | 시간외매도잔량   | String | N        | 20     | 시간외 매도호가 총잔량 |
| ovt_buy_req          | 시간외매수잔량   | String | N        | 20     | 시간외 매수호가 총잔량 |
| ovt_buy_req_pre      | 시간외매수잔량대비 | String | N        | 20     | 시간외 매수호가 총잔량 직전대비 |

#### 요청 예시

```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
    "bid_req_base_tm": "162000",
    "sel_10th_pre_req_pre": "0",
    "sel_10th_pre_req": "0",
    "sel_10th_pre_bid": "0",
    "sel_9th_pre_req_pre": "0",
    "sel_9th_pre_req": "0",
    "sel_9th_pre_bid": "0",
    "sel_8th_pre_req_pre": "0",
    "sel_8th_pre_req": "0",
    "sel_8th_pre_bid": "0",
    "sel_7th_pre_req_pre": "0",
    "sel_7th_pre_req": "0",
    "sel_7th_pre_bid": "0",
    "sel_6th_pre_req_pre": "0",
    "sel_6th_pre_req": "0",
    "sel_6th_pre_bid": "0",
    "sel_5th_pre_req_pre": "0",
    "sel_5th_pre_req": "0",
    "sel_5th_pre_bid": "0",
    "sel_4th_pre_req_pre": "0",
    "sel_4th_pre_req": "0",
    "sel_4th_pre_bid": "0",
    "sel_3th_pre_req_pre": "0",
    "sel_3th_pre_req": "0",
    "sel_3th_pre_bid": "0",
    "sel_2th_pre_req_pre": "0",
    "sel_2th_pre_req": "0",
    "sel_2th_pre_bid": "0",
    "sel_1th_pre_req_pre": "0",
    "sel_fpr_req": "0",
    "sel_fpr_bid": "0",
    "buy_fpr_bid": "0",
    "buy_fpr_req": "0",
    "buy_1th_pre_req_pre": "0",
    "buy_2th_pre_bid": "0",
    "buy_2th_pre_req": "0",
    "buy_2th_pre_req_pre": "0",
    "buy_3th_pre_bid": "0",
    "buy_3th_pre_req": "0",
    "buy_3th_pre_req_pre": "0",
    "buy_4th_pre_bid": "0",
    "buy_4th_pre_req": "0",
    "buy_4th_pre_req_pre": "0",
    "buy_5th_pre_bid": "0",
    "buy_5th_pre_req": "0",
    "buy_5th_pre_req_pre": "0",
    "buy_6th_pre_bid": "0",
    "buy_6th_pre_req": "0",
    "buy_6th_pre_req_pre": "0",
    "buy_7th_pre_bid": "0",
    "buy_7th_pre_req": "0",
    "buy_7th_pre_req_pre": "0",
    "buy_8th_pre_bid": "0",
    "buy_8th_pre_req": "0",
    "buy_8th_pre_req_pre": "0",
    "buy_9th_pre_bid": "0",
    "buy_9th_pre_req": "0",
    "buy_9th_pre_req_pre": "0",
    "buy_10th_pre_bid": "0",
    "buy_10th_pre_req": "0",
    "buy_10th_pre_req_pre": "0",
    "tot_sel_req_jub_pre": "0",
    "tot_sel_req": "0",
    "tot_buy_req": "0",
    "tot_buy_req_jub_pre": "0",
    "ovt_sel_req_pre": "0",
    "ovt_sel_req": "0",
    "ovt_buy_req": "0",
    "ovt_buy_req_pre": "0",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 주식일주월시분요청 (ka10005)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명         | Type   | Required | Length | Description |
| -------------- | -------------- | ------ | -------- | ------ | ----------- |
| stk_ddwkmm     | 주식일주월시분 | LIST   | N        |        |             |
| - date         | 날짜           | String | N        | 20     |             |
| - open_pric    | 시가           | String | N        | 20     |             |
| - high_pric    | 고가           | String | N        | 20     |             |
| - low_pric     | 저가           | String | N        | 20     |             |
| - close_pric   | 종가           | String | N        | 20     |             |
| - pre          | 대비           | String | N        | 20     |             |
| - flu_rt       | 등락률         | String | N        | 20     |             |
| - trde_qty     | 거래량         | String | N        | 20     |             |
| - trde_prica   | 거래대금       | String | N        | 20     |             |
| - for_poss     | 외인보유       | String | N        | 20     |             |
| - for_wght     | 외인비중       | String | N        | 20     |             |
| - for_netprps  | 외인순매수     | String | N        | 20     |             |
| - orgn_netprps | 기관순매수     | String | N        | 20     |             |
| - ind_netprps  | 개인순매수     | String | N        | 20     |             |
| - crd_remn_rt  | 신용잔고율     | String | N        | 20     |             |
| - frgn         | 외국계         | String | N        | 20     |             |
| - prm          | 프로그램       | String | N        | 20     |             |

#### 요청 예시
```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시
```json
{
    "stk_ddwkmm": [
        {
            "date": "20241028",
            "open_pric": "95400",
            "high_pric": "95400",
            "low_pric": "95400",
            "close_pric": "95400",
            "pre": "0",
            "flu_rt": "0.00",
            "trde_qty": "0",
            "trde_prica": "0",
            "cntr_str": "0.00",
            "for_poss": "+26.07",
            "for_wght": "+26.07",
            "for_netprps": "0",
            "orgn_netprps": "",
            "ind_netprps": "",
            "frgn": "",
            "crd_remn_rt": "",
            "prm": ""
        },
        {
            "date": "20241025",
            "open_pric": "95400",
            "high_pric": "95400",
            "low_pric": "95400",
            "close_pric": "95400",
            "pre": "",
            "flu_rt": "",
            "trde_qty": "0",
            "trde_prica": "",
            "cntr_str": "",
            "for_poss": "",
            "for_wght": "",
            "for_netprps": "",
            "orgn_netprps": "",
            "ind_netprps": "",
            "frgn": "",
            "crd_remn_rt": "",
            "prm": ""
        },
        {
            "date": "20241024",
            "open_pric": "94300",
            "high_pric": "95400",
            "low_pric": "94300",
            "close_pric": "+95400",
            "pre": "",
            "flu_rt": "",
            "trde_qty": "70",
            "trde_prica": "",
            "cntr_str": "",
            "for_poss": "",
            "for_wght": "",
            "for_netprps": "",
            "orgn_netprps": "",
            "ind_netprps": "",
            "frgn": "",
            "crd_remn_rt": "",
            "prm": ""
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```---

### 주식시분요청 (ka10006)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| date | 날짜 | String | N | 20 | |
| open_pric | 시가 | String | N | 20 | |
| high_pric | 고가 | String | N | 20 | |
| low_pric | 저가 | String | N | 20 | |
| close_pric | 종가 | String | N | 20 | |
| pre | 대비 | String | N | 20 | |
| flu_rt | 등락률 | String | N | 20 | |
| trde_qty | 거래량 | String | N | 20 | |
| trde_prica | 거래대금 | String | N | 20 | |
| cntr_str | 체결강도 | String | N | 20 | |

#### 요청 예시
```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시
```json
{
    "date": "20241105",
    "open_pric": "0",
    "high_pric": "0",
    "low_pric": "0",
    "close_pric": "135300",
    "pre": "0",
    "flu_rt": "0.00",
    "trde_qty": "0",
    "trde_prica": "0",
    "cntr_str": "0.00",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 시세표성정보요청 (ka10007)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_nm | 종목명 | String | N | 20 | |
| stk_cd | 종목코드 | String | N | 6 | |
| date | 날짜 | String | N | 20 | |
| tm | 시간 | String | N | 20 | |
| pred_close_pric | 전일종가 | String | N | 20 | |
| pred_trde_qty | 전일거래량 | String | N | 20 | |
| upl_pric | 상한가 | String | N | 20 | |
| lst_pric | 하한가 | String | N | 20 | |
| pred_trde_prica | 전일거래대금 | String | N | 20 | |
| flo_stkcnt | 상장주식수 | String | N | 20 | |
| cur_prc | 현재가 | String | N | 20 | |
| smbol | 부호 | String | N | 20 | |
| flu_rt | 등락률 | String | N | 20 | |
| pred_rt | 전일비 | String | N | 20 | |
| open_pric | 시가 | String | N | 20 | |
| high_pric | 고가 | String | N | 20 | |
| low_pric | 저가 | String | N | 20 | |
| cntr_qty | 체결량 | String | N | 20 | |
| trde_qty | 거래량 | String | N | 20 | |
| trde_prica | 거래대금 | String | N | 20 | |
| exp_cntr_pric | 예상체결가 | String | N | 20 | |
| exp_cntr_qty | 예상체결량 | String | N | 20 | |
| exp_sel_pri_bid | 예상매도우선호가 | String | N | 20 | |
| exp_buy_pri_bid | 예상매수우선호가 | String | N | 20 | |
| trde_strt_dt | 거래시작일 | String | N | 20 | |
| exec_pric | 행사가격 | String | N | 20 | |
| hgst_pric | 최고가 | String | N | 20 | |
| lwst_pric | 최저가 | String | N | 20 | |
| hgst_pric_dt | 최고가일 | String | N | 20 | |
| lwst_pric_dt | 최저가일 | String | N | 20 | |
| sel_1bid | 매도1호가 | String | N | 20 | |
| sel_2bid | 매도2호가 | String | N | 20 | |
| sel_3bid | 매도3호가 | String | N | 20 | |
| sel_4bid | 매도4호가 | String | N | 20 | |
| sel_5bid | 매도5호가 | String | N | 20 | |
| sel_6bid | 매도6호가 | String | N | 20 | |
| sel_7bid | 매도7호가 | String | N | 20 | |
| sel_8bid | 매도8호가 | String | N | 20 | |
| sel_9bid | 매도9호가 | String | N | 20 | |
| sel_10bid | 매도10호가 | String | N | 20 | |
| buy_1bid | 매수1호가 | String | N | 20 | |
| buy_2bid | 매수2호가 | String | N | 20 | |
| buy_3bid | 매수3호가 | String | N | 20 | |
| buy_4bid | 매수4호가 | String | N | 20 | |
| buy_5bid | 매수5호가 | String | N | 20 | |
| buy_6bid | 매수6호가 | String | N | 20 | |
| buy_7bid | 매수7호가 | String | N | 20 | |
| buy_8bid | 매수8호가 | String | N | 20 | |
| buy_9bid | 매수9호가 | String | N | 20 | |
| buy_10bid | 매수10호가 | String | N | 20 | |
| sel_1bid_req | 매도1호가잔량 | String | N | 20 | |
| sel_2bid_req | 매도2호가잔량 | String | N | 20 | |
| sel_3bid_req | 매도3호가잔량 | String | N | 20 | |
| sel_4bid_req | 매도4호가잔량 | String | N | 20 | |
| sel_5bid_req | 매도5호가잔량 | String | N | 20 | |
| sel_6bid_req | 매도6호가잔량 | String | N | 20 | |
| sel_7bid_req | 매도7호가잔량 | String | N | 20 | |
| sel_8bid_req | 매도8호가잔량 | String | N | 20 | |
| sel_9bid_req | 매도9호가잔량 | String | N | 20 | |
| sel_10bid_req | 매도10호가잔량 | String | N | 20 | |
| buy_1bid_req | 매수1호가잔량 | String | N | 20 | |
| buy_2bid_req | 매수2호가잔량 | String | N | 20 | |
| buy_3bid_req | 매수3호가잔량 | String | N | 20 | |
| buy_4bid_req | 매수4호가잔량 | String | N | 20 | |
| buy_5bid_req | 매수5호가잔량 | String | N | 20 | |
| buy_6bid_req | 매수6호가잔량 | String | N | 20 | |
| buy_7bid_req | 매수7호가잔량 | String | N | 20 | |
| buy_8bid_req | 매수8호가잔량 | String | N | 20 | |
| buy_9bid_req | 매수9호가잔량 | String | N | 20 | |
| buy_10bid_req | 매수10호가잔량 | String | N | 20 | |
| sel_1bid_jub_pre | 매도1호가직전대비 | String | N | 20 | |
| sel_2bid_jub_pre | 매도2호가직전대비 | String | N | 20 | |
| sel_3bid_jub_pre | 매도3호가직전대비 | String | N | 20 | |
| sel_4bid_jub_pre | 매도4호가직전대비 | String | N | 20 | |
| sel_5bid_jub_pre | 매도5호가직전대비 | String | N | 20 | |
| sel_6bid_jub_pre | 매도6호가직전대비 | String | N | 20 | |
| sel_7bid_jub_pre | 매도7호가직전대비 | String | N | 20 | |
| sel_8bid_jub_pre | 매도8호가직전대비 | String | N | 20 | |
| sel_9bid_jub_pre | 매도9호가직전대비 | String | N | 20 | |
| sel_10bid_jub_pre | 매도10호가직전대비 | String | N | 20 | |
| buy_1bid_jub_pre | 매수1호가직전대비 | String | N | 20 | |
| buy_2bid_jub_pre | 매수2호가직전대비 | String | N | 20 | |
| buy_3bid_jub_pre | 매수3호가직전대비 | String | N | 20 | |
| buy_4bid_jub_pre | 매수4호가직전대비 | String | N | 20 | |
| buy_5bid_jub_pre | 매수5호가직전대비 | String | N | 20 | |
| buy_6bid_jub_pre | 매수6호가직전대비 | String | N | 20 | |
| buy_7bid_jub_pre | 매수7호가직전대비 | String | N | 20 | |
| buy_8bid_jub_pre | 매수8호가직전대비 | String | N | 20 | |
| buy_9bid_jub_pre | 매수9호가직전대비 | String | N | 20 | |
| buy_10bid_jub_pre | 매수10호가직전대비 | String | N | 20 | |
| sel_1bid_cnt | 매도1호가건수 | String | N | 20 | |
| sel_2bid_cnt | 매도2호가건수 | String | N | 20 | |
| sel_3bid_cnt | 매도3호가건수 | String | N | 20 | |
| sel_4bid_cnt | 매도4호가건수 | String | N | 20 | |
| sel_5bid_cnt | 매도5호가건수 | String | N | 20 | |
| buy_1bid_cnt | 매수1호가건수 | String | N | 20 | |
| buy_2bid_cnt | 매수2호가건수 | String | N | 20 | |
| buy_3bid_cnt | 매수3호가건수 | String | N | 20 | |
| buy_4bid_cnt | 매수4호가건수 | String | N | 20 | |
| buy_5bid_cnt | 매수5호가건수 | String | N | 20 | |
| lpsel_1bid_req | LP매도1호가잔량 | String | N | 20 | |
| lpsel_2bid_req | LP매도2호가잔량 | String | N | 20 | |
| lpsel_3bid_req | LP매도3호가잔량 | String | N | 20 | |
| lpsel_4bid_req | LP매도4호가잔량 | String | N | 20 | |
| lpsel_5bid_req | LP매도5호가잔량 | String | N | 20 | |
| lpsel_6bid_req | LP매도6호가잔량 | String | N | 20 | |
| lpsel_7bid_req | LP매도7호가잔량 | String | N | 20 | |
| lpsel_8bid_req | LP매도8호가잔량 | String | N | 20 | |
| lpsel_9bid_req | LP매도9호가잔량 | String | N | 20 | |
| lpsel_10bid_req | LP매도10호가잔량 | String | N | 20 | |
| lpbuy_1bid_req | LP매수1호가잔량 | String | N | 20 | |
| lpbuy_2bid_req | LP매수2호가잔량 | String | N | 20 | |
| lpbuy_3bid_req | LP매수3호가잔량 | String | N | 20 | |
| lpbuy_4bid_req | LP매수4호가잔량 | String | N | 20 | |
| lpbuy_5bid_req | LP매수5호가잔량 | String | N | 20 | |
| lpbuy_6bid_req | LP매수6호가잔량 | String | N | 20 | |
| lpbuy_7bid_req | LP매수7호가잔량 | String | N | 20 | |
| lpbuy_8bid_req | LP매수8호가잔량 | String | N | 20 | |
| lpbuy_9bid_req | LP매수9호가잔량 | String | N | 20 | |
| lpbuy_10bid_req | LP매수10호가잔량 | String | N | 20 | |
| tot_buy_req | 총매수잔량 | String | N | 20 | |
| tot_sel_req | 총매도잔량 | String | N | 20 | |
| tot_buy_cnt | 총매수건수 | String | N | 20 | |
| tot_sel_cnt | 총매도건수 | String | N | 20 | |

#### 요청 예시
```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시
```json
{
    "stk_nm": "삼성전자",
    "stk_cd": "005930",
    "date": "20241105",
    "tm": "104000",
    "pred_close_pric": "135300",
    "pred_trde_qty": "88862",
    "upl_pric": "+175800",
    "lst_pric": "-94800",
    "pred_trde_prica": "11963",
    "flo_stkcnt": "25527",
    "cur_prc": "135300",
    "smbol": "3",
    "flu_rt": "0.00",
    "pred_rt": "0.00",
    "open_pric": "0",
    "high_pric": "0",
    "low_pric": "0",
    "cntr_qty": "",
    "trde_qty": "0",
    "trde_prica": "0",
    "exp_cntr_pric": "-0",
    "exp_cntr_qty": "0",
    "exp_sel_pri_bid": "0",
    "exp_buy_pri_bid": "0",
    "trde_strt_dt": "00000000",
    "exec_pric": "0",
    "hgst_pric": "",
    "lwst_pric": "",
    "hgst_pric_dt": "",
    "lwst_pric_dt": "",
    "sel_1bid": "0",
    "sel_2bid": "0",
    "sel_3bid": "0",
    "sel_4bid": "0",
    "sel_5bid": "0",
    "sel_6bid": "0",
    "sel_7bid": "0",
    "sel_8bid": "0",
    "sel_9bid": "0",
    "sel_10bid": "0",
    "buy_1bid": "0",
    "buy_2bid": "0",
    "buy_3bid": "0",
    "buy_4bid": "0",
    "buy_5bid": "0",
    "buy_6bid": "0",
    "buy_7bid": "0",
    "buy_8bid": "0",
    "buy_9bid": "0",
    "buy_10bid": "0",
    "sel_1bid_req": "0",
    "sel_2bid_req": "0",
    "sel_3bid_req": "0",
    "sel_4bid_req": "0",
    "sel_5bid_req": "0",
    "sel_6bid_req": "0",
    "sel_7bid_req": "0",
    "sel_8bid_req": "0",
    "sel_9bid_req": "0",
    "sel_10bid_req": "0",
    "buy_1bid_req": "0",
    "buy_2bid_req": "0",
    "buy_3bid_req": "0",
    "buy_4bid_req": "0",
    "buy_5bid_req": "0",
    "buy_6bid_req": "0",
    "buy_7bid_req": "0",
    "buy_8bid_req": "0",
    "buy_9bid_req": "0",
    "buy_10bid_req": "0",
    "sel_1bid_jub_pre": "0",
    "sel_2bid_jub_pre": "0",
    "sel_3bid_jub_pre": "0",
    "sel_4bid_jub_pre": "0",
    "sel_5bid_jub_pre": "0",
    "sel_6bid_jub_pre": "0",
    "sel_7bid_jub_pre": "0",
    "sel_8bid_jub_pre": "0",
    "sel_9bid_jub_pre": "0",
    "sel_10bid_jub_pre": "0",
    "buy_1bid_jub_pre": "0",
    "buy_2bid_jub_pre": "0",
    "buy_3bid_jub_pre": "0",
    "buy_4bid_jub_pre": "0",
    "buy_5bid_jub_pre": "0",
    "buy_6bid_jub_pre": "0",
    "buy_7bid_jub_pre": "0",
    "buy_8bid_jub_pre": "0",
    "buy_9bid_jub_pre": "0",
    "buy_10bid_jub_pre": "0",
    "sel_1bid_cnt": "",
    "sel_2bid_cnt": "",
    "sel_3bid_cnt": "",
    "sel_4bid_cnt": "",
    "sel_5bid_cnt": "",
    "buy_1bid_cnt": "",
    "buy_2bid_cnt": "",
    "buy_3bid_cnt": "",
    "buy_4bid_cnt": "",
    "buy_5bid_cnt": "",
    "lpsel_1bid_req": "0",
    "lpsel_2bid_req": "0",
    "lpsel_3bid_req": "0",
    "lpsel_4bid_req": "0",
    "lpsel_5bid_req": "0",
    "lpsel_6bid_req": "0",
    "lpsel_7bid_req": "0",
    "lpsel_8bid_req": "0",
    "lpsel_9bid_req": "0",
    "lpsel_10bid_req": "0",
    "lpbuy_1bid_req": "0",
    "lpbuy_2bid_req": "0",
    "lpbuy_3bid_req": "0",
    "lpbuy_4bid_req": "0",
    "lpbuy_5bid_req": "0",
    "lpbuy_6bid_req": "0",
    "lpbuy_7bid_req": "0",
    "lpbuy_8bid_req": "0",
    "lpbuy_9bid_req": "0",
    "lpbuy_10bid_req": "0",
    "tot_buy_req": "0",
    "tot_sel_req": "0",
    "tot_buy_cnt": "",
    "tot_sel_cnt": "0",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 신주인수권전체시세요청 (ka10011)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| newstk_recvrht_tp | 신주인수권구분 | String | Y | 20 | 00:전체, 05:신주인수권증권, 07:신주인수권증서 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| newstk_recvrht_mrpr | 신주인수권시세 | LIST | N | | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pred_pre_sig | 전일대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - fpr_sel_bid | 최우선매도호가 | String | N | 20 | |
| - fpr_buy_bid | 최우선매수호가 | String | N | 20 | |
| - acc_trde_qty | 누적거래량 | String | N | 20 | |
| - open_pric | 시가 | String | N | 20 | |
| - high_pric | 고가 | String | N | 20 | |
| - low_pric | 저가 | String | N | 20 | |

#### 요청 예시
```json
{
    "newstk_recvrht_tp": "00"
}
```

#### 응답 예시
```json
{
    "newstk_recvrht_mrpr": [
        {
            "stk_cd": "J0036221D",
            "stk_nm": "KG모빌리티 122WR",
            "cur_prc": "988",
            "pred_pre_sig": "3",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "fpr_sel_bid": "-0",
            "fpr_buy_bid": "-0",
            "acc_trde_qty": "0",
            "open_pric": "-0",
            "high_pric": "-0",
            "low_pric": "-0"
        },
        {
            "stk_cd": "J00532219",
            "stk_nm": "온타이드 9WR",
            "cur_prc": "12",
            "pred_pre_sig": "3",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "fpr_sel_bid": "-0",
            "fpr_buy_bid": "-0",
            "acc_trde_qty": "0",
            "open_pric": "-0",
            "high_pric": "-0",
            "low_pric": "-0"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 일별기관매매종목요청 (ka10044)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |
| trde_tp | 매매구분 | String | Y | 1 | 1:순매도, 2:순매수 |
| mrkt_tp | 시장구분 | String | Y | 3 | 001:코스피, 101:코스닥 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| daly_orgn_trde_stk | 일별기관매매종목 | LIST | N | | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - netprps_qty | 순매수수량 | String | N | 20 | |
| - netprps_amt | 순매수금액 | String | N | 20 | |

#### 요청 예시
```json
{
    "strt_dt": "20241106",
    "end_dt": "20241107",
    "trde_tp": "1",
    "mrkt_tp": "001",
    "stex_tp": "3"
}
```

#### 응답 예시
```json
{
    "daly_orgn_trde_stk": [
        {
            "stk_cd": "005930",
            "stk_nm": "삼성전자",
            "netprps_qty": "-0",
            "netprps_amt": "-1",
            "prsm_avg_pric": "140000",
            "cur_prc": "-95100",
            "avg_pric_pre": "--44900",
            "pre_rt": "-32.07"
        },
        {
            "stk_cd": "005930",
            "stk_nm": "삼성전자",
            "netprps_qty": "-0",
            "netprps_amt": "-0",
            "prsm_avg_pric": "12000",
            "cur_prc": "9920",
            "avg_pric_pre": "--2080",
            "pre_rt": "-17.33"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 종목별기관매매추이요청 (ka10045)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |
| orgn_prsm_unp_tp | 기관추정단가구분 | String | Y | 1 | 1:매수단가, 2:매도단가 |
| for_prsm_unp_tp | 외인추정단가구분 | String | Y | 1 | 1:매수단가, 2:매도단가 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| orgn_prsm_avg_pric | 기관추정평균가 | String | N | | |
| for_prsm_avg_pric | 외인추정평균가 | String | N | | |
| stk_orgn_trde_trnsn | 종목별기관매매추이 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - close_pric | 종가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - orgn_dt_acc | 기관기간누적 | String | N | 20 | |
| - orgn_daly_nettrde_qty | 기관일별순매매수량 | String | N | 20 | |
| - for_dt_acc | 외인기간누적 | String | N | 20 | |
| - for_daly_nettrde_qty | 외인일별순매매수량 | String | N | 20 | |
| - limit_exh_rt | 한도소진율 | String | N | 20 | |

#### 요청 예시
```json
{
    "stk_cd": "005930",
    "strt_dt": "20241007",
    "end_dt": "20241107",
    "orgn_prsm_unp_tp": "1",
    "for_prsm_unp_tp": "1"
}
```

#### 응답 예시
```json
{
    "orgn_prsm_avg_pric": "117052",
    "for_prsm_avg_pric": "0",
    "stk_orgn_trde_trnsn": [
        {
            "dt": "20241107",
            "close_pric": "133600",
            "pre_sig": "0",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "trde_qty": "0",
            "orgn_dt_acc": "158",
            "orgn_daly_nettrde_qty": "0",
            "for_dt_acc": "28315",
            "for_daly_nettrde_qty": "0",
            "limit_exh_rt": "+26.14"
        },
        {
            "dt": "20241106",
            "close_pric": "-132500",
            "pre_sig": "5",
            "pred_pre": "-600",
            "flu_rt": "-0.45",
            "trde_qty": "43",
            "orgn_dt_acc": "158",
            "orgn_daly_nettrde_qty": "0",
            "for_dt_acc": "28315",
            "for_daly_nettrde_qty": "11243",
            "limit_exh_rt": "+26.14"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 체결강도추이시간별요청 (ka10046)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cntr_str_tm | 체결강도시간별 | LIST | N | | |
| - cntr_tm | 체결시간 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - pred_pre_sig | 전일대비기호 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - acc_trde_prica | 누적거래대금 | String | N | 20 | |
| - acc_trde_qty | 누적거래량 | String | N | 20 | |
| - cntr_str | 체결강도 | String | N | 20 | |
| - cntr_str_5min | 체결강도5분 | String | N | 20 | |
| - cntr_str_20min | 체결강도20분 | String | N | 20 | |
| - cntr_str_60min | 체결강도60분 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | |
---

### 체결강도추이일별요청 (ka10047)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cntr_str_daly | 체결강도일별 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - pred_pre_sig | 전일대비기호 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - acc_trde_prica | 누적거래대금 | String | N | 20 | |
| - acc_trde_qty | 누적거래량 | String | N | 20 | |
| - cntr_str | 체결강도 | String | N | 20 | |
| - cntr_str_5min | 체결강도5일 | String | N | 20 | |
| - cntr_str_20min | 체결강도20일 | String | N | 20 | |
| - cntr_str_60min | 체결강도60일 | String | N | 20 | |

#### 요청 예시
```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시
```json
{
    "cntr_str_daly": [
        {
            "dt": "20241128",
            "cur_prc": "+219000",
            "pred_pre": "+14000",
            "pred_pre_sig": "2",
            "flu_rt": "+6.83",
            "trde_qty": "",
            "acc_trde_prica": "2",
            "acc_trde_qty": "8",
            "cntr_str": "0.00",
            "cntr_str_5min": "201.54",
            "cntr_str_20min": "139.37",
            "cntr_str_60min": "172.06"
        },
        {
            "dt": "20241127",
            "cur_prc": "+205000",
            "pred_pre": "+40300",
            "pred_pre_sig": "2",
            "flu_rt": "+24.47",
            "trde_qty": "",
            "acc_trde_prica": "9",
            "acc_trde_qty": "58",
            "cntr_str": "0.00",
            "cntr_str_5min": "209.54",
            "cntr_str_20min": "139.37",
            "cntr_str_60min": "180.40"
        },
        {
            "dt": "20241126",
            "cur_prc": "+164700",
            "pred_pre": "+38000",
            "pred_pre_sig": "1",
            "flu_rt": "+29.99",
            "trde_qty": "",
            "acc_trde_prica": "2",
            "acc_trde_qty": "15",
            "cntr_str": "7.69",
            "cntr_str_5min": "309.54",
            "cntr_str_20min": "164.37",
            "cntr_str_60min": "188.73"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 장중투자자별매매요청 (ka10063)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| mrkt_tp | 시장구분 | String | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액, 2:수량 |
| invsr | 투자자별 | String | Y | 1 | 6:외국인, 7:기관계, 1:투신, 0:보험, 2:은행, 3:연기금, 4:국가, 5:기타법인 |
| frgn_all | 외국계전체 | String | Y | 1 | 1:체크, 0:미체크 |
| smtm_netprps_tp | 동시순매수구분 | String | Y | 1 | 1:체크, 0:미체크 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| opmr_invsr_trde | 장중투자자별매매 | LIST | N | | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - acc_trde_qty | 누적거래량 | String | N | 20 | |
| - netprps_qty | 순매수수량 | String | N | 20 | |
| - prev_pot_netprps_qty | 이전시점순매수수량 | String | N | 20 | |
| - netprps_irds | 순매수증감 | String | N | 20 | |
| - buy_qty | 매수수량 | String | N | 20 | |
| - buy_qty_irds | 매수수량증감 | String | N | 20 | |
| - sell_qty | 매도수량 | String | N | 20 | |
| - sell_qty_irds | 매도수량증감 | String | N | 20 | |
---

### 장마감후투자자별매매요청 (ka10066)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| mrkt_tp | 시장구분 | String | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액, 2:수량 |
| trde_tp | 매매구분 | String | Y | 1 | 0:순매수, 1:매수, 2:매도 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| opaf_invsr_trde | 장중투자자별매매차트 | LIST | N | | |
| - stk_cd | 종목코드 | String | N | 20 | |
| - stk_nm | 종목명 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - ind_invsr | 개인투자자 | String | N | 20 | |
| - frgnr_invsr | 외국인투자자 | String | N | 20 | |
| - orgn | 기관계 | String | N | 20 | |
| - fnnc_invt | 금융투자 | String | N | 20 | |
| - insrnc | 보험 | String | N | 20 | |
| - invtrt | 투신 | String | N | 20 | |
| - etc_fnnc | 기타금융 | String | N | 20 | |
| - bank | 은행 | String | N | 20 | |
| - penfnd_etc | 연기금등 | String | N | 20 | |
| - samo_fund | 사모펀드 | String | N | 20 | |
| - natn | 국가 | String | N | 20 | |
| - etc_corp | 기타법인 | String | N | 20 | |

#### 요청 예시
```json
{
    "mrkt_tp": "000",
    "amt_qty_tp": "1",
    "trde_tp": "0",
    "stex_tp": "3"
}
```

#### 응답 예시
```json
{
    "opaf_invsr_trde": [
        {
            "stk_cd": "005930",
            "stk_nm": "삼성전자",
            "cur_prc": "-7410",
            "pre_sig": "5",
            "pred_pre": "-50",
            "flu_rt": "-0.67",
            "trde_qty": "8",
            "ind_invsr": "0",
            "frgnr_invsr": "0",
            "orgn": "0",
            "fnnc_invt": "0",
            "insrnc": "0",
            "invtrt": "0",
            "etc_fnnc": "0",
            "bank": "0",
            "penfnd_etc": "0",
            "samo_fund": "0",
            "natn": "0",
            "etc_corp": "0"
        },
        {
            "stk_cd": "005930",
            "stk_nm": "삼성전자",
            "cur_prc": "542",
            "pre_sig": "3",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "trde_qty": "0",
            "ind_invsr": "0",
            "frgnr_invsr": "0",
            "orgn": "0",
            "fnnc_invt": "0",
            "insrnc": "0",
            "invtrt": "0",
            "etc_fnnc": "0",
            "bank": "0",
            "penfnd_etc": "0",
            "samo_fund": "0",
            "natn": "0",
            "etc_corp": "0"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 증권사별종목매매동향요청 (ka10078)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| mmcm_cd | 회원사코드 | String | Y | 3 | 회원사 코드는 ka10102 조회 |
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| strt_dt | 시작일자 | String | Y | 8 | YYYYMMDD |
| end_dt | 종료일자 | String | Y | 8 | YYYYMMDD |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| sec_stk_trde_trend | 증권사별종목매매동향 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - acc_trde_qty | 누적거래량 | String | N | 20 | |
| - netprps_qty | 순매수수량 | String | N | 20 | |
| - buy_qty | 매수수량 | String | N | 20 | |
| - sell_qty | 매도수량 | String | N | 20 | |

#### 요청 예시
```json
{
    "mmcm_cd": "001",
    "stk_cd": "005930",
    "strt_dt": "20241106",
    "end_dt": "20241107"
}
```

#### 응답 예시
```json
{
    "sec_stk_trde_trend": [
        {
            "dt": "20241107",
            "cur_prc": "10050",
            "pre_sig": "0",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "acc_trde_qty": "0",
            "netprps_qty": "0",
            "buy_qty": "0",
            "sell_qty": "0"
        },
        {
            "dt": "20241106",
            "cur_prc": "10240",
            "pre_sig": "0",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "acc_trde_qty": "0",
            "netprps_qty": "-1016",
            "buy_qty": "951",
            "sell_qty": "1967"
        },
        {
            "dt": "20241105",
            "cur_prc": "10040",
            "pre_sig": "0",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "acc_trde_qty": "0",
            "netprps_qty": "2016",
            "buy_qty": "5002",
            "sell_qty": "2986"
        },
        {
            "dt": "20241101",
            "cur_prc": "-5880",
            "pre_sig": "4",
            "pred_pre": "-2520",
            "flu_rt": "-30.00",
            "acc_trde_qty": "16139969",
            "netprps_qty": "-532",
            "buy_qty": "2454",
            "sell_qty": "2986"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 일별주가요청 (ka10086)

> **주의사항**: 외국인순매수 데이터는 거래소로부터 금액데이터가 제공되지 않고 수량으로만 조회됩니다.

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| qry_dt | 조회일자 | String | Y | 8 | YYYYMMDD |
| indc_tp | 표시구분 | String | Y | 1 | 0:수량, 1:금액(백만원) |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| daly_stkpc | 일별주가 | LIST | N | | |
| - date | 날짜 | String | N | 20 | |
| - open_pric | 시가 | String | N | 20 | |
| - high_pric | 고가 | String | N | 20 | |
| - low_pric | 저가 | String | N | 20 | |
| - close_pric | 종가 | String | N | 20 | |
| - pred_rt | 전일비 | String | N | 20 | |
| - flu_rt | 등락률 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - amt_mn | 금액(백만) | String | N | 20 | |
| - crd_rt | 신용비 | String | N | 20 | |
| - ind | 개인 | String | N | 20 | |
| - orgn | 기관 | String | N | 20 | |
| - for_qty | 외인수량 | String | N | 20 | |
| - frgn | 외국계 | String | N | 20 | |
| - prm | 프로그램 | String | N | 20 | |
| - for_rt | 외인비 | String | N | 20 | |
| - for_poss | 외인보유 | String | N | 20 | |
| - for_wght | 외인비중 | String | N | 20 | |
| - for_netprps | 외인순매수 | String | N | 20 | |
| - orgn_netprps | 기관순매수 | String | N | 20 | |
| - ind_netprps | 개인순매수 | String | N | 20 | |
| - crd_remn_rt | 신용잔고율 | String | N | 20 | |

#### 요청 예시
```json
{
    "stk_cd": "005930",
    "qry_dt": "20241125",
    "indc_tp": "0"
}
```

#### 응답 예시
```json
{
    "daly_stkpc": [
        {
            "date": "20241125",
            "open_pric": "+78800",
            "high_pric": "+101100",
            "low_pric": "-54500",
            "close_pric": "-55000",
            "pred_rt": "-22800",
            "flu_rt": "-29.31",
            "trde_qty": "20278",
            "amt_mn": "1179",
            "crd_rt": "0.00",
            "ind": "--714",
            "orgn": "+693",
            "for_qty": "--266783",
            "frgn": "0",
            "prm": "0",
            "for_rt": "+51.56",
            "for_poss": "+51.56",
            "for_wght": "+51.56",
            "for_netprps": "--266783",
            "orgn_netprps": "+693",
            "ind_netprps": "--714",
            "crd_remn_rt": "0.00"
        },
        {
            "date": "20241122",
            "open_pric": "-54500",
            "high_pric": "77800",
            "low_pric": "-54500",
            "close_pric": "77800",
            "pred_rt": "0",
            "flu_rt": "0.00",
            "trde_qty": "209653",
            "amt_mn": "11447",
            "crd_rt": "0.00",
            "ind": "--196415",
            "orgn": "+196104",
            "for_qty": "--2965929",
            "frgn": "0",
            "prm": "--6",
            "for_rt": "+51.56",
            "for_poss": "+51.56",
            "for_wght": "+51.56",
            "for_netprps": "--2965929",
            "orgn_netprps": "+196104",
            "ind_netprps": "--196415",
            "crd_remn_rt": "0.00"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 시간외단일가요청 (ka10087)

> **주의사항**: 호가잔량기준시간은 시간외거래에 대한 시간이 아닌 정규장시간 값입니다.

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_cd | 종목코드 | String | Y | 6 | |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| bid_req_base_tm | 호가잔량기준시간 | String | N | | |
| ovt_sigpric_sel_bid_jub_pre_5 | 시간외단일가_매도호가직전대비5 | String | N | | |
| ovt_sigpric_sel_bid_jub_pre_4 | 시간외단일가_매도호가직전대비4 | String | N | | |
| ovt_sigpric_sel_bid_jub_pre_3 | 시간외단일가_매도호가직전대비3 | String | N | | |
| ovt_sigpric_sel_bid_jub_pre_2 | 시간외단일가_매도호가직전대비2 | String | N | | |
| ovt_sigpric_sel_bid_jub_pre_1 | 시간외단일가_매도호가직전대비1 | String | N | | |
| ovt_sigpric_sel_bid_qty_5 | 시간외단일가_매도호가수량5 | String | N | | |
| ovt_sigpric_sel_bid_qty_4 | 시간외단일가_매도호가수량4 | String | N | | |
| ovt_sigpric_sel_bid_qty_3 | 시간외단일가_매도호가수량3 | String | N | | |
| ovt_sigpric_sel_bid_qty_2 | 시간외단일가_매도호가수량2 | String | N | | |
| ovt_sigpric_sel_bid_qty_1 | 시간외단일가_매도호가수량1 | String | N | | |
| ovt_sigpric_sel_bid_5 | 시간외단일가_매도호가5 | String | N | | |
| ovt_sigpric_sel_bid_4 | 시간외단일가_매도호가4 | String | N | | |
| ovt_sigpric_sel_bid_3 | 시간외단일가_매도호가3 | String | N | | |
| ovt_sigpric_sel_bid_2 | 시간외단일가_매도호가2 | String | N | | |
| ovt_sigpric_sel_bid_1 | 시간외단일가_매도호가1 | String | N | | |
| ovt_sigpric_buy_bid_1 | 시간외단일가_매수호가1 | String | N | | |
| ovt_sigpric_buy_bid_2 | 시간외단일가_매수호가2 | String | N | | |
| ovt_sigpric_buy_bid_3 | 시간외단일가_매수호가3 | String | N | | |
| ovt_sigpric_buy_bid_4 | 시간외단일가_매수호가4 | String | N | | |
| ovt_sigpric_buy_bid_5 | 시간외단일가_매수호가5 | String | N | | |
| ovt_sigpric_buy_bid_qty_1 | 시간외단일가_매수호가수량1 | String | N | | |
| ovt_sigpric_buy_bid_qty_2 | 시간외단일가_매수호가수량2 | String | N | | |
| ovt_sigpric_buy_bid_qty_3 | 시간외단일가_매수호가수량3 | String | N | | |
| ovt_sigpric_buy_bid_qty_4 | 시간외단일가_매수호가수량4 | String | N | | |
| ovt_sigpric_buy_bid_qty_5 | 시간외단일가_매수호가수량5 | String | N | | |
| ovt_sigpric_buy_bid_jub_pre_1 | 시간외단일가_매수호가직전대비1 | String | N | | |
| ovt_sigpric_buy_bid_jub_pre_2 | 시간외단일가_매수호가직전대비2 | String | N | | |
| ovt_sigpric_buy_bid_jub_pre_3 | 시간외단일가_매수호가직전대비3 | String | N | | |
| ovt_sigpric_buy_bid_jub_pre_4 | 시간외단일가_매수호가직전대비4 | String | N | | |
| ovt_sigpric_buy_bid_jub_pre_5 | 시간외단일가_매수호가직전대비5 | String | N | | |
| ovt_sigpric_sel_bid_tot_req | 시간외단일가_매도호가총잔량 | String | N | | |
| ovt_sigpric_buy_bid_tot_req | 시간외단일가_매수호가총잔량 | String | N | | |
| sel_bid_tot_req_jub_pre | 매도호가총잔량직전대비 | String | N | | |
| sel_bid_tot_req | 매도호가총잔량 | String | N | | |
| buy_bid_tot_req | 매수호가총잔량 | String | N | | |
| buy_bid_tot_req_jub_pre | 매수호가총잔량직전대비 | String | N | | |
| ovt_sel_bid_tot_req_jub_pre | 시간외매도호가총잔량직전대비 | String | N | | |
| ovt_sel_bid_tot_req | 시간외매도호가총잔량 | String | N | | |
| ovt_buy_bid_tot_req | 시간외매수호가총잔량 | String | N | | |
| ovt_buy_bid_tot_req_jub_pre | 시간외매수호가총잔량직전대비 | String | N | | |
| ovt_sigpric_cur_prc | 시간외단일가_현재가 | String | N | | |
| ovt_sigpric_pred_pre_sig | 시간외단일가_전일대비기호 | String | N | | |
| ovt_sigpric_pred_pre | 시간외단일가_전일대비 | String | N | | |
| ovt_sigpric_flu_rt | 시간외단일가_등락률 | String | N | | |
| ovt_sigpric_acc_trde_qty | 시간외단일가_누적거래량 | String | N | | |

#### 요청 예시
```json
{
    "stk_cd": "005930"
}
```

#### 응답 예시
```json
{
    "bid_req_base_tm": "164000",
    "ovt_sigpric_sel_bid_jub_pre_5": "0",
    "ovt_sigpric_sel_bid_jub_pre_4": "0",
    "ovt_sigpric_sel_bid_jub_pre_3": "0",
    "ovt_sigpric_sel_bid_jub_pre_2": "0",
    "ovt_sigpric_sel_bid_jub_pre_1": "0",
    "ovt_sigpric_sel_bid_qty_5": "0",
    "ovt_sigpric_sel_bid_qty_4": "0",
    "ovt_sigpric_sel_bid_qty_3": "0",
    "ovt_sigpric_sel_bid_qty_2": "0",
    "ovt_sigpric_sel_bid_qty_1": "0",
    "ovt_sigpric_sel_bid_5": "-0",
    "ovt_sigpric_sel_bid_4": "-0",
    "ovt_sigpric_sel_bid_3": "-0",
    "ovt_sigpric_sel_bid_2": "-0",
    "ovt_sigpric_sel_bid_1": "-0",
    "ovt_sigpric_buy_bid_1": "-0",
    "ovt_sigpric_buy_bid_2": "-0",
    "ovt_sigpric_buy_bid_3": "-0",
    "ovt_sigpric_buy_bid_4": "-0",
    "ovt_sigpric_buy_bid_5": "-0",
    "ovt_sigpric_buy_bid_qty_1": "0",
    "ovt_sigpric_buy_bid_qty_2": "0",
    "ovt_sigpric_buy_bid_qty_3": "0",
    "ovt_sigpric_buy_bid_qty_4": "0",
    "ovt_sigpric_buy_bid_qty_5": "0",
    "ovt_sigpric_buy_bid_jub_pre_1": "0",
    "ovt_sigpric_buy_bid_jub_pre_2": "0",
    "ovt_sigpric_buy_bid_jub_pre_3": "0",
    "ovt_sigpric_buy_bid_jub_pre_4": "0",
    "ovt_sigpric_buy_bid_jub_pre_5": "0",
    "ovt_sigpric_sel_bid_tot_req": "0",
    "ovt_sigpric_buy_bid_tot_req": "0",
    "sel_bid_tot_req_jub_pre": "0",
    "sel_bid_tot_req": "24028",
    "buy_bid_tot_req": "26579",
    "buy_bid_tot_req_jub_pre": "0",
    "ovt_sel_bid_tot_req_jub_pre": "0",
    "ovt_sel_bid_tot_req": "0",
    "ovt_buy_bid_tot_req": "11",
    "ovt_buy_bid_tot_req_jub_pre": "0",
    "ovt_sigpric_cur_prc": "156600",
    "ovt_sigpric_pred_pre_sig": "0",
    "ovt_sigpric_pred_pre": "0",
    "ovt_sigpric_flu_rt": "0.00",
    "ovt_sigpric_acc_trde_qty": "0",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 프로그램매매추이요청 시간대별 (ka90005)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| date | 날짜 | String | Y | 8 | YYYYMMDD |
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액(백만원), 2:수량(천주) |
| mrkt_tp | 시장구분 | String | Y | 10 | 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01<br/>코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P001_AL02 |
| min_tic_tp | 분틱구분 | String | Y | 1 | 0:틱, 1:분 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| prm_trde_trnsn | 프로그램매매추이 | LIST | N | | |
| - cntr_tm | 체결시간 | String | N | 20 | |
| - dfrt_trde_sel | 차익거래매도 | String | N | 20 | |
| - dfrt_trde_buy | 차익거래매수 | String | N | 20 | |
| - dfrt_trde_netprps | 차익거래순매수 | String | N | 20 | |
| - ndiffpro_trde_sel | 비차익거래매도 | String | N | 20 | |
| - ndiffpro_trde_buy | 비차익거래매수 | String | N | 20 | |
| - ndiffpro_trde_netprps | 비차익거래순매수 | String | N | 20 | |
| - dfrt_trde_sell_qty | 차익거래매도수량 | String | N | 20 | |
| - dfrt_trde_buy_qty | 차익거래매수수량 | String | N | 20 | |
| - dfrt_trde_netprps_qty | 차익거래순매수수량 | String | N | 20 | |
| - ndiffpro_trde_sell_qty | 비차익거래매도수량 | String | N | 20 | |
| - ndiffpro_trde_buy_qty | 비차익거래매수수량 | String | N | 20 | |
| - ndiffpro_trde_netprps_qty | 비차익거래순매수수량 | String | N | 20 | |
| - all_sel | 전체매도 | String | N | 20 | |
| - all_buy | 전체매수 | String | N | 20 | |
| - all_netprps | 전체순매수 | String | N | 20 | |
| - kospi200 | KOSPI200 | String | N | 20 | |
| - basis | BASIS | String | N | 20 | |

#### 요청 예시
```json
{
    "date": "20241101",
    "amt_qty_tp": "1",
    "mrkt_tp": "P00101",
    "min_tic_tp": "1",
    "stex_tp": "1"
}
```

#### 응답 예시
```json
{
    "prm_trde_trnsn": [
        {
            "cntr_tm": "170500",
            "dfrt_trde_sel": "0",
            "dfrt_trde_buy": "0",
            "dfrt_trde_netprps": "0",
            "ndiffpro_trde_sel": "1",
            "ndiffpro_trde_buy": "17",
            "ndiffpro_trde_netprps": "+17",
            "dfrt_trde_sell_qty": "0",
            "dfrt_trde_buy_qty": "0",
            "dfrt_trde_netprps_qty": "0",
            "ndiffpro_trde_sell_qty": "0",
            "ndiffpro_trde_buy_qty": "0",
            "ndiffpro_trde_netprps_qty": "+0",
            "all_sel": "1",
            "all_buy": "17",
            "all_netprps": "+17",
            "kospi200": "+47839",
            "basis": "-146.59"
        },
        {
            "cntr_tm": "170400",
            "dfrt_trde_sel": "0",
            "dfrt_trde_buy": "0",
            "dfrt_trde_netprps": "0",
            "ndiffpro_trde_sel": "1",
            "ndiffpro_trde_buy": "17",
            "ndiffpro_trde_netprps": "+17",
            "dfrt_trde_sell_qty": "0",
            "dfrt_trde_buy_qty": "0",
            "dfrt_trde_netprps_qty": "0",
            "ndiffpro_trde_sell_qty": "0",
            "ndiffpro_trde_buy_qty": "0",
            "ndiffpro_trde_netprps_qty": "+0",
            "all_sel": "1",
            "all_buy": "17",
            "all_netprps": "+17",
            "kospi200": "+47839",
            "basis": "-146.59"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 프로그램매매차익잔고추이요청 (ka90006)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| date | 날짜 | String | Y | 8 | YYYYMMDD |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| prm_trde_dfrt_remn_trnsn | 프로그램매매차익잔고추이 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - buy_dfrt_trde_qty | 매수차익거래수량 | String | N | 20 | |
| - buy_dfrt_trde_amt | 매수차익거래금액 | String | N | 20 | |
| - buy_dfrt_trde_irds_amt | 매수차익거래증감액 | String | N | 20 | |
| - sel_dfrt_trde_qty | 매도차익거래수량 | String | N | 20 | |
| - sel_dfrt_trde_amt | 매도차익거래금액 | String | N | 20 | |
| - sel_dfrt_trde_irds_amt | 매도차익거래증감액 | String | N | 20 | |

#### 요청 예시
```json
{
    "date": "20241125",
    "stex_tp": "1"
}
```

#### 응답 예시
```json
{
    "prm_trde_dfrt_remn_trnsn": [
        {
            "dt": "20241125",
            "buy_dfrt_trde_qty": "0",
            "buy_dfrt_trde_amt": "0",
            "buy_dfrt_trde_irds_amt": "0",
            "sel_dfrt_trde_qty": "0",
            "sel_dfrt_trde_amt": "0",
            "sel_dfrt_trde_irds_amt": "0"
        },
        {
            "dt": "20241122",
            "buy_dfrt_trde_qty": "0",
            "buy_dfrt_trde_amt": "0",
            "buy_dfrt_trde_irds_amt": "-25",
            "sel_dfrt_trde_qty": "0",
            "sel_dfrt_trde_amt": "0",
            "sel_dfrt_trde_irds_amt": "0"
        },
        {
            "dt": "20241121",
            "buy_dfrt_trde_qty": "0",
            "buy_dfrt_trde_amt": "25",
            "buy_dfrt_trde_irds_amt": "25",
            "sel_dfrt_trde_qty": "0",
            "sel_dfrt_trde_amt": "0",
            "sel_dfrt_trde_irds_amt": "0"
        },
        {
            "dt": "20241120",
            "buy_dfrt_trde_qty": "0",
            "buy_dfrt_trde_amt": "0",
            "buy_dfrt_trde_irds_amt": "-48",
            "sel_dfrt_trde_qty": "0",
            "sel_dfrt_trde_amt": "0",
            "sel_dfrt_trde_irds_amt": "0"
        },
        {
            "dt": "20241119",
            "buy_dfrt_trde_qty": "0",
            "buy_dfrt_trde_amt": "48",
            "buy_dfrt_trde_irds_amt": "43",
            "sel_dfrt_trde_qty": "0",
            "sel_dfrt_trde_amt": "0",
            "sel_dfrt_trde_irds_amt": "0"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 프로그램매매누적추이요청 (ka90007)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| date | 날짜 | String | Y | 8 | YYYYMMDD (종료일기준 1년간 데이터만 조회가능) |
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액, 2:수량 |
| mrkt_tp | 시장구분 | String | Y | 5 | 0:코스피, 1:코스닥 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| prm_trde_acc_trnsn | 프로그램매매누적추이 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - kospi200 | KOSPI200 | String | N | 20 | |
| - basis | BASIS | String | N | 20 | |
| - dfrt_trde_tdy | 차익거래당일 | String | N | 20 | |
| - dfrt_trde_acc | 차익거래누적 | String | N | 20 | |
| - ndiffpro_trde_tdy | 비차익거래당일 | String | N | 20 | |
| - ndiffpro_trde_acc | 비차익거래누적 | String | N | 20 | |
| - all_tdy | 전체당일 | String | N | 20 | |
| - all_acc | 전체누적 | String | N | 20 | |
---

### 종목시간별프로그램매매추이요청 (ka90008)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액, 2:수량 |
| stk_cd | 종목코드 | String | Y | 6 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| date | 날짜 | String | Y | 8 | YYYYMMDD |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_tm_prm_trde_trnsn | 종목시간별프로그램매매추이 | LIST | N | | |
| - tm | 시간 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - prm_sell_amt | 프로그램매도금액 | String | N | 20 | |
| - prm_buy_amt | 프로그램매수금액 | String | N | 20 | |
| - prm_netprps_amt | 프로그램순매수금액 | String | N | 20 | |
| - prm_netprps_amt_irds | 프로그램순매수금액증감 | String | N | 20 | |
| - prm_sell_qty | 프로그램매도수량 | String | N | 20 | |
| - prm_buy_qty | 프로그램매수수량 | String | N | 20 | |
| - prm_netprps_qty | 프로그램순매수수량 | String | N | 20 | |
| - prm_netprps_qty_irds | 프로그램순매수수량증감 | String | N | 20 | |
| - base_pric_tm | 기준가시간 | String | N | 20 | |
| - dbrt_trde_rpy_sum | 대차거래상환주수합 | String | N | 20 | |
| - remn_rcvord_sum | 잔고수주합 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | KRX, NXT, 통합 |

#### 요청 예시
```json
{
    "amt_qty_tp": "1",
    "stk_cd": "005930",
    "date": "20241125"
}
```

#### 응답 예시
```json
{
    "stk_tm_prm_trde_trnsn": [
        {
            "tm": "153029",
            "cur_prc": "+245500",
            "pre_sig": "2",
            "pred_pre": "+40000",
            "flu_rt": "+19.46",
            "trde_qty": "104006",
            "prm_sell_amt": "14245",
            "prm_buy_amt": "10773",
            "prm_netprps_amt": "--3472",
            "prm_netprps_amt_irds": "+771",
            "prm_sell_qty": "58173",
            "prm_buy_qty": "43933",
            "prm_netprps_qty": "--14240",
            "prm_netprps_qty_irds": "+3142",
            "base_pric_tm": "",
            "dbrt_trde_rpy_sum": "",
            "remn_rcvord_sum": "",
            "stex_tp": "KRX"
        },
        {
            "tm": "153001",
            "cur_prc": "+245500",
            "pre_sig": "2",
            "pred_pre": "+40000",
            "flu_rt": "+19.46",
            "trde_qty": "94024",
            "prm_sell_amt": "12596",
            "prm_buy_amt": "8353",
            "prm_netprps_amt": "--4243",
            "prm_netprps_amt_irds": "0",
            "prm_sell_qty": "51455",
            "prm_buy_qty": "34073",
            "prm_netprps_qty": "--17382",
            "prm_netprps_qty_irds": "0",
            "base_pric_tm": "",
            "dbrt_trde_rpy_sum": "",
            "remn_rcvord_sum": "",
            "stex_tp": "KRX"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 프로그램매매추이요청 일자별 (ka90010)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| date | 날짜 | String | Y | 8 | YYYYMMDD |
| amt_qty_tp | 금액수량구분 | String | Y | 1 | 1:금액(백만원), 2:수량(천주) |
| mrkt_tp | 시장구분 | String | Y | 10 | 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01, 3일경우:P001_AL01<br/>코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02, 3일경우:P001_AL02 |
| min_tic_tp | 분틱구분 | String | Y | 1 | 0:틱, 1:분 |
| stex_tp | 거래소구분 | String | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| prm_trde_trnsn | 프로그램매매추이 | LIST | N | | |
| - cntr_tm | 체결시간 | String | N | 20 | |
| - dfrt_trde_sel | 차익거래매도 | String | N | 20 | |
| - dfrt_trde_buy | 차익거래매수 | String | N | 20 | |
| - dfrt_trde_netprps | 차익거래순매수 | String | N | 20 | |
| - ndiffpro_trde_sel | 비차익거래매도 | String | N | 20 | |
| - ndiffpro_trde_buy | 비차익거래매수 | String | N | 20 | |
| - ndiffpro_trde_netprps | 비차익거래순매수 | String | N | 20 | |
| - dfrt_trde_sell_qty | 차익거래매도수량 | String | N | 20 | |
| - dfrt_trde_buy_qty | 차익거래매수수량 | String | N | 20 | |
| - dfrt_trde_netprps_qty | 차익거래순매수수량 | String | N | 20 | |
| - ndiffpro_trde_sell_qty | 비차익거래매도수량 | String | N | 20 | |
| - ndiffpro_trde_buy_qty | 비차익거래매수수량 | String | N | 20 | |
| - ndiffpro_trde_netprps_qty | 비차익거래순매수수량 | String | N | 20 | |
| - all_sel | 전체매도 | String | N | 20 | |
| - all_buy | 전체매수 | String | N | 20 | |
| - all_netprps | 전체순매수 | String | N | 20 | |
| - kospi200 | KOSPI200 | String | N | 20 | |
| - basis | BASIS | String | N | 20 | |

#### 요청 예시
```json
{
    "date": "20241125",
    "amt_qty_tp": "1",
    "mrkt_tp": "P00101",
    "min_tic_tp": "0",
    "stex_tp": "1"
}
```

#### 응답 예시
```json
{
    "prm_trde_trnsn": [
        {
            "cntr_tm": "20241125000000",
            "dfrt_trde_sel": "0",
            "dfrt_trde_buy": "0",
            "dfrt_trde_netprps": "0",
            "ndiffpro_trde_sel": "0",
            "ndiffpro_trde_buy": "0",
            "ndiffpro_trde_netprps": "0",
            "dfrt_trde_sell_qty": "0",
            "dfrt_trde_buy_qty": "0",
            "dfrt_trde_netprps_qty": "0",
            "ndiffpro_trde_sell_qty": "0",
            "ndiffpro_trde_buy_qty": "0",
            "ndiffpro_trde_netprps_qty": "0",
            "all_sel": "0",
            "all_buy": "0",
            "all_netprps": "0",
            "kospi200": "0.00",
            "basis": ""
        },
        {
            "cntr_tm": "20241122000000",
            "dfrt_trde_sel": "0",
            "dfrt_trde_buy": "0",
            "dfrt_trde_netprps": "-0",
            "ndiffpro_trde_sel": "96",
            "ndiffpro_trde_buy": "608",
            "ndiffpro_trde_netprps": "+512",
            "dfrt_trde_sell_qty": "0",
            "dfrt_trde_buy_qty": "0",
            "dfrt_trde_netprps_qty": "-0",
            "ndiffpro_trde_sell_qty": "1",
            "ndiffpro_trde_buy_qty": "7",
            "ndiffpro_trde_netprps_qty": "+6",
            "all_sel": "96",
            "all_buy": "608",
            "all_netprps": "512",
            "kospi200": "+341.13",
            "basis": "-8.48"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
---

### 종목일별프로그램매매추이요청 (ka90013)

#### 기본 정보
- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/mrkcond
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 (Request)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| authorization | 접근토큰 | String | Y | 1000 | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx... |
| cont-yn | 연속조회여부 | String | N | 1 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅 |
| next-key | 연속조회키 | String | N | 50 | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| amt_qty_tp | 금액수량구분 | String | N | 1 | 1:금액, 2:수량 |
| stk_cd | 종목코드 | String | Y | 20 | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| date | 날짜 | String | N | 8 | YYYYMMDD |

#### 응답 (Response)

##### Header
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| cont-yn | 연속조회여부 | String | N | 1 | 다음 데이터가 있을시 Y값 전달 |
| next-key | 연속조회키 | String | N | 50 | 다음 데이터가 있을시 다음 키값 전달 |
| api-id | TR명 | String | Y | 10 | |

##### Body
| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| stk_daly_prm_trde_trnsn | 종목일별프로그램매매추이 | LIST | N | | |
| - dt | 일자 | String | N | 20 | |
| - cur_prc | 현재가 | String | N | 20 | |
| - pre_sig | 대비기호 | String | N | 20 | |
| - pred_pre | 전일대비 | String | N | 20 | |
| - flu_rt | 등락율 | String | N | 20 | |
| - trde_qty | 거래량 | String | N | 20 | |
| - prm_sell_amt | 프로그램매도금액 | String | N | 20 | |
| - prm_buy_amt | 프로그램매수금액 | String | N | 20 | |
| - prm_netprps_amt | 프로그램순매수금액 | String | N | 20 | |
| - prm_netprps_amt_irds | 프로그램순매수금액증감 | String | N | 20 | |
| - prm_sell_qty | 프로그램매도수량 | String | N | 20 | |
| - prm_buy_qty | 프로그램매수수량 | String | N | 20 | |
| - prm_netprps_qty | 프로그램순매수수량 | String | N | 20 | |
| - prm_netprps_qty_irds | 프로그램순매수수량증감 | String | N | 20 | |
| - base_pric_tm | 기준가시간 | String | N | 20 | |
| - dbrt_trde_rpy_sum | 대차거래상환주수합 | String | N | 20 | |
| - remn_rcvord_sum | 잔고수주합 | String | N | 20 | |
| - stex_tp | 거래소구분 | String | N | 20 | KRX, NXT, 통합 |

#### 요청 예시
```json
{
    "amt_qty_tp": "",
    "stk_cd": "005930",
    "date": ""
}
```

#### 응답 예시
```json
{
    "stk_daly_prm_trde_trnsn": [
        {
            "dt": "20241125",
            "cur_prc": "+267000",
            "pre_sig": "2",
            "pred_pre": "+60000",
            "flu_rt": "+28.99",
            "trde_qty": "3",
            "prm_sell_amt": "0",
            "prm_buy_amt": "0",
            "prm_netprps_amt": "0",
            "prm_netprps_amt_irds": "0",
            "prm_sell_qty": "0",
            "prm_buy_qty": "0",
            "prm_netprps_qty": "0",
            "prm_netprps_qty_irds": "0",
            "base_pric_tm": "",
            "dbrt_trde_rpy_sum": "",
            "remn_rcvord_sum": "",
            "stex_tp": "통합"
        },
        {
            "dt": "20241122",
            "cur_prc": "0",
            "pre_sig": "0",
            "pred_pre": "0",
            "flu_rt": "0.00",
            "trde_qty": "0",
            "prm_sell_amt": "0",
            "prm_buy_amt": "0",
            "prm_netprps_amt": "0",
            "prm_netprps_amt_irds": "--6",
            "prm_sell_qty": "0",
            "prm_buy_qty": "0",
            "prm_netprps_qty": "0",
            "prm_netprps_qty_irds": "--19",
            "base_pric_tm": "",
            "dbrt_trde_rpy_sum": "",
            "remn_rcvord_sum": "",
            "stex_tp": "KRX"
        }
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```
# 홈페이지 내용 정리

## 1. 국내주식 WEBSOCKET 실시간시세

### 기본 정보

**※ 00 (주문체결)**
실시간 항목 00(주문체결)은 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문 접수, 체결, 정정, 취소 등 매매가 발생할 경우 데이터가 수신됩니다.

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### TR 목록

| TR명 | 코드 |
|------|------|
| 주문체결 | 00 |
| 잔고 | 04 |
| 주식기세 | 0A |
| 주식체결 | 0B |
| 주식우선호가 | 0C |
| 주식호가잔량 | 0D |
| 주식시간외호가 | 0E |
| 주식당일거래원 | 0F |
| ETF NAV | 0G |
| 주식예상체결 | 0H |
| 업종지수 | 0J |
| 업종등락 | 0U |
| 주식종목정보 | 0g |
| ELW 이론가 | 0m |
| 장시작시간 | 0s |
| ELW 지표 | 0u |
| 종목프로그램매매 | 0w |
| VI발동/해제 | 1h |

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 9201 | 계좌번호 | String | N | |
| 9203 | 주문번호 | String | N | |
| 9205 | 관리자사번 | String | N | |
| 9001 | 종목코드,업종코드 | String | N | |
| 912 | 주문업무분류 | String | N | |
| 913 | 주문상태 | String | N | |
| 302 | 종목명 | String | N | |
| 900 | 주문수량 | String | N | |
| 901 | 주문가격 | String | N | |
| 902 | 미체결수량 | String | N | |
| 903 | 체결누계금액 | String | N | |
| 904 | 원주문번호 | String | N | |
| 905 | 주문구분 | String | N | |
| 906 | 매매구분 | String | N | |
| 907 | 매도수구분 | String | N | |
| 908 | 주문/체결시간 | String | N | |
| 909 | 체결번호 | String | N | |
| 910 | 체결가 | String | N | |
| 911 | 체결량 | String | N | |
| 10 | 현재가 | String | N | |
| 27 | (최우선)매도호가 | String | N | |
| 28 | (최우선)매수호가 | String | N | |
| 914 | 단위체결가 | String | N | |
| 915 | 단위체결량 | String | N | |
| 938 | 당일매매수수료 | String | N | |
| 939 | 당일매매세금 | String | N | |
| 919 | 거부사유 | String | N | |
| 920 | 화면번호 | String | N | |
| 921 | 터미널번호 | String | N | |
| 922 | 신용구분 | String | N | 실시간 체결용 |
| 923 | 대출일 | String | N | 실시간 체결용 |
| 10010 | 시간외단일가_현재가 | String | N | |
| 2134 | 거래소구분 | String | N | 0:통합,1:KRX,2:NXT |
| 2135 | 거래소구분명 | String | N | 통합,KRX,NXT |
| 2136 | SOR여부 | String | N | Y,N |

### 요청 예시

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "" ],
		"type" : [ "00" ]
	}]
}
```

### 응답 예시

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data':[
		{
			'values': {
				'9201':'1111111111',
				'9203':'0000018',
				'9205':'',
				'9001':'005930',
				'912':'JJ',
				'913':'접수',
				'302':'삼성전자',
				'900':'1',
				'901':'0',
				'902':'1',
				'903':'0',
				'904':'0000000',
				'905':'+매수',
				'906':'시장가',
				'907':'2',
				'908':'094022',
				'909':'',
				'910':'',
				'911':'',
				'10':'+60700',
				'27':'+60700',
				'28':'-60000',
				'914':'',
				'915':'',
				'938':'0',
				'939':'0',
				'919':'0',
				'920':'',
				'921':'0701002',
				'922':'00',
				'923':'00000000',
				'10010':'',
				'2134':'1',
				'2135':'KRX',
				'2136':'Y'
			},
			'type':'00',
			'name':'주문체결',
			'item':'005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 2. 국내주식 WEBSOCKET 실시간시세 - 잔고(04)

### 기본 정보

**※ 04 (잔고)**
실시간 항목 04(잔고)는 종목코드(item) 등록과 상관 없이 ACCESS TOKEN을 발급한 계좌에 주문 체결이 발생할 경우 데이터가 수신됩니다.

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 104 | |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (잔고 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 9201 | 계좌번호 | String | N | |
| 9001 | 종목코드,업종코드 | String | N | |
| 917 | 신용구분 | String | N | |
| 916 | 대출일 | String | N | |
| 302 | 종목명 | String | N | |
| 10 | 현재가 | String | N | |
| 930 | 보유수량 | String | N | |
| 931 | 매입단가 | String | N | |
| 932 | 총매입가(당일누적) | String | N | |
| 933 | 주문가능수량 | String | N | |
| 945 | 당일순매수량 | String | N | |
| 946 | 매도/매수구분 | String | N | 계약,주 |
| 950 | 당일총매도손익 | String | N | |
| 951 | Extra Item | String | N | |
| 27 | (최우선)매도호가 | String | N | |
| 28 | (최우선)매수호가 | String | N | |
| 307 | 기준가 | String | N | |
| 8019 | 손익률(실현손익) | String | N | |
| 957 | 신용금액 | String | N | |
| 958 | 신용이자 | String | N | |
| 918 | 만기일 | String | N | |
| 990 | 당일실현손익(유가) | String | N | |
| 991 | 당일실현손익율(유가) | String | N | |
| 992 | 당일실현손익(신용) | String | N | |
| 993 | 당일실현손익율(신용) | String | N | |
| 959 | 담보대출수량 | String | N | |
| 924 | Extra Item | String | N | |

### 요청 예시 (잔고)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "" ],
		"type" : [ "04" ]
	}]
}
```

### 응답 예시 (잔고)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'9201': '1111111111',
				'9001': '005930',
				'917': '00',
				'916': '00000000',
				'302': '삼성전자',
				'10': '-60150',
				'930': '102',
				'931': '154116',
				'932': '15719834',
				'933': '102',
				'945': '4',
				'946': '2',
				'950': '0',
				'951': '0',
				'27': '-60200',
				'28': '-60100',
				'307': '60300',
				'8019': '0.00',
				'957': '0',
				'958': '0',
				'918': '00000000',
				'990': '0',
				'991': '0.00',
				'992': '0',
				'993': '0.00',
				'959': '0',
				'924': '0'
			},
			'type': '04',
			'name': '현물잔고',
			'item': '005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 3. 국내주식 WEBSOCKET 실시간시세 - 주식기세(0A)

### 기본 정보

**※ 0A (주식기세)**
특정 종목이 기세일때 발생하는 데이터로 시장에서 체결없이 현재가가 변경되는 대량매매나 거래소에서 종목 종가데이터 보정시 발생하는 실시간입니다.

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지(등록,해지시에만 값 전송,데이터 실시간 수신시 미전송) |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식기세 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 27 | (최우선)매도호가 | String | N | |
| 28 | (최우선)매수호가 | String | N | |
| 13 | 누적거래량 | String | N | |
| 14 | 누적거래대금 | String | N | |
| 16 | 시가 | String | N | |
| 17 | 고가 | String | N | |
| 18 | 저가 | String | N | |
| 25 | 전일대비기호 | String | N | |
| 26 | 전일거래량대비(계약,주) | String | N | |
| 29 | 거래대금증감 | String | N | |
| 30 | 전일거래량대비(비율) | String | N | |
| 31 | 거래회전율 | String | N | |
| 32 | 거래비용 | String | N | |
| 311 | 시가총액(억) | String | N | |
| 567 | 상한가발생시간 | String | N | |
| 568 | 하한가발생시간 | String | N | |

### 요청 예시 (주식기세)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0A" ]
	}]
}
```

### 응답 예시 (주식기세)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'10': '+86800',
				'11': '+19500',
				'12': '+28.97',
				'27': '+85200',
				'28': '+85100',
				'13': '367090',
				'14': '31642',
				'16': '+87400',
				'17': '+87400',
				'18': ' 67300',
				'25': '2',
				'26': '+131995',
				'29': '+15843118000',
				'30': '+156.15',
				'31': '0.01',
				'32': '157',
				'311': '5181771',
				'567': '154912',
				'568': '000000'
			},
			'type': '0A',
			'name': '주식기세',
			'item': '005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 4. 국내주식 WEBSOCKET 실시간시세 - 주식체결(0B)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0B,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식체결 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 27 | (최우선)매도호가 | String | N | |
| 28 | (최우선)매수호가 | String | N | |
| 15 | 거래량 | String | N | +는 매수체결,-는 매도체결 |
| 13 | 누적거래량 | String | N | |
| 14 | 누적거래대금 | String | N | |
| 16 | 시가 | String | N | |
| 17 | 고가 | String | N | |
| 18 | 저가 | String | N | |
| 25 | 전일대비기호 | String | N | |
| 26 | 전일거래량대비(계약,주) | String | N | |
| 29 | 거래대금증감 | String | N | |
| 30 | 전일거래량대비(비율) | String | N | |
| 31 | 거래회전율 | String | N | |
| 32 | 거래비용 | String | N | |
| 228 | 체결강도 | String | N | |
| 311 | 시가총액(억) | String | N | |
| 290 | 장구분 | String | N | 1: 장전 시간외, 2: 장중, 3: 장후 시간외 |
| 691 | K.O 접근도 | String | N | |
| 567 | 상한가발생시간 | String | N | |
| 568 | 하한가발생시간 | String | N | |
| 851 | 전일 동시간 거래량 비율 | String | N | |
| 1890 | 시가시간 | String | N | |
| 1891 | 고가시간 | String | N | |
| 1892 | 저가시간 | String | N | |
| 1030 | 매도체결량 | String | N | |
| 1031 | 매수체결량 | String | N | |
| 1032 | 매수비율 | String | N | |
| 1071 | 매도체결건수 | String | N | |
| 1072 | 매수체결건수 | String | N | |
| 1313 | 순간거래대금 | String | N | |
| 1315 | 매도체결량_단건 | String | N | |
| 1316 | 매수체결량_단건 | String | N | |
| 1314 | 순매수체결량 | String | N | |
| 1497 | CFD증거금 | String | N | |
| 1498 | 유지증거금 | String | N | |
| 620 | 당일거래평균가 | String | N | |
| 732 | CFD거래비용 | String | N | |
| 852 | 대주거래비용 | String | N | |
| 9081 | 거래소구분 | String | N | |

### 요청 예시 (주식체결)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0B" ]
	}]
}
```

### 응답 예시 (주식체결)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'trnm': 'REAL',
	'data': [
		{
			'type': '0B',
			'name': '주식체결',
			'item': '005930',
			'values': {
				'20': '165208',
				'10': '-20800',
				'11': '-50',
				'12': '-0.24',
				'27': '-20800',
				'28': '-20700',
				'15': '+82',
				'13': '30379732',
				'14': '632640',
				'16': '20850',
				'17': '+21150',
				'18': '-20450',
				'25': '5',
				'26': '-1057122',
				'29': '-22041267850',
				'30': '-96.64',
				'31': '36.67',
				'32': '44',
				'228': '98.92',
				'311': '17230',
				'290': '2',
				'691': '0',
				'567': '000000',
				'568': '000000',
				'851': '',
				'1890': '',
				'1891': '',
				'1892': '',
				'1030': '',
				'1031': '',
				'1032': '',
				'1071': '',
				'1072': '',
				'1313': '',
				'1315': '',
				'1316': '',
				'1314': '',
				'1497': '',
				'1498': '',
				'620': '',
				'732': '',
				'852': '',
				'9081': '1'
			}
		}
	]
}
```

---

## 5. 국내주식 WEBSOCKET 실시간시세 - 주식우선호가(0C)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식우선호가 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 27 | (최우선)매도호가 | String | N | |
| 28 | (최우선)매수호가 | String | N | |

### 요청 예시 (주식우선호가)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0C" ]
	}]
}
```

### 응답 예시 (주식우선호가)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'trnm': 'REAL',
	'data': [
		{
			'type': '0C',
			'name': '주식우선호가',
			'item': '005930',
			'values': {
				'27': '-20800',
				'28': '-20700'
			}
		}
	]
}
```

---

## 6. 국내주식 WEBSOCKET 실시간시세 - 주식호가잔량(0D)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식호가잔량 전용)

#### 기본 호가 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 21 | 호가시간 | String | N | |
| 41-50 | 매도호가1-10 | String | N | |
| 61-70 | 매도호가수량1-10 | String | N | |
| 81-90 | 매도호가직전대비1-10 | String | N | |
| 51-60 | 매수호가1-10 | String | N | |
| 71-80 | 매수호가수량1-10 | String | N | |
| 91-100 | 매수호가직전대비1-10 | String | N | |

#### 호가 총계 및 예상체결 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 121 | 매도호가총잔량 | String | N | |
| 122 | 매도호가총잔량직전대비 | String | N | |
| 125 | 매수호가총잔량 | String | N | |
| 126 | 매수호가총잔량직전대비 | String | N | |
| 23 | 예상체결가 | String | N | |
| 24 | 예상체결수량 | String | N | |
| 128 | 순매수잔량 | String | N | |
| 129 | 매수비율 | String | N | |
| 138 | 순매도잔량 | String | N | |
| 139 | 매도비율 | String | N | |
| 200 | 예상체결가전일종가대비 | String | N | |
| 201 | 예상체결가전일종가대비등락율 | String | N | |
| 238 | 예상체결가전일종가대비기호 | String | N | |

#### 예상체결 시간 전용 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 291 | 예상체결가 | String | N | 예상체결 시간동안에만 유효한 값 |
| 292 | 예상체결량 | String | N | |
| 293 | 예상체결가전일대비기호 | String | N | |
| 294 | 예상체결가전일대비 | String | N | |
| 295 | 예상체결가전일대비등락율 | String | N | |

#### LP 호가 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 621-630 | LP매도호가수량1-10 | String | N | |
| 631-640 | LP매수호가수량1-10 | String | N | |

#### 기타 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 13 | 누적거래량 | String | N | |
| 299 | 전일거래량대비예상체결율 | String | N | |
| 215 | 장운영구분 | String | N | |
| 216 | 투자자별ticker | String | N | |

#### KRX 거래소별 호가 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 6044-6053 | KRX 매도호가잔량1-10 | String | N | |
| 6054-6063 | KRX 매수호가잔량1-10 | String | N | |
| 6064 | KRX 매도호가총잔량 | String | N | |
| 6065 | KRX 매수호가총잔량 | String | N | |

#### NXT 거래소별 호가 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 6066-6075 | NXT 매도호가잔량1-10 | String | N | |
| 6076-6085 | NXT 매수호가잔량1-10 | String | N | |
| 6086 | NXT 매도호가총잔량 | String | N | |
| 6087 | NXT 매수호가총잔량 | String | N | |

#### 중간가 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 6100 | KRX 중간가 매도 총잔량 증감 | String | N | |
| 6101 | KRX 중간가 매도 총잔량 | String | N | |
| 6102 | KRX 중간가 | String | N | |
| 6103 | KRX 중간가 매수 총잔량 | String | N | |
| 6104 | KRX 중간가 매수 총잔량 증감 | String | N | |
| 6105 | NXT중간가 매도 총잔량 증감 | String | N | |
| 6106 | NXT중간가 매도 총잔량 | String | N | |
| 6107 | NXT중간가 | String | N | |
| 6108 | NXT중간가 매수 총잔량 | String | N | |
| 6109 | NXT중간가 매수 총잔량 증감 | String | N | |
| 6110 | KRX중간가대비 | String | N | 기준가대비 |
| 6111 | KRX중간가대비 기호 | String | N | 기준가대비 |
| 6112 | KRX중간가대비등락율 | String | N | 기준가대비 |
| 6113 | NXT중간가대비 | String | N | 기준가대비 |
| 6114 | NXT중간가대비 기호 | String | N | 기준가대비 |
| 6115 | NXT중간가대비등락율 | String | N | 기준가대비 |

### 요청 예시 (주식호가잔량)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0D" ]
	}]
}
```

### 응답 예시 (주식호가잔량)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답 (일부 필드만 표시):**
```json
{
	'trnm': 'REAL',
	'data': [
		{
			'type': '0D',
			'name': '주식호가잔량',
			'item': '005930',
			'values': {
				'21': '165207',
				'41': '-20800',
				'61': '82',
				'51': '-20700',
				'71': '23847',
				'42': '+20900',
				'62': '393',
				'52': '-20650',
				'72': '834748',
				'121': '12622527',
				'122': '-1036021',
				'125': '14453430',
				'126': '+1062126',
				'23': '20850',
				'24': '332941',
				'128': '+1830903',
				'129': '114.51',
				...
			}
		}
	]
}
```

---

## 7. 국내주식 WEBSOCKET 실시간시세 - 주식시간외호가(0E)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식시간외호가 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 21 | 호가시간 | String | N | |
| 131 | 시간외매도호가총잔량 | String | N | |
| 132 | 시간외매도호가총잔량직전대비 | String | N | |
| 135 | 시간외매수호가총잔량 | String | N | |
| 136 | 시간외매수호가총잔량직전대비 | String | N | |

### 요청 예시 (주식시간외호가)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0E" ]
	}]
}
```

### 응답 예시 (주식시간외호가)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'trnm': 'REAL',
	'data': [
		{
			'type': '0E',
			'name': '주식시간외호가',
			'item': '005930',
			'values': {
				'21': '165208',
				'131': '43955',
				'132': '+156',
				'135': '0',
				'136': '0'
			}
		}
	]
}
```

---

## 8. 국내주식 WEBSOCKET 실시간시세 - 주식당일거래원(0F)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식당일거래원 전용)

#### 매도 거래원 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 141-145 | 매도거래원1-5 | String | N | |
| 161-165 | 매도거래원수량1-5 | String | N | |
| 166-170 | 매도거래원별증감1-5 | String | N | |
| 146-150 | 매도거래원코드1-5 | String | N | |
| 271-275 | 매도거래원색깔1-5 | String | N | |

#### 매수 거래원 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 151-155 | 매수거래원1-5 | String | N | |
| 171-175 | 매수거래원수량1-5 | String | N | |
| 176-180 | 매수거래원별증감1-5 | String | N | |
| 156-160 | 매수거래원코드1-5 | String | N | |
| 281-285 | 매수거래원색깔1-5 | String | N | |

#### 외국계 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 261 | 외국계매도추정합 | String | N | |
| 262 | 외국계매도추정합변동 | String | N | |
| 263 | 외국계매수추정합 | String | N | |
| 264 | 외국계매수추정합변동 | String | N | |
| 267 | 외국계순매수추정합 | String | N | |
| 268 | 외국계순매수변동 | String | N | |
| 337 | 거래소구분 | String | N | |

### 요청 예시 (주식당일거래원)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0F" ]
	}]
}
```

### 응답 예시 (주식당일거래원)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'trnm': 'REAL',
	'data': [
		{
			'type': '0F',
			'name': '주식당일거래원',
			'item': '005930',
			'values': {
				'141': '',
				'161': '9350409',
				'166': '+8593585',
				'146': '993',
				'271': '!!!!',
				'151': '',
				'171': '9321128',
				'176': '+8557163',
				'156': '993',
				'281': '!!!!',
				'145': '미래에셋',
				'165': '100',
				'170': '0',
				'150': '005',
				'275': '!!!!',
				'155': '미래에셋',
				'175': '50100',
				'180': '0',
				'160': '005',
				'285': '!!!!',
				'261': '0',
				'262': '0',
				'263': '0',
				'264': '0',
				'267': '0',
				'268': '0',
				'337': '2'
			}
		}
	]
}
```

---

## 9. 국내주식 WEBSOCKET 실시간시세 - ETF NAV(0G)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (ETF NAV 전용)

#### NAV 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 36 | NAV | String | N | |
| 37 | NAV전일대비 | String | N | |
| 38 | NAV등락율 | String | N | |
| 39 | 추적오차율 | String | N | |

#### 기본 시세 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 13 | 누적거래량 | String | N | |
| 25 | 전일대비기호 | String | N | |

#### ELW 관련 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 667 | ELW기어링비율 | String | N | |
| 668 | ELW손익분기율 | String | N | |
| 669 | ELW자본지지점 | String | N | |

#### 괴리율 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 265 | NAV/지수괴리율 | String | N | |
| 266 | NAV/ETF괴리율 | String | N | |

### 요청 예시 (ETF NAV)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "069500" ],
		"type" : [ "0G" ]
	}]
}
```

### 응답 예시 (ETF NAV)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'36': '+7488.27',
				'37': '+9.57',
				'38': '+0.13',
				'39': '1.82',
				'20': '105732',
				'10': '+7485',
				'11': '+45',
				'12': '+0.60',
				'13': '16874',
				'25': '2',
				'265': '+10.04',
				'266': '-0.04'
			},
			'type': '0G',
			'name': 'ETF NAV',
			'item': '069500'
		}
	],
	'trnm': 'REAL'
}
```

---

## 10. 국내주식 WEBSOCKET 실시간시세 - 주식예상체결(0H)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식예상체결 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 15 | 거래량 | String | N | +는 매수체결, -는 매도체결 |
| 13 | 누적거래량 | String | N | |
| 25 | 전일대비기호 | String | N | |

### 요청 예시 (주식예상체결)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0H" ]
	}]
}
```

### 응답 예시 (주식예상체결)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '110206',
				'10': '+60500',
				'11': '+200',
				'12': '+0.33',
				'15': '-7805',
				'13': '768293',
				'25': '2'
			},
			'type': '0H',
			'name': '주식예상체결',
			'item': '005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 11. 국내주식 WEBSOCKET 실시간시세 - 업종지수(0J)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (업종지수 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 15 | 거래량 | String | N | +는 매수체결,-는 매도체결 |
| 13 | 누적거래량 | String | N | |
| 14 | 누적거래대금 | String | N | |
| 16 | 시가 | String | N | |
| 17 | 고가 | String | N | |
| 18 | 저가 | String | N | |
| 25 | 전일대비기호 | String | N | |
| 26 | 전일거래량대비 | String | N | 계약,주 |

### 요청 예시 (업종지수)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "001" ],
		"type" : [ "0J" ]
	}]
}
```

### 응답 예시 (업종지수)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '110430',
				'10': '-1762.61',
				'11': '-189.51',
				'12': '-9.71',
				'15': '2800',
				'13': '725277',
				'14': '60711859',
				'16': '-1949.04',
				'17': '+1961.28',
				'18': '-1756.13',
				'25': '5',
				'26': '-1482363'
			},
			'type': '0J',
			'name': '업종지수',
			'item': '001'
		}
	],
	'trnm': 'REAL'
}
```

---

## 12. 국내주식 WEBSOCKET 실시간시세 - 업종등락(0U)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (업종등락 전용)

#### 등락 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 252 | 상승종목수 | String | N | |
| 251 | 상한종목수 | String | N | |
| 253 | 보합종목수 | String | N | |
| 255 | 하락종목수 | String | N | |
| 254 | 하한종목수 | String | N | |

#### 거래 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 13 | 누적거래량 | String | N | |
| 14 | 누적거래대금 | String | N | |
| 10 | 현재가 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 256 | 거래형성종목수 | String | N | 계약,주 |
| 257 | 거래형성비율 | String | N | |
| 25 | 전일대비기호 | String | N | |

### 요청 예시 (업종등락)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "001" ],
		"type" : [ "0U" ]
	}]
}
```

### 응답 예시 (업종등락)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '110710',
				'252': '46',
				'251': '1',
				'253': '166',
				'255': '204',
				'254': '16',
				'13': '741784',
				'14': '62093941',
				'10': '-1757.42',
				'11': '-194.70',
				'12': '-9.97',
				'256': '416',
				'257': '43.20',
				'25': '5'
			},
			'type': '0U',
			'name': '업종등락',
			'item': '001'
		}
	],
	'trnm': 'REAL'
}
```

---

## 13. 국내주식 WEBSOCKET 실시간시세 - 주식종목정보(0g)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (주식종목정보 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 297 | 임의연장 | String | N | |
| 592 | 장전임의연장 | String | N | |
| 593 | 장후임의연장 | String | N | |
| 305 | 상한가 | String | N | |
| 306 | 하한가 | String | N | |
| 307 | 기준가 | String | N | |
| 689 | 조기종료ELW발생 | String | N | |
| 594 | 통화단위 | String | N | |
| 382 | 증거금율표시 | String | N | |
| 370 | 종목정보 | String | N | |

### 요청 예시 (주식종목정보)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0g" ]
	}]
}
```

### 응답 예시 (주식종목정보)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'297': '동정적VI',
				'592': ' ',
				'593': ' ',
				'305': '+78300',
				'306': '-42300',
				'307': '60300',
				'689': '',
				'594': '',
				'382': '',
				'370': ''
			},
			'type': '0g',
			'name': '주식종목정보',
			'item': '005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 14. 국내주식 WEBSOCKET 실시간시세 - ELW 이론가(0m)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (ELW 이론가 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 670 | ELW이론가 | String | N | |
| 671 | ELW내재변동성 | String | N | |
| 672 | ELW델타 | String | N | |
| 673 | ELW감마 | String | N | |
| 674 | ELW쎄타 | String | N | |
| 675 | ELW베가 | String | N | |
| 676 | ELW로 | String | N | |
| 706 | LP호가내재변동성 | String | N | |

### 요청 예시 (ELW 이론가)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "57JBHH" ],
		"type" : [ "0m" ]
	}]
}
```

### 응답 예시 (ELW 이론가)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '140000',
				'10': ' 450',
				'670': '0',
				'671': '0.00',
				'672': '0',
				'673': '0',
				'674': '0.000000',
				'675': '0.000000',
				'676': '0.000000',
				'706': ' 0.00'
			},
			'type': '0m',
			'name': 'ELW 이론가',
			'item': '57JBHH'
		}
	],
	'trnm': 'REAL'
}
```

---

## 15. 국내주식 WEBSOCKET 실시간시세 - 장시작시간(0s)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (장시작시간 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 215 | 장운영구분 | String | N | 0:KRX장전, 3:KRX장시작, P:NXT프리마켓개시, Q:NXT프리마켓종료, R:NXT메인마켓개시, S:NXT메인마켓종료, T:NXT애프터마켓단일가개시, U:NXT애프터마켓개시, V:NXT종가매매종료, W:NXT애프터마켓종료 |
| 20 | 체결시간 | String | N | |
| 214 | 장시작예상잔여시간 | String | N | |

### 요청 예시 (장시작시간)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "" ],
		"type" : [ "0s" ]
	}]
}
```

### 응답 예시 (장시작시간)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data':[
		{
			'values': {
				'215':'b',
				'20':'170000',
				'214':'000000'
			},
			'type':'0s',
			'name':'장시작시간',
			'item':''
		}
	],
	'trnm': 'REAL'
}
```

---

## 16. 국내주식 WEBSOCKET 실시간시세 - ELW 지표(0u)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (ELW 지표 전용)

| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 666 | ELW패리티 | String | N | |
| 1211 | ELW프리미엄 | String | N | |
| 667 | ELW기어링비율 | String | N | |
| 668 | ELW손익분기율 | String | N | |
| 669 | ELW자본지지점 | String | N | |

### 요청 예시 (ELW 지표)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "57JBHH" ],
		"type" : [ "0u" ]
	}]
}
```

### 응답 예시 (ELW 지표)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '111847',
				'666': '69.13',
				'1211': '0',
				'667': '1037.04',
				'668': '+44.73',
				'669': '+44.78'
			},
			'type': '0u',
			'name': 'ELW 지표',
			'item': '57JBHH'
		}
	],
	'trnm': 'REAL'
}
```

---

## 17. 국내주식 WEBSOCKET 실시간시세 - 종목프로그램매매(0w)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (종목프로그램매매 전용)

#### 기본 시세 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 20 | 체결시간 | String | N | |
| 10 | 현재가 | String | N | |
| 25 | 전일대비기호 | String | N | |
| 11 | 전일대비 | String | N | |
| 12 | 등락율 | String | N | |
| 13 | 누적거래량 | String | N | |

#### 프로그램매매 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 202 | 매도수량 | String | N | |
| 204 | 매도금액 | String | N | |
| 206 | 매수수량 | String | N | |
| 208 | 매수금액 | String | N | |
| 210 | 순매수수량 | String | N | |
| 211 | 순매수수량증감 | String | N | 계약,주 |
| 212 | 순매수금액 | String | N | |
| 213 | 순매수금액증감 | String | N | |

#### 기타 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 214 | 장시작예상잔여시간 | String | N | |
| 215 | 장운영구분 | String | N | |
| 216 | 투자자별ticker | String | N | |

### 요청 예시 (종목프로그램매매)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "005930" ],
		"type" : [ "0w" ]
	}]
}
```

### 응답 예시 (종목프로그램매매)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'20': '113442',
				'10': '-60200',
				'25': '5',
				'11': '-100',
				'12': '-0.17',
				'13': '128152628',
				'202': '0',
				'204': '0',
				'206': '8043',
				'208': '483',
				'210': '8043',
				'212': '483',
				'213': '0',
				'211': '0'
			},
			'type': '0w',
			'name': '종목별프로그램매매',
			'item': '005930'
		}
	],
	'trnm': 'REAL'
}
```

---

## 18. 국내주식 WEBSOCKET 실시간시세 - VI발동/해제(1h)

### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

### 요청 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| trnm | 서비스명 | String | Y | 10 | REG : 등록, REMOVE : 해지 |
| grp_no | 그룹번호 | String | Y | 4 | |
| refresh | 기존등록유지여부 | String | Y | 1 | 등록(REG)시 0:기존유지안함 1:기존유지(Default) 0일경우 기존등록한 item/type은 해지, 1일경우 기존등록한 item/type 유지 해지(REMOVE)시 값 불필요 |
| data | 실시간 등록 리스트 | LIST | | | |
| - item | 실시간 등록 요소 | String[] | N | 100 | 거래소별 종목코드, 업종코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| - type | 실시간 항목 | String[] | Y | 2 | TR 명(0A,0B....) |

### 응답 Body

| Element | 한글명 | Type | Required | Length | Description |
|---------|--------|------|----------|--------|-------------|
| return_code | 결과코드 | int | N | | 통신결과에대한 코드 (등록,해지요청시에만 값 전송 0:정상,1:오류, 데이터 실시간 수신시 미전송) |
| return_msg | 결과메시지 | String | N | | 통신결과에대한메시지 |
| trnm | 서비스명 | String | N | | 등록,해지요청시 요청값 반환, 실시간수신시 REAL 반환 |
| data | 실시간 등록리스트 | LIST | N | | |
| - type | 실시간항목 | String | N | | TR 명(0A,0B....) |
| - name | 실시간 항목명 | String | N | | |
| - item | 실시간 등록 요소 | String | N | | 종목코드 |
| - values | 실시간 값 리스트 | LIST | N | | |

### 실시간 값 리스트 필드 (VI발동/해제 전용)

#### 종목 기본 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 9001 | 종목코드 | String | N | |
| 302 | 종목명 | String | N | |
| 13 | 누적거래량 | String | N | |
| 14 | 누적거래대금 | String | N | |

#### VI 발동 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 9068 | VI발동구분 | String | N | |
| 9008 | KOSPI,KOSDAQ,전체구분 | String | N | |
| 9075 | 장전구분 | String | N | |
| 1221 | VI발동가격 | String | N | |
| 1223 | 매매체결처리시각 | String | N | |
| 1224 | VI해제시각 | String | N | |
| 1225 | VI적용구분 | String | N | 정적/동적/동적+정적 |

#### VI 기준가격 및 괴리율
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 1236 | 기준가격 정적 | String | N | 계약,주 |
| 1237 | 기준가격 동적 | String | N | |
| 1238 | 괴리율 정적 | String | N | |
| 1239 | 괴리율 동적 | String | N | |

#### 기타 VI 정보
| 필드 | 한글명 | Type | Required | Description |
|------|--------|------|----------|-------------|
| 1489 | VI발동가 등락율 | String | N | |
| 1490 | VI발동횟수 | String | N | |
| 9069 | 발동방향구분 | String | N | |
| 1279 | Extra Item | String | N | |

### 요청 예시 (VI발동/해제)

```json
{
	"trnm" : "REG",
	"grp_no" : "1",
	"refresh" : "1",
	"data" : [{
		"item" : [ "" ],
		"type" : [ "1h" ]
	}]
}
```

### 응답 예시 (VI발동/해제)

**요청 응답:**
```json
{
	'trnm': 'REG',
	'return_code': 0,
	'return_msg': ''
}
```

**실시간 수신 응답:**
```json
{
	'data': [
		{
			'values': {
				'9001':'005930',
				'302':'삼성전자',
				'13':'1077818',
				'14':'4201',
				'9068':'1',
				'9008':'101',
				'9075':'1',
				'1221':'4125',
				'1223':'111454',
				'1224':'111703',
				'1225':'정적',
				'1236':'3750',
				'1237':'0',
				'1238':'+10.00',
				'1239':'0.00',
				'1489':'+10.00',
				'1490':'1',
				'9069':'1',
				'1279':'+정적'
			},
			'type':'1h',
			'name':'VI발동/해제',
			'item':'005930'
		}
	],
	'trnm':'REAL'
}
```

---# 키움증권 API 문서

## 국내주식 REST API

### 업종

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 업종프로그램요청 | ka10010 | 업종 프로그램 매매 정보 조회 |
| 업종별투자자순매수요청 | ka10051 | 업종별 투자자 순매수 정보 조회 |
| 업종현재가요청 | ka20001 | 업종 현재가 정보 조회 |
| 업종별주가요청 | ka20002 | 업종별 주가 정보 조회 |
| 전업종지수요청 | ka20003 | 전 업종 지수 정보 조회 |
| 업종현재가일별요청 | ka20009 | 업종 현재가 일별 정보 조회 |

### 업종프로그램요청 (ka10010)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                 |
| ------- | -------- | ------ | -------- | ------ | --------------------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명                   | Type   | Required | Length | Description |
| -------------------------- | ------------------------ | ------ | -------- | ------ | ----------- |
| dfrt_trst_sell_qty         | 차익위탁매도수량         | String | N        | 20     |             |
| dfrt_trst_sell_amt         | 차익위탁매도금액         | String | N        | 20     |             |
| dfrt_trst_buy_qty          | 차익위탁매수수량         | String | N        | 20     |             |
| dfrt_trst_buy_amt          | 차익위탁매수금액         | String | N        | 20     |             |
| dfrt_trst_netprps_qty      | 차익위탁순매수수량       | String | N        | 20     |             |
| dfrt_trst_netprps_amt      | 차익위탁순매수금액       | String | N        | 20     |             |
| ndiffpro_trst_sell_qty     | 비차익위탁매도수량       | String | N        | 20     |             |
| ndiffpro_trst_sell_amt     | 비차익위탁매도금액       | String | N        | 20     |             |
| ndiffpro_trst_buy_qty      | 비차익위탁매수수량       | String | N        | 20     |             |
| ndiffpro_trst_buy_amt      | 비차익위탁매수금액       | String | N        | 20     |             |
| ndiffpro_trst_netprps_qty  | 비차익위탁순매수수량     | String | N        | 20     |             |
| ndiffpro_trst_netprps_amt  | 비차익위탁순매수금액     | String | N        | 20     |             |
| all_dfrt_trst_sell_qty     | 전체차익위탁매도수량     | String | N        | 20     |             |
| all_dfrt_trst_sell_amt     | 전체차익위탁매도금액     | String | N        | 20     |             |
| all_dfrt_trst_buy_qty      | 전체차익위탁매수수량     | String | N        | 20     |             |
| all_dfrt_trst_buy_amt      | 전체차익위탁매수금액     | String | N        | 20     |             |
| all_dfrt_trst_netprps_qty  | 전체차익위탁순매수수량   | String | N        | 20     |             |
| all_dfrt_trst_netprps_amt  | 전체차익위탁순매수금액   | String | N        | 20     |             |

#### 요청 예시

```json
{
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"dfrt_trst_sell_qty":"",
	"dfrt_trst_sell_amt":"",
	"dfrt_trst_buy_qty":"",
	"dfrt_trst_buy_amt":"",
	"dfrt_trst_netprps_qty":"",
	"dfrt_trst_netprps_amt":"",
	"ndiffpro_trst_sell_qty":"",
	"ndiffpro_trst_sell_amt":"",
	"ndiffpro_trst_buy_qty":"",
	"ndiffpro_trst_buy_amt":"",
	"ndiffpro_trst_netprps_qty":"",
	"ndiffpro_trst_netprps_amt":"",
	"all_dfrt_trst_sell_qty":"40242",
	"all_dfrt_trst_sell_amt":"",
	"all_dfrt_trst_buy_qty":"69219",
	"all_dfrt_trst_buy_amt":"",
	"all_dfrt_trst_netprps_qty":"346871946",
	"all_dfrt_trst_netprps_amt":"",
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### 업종별투자자순매수요청 (ka10051)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명         | Type   | Required | Length | Description                           |
| ---------- | -------------- | ------ | -------- | ------ | ------------------------------------- |
| mrkt_tp    | 시장구분       | String | Y        | 1      | 코스피:0, 코스닥:1                    |
| amt_qty_tp | 금액수량구분   | String | Y        | 1      | 금액:0, 수량:1                        |
| base_dt    | 기준일자       | String | N        | 8      | YYYYMMDD                              |
| stex_tp    | 거래소구분     | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                  |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                         | 한글명                   | Type   | Required | Length | Description |
| ------------------------------- | ------------------------ | ------ | -------- | ------ | ----------- |
| inds_netprps                    | 업종별순매수             | LIST   | N        |        |             |
| - inds_cd                       | 업종코드                 | String | N        | 20     |             |
| - inds_nm                       | 업종명                   | String | N        | 20     |             |
| - cur_prc                       | 현재가                   | String | N        | 20     |             |
| - pre_smbol                     | 대비부호                 | String | N        | 20     |             |
| - pred_pre                      | 전일대비                 | String | N        | 20     |             |
| - flu_rt                        | 등락율                   | String | N        | 20     |             |
| - trde_qty                      | 거래량                   | String | N        | 20     |             |
| - sc_netprps                    | 증권순매수               | String | N        | 20     |             |
| - insrnc_netprps                | 보험순매수               | String | N        | 20     |             |
| - invtrt_netprps                | 투신순매수               | String | N        | 20     |             |
| - bank_netprps                  | 은행순매수               | String | N        | 20     |             |
| - jnsinkm_netprps               | 종신금순매수             | String | N        | 20     |             |
| - endw_netprps                  | 기금순매수               | String | N        | 20     |             |
| - etc_corp_netprps              | 기타법인순매수           | String | N        | 20     |             |
| - ind_netprps                   | 개인순매수               | String | N        | 20     |             |
| - frgnr_netprps                 | 외국인순매수             | String | N        | 20     |             |
| - native_trmt_frgnr_netprps     | 내국인대우외국인순매수   | String | N        | 20     |             |
| - natn_netprps                  | 국가순매수               | String | N        | 20     |             |
| - samo_fund_netprps             | 사모펀드순매수           | String | N        | 20     |             |
| - orgn_netprps                  | 기관계순매수             | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "0",
	"amt_qty_tp": "0",
	"base_dt": "20241107",
	"stex_tp": "3"
}
```

#### 응답 예시

```json
{
	"inds_netprps":
		[
			{
				"inds_cd":"001_AL",
				"inds_nm":"종합(KOSPI)",
				"cur_prc":"+265381",
				"pre_smbol":"2",
				"pred_pre":"+9030",
				"flu_rt":"352",
				"trde_qty":"1164",
				"sc_netprps":"+255",
				"insrnc_netprps":"+0",
				"invtrt_netprps":"+0",
				"bank_netprps":"+0",
				"jnsinkm_netprps":"+0",
				"endw_netprps":"+0",
				"etc_corp_netprps":"+0",
				"ind_netprps":"-0",
				"frgnr_netprps":"-622",
				"native_trmt_frgnr_netprps":"+4",
				"natn_netprps":"+0",
				"samo_fund_netprps":"+1",
				"orgn_netprps":"+601"
			},
			{
				"inds_cd":"002_AL",
				"inds_nm":"대형주",
				"cur_prc":"+265964",
				"pre_smbol":"2",
				"pred_pre":"+10690",
				"flu_rt":"419",
				"trde_qty":"1145",
				"sc_netprps":"+255",
				"insrnc_netprps":"+0",
				"invtrt_netprps":"+0",
				"bank_netprps":"+0",
				"jnsinkm_netprps":"+0",
				"endw_netprps":"+0",
				"etc_corp_netprps":"+0",
				"ind_netprps":"+16",
				"frgnr_netprps":"-622",
				"native_trmt_frgnr_netprps":"+4",
				"natn_netprps":"+0",
				"samo_fund_netprps":"+1",
				"orgn_netprps":"+602"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### 업종현재가요청 (ka20001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------- | ---------- | ------ | -------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp  | 시장구분   | String | Y        | 1      | 0:코스피, 1:코스닥, 2:코스피200                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| inds_cd  | 업종코드   | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701:KRX100                                                                                                                                                                                                                                                                                                                                                                                               |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| cur_prc                    | 현재가               | String | N        | 20     |             |
| pred_pre_sig               | 전일대비기호         | String | N        | 20     |             |
| pred_pre                   | 전일대비             | String | N        | 20     |             |
| flu_rt                     | 등락률               | String | N        | 20     |             |
| trde_qty                   | 거래량               | String | N        | 20     |             |
| trde_prica                 | 거래대금             | String | N        | 20     |             |
| trde_frmatn_stk_num        | 거래형성종목수       | String | N        | 20     |             |
| trde_frmatn_rt             | 거래형성비율         | String | N        | 20     |             |
| open_pric                  | 시가                 | String | N        | 20     |             |
| high_pric                  | 고가                 | String | N        | 20     |             |
| low_pric                   | 저가                 | String | N        | 20     |             |
| upl                        | 상한                 | String | N        | 20     |             |
| rising                     | 상승                 | String | N        | 20     |             |
| stdns                      | 보합                 | String | N        | 20     |             |
| fall                       | 하락                 | String | N        | 20     |             |
| lst                        | 하한                 | String | N        | 20     |             |
| 52wk_hgst_pric             | 52주최고가           | String | N        | 20     |             |
| 52wk_hgst_pric_dt          | 52주최고가일         | String | N        | 20     |             |
| 52wk_hgst_pric_pre_rt      | 52주최고가대비율     | String | N        | 20     |             |
| 52wk_lwst_pric             | 52주최저가           | String | N        | 20     |             |
| 52wk_lwst_pric_dt          | 52주최저가일         | String | N        | 20     |             |
| 52wk_lwst_pric_pre_rt      | 52주최저가대비율     | String | N        | 20     |             |
| inds_cur_prc_tm            | 업종현재가시간별     | LIST   | N        |        |             |
| - tm_n                     | 시간n                | String | N        | 20     |             |
| - cur_prc_n                | 현재가n              | String | N        | 20     |             |
| - pred_pre_sig_n           | 전일대비기호n        | String | N        | 20     |             |
| - pred_pre_n               | 전일대비n            | String | N        | 20     |             |
| - flu_rt_n                 | 등락률n              | String | N        | 20     |             |
| - trde_qty_n               | 거래량n              | String | N        | 20     |             |
| - acc_trde_qty_n           | 누적거래량n          | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "0",
	"inds_cd": "001"
}
```

#### 응답 예시

```json
{
	"cur_prc":"-2394.49",
	"pred_pre_sig":"5",
	"pred_pre":"-278.47",
	"flu_rt":"-10.42",
	"trde_qty":"890",
	"trde_prica":"41867",
	"trde_frmatn_stk_num":"330",
	"trde_frmatn_rt":"+34.38",
	"open_pric":"-2669.53",
	"high_pric":"-2669.53",
	"low_pric":"-2375.21",
	"upl":"0",
	"rising":"17",
	"stdns":"183",
	"fall":"130",
	"lst":"3",
	"52wk_hgst_pric":"+3001.91",
	"52wk_hgst_pric_dt":"20241004",
	"52wk_hgst_pric_pre_rt":"-20.23",
	"52wk_lwst_pric":"-1608.07",
	"52wk_lwst_pric_dt":"20241031",
	"52wk_lwst_pric_pre_rt":"+48.90",
	"inds_cur_prc_tm":
		[
			{
				"tm_n":"143000",
				"cur_prc_n":"-2394.49",
				"pred_pre_sig_n":"5",
				"pred_pre_n":"-278.47",
				"flu_rt_n":"-10.42",
				"trde_qty_n":"14",
				"acc_trde_qty_n":"890"
			},
			{
				"tm_n":"142950",
				"cur_prc_n":"-2394.49",
				"pred_pre_sig_n":"5",
				"pred_pre_n":"-278.47",
				"flu_rt_n":"-10.42",
				"trde_qty_n":"14",
				"acc_trde_qty_n":"876"
			},
			{
				"tm_n":"142940",
				"cur_prc_n":"-2394.49",
				"pred_pre_sig_n":"5",
				"pred_pre_n":"-278.47",
				"flu_rt_n":"-10.42",
				"trde_qty_n":"14",
				"acc_trde_qty_n":"862"
			},
			{
				"tm_n":"142930",
				"cur_prc_n":"-2395.62",
				"pred_pre_sig_n":"5",
				"pred_pre_n":"-277.34",
				"flu_rt_n":"-10.38",
				"trde_qty_n":"14",
				"acc_trde_qty_n":"848"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### 업종별주가요청 (ka20002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------- | ---------- | ------ | -------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp  | 시장구분   | String | Y        | 1      | 0:코스피, 1:코스닥, 2:코스피200                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| inds_cd  | 업종코드   | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701:KRX100                                                                                                                                                                                                                                                                                                                                                                                               |
| stex_tp  | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| inds_stkpc                 | 업종별주가           | LIST   | N        |        |             |
| - stk_cd                   | 종목코드             | String | N        | 20     |             |
| - stk_nm                   | 종목명               | String | N        | 20     |             |
| - cur_prc                  | 현재가               | String | N        | 20     |             |
| - pred_pre_sig             | 전일대비기호         | String | N        | 20     |             |
| - pred_pre                 | 전일대비             | String | N        | 20     |             |
| - flu_rt                   | 등락률               | String | N        | 20     |             |
| - now_trde_qty             | 현재거래량           | String | N        | 20     |             |
| - sel_bid                  | 매도호가             | String | N        | 20     |             |
| - buy_bid                  | 매수호가             | String | N        | 20     |             |
| - open_pric                | 시가                 | String | N        | 20     |             |
| - high_pric                | 고가                 | String | N        | 20     |             |
| - low_pric                 | 저가                 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "0",
	"inds_cd": "001",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"inds_stkpc":
		[
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"6200",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"now_trde_qty":"116",
				"sel_bid":"+6990",
				"buy_bid":"0",
				"open_pric":"6200",
				"high_pric":"6200",
				"low_pric":"6200"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"465",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"now_trde_qty":"0",
				"sel_bid":"0",
				"buy_bid":"0",
				"open_pric":"0",
				"high_pric":"0",
				"low_pric":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"6090",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"now_trde_qty":"0",
				"sel_bid":"0",
				"buy_bid":"-5000",
				"open_pric":"0",
				"high_pric":"0",
				"low_pric":"0"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"+68100",
				"pred_pre_sig":"2",
				"pred_pre":"+600",
				"flu_rt":"+0.89",
				"now_trde_qty":"3",
				"sel_bid":"0",
				"buy_bid":"+68100",
				"open_pric":"67500",
				"high_pric":"+68100",
				"low_pric":"-66000"
			},
			{
				"stk_cd":"005930",
				"stk_nm":"삼성전자",
				"cur_prc":"55300",
				"pred_pre_sig":"3",
				"pred_pre":"0",
				"flu_rt":"0.00",
				"now_trde_qty":"0",
				"sel_bid":"+55400",
				"buy_bid":"-55000",
				"open_pric":"0",
				"high_pric":"0",
				"low_pric":"0"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### 전업종지수요청 (ka20003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                      |
| -------- | ---------- | ------ | -------- | ------ | ------------------------------------------------ |
| inds_cd  | 업종코드   | String | Y        | 3      | 001:종합(KOSPI), 101:종합(KOSDAQ)                |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| all_inds_idex              | 전업종지수           | LIST   | N        |        |             |
| - stk_cd                   | 종목코드             | String | N        | 20     |             |
| - stk_nm                   | 종목명               | String | N        | 20     |             |
| - cur_prc                  | 현재가               | String | N        | 20     |             |
| - pre_sig                  | 대비기호             | String | N        | 20     |             |
| - pred_pre                 | 전일대비             | String | N        | 20     |             |
| - flu_rt                   | 등락률               | String | N        | 20     |             |
| - trde_qty                 | 거래량               | String | N        | 20     |             |
| - wght                     | 비중                 | String | N        | 20     |             |
| - trde_prica               | 거래대금             | String | N        | 20     |             |
| - upl                      | 상한                 | String | N        | 20     |             |
| - rising                   | 상승                 | String | N        | 20     |             |
| - stdns                    | 보합                 | String | N        | 20     |             |
| - fall                     | 하락                 | String | N        | 20     |             |
| - lst                      | 하한                 | String | N        | 20     |             |
| - flo_stk_num              | 상장종목수           | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001"
}
```

#### 응답 예시

```json
{
	"all_inds_idex":
		[
			{
				"stk_cd":"001",
				"stk_nm":"종합(KOSPI)",
				"cur_prc":"-2393.33",
				"pre_sig":"5",
				"pred_pre":"-279.63",
				"flu_rt":"-10.46",
				"trde_qty":"993",
				"wght":"",
				"trde_prica":"46494",
				"upl":"0",
				"rising":"17",
				"stdns":"184",
				"fall":"129",
				"lst":"4",
				"flo_stk_num":"960"
			},
			{
				"stk_cd":"002",
				"stk_nm":"대형주",
				"cur_prc":"-2379.14",
				"pre_sig":"5",
				"pred_pre":"-326.94",
				"flu_rt":"-12.08",
				"trde_qty":"957",
				"wght":"",
				"trde_prica":"44563",
				"upl":"0",
				"rising":"6",
				"stdns":"32",
				"fall":"56",
				"lst":"2",
				"flo_stk_num":"100"
			},
			{
				"stk_cd":"003",
				"stk_nm":"중형주",
				"cur_prc":"-2691.27",
				"pre_sig":"5",
				"pred_pre":"-58.55",
				"flu_rt":"-2.13",
				"trde_qty":"26",
				"wght":"",
				"trde_prica":"1823",
				"upl":"0",
				"rising":"5",
				"stdns":"75",
				"fall":"49",
				"lst":"2",
				"flo_stk_num":"200"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

### 업종현재가일별요청 (ka20009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/sect
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------- | ---------- | ------ | -------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp  | 시장구분   | String | Y        | 1      | 0:코스피, 1:코스닥, 2:코스피200                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| inds_cd  | 업종코드   | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주, 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701:KRX100                                                                                                                                                                                                                                                                                                                                                                                               |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                    | 한글명               | Type   | Required | Length | Description |
| -------------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| cur_prc                    | 현재가               | String | N        | 20     |             |
| pred_pre_sig               | 전일대비기호         | String | N        | 20     |             |
| pred_pre                   | 전일대비             | String | N        | 20     |             |
| flu_rt                     | 등락률               | String | N        | 20     |             |
| trde_qty                   | 거래량               | String | N        | 20     |             |
| trde_prica                 | 거래대금             | String | N        | 20     |             |
| trde_frmatn_stk_num        | 거래형성종목수       | String | N        | 20     |             |
| trde_frmatn_rt             | 거래형성비율         | String | N        | 20     |             |
| open_pric                  | 시가                 | String | N        | 20     |             |
| high_pric                  | 고가                 | String | N        | 20     |             |
| low_pric                   | 저가                 | String | N        | 20     |             |
| upl                        | 상한                 | String | N        | 20     |             |
| rising                     | 상승                 | String | N        | 20     |             |
| stdns                      | 보합                 | String | N        | 20     |             |
| fall                       | 하락                 | String | N        | 20     |             |
| lst                        | 하한                 | String | N        | 20     |             |
| 52wk_hgst_pric             | 52주최고가           | String | N        | 20     |             |
| 52wk_hgst_pric_dt          | 52주최고가일         | String | N        | 20     |             |
| 52wk_hgst_pric_pre_rt      | 52주최고가대비율     | String | N        | 20     |             |
| 52wk_lwst_pric             | 52주최저가           | String | N        | 20     |             |
| 52wk_lwst_pric_dt          | 52주최저가일         | String | N        | 20     |             |
| 52wk_lwst_pric_pre_rt      | 52주최저가대비율     | String | N        | 20     |             |
| inds_cur_prc_daly_rept     | 업종현재가일별반복   | LIST   | N        |        |             |
| - dt_n                     | 일자n                | String | N        | 20     |             |
| - cur_prc_n                | 현재가n              | String | N        | 20     |             |
| - pred_pre_sig_n           | 전일대비기호n        | String | N        | 20     |             |
| - pred_pre_n               | 전일대비n            | String | N        | 20     |             |
| - flu_rt_n                 | 등락률n              | String | N        | 20     |             |
| - acc_trde_qty_n           | 누적거래량n          | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "0",
	"inds_cd": "001"
}
```

#### 응답 예시

```json
{
	"cur_prc":"-2384.71",
	"pred_pre_sig":"5",
	"pred_pre":"-288.25",
	"flu_rt":"-10.78",
	"trde_qty":"1103",
	"trde_prica":"48151",
	"trde_frmatn_stk_num":"333",
	"trde_frmatn_rt":"+34.69",
	"open_pric":"-2669.53",
	"high_pric":"-2669.53",
	"low_pric":"-2375.21",
	"upl":"0",
	"rising":"18",
	"stdns":"183",
	"fall":"132",
	"lst":"4",
	"52wk_hgst_pric":"+3001.91",
	"52wk_hgst_pric_dt":"20241004",
	"52wk_hgst_pric_pre_rt":"-20.56",
	"52wk_lwst_pric":"-1608.07",
	"52wk_lwst_pric_dt":"20241031",
	"52wk_lwst_pric_pre_rt":"+48.30",
	"inds_cur_prc_daly_rept":
		[
			{
				"dt_n":"20241122",
				"cur_prc_n":"-2384.71",
				"pred_pre_sig_n":"5",
				"pred_pre_n":"-288.25",
				"flu_rt_n":"-10.78",
				"acc_trde_qty_n":"1103"
			},
			{
				"dt_n":"20241121",
				"cur_prc_n":"+2672.96",
				"pred_pre_sig_n":"2",
				"pred_pre_n":"+25.56",
				"flu_rt_n":"+0.97",
				"acc_trde_qty_n":"444"
			},
			{
				"dt_n":"20241120",
				"cur_prc_n":"+2647.40",
				"pred_pre_sig_n":"2",
				"pred_pre_n":"+83.56",
				"flu_rt_n":"+3.26",
				"acc_trde_qty_n":"195"
			}
		],
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 조건검색

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 조건검색 목록조회 | ka10171 | 조건검색 목록 조회 |
| 조건검색 요청 일반 | ka10172 | 조건검색 요청 일반 |
| 조건검색 요청 실시간 | ka10173 | 조건검색 요청 실시간 |

### 조건검색 목록조회 (ka10171)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Body

| Element | 한글명 | Type   | Required | Length | Description    |
| ------- | ------ | ------ | -------- | ------ | -------------- |
| trnm    | TR명   | String | Y        | 7      | CNSRLST고정값  |

#### 응답 Body

| Element     | 한글명          | Type   | Required | Length | Description                    |
| ----------- | --------------- | ------ | -------- | ------ | ------------------------------ |
| return_code | 결과코드        | int    | N        |        | 정상 : 0                       |
| return_msg  | 결과메시지      | String | N        |        | 정상인 경우는 메시지 없음      |
| trnm        | 서비스명        | String | N        | 7      | CNSRLST 고정값                 |
| data        | 조건검색식 목록 | LIST   | N        |        |                                |
| - seq       | 조건검색식 일련번호 | String | N        |        |                            |
| - name      | 조건검색식 명   | String | N        |        |                                |

#### 요청 예시

```json
{
	"trnm": "CNSRLST"
}
```

#### 응답 예시

```json
{
	"trnm": "CNSRLST",
	"return_code": 0,
	"return_msg": "",
	"data": [
		["0","조건1"],
		["1","조건2"],
		["2","조건3"],
		["3","조건4"],
		["4","조건5"]
	]
}
```

---

### 조건검색 요청 일반 (ka10172)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Body

| Element     | 한글명               | Type   | Required | Length | Description                         |
| ----------- | -------------------- | ------ | -------- | ------ | ----------------------------------- |
| trnm        | 서비스명             | String | Y        | 7      | CNSRREQ 고정값                      |
| seq         | 조건검색식 일련번호  | String | Y        | 3      |                                     |
| search_type | 조회타입             | String | Y        |        | 0:조건검색                          |
| stex_tp     | 거래소구분           | String | Y        | 1      | K:KRX                               |
| cont_yn     | 연속조회여부         | String | N        | 1      | Y:연속조회요청, N:연속조회미요청    |
| next_key    | 연속조회키           | String | N        | 20     |                                     |

#### 응답 Body

| Element     | 한글명               | Type   | Required | Length | Description                                        |
| ----------- | -------------------- | ------ | -------- | ------ | -------------------------------------------------- |
| return_code | 결과코드             | int    | N        |        | 정상:0 나머지:에러                                 |
| return_msg  | 결과메시지           | String | N        |        | 정상인 경우는 메시지 없음                          |
| trnm        | 서비스명             | String | N        |        | CNSRREQ                                            |
| seq         | 조건검색식 일련번호  | String | N        |        |                                                    |
| cont_yn     | 연속조회여부         | String | N        |        | 연속 데이터가 존재하는경우 Y, 없으면 N             |
| next_key    | 연속조회키           | String | N        |        | 연속조회여부가Y일경우 다음 조회시 필요한 조회값    |
| data        | 검색결과데이터       | LIST   | N        |        |                                                    |
| - 9001      | 종목코드             | String | N        |        |                                                    |
| - 302       | 종목명               | String | N        |        |                                                    |
| - 10        | 현재가               | String | N        |        |                                                    |
| - 25        | 전일대비기호         | String | N        |        |                                                    |
| - 11        | 전일대비             | String | N        |        |                                                    |
| - 12        | 등락율               | String | N        |        |                                                    |
| - 13        | 누적거래량           | String | N        |        |                                                    |
| - 16        | 시가                 | String | N        |        |                                                    |
| - 17        | 고가                 | String | N        |        |                                                    |
| - 18        | 저가                 | String | N        |        |                                                    |

#### 요청 예시

```json
{
	"trnm": "CNSRREQ",
	"seq": "4",
	"search_type": "0",
	"stex_tp": "K",
	"cont_yn": "N",
	"next_key": ""
}
```

#### 응답 예시

```json
{
	"trnm": "CNSRREQ",
	"seq": "2  ",
	"cont_yn": "N",
	"next_key": "",
	"return_code": 0,
	"data": [
		{
			"9001": "A005930",
			"302": "삼성전자",
			"10": "000021850",
			"25": "3",
			"11": "000000000",
			"12": "000000000",
			"13": "000000000",
			"16": "000000000",
			"17": "000000000",
			"18": "000000000"
		},
		{
			"9001": "A005930",
			"302": "삼성전자",
			"10": "000044350",
			"25": "3",
			"11": "000000000",
			"12": "000000000",
			"13": "000000000",
			"16": "000000000",
			"17": "000000000",
			"18": "000000000"
		},
		{
			"9001": "A005930",
			"302": "삼성전자",
			"10": "000003855",
			"25": "3",
			"11": "000000000",
			"12": "000000000",
			"13": "000000000",
			"16": "000000000",
			"17": "000000000",
			"18": "000000000"
		},
		{
			"9001": "A005930",
			"302": "삼성전자",
			"10": "000075000",
			"25": "5",
			"11": "-00000100",
			"12": "-00000130",
			"13": "010386116",
			"16": "000075100",
			"17": "000075600",
			"18": "000074700"
		},
		{
			"9001": "A005930",
			"302": "삼성전자",
			"10": "000002900",
			"25": "3",
			"11": "000000000",
			"12": "000000000",
			"13": "000000000",
			"16": "000000000",
			"17": "000000000",
			"18": "000000000"
		}
	]
}
```

---

### 조건검색 요청 실시간 (ka10173)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Body

| Element     | 한글명               | Type   | Required | Length | Description                         |
| ----------- | -------------------- | ------ | -------- | ------ | ----------------------------------- |
| trnm        | 서비스명             | String | Y        | 7      | CNSRREQ 고정값                      |
| seq         | 조건검색식 일련번호  | String | Y        | 3      |                                     |
| search_type | 조회타입             | String | Y        | 1      | 1:조건검색+실시간조건검색           |
| stex_tp     | 거래소구분           | String | Y        | 1      | K:KRX                               |

#### 응답 Body (조회 데이터)

| Element     | 한글명               | Type   | Required | Length | Description                                        |
| ----------- | -------------------- | ------ | -------- | ------ | -------------------------------------------------- |
| return_code | 결과코드             | int    | N        |        | 정상:0 나머지:에러                                 |
| return_msg  | 결과메시지           | String | N        |        | 정상인 경우는 메시지 없음                          |
| trnm        | 서비스명             | String | N        |        | CNSRREQ                                            |
| seq         | 조건검색식 일련번호  | String | N        |        |                                                    |
| data        | 검색결과데이터       | LIST   | N        |        |                                                    |
| - jmcode    | 종목코드             | String | N        |        |                                                    |

#### 응답 Body (실시간 데이터)

| Element     | 한글명               | Type   | Required | Length | Description                                        |
| ----------- | -------------------- | ------ | -------- | ------ | -------------------------------------------------- |
| data        | 검색결과데이터       | LIST   | Y        |        |                                                    |
| trnm        | 서비스명             | String | Y        |        | REAL                                               |
| - type      | 실시간 항목          | String | Y        | 2      | TR 명(0A,0B....)                                   |
| - name      | 실시간 항목명        | String | Y        |        | 종목코드                                           |
| - values    | 실시간 수신 값       | Object | Y        |        |                                                    |
| - - 841     | 일련번호             | String | Y        |        |                                                    |
| - - 9001    | 종목코드             | String | Y        |        |                                                    |
| - - 843     | 삽입삭제 구분        | String | Y        |        | I:삽입, D:삭제                                     |
| - - 20      | 체결시간             | String | Y        |        |                                                    |
| - - 907     | 매도/매수 구분       | String | Y        |        |                                                    |

#### 요청 예시

```json
{
	"trnm": "CNSRREQ",
	"seq": "4",
	"search_type": "1",
	"stex_tp": "K"
}
```

#### 응답 예시 (조회 데이터)

```json
{
	"trnm": "CNSRREQ",
	"seq": "4",
	"return_code": 0,
	"data": [
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"},
		{"jmcode": "A005930"}
	]
}
```

#### 응답 예시 (실시간 데이터)

```json
{
	"data": [
		{
			"values": {
				"841": "4",
				"9001": "005930",
				"843": "I",
				"20": "152028",
				"907": "2"
			},
			"type": "02",
			"name": "조건검색",
			"item": "005930"
		}
	],
	"trnm": "REAL"
}
```

---

### 조건검색 실시간 해제 (ka10174)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: wss://api.kiwoom.com:10000
- **모의투자 도메인**: wss://mockapi.kiwoom.com:10000(KRX만 지원가능)
- **URL**: /api/dostk/websocket
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Body

| Element | 한글명               | Type   | Required | Length | Description     |
| ------- | -------------------- | ------ | -------- | ------ | --------------- |
| trnm    | 서비스명             | String | Y        | 7      | CNSRCLR 고정값  |
| seq     | 조건검색식 일련번호  | String | Y        |        |                 |

#### 응답 Body

| Element     | 한글명               | Type   | Required | Length | Description                |
| ----------- | -------------------- | ------ | -------- | ------ | -------------------------- |
| return_code | 결과코드             | int    | Y        |        | 정상:0 나머지:에러         |
| return_msg  | 결과메시지           | String | Y        |        | 정상인 경우는 메시지 없음  |
| trnm        | 서비스명             | String | Y        |        | CNSRCLR 고정값             |
| seq         | 조건검색식 일련번호  | String | Y        |        |                            |

#### 요청 예시

```json
{
	"trnm": "CNSRCLR",
	"seq": "1"
}
```

#### 응답 예시

```json
{
	"trnm": "CNSRCLR",
	"seq": "1",
	"return_code": 0,
	"return_msg": ""
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 종목정보

#### TR 목록

| TR명                       | 코드    | 설명                       |
| -------------------------- | ------- | -------------------------- |
| 주식기본정보요청           | ka10001 | 주식기본정보요청           |
| 주식거래원요청             | ka10002 | 주식거래원요청             |
| 체결정보요청               | ka10003 | 체결정보요청               |
| 신용매매동향요청           | ka10013 | 신용매매동향요청           |
| 일별거래상세요청           | ka10015 | 일별거래상세요청           |
| 신고저가요청               | ka10016 | 신고저가요청               |
| 상하한가요청               | ka10017 | 상하한가요청               |
| 고저가근접요청             | ka10018 | 고저가근접요청             |
| 가격급등락요청             | ka10019 | 가격급등락요청             |
| 거래량갱신요청             | ka10024 | 거래량갱신요청             |
| 매물대집중요청             | ka10025 | 매물대집중요청             |
| 고저PER요청                | ka10026 | 고저PER요청                |
| 시가대비등락률요청         | ka10028 | 시가대비등락률요청         |
| 거래원매물대분석요청       | ka10043 | 거래원매물대분석요청       |
| 거래원순간거래량요청       | ka10052 | 거래원순간거래량요청       |
| 변동성완화장치발동종목요청 | ka10054 | 변동성완화장치발동종목요청 |
| 당일전일체결량요청         | ka10055 | 당일전일체결량요청         |
| 투자자별일별매매종목요청   | ka10058 | 투자자별일별매매종목요청   |
| 종목별투자자기관별요청     | ka10059 | 종목별투자자기관별요청     |
| 종목별투자자기관별합계요청 | ka10061 | 종목별투자자기관별합계요청 |
| 당일전일체결요청           | ka10084 | 당일전일체결요청           |
| 관심종목정보요청           | ka10095 | 관심종목정보요청           |
| 종목정보 리스트            | ka10099 | 종목정보 리스트            |
| 종목정보 조회              | ka10100 | 종목정보 조회              |
| 업종코드 리스트            | ka10101 | 업종코드 리스트            |
| 회원사 리스트              | ka10102 | 회원사 리스트              |
| 프로그램순매수상위50요청   | ka90003 | 프로그램순매수상위50요청   |
| 종목별프로그램매매현황요청 | ka90004 | 종목별프로그램매매현황요청 |

---

### 주식기본정보요청 (ka10001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                    |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element             | 한글명          | Type   | Required | Length | Description                                                                                                  |
| ------------------- | --------------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------------ |
| stk_cd              | 종목코드        | String | N        | 20     |                                                                                                              |
| stk_nm              | 종목명          | String | N        | 20     |                                                                                                              |
| setl_mm             | 결산월          | String | N        | 20     |                                                                                                              |
| fav                 | 액면가          | String | N        | 20     |                                                                                                              |
| cap                 | 자본금          | String | N        | 20     |                                                                                                              |
| flo_stk             | 상장주식        | String | N        | 20     |                                                                                                              |
| crd_rt              | 신용비율        | String | N        | 20     |                                                                                                              |
| oyr_hgst            | 연중최고        | String | N        | 20     |                                                                                                              |
| oyr_lwst            | 연중최저        | String | N        | 20     |                                                                                                              |
| mac                 | 시가총액        | String | N        | 20     |                                                                                                              |
| mac_wght            | 시가총액비중    | String | N        | 20     |                                                                                                              |
| for_exh_rt          | 외인소진률      | String | N        | 20     |                                                                                                              |
| repl_pric           | 대용가          | String | N        | 20     |                                                                                                              |
| per                 | PER             | String | N        | 20     | **[주의]** PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| eps                 | EPS             | String | N        | 20     |                                                                                                              |
| roe                 | ROE             | String | N        | 20     | **[주의]** PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| pbr                 | PBR             | String | N        | 20     |                                                                                                              |
| ev                  | EV              | String | N        | 20     |                                                                                                              |
| bps                 | BPS             | String | N        | 20     |                                                                                                              |
| sale_amt            | 매출액          | String | N        | 20     |                                                                                                              |
| bus_pro             | 영업이익        | String | N        | 20     |                                                                                                              |
| cup_nga             | 당기순이익      | String | N        | 20     |                                                                                                              |
| 250hgst             | 250최고         | String | N        | 20     |                                                                                                              |
| 250lwst             | 250최저         | String | N        | 20     |                                                                                                              |
| high_pric           | 고가            | String | N        | 20     |                                                                                                              |
| open_pric           | 시가            | String | N        | 20     |                                                                                                              |
| low_pric            | 저가            | String | N        | 20     |                                                                                                              |
| upl_pric            | 상한가          | String | N        | 20     |                                                                                                              |
| lst_pric            | 하한가          | String | N        | 20     |                                                                                                              |
| base_pric           | 기준가          | String | N        | 20     |                                                                                                              |
| exp_cntr_pric       | 예상체결가      | String | N        | 20     |                                                                                                              |
| exp_cntr_qty        | 예상체결수량    | String | N        | 20     |                                                                                                              |
| 250hgst_pric_dt     | 250최고가일     | String | N        | 20     |                                                                                                              |
| 250hgst_pric_pre_rt | 250최고가대비율 | String | N        | 20     |                                                                                                              |
| 250lwst_pric_dt     | 250최저가일     | String | N        | 20     |                                                                                                              |
| 250lwst_pric_pre_rt | 250최저가대비율 | String | N        | 20     |                                                                                                              |
| cur_prc             | 현재가          | String | N        | 20     |                                                                                                              |
| pre_sig             | 대비기호        | String | N        | 20     |                                                                                                              |
| pred_pre            | 전일대비        | String | N        | 20     |                                                                                                              |
| flu_rt              | 등락율          | String | N        | 20     |                                                                                                              |
| trde_qty            | 거래량          | String | N        | 20     |                                                                                                              |
| trde_pre            | 거래대비        | String | N        | 20     |                                                                                                              |
| fav_unit            | 액면가단위      | String | N        | 20     |                                                                                                              |
| dstr_stk            | 유통주식        | String | N        | 20     |                                                                                                              |
| dstr_rt             | 유통비율        | String | N        | 20     |                                                                                                              |

#### 요청 예시

```json
{
  "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
  "stk_cd": "005930",
  "stk_nm": "삼성전자",
  "setl_mm": "12",
  "fav": "5000",
  "cap": "1311",
  "flo_stk": "25527",
  "crd_rt": "+0.08",
  "oyr_hgst": "+181400",
  "oyr_lwst": "-91200",
  "mac": "24352",
  "mac_wght": "",
  "for_exh_rt": "0.00",
  "repl_pric": "66780",
  "per": "",
  "eps": "",
  "roe": "",
  "pbr": "",
  "ev": "",
  "bps": "-75300",
  "sale_amt": "0",
  "bus_pro": "0",
  "cup_nga": "0",
  "250hgst": "+124000",
  "250lwst": "-66800",
  "high_pric": "95400",
  "open_pric": "-0",
  "low_pric": "0",
  "upl_pric": "20241016",
  "lst_pric": "-47.41",
  "base_pric": "20231024",
  "exp_cntr_pric": "+26.69",
  "exp_cntr_qty": "95400",
  "250hgst_pric_dt": "3",
  "250hgst_pric_pre_rt": "0",
  "250lwst_pric_dt": "0.00",
  "250lwst_pric_pre_rt": "0",
  "cur_prc": "0.00",
  "pre_sig": "",
  "pred_pre": "",
  "flu_rt": "0",
  "trde_qty": "0",
  "trde_pre": "0",
  "fav_unit": "0",
  "dstr_stk": "0",
  "dstr_rt": "0",
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식거래원요청 (ka10002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                    |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element           | 한글명        | Type   | Required | Length | Description |
| ----------------- | ------------- | ------ | -------- | ------ | ----------- |
| stk_cd            | 종목코드      | String | N        | 20     |             |
| stk_nm            | 종목명        | String | N        | 20     |             |
| cur_prc           | 현재가        | String | N        | 20     |             |
| flu_smbol         | 등락부호      | String | N        | 20     |             |
| base_pric         | 기준가        | String | N        | 20     |             |
| pred_pre          | 전일대비      | String | N        | 20     |             |
| flu_rt            | 등락율        | String | N        | 20     |             |
| sel_trde_ori_nm_1 | 매도거래원명1 | String | N        | 20     |             |
| sel_trde_ori_1    | 매도거래원1   | String | N        | 20     |             |
| sel_trde_qty_1    | 매도거래량1   | String | N        | 20     |             |
| buy_trde_ori_nm_1 | 매수거래원명1 | String | N        | 20     |             |
| buy_trde_ori_1    | 매수거래원1   | String | N        | 20     |             |
| buy_trde_qty_1    | 매수거래량1   | String | N        | 20     |             |
| sel_trde_ori_nm_2 | 매도거래원명2 | String | N        | 20     |             |
| sel_trde_ori_2    | 매도거래원2   | String | N        | 20     |             |
| sel_trde_qty_2    | 매도거래량2   | String | N        | 20     |             |
| buy_trde_ori_nm_2 | 매수거래원명2 | String | N        | 20     |             |
| buy_trde_ori_2    | 매수거래원2   | String | N        | 20     |             |
| buy_trde_qty_2    | 매수거래량2   | String | N        | 20     |             |
| sel_trde_ori_nm_3 | 매도거래원명3 | String | N        | 20     |             |
| sel_trde_ori_3    | 매도거래원3   | String | N        | 20     |             |
| sel_trde_qty_3    | 매도거래량3   | String | N        | 20     |             |
| buy_trde_ori_nm_3 | 매수거래원명3 | String | N        | 20     |             |
| buy_trde_ori_3    | 매수거래원3   | String | N        | 20     |             |
| buy_trde_qty_3    | 매수거래량3   | String | N        | 20     |             |
| sel_trde_ori_nm_4 | 매도거래원명4 | String | N        | 20     |             |
| sel_trde_ori_4    | 매도거래원4   | String | N        | 20     |             |
| sel_trde_qty_4    | 매도거래량4   | String | N        | 20     |             |
| buy_trde_ori_nm_4 | 매수거래원명4 | String | N        | 20     |             |
| buy_trde_ori_4    | 매수거래원4   | String | N        | 20     |             |
| buy_trde_qty_4    | 매수거래량4   | String | N        | 20     |             |
| sel_trde_ori_nm_5 | 매도거래원명5 | String | N        | 20     |             |
| sel_trde_ori_5    | 매도거래원5   | String | N        | 20     |             |
| sel_trde_qty_5    | 매도거래량5   | String | N        | 20     |             |
| buy_trde_ori_nm_5 | 매수거래원명5 | String | N        | 20     |             |
| buy_trde_ori_5    | 매수거래원5   | String | N        | 20     |             |
| buy_trde_qty_5    | 매수거래량5   | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
  "stk_cd": "005930",
  "stk_nm": "삼성전자",
  "cur_prc": "95400",
  "flu_smbol": "3",
  "base_pric": "95400",
  "pred_pre": "0",
  "flu_rt": "0.00",
  "sel_trde_ori_nm_1": "",
  "sel_trde_ori_1": "000",
  "sel_trde_qty_1": "0",
  "buy_trde_ori_nm_1": "",
  "buy_trde_ori_1": "000",
  "buy_trde_qty_1": "0",
  "sel_trde_ori_nm_2": "",
  "sel_trde_ori_2": "000",
  "sel_trde_qty_2": "0",
  "buy_trde_ori_nm_2": "",
  "buy_trde_ori_2": "000",
  "buy_trde_qty_2": "0",
  "sel_trde_ori_nm_3": "",
  "sel_trde_ori_3": "000",
  "sel_trde_qty_3": "0",
  "buy_trde_ori_nm_3": "",
  "buy_trde_ori_3": "000",
  "buy_trde_qty_3": "0",
  "sel_trde_ori_nm_4": "",
  "sel_trde_ori_4": "000",
  "sel_trde_qty_4": "0",
  "buy_trde_ori_nm_4": "",
  "buy_trde_ori_4": "000",
  "buy_trde_qty_4": "0",
  "sel_trde_ori_nm_5": "",
  "sel_trde_ori_5": "000",
  "sel_trde_qty_5": "0",
  "buy_trde_ori_nm_5": "",
  "buy_trde_ori_5": "000",
  "buy_trde_qty_5": "0",
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 체결정보요청 (ka10003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                    |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description    |
| ------------------ | ---------------- | ------ | -------- | ------ | -------------- |
| cntr_infr          | 체결정보         | LIST   | N        |        |                |
| - tm               | 시간             | String | N        | 20     |                |
| - cur_prc          | 현재가           | String | N        | 20     |                |
| - pred_pre         | 전일대비         | String | N        | 20     |                |
| - pre_rt           | 대비율           | String | N        | 20     |                |
| - pri_sel_bid_unit | 우선매도호가단위 | String | N        | 20     |                |
| - pri_buy_bid_unit | 우선매수호가단위 | String | N        | 20     |                |
| - cntr_trde_qty    | 체결거래량       | String | N        | 20     |                |
| - sign             | sign             | String | N        | 20     |                |
| - acc_trde_qty     | 누적거래량       | String | N        | 20     |                |
| - acc_trde_prica   | 누적거래대금     | String | N        | 20     |                |
| - cntr_str         | 체결강도         | String | N        | 20     |                |
| - stex_tp          | 거래소구분       | String | N        | 20     | KRX, NXT, 통합 |

#### 요청 예시

```json
{
  "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
  "cntr_infr": [
    {
      "tm": "130429",
      "cur_prc": "+53500",
      "pred_pre": "+500",
      "pre_rt": "+0.94",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+53500",
      "cntr_trde_qty": "1010",
      "sign": "2",
      "acc_trde_qty": "8735",
      "acc_trde_prica": "524269500",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    },
    {
      "tm": "130153",
      "cur_prc": "+68900",
      "pred_pre": "+15900",
      "pre_rt": "+30.00",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+55000",
      "cntr_trde_qty": "456",
      "sign": "1",
      "acc_trde_qty": "7725",
      "acc_trde_prica": "470234500",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    },
    {
      "tm": "125947",
      "cur_prc": "+55000",
      "pred_pre": "+2000",
      "pre_rt": "+3.77",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+55000",
      "cntr_trde_qty": "1000",
      "sign": "2",
      "acc_trde_qty": "7269",
      "acc_trde_prica": "438816100",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    },
    {
      "tm": "125153",
      "cur_prc": "+68900",
      "pred_pre": "+15900",
      "pre_rt": "+30.00",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+60100",
      "cntr_trde_qty": "2",
      "sign": "1",
      "acc_trde_qty": "6269",
      "acc_trde_prica": "383816100",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    },
    {
      "tm": "124721",
      "cur_prc": "+68900",
      "pred_pre": "+15900",
      "pre_rt": "+30.00",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+60100",
      "cntr_trde_qty": "2",
      "sign": "1",
      "acc_trde_qty": "6267",
      "acc_trde_prica": "383678300",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    },
    {
      "tm": "124507",
      "cur_prc": "+67100",
      "pred_pre": "+14100",
      "pre_rt": "+26.60",
      "pri_sel_bid_unit": "+68900",
      "pri_buy_bid_unit": "+67500",
      "cntr_trde_qty": "-5",
      "sign": "2",
      "acc_trde_qty": "6265",
      "acc_trde_prica": "383540500",
      "cntr_str": "12.99",
      "stex_tp": "KRX"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 신용매매동향요청 (ka10013)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                    |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| dt      | 일자     | String | Y        | 8      | YYYYMMDD                                                       |
| qry_tp  | 조회구분 | String | Y        | 1      | 1:융자, 2:대주                                                 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| crd_trde_trend | 신용매매동향 | LIST   | N        |        |             |
| - dt           | 일자         | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - trde_qty     | 거래량       | String | N        | 20     |             |
| - new          | 신규         | String | N        | 20     |             |
| - rpya         | 상환         | String | N        | 20     |             |
| - remn         | 잔고         | String | N        | 20     |             |
| - amt          | 금액         | String | N        | 20     |             |
| - pre          | 대비         | String | N        | 20     |             |
| - shr_rt       | 공여율       | String | N        | 20     |             |
| - remn_rt      | 잔고율       | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "dt": "20241104",
  "qry_tp": "1"
}
```

#### 응답 예시

```json
{
  "crd_trde_trend": [
    {
      "dt": "20241101",
      "cur_prc": "65100",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "trde_qty": "0",
      "new": "",
      "rpya": "",
      "remn": "",
      "amt": "",
      "pre": "",
      "shr_rt": "",
      "remn_rt": ""
    },
    {
      "dt": "20241031",
      "cur_prc": "65100",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "trde_qty": "0",
      "new": "",
      "rpya": "",
      "remn": "",
      "amt": "",
      "pre": "",
      "shr_rt": "",
      "remn_rt": ""
    },
    {
      "dt": "20241030",
      "cur_prc": "+65100",
      "pred_pre_sig": "2",
      "pred_pre": "+100",
      "trde_qty": "1",
      "new": "",
      "rpya": "",
      "remn": "",
      "amt": "",
      "pre": "",
      "shr_rt": "",
      "remn_rt": ""
    },
    {
      "dt": "20241029",
      "cur_prc": "-65000",
      "pred_pre_sig": "5",
      "pred_pre": "-27300",
      "trde_qty": "4",
      "new": "",
      "rpya": "",
      "remn": "",
      "amt": "",
      "pre": "",
      "shr_rt": "",
      "remn_rt": ""
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 일별거래상세요청 (ka10015)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                    |
| ------- | -------- | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| strt_dt | 시작일자 | String | Y        | 8      | YYYYMMDD                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                   | 한글명           | Type   | Required | Length | Description |
| ------------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| daly_trde_dtl             | 일별거래상세     | LIST   | N        |        |             |
| - dt                      | 일자             | String | N        | 20     |             |
| - close_pric              | 종가             | String | N        | 20     |             |
| - pred_pre_sig            | 전일대비기호     | String | N        | 20     |             |
| - pred_pre                | 전일대비         | String | N        | 20     |             |
| - flu_rt                  | 등락율           | String | N        | 20     |             |
| - trde_qty                | 거래량           | String | N        | 20     |             |
| - trde_prica              | 거래대금         | String | N        | 20     |             |
| - bf_mkrt_trde_qty        | 장전거래량       | String | N        | 20     |             |
| - bf_mkrt_trde_wght       | 장전거래비중     | String | N        | 20     |             |
| - opmr_trde_qty           | 장중거래량       | String | N        | 20     |             |
| - opmr_trde_wght          | 장중거래비중     | String | N        | 20     |             |
| - af_mkrt_trde_qty        | 장후거래량       | String | N        | 20     |             |
| - af_mkrt_trde_wght       | 장후거래비중     | String | N        | 20     |             |
| - tot_3                   | 합계3            | String | N        | 20     |             |
| - prid_trde_qty           | 기간중거래량     | String | N        | 20     |             |
| - cntr_str                | 체결강도         | String | N        | 20     |             |
| - for_poss                | 외인보유         | String | N        | 20     |             |
| - for_wght                | 외인비중         | String | N        | 20     |             |
| - for_netprps             | 외인순매수       | String | N        | 20     |             |
| - orgn_netprps            | 기관순매수       | String | N        | 20     |             |
| - ind_netprps             | 개인순매수       | String | N        | 20     |             |
| - frgn                    | 외국계           | String | N        | 20     |             |
| - crd_remn_rt             | 신용잔고율       | String | N        | 20     |             |
| - prm                     | 프로그램         | String | N        | 20     |             |
| - bf_mkrt_trde_prica      | 장전거래대금     | String | N        | 20     |             |
| - bf_mkrt_trde_prica_wght | 장전거래대금비중 | String | N        | 20     |             |
| - opmr_trde_prica         | 장중거래대금     | String | N        | 20     |             |
| - opmr_trde_prica_wght    | 장중거래대금비중 | String | N        | 20     |             |
| - af_mkrt_trde_prica      | 장후거래대금     | String | N        | 20     |             |
| - af_mkrt_trde_prica_wght | 장후거래대금비중 | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "strt_dt": "20241105"
}
```

#### 응답 예시

```json
{
  "daly_trde_dtl": [
    {
      "dt": "20241105",
      "close_pric": "135300",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "trde_qty": "0",
      "trde_prica": "0",
      "bf_mkrt_trde_qty": "",
      "bf_mkrt_trde_wght": "",
      "opmr_trde_qty": "",
      "opmr_trde_wght": "",
      "af_mkrt_trde_qty": "",
      "af_mkrt_trde_wght": "",
      "tot_3": "0",
      "prid_trde_qty": "0",
      "cntr_str": "",
      "for_poss": "",
      "for_wght": "",
      "for_netprps": "",
      "orgn_netprps": "",
      "ind_netprps": "",
      "frgn": "",
      "crd_remn_rt": "",
      "prm": "",
      "bf_mkrt_trde_prica": "",
      "bf_mkrt_trde_prica_wght": "",
      "opmr_trde_prica": "",
      "opmr_trde_prica_wght": "",
      "af_mkrt_trde_prica": "",
      "af_mkrt_trde_prica_wght": ""
    },
    {
      "dt": "20241101",
      "close_pric": "65100",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "trde_qty": "0",
      "trde_prica": "0",
      "bf_mkrt_trde_qty": "",
      "bf_mkrt_trde_wght": "",
      "opmr_trde_qty": "",
      "opmr_trde_wght": "",
      "af_mkrt_trde_qty": "",
      "af_mkrt_trde_wght": "",
      "tot_3": "0",
      "prid_trde_qty": "0",
      "cntr_str": "",
      "for_poss": "",
      "for_wght": "",
      "for_netprps": "",
      "orgn_netprps": "",
      "ind_netprps": "",
      "frgn": "",
      "crd_remn_rt": "",
      "prm": "",
      "bf_mkrt_trde_prica": "",
      "bf_mkrt_trde_prica_wght": "",
      "opmr_trde_prica": "",
      "opmr_trde_prica_wght": "",
      "af_mkrt_trde_prica": "",
      "af_mkrt_trde_prica_wght": ""
    },
    {
      "dt": "20241031",
      "close_pric": "65100",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "trde_qty": "0",
      "trde_prica": "0",
      "bf_mkrt_trde_qty": "",
      "bf_mkrt_trde_wght": "",
      "opmr_trde_qty": "",
      "opmr_trde_wght": "",
      "af_mkrt_trde_qty": "",
      "af_mkrt_trde_wght": "",
      "tot_3": "0",
      "prid_trde_qty": "0",
      "cntr_str": "",
      "for_poss": "",
      "for_wght": "",
      "for_netprps": "",
      "orgn_netprps": "",
      "ind_netprps": "",
      "frgn": "",
      "crd_remn_rt": "",
      "prm": "",
      "bf_mkrt_trde_prica": "",
      "bf_mkrt_trde_prica_wght": "",
      "opmr_trde_prica": "",
      "opmr_trde_prica_wght": "",
      "af_mkrt_trde_prica": "",
      "af_mkrt_trde_prica_wght": ""
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 신고저가요청 (ka10016)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element           | 한글명     | Type   | Required | Length | Description                                                                                                                                                 |
| ----------------- | ---------- | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp           | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                            |
| ntl_tp            | 신고저구분 | String | Y        | 1      | 1:신고가, 2:신저가                                                                                                                                          |
| high_low_close_tp | 고저종구분 | String | Y        | 1      | 1:고저기준, 2:종가기준                                                                                                                                      |
| stk_cnd           | 종목조건   | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기                                                            |
| trde_qty_tp       | 거래량구분 | String | Y        | 5      | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| crd_cnd           | 신용조건   | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                                      |
| updown_incls      | 상하한포함 | String | Y        | 1      | 0:미포함, 1:포함                                                                                                                                            |
| dt                | 기간       | String | Y        | 3      | 5:5일, 10:10일, 20:20일, 60:60일, 250:250일, 250일까지 입력가능                                                                                             |
| stex_tp           | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                        |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| ntl_pric               | 신고저가         | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호     | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - flu_rt               | 등락률           | String | N        | 20     |             |
| - trde_qty             | 거래량           | String | N        | 20     |             |
| - pred_trde_qty_pre_rt | 전일거래량대비율 | String | N        | 20     |             |
| - sel_bid              | 매도호가         | String | N        | 20     |             |
| - buy_bid              | 매수호가         | String | N        | 20     |             |
| - high_pric            | 고가             | String | N        | 20     |             |
| - low_pric             | 저가             | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "ntl_tp": "1",
  "high_low_close_tp": "1",
  "stk_cnd": "0",
  "trde_qty_tp": "00000",
  "crd_cnd": "0",
  "updown_incls": "0",
  "dt": "5",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "ntl_pric": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "334",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "trde_qty": "3",
      "pred_trde_qty_pre_rt": "-0.00",
      "sel_bid": "0",
      "buy_bid": "0",
      "high_pric": "334",
      "low_pric": "320"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-6230",
      "pred_pre_sig": "5",
      "pred_pre": "-60",
      "flu_rt": "-0.95",
      "trde_qty": "77",
      "pred_trde_qty_pre_rt": "-6.16",
      "sel_bid": "+6300",
      "buy_bid": "-6270",
      "high_pric": "6340",
      "low_pric": "6150"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-140000",
      "pred_pre_sig": "5",
      "pred_pre": "-800",
      "flu_rt": "-0.57",
      "trde_qty": "7",
      "pred_trde_qty_pre_rt": "-0.00",
      "sel_bid": "-140000",
      "buy_bid": "0",
      "high_pric": "140800",
      "low_pric": "70000"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+214000",
      "pred_pre_sig": "2",
      "pred_pre": "+20900",
      "flu_rt": "+10.82",
      "trde_qty": "45",
      "pred_trde_qty_pre_rt": "-0.05",
      "sel_bid": "0",
      "buy_bid": "+214000",
      "high_pric": "214000",
      "low_pric": "89800"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-89000",
      "pred_pre_sig": "5",
      "pred_pre": "-8400",
      "flu_rt": "-8.62",
      "trde_qty": "130",
      "pred_trde_qty_pre_rt": "-0.01",
      "sel_bid": "0",
      "buy_bid": "-89000",
      "high_pric": "97500",
      "low_pric": "58800"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+40300",
      "pred_pre_sig": "2",
      "pred_pre": "+1150",
      "flu_rt": "+2.94",
      "trde_qty": "86",
      "pred_trde_qty_pre_rt": "-0.13",
      "sel_bid": "+40550",
      "buy_bid": "+40300",
      "high_pric": "40300",
      "low_pric": "14000"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-190000",
      "pred_pre_sig": "5",
      "pred_pre": "-4000",
      "flu_rt": "-2.06",
      "trde_qty": "137",
      "pred_trde_qty_pre_rt": "-0.00",
      "sel_bid": "0",
      "buy_bid": "-182000",
      "high_pric": "195000",
      "low_pric": "67300"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 상하한가요청 (ka10017)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명     | Type   | Required | Length | Description                                                                                                                                                                |
| ------------ | ---------- | ------ | -------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp      | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                           |
| updown_tp    | 상하한구분 | String | Y        | 1      | 1:상한, 2:상승, 3:보합, 4:하한, 5:하락, 6:전일상한, 7:전일하한                                                                                                             |
| sort_tp      | 정렬구분   | String | Y        | 1      | 1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순                                                                                                                          |
| stk_cnd      | 종목조건   | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기, 9:증20만 보기, 10:우선주+관리종목+환기종목제외 |
| trde_qty_tp  | 거래량구분 | String | Y        | 5      | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상                |
| crd_cnd      | 신용조건   | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                                                     |
| trde_gold_tp | 매매금구분 | String | Y        | 1      | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상                                                                             |
| stex_tp      | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element         | 한글명       | Type   | Required | Length | Description |
| --------------- | ------------ | ------ | -------- | ------ | ----------- |
| updown_pric     | 상하한가     | LIST   | N        |        |             |
| - stk_cd        | 종목코드     | String | N        | 20     |             |
| - stk_infr      | 종목정보     | String | N        | 20     |             |
| - stk_nm        | 종목명       | String | N        | 20     |             |
| - cur_prc       | 현재가       | String | N        | 20     |             |
| - pred_pre_sig  | 전일대비기호 | String | N        | 20     |             |
| - pred_pre      | 전일대비     | String | N        | 20     |             |
| - flu_rt        | 등락률       | String | N        | 20     |             |
| - trde_qty      | 거래량       | String | N        | 20     |             |
| - pred_trde_qty | 전일거래량   | String | N        | 20     |             |
| - sel_req       | 매도잔량     | String | N        | 20     |             |
| - sel_bid       | 매도호가     | String | N        | 20     |             |
| - buy_bid       | 매수호가     | String | N        | 20     |             |
| - buy_req       | 매수잔량     | String | N        | 20     |             |
| - cnt           | 횟수         | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "updown_tp": "1",
  "sort_tp": "1",
  "stk_cnd": "0",
  "trde_qty_tp": "0000",
  "crd_cnd": "0",
  "trde_gold_tp": "0",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "updown_pric": [
    {
      "stk_cd": "005930",
      "stk_infr": "",
      "stk_nm": "삼성전자",
      "cur_prc": "+235500",
      "pred_pre_sig": "1",
      "pred_pre": "+54200",
      "flu_rt": "+29.90",
      "trde_qty": "0",
      "pred_trde_qty": "96197",
      "sel_req": "0",
      "sel_bid": "0",
      "buy_bid": "+235500",
      "buy_req": "4",
      "cnt": "1"
    },
    {
      "stk_cd": "005930",
      "stk_infr": "",
      "stk_nm": "삼성전자",
      "cur_prc": "+13715",
      "pred_pre_sig": "1",
      "pred_pre": "+3165",
      "flu_rt": "+30.00",
      "trde_qty": "0",
      "pred_trde_qty": "929670",
      "sel_req": "0",
      "sel_bid": "0",
      "buy_bid": "+13715",
      "buy_req": "4",
      "cnt": "1"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 고저가근접요청 (ka10018)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명     | Type   | Required | Length | Description                                                                                                                                                 |
| ----------- | ---------- | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high_low_tp | 고저구분   | String | Y        | 1      | 1:고가, 2:저가                                                                                                                                              |
| alacc_rt    | 근접율     | String | Y        | 2      | 05:0.5, 10:1.0, 15:1.5, 20:2.0, 25:2.5, 30:3.0                                                                                                              |
| mrkt_tp     | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                            |
| trde_qty_tp | 거래량구분 | String | Y        | 5      | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| stk_cnd     | 종목조건   | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기                                                            |
| crd_cnd     | 신용조건   | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                                      |
| stex_tp     | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                        |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element             | 한글명       | Type   | Required | Length | Description |
| ------------------- | ------------ | ------ | -------- | ------ | ----------- |
| high_low_pric_alacc | 고저가근접   | LIST   | N        |        |             |
| - stk_cd            | 종목코드     | String | N        | 20     |             |
| - stk_nm            | 종목명       | String | N        | 20     |             |
| - cur_prc           | 현재가       | String | N        | 20     |             |
| - pred_pre_sig      | 전일대비기호 | String | N        | 20     |             |
| - pred_pre          | 전일대비     | String | N        | 20     |             |
| - flu_rt            | 등락율       | String | N        | 20     |             |
| - flu_rt            | 등락률       | String | N        | 20     |             |
| - trde_qty          | 거래량       | String | N        | 20     |             |
| - sel_bid           | 매도호가     | String | N        | 20     |             |
| - buy_bid           | 매수호가     | String | N        | 20     |             |
| - tdy_high_pric     | 당일고가     | String | N        | 20     |             |
| - tdy_low_pric      | 당일저가     | String | N        | 20     |             |

#### 요청 예시

```json
{
  "high_low_tp": "1",
  "alacc_rt": "05",
  "mrkt_tp": "000",
  "trde_qty_tp": "0000",
  "stk_cnd": "0",
  "crd_cnd": "0",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "high_low_pric_alacc": [
    {
      "stk_cd": "004930",
      "stk_nm": "삼성전자",
      "cur_prc": "334",
      "pred_pre_sig": "0",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "trde_qty": "3",
      "sel_bid": "0",
      "buy_bid": "0",
      "tdy_high_pric": "334",
      "tdy_low_pric": "334"
    },
    {
      "stk_cd": "004930",
      "stk_nm": "삼성전자",
      "cur_prc": "+7470",
      "pred_pre_sig": "2",
      "pred_pre": "+90",
      "flu_rt": "+1.22",
      "trde_qty": "2",
      "sel_bid": "0",
      "buy_bid": "-7320",
      "tdy_high_pric": "+7470",
      "tdy_low_pric": "+7470"
    },
    {
      "stk_cd": "004930",
      "stk_nm": "삼성전자",
      "cur_prc": "+214000",
      "pred_pre_sig": "60",
      "pred_pre": "+20900",
      "flu_rt": "+10.82",
      "trde_qty": "45",
      "sel_bid": "0",
      "buy_bid": "+214000",
      "tdy_high_pric": "+214000",
      "tdy_low_pric": "193100"
    },
    {
      "stk_cd": "004930",
      "stk_nm": "삼성전자",
      "cur_prc": "+40300",
      "pred_pre_sig": "114",
      "pred_pre": "+1150",
      "flu_rt": "+2.94",
      "trde_qty": "86",
      "sel_bid": "+40550",
      "buy_bid": "+40300",
      "tdy_high_pric": "+40300",
      "tdy_low_pric": "39150"
    },
    {
      "stk_cd": "004930",
      "stk_nm": "삼성전자",
      "cur_prc": "-10060",
      "pred_pre_sig": "0",
      "pred_pre": "-1790",
      "flu_rt": "-15.11",
      "trde_qty": "1",
      "sel_bid": "-10060",
      "buy_bid": "0",
      "tdy_high_pric": "-10060",
      "tdy_low_pric": "-10060"
    },
    {
      "stk_cd": "008370",
      "stk_nm": "원풍",
      "cur_prc": "+4970",
      "pred_pre_sig": "0",
      "pred_pre": "+15",
      "flu_rt": "+0.30",
      "trde_qty": "500",
      "sel_bid": "0",
      "buy_bid": "0",
      "tdy_high_pric": "+4970",
      "tdy_low_pric": "+4970"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 가격급등락요청 (ka10019)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명     | Type   | Required | Length | Description                                                                                                                                                 |
| ------------ | ---------- | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp      | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥, 201:코스피200                                                                                                             |
| flu_tp       | 등락구분   | String | Y        | 1      | 1:급등, 2:급락                                                                                                                                              |
| tm_tp        | 시간구분   | String | Y        | 1      | 1:분전, 2:일전                                                                                                                                              |
| tm           | 시간       | String | Y        | 2      | 분 혹은 일 입력                                                                                                                                             |
| trde_qty_tp  | 거래량구분 | String | Y        | 4      | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| stk_cnd      | 종목조건   | String | Y        | 1      | 0:전체조회, 1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기                                                            |
| crd_cnd      | 신용조건   | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                                      |
| pric_cnd     | 가격조건   | String | Y        | 1      | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상                                                              |
| updown_incls | 상하한포함 | String | Y        | 1      | 0:미포함, 1:포함                                                                                                                                            |
| stex_tp      | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                        |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| pric_jmpflu    | 가격급등락   | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_cls      | 종목분류     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - flu_rt       | 등락률       | String | N        | 20     |             |
| - base_pric    | 기준가       | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - base_pre     | 기준대비     | String | N        | 20     |             |
| - trde_qty     | 거래량       | String | N        | 20     |             |
| - jmp_rt       | 급등률       | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "flu_tp": "1",
  "tm_tp": "1",
  "tm": "60",
  "trde_qty_tp": "0000",
  "stk_cnd": "0",
  "crd_cnd": "0",
  "pric_cnd": "0",
  "updown_incls": "1",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "pric_jmpflu": [
    {
      "stk_cd": "005930",
      "stk_cls": "",
      "stk_nm": "삼성전자",
      "pred_pre_sig": "2",
      "pred_pre": "+300",
      "flu_rt": "+0.57",
      "base_pric": "51600",
      "cur_prc": "+52700",
      "base_pre": "1100",
      "trde_qty": "2400",
      "jmp_rt": "+2.13"
    },
    {
      "stk_cd": "005930",
      "stk_cls": "",
      "stk_nm": "삼성전자",
      "pred_pre_sig": "5",
      "pred_pre": "-24200",
      "flu_rt": "-26.68",
      "base_pric": "66000",
      "cur_prc": "-66500",
      "base_pre": "500",
      "trde_qty": "577",
      "jmp_rt": "+0.76"
    },
    {
      "stk_cd": "005930",
      "stk_cls": "",
      "stk_nm": "삼성전자",
      "pred_pre_sig": "2",
      "pred_pre": "+10",
      "flu_rt": "+0.06",
      "base_pric": "16370",
      "cur_prc": "+16380",
      "base_pre": "10",
      "trde_qty": "102",
      "jmp_rt": "+0.06"
    },
    {
      "stk_cd": "005930",
      "stk_cls": "",
      "stk_nm": "삼성전자",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "base_pric": "334",
      "cur_prc": "334",
      "base_pre": "0",
      "trde_qty": "3",
      "jmp_rt": "0.00"
    },
    {
      "stk_cd": "005930",
      "stk_cls": "",
      "stk_nm": "삼성전자",
      "pred_pre_sig": "2",
      "pred_pre": "+90",
      "flu_rt": "+1.22",
      "base_pric": "7470",
      "cur_prc": "+7470",
      "base_pre": "0",
      "trde_qty": "2",
      "jmp_rt": "0.00"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 거래량갱신요청 (ka10024)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element     | 한글명     | Type   | Required | Length | Description                                                                                                             |
| ----------- | ---------- | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp     | 시장구분   | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                        |
| cycle_tp    | 주기구분   | String | Y        | 1      | 5:5일, 10:10일, 20:20일, 60:60일, 250:250일                                                                             |
| trde_qty_tp | 거래량구분 | String | Y        | 1      | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상 |
| stex_tp     | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                    |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element         | 한글명       | Type   | Required | Length | Description |
| --------------- | ------------ | ------ | -------- | ------ | ----------- |
| trde_qty_updt   | 거래량갱신   | LIST   | N        |        |             |
| - stk_cd        | 종목코드     | String | N        | 20     |             |
| - stk_nm        | 종목명       | String | N        | 20     |             |
| - cur_prc       | 현재가       | String | N        | 20     |             |
| - pred_pre_sig  | 전일대비기호 | String | N        | 20     |             |
| - pred_pre      | 전일대비     | String | N        | 20     |             |
| - flu_rt        | 등락률       | String | N        | 20     |             |
| - prev_trde_qty | 이전거래량   | String | N        | 20     |             |
| - now_trde_qty  | 현재거래량   | String | N        | 20     |             |
| - sel_bid       | 매도호가     | String | N        | 20     |             |
| - buy_bid       | 매수호가     | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "cycle_tp": "5",
  "trde_qty_tp": "5",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "trde_qty_updt": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+74800",
      "pred_pre_sig": "1",
      "pred_pre": "+17200",
      "flu_rt": "+29.86",
      "prev_trde_qty": "243520",
      "now_trde_qty": "435771",
      "sel_bid": "0",
      "buy_bid": "+74800"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-42900",
      "pred_pre_sig": "5",
      "pred_pre": "-150",
      "flu_rt": "-0.35",
      "prev_trde_qty": "25377975",
      "now_trde_qty": "31399114",
      "sel_bid": "-42900",
      "buy_bid": "+45250"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-152000",
      "pred_pre_sig": "5",
      "pred_pre": "-100",
      "flu_rt": "-0.07",
      "prev_trde_qty": "22435675",
      "now_trde_qty": "31491771",
      "sel_bid": "-152000",
      "buy_bid": "-151900"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-65300",
      "pred_pre_sig": "5",
      "pred_pre": "-100",
      "flu_rt": "-0.15",
      "prev_trde_qty": "25114462",
      "now_trde_qty": "26395169",
      "sel_bid": "-65300",
      "buy_bid": "+74900"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 매물대집중요청 (ka10025)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element       | 한글명       | Type   | Required | Length | Description                                                    |
| ------------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| mrkt_tp       | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                               |
| prps_cnctr_rt | 매물집중비율 | String | Y        | 3      | 0~100 입력                                                     |
| cur_prc_entry | 현재가진입   | String | Y        | 1      | 0:현재가 매물대 진입 포함안함, 1:현재가 매물대 진입포함        |
| prpscnt       | 매물대수     | String | Y        | 2      | 숫자입력                                                       |
| cycle_tp      | 주기구분     | String | Y        | 2      | 50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일 |
| stex_tp       | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| prps_cnctr     | 매물대집중   | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - flu_rt       | 등락률       | String | N        | 20     |             |
| - now_trde_qty | 현재거래량   | String | N        | 20     |             |
| - pric_strt    | 가격대시작   | String | N        | 20     |             |
| - pric_end     | 가격대끝     | String | N        | 20     |             |
| - prps_qty     | 매물량       | String | N        | 20     |             |
| - prps_rt      | 매물비       | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "prps_cnctr_rt": "50",
  "cur_prc_entry": "0",
  "prpscnt": "10",
  "cycle_tp": "50",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "prps_cnctr": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "30000",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "pric_strt": "31350",
      "pric_end": "31799",
      "prps_qty": "4",
      "prps_rt": "+50.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "30000",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "pric_strt": "32700",
      "pric_end": "33149",
      "prps_qty": "4",
      "prps_rt": "+50.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "109",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "1",
      "pric_strt": "109",
      "pric_end": "326",
      "prps_qty": "8",
      "prps_rt": "+50.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "2555",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "pric_strt": "2669",
      "pric_end": "2685",
      "prps_qty": "4",
      "prps_rt": "+50.00"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 고저PER요청 (ka10026)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                          |
| ------- | ---------- | ------ | -------- | ------ | ---------------------------------------------------- |
| pertp   | PER구분    | String | Y        | 1      | 1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element        | 한글명       | Type   | Required | Length | Description |
| -------------- | ------------ | ------ | -------- | ------ | ----------- |
| high_low_per   | 고저PER      | LIST   | N        |        |             |
| - stk_cd       | 종목코드     | String | N        | 20     |             |
| - stk_nm       | 종목명       | String | N        | 20     |             |
| - per          | PER          | String | N        | 20     |             |
| - cur_prc      | 현재가       | String | N        | 20     |             |
| - pred_pre_sig | 전일대비기호 | String | N        | 20     |             |
| - pred_pre     | 전일대비     | String | N        | 20     |             |
| - flu_rt       | 등락율       | String | N        | 20     |             |
| - now_trde_qty | 현재거래량   | String | N        | 20     |             |
| - sel_bid      | 매도호가     | String | N        | 20     |             |

#### 요청 예시

```json
{
  "pertp": "1",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "high_low_per": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "per": "0.44",
      "cur_prc": "4930",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "sel_bid": "0"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "per": "0.54",
      "cur_prc": "5980",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "sel_bid": "0"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "per": "0.71",
      "cur_prc": "3445",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "sel_bid": "0"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "per": "0.71",
      "cur_prc": "83",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "sel_bid": "0"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "per": "0.82",
      "cur_prc": "7820",
      "pred_pre_sig": "3",
      "pred_pre": "0",
      "flu_rt": "0.00",
      "now_trde_qty": "0",
      "sel_bid": "7820"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 시가대비등락률요청 (ka10028)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                                                                                                                              |
| -------------- | ------------ | ------ | -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sort_tp        | 정렬구분     | String | Y        | 1      | 1:시가, 2:고가, 3:저가, 4:기준가                                                                                                                                                         |
| trde_qty_cnd   | 거래량조건   | String | Y        | 4      | 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0500:50만주이상, 1000:백만주이상                                                                                          |
| mrkt_tp        | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                         |
| updown_incls   | 상하한포함   | String | Y        | 1      | 0:불 포함, 1:포함                                                                                                                                                                        |
| stk_cnd        | 종목조건     | String | Y        | 2      | 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기                                                      |
| crd_cnd        | 신용조건     | String | Y        | 1      | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체                                                                                                   |
| trde_prica_cnd | 거래대금조건 | String | Y        | 4      | 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상 |
| flu_cnd        | 등락조건     | String | Y        | 1      | 1:상위, 2:하위                                                                                                                                                                           |
| stex_tp        | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                                                     |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명         | Type   | Required | Length | Description |
| -------------------- | -------------- | ------ | -------- | ------ | ----------- |
| open_pric_pre_flu_rt | 시가대비등락률 | LIST   | N        |        |             |
| - stk_cd             | 종목코드       | String | N        | 20     |             |
| - stk_nm             | 종목명         | String | N        | 20     |             |
| - cur_prc            | 현재가         | String | N        | 20     |             |
| - pred_pre_sig       | 전일대비기호   | String | N        | 20     |             |
| - pred_pre           | 전일대비       | String | N        | 20     |             |
| - flu_rt             | 등락률         | String | N        | 20     |             |
| - open_pric          | 시가           | String | N        | 20     |             |
| - high_pric          | 고가           | String | N        | 20     |             |
| - low_pric           | 저가           | String | N        | 20     |             |
| - open_pric_pre      | 시가대비       | String | N        | 20     |             |
| - now_trde_qty       | 현재거래량     | String | N        | 20     |             |
| - cntr_str           | 체결강도       | String | N        | 20     |             |

#### 요청 예시

```json
{
  "sort_tp": "1",
  "trde_qty_cnd": "0000",
  "mrkt_tp": "000",
  "updown_incls": "1",
  "stk_cnd": "0",
  "crd_cnd": "0",
  "trde_prica_cnd": "0",
  "flu_cnd": "1",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "open_pric_pre_flu_rt": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+74800",
      "pred_pre_sig": "1",
      "pred_pre": "+17200",
      "flu_rt": "+29.86",
      "open_pric": "+65000",
      "high_pric": "+74800",
      "low_pric": "-57000",
      "open_pric_pre": "+15.08",
      "now_trde_qty": "448203",
      "cntr_str": "346.54"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-200000",
      "pred_pre_sig": "5",
      "pred_pre": "-15000",
      "flu_rt": "-6.98",
      "open_pric": "-180000",
      "high_pric": "215000",
      "low_pric": "-180000",
      "open_pric_pre": "+11.11",
      "now_trde_qty": "619",
      "cntr_str": "385.07"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+200000",
      "pred_pre_sig": "2",
      "pred_pre": "+15600",
      "flu_rt": "+8.46",
      "open_pric": "184400",
      "high_pric": "+200000",
      "low_pric": "-183500",
      "open_pric_pre": "+8.46",
      "now_trde_qty": "143",
      "cntr_str": "500.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+140100",
      "pred_pre_sig": "2",
      "pred_pre": "+4100",
      "flu_rt": "+3.01",
      "open_pric": "+136100",
      "high_pric": "+150000",
      "low_pric": "-129000",
      "open_pric_pre": "+2.94",
      "now_trde_qty": "135",
      "cntr_str": "136.36"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 거래원매물대분석요청 (ka10043)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element   | 한글명       | Type   | Required | Length | Description                                                    |
| --------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd    | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| strt_dt   | 시작일자     | String | Y        | 8      | YYYYMMDD                                                       |
| end_dt    | 종료일자     | String | Y        | 8      | YYYYMMDD                                                       |
| qry_dt_tp | 조회기간구분 | String | Y        | 1      | 0:기간으로 조회, 1:시작일자, 종료일자로 조회                   |
| pot_tp    | 시점구분     | String | Y        | 1      | 0:당일, 1:전일                                                 |
| dt        | 기간         | String | Y        | 4      | 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일           |
| sort_base | 정렬기준     | String | Y        | 1      | 1:종가순, 2:날짜순                                             |
| mmcm_cd   | 회원사코드   | String | Y        | 3      | 회원사 코드는 ka10102 조회                                     |
| stex_tp   | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                           |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description |
| ------------------ | ---------------- | ------ | -------- | ------ | ----------- |
| trde_ori_prps_anly | 거래원매물대분석 | LIST   | N        |        |             |
| - dt               | 일자             | String | N        | 20     |             |
| - close_pric       | 종가             | String | N        | 20     |             |
| - pre_sig          | 대비기호         | String | N        | 20     |             |
| - pred_pre         | 전일대비         | String | N        | 20     |             |
| - sel_qty          | 매도량           | String | N        | 20     |             |
| - buy_qty          | 매수량           | String | N        | 20     |             |
| - netprps_qty      | 순매수수량       | String | N        | 20     |             |
| - trde_qty_sum     | 거래량합         | String | N        | 20     |             |
| - trde_wght        | 거래비중         | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "strt_dt": "20241031",
  "end_dt": "20241107",
  "qry_dt_tp": "0",
  "pot_tp": "0",
  "dt": "5",
  "sort_base": "1",
  "mmcm_cd": "36",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "trde_ori_prps_anly": [
    {
      "dt": "20241105",
      "close_pric": "135300",
      "pre_sig": "2",
      "pred_pre": "+1700",
      "sel_qty": "43",
      "buy_qty": "1090",
      "netprps_qty": "1047",
      "trde_qty_sum": "1133",
      "trde_wght": "+1317.44"
    },
    {
      "dt": "20241107",
      "close_pric": "133600",
      "pre_sig": "3",
      "pred_pre": "0",
      "sel_qty": "0",
      "buy_qty": "0",
      "netprps_qty": "0",
      "trde_qty_sum": "0",
      "trde_wght": "0.00"
    },
    {
      "dt": "20241106",
      "close_pric": "132500",
      "pre_sig": "5",
      "pred_pre": "--1100",
      "sel_qty": "117",
      "buy_qty": "3459",
      "netprps_qty": "3342",
      "trde_qty_sum": "3576",
      "trde_wght": "+4158.14"
    },
    {
      "dt": "20241101",
      "close_pric": "65100",
      "pre_sig": "5",
      "pred_pre": "--68500",
      "sel_qty": "3728",
      "buy_qty": "12680",
      "netprps_qty": "8952",
      "trde_qty_sum": "16408",
      "trde_wght": "+19079.07"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 거래원순간거래량요청 (ka10052)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                                                                                   |
| ------- | ---------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------- |
| mmcm_cd | 회원사코드 | String | Y        | 3      | 회원사 코드는 ka10102 조회                                                                    |
| stk_cd  | 종목코드   | String | N        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)                                |
| mrkt_tp | 시장구분   | String | Y        | 1      | 0:전체, 1:코스피, 2:코스닥, 3:종목                                                            |
| qty_tp  | 수량구분   | String | Y        | 3      | 0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30:30000주, 50:50000주, 100:100000주          |
| pric_tp | 가격구분   | String | Y        | 1      | 0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원 이상 |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| trde_ori_mont_trde_qty | 거래원순간거래량 | LIST   | N        |        |             |
| - tm                   | 시간             | String | N        | 20     |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - trde_ori_nm          | 거래원명         | String | N        | 20     |             |
| - tp                   | 구분             | String | N        | 20     |             |
| - mont_trde_qty        | 순간거래량       | String | N        | 20     |             |
| - acc_netprps          | 누적순매수       | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - pred_pre_sig         | 전일대비기호     | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - flu_rt               | 등락율           | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mmcm_cd": "888",
  "stk_cd": "",
  "mrkt_tp": "0",
  "qty_tp": "0",
  "pric_tp": "0",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "trde_ori_mont_trde_qty": [
    {
      "tm": "161437",
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "trde_ori_nm": "다이와",
      "tp": "-매도",
      "mont_trde_qty": "-399928",
      "acc_netprps": "-1073004",
      "cur_prc": "+57700",
      "pred_pre_sig": "2",
      "pred_pre": "400",
      "flu_rt": "+0.70"
    },
    {
      "tm": "161423",
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "trde_ori_nm": "다이와",
      "tp": "-매도",
      "mont_trde_qty": "-100000",
      "acc_netprps": "-673076",
      "cur_prc": "+57700",
      "pred_pre_sig": "2",
      "pred_pre": "400",
      "flu_rt": "+0.70"
    },
    {
      "tm": "161417",
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "trde_ori_nm": "다이와",
      "tp": "-매도",
      "mont_trde_qty": "-100000",
      "acc_netprps": "-573076",
      "cur_prc": "+57700",
      "pred_pre_sig": "2",
      "pred_pre": "400",
      "flu_rt": "+0.70"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 변동성완화장치발동종목요청 (ka10054)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명       | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                               |
| -------------- | ------------ | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mrkt_tp        | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                                                                                                                                                                                                                                                                                          |
| bf_mkrt_tp     | 장전구분     | String | Y        | 1      | 0:전체, 1:정규시장, 2:시간외단일가                                                                                                                                                                                                                                                                                        |
| stk_cd         | 종목코드     | String | N        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)<br/>공백입력시 시장구분으로 설정한 전체종목조회                                                                                                                                                                                                            |
| motn_tp        | 발동구분     | String | Y        | 1      | 0:전체, 1:정적VI, 2:동적VI, 3:동적VI + 정적VI                                                                                                                                                                                                                                                                             |
| skip_stk       | 제외종목     | String | Y        | 9      | 전종목포함 조회시 9개 0으로 설정(000000000), 전종목제외 조회시 9개 1으로 설정(111111111), 9개 종목조회여부를 조회포함(0), 조회제외(1)로 설정하며 종목순서는 우선주, 관리종목, 투자경고/위험, 투자주의, 환기종목, 단기과열종목, 증거금100%, ETF, ETN가 됨. 우선주만 조회시 "011111111", 관리종목만 조회시 "101111111" 설정 |
| trde_qty_tp    | 거래량구분   | String | Y        | 1      | 0:사용안함, 1:사용                                                                                                                                                                                                                                                                                                        |
| min_trde_qty   | 최소거래량   | String | Y        | 12     | 0주 이상, 거래량구분이 1일때만 입력(공백허용)                                                                                                                                                                                                                                                                             |
| max_trde_qty   | 최대거래량   | String | Y        | 12     | 100000000주 이하, 거래량구분이 1일때만 입력(공백허용)                                                                                                                                                                                                                                                                     |
| trde_prica_tp  | 거래대금구분 | String | Y        | 1      | 0:사용안함, 1:사용                                                                                                                                                                                                                                                                                                        |
| min_trde_prica | 최소거래대금 | String | Y        | 10     | 0백만원 이상, 거래대금구분 1일때만 입력(공백허용)                                                                                                                                                                                                                                                                         |
| max_trde_prica | 최대거래대금 | String | Y        | 10     | 100000000백만원 이하, 거래대금구분 1일때만 입력(공백허용)                                                                                                                                                                                                                                                                 |
| motn_drc       | 발동방향     | String | Y        | 1      | 0:전체, 1:상승, 2:하락                                                                                                                                                                                                                                                                                                    |
| stex_tp        | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                                                                                                                                                                                                                                                      |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| motn_stk               | 발동종목         | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - acc_trde_qty         | 누적거래량       | String | N        | 20     |             |
| - motn_pric            | 발동가격         | String | N        | 20     |             |
| - dynm_dispty_rt       | 동적괴리율       | String | N        | 20     |             |
| - trde_cntr_proc_time  | 매매체결처리시각 | String | N        | 20     |             |
| - virelis_time         | VI해제시각       | String | N        | 20     |             |
| - viaplc_tp            | VI적용구분       | String | N        | 20     |             |
| - dynm_stdpc           | 동적기준가격     | String | N        | 20     |             |
| - static_stdpc         | 정적기준가격     | String | N        | 20     |             |
| - static_dispty_rt     | 정적괴리율       | String | N        | 20     |             |
| - open_pric_pre_flu_rt | 시가대비등락률   | String | N        | 20     |             |
| - vimotn_cnt           | VI발동횟수       | String | N        | 20     |             |
| - stex_tp              | 거래소구분       | String | N        | 20     |             |

#### 요청 예시

```json
{
  "mrkt_tp": "000",
  "bf_mkrt_tp": "0",
  "stk_cd": "",
  "motn_tp": "0",
  "skip_stk": "000000000",
  "trde_qty_tp": "0",
  "min_trde_qty": "0",
  "max_trde_qty": "0",
  "trde_prica_tp": "0",
  "min_trde_prica": "0",
  "max_trde_prica": "0",
  "motn_drc": "0",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "motn_stk": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "acc_trde_qty": "1105968",
      "motn_pric": "67000",
      "dynm_dispty_rt": "+9.30",
      "trde_cntr_proc_time": "172311",
      "virelis_time": "172511",
      "viaplc_tp": "동적",
      "dynm_stdpc": "61300",
      "static_stdpc": "0",
      "static_dispty_rt": "0.00",
      "open_pric_pre_flu_rt": "+16.93",
      "vimotn_cnt": "23",
      "stex_tp": "NXT"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "acc_trde_qty": "1105968",
      "motn_pric": "65000",
      "dynm_dispty_rt": "-3.13",
      "trde_cntr_proc_time": "170120",
      "virelis_time": "170320",
      "viaplc_tp": "동적",
      "dynm_stdpc": "67100",
      "static_stdpc": "0",
      "static_dispty_rt": "0.00",
      "open_pric_pre_flu_rt": "+13.44",
      "vimotn_cnt": "22",
      "stex_tp": "NXT"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "acc_trde_qty": "14",
      "motn_pric": "95100",
      "dynm_dispty_rt": "-1.96",
      "trde_cntr_proc_time": "163030",
      "virelis_time": "163224",
      "viaplc_tp": "동적",
      "dynm_stdpc": "97000",
      "static_stdpc": "0",
      "static_dispty_rt": "0.00",
      "open_pric_pre_flu_rt": "+0.11",
      "vimotn_cnt": "2",
      "stex_tp": "KRX"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "acc_trde_qty": "153",
      "motn_pric": "250000",
      "dynm_dispty_rt": "+22.55",
      "trde_cntr_proc_time": "163030",
      "virelis_time": "163224",
      "viaplc_tp": "동적+정적",
      "dynm_stdpc": "204000",
      "static_stdpc": "203500",
      "static_dispty_rt": "+22.85",
      "open_pric_pre_flu_rt": "+27.62",
      "vimotn_cnt": "3",
      "stex_tp": "KRX"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 당일전일체결량요청 (ka10055)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명   | Type   | Required | Length | Description                                                     |
| -------- | -------- | ------ | -------- | ------ | --------------------------------------------------------------- |
| stk_cd   | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)  |
| tdy_pred | 당일전일 | String | Y        | 1      | 당일 : 1, 전일 : 2                                              |
| tic_min  | 틱분     | String | Y        | 1      | 0:틱, 1:분                                                      |
| tm       | 시간     | String | N        | 4      | 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description      |
| ------------------ | ---------------- | ------ | -------- | ------ | ---------------- |
| tdy_pred_cntr      | 당일전일체결     | LIST   | N        |        |                  |
| - tm               | 시간             | String | N        | 20     |                  |
| - cur_prc          | 현재가           | String | N        | 20     |                  |
| - pred_pre         | 전일대비         | String | N        | 20     |                  |
| - pre_rt           | 대비율           | String | N        | 20     |                  |
| - pri_sel_bid_unit | 우선매도호가단위 | String | N        | 20     |                  |
| - pri_buy_bid_unit | 우선매수호가단위 | String | N        | 20     |                  |
| - cntr_trde_qty    | 체결거래량       | String | N        | 20     |                  |
| - sign             | 전일대비기호     | String | N        | 20     |                  |
| - acc_trde_qty     | 누적거래량       | String | N        | 20     |                  |
| - acc_trde_prica   | 누적거래대금     | String | N        | 20     |                  |
| - cntr_str         | 체결강도         | String | N        | 20     |                  |
| - stex_tp          | 거래소구분       | String | N        | 20     | KRX , NXT , 통합 |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "tdy_pred": "2",
  "tic_min": "0",
  "tm": ""
}
```

#### 응답 예시

```json
{
  "tdy_pred_cntr": [
    {
      "tm": "112711",
      "cur_prc": "+128300",
      "pred_pre": "+700",
      "pre_rt": "+0.55",
      "pri_sel_bid_unit": "-0",
      "pri_buy_bid_unit": "+128300",
      "cntr_trde_qty": "-1",
      "sign": "2",
      "acc_trde_qty": "2",
      "acc_trde_prica": "0",
      "cntr_str": "0.00"
    },
    {
      "tm": "111554",
      "cur_prc": "+128300",
      "pred_pre": "+700",
      "pre_rt": "+0.55",
      "pri_sel_bid_unit": "-0",
      "pri_buy_bid_unit": "+128300",
      "cntr_trde_qty": "-1",
      "sign": "2",
      "acc_trde_qty": "1",
      "acc_trde_prica": "0",
      "cntr_str": "0.00"
    }
  ],
  "returnCode": 0,
  "returnMsg": "정상적으로 처리되었습니다"
}
```

---

### 투자자별일별매매종목요청 (ka10058)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명     | Type   | Required | Length | Description                                                                                                                               |
| -------- | ---------- | ------ | -------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| strt_dt  | 시작일자   | String | Y        | 8      | YYYYMMDD                                                                                                                                  |
| end_dt   | 종료일자   | String | Y        | 8      | YYYYMMDD                                                                                                                                  |
| trde_tp  | 매매구분   | String | Y        | 1      | 순매도:1, 순매수:2                                                                                                                        |
| mrkt_tp  | 시장구분   | String | Y        | 3      | 001:코스피, 101:코스닥                                                                                                                    |
| invsr_tp | 투자자구분 | String | Y        | 4      | 8000:개인, 9000:외국인, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계 |
| stex_tp  | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT 3.통합                                                                                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element             | 한글명               | Type   | Required | Length | Description |
| ------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| invsr_daly_trde_stk | 투자자별일별매매종목 | LIST   | N        |        |             |
| - stk_cd            | 종목코드             | String | N        | 20     |             |
| - stk_nm            | 종목명               | String | N        | 20     |             |
| - netslmt_qty       | 순매도수량           | String | N        | 20     |             |
| - netslmt_amt       | 순매도금액           | String | N        | 20     |             |
| - prsm_avg_pric     | 추정평균가           | String | N        | 20     |             |
| - cur_prc           | 현재가               | String | N        | 20     |             |
| - pre_sig           | 대비기호             | String | N        | 20     |             |
| - pred_pre          | 전일대비             | String | N        | 20     |             |
| - avg_pric_pre      | 평균가대비           | String | N        | 20     |             |
| - pre_rt            | 대비율               | String | N        | 20     |             |
| - dt_trde_qty       | 기간거래량           | String | N        | 20     |             |

#### 요청 예시

```json
{
  "strt_dt": "20241106",
  "end_dt": "20241107",
  "trde_tp": "2",
  "mrkt_tp": "101",
  "invsr_tp": "8000",
  "stex_tp": "3"
}
```

#### 응답 예시

```json
{
  "invsr_daly_trde_stk": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "netslmt_qty": "+4464",
      "netslmt_amt": "+25467",
      "prsm_avg_pric": "57056",
      "cur_prc": "+61300",
      "pre_sig": "2",
      "pred_pre": "+4000",
      "avg_pric_pre": "+4244",
      "pre_rt": "+7.43",
      "dt_trde_qty": "1554171"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "netslmt_qty": "+12",
      "netslmt_amt": "+106",
      "prsm_avg_pric": "86658",
      "cur_prc": "+100200",
      "pre_sig": "2",
      "pred_pre": "+5200",
      "avg_pric_pre": "+13542",
      "pre_rt": "+15.62",
      "dt_trde_qty": "12868"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "netslmt_qty": "+46",
      "netslmt_amt": "+75",
      "prsm_avg_pric": "16320",
      "cur_prc": "15985",
      "pre_sig": "3",
      "pred_pre": "0",
      "avg_pric_pre": "--335",
      "pre_rt": "-2.05",
      "dt_trde_qty": "4770"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 종목별투자자기관별요청 (ka10059)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명       | Type   | Required | Length | Description                                                    |
| ---------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| dt         | 일자         | String | Y        | 8      | YYYYMMDD                                                       |
| stk_cd     | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| amt_qty_tp | 금액수량구분 | String | Y        | 1      | 1:금액, 2:수량                                                 |
| trde_tp    | 매매구분     | String | Y        | 1      | 0:순매수, 1:매수, 2:매도                                       |
| unit_tp    | 단위구분     | String | Y        | 4      | 1000:천주, 1:단주                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명             | Type   | Required | Length | Description             |
| ---------------- | ------------------ | ------ | -------- | ------ | ----------------------- |
| stk_invsr_orgn   | 종목별투자자기관별 | LIST   | N        |        |                         |
| - dt             | 일자               | String | N        | 20     |                         |
| - cur_prc        | 현재가             | String | N        | 20     |                         |
| - pre_sig        | 대비기호           | String | N        | 20     |                         |
| - pred_pre       | 전일대비           | String | N        | 20     |                         |
| - flu_rt         | 등락율             | String | N        | 20     | 우측 2자리 소수점자리수 |
| - acc_trde_qty   | 누적거래량         | String | N        | 20     |                         |
| - acc_trde_prica | 누적거래대금       | String | N        | 20     |                         |
| - ind_invsr      | 개인투자자         | String | N        | 20     |                         |
| - frgnr_invsr    | 외국인투자자       | String | N        | 20     |                         |
| - orgn           | 기관계             | String | N        | 20     |                         |
| - fnnc_invt      | 금융투자           | String | N        | 20     |                         |
| - insrnc         | 보험               | String | N        | 20     |                         |
| - invtrt         | 투신               | String | N        | 20     |                         |
| - etc_fnnc       | 기타금융           | String | N        | 20     |                         |
| - bank           | 은행               | String | N        | 20     |                         |
| - penfnd_etc     | 연기금등           | String | N        | 20     |                         |
| - samo_fund      | 사모펀드           | String | N        | 20     |                         |
| - natn           | 국가               | String | N        | 20     |                         |
| - etc_corp       | 기타법인           | String | N        | 20     |                         |
| - natfor         | 내외국인           | String | N        | 20     |                         |

#### 요청 예시

```json
{
  "dt": "20241107",
  "stk_cd": "005930",
  "amt_qty_tp": "1",
  "trde_tp": "0",
  "unit_tp": "1000"
}
```

#### 응답 예시

```json
{
  "stk_invsr_orgn": [
    {
      "dt": "20241107",
      "cur_prc": "+61300",
      "pre_sig": "2",
      "pred_pre": "+4000",
      "flu_rt": "+698",
      "acc_trde_qty": "1105968",
      "acc_trde_prica": "64215",
      "ind_invsr": "1584",
      "frgnr_invsr": "-61779",
      "orgn": "60195",
      "fnnc_invt": "25514",
      "insrnc": "0",
      "invtrt": "0",
      "etc_fnnc": "34619",
      "bank": "4",
      "penfnd_etc": "-1",
      "samo_fund": "58",
      "natn": "0",
      "etc_corp": "0",
      "natfor": "1"
    },
    {
      "dt": "20241106",
      "cur_prc": "+74800",
      "pre_sig": "1",
      "pred_pre": "+17200",
      "flu_rt": "+2986",
      "acc_trde_qty": "448203",
      "acc_trde_prica": "33340",
      "ind_invsr": "-639",
      "frgnr_invsr": "-7",
      "orgn": "646",
      "fnnc_invt": "-47",
      "insrnc": "15",
      "invtrt": "-2",
      "etc_fnnc": "730",
      "bank": "-51",
      "penfnd_etc": "1",
      "samo_fund": "0",
      "natn": "0",
      "etc_corp": "0",
      "natfor": "0"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 종목별투자자기관별합계요청 (ka10061)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명       | Type   | Required | Length | Description                                                    |
| ---------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd     | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| strt_dt    | 시작일자     | String | Y        | 8      | YYYYMMDD                                                       |
| end_dt     | 종료일자     | String | Y        | 8      | YYYYMMDD                                                       |
| amt_qty_tp | 금액수량구분 | String | Y        | 1      | 1:금액, 2:수량                                                 |
| trde_tp    | 매매구분     | String | Y        | 1      | 0:순매수, 1:매수, 2:매도                                       |
| unit_tp    | 단위구분     | String | Y        | 4      | 1000:천주, 1:단주                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명                 | Type   | Required | Length | Description |
| ------------------ | ---------------------- | ------ | -------- | ------ | ----------- |
| stk_invsr_orgn_tot | 종목별투자자기관별합계 | LIST   | N        |        |             |
| - ind_invsr        | 개인투자자             | String | N        | 20     |             |
| - frgnr_invsr      | 외국인투자자           | String | N        | 20     |             |
| - orgn             | 기관계                 | String | N        | 20     |             |
| - fnnc_invt        | 금융투자               | String | N        | 20     |             |
| - insrnc           | 보험                   | String | N        | 20     |             |
| - invtrt           | 투신                   | String | N        | 20     |             |
| - etc_fnnc         | 기타금융               | String | N        | 20     |             |
| - bank             | 은행                   | String | N        | 20     |             |
| - penfnd_etc       | 연기금등               | String | N        | 20     |             |
| - samo_fund        | 사모펀드               | String | N        | 20     |             |
| - natn             | 국가                   | String | N        | 20     |             |
| - etc_corp         | 기타법인               | String | N        | 20     |             |
| - natfor           | 내외국인               | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "strt_dt": "20241007",
  "end_dt": "20241107",
  "amt_qty_tp": "1",
  "trde_tp": "0",
  "unit_tp": "1000"
}
```

#### 응답 예시

```json
{
  "stk_invsr_orgn_tot": [
    {
      "ind_invsr": "--28837",
      "frgnr_invsr": "--40142",
      "orgn": "+64891",
      "fnnc_invt": "+72584",
      "insrnc": "--9071",
      "invtrt": "--7790",
      "etc_fnnc": "+35307",
      "bank": "+526",
      "penfnd_etc": "--22783",
      "samo_fund": "--3881",
      "natn": "0",
      "etc_corp": "+1974",
      "natfor": "+2114"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 당일전일체결요청 (ka10084)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element  | 한글명   | Type   | Required | Length | Description                                                     |
| -------- | -------- | ------ | -------- | ------ | --------------------------------------------------------------- |
| stk_cd   | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)  |
| tdy_pred | 당일전일 | String | Y        | 1      | 당일 : 1, 전일 : 2                                              |
| tic_min  | 틱분     | String | Y        | 1      | 0:틱, 1:분                                                      |
| tm       | 시간     | String | N        | 4      | 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description      |
| ------------------ | ---------------- | ------ | -------- | ------ | ---------------- |
| tdy_pred_cntr      | 당일전일체결     | LIST   | N        |        |                  |
| - tm               | 시간             | String | N        | 20     |                  |
| - cur_prc          | 현재가           | String | N        | 20     |                  |
| - pred_pre         | 전일대비         | String | N        | 20     |                  |
| - pre_rt           | 대비율           | String | N        | 20     |                  |
| - pri_sel_bid_unit | 우선매도호가단위 | String | N        | 20     |                  |
| - pri_buy_bid_unit | 우선매수호가단위 | String | N        | 20     |                  |
| - cntr_trde_qty    | 체결거래량       | String | N        | 20     |                  |
| - sign             | 전일대비기호     | String | N        | 20     |                  |
| - acc_trde_qty     | 누적거래량       | String | N        | 20     |                  |
| - acc_trde_prica   | 누적거래대금     | String | N        | 20     |                  |
| - cntr_str         | 체결강도         | String | N        | 20     |                  |
| - stex_tp          | 거래소구분       | String | N        | 20     | KRX , NXT , 통합 |

#### 요청 예시

```json
{
  "stk_cd": "005930",
  "tdy_pred": "1",
  "tic_min": "0",
  "tm": ""
}
```

#### 응답 예시

```json
{
  "tdy_pred_cntr": [
    {
      "tm": "112711",
      "cur_prc": "+128300",
      "pred_pre": "+700",
      "pre_rt": "+0.55",
      "pri_sel_bid_unit": "-0",
      "pri_buy_bid_unit": "+128300",
      "cntr_trde_qty": "-1",
      "sign": "2",
      "acc_trde_qty": "2",
      "acc_trde_prica": "0",
      "cntr_str": "0.00"
    },
    {
      "tm": "111554",
      "cur_prc": "+128300",
      "pred_pre": "+700",
      "pre_rt": "+0.55",
      "pri_sel_bid_unit": "-0",
      "pri_buy_bid_unit": "+128300",
      "cntr_trde_qty": "-1",
      "sign": "2",
      "acc_trde_qty": "1",
      "acc_trde_prica": "0",
      "cntr_str": "0.00"
    }
  ],
  "returnCode": 0,
  "returnMsg": "정상적으로 처리되었습니다"
}
```

---

### 관심종목정보요청 (ka10095)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                                            |
| ------- | -------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------ |
| stk_cd  | 종목코드 | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL)<br/>여러개의 종목코드 입력시 \| 로 구분 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element             | 한글명         | Type   | Required | Length | Description |
| ------------------- | -------------- | ------ | -------- | ------ | ----------- |
| atn_stk_infr        | 관심종목정보   | LIST   | N        |        |             |
| - stk_cd            | 종목코드       | String | N        | 20     |             |
| - stk_nm            | 종목명         | String | N        | 20     |             |
| - cur_prc           | 현재가         | String | N        | 20     |             |
| - base_pric         | 기준가         | String | N        | 20     |             |
| - pred_pre          | 전일대비       | String | N        | 20     |             |
| - pred_pre_sig      | 전일대비기호   | String | N        | 20     |             |
| - flu_rt            | 등락율         | String | N        | 20     |             |
| - trde_qty          | 거래량         | String | N        | 20     |             |
| - trde_prica        | 거래대금       | String | N        | 20     |             |
| - cntr_qty          | 체결량         | String | N        | 20     |             |
| - cntr_str          | 체결강도       | String | N        | 20     |             |
| - pred_trde_qty_pre | 전일거래량대비 | String | N        | 20     |             |
| - sel_bid           | 매도호가       | String | N        | 20     |             |
| - buy_bid           | 매수호가       | String | N        | 20     |             |
| - sel_1th_bid       | 매도1차호가    | String | N        | 20     |             |
| - sel_2th_bid       | 매도2차호가    | String | N        | 20     |             |
| - sel_3th_bid       | 매도3차호가    | String | N        | 20     |             |
| - sel_4th_bid       | 매도4차호가    | String | N        | 20     |             |
| - sel_5th_bid       | 매도5차호가    | String | N        | 20     |             |
| - buy_1th_bid       | 매수1차호가    | String | N        | 20     |             |
| - buy_2th_bid       | 매수2차호가    | String | N        | 20     |             |
| - buy_3th_bid       | 매수3차호가    | String | N        | 20     |             |
| - buy_4th_bid       | 매수4차호가    | String | N        | 20     |             |
| - buy_5th_bid       | 매수5차호가    | String | N        | 20     |             |
| - upl_pric          | 상한가         | String | N        | 20     |             |
| - lst_pric          | 하한가         | String | N        | 20     |             |
| - open_pric         | 시가           | String | N        | 20     |             |
| - high_pric         | 고가           | String | N        | 20     |             |
| - low_pric          | 저가           | String | N        | 20     |             |
| - close_pric        | 종가           | String | N        | 20     |             |
| - cntr_tm           | 체결시간       | String | N        | 20     |             |
| - exp_cntr_pric     | 예상체결가     | String | N        | 20     |             |
| - exp_cntr_qty      | 예상체결량     | String | N        | 20     |             |
| - cap               | 자본금         | String | N        | 20     |             |
| - fav               | 액면가         | String | N        | 20     |             |
| - mac               | 시가총액       | String | N        | 20     |             |
| - stkcnt            | 주식수         | String | N        | 20     |             |
| - bid_tm            | 호가시간       | String | N        | 20     |             |
| - dt                | 일자           | String | N        | 20     |             |
| - pri_sel_req       | 우선매도잔량   | String | N        | 20     |             |
| - pri_buy_req       | 우선매수잔량   | String | N        | 20     |             |
| - pri_sel_cnt       | 우선매도건수   | String | N        | 20     |             |
| - pri_buy_cnt       | 우선매수건수   | String | N        | 20     |             |
| - tot_sel_req       | 총매도잔량     | String | N        | 20     |             |
| - tot_buy_req       | 총매수잔량     | String | N        | 20     |             |
| - tot_sel_cnt       | 총매도건수     | String | N        | 20     |             |
| - tot_buy_cnt       | 총매수건수     | String | N        | 20     |             |
| - prty              | 패리티         | String | N        | 20     |             |
| - gear              | 기어링         | String | N        | 20     |             |
| - pl_qutr           | 손익분기       | String | N        | 20     |             |
| - cap_support       | 자본지지       | String | N        | 20     |             |
| - elwexec_pric      | ELW행사가      | String | N        | 20     |             |
| - cnvt_rt           | 전환비율       | String | N        | 20     |             |
| - elwexpr_dt        | ELW만기일      | String | N        | 20     |             |
| - cntr_engg         | 미결제약정     | String | N        | 20     |             |
| - cntr_pred_pre     | 미결제전일대비 | String | N        | 20     |             |
| - theory_pric       | 이론가         | String | N        | 20     |             |
| - innr_vltl         | 내재변동성     | String | N        | 20     |             |
| - delta             | 델타           | String | N        | 20     |             |
| - gam               | 감마           | String | N        | 20     |             |
| - theta             | 쎄타           | String | N        | 20     |             |
| - vega              | 베가           | String | N        | 20     |             |
| - law               | 로             | String | N        | 20     |             |

#### 요청 예시

```json
{
  "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
  "atn_stk_infr": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+156600",
      "base_pric": "121700",
      "pred_pre": "+34900",
      "pred_pre_sig": "2",
      "flu_rt": "+28.68",
      "trde_qty": "118636",
      "trde_prica": "14889",
      "cntr_qty": "-1",
      "cntr_str": "172.01",
      "pred_trde_qty_pre": "+1995.22",
      "sel_bid": "+156700",
      "buy_bid": "+156600",
      "sel_1th_bid": "+156700",
      "sel_2th_bid": "+156800",
      "sel_3th_bid": "+156900",
      "sel_4th_bid": "+158000",
      "sel_5th_bid": "+158100",
      "buy_1th_bid": "+156600",
      "buy_2th_bid": "+156500",
      "buy_3th_bid": "+156400",
      "buy_4th_bid": "+130000",
      "buy_5th_bid": "121700",
      "upl_pric": "+158200",
      "lst_pric": "-85200",
      "open_pric": "121700",
      "high_pric": "+158200",
      "low_pric": "-85200",
      "close_pric": "+156600",
      "cntr_tm": "163713",
      "exp_cntr_pric": "+156600",
      "exp_cntr_qty": "823",
      "cap": "7780",
      "fav": "100",
      "mac": "9348679",
      "stkcnt": "5969783",
      "bid_tm": "164000",
      "dt": "20241128",
      "pri_sel_req": "8003",
      "pri_buy_req": "7705",
      "pri_sel_cnt": "",
      "pri_buy_cnt": "",
      "tot_sel_req": "24028",
      "tot_buy_req": "26579",
      "tot_sel_cnt": "-11",
      "tot_buy_cnt": "",
      "prty": "0.00",
      "gear": "0.00",
      "pl_qutr": "0.00",
      "cap_support": "0.00",
      "elwexec_pric": "0",
      "cnvt_rt": "0.0000",
      "elwexpr_dt": "00000000",
      "cntr_engg": "",
      "cntr_pred_pre": "",
      "theory_pric": "",
      "innr_vltl": "",
      "delta": "",
      "gam": "",
      "theta": "",
      "vega": "",
      "law": ""
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 종목정보 리스트 (ka10099)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                                                   |
| ------- | -------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------- |
| mrkt_tp | 시장구분 | String | Y        | 2      | 0:코스피,10:코스닥,3:ELW,8:ETF,30:K-OTC,50:코넥스,5:신주인수권,4:뮤추얼펀드,6:리츠,9:하이일드 |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element            | 한글명           | Type   | Required | Length | Description                                                                                            |
| ------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------ |
| list               | 종목리스트       | LIST   | N        |        |                                                                                                        |
| - code             | 종목코드         | String | N        | 20     | 단축코드                                                                                               |
| - name             | 종목명           | String | N        | 20     |                                                                                                        |
| - listCount        | 상장주식수       | String | N        | 20     |                                                                                                        |
| - auditInfo        | 감리구분         | String | N        | 20     |                                                                                                        |
| - regDay           | 상장일           | String | N        | 20     |                                                                                                        |
| - lastPrice        | 전일종가         | String | N        | 20     |                                                                                                        |
| - state            | 종목상태         | String | N        | 20     |                                                                                                        |
| - marketCode       | 시장구분코드     | String | N        | 20     |                                                                                                        |
| - marketName       | 시장명           | String | N        | 20     |                                                                                                        |
| - upName           | 업종명           | String | N        | 20     |                                                                                                        |
| - upSizeName       | 회사크기분류     | String | N        | 20     |                                                                                                        |
| - companyClassName | 회사분류         | String | N        | 20     | 코스닥만 존재함                                                                                        |
| - orderWarning     | 투자유의종목여부 | String | N        | 20     | 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달) |
| - nxtEnable        | NXT가능여부      | String | N        | 20     | Y: 가능                                                                                                |

#### 요청 예시

```json
{
  "mrkt_tp": "0"
}
```

#### 응답 예시

```json
{
  "return_msg": "정상적으로 처리되었습니다",
  "return_code": 0,
  "list": [
    {
      "code": "005930",
      "name": "삼성전자",
      "listCount": "0000000123759593",
      "auditInfo": "투자주의환기종목",
      "regDay": "20091204",
      "lastPrice": "00000197",
      "state": "관리종목",
      "marketCode": "10",
      "marketName": "코스닥",
      "upName": "",
      "upSizeName": "",
      "companyClassName": "",
      "orderWarning": "0",
      "nxtEnable": "Y"
    },
    {
      "code": "005930",
      "name": "삼성전자",
      "listCount": "0000000136637536",
      "auditInfo": "정상",
      "regDay": "20100423",
      "lastPrice": "00000213",
      "state": "증거금100%",
      "marketCode": "10",
      "marketName": "코스닥",
      "upName": "",
      "upSizeName": "",
      "companyClassName": "외국기업",
      "orderWarning": "0",
      "nxtEnable": "Y"
    },
    {
      "code": "005930",
      "name": "삼성전자",
      "listCount": "0000000080000000",
      "auditInfo": "정상",
      "regDay": "20160818",
      "lastPrice": "00000614",
      "state": "증거금100%",
      "marketCode": "10",
      "marketName": "코스닥",
      "upName": "",
      "upSizeName": "",
      "companyClassName": "외국기업",
      "orderWarning": "0",
      "nxtEnable": "Y"
    },
    {
      "code": "005930",
      "name": "삼성전자",
      "listCount": "0000000141781250",
      "auditInfo": "정상",
      "regDay": "20160630",
      "lastPrice": "00000336",
      "state": "증거금100%",
      "marketCode": "10",
      "marketName": "코스닥",
      "upName": "",
      "upSizeName": "",
      "companyClassName": "외국기업",
      "orderWarning": "0",
      "nxtEnable": "Y"
    },
    {
      "code": "005930",
      "name": "삼성전자",
      "listCount": "0000000141781250",
      "auditInfo": "정상",
      "regDay": "20160630",
      "lastPrice": "00000336",
      "state": "증거금100%",
      "marketCode": "10",
      "marketName": "코스닥",
      "upName": "",
      "upSizeName": "",
      "companyClassName": "외국기업",
      "orderWarning": "0",
      "nxtEnable": "Y"
    }
  ]
}
```

---

### 종목정보 조회 (ka10100)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description |
| ------- | -------- | ------ | -------- | ------ | ----------- |
| stk_cd  | 종목코드 | String | Y        | 6      |             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명           | Type   | Required | Length | Description                                                                                            |
| ---------------- | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------------------------------------ |
| code             | 종목코드         | String | N        |        | 단축코드                                                                                               |
| name             | 종목명           | String | N        |        |                                                                                                        |
| listCount        | 상장주식수       | String | N        |        |                                                                                                        |
| auditInfo        | 감리구분         | String | N        |        |                                                                                                        |
| regDay           | 상장일           | String | N        |        |                                                                                                        |
| lastPrice        | 전일종가         | String | N        |        |                                                                                                        |
| state            | 종목상태         | String | N        |        |                                                                                                        |
| marketCode       | 시장구분코드     | String | N        |        |                                                                                                        |
| marketName       | 시장명           | String | N        |        |                                                                                                        |
| upName           | 업종명           | String | N        |        |                                                                                                        |
| upSizeName       | 회사크기분류     | String | N        |        |                                                                                                        |
| companyClassName | 회사분류         | String | N        |        | 코스닥만 존재함                                                                                        |
| orderWarning     | 투자유의종목여부 | String | N        |        | 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달) |
| nxtEnable        | NXT가능여부      | String | N        |        | Y: 가능                                                                                                |

#### 요청 예시

```json
{
  "stk_cd": "005930"
}
```

#### 응답 예시

```json
{
  "code": "005930",
  "name": "삼성전자",
  "listCount": "0000000026034239",
  "auditInfo": "정상",
  "regDay": "20090803",
  "lastPrice": "00136000",
  "state": "증거금20%|담보대출|신용가능",
  "marketCode": "0",
  "marketName": "거래소",
  "upName": "금융업",
  "upSizeName": "대형주",
  "companyClassName": "",
  "orderWarning": "0",
  "nxtEnable": "Y",
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 업종코드 리스트 (ka10101)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명   | Type   | Required | Length | Description                                                        |
| ------- | -------- | ------ | -------- | ------ | ------------------------------------------------------------------ |
| mrkt_tp | 시장구분 | String | Y        | 1      | 0:코스피(거래소),1:코스닥,2:KOSPI200,4:KOSPI100,7:KRX100(통합지수) |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element      | 한글명         | Type   | Required | Length | Description |
| ------------ | -------------- | ------ | -------- | ------ | ----------- |
| list         | 업종코드리스트 | LIST   | N        |        |             |
| - marketCode | 시장구분코드   | String | N        |        |             |
| - code       | 코드           | String | N        |        |             |
| - name       | 업종명         | String | N        |        |             |
| - group      | 그룹           | String | N        |        |             |

#### 요청 예시

```json
{
  "mrkt_tp": "0"
}
```

#### 응답 예시

```json
{
  "return_msg": "정상적으로 처리되었습니다",
  "list": [
    {
      "marketCode": "0",
      "code": "001",
      "name": "종합(KOSPI)",
      "group": "1"
    },
    {
      "marketCode": "0",
      "code": "002",
      "name": "대형주",
      "group": "2"
    },
    {
      "marketCode": "0",
      "code": "003",
      "name": "중형주",
      "group": "3"
    },
    {
      "marketCode": "0",
      "code": "004",
      "name": "소형주",
      "group": "4"
    },
    {
      "marketCode": "0",
      "code": "005",
      "name": "음식료업",
      "group": "5"
    },
    {
      "marketCode": "0",
      "code": "006",
      "name": "섬유의복",
      "group": "6"
    },
    {
      "marketCode": "0",
      "code": "007",
      "name": "종이목재",
      "group": "7"
    },
    {
      "marketCode": "0",
      "code": "008",
      "name": "화학",
      "group": "8"
    },
    {
      "marketCode": "0",
      "code": "009",
      "name": "의약품",
      "group": "9"
    },
    {
      "marketCode": "0",
      "code": "010",
      "name": "비금속광물",
      "group": "10"
    },
    {
      "marketCode": "0",
      "code": "011",
      "name": "철강금속",
      "group": "11"
    }
  ],
  "return_code": 0
}
```

---

### 회원사 리스트 (ka10102)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

요청 Body 없음

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element | 한글명           | Type   | Required | Length | Description |
| ------- | ---------------- | ------ | -------- | ------ | ----------- |
| list    | 회원사코드리스트 | LIST   | N        |        |             |
| - code  | 코드             | String | N        |        |             |
| - name  | 업종명           | String | N        |        |             |
| - gb    | 구분             | String | N        |        |             |

#### 요청 예시

```json
{}
```

#### 응답 예시

```json
{
  "return_msg": "정상적으로 처리되었습니다",
  "list": [
    {
      "code": "001",
      "name": "교  보",
      "gb": "0"
    },
    {
      "code": "002",
      "name": "신한금융투자",
      "gb": "0"
    },
    {
      "code": "003",
      "name": "한국투자증권",
      "gb": "0"
    },
    {
      "code": "004",
      "name": "대  신",
      "gb": "0"
    },
    {
      "code": "005",
      "name": "미래대우",
      "gb": "0"
    },
    {
      "code": "006",
      "name": "신  영",
      "gb": "0"
    },
    {
      "code": "008",
      "name": "유진투자증권",
      "gb": "0"
    },
    {
      "code": "009",
      "name": "한  양",
      "gb": "0"
    },
    {
      "code": "010",
      "name": "메리츠",
      "gb": "0"
    },
    {
      "code": "012",
      "name": "NH투자증권",
      "gb": "0"
    }
  ],
  "return_code": 0
}
```

---

### 프로그램순매수상위50요청 (ka90003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element       | 한글명       | Type   | Required | Length | Description                  |
| ------------- | ------------ | ------ | -------- | ------ | ---------------------------- |
| trde_upper_tp | 매매상위구분 | String | Y        | 1      | 1:순매도상위, 2:순매수상위   |
| amt_qty_tp    | 금액수량구분 | String | Y        | 2      | 1:금액, 2:수량               |
| mrkt_tp       | 시장구분     | String | Y        | 10     | P00101:코스피, P10102:코스닥 |
| stex_tp       | 거래소구분   | String | Y        | 1      | 1:KRX, 2:NXT 3.통합          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element              | 한글명               | Type   | Required | Length | Description |
| -------------------- | -------------------- | ------ | -------- | ------ | ----------- |
| prm_netprps_upper_50 | 프로그램순매수상위50 | LIST   | N        |        |             |
| - rank               | 순위                 | String | N        | 20     |             |
| - stk_cd             | 종목코드             | String | N        | 20     |             |
| - stk_nm             | 종목명               | String | N        | 20     |             |
| - cur_prc            | 현재가               | String | N        | 20     |             |
| - flu_sig            | 등락기호             | String | N        | 20     |             |
| - pred_pre           | 전일대비             | String | N        | 20     |             |
| - flu_rt             | 등락률               | String | N        | 20     |             |
| - acc_trde_qty       | 누적거래량           | String | N        | 20     |             |
| - prm_sell_amt       | 프로그램매도금액     | String | N        | 20     |             |
| - prm_buy_amt        | 프로그램매수금액     | String | N        | 20     |             |
| - prm_netprps_amt    | 프로그램순매수금액   | String | N        | 20     |             |

#### 요청 예시

```json
{
  "trde_upper_tp": "1",
  "amt_qty_tp": "1",
  "mrkt_tp": "P00101",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "prm_trde_trnsn": [
    {
      "cntr_tm": "170500",
      "dfrt_trde_sel": "0",
      "dfrt_trde_buy": "0",
      "dfrt_trde_netprps": "0",
      "ndiffpro_trde_sel": "1",
      "ndiffpro_trde_buy": "17",
      "ndiffpro_trde_netprps": "+17",
      "dfrt_trde_sell_qty": "0",
      "dfrt_trde_buy_qty": "0",
      "dfrt_trde_netprps_qty": "0",
      "ndiffpro_trde_sell_qty": "0",
      "ndiffpro_trde_buy_qty": "0",
      "ndiffpro_trde_netprps_qty": "+0",
      "all_sel": "1",
      "all_buy": "17",
      "all_netprps": "+17",
      "kospi200": "+47839",
      "basis": "-146.59"
    },
    {
      "cntr_tm": "170400",
      "dfrt_trde_sel": "0",
      "dfrt_trde_buy": "0",
      "dfrt_trde_netprps": "0",
      "ndiffpro_trde_sel": "1",
      "ndiffpro_trde_buy": "17",
      "ndiffpro_trde_netprps": "+17",
      "dfrt_trde_sell_qty": "0",
      "dfrt_trde_buy_qty": "0",
      "dfrt_trde_netprps_qty": "0",
      "ndiffpro_trde_sell_qty": "0",
      "ndiffpro_trde_buy_qty": "0",
      "ndiffpro_trde_netprps_qty": "+0",
      "all_sel": "1",
      "all_buy": "17",
      "all_netprps": "+17",
      "kospi200": "+47839",
      "basis": "-146.59"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---

### 종목별프로그램매매현황요청 (ka90004)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/stkinfo
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element | 한글명     | Type   | Required | Length | Description                  |
| ------- | ---------- | ------ | -------- | ------ | ---------------------------- |
| dt      | 일자       | String | Y        | 8      | YYYYMMDD                     |
| mrkt_tp | 시장구분   | String | Y        | 10     | P00101:코스피, P10102:코스닥 |
| stex_tp | 거래소구분 | String | Y        | 1      | 1:KRX, 2:NXT 3.통합          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element           | 한글명                 | Type   | Required | Length | Description |
| ----------------- | ---------------------- | ------ | -------- | ------ | ----------- |
| tot_1             | 매수체결수량합계       | String | N        | 20     |             |
| tot_2             | 매수체결금액합계       | String | N        | 20     |             |
| tot_3             | 매도체결수량합계       | String | N        | 20     |             |
| tot_4             | 매도체결금액합계       | String | N        | 20     |             |
| tot_5             | 순매수대금합계         | String | N        | 20     |             |
| tot_6             | 합계6                  | String | N        | 20     |             |
| stk_prm_trde_prst | 종목별프로그램매매현황 | LIST   | N        |        |             |
| - stk_cd          | 종목코드               | String | N        | 20     |             |
| - stk_nm          | 종목명                 | String | N        | 20     |             |
| - cur_prc         | 현재가                 | String | N        | 20     |             |
| - flu_sig         | 등락기호               | String | N        | 20     |             |
| - pred_pre        | 전일대비               | String | N        | 20     |             |
| - buy_cntr_qty    | 매수체결수량           | String | N        | 20     |             |
| - buy_cntr_amt    | 매수체결금액           | String | N        | 20     |             |
| - sel_cntr_qty    | 매도체결수량           | String | N        | 20     |             |
| - sel_cntr_amt    | 매도체결금액           | String | N        | 20     |             |
| - netprps_prica   | 순매수대금             | String | N        | 20     |             |
| - all_trde_rt     | 전체거래비율           | String | N        | 20     |             |

#### 요청 예시

```json
{
  "dt": "20241125",
  "mrkt_tp": "P00101",
  "stex_tp": "1"
}
```

#### 응답 예시

```json
{
  "tot_1": "0",
  "tot_2": "2",
  "tot_3": "0",
  "tot_4": "2",
  "tot_5": "0",
  "tot_6": "",
  "stk_prm_trde_prst": [
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "-75000",
      "flu_sig": "5",
      "pred_pre": "-2800",
      "buy_cntr_qty": "0",
      "buy_cntr_amt": "0",
      "sel_cntr_qty": "0",
      "sel_cntr_amt": "0",
      "netprps_prica": "0",
      "all_trde_rt": "+0.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "+130000",
      "flu_sig": "2",
      "pred_pre": "+6800",
      "buy_cntr_qty": "0",
      "buy_cntr_amt": "0",
      "sel_cntr_qty": "0",
      "sel_cntr_amt": "0",
      "netprps_prica": "0",
      "all_trde_rt": "+0.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "360000",
      "flu_sig": "3",
      "pred_pre": "0",
      "buy_cntr_qty": "0",
      "buy_cntr_amt": "0",
      "sel_cntr_qty": "0",
      "sel_cntr_amt": "0",
      "netprps_prica": "0",
      "all_trde_rt": "+0.00"
    },
    {
      "stk_cd": "005930",
      "stk_nm": "삼성전자",
      "cur_prc": "1000000",
      "flu_sig": "3",
      "pred_pre": "0",
      "buy_cntr_qty": "0",
      "buy_cntr_amt": "0",
      "sel_cntr_qty": "0",
      "sel_cntr_amt": "0",
      "netprps_prica": "0",
      "all_trde_rt": "+0.00"
    }
  ],
  "return_code": 0,
  "return_msg": "정상적으로 처리되었습니다"
}
```

---
# 키움증권 API 문서

## 국내주식 REST API

### 주문

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 주식 매수주문 | kt10000 | 주식 매수주문 처리 |
| 주식 매도주문 | kt10001 | 주식 매도주문 처리 |
| 주식 정정주문 | kt10002 | 주식 정정주문 처리 |
| 주식 취소주문 | kt10003 | 주식 취소주문 처리 |
| 신용 매수주문 | kt10006 | 신용 매수주문 처리 |
| 신용 매도주문 | kt10007 | 신용 매도주문 처리 |
| 신용 정정주문 | kt10008 | 신용 정정주문 처리 |
| 신용 취소주문 | kt10009 | 신용 취소주문 처리 |

---

### 주식 매수주문 (kt10000)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/ordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------ | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                                                                                                                                                                                                                                                                                                                                                                                                                 |
| stk_cd       | 종목코드       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_qty      | 주문수량       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_uv       | 주문단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_tp      | 매매구분       | String | Y        | 20     | 0:보통, 3:시장가, 5:조건부지정가, 81:장마감후시간외, 61:장시작전시간외, 62:시간외단일가, 6:최유리지정가, 7:최우선지정가, 10:보통(IOC), 13:시장가(IOC), 16:최유리(IOC), 20:보통(FOK), 23:시장가(FOK), 26:최유리(FOK), 28:스톱지정가, 29:중간가, 30:중간가(IOC), 31:중간가(FOK)                                                                                                                                                     |
| cond_uv      | 조건단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element      | 한글명         | Type   | Required | Length | Description |
| ------------ | -------------- | ------ | -------- | ------ | ----------- |
| ord_no       | 주문번호       | String | N        | 7      |             |
| dmst_stex_tp | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"stk_cd": "005930",
	"ord_qty": "1",
	"ord_uv": "",
	"trde_tp": "3",
	"cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "00024",
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식 매도주문 (kt10001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/ordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------ | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                                                                                                                                                                                                                                                                                                                                                                                                                 |
| stk_cd       | 종목코드       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_qty      | 주문수량       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_uv       | 주문단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_tp      | 매매구분       | String | Y        | 20     | 0:보통, 3:시장가, 5:조건부지정가, 81:장마감후시간외, 61:장시작전시간외, 62:시간외단일가, 6:최유리지정가, 7:최우선지정가, 10:보통(IOC), 13:시장가(IOC), 16:최유리(IOC), 20:보통(FOK), 23:시장가(FOK), 26:최유리(FOK), 28:스톱지정가, 29:중간가, 30:중간가(IOC), 31:중간가(FOK)                                                                                                                                                     |
| cond_uv      | 조건단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element      | 한글명         | Type   | Required | Length | Description |
| ------------ | -------------- | ------ | -------- | ------ | ----------- |
| ord_no       | 주문번호       | String | N        | 7      |             |
| dmst_stex_tp | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"stk_cd": "005930",
	"ord_qty": "1",
	"ord_uv": "",
	"trde_tp": "3",
	"cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "0000138",
	"dmst_stex_tp": "KRX",
	"return_code": 0,
	"return_msg": "매도주문이 완료되었습니다."
}
```

---

### 주식 정정주문 (kt10002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/ordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명         | Type   | Required | Length | Description         |
| -------------- | -------------- | ------ | -------- | ------ | ------------------- |
| dmst_stex_tp   | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR         |
| orig_ord_no    | 원주문번호     | String | Y        | 7      |                     |
| stk_cd         | 종목코드       | String | Y        | 12     |                     |
| mdfy_qty       | 정정수량       | String | Y        | 12     |                     |
| mdfy_uv        | 정정단가       | String | Y        | 12     |                     |
| mdfy_cond_uv   | 정정조건단가   | String | N        | 12     |                     |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명         | Type   | Required | Length | Description |
| ---------------- | -------------- | ------ | -------- | ------ | ----------- |
| ord_no           | 주문번호       | String | N        | 7      |             |
| base_orig_ord_no | 모주문번호     | String | N        | 7      |             |
| mdfy_qty         | 정정수량       | String | N        | 12     |             |
| dmst_stex_tp     | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"orig_ord_no": "0000139",
	"stk_cd": "005930",
	"mdfy_qty": "1",
	"mdfy_uv": "199700",
	"mdfy_cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "0000140",
	"base_orig_ord_no": "0000139",
	"mdfy_qty": "000000000001",
	"dmst_stex_tp": "KRX",
	"return_code": 0,
	"return_msg": "매수정정 주문입력이 완료되었습니다"
}
```

---

### 주식 취소주문 (kt10003)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/ordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                     |
| ------------ | -------------- | ------ | -------- | ------ | ------------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                     |
| orig_ord_no  | 원주문번호     | String | Y        | 7      |                                 |
| stk_cd       | 종목코드       | String | Y        | 12     |                                 |
| cncl_qty     | 취소수량       | String | Y        | 12     | '0' 입력시 잔량 전부 취소       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명         | Type   | Required | Length | Description |
| ---------------- | -------------- | ------ | -------- | ------ | ----------- |
| ord_no           | 주문번호       | String | N        | 7      |             |
| base_orig_ord_no | 모주문번호     | String | N        | 7      |             |
| cncl_qty         | 취소수량       | String | N        | 12     |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"orig_ord_no": "0000140",
	"stk_cd": "005930",
	"cncl_qty": "1"
}
```

#### 응답 예시

```json
{
	"ord_no": "0000141",
	"base_orig_ord_no": "0000139",
	"cncl_qty": "000000000001",
	"return_code": 0,
	"return_msg": "매수취소 주문입력이 완료되었습니다"
}
```

---

### 신용 매수주문 (kt10006)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/crdordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------ | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                                                                                                                                                                                                                                                                                                                                                                                                                 |
| stk_cd       | 종목코드       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_qty      | 주문수량       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_uv       | 주문단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_tp      | 매매구분       | String | Y        | 20     | 0:보통, 3:시장가, 5:조건부지정가, 81:장마감후시간외, 61:장시작전시간외, 62:시간외단일가, 6:최유리지정가, 7:최우선지정가, 10:보통(IOC), 13:시장가(IOC), 16:최유리(IOC), 20:보통(FOK), 23:시장가(FOK), 26:최유리(FOK), 28:스톱지정가, 29:중간가, 30:중간가(IOC), 31:중간가(FOK)                                                                                                                                                     |
| cond_uv      | 조건단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element      | 한글명         | Type   | Required | Length | Description |
| ------------ | -------------- | ------ | -------- | ------ | ----------- |
| ord_no       | 주문번호       | String | N        | 7      |             |
| dmst_stex_tp | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"stk_cd": "005930",
	"ord_qty": "1",
	"ord_uv": "2580",
	"trde_tp": "0",
	"cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "0001615",
	"dmst_stex_tp": "KRX",
	"return_code": 0,
	"return_msg": "신용 매수주문이 완료되었습니다."
}
```

---

### 신용 매도주문 (kt10007)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/crdordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------ | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                                                                                                                                                                                                                                                                                                                                                                                                                 |
| stk_cd       | 종목코드       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_qty      | 주문수량       | String | Y        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ord_uv       | 주문단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |
| trde_tp      | 매매구분       | String | Y        | 20     | 0:보통, 3:시장가, 5:조건부지정가, 81:장마감후시간외, 61:장시작전시간외, 62:시간외단일가, 6:최유리지정가, 7:최우선지정가, 10:보통(IOC), 13:시장가(IOC), 16:최유리(IOC), 20:보통(FOK), 23:시장가(FOK), 26:최유리(FOK), 28:스톱지정가, 29:중간가, 30:중간가(IOC), 31:중간가(FOK)                                                                                                                                                     |
| crd_deal_tp  | 신용거래구분   | String | Y        | 2      | 33:융자, 99:융자합                                                                                                                                                                                                                                                                                                                                                                                                          |
| crd_loan_dt  | 대출일         | String | N        | 8      | YYYYMMDD(융자일경우필수)                                                                                                                                                                                                                                                                                                                                                                                                     |
| cond_uv      | 조건단가       | String | N        | 12     |                                                                                                                                                                                                                                                                                                                                                                                                                             |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element      | 한글명         | Type   | Required | Length | Description |
| ------------ | -------------- | ------ | -------- | ------ | ----------- |
| ord_no       | 주문번호       | String | N        | 7      |             |
| dmst_stex_tp | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"stk_cd": "005930",
	"ord_qty": "3",
	"ord_uv": "6450",
	"trde_tp": "0",
	"crd_deal_tp": "99",
	"crd_loan_dt": "",
	"cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "0001614",
	"dmst_stex_tp": "KRX",
	"return_code": 0,
	"return_msg": "신용 매도주문이 완료되었습니다."
}
```

---

### 신용 정정주문 (kt10008)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/crdordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명         | Type   | Required | Length | Description         |
| -------------- | -------------- | ------ | -------- | ------ | ------------------- |
| dmst_stex_tp   | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR         |
| orig_ord_no    | 원주문번호     | String | Y        | 7      |                     |
| stk_cd         | 종목코드       | String | Y        | 12     |                     |
| mdfy_qty       | 정정수량       | String | Y        | 12     |                     |
| mdfy_uv        | 정정단가       | String | Y        | 12     |                     |
| mdfy_cond_uv   | 정정조건단가   | String | N        | 12     |                     |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명         | Type   | Required | Length | Description |
| ---------------- | -------------- | ------ | -------- | ------ | ----------- |
| ord_no           | 주문번호       | String | N        | 7      |             |
| base_orig_ord_no | 모주문번호     | String | N        | 7      |             |
| mdfy_qty         | 정정수량       | String | N        | 12     |             |
| dmst_stex_tp     | 국내거래소구분 | String | N        | 6      |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"orig_ord_no": "0001615",
	"stk_cd": "005930",
	"mdfy_qty": "2",
	"mdfy_uv": "2600",
	"mdfy_cond_uv": ""
}
```

#### 응답 예시

```json
{
	"ord_no": "0001616",
	"base_orig_ord_no": "0001615",
	"mdfy_qty": "000000000002",
	"dmst_stex_tp": "KRX",
	"return_code": 0,
	"return_msg": "신용 정정주문이 완료되었습니다."
}
```

---

### 신용 취소주문 (kt10009)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/crdordr
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명         | Type   | Required | Length | Description                 |
| ------------ | -------------- | ------ | -------- | ------ | --------------------------- |
| dmst_stex_tp | 국내거래소구분 | String | Y        | 3      | KRX,NXT,SOR                 |
| orig_ord_no  | 원주문번호     | String | Y        | 7      |                             |
| stk_cd       | 종목코드       | String | Y        | 12     |                             |
| cncl_qty     | 취소수량       | String | Y        | 12     | '0' 입력시 잔량 전부 취소   |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element          | 한글명         | Type   | Required | Length | Description |
| ---------------- | -------------- | ------ | -------- | ------ | ----------- |
| ord_no           | 주문번호       | String | N        | 7      |             |
| base_orig_ord_no | 모주문번호     | String | N        | 7      |             |
| cncl_qty         | 취소수량       | String | N        | 12     |             |

#### 요청 예시

```json
{
	"dmst_stex_tp": "KRX",
	"orig_ord_no": "0001616",
	"stk_cd": "005930",
	"cncl_qty": "2"
}
```

#### 응답 예시

```json
{
	"ord_no": "0001617",
	"base_orig_ord_no": "0001615",
	"cncl_qty": "000000000002",
	"return_code": 0,
	"return_msg": "신용 취소주문이 완료되었습니다."
}
```

--- # 키움증권 API 문서

## 국내주식 REST API

### 차트

#### TR 목록

| TR명                           | 코드    | 설명                           |
| ------------------------------ | ------- | ------------------------------ |
| 종목별투자자기관별차트요청     | ka10060 | 종목별투자자기관별차트요청     |
| 장중투자자별매매차트요청       | ka10064 | 장중투자자별매매차트요청       |
| 주식틱차트조회요청             | ka10079 | 주식틱차트조회요청             |
| 주식분봉차트조회요청           | ka10080 | 주식분봉차트조회요청           |
| 주식일봉차트조회요청           | ka10081 | 주식일봉차트조회요청           |
| 주식주봉차트조회요청           | ka10082 | 주식주봉차트조회요청           |
| 주식월봉차트조회요청           | ka10083 | 주식월봉차트조회요청           |
| 주식년봉차트조회요청           | ka10094 | 주식년봉차트조회요청           |
| 업종틱차트조회요청             | ka20004 | 업종틱차트조회요청             |
| 업종분봉조회요청               | ka20005 | 업종분봉조회요청               |
| 업종일봉조회요청               | ka20006 | 업종일봉조회요청               |
| 업종주봉조회요청               | ka20007 | 업종주봉조회요청               |
| 업종월봉조회요청               | ka20008 | 업종월봉조회요청               |
| 업종년봉조회요청               | ka20019 | 업종년봉조회요청               |

---

### 종목별투자자기관별차트요청 (ka10060)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명       | Type   | Required | Length | Description                                                    |
| ---------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| dt         | 일자         | String | Y        | 8      | YYYYMMDD                                                       |
| stk_cd     | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| amt_qty_tp | 금액수량구분 | String | Y        | 1      | 1:금액, 2:수량                                                 |
| trde_tp    | 매매구분     | String | Y        | 1      | 0:순매수, 1:매수, 2:매도                                       |
| unit_tp    | 단위구분     | String | Y        | 4      | 1000:천주, 1:단주                                              |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명                     | Type   | Required | Length | Description |
| ---------------------- | -------------------------- | ------ | -------- | ------ | ----------- |
| stk_invsr_orgn_chart   | 종목별투자자기관별차트     | LIST   | N        |        |             |
| - dt                   | 일자                       | String | N        | 20     |             |
| - cur_prc              | 현재가                     | String | N        | 20     |             |
| - pred_pre             | 전일대비                   | String | N        | 20     |             |
| - acc_trde_prica       | 누적거래대금               | String | N        | 20     |             |
| - ind_invsr            | 개인투자자                 | String | N        | 20     |             |
| - frgnr_invsr          | 외국인투자자               | String | N        | 20     |             |
| - orgn                 | 기관계                     | String | N        | 20     |             |
| - fnnc_invt            | 금융투자                   | String | N        | 20     |             |
| - insrnc               | 보험                       | String | N        | 20     |             |
| - invtrt               | 투신                       | String | N        | 20     |             |
| - etc_fnnc             | 기타금융                   | String | N        | 20     |             |
| - bank                 | 은행                       | String | N        | 20     |             |
| - penfnd_etc           | 연기금등                   | String | N        | 20     |             |
| - samo_fund            | 사모펀드                   | String | N        | 20     |             |
| - natn                 | 국가                       | String | N        | 20     |             |
| - etc_corp             | 기타법인                   | String | N        | 20     |             |
| - natfor               | 내외국인                   | String | N        | 20     |             |


#### 요청 예시

```json
{
	"dt": "20241107",
	"stk_cd": "005930",
	"amt_qty_tp": "1",
	"trde_tp": "0",
	"unit_tp": "1000"
}
```

#### 응답 예시

```json
{
	"stk_invsr_orgn_chart": [
		{
			"dt": "20241107",
			"cur_prc": "+61300",
			"pred_pre": "+4000",
			"acc_trde_prica": "1105968",
			"ind_invsr": "1584",
			"frgnr_invsr": "-61779",
			"orgn": "60195",
			"fnnc_invt": "25514",
			"insrnc": "0",
			"invtrt": "0",
			"etc_fnnc": "34619",
			"bank": "4",
			"penfnd_etc": "-1",
			"samo_fund": "58",
			"natn": "0",
			"etc_corp": "0",
			"natfor": "1"
		},
		{
			"dt": "20241106",
			"cur_prc": "+74800",
			"pred_pre": "+17200",
			"acc_trde_prica": "448203",
			"ind_invsr": "-639",
			"frgnr_invsr": "-7",
			"orgn": "646",
			"fnnc_invt": "-47",
			"insrnc": "15",
			"invtrt": "-2",
			"etc_fnnc": "730",
			"bank": "-51",
			"penfnd_etc": "1",
			"samo_fund": "0",
			"natn": "0",
			"etc_corp": "0",
			"natfor": "0"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 장중투자자별매매차트요청 (ka10064)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element    | 한글명       | Type   | Required | Length | Description                                                    |
| ---------- | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| mrkt_tp    | 시장구분     | String | Y        | 3      | 000:전체, 001:코스피, 101:코스닥                               |
| amt_qty_tp | 금액수량구분 | String | Y        | 1      | 1:금액, 2:수량                                                 |
| trde_tp    | 매매구분     | String | Y        | 1      | 0:순매수, 1:매수, 2:매도                                       |
| stk_cd     | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명               | Type   | Required | Length | Description |
| ------------------------ | -------------------- | ------ | -------- | ------ | ----------- |
| opmr_invsr_trde_chart    | 장중투자자별매매차트 | LIST   | N        |        |             |
| - tm                     | 시간                 | String | N        | 20     |             |
| - frgnr_invsr            | 외국인투자자         | String | N        | 20     |             |
| - orgn                   | 기관계               | String | N        | 20     |             |
| - invtrt                 | 투신                 | String | N        | 20     |             |
| - insrnc                 | 보험                 | String | N        | 20     |             |
| - bank                   | 은행                 | String | N        | 20     |             |
| - penfnd_etc             | 연기금등             | String | N        | 20     |             |
| - etc_corp               | 기타법인             | String | N        | 20     |             |
| - natn                   | 국가                 | String | N        | 20     |             |

#### 요청 예시

```json
{
	"mrkt_tp": "000",
	"amt_qty_tp": "1",
	"trde_tp": "0",
	"stk_cd": "005930"
}
```

#### 응답 예시

```json
{
	"opmr_invsr_trde_chart": [
		{
			"tm": "090000",
			"frgnr_invsr": "0",
			"orgn": "0",
			"invtrt": "0",
			"insrnc": "0",
			"bank": "0",
			"penfnd_etc": "0",
			"etc_corp": "0",
			"natn": "0"
		},
		{
			"tm": "092200",
			"frgnr_invsr": "3",
			"orgn": "0",
			"invtrt": "0",
			"insrnc": "0",
			"bank": "0",
			"penfnd_etc": "0",
			"etc_corp": "0",
			"natn": "0"
		},
		{
			"tm": "095200",
			"frgnr_invsr": "-68",
			"orgn": "0",
			"invtrt": "0",
			"insrnc": "0",
			"bank": "0",
			"penfnd_etc": "0",
			"etc_corp": "0",
			"natn": "0"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식틱차트조회요청 (ka10079)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| tic_scope    | 틱범위       | String | Y        | 2      | 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱                          |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description                                                               |
| --------------------- | -------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                | 종목코드       | String | N        | 6      |                                                                           |
| last_tic_cnt          | 마지막틱갯수   | String | N        |        |                                                                           |
| stk_tic_chart_qry     | 주식틱차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc             | 현재가         | String | N        | 20     |                                                                           |
| - trde_qty            | 거래량         | String | N        | 20     |                                                                           |
| - cntr_tm             | 체결시간       | String | N        | 20     |                                                                           |
| - open_pric           | 시가           | String | N        | 20     |                                                                           |
| - high_pric           | 고가           | String | N        | 20     |                                                                           |
| - low_pric            | 저가           | String | N        | 20     |                                                                           |
| - upd_stkpc_tp        | 수정주가구분   | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt              | 수정비율       | String | N        | 20     |                                                                           |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |                                                                           |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |                                                                           |
| - stk_infr            | 종목정보       | String | N        | 20     |                                                                           |
| - upd_stkpc_event     | 수정주가이벤트 | String | N        | 20     |                                                                           |
| - pred_close_pric     | 전일종가       | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"tic_scope": "1",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"last_tic_cnt": "",
	"stk_tic_chart_qry": [
		{
			"cur_prc": "132500",
			"trde_qty": "1",
			"cntr_tm": "20241106141853",
			"open_pric": "132500",
			"high_pric": "132500",
			"low_pric": "132500",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "132600",
			"trde_qty": "10",
			"cntr_tm": "20241106111111",
			"open_pric": "132600",
			"high_pric": "132600",
			"low_pric": "132600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "132600",
			"trde_qty": "10",
			"cntr_tm": "20241106110519",
			"open_pric": "132600",
			"high_pric": "132600",
			"low_pric": "132600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식분봉차트조회요청 (ka10080)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| tic_scope    | 틱범위       | String | Y        | 2      | 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분 |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description                                                               |
| ------------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                   | 종목코드         | String | N        | 6      |                                                                           |
| stk_min_pole_chart_qry   | 주식분봉차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc                | 현재가           | String | N        | 20     |                                                                           |
| - trde_qty               | 거래량           | String | N        | 20     |                                                                           |
| - cntr_tm                | 체결시간         | String | N        | 20     |                                                                           |
| - open_pric              | 시가             | String | N        | 20     |                                                                           |
| - high_pric              | 고가             | String | N        | 20     |                                                                           |
| - low_pric               | 저가             | String | N        | 20     |                                                                           |
| - upd_stkpc_tp           | 수정주가구분     | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt                 | 수정비율         | String | N        | 20     |                                                                           |
| - bic_inds_tp            | 대업종구분       | String | N        | 20     |                                                                           |
| - sm_inds_tp             | 소업종구분       | String | N        | 20     |                                                                           |
| - stk_infr               | 종목정보         | String | N        | 20     |                                                                           |
| - upd_stkpc_event        | 수정주가이벤트   | String | N        | 20     |                                                                           |
| - pred_close_pric        | 전일종가         | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"tic_scope": "1",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"stk_min_pole_chart_qry": [
		{
			"cur_prc": "-132500",
			"trde_qty": "1",
			"cntr_tm": "20241106141800",
			"open_pric": "-132500",
			"high_pric": "-132500",
			"low_pric": "-132500",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "-132600",
			"trde_qty": "10",
			"cntr_tm": "20241106111100",
			"open_pric": "-132600",
			"high_pric": "-132600",
			"low_pric": "-132600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "-132600",
			"trde_qty": "20",
			"cntr_tm": "20241106110500",
			"open_pric": "133100",
			"high_pric": "133100",
			"low_pric": "-132600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식일봉차트조회요청 (ka10081)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description                                                               |
| ------------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                   | 종목코드         | String | N        | 6      |                                                                           |
| stk_dt_pole_chart_qry    | 주식일봉차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc                | 현재가           | String | N        | 20     |                                                                           |
| - trde_qty               | 거래량           | String | N        | 20     |                                                                           |
| - trde_prica             | 거래대금         | String | N        | 20     |                                                                           |
| - dt                     | 일자             | String | N        | 20     |                                                                           |
| - open_pric              | 시가             | String | N        | 20     |                                                                           |
| - high_pric              | 고가             | String | N        | 20     |                                                                           |
| - low_pric               | 저가             | String | N        | 20     |                                                                           |
| - upd_stkpc_tp           | 수정주가구분     | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt                 | 수정비율         | String | N        | 20     |                                                                           |
| - bic_inds_tp            | 대업종구분       | String | N        | 20     |                                                                           |
| - sm_inds_tp             | 소업종구분       | String | N        | 20     |                                                                           |
| - stk_infr               | 종목정보         | String | N        | 20     |                                                                           |
| - upd_stkpc_event        | 수정주가이벤트   | String | N        | 20     |                                                                           |
| - pred_close_pric        | 전일종가         | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"base_dt": "20241108",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"stk_dt_pole_chart_qry": [
		{
			"cur_prc": "133600",
			"trde_qty": "0",
			"trde_prica": "0",
			"dt": "20241107",
			"open_pric": "133600",
			"high_pric": "133600",
			"low_pric": "133600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "133600",
			"trde_qty": "53",
			"trde_prica": "7",
			"dt": "20241106",
			"open_pric": "134205",
			"high_pric": "134205",
			"low_pric": "133600",
			"upd_stkpc_tp": "",
			"upd_rt": "-1.63",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "134204",
			"trde_qty": "0",
			"trde_prica": "0",
			"dt": "20241105",
			"open_pric": "134204",
			"high_pric": "134204",
			"low_pric": "134204",
			"upd_stkpc_tp": "",
			"upd_rt": "+107.83",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "134204",
			"trde_qty": "0",
			"trde_prica": "0",
			"dt": "20241101",
			"open_pric": "134204",
			"high_pric": "134204",
			"low_pric": "134204",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식주봉차트조회요청 (ka10082)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description                                                               |
| ------------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                   | 종목코드         | String | N        | 6      |                                                                           |
| stk_wk_pole_chart_qry    | 주식주봉차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc                | 현재가           | String | N        | 20     |                                                                           |
| - trde_qty               | 거래량           | String | N        | 20     |                                                                           |
| - trde_prica             | 거래대금         | String | N        | 20     |                                                                           |
| - dt                     | 일자             | String | N        | 20     |                                                                           |
| - open_pric              | 시가             | String | N        | 20     |                                                                           |
| - high_pric              | 고가             | String | N        | 20     |                                                                           |
| - low_pric               | 저가             | String | N        | 20     |                                                                           |
| - upd_stkpc_tp           | 수정주가구분     | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt                 | 수정비율         | String | N        | 20     |                                                                           |
| - bic_inds_tp            | 대업종구분       | String | N        | 20     |                                                                           |
| - sm_inds_tp             | 소업종구분       | String | N        | 20     |                                                                           |
| - stk_infr               | 종목정보         | String | N        | 20     |                                                                           |
| - upd_stkpc_event        | 수정주가이벤트   | String | N        | 20     |                                                                           |
| - pred_close_pric        | 전일종가         | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"base_dt": "20241108",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"stk_wk_pole_chart_qry": [
		{
			"cur_prc": "133600",
			"trde_qty": "53",
			"trde_prica": "7",
			"dt": "20241107",
			"open_pric": "134205",
			"high_pric": "134205",
			"low_pric": "133600",
			"upd_stkpc_tp": "",
			"upd_rt": "-0.45",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "134204",
			"trde_qty": "2694",
			"trde_prica": "361",
			"dt": "20241101",
			"open_pric": "134204",
			"high_pric": "134204",
			"low_pric": "134204",
			"upd_stkpc_tp": "",
			"upd_rt": "+2.45",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "130990",
			"trde_qty": "2694",
			"trde_prica": "361",
			"dt": "20241025",
			"open_pric": "130990",
			"high_pric": "130990",
			"low_pric": "130990",
			"upd_stkpc_tp": "",
			"upd_rt": "-0.83",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식월봉차트조회요청 (ka10083)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description                                                               |
| ------------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                   | 종목코드         | String | N        | 6      |                                                                           |
| stk_mth_pole_chart_qry   | 주식월봉차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc                | 현재가           | String | N        | 20     |                                                                           |
| - trde_qty               | 거래량           | String | N        | 20     |                                                                           |
| - trde_prica             | 거래대금         | String | N        | 20     |                                                                           |
| - dt                     | 일자             | String | N        | 20     |                                                                           |
| - open_pric              | 시가             | String | N        | 20     |                                                                           |
| - high_pric              | 고가             | String | N        | 20     |                                                                           |
| - low_pric               | 저가             | String | N        | 20     |                                                                           |
| - upd_stkpc_tp           | 수정주가구분     | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt                 | 수정비율         | String | N        | 20     |                                                                           |
| - bic_inds_tp            | 대업종구분       | String | N        | 20     |                                                                           |
| - sm_inds_tp             | 소업종구분       | String | N        | 20     |                                                                           |
| - stk_infr               | 종목정보         | String | N        | 20     |                                                                           |
| - upd_stkpc_event        | 수정주가이벤트   | String | N        | 20     |                                                                           |
| - pred_close_pric        | 전일종가         | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"base_dt": "20241108",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"stk_mth_pole_chart_qry": [
		{
			"cur_prc": "127600",
			"trde_qty": "55",
			"trde_prica": "7043700",
			"dt": "20241101",
			"open_pric": "128171",
			"high_pric": "128179",
			"low_pric": "127600",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "128169",
			"trde_qty": "455",
			"trde_prica": "87853100",
			"dt": "20241002",
			"open_pric": "264016",
			"high_pric": "274844",
			"low_pric": "127972",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "264016",
			"trde_qty": "5101",
			"trde_prica": "1354698100",
			"dt": "20240902",
			"open_pric": "265788",
			"high_pric": "269529",
			"low_pric": "188808",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 주식년봉차트조회요청 (ka10094)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| stk_cd       | 종목코드     | String | Y        | 20     | 거래소별 종목코드<br/>(KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |
| upd_stkpc_tp | 수정주가구분 | String | Y        | 1      | 0 or 1                                                         |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                  | 한글명           | Type   | Required | Length | Description                                                               |
| ------------------------ | ---------------- | ------ | -------- | ------ | ------------------------------------------------------------------------- |
| stk_cd                   | 종목코드         | String | N        | 6      |                                                                           |
| stk_yr_pole_chart_qry    | 주식년봉차트조회 | LIST   | N        |        |                                                                           |
| - cur_prc                | 현재가           | String | N        | 20     |                                                                           |
| - trde_qty               | 거래량           | String | N        | 20     |                                                                           |
| - trde_prica             | 거래대금         | String | N        | 20     |                                                                           |
| - dt                     | 일자             | String | N        | 20     |                                                                           |
| - open_pric              | 시가             | String | N        | 20     |                                                                           |
| - high_pric              | 고가             | String | N        | 20     |                                                                           |
| - low_pric               | 저가             | String | N        | 20     |                                                                           |
| - upd_stkpc_tp           | 수정주가구분     | String | N        | 20     | 1:유상증자, 2:무상증자, 4:배당락, 8:액면분할, 16:액면병합, 32:기업합병, 64:감자, 256:권리락 |
| - upd_rt                 | 수정비율         | String | N        | 20     |                                                                           |
| - bic_inds_tp            | 대업종구분       | String | N        | 20     |                                                                           |
| - sm_inds_tp             | 소업종구분       | String | N        | 20     |                                                                           |
| - stk_infr               | 종목정보         | String | N        | 20     |                                                                           |
| - upd_stkpc_event        | 수정주가이벤트   | String | N        | 20     |                                                                           |
| - pred_close_pric        | 전일종가         | String | N        | 20     |                                                                           |

#### 요청 예시

```json
{
	"stk_cd": "005930",
	"base_dt": "20241212",
	"upd_stkpc_tp": "1"
}
```

#### 응답 예시

```json
{
	"stk_cd": "005930",
	"stk_yr_pole_chart_qry": [
		{
			"cur_prc": "11510",
			"trde_qty": "83955682",
			"trde_prica": "1473889778085",
			"dt": "20240102",
			"open_pric": "38950",
			"high_pric": "39100",
			"low_pric": "10500",
			"upd_stkpc_tp": "",
			"upd_rt": "",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "39000",
			"trde_qty": "337617963",
			"trde_prica": "16721059332050",
			"dt": "20230102",
			"open_pric": "20369",
			"high_pric": "93086",
			"low_pric": "20369",
			"upd_stkpc_tp": "1,4,256",
			"upd_rt": "-1.60",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "20221",
			"trde_qty": "284497691",
			"trde_prica": "5829021315600",
			"dt": "20220103",
			"open_pric": "13942",
			"high_pric": "30160",
			"low_pric": "9940",
			"upd_stkpc_tp": "1,2,4,256",
			"upd_rt": "-12.54",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"upd_stkpc_event": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종틱차트조회요청 (ka20004)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| tic_scope    | 틱범위       | String | Y        | 2      | 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱                          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_tic_chart_qry    | 업종틱차트조회 | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - cntr_tm             | 체결시간       | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001",
	"tic_scope": "1"
}
```

#### 응답 예시

```json
{
	"inds_cd": "001",
	"inds_tic_chart_qry": [
		{
			"cur_prc": "239326",
			"trde_qty": "0",
			"cntr_tm": "20241122144300",
			"open_pric": "239326",
			"high_pric": "239326",
			"low_pric": "239326",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "239326",
			"trde_qty": "0",
			"cntr_tm": "20241122144250",
			"open_pric": "239326",
			"high_pric": "239326",
			"low_pric": "239326",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "239326",
			"trde_qty": "0",
			"cntr_tm": "20241122144240",
			"open_pric": "239326",
			"high_pric": "239326",
			"low_pric": "239326",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "239329",
			"trde_qty": "1",
			"cntr_tm": "20241122144230",
			"open_pric": "239329",
			"high_pric": "239329",
			"low_pric": "239329",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "239337",
			"trde_qty": "0",
			"cntr_tm": "20241122144220",
			"open_pric": "239337",
			"high_pric": "239337",
			"low_pric": "239337",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종분봉조회요청 (ka20005)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| tic_scope    | 틱범위       | String | Y        | 2      | 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱                          |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_min_pole_qry     | 업종분봉조회   | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - cntr_tm             | 체결시간       | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001",
	"tic_scope": "5"
}
```

#### 응답 예시

```json
{
	"inds_cd": "001",
	"inds_min_pole_qry": [
		{
			"cur_prc": "-239417",
			"trde_qty": "2",
			"cntr_tm": "20241122144500",
			"open_pric": "+239252",
			"high_pric": "+239417",
			"low_pric": "+239250",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "-239326",
			"trde_qty": "1",
			"cntr_tm": "20241122144000",
			"open_pric": "+239329",
			"high_pric": "+239329",
			"low_pric": "+239326",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "-239116",
			"trde_qty": "5",
			"cntr_tm": "20241122143500",
			"open_pric": "+239405",
			"high_pric": "+239405",
			"low_pric": "+239111",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "-238846",
			"trde_qty": "112",
			"cntr_tm": "20241122143000",
			"open_pric": "+239449",
			"high_pric": "+239449",
			"low_pric": "+238846",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종일봉조회요청 (ka20006)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_dt_pole_qry      | 업종일봉조회   | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - dt                  | 일자           | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - trde_prica          | 거래대금       | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001",
	"base_dt": "20241122"
}
```

#### 응답 예시

```json
{
	"inds_cd": "001",
	"inds_dt_pole_qry": [
		{
			"cur_prc": "239260",
			"trde_qty": "996",
			"dt": "20241122",
			"open_pric": "266953",
			"high_pric": "266953",
			"low_pric": "237521",
			"trde_prica": "46668",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "267296",
			"trde_qty": "444",
			"dt": "20241121",
			"open_pric": "264741",
			"high_pric": "278714",
			"low_pric": "254751",
			"trde_prica": "8961",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "264740",
			"trde_qty": "195",
			"dt": "20241120",
			"open_pric": "256331",
			"high_pric": "279354",
			"low_pric": "256331",
			"trde_prica": "15465",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "256384",
			"trde_qty": "169",
			"dt": "20241119",
			"open_pric": "246075",
			"high_pric": "256424",
			"low_pric": "241051",
			"trde_prica": "7891",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종주봉조회요청 (ka20007)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_stk_pole_qry     | 업종주봉조회   | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - dt                  | 일자           | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - trde_prica          | 거래대금       | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001",
	"base_dt": "20241122"
}
```

#### 응답 예시

```json
{
	"inds_cd": "001",
	"inds_stk_pole_qry": [
		{
			"cur_prc": "238457",
			"trde_qty": "1988",
			"dt": "20241118",
			"open_pric": "244182",
			"high_pric": "279354",
			"low_pric": "237521",
			"trde_prica": "86023",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "248731",
			"trde_qty": "491",
			"dt": "20241111",
			"open_pric": "256115",
			"high_pric": "275840",
			"low_pric": "241690",
			"trde_prica": "31221",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "262459",
			"trde_qty": "2740",
			"dt": "20241105",
			"open_pric": "258897",
			"high_pric": "273980",
			"low_pric": "251876",
			"trde_prica": "199996",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "175851",
			"trde_qty": "1849",
			"dt": "20241028",
			"open_pric": "192710",
			"high_pric": "203154",
			"low_pric": "160807",
			"trde_prica": "93455",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종월봉조회요청 (ka20008)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_mth_pole_qry     | 업종월봉조회   | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - dt                  | 일자           | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - trde_prica          | 거래대금       | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "002",
	"base_dt": "20241122"
}
```

#### 응답 예시

```json
{
	"inds_cd": "002",
	"inds_mth_pole_qry": [
		{
			"cur_prc": "237044",
			"trde_qty": "4586",
			"dt": "20241101",
			"open_pric": "167825",
			"high_pric": "285472",
			"low_pric": "154868",
			"trde_prica": "310647",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "164837",
			"trde_qty": "10944",
			"dt": "20241002",
			"open_pric": "264799",
			"high_pric": "307362",
			"low_pric": "151279",
			"trde_prica": "726698",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "264799",
			"trde_qty": "16025",
			"dt": "20240902",
			"open_pric": "267667",
			"high_pric": "298760",
			"low_pric": "191274",
			"trde_prica": "1212938",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		},
		{
			"cur_prc": "228272",
			"trde_qty": "828829",
			"dt": "20240801",
			"open_pric": "279434",
			"high_pric": "293154",
			"low_pric": "227409",
			"trde_prica": "60578562",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

### 업종년봉조회요청 (ka20019)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com (KRX만 지원가능)
- **URL**: /api/dostk/chart
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element      | 한글명       | Type   | Required | Length | Description                                                    |
| ------------ | ------------ | ------ | -------- | ------ | -------------------------------------------------------------- |
| inds_cd      | 업종코드     | String | Y        | 3      | 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주<br/>101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100<br/>나머지 ※ 업종코드 참고 |
| base_dt      | 기준일자     | String | Y        | 8      | YYYYMMDD                                                       |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element               | 한글명         | Type   | Required | Length | Description |
| --------------------- | -------------- | ------ | -------- | ------ | ----------- |
| inds_cd               | 업종코드       | String | N        | 20     |             |
| inds_yr_pole_qry      | 업종년봉조회   | LIST   | N        |        |             |
| - cur_prc             | 현재가         | String | N        | 20     |             |
| - trde_qty            | 거래량         | String | N        | 20     |             |
| - dt                  | 일자           | String | N        | 20     |             |
| - open_pric           | 시가           | String | N        | 20     |             |
| - high_pric           | 고가           | String | N        | 20     |             |
| - low_pric            | 저가           | String | N        | 20     |             |
| - trde_prica          | 거래대금       | String | N        | 20     |             |
| - bic_inds_tp         | 대업종구분     | String | N        | 20     |             |
| - sm_inds_tp          | 소업종구분     | String | N        | 20     |             |
| - stk_infr            | 종목정보       | String | N        | 20     |             |
| - pred_close_pric     | 전일종가       | String | N        | 20     |             |

#### 요청 예시

```json
{
	"inds_cd": "001",
	"base_dt": "20241122"
}
```

#### 응답 예시

```json
{
	"inds_cd": "001",
	"inds_yr_pole_qry": [
		{
			"cur_prc": "238630",
			"trde_qty": "50610088",
			"dt": "20240313",
			"open_pric": "269471",
			"high_pric": "300191",
			"low_pric": "160807",
			"trde_prica": "1150879139",
			"bic_inds_tp": "",
			"sm_inds_tp": "",
			"stk_infr": "",
			"pred_close_pric": ""
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
``` # 키움증권 API 문서

## 국내주식 REST API

### 테마

#### TR 목록

| TR명 | 코드 | 설명 |
| ---- | ---- | ---- |
| 테마그룹별요청 | ka90001 | 테마 그룹별 정보 조회 |
| 테마구성종목요청 | ka90002 | 테마 구성종목 정보 조회 |

---

### 테마그룹별요청 (ka90001)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/thme
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명         | Type   | Required | Length | Description                                                                             |
| -------------- | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| qry_tp         | 검색구분       | String | Y        | 1      | 0:전체검색, 1:테마검색, 2:종목검색                                                      |
| stk_cd         | 종목코드       | String | N        | 6      | 검색하려는 종목코드                                                                     |
| date_tp        | 날짜구분       | String | Y        | 2      | n일전 (1일 ~ 99일 날짜입력)                                                             |
| thema_nm       | 테마명         | String | N        | 50     | 검색하려는 테마명                                                                       |
| flu_pl_amt_tp  | 등락수익구분   | String | Y        | 1      | 1:상위기간수익률, 2:하위기간수익률, 3:상위등락률, 4:하위등락률                          |
| stex_tp        | 거래소구분     | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                    |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| thema_grp              | 테마그룹별       | LIST   | N        |        |             |
| - thema_grp_cd         | 테마그룹코드     | String | N        | 20     |             |
| - thema_nm             | 테마명           | String | N        | 20     |             |
| - stk_num              | 종목수           | String | N        | 20     |             |
| - flu_sig              | 등락기호         | String | N        | 20     |             |
| - flu_rt               | 등락율           | String | N        | 20     |             |
| - rising_stk_num       | 상승종목수       | String | N        | 20     |             |
| - fall_stk_num         | 하락종목수       | String | N        | 20     |             |
| - dt_prft_rt           | 기간수익률       | String | N        | 20     |             |
| - main_stk             | 주요종목         | String | N        | 20     |             |

#### 요청 예시

```json
{
	"qry_tp": "0",
	"stk_cd": "",
	"date_tp": "10",
	"thema_nm": "",
	"flu_pl_amt_tp": "1",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"thema_grp": [
		{
			"thema_grp_cd": "319",
			"thema_nm": "건강식품",
			"stk_num": "5",
			"flu_sig": "2",
			"flu_rt": "+0.02",
			"rising_stk_num": "1",
			"fall_stk_num": "0",
			"dt_prft_rt": "+157.80",
			"main_stk": "삼성전자"
		},
		{
			"thema_grp_cd": "452",
			"thema_nm": "SNS(Social Network Service)",
			"stk_num": "3",
			"flu_sig": "5",
			"flu_rt": "-0.09",
			"rising_stk_num": "0",
			"fall_stk_num": "1",
			"dt_prft_rt": "+67.60",
			"main_stk": "삼성전자"
		},
		{
			"thema_grp_cd": "553",
			"thema_nm": "반도체_후공정장비",
			"stk_num": "5",
			"flu_sig": "5",
			"flu_rt": "-0.27",
			"rising_stk_num": "0",
			"fall_stk_num": "1",
			"dt_prft_rt": "+56.88",
			"main_stk": "삼성전자"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---

### 테마구성종목요청 (ka90002)

#### 기본 정보

- **Method**: POST
- **운영 도메인**: https://api.kiwoom.com
- **모의투자 도메인**: https://mockapi.kiwoom.com(KRX만 지원가능)
- **URL**: /api/dostk/thme
- **Format**: JSON
- **Content-Type**: application/json;charset=UTF-8

#### 요청 Header

| Element       | 한글명       | Type   | Required | Length | Description                                                                             |
| ------------- | ------------ | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| authorization | 접근토큰     | String | Y        | 1000   | 토큰 지정시 토큰타입("Bearer") 붙혀서 호출<br/>예) Bearer Egicyx...                     |
| cont-yn       | 연속조회여부 | String | N        | 1      | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 cont-yn값 세팅  |
| next-key      | 연속조회키   | String | N        | 50     | 응답 Header의 연속조회여부값이 Y일 경우 다음데이터 요청시 응답 Header의 next-key값 세팅 |
| api-id        | TR명         | String | Y        | 10     |                                                                                         |

#### 요청 Body

| Element        | 한글명         | Type   | Required | Length | Description                                                                             |
| -------------- | -------------- | ------ | -------- | ------ | --------------------------------------------------------------------------------------- |
| date_tp        | 날짜구분       | String | N        | 1      | 1일 ~ 99일 날짜입력                                                                     |
| thema_grp_cd   | 테마그룹코드   | String | Y        | 6      | 테마그룹코드 번호                                                                       |
| stex_tp        | 거래소구분     | String | Y        | 1      | 1:KRX, 2:NXT, 3:통합                                                                    |

#### 응답 Header

| Element  | 한글명       | Type   | Required | Length | Description                         |
| -------- | ------------ | ------ | -------- | ------ | ----------------------------------- |
| cont-yn  | 연속조회여부 | String | N        | 1      | 다음 데이터가 있을시 Y값 전달       |
| next-key | 연속조회키   | String | N        | 50     | 다음 데이터가 있을시 다음 키값 전달 |
| api-id   | TR명         | String | Y        | 10     |                                     |

#### 응답 Body

| Element                | 한글명           | Type   | Required | Length | Description |
| ---------------------- | ---------------- | ------ | -------- | ------ | ----------- |
| flu_rt                 | 등락률           | String | N        | 20     |             |
| dt_prft_rt             | 기간수익률       | String | N        | 20     |             |
| thema_comp_stk         | 테마구성종목     | LIST   | N        |        |             |
| - stk_cd               | 종목코드         | String | N        | 20     |             |
| - stk_nm               | 종목명           | String | N        | 20     |             |
| - cur_prc              | 현재가           | String | N        | 20     |             |
| - flu_sig              | 등락기호         | String | N        | 20     |             |
| - pred_pre             | 전일대비         | String | N        | 20     |             |
| - flu_rt               | 등락율           | String | N        | 20     |             |
| - acc_trde_qty         | 누적거래량       | String | N        | 20     |             |
| - sel_bid              | 매도호가         | String | N        | 20     |             |
| - sel_req              | 매도잔량         | String | N        | 20     |             |
| - buy_bid              | 매수호가         | String | N        | 20     |             |
| - buy_req              | 매수잔량         | String | N        | 20     |             |
| - dt_prft_rt_n         | 기간수익률n      | String | N        | 20     |             |

#### 요청 예시

```json
{
	"date_tp": "2",
	"thema_grp_cd": "100",
	"stex_tp": "1"
}
```

#### 응답 예시

```json
{
	"flu_rt": "0.00",
	"dt_prft_rt": "0.00",
	"thema_comp_stk": [
		{
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"cur_prc": "57800",
			"flu_sig": "3",
			"pred_pre": "0",
			"flu_rt": "0.00",
			"acc_trde_qty": "0",
			"sel_bid": "0",
			"sel_req": "0",
			"buy_bid": "0",
			"buy_req": "0",
			"dt_prft_rt_n": "0.00"
		},
		{
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"cur_prc": "36700",
			"flu_sig": "3",
			"pred_pre": "0",
			"flu_rt": "0.00",
			"acc_trde_qty": "0",
			"sel_bid": "0",
			"sel_req": "0",
			"buy_bid": "0",
			"buy_req": "0",
			"dt_prft_rt_n": "0.00"
		},
		{
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"cur_prc": "17380",
			"flu_sig": "3",
			"pred_pre": "0",
			"flu_rt": "0.00",
			"acc_trde_qty": "0",
			"sel_bid": "0",
			"sel_req": "0",
			"buy_bid": "0",
			"buy_req": "0",
			"dt_prft_rt_n": "0.00"
		},
		{
			"stk_cd": "005930",
			"stk_nm": "삼성전자",
			"cur_prc": "1410",
			"flu_sig": "3",
			"pred_pre": "0",
			"flu_rt": "0.00",
			"acc_trde_qty": "0",
			"sel_bid": "0",
			"sel_req": "0",
			"buy_bid": "1410",
			"buy_req": "1000",
			"dt_prft_rt_n": "0.00"
		}
	],
	"return_code": 0,
	"return_msg": "정상적으로 처리되었습니다"
}
```

---
