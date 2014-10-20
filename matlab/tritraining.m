function tritraining(           ...
    access_point_location_file, ...
    training_location_file,     ...
    log_file_info_dir,          ...
    output_dir,                 ...
    num_training,               ...
    num_antenna                 ...
)

access_point = load(access_point_location_file);
training_location = load(training_location_file);
num_ap = size(access_point,1);

% read log_file info
log_file_path = cell(num_training,num_ap);
d = dir(log_file_info_dir);
index = ~[d(:).isdir];
info_file = {d(index).name};

for i=1:num_ap
   
    file = sprintf('%s/%s',log_file_info_dir,info_file{i});
    fid = fopen(file);
    for j=1:num_training
        log_file_path{i,j} = fgetl(fid);
    end
    
end

% get CSI data
data = zeros(num_training, num_antenna, num_ap);
for i=1:num_ap
   
    for j=1:num_training
        
        csi_trace = read_bf_file(log_file_path{i,j});
        num_packets = size(csi_trace,1);
        tmp = zeros(1, num_antenna);
        
        for k=1:num_packets
            
            if(~isstruct(csi_trace{k}))
                break;
            end
            csi = csi_trace{k}.csi ./ sqrt(dbinv(csi_trace{k}.agc));
            ifft_csi = ifft(squeeze(csi).');
            los = max(ifft_csi.*conj(ifft_csi));
            tmp(k,:) = los(csi_trace{k}.perm);
            
        end
         data(j,:,i)= mean(tmp);
    end
    
end

disp(db(data,'pow'));
fit_result = zeros(num_antenna,2,num_ap);
for i=1:num_ap
   
    for j=1:num_antenna
        
        diff_point = training_location(1:num_training,:) - ones(num_training,1)*access_point(i,:);
        dist = zeros(num_training,1);
        
        h = figure('visible','off');
        for k=1:num_training
            dist(k) = norm(diff_point(k,:));
        end
        % find fit function
        fit_result(j,:,i) = polyfit(db(data(:,j,i),'power'),db(dist,'pow'), 1);
        
        % draw fit result in output dir
        y = polyval(fit_result(j,:,i), db(data(:,j,i),'power'));
        plot(db(data(:,j,i),'power'),db(dist,'pow'),'*');
        hold on;
        plot(db(data(:,j,i),'power'), y, 'r');
        hold on;
        grid on;
        xlabel('distance [db]');
        ylabel('power [dbm]');
        
        save_figure_filename = sprintf('%s/ap%d_ant_%d.eps',output_dir,i,j);
        saveas(h,save_figure_filename,'eps');
        clf;
    end
    
end

output_training_filename = sprintf('%s/tritraining.mat',output_dir);
save(output_training_filename, 'fit_result');

