clear all;
close all;

num_ap = 4;
room_width = 577;
room_height = 647;

while 1
    
    d = dir('../tmp/');
    index = ~[d(:).isdir];
    file_list = {d(index).name};
    num_file = size(file_list,2);
    
    while(num_file ~= num_ap)
        d = dir('../tmp/');
        index = ~[d(:).isdir];
        file_list = {d(index).name};
        num_file = size(file_list,2);
    end
    
    for i=1:num_file
        fileName = sprintf('../tmp/%s',file_list{i});
        file_list{i} = fileName;
    end
    
    result = tripositioning( ...
        '/home/chang-ning/linux-80211n-csitool-supplementary/log_file/APL.dat', ...
        '/home/chang-ning/linux-80211n-csitool-supplementary/log_file/output/tritraining.mat', ...
        file_list, 3);
    
    % show result on the map
    map = imread('lab.jpg');
    if(result(1,1)<12)
        result(1,1) = 12; 
    elseif(result(1,1)>room_height-12)
        result(1,1) = room_height-12;
    end
    
    if(result(1,2)<12)
        result(1,2) = 12;
    elseif(result(1,2)>room_width-12)
        result(1,2) = room_height-12;
    end
    
    map(result(1,1)-11:result(1,1)+11 , ...
        result(1,2)-11:result(1,2)+11, ...
        1) = 255;
    
    map(result(1,1)-11:result(1,1)+11 , ...
        result(1,2)-11:result(1,2)+11, ...
        2) = 0;
    
    map(result(1,1)-11:result(1,1)+11 , ...
        result(1,2)-11:result(1,2)+11, ...
        3) = 0;
    imshow(map);
    pause(0.5);
    
    fprintf('estimate position\n');
    disp(result);

end