clc, clear all, format compact
gameId = 1:10000;
maxRounds  = min(100, round(ceil(gameId / 1000.0)) * 10);

plot(gameId, maxRounds)