'''
Copyright (C) 2017-2019  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.


Pair generation code for exchanges
'''
import requests

from cryptofeed.defines import BITSTAMP, BITFINEX, COINBASE, GEMINI, HITBTC, POLONIEX, KRAKEN, BINANCE, EXX


def gen_pairs(exchange):
    return _exchange_function_map[exchange]()


def binance_pairs():
    ret = {}
    pairs = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()
    for symbol in pairs['symbols']:
        split = len(symbol['baseAsset'])
        normalized = symbol['symbol'][:split] + '-' + symbol['symbol'][split:]
        ret[normalized] = symbol['symbol']
    return ret


def bitfinex_pairs():
    ret = {}
    r = requests.get('https://api.bitfinex.com/v2/tickers?symbols=ALL').json()
    for data in r:
        pair = data[0]
        if pair[0] == 'f':
            continue
        else:
            normalized = pair[1:-3] + '-' + pair[-3:]
            ret[normalized] = pair
    return ret


def coinbase_pairs():
    r = requests.get('https://api.pro.coinbase.com/products').json()

    return {data['id']: data['id'] for data in r}


def gemini_pairs():
    ret = {}
    r = requests.get('https://api.gemini.com/v1/symbols').json()

    for pair in r:
        std = "{}-{}".format(pair[:-3], pair[-3:])
        std = std.upper()
        ret[std] = pair

    return ret


def hitbtc_pairs():
    ret = {}
    pairs = requests.get('https://api.hitbtc.com/api/2/public/symbol').json()
    for symbol in pairs:
        split = len(symbol['baseCurrency'])
        normalized = symbol['id'][:split] + '-' + symbol['id'][split:]
        ret[normalized] = symbol['id']
    return ret


def poloniex_id_pair_mapping():
    ret = {}
    pairs = requests.get('https://poloniex.com/public?command=returnTicker').json()
    for pair in pairs:
        ret[pairs[pair]['id']] = pair
    return ret


def poloniex_pairs():
    return {value.split("_")[1] + "-" + value.split("_")[0]: value for _, value in poloniex_id_pair_mapping().items()}


def bitstamp_pairs():
    ret = {}
    r = requests.get('https://www.bitstamp.net/api/v2/trading-pairs-info/').json()
    for data in r:
        normalized = data['name'].replace("/", "-")
        pair = data['url_symbol']
        ret[normalized] = pair
    return ret


def kraken_pairs():
    ret = {}
    r = requests.get('https://api.kraken.com/0/public/AssetPairs')
    data = r.json()
    for pair in data['result']:
        alt = data['result'][pair]['altname']
        modifier = -3
        if ".d" in alt:
            modifier = -5
        normalized = alt[:modifier] + '-' + alt[modifier:]
        exch = normalized.replace("-", "/")
        normalized = normalized.replace('XBT', 'BTC')
        normalized = normalized.replace('XDG', 'DOG')
        ret[normalized] = exch
    return ret


def exx_pairs():
    r = requests.get('https://api.exx.com/data/v1/tickers').json()

    exchange = [key.upper() for key in r.keys()]
    pairs = [key.replace("_", "-") for key in exchange]
    return {pair: exchange for pair, exchange in zip(pairs, exchange)}


_exchange_function_map = {
    BITFINEX: bitfinex_pairs,
    COINBASE: coinbase_pairs,
    GEMINI: gemini_pairs,
    HITBTC: hitbtc_pairs,
    POLONIEX: poloniex_pairs,
    BITSTAMP: bitstamp_pairs,
    KRAKEN: kraken_pairs,
    BINANCE: binance_pairs,
    EXX: exx_pairs
}