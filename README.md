# Stock_Strategy_Backtesting
터틀 전략 및 미네르비니 전략을 이용한 백테스팅 및 추천 시스템

# 📈 주식 전략 백테스팅 및 추천 시스템

## 설명 📋
본 프로젝트는 터틀 트레이딩 전략과 미네르비니 전략을 이용하여 주식을 분석하고, 두 전략에 부합하는 주식을 추천합니다.

## 설치 방법 🛠️
\`\`\`
pip install pandas
pip install datetime
pip install numpy
pip install FinanceDataReader
\`\`\`

## 사용 방법 📝
1. 터미널을 열고, 스크립트가 있는 디렉터리로 이동합니다.
2. \`python 파일명.py\`를 실행합니다.

## 코드 구조 🏗️

### 라이브러리 임포트
- \`pandas, datetime, numpy, FinanceDataReader\`

### 터틀 트레이딩 전략 함수 (\`turtle_trading_strategy\`)
- 지정된 기간 \`N\` 동안의 최고가와 최저가를 계산합니다.
- 매수 및 매도 신호를 생성합니다.

### 미네르비니 전략 함수 (\`minervini_strategy\`)
- 여러 이동 평균과 주가의 상태를 분석하여 전략에 부합하는지를 판단합니다.

### 메인 코드
- KOSPI와 KOSDAQ에서 모든 주식 데이터를 가져옵니다.
- 두 전략에 부합하는 주식을 찾아 CSV 파일로 저장합니다.

## 결과 해설 📊
- \`common_tickers_df\`에는 두 전략에 부합하는 주식 정보가 저장됩니다.
- 이 정보는 'Marketcap'과 'Market' 등으로 정렬되어 CSV 파일에 저장됩니다.

## 개발자 정보 📫
- 이메일: qwer29382938@gmail.com

## 라이선스 📄
이 프로젝트는 MIT 라이선스를 따릅니다.
