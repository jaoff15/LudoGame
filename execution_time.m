clc, clear all, format compact

% maxRounds = ones(1,10) * 100;
maxRounds = 10:10:100;
population = 100;
generationsPerStep = 1000;
FFtimePerRoundPerIndiv = 1/1000; %[s]

totalTimeSec = 0;
for r = maxRounds
    timePerGen = (FFtimePerRoundPerIndiv * r * population);
    totalTimeSec = totalTimeSec + timePerGen * generationsPerStep
end
totalTimeSec
totalTimeMin = totalTimeSec/60
totalTimeHours = totalTimeMin/60
totalTimeDays = totalTimeHours/24