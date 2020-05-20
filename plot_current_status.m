clc, clear all, format compact

% Windows
% files = ["F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\fitness.csv",
%          "F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\fitness_avg.csv",
%          "F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data\69\win_percent.csv"];
% Linux

version = "39";
continuous = 0;
refresh_rate = 10; %[s]

% /home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/106/fitness.csv
files = [strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/fitness.csv"),
         strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/win_percent.csv")];
%      /home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/
winners = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/winners.csv");
avg_gen_fit = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/avg_gen_fitness.csv");
max_turns = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/max_turns.csv");
rand_fitness = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/rand_fitness.csv");

first = 1;
while(first | continuous)
    first = 0;
    figure(1)
    clf(1)
    % Fitness AI
    M = csvread(files(1));
    x = M(:,1);
    y = M(:,2);
    M1 = csvread(avg_gen_fit);
    x1 = M1(:,1);
    y1 = M1(:,2);
    subplot(4,1,1)
    hold all
    plot(x,y)
    plot(x1,y1)
    legend("Max", "Avg")
    title("Fitness AI")
    ylabel("Fitness")
    ylim([min(y),1000])

    % Rolling average fitness
    y = movmean(y,10);
    y1 = movmean(y1,10);
    subplot(4,1,2)
    hold all
    plot(x,y)
    plot(x1,y1)
    legend("Max", "Avg")
    title("Fitness rolling average (10 generations) AI")
    ylabel("Fitness")
    ylim([-1000,1000])

    % Fitness Random
    M = csvread(rand_fitness);
    x = M(:,1);
    y = M(:,2);
    y1 = M(:,3);
    subplot(4,1,3)
    hold all
    plot(x,y)
    plot(x,y1)
    legend('max', 'avg')
    title("Fitness Random")
    ylabel("Fitness")
    ylim([min(y),1000])

    % Rolling average fitness
    y = movmean(y,10);
    y1 = movmean(y1,10);
    subplot(4,1,4)
    hold all
    plot(x,y)
    plot(x,y1)
    legend('max', 'avg')
    title("Fitness rolling average (10 generations) Random")
    ylabel("Fitness")
    ylim([-1000,1000])
    
    
    
    figure(2)
    clf(2)
    M = csvread(winners);
    x = M(:,1);
    tie = M(:,2);
    AI = M(:,3);
    p = sum(M(:,4:6),2);
    subplot(3,1,1)
    hold all
    plot(x, tie)
    plot(x,movmean(tie,20))
    title("Ties")
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    subplot(3,1,2)
    hold all
    plot(x, AI)
    plot(x,movmean(AI,20))
    title("AI wins") 
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    
    subplot(3,1,3)
    hold all
    plot(x, p)
    plot(x,movmean(p,20))
    title("Random player wins")
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    
    figure(3)
    clf(3)
        % Win percent
    try
        M = csvread(files(2));
        x = M(:,1);
        y = M(:,2);
%         subplot(3,1,3)
        plot(x,y)
%     title(titles(2)) 
    catch
        a = 0;
    end
    title("Win percentage in 100 games for best individual from every 100th generation")
    ylabel("%")
    xlabel("Generation")
    ylim([0,100])
    
    figure(4)
    clf(4)
    M = csvread(max_turns);
    x = M(:,1);
    y = M(:,2);
    plot(x,y)
    title("Turns per game")
    ylabel("Turns")
    xlabel("Generation")
    if continuous 
        pause(refresh_rate)
    end
end 