import pandas as pd
import datetime
import numpy as np
import FinanceDataReader as fdr
import concurrent.futures

# 거북이 트레이딩 전략 함수
def turtle_trading_strategy(data, N=20):
    data['High_N'] = data['High'].rolling(window=N).max()
    data['Low_N'] = data['Low'].rolling(window=N).min()
    data['Buy_Signal'] = np.where(data['Close'] > data['High_N'].shift(1), 1, 0)
    data['Sell_Signal'] = np.where(data['Close'] < data['Low_N'].shift(1), -1, 0)
    data['Position'] = data['Buy_Signal'] + data['Sell_Signal']
    return data['Position'].iloc[-1]

# 미네르비니 전략 함수
def minervini_strategy(data):
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA150'] = data['Close'].rolling(window=150).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()
    conditions = [
        (data['Close'] > data['MA150']) & (data['Close'] > data['MA200']),
        data['MA150'] > data['MA200'],
        data['MA200'] > data['MA200'].shift(21),
        (data['MA50'] > data['MA150']) & (data['MA50'] > data['MA200']),
        data['Close'] > data['MA50'],
        data['Close'] > (data['Low'].rolling(window=252).min() * 1.3),
        data['Close'] >= (data['High'].rolling(window=252).max() * 0.75),
        100 - (100 / (1 + (data['Close'].diff().where(lambda x: x > 0, 0).rolling(window=14).mean() /
                        -data['Close'].diff().where(lambda x: x < 0, 0).rolling(window=14).mean()))) >= 70
    ]
    return all(cond.iloc[-1] for cond in conditions)

# 종목 테스트 함수 (병렬 처리 대상)
def test_strategy(ticker, all_stocks):
    data = fdr.DataReader(ticker, start="2022-01-01")
    result = {
        'Ticker': ticker,
        'Name': all_stocks.loc[ticker, 'Name'],
        'Marketcap': all_stocks.loc[ticker, 'Marcap'],
        'Market': all_stocks.loc[ticker, 'Market']
    }
    if turtle_trading_strategy(data) == 1 and minervini_strategy(data):
        return result
    return None

# 메인 실행 부분
if __name__ == "__main__":
    all_stocks = pd.concat([fdr.StockListing('KOSPI'), fdr.StockListing('KOSDAQ')]).set_index('Code')
    common_tickers = []
    start_time = datetime.datetime.now()  # 시작 시간 기록

    # 병렬 처리로 각 종목 테스트
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(test_strategy, all_stocks.index, [all_stocks]*len(all_stocks.index)))

    # 결과 처리
    for result in results:
        if result is not None:
            common_tickers.append(result)

    common_tickers_df = pd.DataFrame(common_tickers)
    common_tickers_df = common_tickers_df.sort_values(by='Marketcap', ascending=False)
    common_tickers_df['Marketcap'] = (common_tickers_df['Marketcap'] / 10**8).round().astype(int).astype(str) + '억'
    common_tickers_df['Market'] = common_tickers_df['Market'].replace({'KOSPI': '코스피', 'KOSDAQ': '코스닥', 'KOSDAQ GLOBAL': '코스닥'})
    
    end_time = datetime.datetime.now()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 경과 시간 계산
    current_date_str = datetime.datetime.now().strftime('%m-%d')
    filename = f"TurtleMinervini_{current_date_str}.csv"

    common_tickers_df.to_csv(filename, index=False)

    print(f"백테스트에 걸린 시간: {elapsed_time}")
