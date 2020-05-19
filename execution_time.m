clc, clear all, format compact

% maxRounds = ones(1,10) * 100;
maxRounds = 20:20:160;
population = 100;
generationsPerStep = 1000;
FFtimePerRoundPerIndiv = 0.7/1000; %[s]

totalTimeSec = 0;
for r = maxRounds
    timePerGen = (FFtimePerRoundPerIndiv * r * population);
    totalTimeSec = totalTimeSec + timePerGen * generationsPerStep;
end
totalTimeSec
totalTimeMin = totalTimeSec/60
totalTimeHours = totalTimeMin/60
totalTimeDays = totalTimeHours/24