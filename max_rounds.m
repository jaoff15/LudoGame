% clc, clear all, format compact
gameId = 1:10000;
maxRounds  = min(160, ceil(gameId / 160.0) * 20);
fig = 3

figure(fig)
clf(fig)
% subplot(2,1,1)
stairs(gameId, maxRounds)
title("Number of turns per game")
xlabel("Game number")
ylabel("Number of turns")

firstFullLengthRound =min(find(maxRounds==max(max(maxRounds))))
xlim([0,firstFullLengthRound ])

% subplot(2,1,2)
% 
% stairs((20:20:160).*8,20:20:160)
% 
% xlim([0,firstFullLengthRound ])