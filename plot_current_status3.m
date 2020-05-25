clc, clear all, format compact

versions = ["0", "151", "157", "147"];
details = ["(MR=  2%, \sigma^2 =0.15)", "(MR=10%, \sigma^2 =0.15)","(MR=  2%, \sigma^2 =0.4)","(MR=10%, \sigma^2 =0.4)"];
figure(2)
clf(2)

cs = [0     , 0.4470, 0.7410, 0.8500, 0.3250, 0.0980,0.9290, 0.6940, 0.1250,0.4940, 0.1840, 0.5560];
for i = 1:4
    
    version = versions(i);
    files = [strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\LudoVersion2\data/",version,"/fitness.csv");
             strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data/",version,"/fitness.csv");
             strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data/",version,"/fitness.csv");
             strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data/",version,"/fitness.csv")];

    % version = "0";
    continuous = 0;
    fig = i;

    refresh_rate = 10; %[s]

    % /home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/106/fitness.csv
    % fitness_file = strcat("/home/jacoboffersen/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/",version,"/fitness.csv")
    % fitness_file = strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\Ludo64bitVersion\data/",version,"/fitness.csv")
    % fitness_file = strcat("F:\Dropbox\3rd Semester Master\Tools of Artificial Intelligence\LudoGame\LudoVersion2\data/",version,"/fitness.csv")
    fitness_file = files(i);

%     first = 1;
%     subplot(2,2,fig)
%     while(first | continuous)
%         first = 0;
        
    %     subplot(2,1,1)
        hold all
        % Fitness AI
        M = csvread(fitness_file);
        x  = M(:,1);
        y1 = M(:,2)*100;
        y2 = M(:,3)*100;
        y3 = M(:,4)*100;
        hold all
%         c = [0, 0.4470, 0.7410];
        c = cs((i-1)*3+1:i*3)
%         scatter(x,y1,20, c, 'HandleVisibility','off')
        y1m = movmean(y1,10);
        p = plot(x,y1m,'LineWidth',2);
        p.Color = c;

%         c = [0.8500, 0.3250, 0.0980];
%         scatter(x,y2,20, c, 'HandleVisibility','off')
        y2m = movmean(y2,10);
        p = plot(x,y2m,'--','LineWidth',2);
        p.Color = c;
        
    %     c =[0.9290, 0.6940, 0.1250];
    %     scatter(x,y3,20, c, 'HandleVisibility','off')
    %     y3 = movmean(y3,10);
    %     plot(x,y3,'MarkerFaceColor',c,'LineWidth',2)

    %     legend("Max", "Avg", "Min")
        legend(strcat("Max", details(i)), strcat("Avg", details(i)))
    %     legend("Max")
        title(strcat("AI win percent of 100 games with different MR and \sigma"))
        ylabel("Wins [%]")
        xlabel("Generation")
    %     ylim([min([min(y1),min(y2), min(y3)]),max([max(y1),max(y2), max(y3)])+1])
        ylim([min([min(y1),min(y2)]),max([max(y1),max(y2)])+1])
        grid on

        display(strcat(num2str(i), " max: ", num2str(max(y1)),"%, ", num2str(max(y1m)),"%"))
        display(strcat(num2str(i), " avg: ", num2str(max(y2)),"%, ", num2str(max(y2m)),"%"))
        display("")

        xlim([0,120])

%         if continuous 
%             pause(refresh_rate)
%         end
%     end 
end 
% legend( strcat("Max", details(1)), strcat("Max", details(2)),strcat("Max", details(3)), strcat("Max", details(4)),strcat("Avg", details(1)), strcat("Avg", details(2)), strcat("Avg", details(3)),  strcat("Avg", details(4)))
legend( strcat("Max", details(1)), strcat("Avg", details(1)), strcat("Max", details(2)), strcat("Avg", details(2)),strcat("Max", details(3)), strcat("Avg", details(3)), strcat("Max", details(4)), strcat("Avg", details(4)))











