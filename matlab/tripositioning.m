function ret = tripositioning(  ...
    access_point_location_file, ...
    training_result_file,       ...
    input_log_file_list,        ...
    num_antenna                 ...
)

access_point = load(access_point_location_file);
data = load(training_result_file);
fit_result = data.fit_result;
num_ap = size(fit_result,3);

% read input log file

numOfFileNotRecv = num_ap;
data = zeros(num_ap ,num_antenna);
for i=1:num_ap
    
    csi_trace = read_bf_file(input_log_file_list{i});
    if(size(csi_trace,1) == 0)
        numOfFileNotRecv = numOfFileNotRecv -1;
        continue;
    end
    
    num_packets = size(csi_trace,1);
    tmp = zeros(1, num_antenna);
    
    for j=1:num_packets
        
        if(~isstruct(csi_trace{j}))
           break; 
        end
        
        csi = csi_trace{j}.csi ./ sqrt(dbinv(csi_trace{j}.agc));
        ifft_csi = ifft(squeeze(csi)');
        los = max(ifft_csi.*conj(ifft_csi));
        tmp(j,:) = los(csi_trace{j}.perm);
        
    end
    tmp_mean = mean(tmp);
    
    for j=1:num_antenna
        data(i,j) = polyval(fit_result(j,:,i),tmp_mean(j));
    end
    
end

positioning_result = zeros(num_antenna,2);
for i=1:num_antenna
    
    if(numOfFileNotRecv < 3)
        break;
    end
    
    A = zeros(num_ap-1,2);
    b = zeros(num_ap-1,1);
    for j=1:(num_ap-1)   
        A(j,1) = 2*(access_point(j+1,1) - access_point(1,1));
        A(j,2) = 2*(access_point(j+1,2) - access_point(1,2));
        b(j) = data(1,i)^2 - data(j+1,i)^2 + ...
            access_point(j+1,1)^2 + access_point(j+1,2)^2 + ...
            access_point(1,1)^2 + access_point(1,2)^2;
    end
    
    positioning_result(i,:) =((A'*A)\(A'*b))';
    % disp(positioning_result(i,:));
end

if(numOfFileNotRecv > 2)
    ret = mean(positioning_result);
else
    ret = [0,0]; 
end
    
for i=1:num_ap
    delete(input_log_file_list{i})
end



